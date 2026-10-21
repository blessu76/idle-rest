"""Tests for scripts/check_sitemap.py — run: python3 -m unittest discover -s tests"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POST = """---
title: T
date: 2026-10-21
slug: ten-letters
lang: %s
description: d
category: behind-the-music
%s---

body
"""


class CheckSitemap(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for f in ("index.html", "sitemap.xml", "llms.txt"):
            shutil.copy(REPO / f, self.tmp / f)
        for lang, extra in (("ko", ""), ("en", "translation_of: ko\n"), ("ja", "translation_of: en\n")):
            d = self.tmp / "content/journal" / lang
            d.mkdir(parents=True)
            (d / "ten-letters.md").write_text(POST % (lang, extra), encoding="utf-8")
        self.sh("build_journal.py")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def sh(self, script, *a):
        return subprocess.run([sys.executable, str(REPO / "scripts" / script), "--root", str(self.tmp), *a], capture_output=True, text=True)

    def sitemap(self, f=None):
        p = self.tmp / "sitemap.xml"
        if f:
            p.write_text(f(p.read_text(encoding="utf-8")), encoding="utf-8")
        return self.sh("check_sitemap.py")

    def test_ok(self):
        r = self.sitemap()
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_missing_post_url(self):
        def drop(t):
            a = t.index("  <url>\n    <loc>https://idle.ipe.rest/journal/ja/ten-letters")
            return t[:a] + t[t.index("</url>", a) + 7:]
        r = self.sitemap(drop)
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing from sitemap: https://idle.ipe.rest/journal/ja/ten-letters/", r.stderr)

    def test_missing_language_list(self):
        r = self.sitemap(lambda t: t.replace("<loc>https://idle.ipe.rest/journal/ja/</loc>", "<loc>https://idle.ipe.rest/zz/</loc>"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing from sitemap: https://idle.ipe.rest/journal/ja/", r.stderr)

    def test_stale_and_hreflang_problems(self):
        r = self.sitemap(lambda t: t.replace('<xhtml:link rel="alternate" hreflang="ja" href="https://idle.ipe.rest/journal/ja/ten-letters/"/>', '<xhtml:link rel="alternate" hreflang="ja" href="https://idle.ipe.rest/ja/journal/ghost/"/>', 1))
        self.assertEqual(r.returncode, 1)
        self.assertIn("is not in the sitemap", r.stderr)

    def test_not_reciprocal(self):
        def cut(t):  # remove the ko entry from the ja page's alternates only
            a = t.index("<loc>https://idle.ipe.rest/journal/ja/ten-letters")
            b = t.index("</url>", a)
            seg = t[a:b]
            seg = "\n".join(l for l in seg.split("\n") if 'hreflang="ko"' not in l)
            return t[:a] + seg + t[b:]
        r = self.sitemap(cut)
        self.assertEqual(r.returncode, 1)
        self.assertIn("not reciprocal", r.stderr)

    def test_draft_translation_not_required(self):
        f = self.tmp / "content/journal/ja/ten-letters.md"
        f.write_text(POST % ("ja", "translation_of: en\ndraft: true\n"), encoding="utf-8")
        self.sh("build_journal.py")
        self.assertEqual(self.sh("check_sitemap.py").returncode, 0)

    def test_invalid_xml(self):
        r = self.sitemap(lambda t: t + "<broken")
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
