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


if __name__ == "__main__":
    unittest.main()
