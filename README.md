# ipe() — 홈페이지

> AI 로파이 · 힐링 음악 브랜드 `ipe()` ("idle process")의 공식 홈페이지.
> *when the process finally rests*

정적 사이트입니다. 홈은 `index.html` + 공용 `assets/idle.css`·`assets/idle.js` 로 동작하고, 저널(`/journal/`)만 의존성 없는 파이썬 스크립트로 빌드합니다.
디자인: 「The Quiet Frequency」(2026-10-20) — 밝은 화면 기본 + 다크 토글.
(이 폴더가 공개 GitHub Pages 저장소로 배포됩니다. 스튜디오 저장소 전체 개요는 루트 [`../README.md`](../README.md) 참고.)

## 파일 구성

| 파일 | 역할 |
|---|---|
| `index.html` | 사이트 본체 (12개국어 i18n · SEO · GEO · GA4 · 쇼핑 섹션 모두 포함) |
| `assets/idle.css` · `assets/idle.js` | 홈·저널 공용 스타일 / 테마 토글·모바일 메뉴 (바꾸면 각 페이지의 `?v=` 와 `scripts/build_journal.py` 의 `ASSET_V` 를 같이 올림) |
| `content/journal/*.md` | 저널 원고 (front matter + Markdown) |
| `scripts/build_journal.py` | 저널 빌드 → `journal/` · `journal/feed.xml` · `sitemap.xml` · 홈 저널 카드 |
| `journal/` | **생성물** — 손으로 고치지 않음 |
| `robots.txt` | 검색/AI 크롤러 허용 + 사이트맵 위치 |
| `sitemap.xml` | 검색엔진용 사이트맵(언어별 hreflang 포함) |
| `llms.txt` | AI/생성형 답변엔진이 읽고 인용하기 좋은 요약(GEO) |
| `.github/workflows/deploy.yml` | push 시 GitHub Pages 자동 배포 |
| `.nojekyll` | GitHub Pages의 Jekyll 처리 비활성화 |

## 배포 (GitHub Pages)

1. GitHub에서 **개인 저장소** 생성 (예: `ipe-rest`) → 이 폴더 내용을 push (기본 브랜치 `main`)
2. 저장소 **Settings → Pages → Build and deployment → Source = "GitHub Actions"** 선택
3. push 하면 Actions가 자동 배포. 기본 주소: `https://<사용자명>.github.io/<저장소명>/`
4. 커스텀 도메인(`ipe.rest`) 연결:
   - 저장소 루트에 `CNAME` 파일 생성 → 내용은 `ipe.rest` 한 줄
   - 도메인 DNS에 GitHub Pages용 레코드 추가 (Settings → Pages 안내에 따름)
   - Settings → Pages에서 도메인 입력 + **Enforce HTTPS** 체크

## Google Analytics (GA4) 연결

1. [analytics.google.com](https://analytics.google.com) → 속성 생성 → **측정 ID**(`G-XXXXXXXXXX`) 발급
2. `index.html`에서 `var GA_MEASUREMENT_ID = 'G-XXXXXXXXXX';` 의 값을 본인 ID로 교체
3. push → 배포되면 자동 추적 시작 (ID가 `G-XXXX...` placeholder면 추적 비활성)
> Google Search Console([search.google.com/search-console](https://search.google.com/search-console))도 함께 등록하면 검색 노출/색인 상태를 볼 수 있습니다.

## 곡 추가하는 법

1. `go/redirects.json` 에 트랙 코드·EN/KO YouTube 주소를 넣고 `/go/<코드>/` 페이지를 다시 만든다(스튜디오 `infra/scripts/build_go_redirects.py`).
2. `index.html`:
   - 앨범 곡 → `#album` 의 `<ol class="tracklist">` 에 `<li>` 한 줄 + 아래 플레이어 스크립트 `TRACKS` 배열에 `[코드, 제목]` 추가
   - 싱글 → `#singles` 의 `<article class="single">` 카드를 복사해 코드·제목·설명(`data-i18n` 키) 수정
   - 링크는 `data-track="<코드>"` 만 맞추면 플레이어의 EN/KR 선택에 따라 `/go/<코드>/?l=..` 로 자동 갱신된다
3. SEO/GEO: `<head>` 의 `MusicAlbum`/`ItemList` JSON-LD 와 `llms.txt` 도 같이 갱신.
4. 문구 다국어화: `data-i18n="키"` + 스크립트 `I18N`(기존 12개 언어) 또는 `EXTRA` 에 키 추가(없는 언어는 영어로 폴백).

## 저널 글 추가 → 빌드 → 커밋

1. `content/journal/<아무이름>.md` 를 만든다:
   ```
   ---
   title: 글 제목
   date: 2026-10-21
   slug: my-first-note          # 소문자·숫자·하이픈 → /journal/my-first-note/
   lang: ko                     # ko | en
   description: 한 문장 요약 (검색 설명·카드·RSS 에 쓰임)
   category: notes
   draft: false                 # true 면 어디에도 안 나감
   ---
   본문 (Markdown: ## 소제목, **굵게**, *기울임*, [링크](https://…), - 목록, > 인용, ``` 코드)
   ```
2. 검사 → 빌드 (파이썬 3.8+, 설치할 것 없음):
   ```
   python3 scripts/build_journal.py --check
   python3 scripts/build_journal.py
   ```
   `journal/<slug>/index.html`, `journal/index.html`, `journal/feed.xml`, `sitemap.xml`(journal 구간), `index.html`(홈 저널 카드 최근 3개)이 다시 만들어진다. 여러 번 돌려도 결과가 같다.
3. `git add content/journal journal sitemap.xml index.html && git commit -m "journal: <제목>"` → main push 시 자동 배포.

- 미리보기(초안 포함): 사이트를 **복사한 폴더**에서 `python3 scripts/build_journal.py --root <복사본> --drafts` — 이 결과는 커밋하지 않는다.
- 글이 0개면 목록은 「곧 첫 글이 올라옵니다」 + `noindex`, 사이트맵에서도 빠진다. 첫 글이 생기면 자동으로 색인 허용.
- 글 페이지마다 광고 칸 자리(`data-ad-slot="journal-post"`)가 하나 있다(AdSense 승인 뒤 그 안에 광고 코드를 넣는다).
- 광고 칸은 승인 전까지 숨김: `index.html`의 `<html data-ads="off">` 한 곳이 스위치다. 승인 뒤 `data-ads="on"`으로 바꾸고 `python3 scripts/build_journal.py`를 돌리면 홈·저널 글 모두 칸이 나타난다.
- 홈의 Journal 섹션은 글이 0개면 `hidden`(메뉴의 Journal 링크는 유지), 1개 이상이면 최근 3개 카드로 자동 표시된다(`build_journal.py`).

## 언어 추가하는 법

1. `<select id="lang">`에 `<option value="xx">언어명</option>` 추가
2. `<script>`의 `I18N`에 `xx: { ... }` 블록 추가 (en 키를 복사해 번역)
3. RTL 언어면 `var RTL = ['ar', 'xx'];` 에 추가, `LOCALE`에도 매핑 추가
4. `sitemap.xml`·`<head>` hreflang에도 한 줄씩 추가

## 로컬에서 미리보기

`index.html`을 브라우저로 바로 열면 됩니다(`open index.html`).
GA·외부 폰트 등 외부요청은 로컬/Artifact에선 막힐 수 있으나, 실제 배포에선 정상 동작합니다.

---
*ipe(); // be still*
