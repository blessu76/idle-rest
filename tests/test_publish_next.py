"""scripts/publish_next.py — slot rhythm, forbidden windows, stamping, queue validation, guards, and the whole tick against a
temporary bare git remote (build/check/tests stubbed out, no network, no notifications)."""
import datetime as dt
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import publish_next as pn  # noqa: E402

os.environ["IDLE_PUBLISH_NO_NOTIFY"] = "1"
KST = pn.KST


def at(day, hm):
    h, m = map(int, hm.split(":"))
    return dt.datetime(2026, 11, day, h, m, tzinfo=KST)


def entry(lang, slug="a-slug", title="A Title", extra=""):
    tr = "translation_of: ko\n" if lang == "en" else ""
    return ("---\ntitle: %s\ndate: 2026-01-01\nslug: %s\nlang: %s\n%sdescription: d\ncategory: behind-the-music\n%s---\n\nbody %s\n"
            % (title, slug, lang, tr, extra, lang))


class Rhythm(unittest.TestCase):
    def test_forbidden_windows_half_open(self):
        for hm, bad in (("09:59", False), ("10:00", True), ("10:59", True), ("11:00", False),
                        ("12:59", False), ("13:00", True), ("14:29", True), ("14:30", False)):
            self.assertEqual(pn.in_forbidden(dt.time.fromisoformat(hm)), bad, hm)

    def test_next_allowed_skips_window(self):
        self.assertEqual(pn.next_allowed(at(6, "10:20")), at(6, "11:00"))
        self.assertEqual(pn.next_allowed(at(6, "13:05")), at(6, "14:30"))
        self.assertEqual(pn.next_allowed(at(6, "12:00")), at(6, "12:00"))

    def test_morning_slot_is_stable_and_never_forbidden(self):
        for d in range(1, 29):
            day = dt.date(2026, 11, d)
            t = pn.morning_target(day)
            self.assertEqual(t, pn.morning_target(day))
            self.assertTrue(dt.time(11, 0) <= t.timetz().replace(tzinfo=None) <= dt.time(12, 59))

    def test_afternoon_is_four_hours_after_the_real_first_publish(self):
        for d in range(1, 29):
            day = dt.date(2026, 11, d)
            first = dt.time(11, 37)
            t = pn.afternoon_target(day, first)
            self.assertGreaterEqual(t, at(d, "15:37"))
            self.assertLess(t, at(d, "15:37") + dt.timedelta(minutes=pn.AFTERNOON_SPREAD_MIN))
            self.assertFalse(pn.in_forbidden(t.timetz().replace(tzinfo=None)))

    def test_decide_morning(self):
        target = pn.morning_target(dt.date(2026, 11, 6))
        self.assertFalse(pn.decide(target - dt.timedelta(minutes=1), [])[0])
        self.assertTrue(pn.decide(target, [])[0])
        self.assertTrue(pn.decide(at(6, "20:00"), [])[0])  # late first slot is allowed (catch-up of today, never of yesterday)

    def test_decide_never_inside_a_forbidden_window_even_forced(self):
        self.assertFalse(pn.decide(at(6, "10:30"), [], force=True)[0])
        self.assertFalse(pn.decide(at(6, "13:30"), [dt.time(11, 0)], force=True)[0])

    def test_decide_afternoon_and_limit(self):
        first = dt.time(11, 30)
        target = pn.afternoon_target(dt.date(2026, 11, 6), first)
        self.assertFalse(pn.decide(target - dt.timedelta(minutes=1), [first])[0])
        self.assertTrue(pn.decide(target, [first])[0])
        self.assertFalse(pn.decide(at(6, "23:00"), [first, dt.time(16, 0)])[0])  # 2 per day

    def test_afternoon_slot_past_midnight_is_not_today(self):
        ok, why = pn.decide(at(6, "23:59"), [dt.time(22, 30)])
        self.assertFalse(ok)
        self.assertIn("tomorrow", why)

    def test_now_needs_an_offset(self):
        with self.assertRaises(ValueError):
            pn.to_kst(dt.datetime(2026, 11, 6, 12, 0))


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
        if kw.get("ko", True):
            (d / "ko.md").write_text(entry("ko") if kw.get("ko") in (True, None) else kw["ko"], encoding="utf-8")
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
        (d / "a.md").write_text(entry("en", slug="a").replace("2026-01-01", "2026-11-06") .replace("---\n\nbody", 'time: "12:05"\n---\n\nbody'), encoding="utf-8")
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
        self.assertEqual(self.pub(at(6, "12:59")).locked_tick(), 0)
        self.assertNotEqual(self.head(), before)
        files = self.remote_files()
        self.assertIn("content/journal/en/first.md", files)
        self.assertIn("content/journal/ko/first.md", files)
        self.assertNotIn("content/journal/en/second.md", files)
        meta = pn.front_meta(self.remote_show("content/journal/en/first.md"))
        self.assertEqual((meta["date"], meta["time"]), ("2026-11-06", "12:59"))
        self.assertIn("idle-v11", self.remote_show("sw.js"))
        self.assertTrue((self.queue / ".published" / "01-first").is_dir())
        self.assertEqual([p.name for p in pn.queue_items(self.queue)], ["02-second", "03-third", "04-fourth"])
        self.assertFalse((self.tmp / "base" / "STOCK_ALERT").exists())

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
        self.assertEqual(self.pub(at(6, "12:59")).locked_tick(), 3)
        self.assertEqual(self.head(), before)
        self.assertIn("EMPTY", (self.tmp / "base" / "STOCK_ALERT").read_text())

    def test_low_stock_warns_once_a_day(self):
        self.add("01-a", "a")
        p = self.pub(at(6, "09:00"))
        p.locked_tick()
        first = (self.tmp / "base" / "STOCK_ALERT").read_text()
        notices = [l for l in self.logs if "NOTIFY" in l]
        self.assertEqual(len(notices), 1)
        p.locked_tick()
        self.assertEqual([l for l in self.logs if "NOTIFY" in l], notices)  # same day, same level: no second notification
        self.assertEqual((self.tmp / "base" / "STOCK_ALERT").read_text(), first)

    def test_second_slot_is_four_hours_after_the_first_and_third_never(self):
        for n in range(1, 5):
            self.add("0%d-x" % n, "x%d" % n)
        self.pub(at(6, "12:05")).locked_tick()
        self.assertEqual(self.pub(at(6, "15:00")).locked_tick(), 0)  # < 16:05
        self.assertNotIn("content/journal/en/x2.md", self.remote_files())
        self.pub(at(6, "16:30")).locked_tick()
        self.assertIn("content/journal/en/x2.md", self.remote_files())
        self.pub(at(6, "22:00")).locked_tick()
        self.assertNotIn("content/journal/en/x3.md", self.remote_files())

    def test_dry_run_changes_nothing(self):
        self.add("01-a", "a")
        before = self.head()
        self.assertEqual(self.pub(at(6, "12:59"), dry_run=True).locked_tick(), 0)
        self.assertEqual(self.head(), before)
        self.assertTrue((self.queue / "01-a").is_dir())
        self.assertFalse((self.queue / ".published").exists())

    def test_red_check_is_a_hard_fail_and_blocks_later_ticks(self):
        self.add("01-a", "a")
        before = self.head()
        red = [[sys.executable, "-c", "import sys; sys.exit(1)"]]
        self.assertEqual(self.pub(at(6, "12:59"), check_cmds=red).locked_tick(), 1)
        self.assertEqual(self.head(), before)
        self.assertTrue((self.tmp / "base" / "FAILED").exists())
        self.assertTrue((self.queue / "01-a").is_dir())  # manuscript not lost
        self.assertEqual(self.pub(at(6, "13:00")).locked_tick(), 0)  # FAILED present: waits for a human
        self.assertEqual(self.head(), before)

    def test_bad_manuscript_is_a_hard_fail(self):
        self.add("01-a", "a")
        (self.queue / "01-a" / "ko.md").unlink()
        before = self.head()
        self.assertEqual(self.pub(at(6, "12:59")).locked_tick(), 1)
        self.assertEqual(self.head(), before)

    def test_no_backdating_time_is_re_stamped_to_the_push_minute(self):
        """verification takes time: the stamp must follow the clock, not the minute the run started."""
        self.add("01-a", "a")
        clock = iter([at(6, "12:00"), at(6, "12:00"), at(6, "12:00"), at(6, "12:02"), at(6, "12:02"), at(6, "12:02"), at(6, "12:02")])
        last = [at(6, "12:02")]

        def now():
            try:
                last[0] = next(clock)
            except StopIteration:
                pass
            return last[0]

        p = pn.Publisher(self.tmp / "base", self.queue, str(self.remote), "http://invalid.invalid", now_fn=now, verify=False,
                         build_cmds=[], check_cmds=[], test_cmds=[], min_stock=0, log=self.logs.append)
        self.assertEqual(p.locked_tick(), 0)
        meta = pn.front_meta(self.remote_show("content/journal/en/a.md"))
        self.assertEqual(meta["time"], "12:02")

    def test_already_published_folder_self_heals_without_a_second_push(self):
        self.add("01-old", "old", title="Old")
        self.add("02-next", "next")
        self.assertEqual(self.pub(at(6, "12:59")).locked_tick(), 0)
        self.assertTrue((self.queue / ".published" / "01-old").is_dir())
        self.assertIn("content/journal/en/next.md", self.remote_files())

    def test_same_slug_different_title_is_a_hard_fail(self):
        self.add("01-old", "old", title="Something Else")
        self.assertEqual(self.pub(at(6, "12:59")).locked_tick(), 1)

    def test_stale_lock_is_taken_over(self):
        self.add("01-a", "a")
        lock = self.tmp / "base" / "lock"
        lock.mkdir(parents=True)
        (lock / "pid").write_text("999999")
        self.assertEqual(self.pub(at(6, "12:59")).locked_tick(), 0)
        self.assertIn("content/journal/en/a.md", self.remote_files())


if __name__ == "__main__":
    unittest.main()
