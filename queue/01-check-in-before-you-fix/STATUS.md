# 01 · check-in-before-you-fix — 해결책 대신 안부부터 (계획서 #2)

- 상태: **원고 완료** (KO/EN, 날짜 칸 TBD) · 2026-10-22 00:2x KST
- 분량: KO 5,073자(공백 포함) / 3,846자(공백 제외) · EN 1,651단어 (본문만, 이미지 제외)
- 이미지 3장(KO·EN 공통 파일, alt 는 각 md 에 언어별): `images/cover-s1a1-01.jpg`(studio/brand/covers 커버 → jpg 1000px, 68KB) · `emotion-arc.jpg`(직접 제작 1600px, 130KB) · `blueprint-s1a1-01.jpg`(직접 제작, 124KB)
- 게시 전: `images/*` 를 레포 `assets/journal/check-in-before-you-fix/` 로 복사하고 date 를 채운 뒤 `scripts/build_journal.py`.
- 대조한 파일: studio/lyrics/songs/S1A1.01_today-you-worked-so-hard.md (Theme·Story·Verse·Outro·Suno Style·메모) · albums/dear-you_album.md (§2 컨셉, §3 아크, §4 사운드) · S1A1.02 Theme(2번 설명) · 줄 수는 스크립트 집계(01=59/59, 03=82/82, 09=70/70 → "전체 줄 수 같은 곡 1·3·9번").
- 가사 인용(글자 일치 확인): KO "오늘은 내가 먼저 네 안부를 물어볼게." · "쉬고 싶은 마음보다 미안한 마음이 조금 더 컸던 하루." · EN "Today, let me be the first to ask how you've been." · "More than the wish to rest, it was the sorry feeling that weighed a little heavier today." (+ 짧은 파편: "괜찮아. 오늘은 조금 늦어도 괜찮아." "그걸로 충분해. 정말.")
- 지어내지 않은 것: 가사를 고친 과정(일지 미기입), Final Chorus 가 3번부터 생긴 이유("기록에 남아 있지 않다"로 명시).
- 걸리는 점: 커버는 studio/brand/covers 원본이며 발매본과 동일한지 [미검증]. 앨범 사운드 아크(9번 새소리 등)는 기획서 기준이며 음원 청취로 [미검증].
- 로컬 렌더(file://, 320/375/768/1280): 가로 넘침 없음, 이미지 깨짐 0.
- 2026-10-22 Davy 요청 반영: 「들어 보기」 섹션에 유튜브 링크 추가(사이트 llms.txt 값, oEmbed 로 영상 제목 일치 확인). 최종 분량은 아래 표 참조 — 갱신본: KO(공백 제외)·EN 단어 수는 방 노트 기재.

---

## 카피 검수 (Iris · 2026-10-22 01:05 KST)

- 대조: 가사 원고 S1A1.01(Theme·Mood·Story·두 버전·Suno Style·속삭임) · 앨범 기획서(아크·사운드 아크·수미상관) · S1A1.02 Theme · 사이트 llms.txt(유튜브 링크). 글 속 인용 4건·섹션별 줄 수(11/12/8/12/9/7=59)·1·3·9번 전체 줄 수 일치(스크립트 재집계)·제목·BPM·악기·속삭임 목록·유튜브 링크 모두 일치.
- 고친 것: ① KO 「분위기 칸」 문장 중복 제거 ② 상투적 도입 「흥미로운 점은」·「해상도가 올라갑니다」 삭제/교체 ③ 일반화 주장 「대개 체력이 아니라 미안함」 → 「일 수 있다」(근거 없는 단정 완화) ④ Pre-Chorus 가사 인용에 「」 표시 ⑤ 「아무것도 요구하지 않는」 → 「거의」(후렴이 숨 쉬기를 청하므로 본문 모순 제거, KO·EN) ⑥ EN 어색한 표현 정리(「sits on top of that skeleton first」·「the resolution of the scene」·「a particle」·「refuses to do」·cafe→café) ⑦ frontmatter 를 첫 글 형식에 맞춤(translation·translation_of·keywords·album·songs 추가, date: TBD 유지) ⑧ EN AI 공개 문장을 정확한 문장 그대로 쓰도록 문장 분리.
- 확인: 금지어 grep 0건(Matt·Paul·Jin·Davy·이메일·내부 경로·결정 번호·시편·S1A2~4·사람이 고친 과정). AI 공개 문장 KO·EN 모두 있음. 분량 KO 3,846자(공백 제외) · EN 1,681단어. 이미지 alt 3개 KO·EN 모두 있음. dear-you 커버 사용 없음.
- 남은 것 / 제안(뜻이 바뀌는 큰 수정이라 하지 않음):
  - [미검증] 커버가 발매본과 동일한지, 앨범 사운드 아크(9번 새소리 등)는 기획서 기준(음원 청취 안 함).
  - ✅ emotion-arc.jpg 하단 문구 「closes with thanks」→「closes with comfort」로 수정(1600×720, 약 88KB). (10-22 01:xx)
  - 본문의 「곡 설계 문서」·「앨범 기획서」 표현은 내부 문서 이름이 아니라 일반 명사지만, 게시 전 한 번 더 읽어 거슬리면 「가사 원고」로 통일.

카피 검수 통과 — Iris · 2026-10-22 01:05 KST
