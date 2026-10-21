# idle() 홈 페이지 — 12개 언어 정적 페이지

`python3 scripts/build_journal.py` 한 번이 저널과 홈을 같이 만든다(홈은 `scripts/build_home.py`).

- 원본: `template.html`(영어 마크업, `data-i18n="키"`·`data-i18n-aria="키"`·`{{자리표시}}`) + `i18n.json`(언어별 문구, 없는 키는 영어로).
- 결과: `/<lang>/index.html` 12개(en ko ja zh es fr de pt ru ar hi id) — 각자 `html lang/dir`(ar=rtl), 자기 자신 canonical, 그 언어 title·description·og:locale(+alternate), hreflang 12 + x-default. `/index.html` 은 x-default(영어 내용, canonical `/`).
- `/index.html`·`/<lang>/index.html` 은 **생성물** — 고치지 말고 template/i18n 을 고친다. 문구를 바꾸면 `scripts/build_home.py` 의 `HOME_UPDATED` 날짜(사이트맵 lastmod)도 올린다.
- 로봇·방문자를 자동으로 보내지 않는다. 루트 `/` 에서만 저장된 선호(`localStorage ipe_lang`)·브라우저 언어를 보고 「日本語 →」 안내 띠를 띄운다(닫으면 세션 동안 숨김). 옛 `?lang=xx` 주소는 JS 로 `/xx/` 로 이동.
- 언어 선택(select)은 해당 언어 주소로 이동한다. 푸터에 12개 언어 링크(크롤러용).
- 저널 카드: 그 언어 글이 있으면 그 글, 없으면 영어(없으면 한국어) 글. 「전체 보기」는 그 언어 목록이 있으면 `/journal/<lang>/`, 없으면 `/journal/`.
- about·contact·privacy 는 en/ko 만 있어 주소 `/about/`·`/ko/about/` 그대로(hreflang en·ko·x-default).
