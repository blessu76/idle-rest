"""Publish gates: copy_review (Iris) required from 2026-11-14 for non-draft posts, in the build and in the queue; draft flag is case-insensitive."""
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_journal as bj  # noqa: E402
import build_home as bh  # noqa: E402
import publish_next as pn  # noqa: E402

os.environ["IDLE_PUBLISH_NO_NOTIFY"] = "1"
REVIEW = "copy_review: iris\ncopy_review_date: 2026-11-14\n"


def post(lang="en", date="2026-11-14", extra="", review=REVIEW, body="body"):
    tr = "translation_of: ko\n" if lang == "en" else ""
    return ("---\ntitle: T\ndate: %s\ntime: 12:00\nslug: a-slug\nlang: %s\n%sdescription: d\ncategory: behind-the-music\n%s%s---\n\n%s\n"
            % (date, lang, tr, review, extra, body))


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def parse(self, text):
        f = self.tmp / "p.md"
        f.write_text(text, encoding="utf-8")
        return bj.parse_post(f)


class BuildGate(Fixture):
    def test_missing_review_from_cutoff_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "copy_review"):
            self.parse(post(review=""))

    def test_pending_review_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "copy_review"):
            self.parse(post(review="copy_review: pending\ncopy_review_date: 2026-11-14\n"))

    def test_missing_review_date_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "copy_review_date"):
            self.parse(post(review="copy_review: iris\n"))

    def test_posts_before_cutoff_are_exempt(self):
        self.assertFalse(self.parse(post(date="2026-11-13", review=""))["draft"])

    def test_draft_is_exempt_in_any_case(self):
        for v in ("true", "True", "TRUE", "yes", "1"):
            self.assertTrue(self.parse(post(review="", extra="draft: %s\n" % v))["draft"], v)
        self.assertTrue(self.parse(post(review="", extra="Draft: True\n"))["draft"])

    def test_draft_false_is_still_gated(self):
        with self.assertRaisesRegex(ValueError, "copy_review"):
            self.parse(post(review="", extra="draft: False\n"))


class QueueGate(Fixture):
    def folder(self, en, ko):
        d = self.tmp / "01-x"
        d.mkdir()
        (d / "en.md").write_text(en, encoding="utf-8")
        (d / "ko.md").write_text(ko, encoding="utf-8")
        return d

    def pair(self, **kw):
        return post("en", date="2026-01-01", **kw), post("ko", date="2026-01-01", **kw)

    def test_valid_pair_loads(self):
        en, ko = self.pair()
        self.assertEqual(pn.load_item(self.folder(en, ko))["slug"], "a-slug")

    def test_ko_without_review_is_rejected_by_load_item(self):
        en = post("en", date="2026-01-01")
        ko = post("ko", date="2026-01-01", review="")
        with self.assertRaisesRegex(pn.HardFail, "ko.md.*copy_review"):
            pn.load_item(self.folder(en, ko))

    def test_en_without_review_is_rejected_by_load_item(self):
        en = post("en", date="2026-01-01", review="")
        with self.assertRaisesRegex(pn.HardFail, "en.md.*copy_review"):
            pn.load_item(self.folder(en, post("ko", date="2026-01-01")))

    def test_draft_case_variants_are_rejected_in_queue(self):
        for line in ("Draft: True\n", "draft: TRUE\n"):
            en, ko = self.pair(extra=line)
            d = self.folder(en, ko)
            with self.assertRaisesRegex(pn.HardFail, "draft"):
                pn.load_item(d)
            shutil.rmtree(d)

    def test_check_queue_flags_ko_without_review(self):
        self.folder(post("en", date="2026-01-01", body=" ".join(["w"] * 400)),
                    post("ko", date="2026-01-01", review="", body=" ".join(["w"] * 400)))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(pn.check_queue(self.tmp), 1)
        self.assertIn("INVALID 01-x/ko.md", out.getvalue())
        self.assertNotIn("INVALID 01-x/en.md", out.getvalue())


class FooterTerms(unittest.TestCase):
    def test_every_language_has_translated_terms_label(self):
        for lang in bj.LANGS:
            self.assertTrue(bj.ui(lang)["terms"], lang)
        self.assertEqual(bj.ui("ko")["terms"], "이용약관")
        for lang in bj.LANGS:
            if lang != "en":
                self.assertNotEqual(bj.ui(lang)["terms"], "Terms", lang)

    def test_rendered_footer_uses_translated_terms(self):
        # journal footer (build_journal.footer) and home footer (build_home.render_page) both render the shared _TERMS label
        self.assertIn("利用規約", bj.footer("ja"))
        self.assertNotIn(">Terms<", bj.footer("ja"))
        root = Path(__file__).resolve().parent.parent
        tpl = (root / bh.TEMPLATE).read_text(encoding="utf-8")
        strings = __import__("json").loads((root / bh.STRINGS).read_text(encoding="utf-8"))
        ko = bh.render_page(tpl, strings, "ko", False, [])
        self.assertIn('<a href="/ko/terms/">이용약관</a>', ko)
        self.assertNotIn(">Terms</a>", ko)


if __name__ == "__main__":
    unittest.main()
