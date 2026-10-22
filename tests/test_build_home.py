"""Tests for scripts/build_home.py (12 static home pages) — run: python3 -m unittest discover -s tests"""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LANGS = "en ko ja zh es fr de pt ru ar hi id".split()
POST = """---
title: Hello %(l)s
date: 2026-10-22
slug: hello
lang: %(l)s
description: Desc %(l)s.
category: notes
%(extra)s---

Body.
"""


class BuildHome(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for f in ("index.html", "sitemap.xml", "llms.txt"):
            shutil.copy(REPO / f, self.tmp / f)
        shutil.copytree(REPO / "content/home", self.tmp / "content/home")
        shutil.copytree(REPO / "content/pages", self.tmp / "content/pages")
        for lang, extra in (("en", ""), ("ja", "translation_of: en\n")):
            d = self.tmp / "content/journal" / lang
            d.mkdir(parents=True)
            (d / "hello.md").write_text(POST % dict(l=lang, extra=extra), encoding="utf-8")
        self.build()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def build(self):
        r = subprocess.run([sys.executable, str(REPO / "scripts/build_journal.py"), "--root", str(self.tmp)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def page(self, lang=None):
        return (self.tmp / (lang + "/index.html" if lang else "index.html")).read_text(encoding="utf-8")

    def test_every_language_is_a_static_page(self):
        for l in LANGS:
            h = self.page(l)
            self.assertIn('<html lang="%s" dir="%s"' % (l, "rtl" if l == "ar" else "ltr"), h, l)
            self.assertIn('<link rel="canonical" href="https://idle.ipe.rest/%s/">' % l, h, l)
            got = dict(re.findall(r'<link rel="alternate" hreflang="([\w-]+)" href="([^"]+)"', h))
            self.assertEqual(set(got), set(LANGS) | {"x-default"}, l)
            self.assertEqual(got["x-default"], "https://idle.ipe.rest/")
            self.assertTrue(all(got[x] == "https://idle.ipe.rest/%s/" % x for x in LANGS), l)
            self.assertNotIn("?lang=", h.replace("get('lang')", "").replace("location.replace", ""), l)
            self.assertEqual(h.count('rel="canonical"'), 1)
            self.assertNotIn("{{", h)
            self.assertIn('property="og:locale" content="', h)
            self.assertIn('og:locale:alternate', h)
            self.assertIn('data-ads="off"', h)
            self.assertIn("googletagmanager", h)  # GA4 kept
            self.assertIn("cloudflareinsights", h)
            self.assertIn('class="ad-slot"', h)

    def test_titles_and_text_follow_the_language(self):
        titles = {re.search(r"<title>(.*?)</title>", self.page(l)).group(1) for l in LANGS}
        self.assertGreaterEqual(len(titles), 10)  # a few languages may share the English title, not most
        self.assertIn("ja_JP", self.page("ja"))
        self.assertIn("Skip to content", self.page("en"))
        self.assertNotIn("Skip to content", self.page("ko"))
        self.assertIn('<option value="ja" selected>JA</option>', self.page("ja"))

    def test_no_bottom_lang_list_but_select_and_hreflang_stay(self):
        for l in [None] + LANGS:
            h = self.page(l)
            self.assertNotIn("lang-list", h, l)
            self.assertIn("<select", h, l)
            self.assertIn('<link rel="alternate" hreflang="x-default" href="https://idle.ipe.rest/">', h, l)

    def test_root_is_x_default_without_forced_redirect(self):
        h = self.page()
        self.assertIn('<link rel="canonical" href="https://idle.ipe.rest/">', h)
        self.assertIn('<html lang="en"', h)
        self.assertIn('id="langHint" hidden', h)  # hint only: hidden until JS decides, never a redirect
        self.assertNotIn('http-equiv="refresh"', h)
        self.assertNotIn("langHint", self.page("ja").replace("lang-hint", ""))  # only the root has the hint

    def test_legacy_query_redirect_script_everywhere(self):
        for l in (None, "ko"):
            self.assertIn("get('lang')", self.page(l))

    def test_journal_cards_per_language(self):
        ja = self.page("ja")
        self.assertIn('href="/journal/ja/hello/"', ja)
        self.assertIn('href="/journal/ja/"', ja)  # "view all" goes to that language's list
        ko = self.page("ko")  # no ko post: falls back to the English card, linked to the English page
        self.assertIn('href="/journal/en/hello/"', ko)
        self.assertIn('href="/journal/"', ko)  # ko has no list -> x-default hub

    def test_sitemap_has_home_in_every_language(self):
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
        root = ET.parse(self.tmp / "sitemap.xml").getroot()
        rows = {u.find("s:loc", ns).text: u for u in root.findall("s:url", ns)}
        for l in LANGS:
            u = rows["https://idle.ipe.rest/%s/" % l]
            self.assertEqual(len(u.findall("x:link", ns)), 13)
            self.assertIsNotNone(u.find("s:lastmod", ns))
        self.assertIn("https://idle.ipe.rest/", rows)
        self.assertFalse([l for l in rows if "?lang=" in l])
        self.assertIn("https://idle.ipe.rest/ja/", self.tmp.joinpath("llms.txt").read_text(encoding="utf-8"))

    def test_idempotent(self):
        before = {p: p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()}
        self.build()
        self.assertEqual(before, {p: p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()})


if __name__ == "__main__":
    unittest.main()
