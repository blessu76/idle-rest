#!/usr/bin/env python3
"""Unattended journal publisher for idle.ipe.rest — stdlib only (Python 3.8+).

Takes ONE ready-made entry (ko + en) from a stock queue that lives OUTSIDE the repo, stamps today's date and the real
publish time (KST), then build -> --check -> check_sitemap -> unittest -> commit -> push -> live 200, back to back.
Nothing is ever back-dated: the date is today (KST) and `time:` is the minute of the push (re-stamped right before it).

  python3 scripts/publish_next.py              # normal tick (launchd runs this every 5 min; nothing due -> exits quietly)
  python3 scripts/publish_next.py --dry-run    # everything except the real push and the queue move (git push --dry-run)
  python3 scripts/publish_next.py --status     # queue stock + today's schedule, touches nothing
  python3 scripts/publish_next.py --force      # ignore the slot times (still never inside a forbidden window / 2 per day)

Queue (default ~/.ipe/queue/idle, outside the repo so unpublished drafts never reach the public GitHub repo):
  <queue>/<NN-anything>/en.md     front matter + body; `date:` and `time:` are overwritten at publish time
  <queue>/<NN-anything>/ko.md     same slug; en has `translation_of: ko`
Folders go out in name order. A published folder moves to <queue>/.published/. Queue empty when something is due ->
NO push, STOCK_ALERT file + macOS notification, exit 3. Fewer than --min-stock left -> same warning, once a day.

Rhythm (see SLOT constants): 2 per day. First slot = MORNING_START + a stable per-day random minute offset; second slot = actual
first publish + 4 h (+ small random minutes). Davy's original morning window was 10:00-10:59, but pushes are forbidden 10:00-11:00 and
13:00-14:30 KST (web push guard), so the morning slot starts at 11:00. Change the constants if that rule changes.

Guards: lock · FAILED file stops everything until a human deletes it · dedicated clone = origin/main exactly · no deleted files ·
only allow-listed paths staged · no leftovers · push must fast-forward (otherwise soft retry from a clean clone, 3 in a row -> SOFT_ALERT).
State dir: --base (default ~/.ipe/idle-publish): repo/ lock/ FAILED SOFT_ALERT STOCK_ALERT.
Test knobs: --now ISO · --remote · --base · --queue · --no-verify · IDLE_PUBLISH_NO_NOTIFY=1.
"""
import argparse
import datetime as dt
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

KST = dt.timezone(dt.timedelta(hours=9))
MORNING_START = dt.time(11, 0)          # first slot opens here (10:00-11:00 is a forbidden push window)
MORNING_SPREAD_MIN = 120                # + stable random 0..119 min -> 11:00-12:59
AFTERNOON_GAP = dt.timedelta(hours=4)   # second slot = actual first publish + 4 h
AFTERNOON_SPREAD_MIN = 15               # + stable random 0..14 min
FORBIDDEN = [(dt.time(10, 0), dt.time(11, 0)), (dt.time(13, 0), dt.time(14, 30))]  # [start, end) KST — never push inside
MAX_PER_DAY = 2
MIN_STOCK = 3
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
MAIN_LANGS = ("en", "ko")
# the only paths a publish may touch (everything else staged = hard fail)
ALLOWED_PATH = re.compile(
    r"^(journal/|content/journal/(en|ko)/[a-z0-9-]+\.md$|sitemap\.xml$|llms\.txt$|sw\.js$|index\.html$|[a-z]{2}/index\.html$)")
DEFAULT_REMOTE = "https://github.com/blessu76/idle-rest.git"
DEFAULT_LIVE = "https://idle.ipe.rest"


class HardFail(Exception):
    """bad manuscript / check red / guard tripped — stop until a human removes FAILED."""


class SoftFail(Exception):
    """network, non-ff push, or a forbidden window reached mid-run — retried next tick from a clean clone."""


# ---------------------------------------------------------------- pure helpers

def to_kst(now):
    if now.tzinfo is None:
        raise ValueError("now must carry a UTC offset: %r" % now)
    return now.astimezone(KST)


def in_forbidden(t):
    """t: datetime.time (KST). True when a push would land in a forbidden window."""
    return any(a <= t < b for a, b in FORBIDDEN)


def next_allowed(moment):
    """first instant >= moment (aware KST datetime) that is outside every forbidden window."""
    changed = True
    while changed:
        changed = False
        for a, b in FORBIDDEN:
            if a <= moment.timetz().replace(tzinfo=None) < b:
                moment = dt.datetime.combine(moment.date(), b, tzinfo=KST)
                changed = True
    return moment


def jitter(tag, day, spread):
    """stable per-day pseudo-random integer in [0, spread) — the same on every tick of that day."""
    h = hashlib.sha256(("%s|%s" % (tag, day.isoformat())).encode()).hexdigest()
    return int(h[:8], 16) % spread


def morning_target(day):
    base = dt.datetime.combine(day, MORNING_START, tzinfo=KST)
    return next_allowed(base + dt.timedelta(minutes=jitter("morning", day, MORNING_SPREAD_MIN)))


def afternoon_target(day, first_time):
    first = dt.datetime.combine(day, first_time, tzinfo=KST)
    return next_allowed(first + AFTERNOON_GAP + dt.timedelta(minutes=jitter("afternoon", day, AFTERNOON_SPREAD_MIN)))


def decide(now, today_times, force=False):
    """-> (due: bool, reason: str). today_times = sorted datetime.time of posts already published today (KST)."""
    now = to_kst(now)
    n = len(today_times)
    if n >= MAX_PER_DAY:
        return False, "daily limit reached (%d published today)" % n
    if in_forbidden(now.timetz().replace(tzinfo=None)):
        return False, "inside a forbidden push window (%s KST)" % now.strftime("%H:%M")
    target = morning_target(now.date()) if n == 0 else afternoon_target(now.date(), today_times[-1])
    if target.date() != now.date():
        return False, "next slot would be tomorrow (%s)" % target.strftime("%m-%d %H:%M")
    label = "morning slot" if n == 0 else "afternoon slot"
    if force:
        return True, "forced (%s was %s)" % (label, target.strftime("%H:%M"))
    if now >= target:
        return True, "%s due since %s" % (label, target.strftime("%H:%M"))
    return False, "%s opens at %s" % (label, target.strftime("%H:%M"))


def split_front(text):
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise HardFail("missing front matter (file must start with ---)")
    end = text.find("\n---", 4)
    if end == -1:
        raise HardFail("front matter is not closed with ---")
    return text[4:end], text[end:]


def front_meta(text):
    head, _ = split_front(text)
    meta = {}
    for line in head.split("\n"):
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        meta[k.strip().lower()] = v
    return meta


def stamp(text, day, hm):
    """set `date:` and `time:` in the front matter (time goes right after date, replacing any old one). Nothing else changes."""
    head, rest = split_front(text)
    out, seen_date = [], False
    for line in head.split("\n"):
        key = line.split(":", 1)[0].strip().lower() if ":" in line and not line.startswith((" ", "#")) else ""
        if key == "date":
            if seen_date:
                raise HardFail("duplicate date: line")
            seen_date = True
            out += ["date: %s" % day.isoformat(), 'time: "%s"' % hm]
        elif key != "time":
            out.append(line)
    if not seen_date:
        raise HardFail("front matter has no date: line")
    return "---\n" + "\n".join(out) + rest


def today_published_times(repo, day):
    """sorted times of en posts in the repo dated `day` (published = non-draft)."""
    times = []
    d = Path(repo) / "content" / "journal" / "en"
    for f in sorted(d.glob("*.md")) if d.is_dir() else []:
        if f.name.lower() == "readme.md":
            continue
        try:
            m = front_meta(f.read_text(encoding="utf-8"))
        except HardFail:
            continue
        if m.get("date") == day.isoformat() and m.get("draft", "false").lower() not in ("true", "yes", "1"):
            hm = m.get("time", "00:00")
            try:
                times.append(dt.time.fromisoformat(hm))
            except ValueError:
                times.append(dt.time(0, 0))
    return sorted(times)


def queue_items(queue):
    q = Path(queue)
    if not q.is_dir():
        return []
    return sorted(p for p in q.iterdir() if p.is_dir() and not p.name.startswith("."))


def load_item(folder):
    """validate one queue folder -> {'slug','title','en','ko'} (texts). HardFail on anything off."""
    folder = Path(folder)
    texts, metas = {}, {}
    for lang in MAIN_LANGS:
        f = folder / (lang + ".md")
        if not f.is_file():
            raise HardFail("%s: %s.md is missing" % (folder.name, lang))
        texts[lang] = f.read_text(encoding="utf-8")
        metas[lang] = front_meta(texts[lang])
        m = metas[lang]
        for k in ("title", "slug", "lang", "description", "category"):
            if not m.get(k):
                raise HardFail("%s/%s.md: front matter `%s` is missing" % (folder.name, lang, k))
        if m["lang"] != lang:
            raise HardFail("%s/%s.md: lang is %r" % (folder.name, lang, m["lang"]))
        if m.get("draft", "false").lower() in ("true", "yes", "1"):
            raise HardFail("%s/%s.md: draft: true — a queued entry must be ready" % (folder.name, lang))
    slug = metas["en"]["slug"]
    if metas["ko"]["slug"] != slug:
        raise HardFail("%s: en and ko slugs differ" % folder.name)
    if not SLUG_RE.match(slug) or slug in ("feed", "page"):
        raise HardFail("%s: bad slug %r" % (folder.name, slug))
    if metas["en"].get("translation_of") != "ko":
        raise HardFail("%s/en.md: `translation_of: ko` is required" % folder.name)
    return {"slug": slug, "title": metas["en"]["title"], "en": texts["en"], "ko": texts["ko"], "folder": folder}


def check_staged(name_status, untracked_or_unstaged=""):
    """name_status = `git diff --cached --name-status` text. Raises HardFail on a deletion / foreign path / leftovers."""
    dels, bad = [], []
    for line in name_status.splitlines():
        parts = line.split("\t")
        if not parts or not parts[0]:
            continue
        if parts[0].startswith("D"):
            dels.append(parts[-1])
        for p in parts[1:]:
            if not ALLOWED_PATH.match(p):
                bad.append(p)
    if dels:
        raise HardFail("deletions staged (never pushed): " + " ".join(dels))
    if bad:
        raise HardFail("unexpected paths staged: " + " ".join(bad))
    if untracked_or_unstaged.strip():
        raise HardFail("unstaged/untracked leftovers: " + " ".join(untracked_or_unstaged.split())[:200])


def bump_sw(text):
    m = re.search(r"const CACHE = 'idle-v(\d+)';", text)
    if not m:
        raise HardFail("sw.js: CACHE = 'idle-vNN' not found")
    return text[:m.start()] + "const CACHE = 'idle-v%d';" % (int(m.group(1)) + 1) + text[m.end():]


# ---------------------------------------------------------------- publisher

class Publisher:
    def __init__(self, base, queue, remote, live, now_fn=None, dry_run=False, force=False, verify=True,
                 min_stock=MIN_STOCK, build_cmds=None, check_cmds=None, test_cmds=None, branch="main", log=print):
        self.base, self.queue, self.remote, self.live = Path(base), Path(queue), remote, live
        self.clone = self.base / "repo"
        self.now_fn = now_fn or (lambda: dt.datetime.now(KST))
        self.dry, self.force, self.verify, self.min_stock, self.branch = dry_run, force, verify, min_stock, branch
        py = sys.executable or "python3"
        self.build_cmds = [[py, "scripts/build_journal.py"]] if build_cmds is None else build_cmds
        self.check_cmds = [[py, "scripts/build_journal.py", "--check"], [py, "scripts/check_sitemap.py"]] if check_cmds is None else check_cmds
        self.test_cmds = [[py, "-m", "unittest", "discover", "-s", "tests"]] if test_cmds is None else test_cmds
        self.log = log

    # -- utils
    def now(self):
        return to_kst(self.now_fn())

    def say(self, msg):
        self.log("[%s] %s" % (self.now().strftime("%Y-%m-%d %H:%M:%S KST"), msg))

    def notify(self, msg):
        self.say("NOTIFY: " + msg)
        if os.environ.get("IDLE_PUBLISH_NO_NOTIFY") == "1":
            return
        try:
            subprocess.run(["osascript", "-e", 'display notification "%s" with title "idle publish"' % msg.replace('"', "'")],
                           capture_output=True, timeout=10)
        except Exception:  # noqa: BLE001 — a notification must never break the run
            pass

    def run(self, cmd, cwd=None, check=True, timeout=900):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")  # no __pycache__ in the clone (it would trip the leftovers guard)
        r = subprocess.run(cmd, cwd=str(cwd or self.clone), capture_output=True, text=True, timeout=timeout, env=env)
        if check and r.returncode != 0:
            raise subprocess.CalledProcessError(r.returncode, cmd, r.stdout, r.stderr)
        return r

    def git(self, *args, check=True):
        return self.run(["git"] + list(args), check=check)

    def tail(self, e):
        return " ".join(((getattr(e, "stderr", "") or "") + (getattr(e, "stdout", "") or "")).split())[-300:]

    # -- state files
    def f(self, name):
        return self.base / name

    def write_flag(self, name, *lines):
        self.f(name).write_text("\n".join((self.now().isoformat(),) + lines) + "\n", encoding="utf-8")

    # -- stock
    def check_stock(self, n):
        """warn when the queue runs low — at most one notification per day per level."""
        if n >= self.min_stock:
            self.f("STOCK_ALERT").unlink(missing_ok=True)
            return
        level = "EMPTY" if n == 0 else "LOW"
        marker = "%s %s" % (self.now().date().isoformat(), level)
        flag = self.f("STOCK_ALERT")
        prev = flag.read_text(encoding="utf-8").splitlines()[1:2] if flag.exists() else []
        msg = "queue %s: %d entr%s left (min %d) — write more ko+en entries into %s" % (level, n, "y" if n == 1 else "ies", self.min_stock, self.queue)
        if prev != [marker]:
            self.write_flag("STOCK_ALERT", marker, msg)
            self.notify(msg)
        else:
            self.say("stock: " + msg)

    # -- repo
    def sync_clone(self):
        self.base.mkdir(parents=True, exist_ok=True)
        if not (self.clone / ".git").is_dir():
            try:
                subprocess.run(["git", "clone", "--quiet", self.remote, str(self.clone)], check=True, capture_output=True, text=True, timeout=300)
            except subprocess.CalledProcessError as e:
                raise SoftFail("clone failed: " + self.tail(e))
        try:
            self.git("remote", "set-url", "origin", self.remote)
            self.git("fetch", "--quiet", "origin", self.branch)
            self.git("checkout", "--quiet", "-B", self.branch, "origin/" + self.branch)
            self.git("reset", "--hard", "--quiet", "origin/" + self.branch)
            self.git("clean", "-fdq")
        except subprocess.CalledProcessError as e:
            raise SoftFail("git sync failed: " + self.tail(e))

    def reset_clone(self):
        if (self.clone / ".git").is_dir():
            self.run(["git", "reset", "--hard", "--quiet", "origin/" + self.branch], check=False)
            self.run(["git", "clean", "-fdq"], check=False)

    # -- publish steps
    def stage_item(self, item, day, hm):
        for lang in MAIN_LANGS:
            dest = self.clone / "content" / "journal" / lang / (item["slug"] + ".md")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(stamp(item[lang], day, hm), encoding="utf-8")

    def steps(self, cmds, what):
        for cmd in cmds:
            try:
                self.run(cmd)
            except subprocess.CalledProcessError as e:
                raise HardFail("%s red (%s): %s" % (what, " ".join(cmd[1:3]), self.tail(e)))
            except subprocess.TimeoutExpired:
                raise HardFail("%s timed out: %s" % (what, " ".join(cmd)))

    def build_and_bump(self, first):
        self.steps(self.build_cmds, "build")
        if first:
            sw = self.clone / "sw.js"
            sw.write_text(bump_sw(sw.read_text(encoding="utf-8")), encoding="utf-8")

    def self_heal(self, items):
        """a folder whose slug is already published (push went through, move did not) goes to .published/ — same title only."""
        out = []
        for folder in items:
            item = load_item(folder)
            pub = self.clone / "content" / "journal" / "en" / (item["slug"] + ".md")
            if pub.exists():
                if front_meta(pub.read_text(encoding="utf-8")).get("title") == item["title"]:
                    self.say("queue: %s already published — moving to .published/" % folder.name)
                    if not self.dry:
                        self.move_published(folder)
                    continue
                raise HardFail("slug %r already exists in the repo with a different title (queue folder %s)" % (item["slug"], folder.name))
            out.append(item)
        return out

    def move_published(self, folder):
        dest = self.queue / ".published"
        dest.mkdir(parents=True, exist_ok=True)
        target = dest / folder.name
        if target.exists():
            target = dest / ("%s.%d" % (folder.name, int(time.time())))
        shutil.move(str(folder), str(target))

    def publish(self, item, day, hm):
        self.stage_item(item, day, hm)
        self.build_and_bump(first=True)
        self.steps(self.check_cmds, "check")
        self.steps(self.test_cmds, "tests")
        # tests take a while: re-stamp to the real minute right before commit (rebuild is deterministic + fast)
        for _ in range(3):
            n = self.now()
            if in_forbidden(n.timetz().replace(tzinfo=None)):
                raise SoftFail("reached a forbidden push window while verifying (%s)" % n.strftime("%H:%M"))
            if n.date() != day:
                raise SoftFail("date changed while verifying (midnight) — retry next tick")
            nhm = n.strftime("%H:%M")
            if nhm == hm:
                break
            hm = nhm
            self.stage_item(item, day, hm)
            self.build_and_bump(first=False)
            self.steps(self.check_cmds, "check")
        else:
            raise SoftFail("could not settle the publish minute")
        self.git("add", "-A")
        names = self.git("diff", "--cached", "--name-status").stdout
        left = "\n".join(l for l in self.git("status", "--porcelain").stdout.splitlines() if not re.match(r"^[AM] ", l))
        check_staged(names, left)
        added = [l.split("\t")[-1] for l in names.splitlines() if l.startswith("A")]
        for lang in MAIN_LANGS:
            if "content/journal/%s/%s.md" % (lang, item["slug"]) not in added:
                raise HardFail("expected new file content/journal/%s/%s.md was not staged" % (lang, item["slug"]))
        if not names.strip():
            raise HardFail("publish produced no diff")
        return hm

    def commit_and_push(self, item, day, hm):
        cfg = []
        for k, v in (("user.name", "ipe() idle publisher"), ("user.email", "noreply@ipe.rest")):
            if not self.git("config", k, check=False).stdout.strip():
                cfg += ["-c", "%s=%s" % (k, v)]
        msg = "journal: %s (en+ko) — %s auto publish %s KST" % (item["slug"], day.isoformat(), hm)
        body = "Unattended publish (scripts/publish_next.py). date = today KST, time = push minute; never back-dated."
        self.git(*cfg, "commit", "--quiet", "-m", msg, "-m", body)
        sha = self.git("rev-parse", "--short", "HEAD").stdout.strip()
        n = self.now()
        if in_forbidden(n.timetz().replace(tzinfo=None)):
            raise SoftFail("forbidden push window right before push (%s)" % n.strftime("%H:%M"))
        if self.dry:
            r = self.git("push", "--dry-run", "origin", "HEAD:" + self.branch, check=False)
            self.say("DRY RUN: would push %s (%s) rc=%d" % (sha, item["slug"], r.returncode))
            if r.returncode != 0:
                raise SoftFail("dry-run push failed: " + self.tail(r))
            self.say("diffstat: " + self.git("diff", "HEAD~1", "--shortstat").stdout.strip())
            return sha
        try:
            self.git("push", "--quiet", "origin", "HEAD:" + self.branch)
        except subprocess.CalledProcessError as e:
            raise SoftFail("git push failed/rejected: " + self.tail(e))
        self.say("PUSHED %s: %s (%s KST)" % (sha, item["slug"], hm))
        return sha

    def verify_live(self, slug):
        """soft: wait for the Pages deploy, then en+ko 200 and check_sitemap --live. Never fails the run."""
        ok_all = True
        for lang in MAIN_LANGS:
            url = "%s/journal/%s/%s/" % (self.live.rstrip("/"), lang, slug)
            ok = False
            for _ in range(24):  # ~12 min
                try:
                    with urllib.request.urlopen(url + "?v=%d" % time.time(), timeout=20) as r:
                        ok = r.status == 200
                except Exception:  # noqa: BLE001
                    ok = False
                if ok:
                    break
                time.sleep(30)
            self.say("live %s: %s" % ("OK" if ok else "NOT 200", url))
            ok_all &= ok
        if ok_all:
            r = self.run([sys.executable or "python3", "scripts/check_sitemap.py", "--live"], check=False)
            ok_all = r.returncode == 0
            self.say("check_sitemap --live: " + ("OK" if ok_all else "FAILED " + self.tail(r)))
        if not ok_all:
            self.write_flag("LIVE_CHECK_FAILED", slug)
            self.notify("live check failed for %s — look at the site" % slug)
        else:
            self.f("LIVE_CHECK_FAILED").unlink(missing_ok=True)
        return ok_all

    # -- one tick
    def tick(self):
        """returns exit code: 0 ok/nothing due · 1 failed · 3 queue empty while something was due."""
        self.base.mkdir(parents=True, exist_ok=True)
        if self.f("FAILED").exists() and not self.dry:
            self.say("FAILED file present — waiting for a human (%s)" % self.f("FAILED"))
            return 0
        try:
            self.sync_clone()
            now = self.now()
            day = now.date()
            times = today_published_times(self.clone, day)
            due, why = decide(now, times, self.force)
            items = queue_items(self.queue)
            self.check_stock(len(items))
            if not due:
                self.say("nothing due: " + why)
                self.f("SOFT_FAILS").unlink(missing_ok=True)
                return 0
            self.say("due: " + why)
            valid = self.self_heal(items)
            if not valid:
                self.say("queue EMPTY while a slot was due — nothing pushed (STOCK_ALERT written by the stock check)")
                return 3
            item = valid[0]
            self.say("publishing %s (%s)" % (item["slug"], item["folder"].name))
            hm = self.publish(item, day, now.strftime("%H:%M"))
            sha = self.commit_and_push(item, day, hm)
            if self.dry:
                self.reset_clone()
                return 0
            self.move_published(item["folder"])
            self.f("SOFT_FAILS").unlink(missing_ok=True)
            self.f("SOFT_ALERT").unlink(missing_ok=True)
            self.check_stock(len(valid) - 1)
            if self.verify:
                self.verify_live(item["slug"])
            return 0
        except HardFail as e:
            self.say("HARD FAIL: %s" % e)
            self.reset_clone()
            if not self.dry:
                self.write_flag("FAILED", str(e))
            self.notify("FAILED: %s" % str(e)[:150])
            return 1
        except SoftFail as e:
            self.reset_clone()
            n = int((self.f("SOFT_FAILS").read_text().strip() if self.f("SOFT_FAILS").exists() else "0") or 0) + 1
            self.f("SOFT_FAILS").write_text(str(n))
            self.say("soft fail #%d: %s (retry next tick)" % (n, e))
            if n == 3:
                self.write_flag("SOFT_ALERT", "3 soft failures in a row, last: %s" % e)
                self.notify("3 retries failed: %s" % str(e)[:120])
            return 1

    def locked_tick(self):
        lock = self.base / "lock"
        self.base.mkdir(parents=True, exist_ok=True)
        try:
            lock.mkdir()
        except FileExistsError:
            try:
                pid = int((lock / "pid").read_text().strip())
                os.kill(pid, 0)
                return 0  # a live run is in progress
            except (OSError, ValueError):
                shutil.rmtree(lock, ignore_errors=True)
                lock.mkdir()
        (lock / "pid").write_text(str(os.getpid()))
        try:
            return self.tick()
        finally:
            shutil.rmtree(lock, ignore_errors=True)

    def status(self):
        items = queue_items(self.queue)
        self.say("queue: %d entr%s in %s" % (len(items), "y" if len(items) == 1 else "ies", self.queue))
        for p in items:
            try:
                self.say("  %s -> %s" % (p.name, load_item(p)["slug"]))
            except HardFail as e:
                self.say("  %s -> INVALID: %s" % (p.name, e))
        now = self.now()
        if (self.clone / ".git").is_dir():
            times = today_published_times(self.clone, now.date())
            self.say("today (from clone content/): %s" % (", ".join(t.strftime("%H:%M") for t in times) or "none"))
            self.say("decision now: %s" % (decide(now, times, self.force),))
        else:
            self.say("no clone yet at %s (first tick clones it)" % self.clone)
        for flag in ("FAILED", "SOFT_ALERT", "STOCK_ALERT", "LIVE_CHECK_FAILED"):
            if self.f(flag).exists():
                self.say("%s: %s" % (flag, " | ".join(self.f(flag).read_text().strip().splitlines())))
        return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default=os.environ.get("IDLE_PUBLISH_BASE", str(Path.home() / ".ipe" / "idle-publish")))
    ap.add_argument("--queue", default=os.environ.get("IDLE_PUBLISH_QUEUE", str(Path.home() / ".ipe" / "queue" / "idle")))
    ap.add_argument("--remote", default=os.environ.get("IDLE_PUBLISH_REMOTE", DEFAULT_REMOTE))
    ap.add_argument("--live-base", default=os.environ.get("IDLE_PUBLISH_LIVE", DEFAULT_LIVE))
    ap.add_argument("--now", help="ISO time with offset (test knob), e.g. 2026-11-06T11:30:00+09:00")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="ignore slot times (never the forbidden windows or the 2/day limit)")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--no-verify", action="store_true", help="skip the live 200 wait after push")
    ap.add_argument("--min-stock", type=int, default=MIN_STOCK)
    a = ap.parse_args(argv)
    now_fn = (lambda: dt.datetime.fromisoformat(a.now)) if a.now else None
    pub = Publisher(a.base, a.queue, a.remote, a.live_base, now_fn=now_fn, dry_run=a.dry_run, force=a.force,
                    verify=not a.no_verify, min_stock=a.min_stock)
    return pub.status() if a.status else pub.locked_tick()


if __name__ == "__main__":
    sys.exit(main())
