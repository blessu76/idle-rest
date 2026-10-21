# idle() 저널 원고 형식 (12개 언어)

빌드: `python3 scripts/build_journal.py` (검증만: `--check`, 초안 미리보기: 사이트 **복사본**에서 `--root /tmp/x --drafts`). 테스트: `python3 -m unittest discover -s tests`.

## 파일 구조와 URL — 12개 언어 모두 같은 규칙

원고는 **`content/journal/<lang>/<slug>.md`** (ko·en 포함, 폴더 = 언어, 파일명 = slug). 한 글의 모든 언어판은 **같은 slug**.

| 언어 | 구분 | 파일 | URL |
|---|---|---|---|
| `ko`, `en` | 원문(사람 감수) | `content/journal/ko/<slug>.md` · `content/journal/en/<slug>.md` | `/journal/ko/<slug>/` · `/journal/en/<slug>/` |
| `ja zh es fr de pt ru ar hi id` | AI 번역 | `content/journal/<lang>/<slug>.md` | `/journal/<lang>/<slug>/` |

- 언어별 목록 `/journal/<lang>/`(그 언어 글이 1편 이상일 때만 생성). `/journal/` = x-default 허브(언어 링크 + ko/en 원문 목록).
- canonical = 각 페이지 자기 자신. hreflang = 그 글이 있는 언어 전부 + x-default(en, 없으면 ko), 서로 상호참조. 번역이 없는 언어는 페이지·sitemap·hreflang·llms.txt 어디에도 나오지 않는다(빈 페이지·폴백 없음).
- slug 는 `[a-z0-9-]+`, 언어 코드(`ja` 등)와 `feed` 는 쓸 수 없다. `?lang=` 은 쓰지 않는다.

## front matter

```
---
title: (그 언어 제목)
date: 2026-10-23              # 원문과 같은 날짜
slug: ten-letters-one-skeleton   # 모든 언어판 동일, 파일명과 같게
lang: ja                      # 폴더 이름과 같아야 한다
description: (그 언어 한 문장)
category: behind-the-music    # 원문과 같게
translation_of: en            # ← 번역본만: 번역 원본 언어(ko 또는 en). 10개 AI 번역은 필수, en 은 보통 `translation_of: ko`
aliases: /journal/old-slug/   # ← 선택: 옛 주소(쉼표로 여러 개). 새 주소로 가는 정적 리다이렉트가 생기고 sitemap 에서는 빠진다
---
```

- `translation_of` 가 있으면 「AI 번역」 표시(ko·en 제외 10개 언어)·원문 링크·`translationOfWork`(번역→원문)·`workTranslation`(원문→번역들)이 자동. 원문 파일은 고칠 필요가 없다.
- 선택 칸 `updated`·`image`·`image_alt`·`keywords`·`album`·`songs`·`citations` 은 `content/journal/ko/sample-template.md`(draft) 참고. 본문 이미지 `![](/assets/journal/<slug>/x.jpg)` 는 원문 것을 그대로 쓰고 alt·캡션만 번역.
- 예전 `translation:` 칸은 없어졌다(쓰면 오류) — slug 가 같으면 한 묶음이다. 한 묶음에 같은 언어 글은 1개(파일 경로가 곧 유일).
- 마크다운은 기존 부분집합(제목·문단·목록·인용·코드·이미지·링크). 번역하지 말 것: 곡/앨범 제목, `idle()`, `ipe()`, 코드, URL. 새 UI 문구(목록 제목·버튼)는 `scripts/build_journal.py` 의 `_T` 표.
- 옛 주소가 있던 글(`/journal/ten-letters-one-skeleton-ko/`, `-en/`, `/<lang>/journal/...-en/`)은 `aliases` 로 리다이렉트를 남겨 두었다. 목록 `/<lang>/journal/` → `/journal/<lang>/` 리다이렉트는 자동.

## 게시 절차

1. 원고(ko/en + 번역) 작성 → `python3 scripts/build_journal.py` (빌드가 형식 오류를 잡는다).
2. **`python3 scripts/check_sitemap.py` 통과 필수** — sitemap.xml 유효 · 공개 저널 URL(허브·언어별 목록·글) 누락 0 · 옛 주소 미등재 · hreflang 상호참조+x-default. 실패하면 exit 1(게시 금지).
3. `python3 -m unittest discover -s tests` 통과 → 커밋·push → 배포 후 `python3 scripts/check_sitemap.py --live`(모든 URL HTTP 200).

빌드가 대신 잡아 주는 것: 필수 칸 누락 · 폴더/`lang`/파일명 불일치 · `content/journal/` 바로 아래 평면 파일 · `translation_of` 가 가리키는 같은 slug 원문 없음/draft · AI 번역에 `translation_of` 없음 · 예약 slug · alias 중복/실제 페이지와 충돌 · 이미지 파일 없음. `draft: true` 는 sitemap·llms·목록·hreflang·언어 폴더 어디에도 나오지 않는다(테스트로 보장).
`content/`·`scripts/`·`tests/` 는 배포 산출물에서 제외된다(원고 .md 가 공개 URL 이 되지 않음).

## 새 글마다 10개 언어 번역 만드는 절차

1. ko/en 원문을 확정(`content/journal/ko/<slug>.md`, `content/journal/en/<slug>.md` — en 은 `translation_of: ko`).
2. **EN 원문 기준**으로 10개 언어(`ja zh es fr de pt ru ar hi id`)를 번역 — 고유명사·곡명·앨범명·`idle()`·`ipe()`·코드·URL 은 원문 표기 그대로, 의미·사실을 덧붙이지 않는다. 직원 이름은 원문에 있을 때만.
3. 각 번역을 `content/journal/<lang>/<slug>.md` 로 저장: 원문과 같은 `date`·`slug`·`category`·`album`, `lang`, `translation_of: en`, 번역한 `title`·`description`·`keywords`. 본문은 문단·제목 수·순서를 원문과 똑같이(그림 줄은 그대로, alt·캡션만 번역). 「다른 언어로 읽기」 같은 링크 줄은 번역하지 않는다(AI 번역 표시가 원문 링크를 자동으로 붙인다).
4. 빌드 → `check_sitemap.py` → 테스트 통과 후 커밋.
5. AI 에이전트에게 맡길 때는 위 2~3 을 브리프에 붙인다(언어별 에이전트 병렬 가능, 한 에이전트 = 한 언어 = 파일 하나).
