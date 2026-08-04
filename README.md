# ipe() — 홈페이지

> AI 로파이 · 힐링 음악 브랜드 `ipe()` ("idle process")의 공식 홈페이지.
> *when the process finally rests*

단일 파일 정적 사이트입니다. 빌드 과정이 없고 `index.html` 하나로 동작합니다.
(이 폴더가 공개 GitHub Pages 저장소로 배포됩니다. 스튜디오 저장소 전체 개요는 루트 [`../README.md`](../README.md) 참고.)

## 파일 구성

| 파일 | 역할 |
|---|---|
| `index.html` | 사이트 본체 (12개국어 i18n · SEO · GEO · GA4 · 쇼핑 섹션 모두 포함) |
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

## 음원(상품) 추가하는 법

`index.html`의 `#releases` 섹션에서 `<article class="product">` 카드를 복사해 수정:
- 커버의 `.ct` (코드 스타일 제목), `.ptitle`, 설명(`pdesc`), 포맷(`pformat`) 수정
- 구매가 가능해지면 `<button ... disabled>` 를 실제 구매/스트리밍 링크(`<a class="btn primary sm" href="...">`)로 교체
- 설명 다국어화: `data-i18n="키"` 를 붙이고 `<script>`의 `I18N` 객체 각 언어에 같은 키 추가 (없으면 영어→한국어로 자동 폴백)
- SEO/GEO: `<head>`의 `MusicAlbum` JSON-LD 블록을 복사해 새 릴리스용으로 추가하면 검색·AI 인용에 유리

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
