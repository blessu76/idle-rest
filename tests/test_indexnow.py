import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import indexnow  # noqa: E402

KEY = "0123456789abcdef0123456789abcdef"
SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url><loc>https://example.test/</loc>
    <xhtml:link rel="alternate" hreflang="ko" href="https://example.test/?lang=ko"/></url>
  <url><loc>https://example.test/a/</loc></url>
  <url><loc>https://example.test/a/</loc></url>
</urlset>
"""


class IndexNow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def test_find_key(self):
        (self.dir / "notes.txt").write_text("x\n")
        (self.dir / (KEY + ".txt")).write_text(KEY + "\n")
        self.assertEqual(indexnow.find_key(self.dir), KEY)

    def test_find_key_ignores_mismatch_and_long_names(self):
        (self.dir / (KEY + ".txt")).write_text("other\n")
        (self.dir / ("a" * 64 + ".txt")).write_text("a" * 64)
        with self.assertRaises(SystemExit):
            indexnow.find_key(self.dir)

    def test_sitemap_urls(self):
        (self.dir / "sitemap.xml").write_text(SITEMAP)
        self.assertEqual(indexnow.sitemap_urls(self.dir / "sitemap.xml"),
                         ["https://example.test/", "https://example.test/a/"])

    def test_payload(self):
        p = indexnow.build_payload(KEY, ["https://example.test/", "https://example.test/a/"])
        self.assertEqual(p["host"], "example.test")
        self.assertEqual(p["key"], KEY)
        self.assertEqual(p["keyLocation"], "https://example.test/%s.txt" % KEY)
        self.assertEqual(len(p["urlList"]), 2)

    def test_payload_rejects_empty_and_mixed_hosts(self):
        with self.assertRaises(SystemExit):
            indexnow.build_payload(KEY, [])
        with self.assertRaises(SystemExit):
            indexnow.build_payload(KEY, ["https://a.test/", "https://b.test/"])

    def test_dry_run_sends_nothing(self):
        (self.dir / "sitemap.xml").write_text(SITEMAP)
        (self.dir / (KEY + ".txt")).write_text(KEY)
        orig = indexnow.send
        indexnow.send = lambda *a, **k: self.fail("network call in dry-run")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(indexnow.main(["--root", str(self.dir), "--dry-run"]), 0)
        finally:
            indexnow.send = orig

    def test_repo_has_valid_key_and_sitemap(self):
        key = indexnow.find_key(ROOT)
        urls = indexnow.sitemap_urls(ROOT / "sitemap.xml")
        indexnow.build_payload(key, urls)


if __name__ == "__main__":
    unittest.main()


class ChangedUrls(unittest.TestCase):
    def test_changed_pages_only_public_indexable(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            git = lambda *a: subprocess.run(["git", "-C", d, "-c", "user.email=t@t", "-c", "user.name=t"] + list(a), check=True, capture_output=True)
            git("init", "-q")
            (root / "CNAME").write_text("example.test\n")
            page = lambda body, robots="index, follow": '<html><head><meta name="robots" content="%s"></head><body>%s</body></html>' % (robots, body)
            for rel in ("index.html", "a/index.html", "b/index.html", "go/x/index.html", "content/n/index.html", "old/index.html"):
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text(page("v1", "noindex" if rel == "old/index.html" else "index, follow"))
            git("add", "-A")
            git("commit", "-qm", "one")
            for rel in ("index.html", "a/index.html", "go/x/index.html", "content/n/index.html", "old/index.html"):
                (root / rel).write_text(page("v2", "noindex" if rel == "old/index.html" else "index, follow"))
            (root / "n/new").mkdir(parents=True)
            (root / "n/new/index.html").write_text(page("new"))
            git("add", "-A")
            git("commit", "-qm", "two")
            want = ["https://example.test/", "https://example.test/a/", "https://example.test/n/new/"]
            self.assertEqual(indexnow.changed_urls(root, "HEAD~1"), want)
            self.assertEqual(indexnow.changed_urls(root, "0" * 40), want)  # unknown/zero rev -> HEAD~1


class Today(unittest.TestCase):
    def test_modified_only_that_day(self):
        with tempfile.TemporaryDirectory() as d:
            sm = Path(d) / "sitemap.xml"
            sm.write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                          '<url><loc>https://example.test/a/</loc><lastmod>2026-10-29</lastmod></url>'
                          '<url><loc>https://example.test/b/</loc><lastmod>2026-10-28</lastmod></url>'
                          '<url><loc>https://example.test/c/</loc></url></urlset>')
            self.assertEqual(indexnow.sitemap_urls_modified(sm, "2026-10-29"), ["https://example.test/a/"])
            self.assertEqual(indexnow.sitemap_urls_modified(sm, "2000-01-01"), [])
