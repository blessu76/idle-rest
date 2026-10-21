# 04 · i-was-scared-too — 두려움을 없애지 않고 인정하기 (계획서 #6)

- 상태: **원고 완료** (KO/EN, 날짜 TBD) · 2026-10-22 01:xx KST
- 이미지 3장: `cover-dear-you-titled.jpg`(레포 assets/covers 복사, 171KB — 사이트 홈 히어로가 쓰는 것과 동일) · `seven-slots.jpg` · `pre-chorus.jpg`(직접 제작 1600px, ~104KB)
- 게시 전: images/* → 레포 assets/journal/i-was-scared-too/ , date 채우기, build.
- 대조한 파일: studio/lyrics/songs/S1A1.03_i-was-scared-too.md 전체(Theme·Story·Verse·Pre-Chorus·Chorus·Bridge·Final Chorus·Outro·Suno Style·메모) · albums/dear-you_album.md(§2 정서 중심, §4 사운드, §6 브릿지 리프레인) · S1A1.04/07 의 브릿지 문장 존재 확인(grep). 줄 수는 스크립트 집계(EN 82줄=KO 82줄).
- 가사 인용(글자 일치 확인): KO "또 하나. 또 하나." · "그런 생각. 한 번쯤은 했잖아." · "불안하다는 건 포기했다는 뜻이 아니라 아직 소중하게 생각하고 있다는 뜻이니까." · "속도를 따라가기 위해 존재하는 사람이 아니라 누군가의 내일을 조금 더 따뜻하게 만들어 주는 사람이니까." / EN "One more. And one more." · "That kind of thought — you've had it once, haven't you?" · "Being anxious doesn't mean you've given up — it means you still hold it dear." · "Because you don't exist to keep up with the speed — you're someone who makes someone else's tomorrow a little warmer."
- 외부 링크: Stack Overflow 2025 Developer Survey AI 장 (https://survey.stackoverflow.co/2025/ai, 2026-10-22 HTTP 200·제목 확인). 수치 인용 없음.
- 지어내지 않은 것: 가사를 고친 과정(일지 없음). Final Chorus 가 3번부터 생긴 이유는 "기록에 없다"고 명시.
- 유튜브: S1A1.03 EN rXwAwZ2cu2g / KR tAzst5cWLKI (llms.txt 값, oEmbed 로 제목 일치 확인).
- 렌더(file://, 320/375/768/1280): 가로 넘침 0, 이미지 깨짐 0.

---

## 카피 검수 (Iris · 2026-10-22 01:12 KST)

- 대조: 가사 원고 S1A1.03(Theme·Mood·Story·Version A/B 전문·Suno Style·속삭임) · 앨범 기획서(§2 정서 중심, §3 아크, §4 사운드, §6 브릿지 리프레인) · S1A1.01·02·04·07 원고(Pre-Chorus 8줄·Final Chorus 유무·4/7번 Bridge 문장) · llms.txt(곡명·유튜브 링크). 인용 가사·섹션별 줄 수(14/15/7/13/13/11/9=82, KO도 82)·BPM 72·악기·속삭임 6개·제목(KO/EN)·유튜브 2개 모두 일치(스크립트 재집계).
- Stack Overflow 링크: https://survey.stackoverflow.co/2025/ai — 열어서 제목(「AI | 2025 Stack Overflow Developer Survey」)·사용 현황·신뢰/호감 항목 존재 확인. 본문에 수치 인용 0건, 링크는 출처로만 둠(그대로 통과).
- 금지어 grep 0건(Matt·Paul·Jin·Davy·이메일·내부 경로·결정 번호·시편·S1A2~4 코드·사람이 고친 과정). 상투구 0건. AI 공개 문장 KO·EN 모두 있음(서두 + 맺음). 분량 KO 4,100자(공백 제외) · EN 1,760단어. 이미지 alt 3개 KO·EN 모두 있음.
- 고친 것:
  ① 「AI라는 단어를 처음으로 정면에서 부른다」(Bridge) — 1절 첫 줄에 이미 「새로운 AI」가 나와 사실과 다름 → 「두려움의 이름이던 AI를 정면으로 마주한다」(KO·EN).
  ② 「후렴은 곡의 제목을 말하면서 시작」 — 실제 후렴은 속삭임(걱정 마… / Don't worry...)이 먼저 → 「속삭임 한마디 뒤에 제목을 말하며 시작」(KO·EN).
  ③ 「이 모순을 오히려 이 곡의 출발점으로 삼았다」 — 기록에 없는 제작 의도 → 「이 아이러니를 숨기지 않습니다」(KO·EN).
  ④ 설계 문서를 그대로 옮긴 문장 두 곳에 「」 인용 표시(KO).
  ⑤ frontmatter 를 첫 글 형식에 맞춤(translation·translation_of·keywords·album 추가, date: TBD 유지).
- ⚠️ **dear-you 커버 사용 — 라이선스 확인 전이면 게시 때 뺀다.** `images/cover-dear-you-titled.jpg`(레포 assets/covers/dear-you-titled.jpg 와 동일, 스톡 사진 기반·라이선스 미확인). 지우지 않고 둠. 뺄 때는 두 md 의 맨 위 이미지 + 캡션(KO「*dear(you); vol.1의 커버…*」·EN「*The cover of dear(you); vol.1…*」) 4줄을 같이 삭제하면 된다(다른 본문은 커버를 참조하지 않음).
- 남은 것 / 제안:
  - 「곡 설계 문서」「앨범 기획서」 표현은 일반 명사로 쓰였고 내부 경로·파일명 노출은 없음. 게시 전 거슬리면 「가사 원고」로 통일.
  - 앨범 사운드 아크(3·4번 잔잔한 스트링)는 기획서 기준 — 음원 청취로 [미검증].

카피 검수 통과 — Iris · 2026-10-22 01:12 KST
