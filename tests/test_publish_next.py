"""scripts/publish_next.py — daily slot rhythm, forbidden windows, stamping, queue validation, guards, and the whole tick against a
temporary bare git remote (build/check/tests stubbed out, no network, no notifications)."""
import contextlib
import datetime as dt
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_journal as bj  # noqa: E402
import publish_next as pn  # noqa: E402

os.environ["IDLE_PUBLISH_NO_NOTIFY"] = "1"
KST = pn.KST


def at(day, hm):
    h, m = map(int, hm.split(":"))
    return dt.datetime(2026, 11, day, h, m, tzinfo=KST)


def slot(day=6, yesterday=()):
    return at(day, pn.day_target(dt.date(2026, 11, day), list(yesterday)).strftime("%H:%M"))


REVIEW = "copy_review: iris\ncopy_review_date: 2026-11-14\n"


def entry(lang, slug="a-slug", title="A Title", extra=""):
    tr = "translation_of: ko\n" if lang == "en" else ""
    return ("---\ntitle: %s\ndate: 2026-01-01\nslug: %s\nlang: %s\n%sdescription: d\ncategory: behind-the-music\n%s%s---\n\nbody %s\n"
            % (title, slug, lang, tr, REVIEW, extra, lang))


class Rhythm(unittest.TestCase):
    def test_forbidden_windows_half_open(self):
        for hm, bad in (("09:59", False), ("10:00", True), ("10:59", True), ("11:00", False),
                        ("12:59", False), ("13:00", True), ("14:29", True), ("14:30", False)):
            self.assertEqual(pn.in_forbidden(dt.time.fromisoformat(hm)), bad, hm)

    def test_slot_is_stable_inside_the_window_and_never_forbidden(self):
        for d in range(1, 29):
            day = dt.date(2026, 11, d)
            t = pn.day_target(day, [])
            self.assertEqual(t, pn.day_target(day, []))
            self.assertTrue(dt.time(12, 0) <= t < dt.time(18, 0))
            self.assertFalse(pn.in_forbidden(t))

    def test_slot_varies_across_days(self):
        self.assertGreater(len({pn.day_target(dt.date(2026, 11, d), []) for d in range(1, 29)}), 10)

    def test_slot_avoids_yesterdays_hour(self):
        for d in range(1, 29):
            day = dt.date(2026, 11, d)
            for h in range(12, 18):
                self.assertNotEqual(pn.day_target(day, [dt.time(h, 40)]).hour, h)

    def test_no_hour_is_avoided_when_yesterday_was_outside_the_window(self):
        self.assertEqual(pn.slot_candidates(None), pn.slot_candidates(21))

    def test_decide_waits_for_the_slot_then_publishes(self):
        target = slot()
        self.assertFalse(pn.decide(target - dt.timedelta(minutes=1), [], [])[0])
        self.assertTrue(pn.decide(target, [], [])[0])
        self.assertTrue(pn.decide(at(6, "17:59"), [], [])[0])

    def test_nothing_before_noon_and_nothing_at_or_after_18(self):
        self.assertFalse(pn.decide(at(6, "09:00"), [], [])[0])
        self.assertFalse(pn.decide(at(6, "18:00"), [], [])[0])
        self.assertFalse(pn.decide(at(6, "23:30"), [], [])[0])

    def test_one_per_day(self):
        ok, why = pn.decide(at(6, "17:00"), [dt.time(12, 30)], [])
        self.assertFalse(ok)
        self.assertIn("already published today", why)

    def test_forced_is_flagged_and_still_respects_forbidden_windows_and_daily_limit(self):
        ok, why = pn.decide(at(6, "09:00"), [], [], force=True)
        self.assertTrue(ok)
        self.assertIn("forced", why)
        self.assertFalse(pn.decide(at(6, "10:30"), [], [], force=True)[0])
        self.assertFalse(pn.decide(at(6, "13:30"), [], [], force=True)[0])
        self.assertFalse(pn.decide(at(6, "17:00"), [dt.time(12, 30)], [], force=True)[0])

    def test_next_publish(self):
        self.assertEqual(pn.next_publish(at(6, "09:00"), [], []), slot(6))
        published = dt.time(15, 10)
        nxt = pn.next_publish(at(6, "16:00"), [published], [])
        self.assertEqual(nxt, slot(7, [published]))
        self.assertNotEqual(nxt.hour, 15)
        self.assertEqual(pn.next_publish(at(6, "18:30"), [], []), slot(7, []))

    def test_now_needs_an_offset(self):
        with self.assertRaises(ValueError):
            pn.to_kst(dt.datetime(2026, 11, 6, 12, 0))


class QueueLint(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def write(self, name, words):
        d = self.tmp / name
        d.mkdir()
        body = " ".join(["word"] * words)
        (d / "en.md").write_text(entry("en").replace("body en", body), encoding="utf-8")
        (d / "ko.md").write_text(entry("ko").replace("body ko", body), encoding="utf-8")
        return d

    def test_short_original_is_listed_and_check_exits_1(self):
        self.write("05-short", bj.LINT_ERROR_WORDS - 1)
        low, invalid = pn.queue_lint(self.tmp)
        self.assertEqual(sorted(src for src, _ in low), ["05-short/en.md", "05-short/ko.md"])
        self.assertEqual(invalid, [])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(pn.main(["--queue", str(self.tmp), "--check-queue"]), 1)
        self.assertIn("LOW WORDS 05-short/ko.md", out.getvalue())

    def test_enough_words_passes_and_check_exits_0(self):
        self.write("06-long", bj.LINT_ERROR_WORDS)
        self.assertEqual(pn.queue_lint(self.tmp), ([], []))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(pn.main(["--queue", str(self.tmp), "--check-queue"]), 0)
        self.assertIn("queue lint: ok", out.getvalue())

    def test_status_shows_low_words_line(self):
        self.write("07-short", 10)
        pub = pn.Publisher(self.tmp / "base", self.tmp, "unused", "unused", now_fn=lambda: at(15, "12:30"), verify=False)
        lines = []
        pub.log = lines.append
        pub.status()
        self.assertTrue(any("LOW WORDS" in line and "07-short/ko.md" in line for line in lines), lines)


class Stamping(unittest.TestCase):
    def test_stamp_replaces_date_and_time_only(self):
        src = entry("en", extra='time: "09:00"\n')
        out = pn.stamp(src, dt.date(2026, 11, 6), "11:42")
        self.assertIn("date: 2026-11-06\ntime: \"11:42\"\nslug: a-slug", out)
        self.assertEqual(out.count("time:"), 1)
        self.assertEqual(out.split("\n---", 1)[1], src.split("\n---", 1)[1])  # body untouched
        meta = pn.front_meta(out)
        self.assertEqual((meta["date"], meta["time"]), ("2026-11-06", "11:42"))

    def test_stamp_needs_a_date_line(self):
        with self.assertRaises(pn.HardFail):
            pn.stamp("---\ntitle: x\n---\nbody\n", dt.date(2026, 11, 6), "11:00")

    def test_bump_sw(self):
        self.assertIn("'idle-v64'", pn.bump_sw("const CACHE = 'idle-v63';\n"))
        with self.assertRaises(pn.HardFail):
            pn.bump_sw("nothing here")


class QueueAndGuards(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def folder(self, name, **kw):
        d = self.tmp / name
        d.mkdir()
        (d / "en.md").write_text(kw.get("en", entry("en")), encoding="utf-8")
        ko = kw.get("ko", True)
        if ko is True:
            (d / "ko.md").write_text(entry("ko"), encoding="utf-8")
        elif ko:
            (d / "ko.md").write_text(ko, encoding="utf-8")
        return d

    def test_valid_item(self):
        it = pn.load_item(self.folder("01-a"))
        self.assertEqual((it["slug"], it["title"]), ("a-slug", "A Title"))

    def test_invalid_items_hard_fail(self):
        cases = {
            "missing ko": dict(ko=False),
            "draft": dict(en=entry("en", extra="draft: true\n")),
            "no translation_of": dict(en=entry("en").replace("translation_of: ko\n", "")),
            "slug differs": dict(ko=entry("ko", slug="other")),
            "bad slug": dict(en=entry("en", slug="Bad_Slug"), ko=entry("ko", slug="Bad_Slug")),
            "lang mismatch": dict(ko=entry("ko").replace("lang: ko", "lang: en")),
            "no copy_review": dict(en=entry("en").replace(REVIEW, "")),
            "copy_review by someone else": dict(en=entry("en").replace("copy_review: iris", "copy_review: dane")),
            "no copy_review_date": dict(ko=entry("ko").replace("copy_review_date: 2026-11-14\n", "")),
        }
        for i, (what, kw) in enumerate(cases.items()):
            with self.assertRaises(pn.HardFail, msg=what):
                pn.load_item(self.folder("%02d-x" % i, **kw))

    def test_queue_order_and_hidden_dirs(self):
        for n in ("02-b", "01-a", ".published"):
            (self.tmp / n).mkdir()
        (self.tmp / "note.txt").write_text("x")
        self.assertEqual([p.name for p in pn.queue_items(self.tmp)], ["01-a", "02-b"])
        self.assertEqual(pn.queue_items(self.tmp / "nope"), [])

    def test_staged_guard(self):
        ok = "M\tindex.html\nA\tcontent/journal/en/a-slug.md\nA\tjournal/en/a-slug/index.html\nM\tsw.js\nM\tsitemap.xml\nM\tko/index.html"
        pn.check_staged(ok)
        for bad in ("D\tjournal/en/old/index.html", "M\tassets/idle.css", "A\tscripts/x.py", "A\tcontent/journal/de/a.md",
                    "M\tcontent/pages/en/about.html"):
            with self.assertRaises(pn.HardFail, msg=bad):
                pn.check_staged(ok + "\n" + bad)
        with self.assertRaises(pn.HardFail):
            pn.check_staged(ok, "?? scripts/__pycache__/")

    def test_today_published_times_ignores_drafts_and_other_days(self):
        d = self.tmp / "content" / "journal" / "en"
        d.mkdir(parents=True)
        (d / "a.md").write_text(entry("en", slug="a").replace("2026-01-01", "2026-11-06").replace("---\n\nbody", 'time: "12:05"\n---\n\nbody'), encoding="utf-8")
        (d / "b.md").write_text(entry("en", slug="b").replace("2026-01-01", "2026-11-06").replace("---\n\nbody", 'time: "16:10"\ndraft: true\n---\n\nbody'), encoding="utf-8")
        (d / "c.md").write_text(entry("en", slug="c").replace("2026-01-01", "2026-11-05").replace("---\n\nbody", 'time: "09:00"\n---\n\nbody'), encoding="utf-8")
        self.assertEqual(pn.today_published_times(self.tmp, dt.date(2026, 11, 6)), [dt.time(12, 5)])


def sh(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True,
                   env=dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t"))


class Tick(unittest.TestCase):
    """whole tick: bare remote with a tiny fake site, real git, stubbed build/check/test commands."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.remote = self.tmp / "remote.git"
        seed = self.tmp / "seed"
        sh("git", "init", "-q", "--bare", "-b", "main", str(self.remote))
        sh("git", "init", "-q", "-b", "main", str(seed))
        (seed / "content/journal/en").mkdir(parents=True)
        (seed / "content/journal/en/old.md").write_text(entry("en", slug="old", title="Old"), encoding="utf-8")
        (seed / "sw.js").write_text("const CACHE = 'idle-v10';\n", encoding="utf-8")
        (seed / "index.html").write_text("<html>home</html>\n", encoding="utf-8")
        sh("git", "add", "-A", cwd=seed)
        sh("git", "commit", "-q", "-m", "seed", cwd=seed)
        sh("git", "push", "-q", str(self.remote), "main", cwd=seed)
        self.queue = self.tmp / "queue"
        self.queue.mkdir()
        self.logs = []

    def add(self, name, slug, title="T"):
        d = self.queue / name
        d.mkdir()
        (d / "en.md").write_text(entry("en", slug=slug, title=title), encoding="utf-8")
        (d / "ko.md").write_text(entry("ko", slug=slug, title=title), encoding="utf-8")

    def pub(self, now, **kw):
        for k in ("build_cmds", "check_cmds", "test_cmds"):
            kw.setdefault(k, [])
        return pn.Publisher(self.tmp / "base", self.queue, str(self.remote), "http://invalid.invalid",
                            now_fn=lambda: now, verify=False, log=self.logs.append, **kw)

    def remote_files(self):
        out = subprocess.run(["git", "--git-dir", str(self.remote), "ls-tree", "-r", "--name-only", "main"], capture_output=True, text=True).stdout
        return out.split()

    def remote_show(self, path):
        return subprocess.run(["git", "--git-dir", str(self.remote), "show", "main:" + path], capture_output=True, text=True).stdout

    def head(self):
        return subprocess.run(["git", "--git-dir", str(self.remote), "rev-parse", "main"], capture_output=True, text=True).stdout.strip()

    def test_publishes_one_entry_with_real_date_time_and_bumps_sw(self):
        for n, s in (("01-first", "first"), ("02-second", "second"), ("03-third", "third"), ("04-fourth", "fourth")):
            self.add(n, s)
        before = self.head()
        self.assertEqual(self.pub(slot()).locked_tick(), 0)
        self.assertNotEqual(self.head(), before)
        files = self.remote_files()
        self.assertIn("content/journal/en/first.md", files)
        self.assertIn("content/journal/ko/first.md", files)
        self.assertNotIn("content/journal/en/second.md", files)
        meta = pn.front_meta(self.remote_show("content/journal/en/first.md"))
        self.assertEqual((meta["date"], meta["time"]), ("2026-11-06", slot().strftime("%H:%M")))
        self.assertIn("idle-v11", self.remote_show("sw.js"))
        self.assertTrue((self.queue / ".published" / "01-first").is_dir())
        self.assertEqual([p.name for p in pn.queue_items(self.queue)], ["02-second", "03-third", "04-fourth"])
        self.assertFalse((self.tmp / "base" / "low_queue").exists())

    def test_nothing_due_before_the_slot_pushes_nothing(self):
        self.add("01-a", "a")
        before = self.head()
        self.assertEqual(self.pub(at(6, "09:30")).locked_tick(), 0)
        self.assertEqual(self.head(), before)
        self.assertTrue((self.queue / "01-a").is_dir())

    def test_forbidden_window_pushes_nothing_even_forced(self):
        self.add("01-a", "a")
        before = self.head()
        self.assertEqual(self.pub(at(6, "10:15"), force=True).locked_tick(), 0)
        self.assertEqual(self.pub(at(6, "13:40"), force=True).locked_tick(), 0)
        self.assertEqual(self.head(), before)

    def test_empty_queue_when_due_does_not_push_and_warns(self):
        before = self.head()
        self.assertEqual(self.pub(slot()).locked_tick(), 3)
        self.assertEqual(self.head(), before)
        self.assertIn("EMPTY", (self.tmp / "base" / "low_queue").read_text())

    def test_low_stock_warns_on_stderr_at_publish_time_and_notifies_once(self):
        self.add("01-a", "a")
        self.add("02-b", "b")
        self.assertEqual(self.pub(at(6, "09:00")).locked_tick(), 0)
        self.assertFalse((self.tmp / "base" / "low_queue").exists())
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(self.pub(slot()).locked_tick(), 0)
        self.assertIn("LOW", (self.tmp / "base" / "low_queue").read_text())
        self.assertIn("WARNING", err.getvalue())
        self.assertEqual(len([l for l in self.logs if "NOTIFY" in l]), 1)

    def test_one_per_day_and_the_next_day_avoids_the_previous_hour(self):
        for n in range(1, 5):
            self.add("0%d-x" % n, "x%d" % n)
        first = slot(6)
        self.assertEqual(self.pub(first).locked_tick(), 0)
        self.assertEqual(self.pub(at(6, "17:50")).locked_tick(), 0)
        self.assertNotIn("content/journal/en/x2.md", self.remote_files())
        self.assertEqual(self.pub(slot(7, [first.time()])).locked_tick(), 0)
        self.assertIn("content/journal/en/x2.md", self.remote_files())
        self.assertNotEqual(slot(7, [first.time()]).hour, first.hour)

    def test_status_reports_the_next_publish(self):
        self.add("01-a", "a")
        p = self.pub(at(6, "09:00"))
        self.assertEqual(p.status(), 0)
        expected = "next publish: 2026-11-06 %s KST" % slot().strftime("%H:%M")
        self.assertTrue(any(expected in l for l in self.logs), self.logs)

    def test_dry_run_changes_nothing(self):
        self.add("01-a", "a")
        before = self.head()
        self.assertEqual(self.pub(slot(), dry_run=True).locked_tick(), 0)
        self.assertEqual(self.head(), before)
        self.assertTrue((self.queue / "01-a").is_dir())
        self.assertFalse((self.queue / ".published").exists())

    def test_red_check_is_a_hard_fail_and_blocks_later_ticks(self):
        self.add("01-a", "a")
        before = self.head()
        red = [[sys.executable, "-c", "import sys; sys.exit(1)"]]
        self.assertEqual(self.pub(slot(), check_cmds=red).locked_tick(), 1)
        self.assertEqual(self.head(), before)
        self.assertTrue((self.tmp / "base" / "FAILED").exists())
        self.assertTrue((self.queue / "01-a").is_dir())  # manuscript not lost
        self.assertEqual(self.pub(at(6, "17:00")).locked_tick(), 0)  # FAILED present: waits for a human
        self.assertEqual(self.head(), before)

    def test_bad_manuscript_is_a_hard_fail(self):
        self.add("01-a", "a")
        (self.queue / "01-a" / "ko.md").unlink()
        before = self.head()
        self.assertEqual(self.pub(slot()).locked_tick(), 1)
        self.assertEqual(self.head(), before)

    def test_time_is_re_stamped_to_the_push_minute_not_the_start_minute(self):
        self.add("01-a", "a")
        clock = [at(6, "12:00")]

        class Slow(pn.Publisher):
            def steps(self, cmds, what):
                if what == "tests":
                    clock[0] = at(6, "12:02")  # verification takes two minutes
                super().steps(cmds, what)

        p = Slow(self.tmp / "base", self.queue, str(self.remote), "http://invalid.invalid", now_fn=lambda: clock[0],
                 verify=False, build_cmds=[], check_cmds=[], test_cmds=[], min_stock=0, force=True, log=self.logs.append)
        self.assertEqual(p.locked_tick(), 0)
        meta = pn.front_meta(self.remote_show("content/journal/en/a.md"))
        self.assertEqual(meta["time"], "12:02")

    def test_already_published_folder_self_heals_without_a_second_push(self):
        self.add("01-old", "old", title="Old")
        self.add("02-next", "next")
        self.assertEqual(self.pub(slot()).locked_tick(), 0)
        self.assertTrue((self.queue / ".published" / "01-old").is_dir())
        self.assertIn("content/journal/en/next.md", self.remote_files())

    def test_same_slug_different_title_is_a_hard_fail(self):
        self.add("01-old", "old", title="Something Else")
        self.assertEqual(self.pub(slot()).locked_tick(), 1)

    def test_stale_lock_is_taken_over(self):
        self.add("01-a", "a")
        lock = self.tmp / "base" / "lock"
        lock.mkdir(parents=True)
        (lock / "pid").write_text("999999")
        self.assertEqual(self.pub(slot()).locked_tick(), 0)
        self.assertIn("content/journal/en/a.md", self.remote_files())


if __name__ == "__main__":
    unittest.main()
