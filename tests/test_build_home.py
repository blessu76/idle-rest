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
        ko = self.page("ko")  # no ko post: no cards, never another language's post; the section is hidden
        self.assertNotIn('class="j-card"', ko)
        self.assertNotIn('href="/journal/en/hello/"', ko)
        self.assertRegex(ko, r'<section class="section" id="journal"[^>]* hidden>')
        self.assertIn('href="/journal/"', ko)  # ko has no list -> x-default hub

    def add_posts(self, lang, rows):
        for slug, date, time in rows:
            body = POST % dict(l=lang, extra="translation_of: en\n" if lang != "en" else "")
            body = body.replace("slug: hello", "slug: " + slug).replace("date: 2026-10-22", "date: %s%s" % (date, '\ntime: "%s"' % time if time else ""))
            (self.tmp / "content/journal" / lang / (slug + ".md")).write_text(body, encoding="utf-8")

    def cards(self, lang):
        return re.findall(r'<a class="j-card" href="([^"]+)" lang="([^"]+)">(.*?)</a>', self.page(lang), re.S)

    def test_cards_are_the_latest_three_newest_first_one_link_each(self):
        self.add_posts("en", [("p-old", "2026-10-01", None), ("p-mid", "2026-10-23", "09:54"), ("p-new", "2026-10-23", "13:10"), ("p-new2", "2026-10-25", "08:00")])
        self.build()
        got = self.cards("en")
        self.assertEqual([g[0] for g in got], ["/journal/en/p-new2/", "/journal/en/p-new/", "/journal/en/p-mid/"])
        self.assertEqual([g[1] for g in got], ["en"] * 3)
        self.assertEqual(self.page("en").count('class="j-card"'), 3)
        self.assertEqual(self.cards("ja")[0][0], "/journal/ja/hello/")  # other languages: only their own posts
        self.assertEqual(len(self.cards("ja")), 1)  # fewer than 3 -> as many as there are, no filler
        for href, lang, inner in got:
            self.assertNotIn("<a ", inner)  # one <a> per card (no nested links)
            self.assertIn("<h3>", inner)
            self.assertIn("<p>Desc en.</p>", inner)
        self.assertIn('<time datetime="2026-10-23T13:10:00+09:00" data-ipe-time>2026-10-23 13:10 KST</time>', self.page("en"))
        self.assertIn('href="/journal/en/"', self.page("en"))  # "view all"

    def test_check_fails_when_home_cards_are_stale(self):
        cmd = [sys.executable, str(REPO / "scripts/build_journal.py"), "--root", str(self.tmp), "--check"]
        self.assertEqual(subprocess.run(cmd, capture_output=True, text=True).returncode, 0)
        self.add_posts("en", [("fresh", "2026-10-25", "09:54")])  # published but the build was not run
        r = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("home cards are not up to date", r.stderr)
        self.build()
        self.assertEqual(subprocess.run(cmd, capture_output=True, text=True).returncode, 0)

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

    def test_footer_has_crawlable_hreflang_links_to_all_12(self):
        for l in [None] + LANGS:
            h = self.page(l)
            got = dict(re.findall(r'<a href="([^"]+)" hreflang="(\w+)" lang="\2"', h))
            self.assertEqual(sorted(got.values()), sorted(LANGS), l)
            self.assertTrue(all(u == "https://idle.ipe.rest/%s/" % x for u, x in got.items()), l)

    def test_root_title_and_description_differ_from_en(self):
        pick = lambda h, pat: re.search(pat, h).group(1)
        root, en = self.page(), self.page("en")
        self.assertNotEqual(pick(root, r"<title>(.*?)</title>"), pick(en, r"<title>(.*?)</title>"))
        self.assertNotEqual(pick(root, r'name="description" content="([^"]*)"'), pick(en, r'name="description" content="([^"]*)"'))

    def test_root_description_within_160(self):
        import html
        d = html.unescape(re.search(r'name="description" content="([^"]*)"', self.page()).group(1))
        self.assertLessEqual(len(d), 160, len(d))

    def test_404_noindex_and_asset_version_matches(self):
        h = (REPO / "404.html").read_text(encoding="utf-8")
        self.assertIn("noindex", h)
        src = (REPO / "scripts/build_journal.py").read_text(encoding="utf-8")
        v = re.search(r'^ASSET_V = "(\d+)"', src, re.M).group(1)
        self.assertEqual(set(re.findall(r"\?v=(\d+)", h)), {v})

    def test_translated_subtitles_in_all_languages(self):
        import json
        d = json.loads((REPO / "content/home/i18n.json").read_text(encoding="utf-8"))
        for l in LANGS[1:]:
            for k in ("singles_sub", "journal_sub"):
                self.assertIn(k, d[l], (l, k))
                self.assertNotEqual(d[l][k], d["en"][k], (l, k))

    def test_static_root_files(self):
        self.assertGreater((REPO / "favicon.ico").stat().st_size, 100)
        h = (REPO / "404.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="en"', h)
        self.assertIn("noindex", h)

    def test_journal_list_descriptions_are_snippet_sized(self):
        import html
        files = [f for f in REPO.glob("journal/**/index.html") if 'class="j-list"' in f.read_text(encoding="utf-8")]
        self.assertGreater(len(files), 12)
        for f in files:
            n = len(html.unescape(re.search(r'name="description" content="([^"]*)"', f.read_text(encoding="utf-8")).group(1)))
            self.assertTrue(70 <= n <= 160, (str(f.relative_to(REPO)), n))

    def test_idempotent(self):
        before = {p: p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()}
        self.build()
        self.assertEqual(before, {p: p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()})


if __name__ == "__main__":
    unittest.main()
