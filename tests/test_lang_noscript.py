"""언어 선택의 <noscript> 대안 — JS 가 꺼진 환경에서도 12개 언어로 갈 수 있어야 한다.
run: python3 -m unittest discover -s tests"""
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import build_journal as bj  # noqa: E402

NOSCRIPT = re.compile(r'<noscript><span class="lang-fallback">(.*?)</span></noscript>', re.S)


class LangNoscript(unittest.TestCase):
    def test_header_select_has_noscript_links_for_every_target(self):
        targets = {l: "/%s/journal/" % l for l in bj.LANGS}
        out = bj.lang_select("en", targets)
        m = NOSCRIPT.search(out)
        self.assertIsNotNone(m, "lang_select 출력에 <noscript> 대안이 없다")
        links = re.findall(r'<a href="([^"]+)" hreflang="([^"]+)"', m.group(1))
        self.assertEqual([h for _, h in links], list(bj.LANGS))
        self.assertEqual(links[0][0], "/en/journal/")

    def test_noscript_sits_after_select_and_before_menu(self):
        out = bj.lang_select("ko", {"ko": "/ko/x/", "en": "/en/x/"})
        self.assertLess(out.index("</select>"), out.index("<noscript>"))

    def test_home_pages_contain_noscript_links(self):
        # 생성된 홈(12개 언어) 각 파일의 헤더 select 옆에 noscript 링크 줄이 있어야 한다
        for lang in bj.LANGS:
            path = REPO / lang / "index.html"
            text = path.read_text(encoding="utf-8")
            m = NOSCRIPT.search(text)
            self.assertIsNotNone(m, "%s: 홈 헤더에 <noscript> 대안이 없다" % path)
            hreflangs = re.findall(r'hreflang="([^"]+)"', m.group(1))
            self.assertEqual(hreflangs, list(bj.LANGS), "%s: 언어 링크 순서·개수" % path)

    def test_lang_fallback_has_css_rule(self):
        # no-JS 언어 링크가 헤더 아래 한 줄로 내려가도록 assets/idle.css 에 규칙이 있어야 한다
        css = (REPO / "assets" / "idle.css").read_text(encoding="utf-8")
        self.assertIn(".lang-fallback {", css)


if __name__ == "__main__":
    unittest.main()
