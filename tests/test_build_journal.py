"""Smoke tests for scripts/build_journal.py — run: python3 -m unittest discover -s tests"""
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def png(w, h):
    raw = b"".join(b"\x00" + b"\x00\x00\x00" * w for _ in range(h))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


POST = """---
title: %(t)s
date: 2026-10-22
slug: a
lang: %(l)s
description: A test post.
category: notes
%(extra)s---

Intro with an [article](https://news.example.com/a) and a [video](https://youtu.be/x).

## Section

![Cover alt](/assets/journal/a/c.png "Cap")
"""

LD = re.compile(r'<script type="application/ld\+json">\n(.*?)\n</script>', re.S)


class Site(unittest.TestCase):
    """Fresh site copy per test; write posts to content/journal/<lang>/<slug>.md, then build / --check."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for f in ("index.html", "sitemap.xml", "llms.txt"):
            shutil.copy(REPO / f, self.tmp / f)
        shutil.copytree(REPO / "content/home", self.tmp / "content/home")
        shutil.copytree(REPO / "content/pages", self.tmp / "content/pages")
        (self.tmp / "content/journal").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def post(self, slug="a", lang="en", extra="", body=None, draft=False, sub=None, title=None):
        text = MINIMAL % dict(s=slug, l=lang, t=title or "T-" + lang, extra=extra + ("draft: true\n" if draft else ""))
        if body:
            text += "\n" + body
        d = self.tmp / "content/journal" / (lang if sub is None else sub)
        d.mkdir(parents=True, exist_ok=True)
        (d / ("%s.md" % slug)).write_text(text, encoding="utf-8")

    def pair(self, slug="a"):
        self.post(slug, "ko")
        self.post(slug, "en", extra="translation_of: ko\n")

    def ai(self, lang, slug="a", of="en", extra="", **kw):
        self.post(slug, lang, extra="translation_of: %s\n%s" % (of, extra), **kw)

    def run_build(self, *flags):
        return subprocess.run([sys.executable, str(REPO / "scripts/build_journal.py"), "--root", str(self.tmp), *flags],
                              capture_output=True, text=True)

    def build(self):
        r = self.run_build()
        self.assertEqual(r.returncode, 0, r.stderr)

    def read(self, rel):
        return (self.tmp / rel).read_text(encoding="utf-8")

    def ld(self, rel):
        h = self.read(rel)
        return h, [json.loads(m) for m in LD.findall(h)]

    def fails(self, expect, *flags):
        r = self.run_build(*(flags or ("--check",)))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn(expect, r.stderr)


MINIMAL = """---
title: %(t)s
date: 2026-10-22
slug: %(s)s
lang: %(l)s
description: Only the required fields.
category: notes
%(extra)s---

Plain body, no image, no link.
"""


class BuildJournal(Site):
    def setUp(self):
        super().setUp()
        (self.tmp / "assets/journal/a").mkdir(parents=True)
        (self.tmp / "assets/journal/a/c.png").write_bytes(png(30, 20))
        extra_en = "keywords: x, y\nsongs: Song A @ https://youtu.be/abc | Song B\nalbum: Alb @ https://idle.ipe.rest/#album\ntranslation_of: ko\naliases: /journal/a-en/\n"
        for lang, extra in (("en", extra_en), ("ko", "aliases: /journal/a-ko/\n")):
            d = self.tmp / "content/journal" / lang
            d.mkdir()
            (d / "a.md").write_text(POST % dict(t=lang.upper(), l=lang, extra=extra), encoding="utf-8")
        self.build()

    def test_post_jsonld_and_html(self):
        h, blocks = self.ld("journal/en/a/index.html")
        post = next(b for b in blocks if b["@type"] == "BlogPosting")
        for k in ("headline", "datePublished", "author", "publisher", "image", "inLanguage", "wordCount", "keywords"):
            self.assertIn(k, post)
        self.assertEqual(post["url"], "https://idle.ipe.rest/journal/en/a/")
        self.assertEqual(post["image"]["width"], 30)
        self.assertEqual(post["translationOfWork"]["inLanguage"], "ko")
        self.assertEqual(post["isPartOf"]["url"], "https://idle.ipe.rest/journal/en/")
        self.assertEqual([a["@type"] for a in post["about"]], ["MusicAlbum", "MusicRecording", "MusicRecording"])
        self.assertEqual(post["about"][1]["sameAs"], "https://youtu.be/abc")
        self.assertEqual([c["url"] for c in post["citation"]], ["https://news.example.com/a"])  # youtube not cited
        self.assertIn("BreadcrumbList", [b["@type"] for b in blocks])
        self.assertIn('<link rel="canonical" href="https://idle.ipe.rest/journal/en/a/">', h)
        self.assertIn('hreflang="x-default" href="https://idle.ipe.rest/journal/en/a/"', h)
        self.assertIn('<figure><img src="/assets/journal/a/c.png" alt="Cover alt" width="30" height="20" loading="lazy"', h)
        self.assertNotIn('class="ai-note"', h)  # ko/en are originals: no AI notice
        ko = self.ld("journal/ko/a/index.html")[1][0]
        self.assertEqual(ko["workTranslation"]["inLanguage"], "en")
        self.assertNotIn("keywords", ko)  # optional fields are omitted, not empty

    def test_hub_lists_sitemap_llms_feed(self):
        _, blocks = self.ld("journal/index.html")
        self.assertEqual({"Blog", "ItemList", "BreadcrumbList"}, {b["@type"] for b in blocks})
        hub = self.read("journal/index.html")
        self.assertIn('hreflang="x-default" href="https://idle.ipe.rest/journal/"', hub)
        self.assertIn('href="/journal/ko/a/"', hub)
        root = ET.parse(self.tmp / "sitemap.xml").getroot()
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml",
              "i": "http://www.google.com/schemas/sitemap-image/1.1"}
        locs = [u.find("s:loc", ns).text for u in root.findall("s:url", ns)]
        for want in ("/journal/", "/journal/ko/", "/journal/en/", "/journal/ko/a/", "/journal/en/a/"):
            self.assertIn("https://idle.ipe.rest" + want, locs)
        self.assertFalse([l for l in locs if "/journal/a-" in l])  # old URLs are not listed
        row = next(u for u in root.findall("s:url", ns) if u.find("s:loc", ns).text.endswith("/journal/ko/a/"))
        self.assertEqual({l.get("hreflang") for l in row.findall("x:link", ns)}, {"ko", "en", "x-default"})
        self.assertEqual(row.find("i:image/i:loc", ns).text, "https://idle.ipe.rest/assets/journal/a/c.png")
        self.assertIsNotNone(row.find("s:lastmod", ns))
        llms = self.read("llms.txt")
        self.assertIn("## Journal", llms)
        self.assertIn("https://idle.ipe.rest/journal/en/a/", llms)
        self.assertIn('Please attribute to "idle() (the music of ipe())"', llms)
        self.assertIn("https://idle.ipe.rest/journal/en/a/", self.read("journal/feed.xml"))

    def test_old_urls_redirect_stubs(self):
        for old, new in (("journal/a-en", "/journal/en/a/"), ("journal/a-ko", "/journal/ko/a/")):
            h = self.read(old + "/index.html")
            self.assertIn('<link rel="canonical" href="https://idle.ipe.rest%s">' % new, h)
            self.assertIn('http-equiv="refresh" content="0; url=https://idle.ipe.rest%s"' % new, h)
            self.assertIn('<a href="https://idle.ipe.rest%s">' % new, h)

    def test_dropped_alias_is_swept(self):
        p = self.tmp / "content/journal/ko/a.md"
        p.write_text(p.read_text(encoding="utf-8").replace("aliases: /journal/a-ko/\n", ""), encoding="utf-8")
        self.build()
        self.assertFalse((self.tmp / "journal/a-ko").exists())
        self.assertTrue((self.tmp / "journal/a-en/index.html").exists())

    def test_idempotent(self):
        before = {p: p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()}
        self.build()
        self.assertEqual(before, {p: p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()})


class PostTime(Site):
    def test_time_shown_and_machine_values(self):
        self.post("t", "en", extra='time: "09:09"\n')
        self.post("n", "en")
        self.build()
        h, blocks = self.ld("journal/en/t/index.html")
        post = next(b for b in blocks if b["@type"] == "BlogPosting")
        self.assertIn('<time datetime="2026-10-22T09:09:00+09:00">2026. 10. 22 09:09</time>', h)
        self.assertEqual(post["datePublished"], "2026-10-22T09:09:00+09:00")
        self.assertEqual(post["dateModified"], "2026-10-22T09:09:00+09:00")
        self.assertIn('article:published_time" content="2026-10-22T09:09:00+09:00"', h)
        lst = self.read("journal/en/index.html")
        self.assertIn('<time datetime="2026-10-22T09:09:00+09:00">2026. 10. 22 09:09</time>', lst)
        self.assertIn('<time datetime="2026-10-22">2026. 10. 22</time>', lst)  # post without time

    def test_no_time_stays_date_only(self):
        self.post("n", "en")
        self.build()
        h, blocks = self.ld("journal/en/n/index.html")
        post = next(b for b in blocks if b["@type"] == "BlogPosting")
        self.assertIn('<time datetime="2026-10-22">2026. 10. 22</time>', h)
        self.assertEqual(post["datePublished"], "2026-10-22")
        self.assertEqual(post["dateModified"], "2026-10-22")
        self.assertNotIn("T00:00", h)

    def test_same_day_order_feed_and_modified(self):
        for slug, tm in (("zz", "08:00"), ("aa", "12:30"), ("mm", "10:15")):
            self.post(slug, "en", extra='time: "%s"\nupdated: 2026-10-22\n' % tm)
        self.build()
        lst = self.read("journal/en/index.html")
        order = [lst.index('/journal/en/%s/' % s) for s in ("aa", "mm", "zz")]
        self.assertEqual(order, sorted(order))  # newest time first, not slug order
        feed = self.read("journal/feed.xml")
        self.assertIn("<pubDate>Thu, 22 Oct 2026 12:30:00 +0900</pubDate>", feed)
        h, blocks = self.ld("journal/en/aa/index.html")
        post = next(b for b in blocks if b["@type"] == "BlogPosting")
        self.assertEqual(post["dateModified"], post["datePublished"])  # date-only updated on publish day
        self.assertIn('article:modified_time" content="2026-10-22T12:30:00+09:00"', h)
        self.post("aa", "en", extra='time: "12:30"\nupdated: 2026-10-25\n')
        self.build()
        post = next(b for b in self.ld("journal/en/aa/index.html")[1] if b["@type"] == "BlogPosting")
        self.assertEqual(post["dateModified"], "2026-10-25")

    def test_dates_wrap_in_units_and_ltr(self):
        self.post("t", "en", extra='time: "09:09"\n')
        self.build()
        self.assertIn('<span class="j-cat">· notes</span>', self.read("journal/en/t/index.html"))
        self.assertIn(".j-date time { direction: ltr; unicode-bidi: isolate; }", (REPO / "assets/idle.css").read_text())

    def test_bad_time_fails(self):
        for bad in ("9:09", "24:00", "09:09:00", "noon", "09:60", "9:9", " 09:09 "):
            self.post("b", "en", extra='time: "%s"\n' % bad)
            self.fails("time must be HH:MM")


class Validation(Site):
    def test_post_without_optional_fields(self):
        self.post("plain")
        self.assertEqual(self.run_build("--check").returncode, 0)
        self.build()
        h, blocks = self.ld("journal/en/plain/index.html")
        post = next(b for b in blocks if b["@type"] == "BlogPosting")
        for k in ("keywords", "about", "citation", "translationOfWork", "workTranslation"):
            self.assertNotIn(k, post)
        self.assertEqual(post["image"], "https://idle.ipe.rest/og-image.png")
        self.assertIn('hreflang="x-default" href="https://idle.ipe.rest/journal/en/plain/"', h)

    def test_missing_image_fails(self):
        self.post("front", extra="image: /assets/journal/front/nope.jpg\n")
        self.post("inline", body="![x](/assets/journal/inline/nope.jpg)\n")
        for flags in (("--check",), ()):
            r = self.run_build(*flags)
            self.assertEqual(r.returncode, 1, flags)
            self.assertIn("en/front.md: image file not found: /assets/journal/front/nope.jpg", r.stderr)
            self.assertIn("en/inline.md: image file not found: /assets/journal/inline/nope.jpg", r.stderr)
        self.assertFalse((self.tmp / "journal").exists())  # nothing half-written

    def test_existing_image_ok_and_external_image_skipped(self):
        (self.tmp / "assets/journal/ok").mkdir(parents=True)
        (self.tmp / "assets/journal/ok/c.png").write_bytes(png(4, 4))
        self.post("ok", extra="image: https://example.com/c.png\n", body="![x](/assets/journal/ok/c.png)\n")
        self.assertEqual(self.run_build("--check").returncode, 0)

    def test_valid_pair_ok(self):
        self.pair()
        self.assertEqual(self.run_build("--check").returncode, 0)

    def test_old_translation_field_removed(self):
        self.post("a", "ko", extra="translation: a-en\n")
        self.fails("`translation:` was removed")

    def test_translation_of_must_exist_in_group(self):
        self.post("a", "en", extra="translation_of: ko\n")
        self.fails("translation_of ko but there is no ko post with slug 'a'")

    def test_translation_of_draft_fails(self):
        self.post("a", "ko", draft=True)
        self.post("a", "en", extra="translation_of: ko\n")
        self.fails("translation_of ko refers to a draft")

    def test_translation_of_values(self):
        self.post("a", "en", extra="translation_of: en\n")
        self.fails("translation_of must be the language code of the ko/en original")
        self.post("a", "en", extra="translation_of: ja\n")
        self.fails("translation_of must be the language code of the ko/en original")

    def test_slug_reserved_and_filename(self):
        self.post("ja", "en")
        self.fails("is reserved")
        shutil.rmtree(self.tmp / "content/journal/en")
        self.post("a", "en")
        (self.tmp / "content/journal/en/a.md").rename(self.tmp / "content/journal/en/b.md")
        self.fails("file name must be <slug>.md")

    def test_folder_must_match_lang(self):
        self.post("a", "en", sub="ko")
        self.fails("file is in ko/ but lang is en")

    def test_flat_file_rejected(self):
        self.post("a", "en", sub=".")
        self.fails("move to content/journal/<lang>/a.md")

    def test_alias_errors(self):
        self.post("a", "en", extra="aliases: /journal/en/\n")
        self.fails("alias /journal/en/ is a real page")
        self.post("a", "en", extra="aliases: /journal/old/\n")
        self.post("b", "en", extra="aliases: /journal/old/\n")
        self.fails("alias /journal/old/ already used")
        self.post("b", "en", extra="aliases: https://x.example/\n")
        self.fails("alias must be a site path")


class I18n(Site):
    """12-language structure: every language at /journal/<lang>/<slug>/; one slug = one translation group."""

    def test_group_urls_hreflang_jsonld(self):
        self.pair()
        self.ai("ja")
        self.ai("ar")
        self.build()
        want = {"ko": "/journal/ko/a/", "en": "/journal/en/a/", "ja": "/journal/ja/a/", "ar": "/journal/ar/a/"}
        for rel in want.values():  # every member lists every member
            h, _ = self.ld(rel.strip("/") + "/index.html")
            got = dict(re.findall(r'<link rel="alternate" hreflang="([\w-]+)" href="https://idle.ipe.rest([^"]+)"', h))
            self.assertEqual(got, dict(want, **{"x-default": "/journal/en/a/"}), rel)
            self.assertIn('<link rel="canonical" href="https://idle.ipe.rest%s">' % rel, h)
        h, blocks = self.ld("journal/ja/a/index.html")
        post = next(b for b in blocks if b["@type"] == "BlogPosting")
        self.assertEqual(post["inLanguage"], "ja")
        self.assertEqual(post["translationOfWork"]["url"], "https://idle.ipe.rest/journal/en/a/")
        self.assertEqual(post["isPartOf"]["url"], "https://idle.ipe.rest/journal/ja/")
        self.assertEqual(post["translator"]["@type"], "Organization")
        self.assertIn('<html lang="ja" dir="ltr"', h)
        self.assertIn('class="ai-note"', h)
        self.assertIn('og:locale" content="ja_JP"', h)
        self.assertIn('og:locale:alternate" content="ar_AR"', h)
        self.assertIn('<html lang="ar" dir="rtl"', self.read("journal/ar/a/index.html"))
        en = self.ld("journal/en/a/index.html")[1][0]
        self.assertEqual({w["inLanguage"] for w in en["workTranslation"]}, {"ja", "ar"})
        self.assertEqual(en["translationOfWork"]["inLanguage"], "ko")
        self.assertNotIn("ai-note", self.read("journal/en/a/index.html"))
        self.assertEqual({b["@type"] for b in self.ld("journal/ja/index.html")[1]}, {"Blog", "ItemList", "BreadcrumbList"})

    def test_ko_translation_source(self):
        self.pair()
        self.ai("fr", of="ko")
        self.build()
        post = next(b for b in self.ld("journal/fr/a/index.html")[1] if b["@type"] == "BlogPosting")
        self.assertEqual(post["translationOfWork"]["inLanguage"], "ko")

    def test_only_existing_languages_exported(self):
        self.pair()
        self.ai("ja")
        self.build()
        self.assertFalse((self.tmp / "journal/fr").exists())
        sm = self.read("sitemap.xml")
        self.assertIn("/journal/ja/a/", sm)
        self.assertNotIn("/journal/fr", sm)
        self.assertNotIn('hreflang="fr"', sm.split("journal:start")[1])
        ET.parse(self.tmp / "sitemap.xml")
        llms = self.read("llms.txt")
        self.assertIn("### Journal — 日本語 (ja)", llms)
        self.assertNotIn("(fr)", llms)
        self.assertNotIn("/journal/ja/", self.read("journal/feed.xml"))  # feed stays ko/en

    def test_removed_translation_is_swept(self):
        self.pair()
        self.ai("ja", extra="aliases: /ja/journal/a-en/\n")
        self.build()
        self.assertTrue((self.tmp / "ja/journal/a-en/index.html").exists())
        (self.tmp / "content/journal/ja/a.md").unlink()
        self.build()
        self.assertFalse((self.tmp / "journal/ja").exists())
        self.assertFalse((self.tmp / "ja/journal").exists())
        self.assertTrue((self.tmp / "ja/index.html").exists())  # the home page of /ja/ stays

    def test_sitemap_hreflang_mutual(self):
        self.pair()
        self.ai("ja")
        self.build()
        root = ET.parse(self.tmp / "sitemap.xml").getroot()
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
        sets = {}
        for u in root.findall("s:url", ns):
            loc = u.find("s:loc", ns).text
            if re.search(r"/journal/(ko|en|ja)/a/$", loc):
                sets[loc] = {l.get("hreflang") for l in u.findall("x:link", ns)}
        self.assertEqual(len(sets), 3)
        self.assertTrue(all(v == {"ko", "en", "ja", "x-default"} for v in sets.values()), sets)

    def test_old_language_list_redirects(self):
        self.pair()
        self.ai("ja")
        self.build()
        h = self.read("ja/journal/index.html")
        self.assertIn('rel="canonical" href="https://idle.ipe.rest/journal/ja/"', h)

    def test_language_select_points_only_at_existing_pages(self):
        self.pair()
        self.ai("ja")
        self.build()
        opts = lambda rel: re.findall(r'<option value="([^"]+)"( selected)?>', self.read(rel).split("</select>")[0])
        post = opts("journal/ja/a/index.html")
        self.assertEqual({v for v, _ in post}, {"/journal/ko/a/", "/journal/en/a/", "/journal/ja/a/"})
        self.assertEqual([v for v, sel in post if sel], ["/journal/ja/a/"])
        for v, _ in post:
            self.assertTrue((self.tmp / v.strip("/") / "index.html").exists(), v)
        lst = opts("journal/ko/index.html")
        self.assertEqual({v for v, _ in lst}, {"/journal/ko/", "/journal/en/", "/journal/ja/"})
        self.assertEqual([v for v, sel in lst if sel], ["/journal/ko/"])
        self.assertEqual({v for v, _ in opts("journal/index.html")}, {"/journal/ko/", "/journal/en/", "/journal/ja/"})

    def test_no_bottom_lang_list_but_select_and_hreflang_stay(self):
        self.pair()
        self.ai("ja")
        self.build()
        for rel in ("journal/ja/a/index.html", "journal/ko/a/index.html", "journal/ko/index.html", "journal/index.html"):
            h = self.read(rel)
            self.assertNotIn("lang-list", h, rel)
            self.assertIn("<select", h, rel)
            self.assertIn('<link rel="alternate" hreflang="x-default"', h, rel)
            self.assertIn('<link rel="alternate" hreflang="en"', h, rel)

    def test_ai_translation_needs_translation_of(self):
        self.pair()
        self.post("a", "ja")
        self.fails("AI translation: `translation_of: en")

    def test_duplicate_language_in_group_impossible(self):
        self.pair()
        self.ai("ja")
        self.ai("ja", sub="ja")  # same file again = same language/slug
        self.assertEqual(self.run_build("--check").returncode, 0)

    def test_draft_translation_does_not_leak(self):
        self.pair()
        self.ai("ja")
        self.ai("ar", extra="draft: true\n")
        self.build()
        self.assertFalse((self.tmp / "journal/ar").exists())
        for rel in ("sitemap.xml", "llms.txt", "journal/index.html", "journal/feed.xml", "journal/en/a/index.html",
                    "journal/ko/a/index.html", "journal/ja/a/index.html", "journal/ja/index.html"):
            t = self.read(rel)
            if rel == "sitemap.xml":
                t = t.split("journal:start")[1]
            self.assertNotIn("/journal/ar/", t, rel)
            self.assertNotIn('hreflang="ar"', t, rel)
            self.assertNotIn("ar_AR", t, rel)
        self.assertNotIn("(ar)", self.read("llms.txt"))

    def test_wordcount_cjk(self):
        self.pair()
        self.ai("ja", body="これは日本語の本文です。" * 5)
        self.build()
        post = next(b for b in self.ld("journal/ja/a/index.html")[1] if b["@type"] == "BlogPosting")
        self.assertGreater(post["wordCount"], 40)


if __name__ == "__main__":
    unittest.main()
