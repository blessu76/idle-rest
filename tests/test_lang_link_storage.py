"""언어 링크 클릭 시 ipe_lang 저장 — 홈 <select> 말고 <a hreflang> 클릭 경로도 저장돼야 루트 리다이렉트가 따른다.
정적 검사(JS 런타임 없음). run: python3 -m unittest discover -s tests"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JS = (REPO / "assets/idle.js").read_text(encoding="utf-8")
LANGS = ["en", "ko", "ja", "zh", "es", "fr", "de", "pt", "ru", "ar", "hi", "id"]
LANG_ANCHOR = re.compile(r'<a [^>]*hreflang="([a-z]{2})"[^>]*>')


class LangLinkStorage(unittest.TestCase):
    def test_idle_js_saves_ipe_lang_on_hreflang_link_click(self):
        self.assertIn("closest('a[hreflang]')", JS)
        self.assertIn("localStorage.setItem('ipe_lang', a.getAttribute('hreflang'))", JS)
        self.assertIn("addEventListener('click'", JS)

    def test_listener_only_accepts_the_twelve_language_codes(self):
        m = re.search(r"var LANG_CODES = \[(.*?)\];", JS)
        self.assertIsNotNone(m)
        self.assertEqual(re.findall(r"'([a-z]{2})'", m.group(1)), LANGS)

    def test_save_is_guarded_by_try(self):
        i = JS.index("localStorage.setItem('ipe_lang', a.getAttribute")
        self.assertIn("try {", JS[i - 80:i])
        self.assertIn("catch (err) {}", JS[i:i + 120])

    def test_every_page_with_language_links_loads_idle_js(self):
        # 언어 링크가 있는 페이지는 전부 idle.js 를 불러야 위임 리스너가 붙는다
        missing = []
        for path in REPO.rglob("*.html"):
            if any(part in ("vendor", "tests", ".git") for part in path.relative_to(REPO).parts):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            hits = [m.group(1) for m in LANG_ANCHOR.finditer(text) if m.group(1) in LANGS]
            if hits and "/assets/idle.js" not in text:
                missing.append(str(path.relative_to(REPO)))
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
