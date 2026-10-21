# idle() 저널 원고 형식 (12개 언어)

빌드: `python3 scripts/build_journal.py` (검증만: `--check`, 초안 미리보기: 사이트 **복사본**에서 `--root /tmp/x --drafts`). 테스트: `python3 -m unittest discover -s tests`.

## 언어와 URL

| 구분 | 언어 | 파일 | URL |
|---|---|---|---|
| 원문(사람 감수) | `ko`, `en` | `content/journal/<slug>.md` | `/journal/<slug>/` (기존 그대로) |
| AI 번역 | `ja zh es fr de pt ru ar hi id` | `content/journal/<lang>/<slug>.md` | `/<lang>/journal/<slug>/` |

- 언어별 목록: `/<lang>/journal/` (그 언어 글이 1편 이상일 때만 생성). ko+en 목록은 `/journal/`(그대로).
- 번역이 없는 언어는 페이지·사이트맵·hreflang·llms.txt 어디에도 나오지 않는다(빈 페이지·폴백 없음).
- 번역 글의 `slug` 는 **원문 slug 와 같게** 두는 것을 권장(같은 폴더 안에서만 유일하면 된다).

## 번역 파일 front matter (필수)

```
---
title: (번역된 제목)
date: 2026-10-23              # 원문과 같은 날짜
slug: ten-letters-one-skeleton-en   # 권장: 원문 slug
lang: ja                      # 폴더 이름과 같아야 한다
description: (번역된 한 문장)
category: behind-the-music    # 원문과 같게
translation_of: ten-letters-one-skeleton-en   # ko/en 원문의 slug — 이것 하나만. `translation:` 은 쓰지 않는다
---
```

선택 칸(`updated`, `image`, `image_alt`, `keywords`, `album`, `songs`, `citations`)은 원문과 같은 의미. 본문의 `![](/assets/journal/<원문slug>/x.jpg)` 이미지는 원문 것을 그대로 쓰고 `image_alt`·캡션만 번역한다.

- 원문 파일(ko/en)은 **고칠 필요 없다.** hreflang·`workTranslation` 은 `translation_of` 로 자동 연결된다.
- `translation_of` 는 ko/en 원문만 가리킨다(번역의 번역 금지). 한 번역 그룹에 같은 언어 글은 1개.
- 글마다 자동으로 나오는 것: 「AI 번역」 표시 + 원문 링크(그 언어 문구), `inLanguage`, `translationOfWork`(번역→원문), `workTranslation`(원문→번역들), hreflang 12개+x-default 상호 참조, `og:locale`/`og:locale:alternate`, 사이트맵 `xhtml:link`·`image:image`, llms.txt 언어별 섹션, 다른 언어 링크 목록. `ar` 는 `dir="rtl"`.
- 마크다운은 기존 부분집합(제목·문단·목록·인용·코드·이미지·링크). 번역하지 말 것: 곡/앨범 제목, `idle()`, `ipe()`, 코드, URL.
- 새 UI 문구(목록 제목·버튼 등)는 `scripts/build_journal.py` 의 `_T` 표에 언어별로 들어 있다.

## ko/en 원문 쌍 (기존 규칙)

양쪽 글에 `translation: <상대 slug>`, 번역본(보통 en)에는 `translation_of: <원문 slug>` 도 함께. 빌드가 비대칭·자기참조·없는 slug·draft 참조를 오류로 잡는다.

## 게시 절차

1. 원고(ko/en + `<lang>/`) 작성 → `python3 scripts/build_journal.py` (빌드가 형식 오류를 잡는다).
2. **`python3 scripts/check_sitemap.py` 통과 필수** — sitemap.xml 유효 · 공개 저널 URL(목록·언어별 목록·글) 누락 0 · hreflang 상호참조+x-default. 실패하면 exit 1(게시 금지).
3. `python3 -m unittest discover -s tests` 통과 → 커밋·push → 배포 후 `python3 scripts/check_sitemap.py --live`(모든 URL HTTP 200).

빌드가 대신 잡아 주는 것: 필수 칸 누락 · 폴더/`lang` 불일치 · 같은 URL 중복 · `translation_of` 없는 번역 · 없는 원문 · 같은 언어 중복 · 이미지 파일 없음. `draft: true` 번역은 sitemap·llms·목록·hreflang·`/<lang>/` 폴더 어디에도 나오지 않는다(테스트로 보장).
`content/`·`scripts/`·`tests/` 는 배포 산출물에서 제외된다(원고 .md 가 공개 URL 이 되지 않음).

## 새 글마다 10개 언어 번역 만드는 절차

1. ko/en 원문을 확정·게시 준비(원문은 사람이 감수한 것).
2. **EN 원문 기준**으로 10개 언어(`ja zh es fr de pt ru ar hi id`) 번역을 만든다 — 고유명사·곡명·앨범명·`idle()`·`ipe()`·코드·URL 은 원문 표기 그대로, 의미·사실을 덧붙이지 않는다. 직원 이름은 원문에 있을 때만 쓴다.
3. 각 번역을 `content/journal/<lang>/<원문slug>.md` 로 저장: front matter 는 원문과 같은 `date`·`category`·`album`, `slug` = EN 원문 slug, `lang`, `translation_of: <EN 원문 slug>`, 번역한 `title`·`description`·`keywords`. 본문은 문단·제목 수·순서를 원문과 똑같이(그림 줄 `![](/assets/journal/...)` 은 그대로 두고 alt·캡션만 번역). 원문 본문의 「다른 언어로 읽기」 링크 줄은 번역하지 않는다(AI 번역 표시가 원문 링크를 자동으로 붙인다).
4. `python3 scripts/build_journal.py` → `python3 scripts/check_sitemap.py` → `python3 -m unittest discover -s tests` 통과 후 커밋.
5. 번역을 AI 에이전트에게 맡길 때는 위 2~3 을 그대로 브리프에 붙인다(언어별 에이전트 병렬 가능, 한 에이전트 = 한 언어 = 파일 하나).
