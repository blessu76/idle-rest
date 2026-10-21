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

## 게시 전 체크 (빌드가 대신 잡아 주는 것)

필수 칸 누락 · 폴더/`lang` 불일치 · 같은 URL 중복 · `translation_of` 없는 번역 · 없는 원문 · 같은 언어 중복 · 이미지 파일 없음. 샘플 `content/journal/ja/`·`ar/` 는 `draft: true` 구조 확인용 — 실제 번역으로 교체하거나 삭제한다.
