# 03 · six-series-of-idle — idle()의 여섯 시리즈 (계획서 #4)

- 상태: **원고 완료** (KO/EN, 날짜 TBD) · 2026-10-22 00:5x KST
- 이미지 3장(전부 직접 제작 1600px): `six-series.jpg`(166KB) · `song-codes.jpg`(~123KB) · `singles-to-album.jpg`(114KB)
- 게시 전: images/* → 레포 assets/journal/six-series-of-idle/ , date 채우기, build.
- 근거: 사이트 llms.txt(Track series·Releases·Album Universe — 공개 문구만) · studio/lyrics/INDEX.md 「넘버링 규칙」(접두 N/U 의미, 이관·재사용 금지) · albums/dear-you_album.md §7(릴리스 전략)
- 곡 언급: still compiling(N-001)·good morning, world(U-001)는 llms.txt 의 공개 한 줄 설명만 인용(가사 인용 없음). 발매곡 없는 4개 시리즈(be still; · rest() { chill(); } · grace_in_the_loop · night_mode // not_alone)는 이름·장르·공개 주제만. 시리즈 숨은 메시지(INDEX 내부 열)와 성경 구절은 쓰지 않음.
- 해석 표시: 이름을 코드로 읽는 부분은 "읽는 법"이며 지은 의도가 아니라고 본문에 명시. 이름 유래 기록 없음.
- S1A2~4 앨범 제목·트랙은 쓰지 않고 시즌1의 시간대 구조(밤·새벽·오전·저녁, llms.txt 공개분)만.
- 사진 주의: 레포 assets/covers 의 dear-you*.jpg 는 스톡 사진 기반(라떼) — 이 글에는 쓰지 않음. 2편(커버)·4편(커버)에 쓴 titled 버전은 사이트 홈이 이미 쓰는 것과 동일.
- 렌더(file://, 320/375/768/1280): 가로 넘침 0, 이미지 깨짐 0.
- 2026-10-22 Davy 요청 반영: 「들어 보기」 섹션에 유튜브 링크 추가(사이트 llms.txt 값, oEmbed 로 영상 제목 일치 확인). 최종 분량은 아래 표 참조 — 갱신본: KO(공백 제외)·EN 단어 수는 방 노트 기재.

---

## 카피 검수 (Iris · 2026-10-22 01:10 KST)

- 대조: 사이트 llms.txt(시리즈 6개·싱글·앨범·유튜브 링크 전부 일치 확인) · studio/lyrics/INDEX.md 「넘버링 규칙」(접두 N=Night·U=Undefined, 재사용 금지, 편입 시 이관) · albums/dear-you_album.md §7(싱글 드립 → 앨범 컴파일) · 곡 제목(KO/EN)·곡 번호 S1A1.01~10·유튜브 6개 링크 일치. 금지어 grep 0건(Matt·Paul·Jin·Davy·이메일·내부 경로·결정 번호·시편·S1A2~4 코드·사람이 고친 과정). 상투구(여정·깊이 있는·fast-paced) 0건.
- 분량: KO 3,589자(공백 제외) · EN 1,424단어. AI 공개 문장 KO·EN 모두 있음. 이미지 alt 3개 KO·EN 모두 있음.
- 고친 것(사실 오류 3건 + 문장):
  ① **근거 없는 주장 삭제** — 「앨범의 이름은 시리즈 이름에 번호를 붙여 정한다」「한 시리즈가 충분히 쌓이면 앨범으로 묶는다」: 정본에 없고(앨범은 시리즈와 별개 이름: Dear You·Breathe. Code. Rest. 등) 본문의 「dear(you);는 여섯 시리즈 밖」과도 모순 → 「싱글을 하나씩 내고 곡이 충분히 쌓이면 앨범으로 묶는다(싱글 드립 → 앨범 컴파일)」로 교체(KO·EN, 캡션·alt 포함).
  ② 「이 시리즈의 첫 싱글」(still compiling·good morning, world) — 사이트 문구에는 「시리즈의 첫 싱글」 표현이 없어 「이 시리즈에서 나온 싱글」로(KO·EN). 「시리즈의 문을 연 셈」도 삭제.
  ③ 「같은 시리즈 이름 아래에서도 앨범 번호가 바뀌면…」(시리즈·앨범 혼동) → 「앨범 번호가 바뀌면 하루의 다른 시간대로 넘어갑니다」.
  ④ 소제목 「곡을 묶는 결이다」→「이름표다」(본문 어휘와 맞춤) · EN 「calls up a loop」→「brings a loop to mind」.
  ⑤ frontmatter 를 첫 글 형식에 맞춤(translation·translation_of·keywords·album 추가, date: TBD 유지).
- ⚠️ **이미지 교체 필요(내가 못 함)** — `images/singles-to-album.jpg` 안의 글자가 위 ①과 같은 근거 없는 문구(「album = {series} vol.N」「시리즈 이름 + vol.번호가 앨범 이름이 된다」「once a series has enough songs」)다. 수정본을 만들어 두었으나 이 세션은 기존 이미지 덮어쓰기가 권한으로 거절됨. 수정본: `/private/tmp/claude-501/-Users-davy-kim-Desktop-Ipe-ipe-room/0238458b-aab7-48b5-8654-45a38345dcbb/scratchpad/singles-to-album-fixed.jpg` (1600×640, 패널 문구 「first album of Season 1 / 시즌 1의 첫 앨범」, 하단 「Singles come out one by one; once there are enough songs, they are gathered into an album.」) → 이 파일로 `images/singles-to-album.jpg` 를 교체하면 본문 alt·캡션과 일치한다.
- 남은 것 / 제안:
  - six-series.jpg 의 카드 문구 「야근 후 퇴근길」(내부 표기)과 본문 「늦은 밤 퇴근길」(사이트 문구)이 살짝 다름 — 의미 같아 그대로 둠. 접두 글자 B·R·G·M 은 사이트에 없는 내부 번호 체계 일부(미발매 시리즈 접두)지만 비밀 항목은 아님. 마음에 걸리면 이미지에서 접두 글자 빼기.
  - 시리즈 이름 「읽는 법」은 해석이며 지은 의도가 아님을 본문이 세 번 밝힘(서두·소제목 아래·마지막 문단). 중복이 거슬리면 소제목 아래 한 번만 남겨도 됨.
  - dear-you 커버 사용 없음(이 글).

카피 검수 보류 — 이미지 singles-to-album.jpg 교체 대기(원고는 수정 완료). 교체 후 통과 · Iris · 2026-10-22 01:10 KST
