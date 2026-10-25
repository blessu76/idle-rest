"""sw.js guards (pure text checks — no JS runtime): same-origin only, cache only ok responses, CORE files exist."""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SW = (REPO / "sw.js").read_text(encoding="utf-8")


class ServiceWorker(unittest.TestCase):
    def test_cache_name_defined(self):
        self.assertRegex(SW, r"const CACHE = 'idle-v\d+';")

    def test_cross_origin_requests_are_left_to_the_browser(self):
        guard = "if (new URL(req.url).origin !== self.location.origin) return;"
        self.assertIn(guard, SW)
        self.assertLess(SW.index(guard), SW.index("respondWith"))

    def test_only_ok_responses_are_cached(self):
        puts = [m.start() for m in re.finditer(r"c\.put\(", SW)]
        self.assertEqual(len(puts), 2)  # html branch + asset branch
        for i in puts:
            self.assertIn("if (res.ok)", SW[max(0, i - 200):i])

    def test_core_files_exist(self):
        core = re.search(r"const CORE = \[(.*?)\];", SW, re.S).group(1)
        paths = re.findall(r"'(/[^']*)'", core)
        self.assertTrue(paths)
        for p in paths:
            f = REPO / (p.lstrip("/") or "index.html")
            self.assertTrue(f.is_file(), p)


if __name__ == "__main__":
    unittest.main()
