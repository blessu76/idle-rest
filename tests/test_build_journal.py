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
slug: %(s)s
lang: %(l)s
description: A test post.
category: notes
translation: %(o)s
%(extra)s---

Intro with an [article](https://news.example.com/a) and a [video](https://youtu.be/x).

## Section

![Cover alt](/assets/journal/%(s)s/c.png "Cap")
"""


class BuildJournal(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for f in ("index.html", "sitemap.xml", "llms.txt"):
            shutil.copy(REPO / f, self.tmp / f)
        (self.tmp / "content/journal").mkdir(parents=True)
        (self.tmp / "assets/journal/a-en").mkdir(parents=True)
        (self.tmp / "assets/journal/a-en/c.png").write_bytes(png(30, 20))
        (self.tmp / "assets/journal/a-ko").mkdir(parents=True)
        (self.tmp / "assets/journal/a-ko/c.png").write_bytes(png(30, 20))
        extra_en = "keywords: x, y\nsongs: Song A @ https://youtu.be/abc | Song B\nalbum: Alb @ https://idle.ipe.rest/#album\ntranslation_of: a-ko\n"
        (self.tmp / "content/journal/a-en.md").write_text(POST % dict(t="EN", s="a-en", l="en", o="a-ko", extra=extra_en), encoding="utf-8")
        (self.tmp / "content/journal/a-ko.md").write_text(POST % dict(t="KO", s="a-ko", l="ko", o="a-en", extra=""), encoding="utf-8")
        r = subprocess.run([sys.executable, str(REPO / "scripts/build_journal.py"), "--root", str(self.tmp)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def ldjson(self, rel):
        h = (self.tmp / rel).read_text(encoding="utf-8")
        return h, [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', h, re.S)]

    def test_post_jsonld_and_html(self):
        h, blocks = self.ldjson("journal/a-en/index.html")
        post = next(b for b in blocks if b["@type"] == "BlogPosting")
        for k in ("headline", "datePublished", "author", "publisher", "image", "inLanguage", "wordCount", "keywords"):
            self.assertIn(k, post)
        self.assertEqual(post["image"]["width"], 30)
        self.assertEqual(post["translationOfWork"]["inLanguage"], "ko")
        self.assertEqual([a["@type"] for a in post["about"]], ["MusicAlbum", "MusicRecording", "MusicRecording"])
        self.assertEqual(post["about"][1]["sameAs"], "https://youtu.be/abc")
        self.assertEqual([c["url"] for c in post["citation"]], ["https://news.example.com/a"])  # youtube not cited
        self.assertIn("BreadcrumbList", [b["@type"] for b in blocks])
        self.assertIn('hreflang="x-default"', h)
        self.assertIn('<figure><img src="/assets/journal/a-en/c.png" alt="Cover alt" width="30" height="20" loading="lazy"', h)
        self.assertIn('<meta property="og:image" content="https://idle.ipe.rest/assets/journal/a-en/c.png">', h)
        ko = self.ldjson("journal/a-ko/index.html")[1][0]
        self.assertEqual(ko["workTranslation"]["inLanguage"], "en")
        self.assertNotIn("keywords", ko)  # optional fields are omitted, not empty

    def test_list_sitemap_llms(self):
        _, blocks = self.ldjson("journal/index.html")
        self.assertEqual({"Blog", "ItemList", "BreadcrumbList"}, {b["@type"] for b in blocks})
        root = ET.parse(self.tmp / "sitemap.xml").getroot()
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml",
              "i": "http://www.google.com/schemas/sitemap-image/1.1"}
        row = next(u for u in root.findall("s:url", ns) if u.find("s:loc", ns).text.endswith("/a-ko/"))
        self.assertEqual({l.get("hreflang") for l in row.findall("x:link", ns)}, {"ko", "en", "x-default"})
        self.assertEqual(row.find("i:image/i:loc", ns).text, "https://idle.ipe.rest/assets/journal/a-ko/c.png")
        self.assertIsNotNone(row.find("s:lastmod", ns))
        llms = (self.tmp / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("## Journal", llms)
        self.assertIn("https://idle.ipe.rest/journal/a-en/", llms)
        self.assertIn('Please attribute to "idle() (the music of ipe())"', llms)

    def test_idempotent(self):
        before = {p: p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()}
        subprocess.run([sys.executable, str(REPO / "scripts/build_journal.py"), "--root", str(self.tmp)], check=True, capture_output=True)
        self.assertEqual(before, {p: p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()})


MINIMAL = """---
title: Min
date: 2026-10-22
slug: %(s)s
lang: en
description: Only the required fields.
category: notes
%(extra)s---

Plain body, no image, no link.
"""


class Validation(unittest.TestCase):
    """Fresh site copy per test; write posts, then run the build / --check and inspect the result."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for f in ("index.html", "sitemap.xml", "llms.txt"):
            shutil.copy(REPO / f, self.tmp / f)
        (self.tmp / "content/journal").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def post(self, slug, extra="", body=None, draft=False):
        text = MINIMAL % dict(s=slug, extra=extra + ("draft: true\n" if draft else ""))
        if body:
            text += "\n" + body
        (self.tmp / "content/journal" / ("%s.md" % slug)).write_text(text, encoding="utf-8")

    def run_build(self, *flags):
        return subprocess.run([sys.executable, str(REPO / "scripts/build_journal.py"), "--root", str(self.tmp), *flags],
                              capture_output=True, text=True)

    def test_post_without_optional_fields(self):
        self.post("plain")
        self.assertEqual(self.run_build("--check").returncode, 0)
        r = self.run_build()
        self.assertEqual(r.returncode, 0, r.stderr)
        h = (self.tmp / "journal/plain/index.html").read_text(encoding="utf-8")
        blocks = [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', h, re.S)]
        post = next(b for b in blocks if b["@type"] == "BlogPosting")
        for k in ("keywords", "about", "citation", "translationOfWork", "workTranslation"):
            self.assertNotIn(k, post)
        self.assertEqual(post["image"], "https://idle.ipe.rest/og-image.png")
        self.assertIn('hreflang="x-default" href="https://idle.ipe.rest/journal/plain/"', h)

    def test_missing_image_fails(self):
        self.post("front", extra="image: /assets/journal/front/nope.jpg\n")
        self.post("inline", body="![x](/assets/journal/inline/nope.jpg)\n")
        for flags in (("--check",), ()):
            r = self.run_build(*flags)
            self.assertEqual(r.returncode, 1, flags)
            self.assertIn("front.md: image file not found: /assets/journal/front/nope.jpg", r.stderr)
            self.assertIn("inline.md: image file not found: /assets/journal/inline/nope.jpg", r.stderr)
        self.assertFalse((self.tmp / "journal").exists())  # nothing half-written

    def test_existing_image_ok_and_external_image_skipped(self):
        (self.tmp / "assets/journal/ok").mkdir(parents=True)
        (self.tmp / "assets/journal/ok/c.png").write_bytes(png(4, 4))
        self.post("ok", extra="image: https://example.com/c.png\n", body="![x](/assets/journal/ok/c.png)\n")
        self.assertEqual(self.run_build("--check").returncode, 0)

    def assert_pair_fails(self, expect):
        r = self.run_build("--check")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn(expect, r.stderr)

    def test_translation_not_mutual_fails(self):
        self.post("a", extra="translation: b\n")
        self.post("b")
        self.assert_pair_fails("a.md: translation 'b' does not point back")

    def test_translation_self_reference_fails(self):
        self.post("a", extra="translation: a\ntranslation_of: a\n")
        self.assert_pair_fails("a.md: translation points at the post itself")

    def test_translation_to_draft_fails(self):
        self.post("a", extra="translation: b\n")
        self.post("b", extra="translation: a\n", draft=True)
        self.assert_pair_fails("a.md: translation refers to draft post 'b'")

    def test_translation_of_without_translation_fails(self):
        self.post("a", extra="translation_of: b\n")
        self.post("b", extra="translation: a\n")
        self.assert_pair_fails("a.md: translation_of 'b' needs `translation: b` too")

    def test_translation_unknown_slug_fails(self):
        self.post("a", extra="translation: ghost\n")
        self.assert_pair_fails("a.md: translation refers to unknown slug 'ghost'")

    def test_valid_pair_ok(self):
        self.post("a", extra="translation: b\n")
        self.post("b", extra="translation: a\ntranslation_of: a\n")
        self.assertEqual(self.run_build("--check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
