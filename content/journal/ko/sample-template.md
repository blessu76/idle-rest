---
title: 샘플 글 — 저널 템플릿 확인용
date: 2026-10-20
slug: sample-template
lang: ko
description: 빌드 결과(제목·날짜·본문·광고 칸)를 확인하기 위한 샘플입니다. draft 라서 사이트에는 나가지 않습니다.
category: notes
draft: true
# --- 선택 칸 (GEO: JSON-LD·hreflang·사이트맵·llms.txt). 없으면 그냥 빠진다. ---
# updated: 2026-10-23                      # 수정일 (dateModified·lastmod)
# image: /assets/journal/sample-template/cover.jpg   # 대표 이미지. 없으면 본문 첫 /assets/journal/ 이미지, 그것도 없으면 og-image
# image_alt: 대표 이미지 설명
# keywords: dear(you);, idle(), 로파이        # 쉼표로 구분
# translation_of: en                        # 번역본일 때만: 원문 언어(ko|en). 10개 AI 번역은 필수. 언어판은 slug 가 같으면 자동으로 한 묶음(hreflang)
# aliases: /journal/old-slug/                # 옛 주소(쉼표로 여러 개) — 새 주소로 가는 정적 리다이렉트가 생기고 사이트맵에서는 빠진다
# album: dear(you); vol.1 @ https://idle.ipe.rest/#album        # 제목 @ 주소 (주소 생략 가능)
# songs: Hard Day Again, Wasn't It? @ https://youtu.be/yGa2_hjw4ZI | It's Okay, Take Your Time.   # 항목은 | 로 구분, 곡마다 @ 스트리밍 주소
# citations: 기사 제목 @ https://example.com/article | 다른 글 @ https://example.com/b   # 본문의 외부 링크(유튜브·SNS 제외)는 자동으로 citation 에 들어간다
---

이 글은 **저널 템플릿**을 확인하기 위한 샘플입니다. `draft: true` 이므로 실제 빌드에서는 페이지·목록·사이트맵·RSS 어디에도 나오지 않습니다.

## 소제목

문단 사이 간격과 글자 크기를 봅니다. [idle() 홈](/)으로 가는 링크와 *기울임*도 넣어 둡니다.

- 목록 하나
- 목록 둘
- 목록 셋

> 인용문은 이렇게 보입니다.

```
ipe(); // be still
```

이미지는 `/assets/journal/<slug>/파일.jpg` 에 두고, 한 줄에 이미지만 쓰면 `<figure>` 로 나옵니다. 따옴표 안은 캡션입니다. 가로·세로는 빌드가 파일에서 읽어 레이아웃 밀림을 막습니다.

(실제 글에서는 이미지 파일을 먼저 `assets/journal/<slug>/` 에 넣어야 합니다. 파일이 없으면 빌드와 `--check` 가 실패합니다. 그래서 이 샘플에는 이미지를 넣지 않았습니다.)
