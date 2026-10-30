"""Image speed checks (WebP siblings, <picture>, width/height, LCP priority) — run: python3 -m unittest discover -s tests"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


class Images(unittest.TestCase):
    def test_every_jpg_has_webp(self):
        jpgs = list((REPO / "assets").rglob("*.jpg"))
        self.assertTrue(jpgs)
        for j in jpgs:
            w = j.with_suffix(".webp")
            self.assertTrue(w.is_file(), w)
            self.assertLess(w.stat().st_size, j.stat().st_size, w)

    def test_icon_is_small(self):
        self.assertLess((REPO / "idle-app-icon.png").stat().st_size, 600_000)
        self.assertTrue((REPO / "idle-app-icon.webp").is_file())

    def test_home_lcp_cover(self):
        h = (REPO / "index.html").read_text()
        self.assertRegex(h, r'<link rel="preload" as="image" href="/assets/covers/dear-you-titled-660\.webp" imagesrcset="[^"]*dear-you-titled-660\.webp 660w[^"]*" imagesizes="[^"]+" type="image/webp" fetchpriority="high">')
        m = re.search(r'<picture><source type="image/webp" srcset="[^"]+\.webp[^"]*"[^>]*><img class="art-cover"[^>]*>', h)
        self.assertTrue(m)
        self.assertIn('fetchpriority="high"', m.group(0))
        self.assertNotIn('loading="lazy"', m.group(0))

    def test_home_images_sized_and_lazy_below_fold(self):
        h = (REPO / "index.html").read_text()
        for tag in re.findall(r"<img [^>]*>", h):
            if "/assets/covers/" in tag or "idle-app-icon" in tag:
                self.assertIn("width=", tag)
                self.assertIn("height=", tag)
                if "art-cover" not in tag:
                    self.assertIn('loading="lazy"', tag)

    def test_journal_posts_use_picture_webp(self):
        p = REPO / "journal/en/english-female-korean-male/index.html"
        if not p.exists():
            self.skipTest("post path differs")
        h = p.read_text()
        imgs = re.findall(r'<picture><source type="image/webp" srcset="(/assets/journal/[^"]+\.webp)"><img [^>]*width="\d+" height="\d+"[^>]*loading="lazy" decoding="async"></picture>', h)
        self.assertTrue(imgs)
        for w in imgs:
            self.assertTrue((REPO / w.lstrip("/")).is_file(), w)


if __name__ == "__main__":
    unittest.main()
