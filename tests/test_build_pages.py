"""Tests for scripts/build_pages.py (About / Contact / Privacy in 12 languages) — run: python3 -m unittest discover -s tests"""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import build_journal as bj  # noqa: E402
import build_pages as bp  # noqa: E402

LANGS = list(bj.LANGS)
TRANSLATED = [l for l in LANGS if l not in bj.MAIN_LANGS]
SLUGS = bp.SLUGS
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
ALT = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">')
CANON = re.compile(r'<link rel="canonical" href="([^"]+)">')


class Built(unittest.TestCase):
    """one fresh site copy per class, built once with build_journal.py (which also builds the pages)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        for f in ("index.html", "sitemap.xml", "llms.txt"):
            shutil.copy(REPO / f, cls.tmp / f)
        shutil.copytree(REPO / "content/home", cls.tmp / "content/home")
        shutil.copytree(REPO / "content/pages", cls.tmp / "content/pages")
        (cls.tmp / "content/journal").mkdir(parents=True)
        cls.build()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    @classmethod
    def run_script(cls, script, *args):
        return subprocess.run([sys.executable, str(REPO / "scripts" / script), "--root", str(cls.tmp), *args], capture_output=True, text=True)

    @classmethod
    def build(cls):
        r = cls.run_script("build_journal.py")
        assert r.returncode == 0, r.stderr

    def page(self, lang, slug):
        return (self.tmp / (lang or "") / slug / "index.html").read_text(encoding="utf-8")


class Pages(Built):
    def test_all_39_pages_exist(self):
        for slug in SLUGS:
            for lang in [None] + LANGS:
                self.assertTrue((self.tmp / (lang or "") / slug / "index.html").is_file(), (lang, slug))

    def test_canonical_is_itself_and_hreflang_is_absolute_and_symmetric(self):
        want_langs = LANGS + ["x-default"]
        for slug in SLUGS:
            sets = []
            for lang in [None] + LANGS:
                h = self.page(lang, slug)
                self.assertEqual(CANON.findall(h), [bp.page_url(lang, slug)], (lang, slug))
                alts = ALT.findall(h)
                self.assertEqual([l for l, _ in alts], want_langs, (lang, slug))
                for l, u in alts:
                    self.assertEqual(u, bp.page_url(None if l == "x-default" else l, slug))
                    self.assertTrue(u.startswith("https://idle.ipe.rest/"))
                sets.append(alts)
                self.assertIn(bp.page_url(lang, slug), [u for l, u in alts if l == (lang or "x-default")])
            self.assertTrue(all(s == sets[0] for s in sets), slug)  # every page of a slug lists the same 13 alternates

    def test_html_lang_dir_and_rtl(self):
        for slug in SLUGS:
            for lang in LANGS:
                h = self.page(lang, slug)
                self.assertIn('<html lang="%s" dir="%s"' % (lang, "rtl" if lang == "ar" else "ltr"), h)
            self.assertIn('<html lang="en" dir="ltr"', self.page(None, slug))

    def test_ai_notice_only_on_the_ten_translations(self):
        for slug in SLUGS:
            for lang in LANGS:
                h = self.page(lang, slug)
                if lang in TRANSLATED:
                    self.assertEqual(h.count('class="ai-note"'), 1, (lang, slug))
                    # first thing in the content, with links to both originals
                    self.assertLess(h.index('class="ai-note"'), h.index('class="page-head"'))
                    self.assertIn('href="/en/%s/"' % slug, h.split('class="page-head"')[0].split('class="ai-note"')[1])
                    self.assertIn('href="/ko/%s/"' % slug, h.split('class="page-head"')[0].split('class="ai-note"')[1])
                else:
                    self.assertNotIn("ai-note", h, (lang, slug))
            self.assertNotIn("ai-note", self.page(None, slug))

    def test_privacy_notice_says_originals_prevail(self):
        # the privacy notice carries one more sentence than the about/contact one
        for lang in TRANSLATED:
            notes = {}
            for slug in SLUGS:
                m = re.search(r'<p class="ai-note">(.*?)</p>', self.page(lang, slug), re.S)
                notes[slug] = len(re.sub(r"<[^>]+>", "", m.group(1)))
            self.assertGreater(notes["privacy"], notes["about"] + 20, lang)

    def test_operator_and_email_are_filled_not_translated(self):
        for slug in SLUGS:
            for lang in LANGS:
                h = self.page(lang, slug)
                self.assertNotIn("{{", h, (lang, slug))
                if slug in ("contact", "privacy"):
                    self.assertIn("Davy Kim (ipe Studio)", h)
                    self.assertIn('href="mailto:ipe.haven@gmail.com"', h)
        self.assertIn('<bdi class="ltr">Davy Kim (ipe Studio)</bdi>', self.page("ar", "contact"))
        self.assertIn('class="ltr"', self.page("ar", "contact").split("mailto:")[1][:60])

    def test_language_select_top_right_and_no_bottom_list(self):
        for slug in SLUGS:
            for lang in [None] + LANGS:
                h = self.page(lang, slug)
                sel = re.search(r'<select class="lang" id="lang"[^>]*data-nav>(.*?)</select>', h, re.S)
                self.assertIsNotNone(sel, (lang, slug))
                opts = re.findall(r'<option value="([^"]+)"( selected)?>([A-Z]+)</option>', sel.group(1))
                self.assertEqual([o[2].lower() for o in opts], LANGS)
                for v, _, code in opts:
                    self.assertEqual(v, "/%s/%s/" % (code.lower(), slug))
                    self.assertTrue((self.tmp / v.strip("/") / "index.html").is_file(), v)
                self.assertEqual([o[2].lower() for o in opts if o[1]], [lang or "en"])
                self.assertNotIn("lang-list", h)

    def test_footer_links_follow_the_page_language(self):
        for lang in LANGS:
            h = self.page(lang, "about")
            for s in SLUGS:
                self.assertIn('<li><a href="/%s/%s/">' % (lang, s), h, lang)
        h = self.page(None, "contact")
        for s in SLUGS:
            self.assertIn('<li><a href="/%s/">' % s, h)

    def test_x_default_is_a_language_chooser_without_forced_redirect(self):
        for slug in SLUGS:
            h = self.page(None, slug)
            grid = re.search(r'<ul class="lang-grid">(.*?)</ul>', h, re.S).group(1)
            self.assertEqual(re.findall(r'<a class="lang-card" href="([^"]+)" hreflang="([^"]+)"', grid),
                             [("/%s/%s/" % (l, slug), l) for l in LANGS])  # plain links, visible without JS
            self.assertIn("location.replace('/' + q + '/' + SLUG + '/'", h)  # old ?lang=xx
            self.assertEqual(h.count("location.replace("), 1)  # nothing else redirects: the browser language is only suggested
            self.assertIn('id="langHint" hidden', h)
            self.assertIn("ipe_hint_off", h)
            self.assertNotIn("NAMES[q]", h)  # ?lang=constructor must not match an Object.prototype key
            self.assertIn("hasOwnProperty.call(NAMES, q)", h)
        for lang in LANGS:
            self.assertNotIn("langHint", self.page(lang, "about"))

    def test_generated_comment_names_build_pages(self):
        for slug in SLUGS:
            for lang in [None] + LANGS:
                self.assertIn("<!-- generated by scripts/build_pages.py", self.page(lang, slug))

    def test_root_and_language_pages_have_the_right_content(self):
        self.assertIn("About idle()", self.page("en", "about"))
        self.assertIn("idle() 소개", self.page("ko", "about"))
        self.assertIn("<h1>About idle()</h1>", self.page(None, "about"))
        self.assertIn("개인정보처리방침", self.page("ko", "privacy"))

    def test_sitemap_has_39_page_urls_and_check_passes(self):
        locs = [u.findtext("s:loc", namespaces=NS) for u in ET.parse(self.tmp / "sitemap.xml").getroot().findall("s:url", NS)]
        for slug in SLUGS:
            for lang in [None] + LANGS:
                self.assertEqual(locs.count(bp.page_url(lang, slug)), 1, (lang, slug))
        r = self.run_script("check_sitemap.py")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_check_sitemap_fails_for_a_missing_page_file(self):
        (self.tmp / "ja" / "privacy" / "index.html").rename(self.tmp / "ja" / "privacy" / "gone.html")
        try:
            r = self.run_script("check_sitemap.py")
            self.assertEqual(r.returncode, 1)
            self.assertIn("no file for sitemap URL", r.stderr)
        finally:
            (self.tmp / "ja" / "privacy" / "gone.html").rename(self.tmp / "ja" / "privacy" / "index.html")

    def test_llms_lists_all_pages(self):
        t = (self.tmp / "llms.txt").read_text(encoding="utf-8")
        for slug in SLUGS:
            for lang in [None] + LANGS:
                self.assertIn(bp.page_url(lang, slug), t)
        self.assertEqual(t.count("pages:llms:start"), 1)

    def test_idempotent(self):
        files = [p for p in self.tmp.rglob("*") if p.is_file()]
        before = {p: p.read_bytes() for p in files}
        self.build()
        self.assertEqual({p: p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()}, before)


class Sources(unittest.TestCase):
    """--check on broken sources: a translation may not add/remove anything."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(REPO / "content/pages", self.tmp / "content/pages")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def check(self):
        return subprocess.run([sys.executable, str(REPO / "scripts/build_pages.py"), "--root", str(self.tmp), "--check"], capture_output=True, text=True)

    def edit(self, rel, fn):
        f = self.tmp / "content/pages" / rel
        f.write_text(fn(f.read_text(encoding="utf-8")), encoding="utf-8")

    def test_repo_sources_are_valid(self):
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_missing_file(self):
        (self.tmp / "content/pages/de/about.html").unlink()
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("de/about.html: missing", r.stderr)

    def test_translation_with_an_extra_paragraph_fails(self):
        self.edit("fr/contact.html", lambda t: t + "<p>extra</p>\n")
        r = self.check()
        self.assertEqual(r.returncode, 1)
        self.assertIn("tags differ from English", r.stderr)

    def test_translation_with_a_changed_link_fails(self):
        self.edit("es/privacy.html", lambda t: t.replace("https://adssettings.google.com", "https://example.com", 1))
        self.assertIn("links differ from English", self.check().stderr)

    def test_translation_dropping_a_placeholder_fails(self):
        self.edit("zh/contact.html", lambda t: t.replace("{{REPLY_DAYS}}", "10", 1))
        self.assertIn("placeholders differ from English", self.check().stderr)

    def test_literal_operator_or_email_fails(self):
        self.edit("pt/about.html", lambda t: t.replace("{{EMAIL}}", "ipe.haven@gmail.com", 1))
        self.assertIn("write {{OPERATOR}}/{{EMAIL}}", self.check().stderr)

    def test_translation_without_ai_notice_fails(self):
        self.edit("ru/about.html", lambda t: re.sub(r"^ai:.*\n", "", t, flags=re.M))
        self.assertIn("needs an ai: line", self.check().stderr)

    def test_ai_notice_must_link_the_originals(self):
        self.edit("id/privacy.html", lambda t: t.replace("{{ORIGINALS}}", "", 1))
        self.assertIn("ai: line must contain {{ORIGINALS}}", self.check().stderr)

    def test_original_must_not_have_an_ai_notice(self):
        self.edit("ko/about.html", lambda t: t.replace("\n---\n", "\nai: AI 번역\n---\n", 1))
        self.assertIn("must not carry an ai: line", self.check().stderr)


class SiteLinks(unittest.TestCase):
    """the committed site: every internal link of every page resolves to a real file (root included)."""

    def test_internal_links_resolve(self):
        bad = []
        skip = {".git", ".github", "content", "scripts", "tests"}
        for f in REPO.rglob("*.html"):
            if skip & set(f.relative_to(REPO).parts[:1]):
                continue
            text = f.read_text(encoding="utf-8")
            for m in re.finditer(r'(?:href|src|action)="(/[^"#?]*)', text):
                path = m.group(1)
                if path.startswith("//") or "'" in path:  # protocol-relative, or a JS string (e.g. '/' + lang + '/')
                    continue
                target = REPO / path.lstrip("/")
                if not (target.is_file() or (target / "index.html").is_file()):
                    bad.append("%s -> %s" % (f.relative_to(REPO), path))
        self.assertEqual(sorted(set(bad)), [])

    def test_committed_pages_are_up_to_date(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            for f in ("index.html", "sitemap.xml", "llms.txt"):
                shutil.copy(REPO / f, tmp / f)
            shutil.copytree(REPO / "content/pages", tmp / "content/pages")
            shutil.copytree(REPO / "content/home", tmp / "content/home")
            shutil.copytree(REPO / "content/journal", tmp / "content/journal")
            shutil.copytree(REPO / "assets", tmp / "assets")
            r = subprocess.run([sys.executable, str(REPO / "scripts/build_pages.py"), "--root", str(tmp)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            stale = [str(p.relative_to(tmp)) for slug in SLUGS for l in [""] + LANGS
                     for p in [tmp / l / slug / "index.html"] if p.read_bytes() != (REPO / l / slug / "index.html").read_bytes()]
            self.assertEqual(stale, [], "run: python3 scripts/build_journal.py")
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
