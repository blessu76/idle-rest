---
title: still compiling — One Night, Two Languages
date: 2026-10-30
time: "10:22"
slug: still-compiling-one-night-two-languages
lang: en
description: We lay the lyric draft of "still compiling", the first song of late_night.lofi, beside the entered lyrics of its two versions and follow its three // comments.
category: behind-the-music
draft: false
translation_of: ko
keywords: still compiling, N-001, late_night.lofi, lo-fi, lyric draft, code comments, be still, idle(), ipe(), AI music, Suno
---

[한국어로 읽기 →](/journal/ko/still-compiling-one-night-two-languages/)

"still compiling" is the first song of the `late_night.lofi` series, song number N-001. It is a song for someone still at the monitor at two in the morning, waiting for a build to finish. This song also has its lyrics in two layers. One is the Korean lyric in the draft file. The other is the lyrics actually entered into the music tool, in an English version and a Korean version. This post reads the two side by side. The thing to watch is what became of the three `//` comment lines of the draft once the lyrics were entered.

First, the scope. What we read: the lyric draft, the creation log, the production package document, and the description file of the folder that holds the production screen captures. We do not describe how anything sounds from listening, and the style settings in the package are inputs, not what the recording sounds like. And, as always: the music is produced with AI (Suno). Lyrics are AI-drafted and reviewed by a person.

## Where the song sits, and its two versions

The header of the draft file lists the song as lo-fi, with the theme "a developer's sorrow", and as the second release. How to read the series name is in [The Six Series of idle()](/journal/en/six-series-of-idle/). The dates in the log are these: the lyric draft was finished on 2026-06-29, the music was generated on 2026-06-30 (from the record in the screen-capture folder), and the release date is 2026-07-06.

There are two versions. The production package separates version A, English-led with Korean mixed in here and there, from version B, Korean-led with English mixed in, and says the one that goes on the home page is A. The log lists both the English and the Korean version as male vocal.

## Twenty lines and twenty-one

The lyric in the draft file has six sections and twenty lines: four in Verse 1, two in the Pre-Chorus, four in the Chorus, four in Verse 2, three in the Bridge, and three in the Outro. The entered lyrics add one Intro line, so they run to twenty-one. The English Intro is "two a.m. — still compiling" and the Korean one is "새벽 두 시, still compiling". In both versions it is a line the draft did not have, and a bracketed direction asks for it to start softly. The other twenty lines keep the draft's section order and line count.

The Korean version is nearly untouched. The only differences are that "롤백" in Verse 2 is written as rollback, and the treatment of `//`, which we come to below. The English version is a paraphrase. The draft's "빨간 줄 하나에 무너진 하루" becomes "one red line, and the day falls apart", and "한 줄 고치면 두 줄이 우는데" becomes "fix one line and two more cry". The sense carries over line by line, but some words were added in the move to English: "tonight" in the Pre-Chorus, "but I go on" at the end of Verse 2, and "we wrote for you" at the end of the Chorus. The log does not say why they were added.

## A night written in build terms

The scene of this song is made only of build vocabulary: two a.m., a blinking cursor, one red line, two more lines that cry when you fix one, a spec that changed. The chorus opens on "still compiling, 아직 끝나지 않아" and runs on to "무한 루프 같은 이 밤을 도는 중". In Verse 2 a fingertip is on the deploy button, a green light turns red, and after a rollback and an apology the dawn comes again. The word burnout is too frightening to say. The lyric reads like the build log of one night, and that log does not end in success. Only in the Bridge does the voice change: "다 못 끝내도 세상은 안 멈춰 / 충분히 수고했어, 오늘도".

## The three `//` comments

The draft has three lines that start with `//`:

- Chorus: `// 그래도 괜찮아`
- Bridge: `// TODO: 좀 쉬어도 돼`
- Outro: `ipe(); // be still`

In the entered lyrics all three lose their `//`. But not all the words are lost. The Chorus line becomes "but it's okay — 그래도 괜찮아" in the English version and "그래도 괜찮아" in the Korean one. The Bridge line drops its `TODO:` and becomes "it's alright to rest" in English and "좀 쉬어도 돼" in Korean. The Outro line loses `ipe();` and the `//` and keeps only "be still". The log's memo says the song handles its Christian message not by naming it directly but gently, through the `//` comment lines alone. What it means that the comment marker left the sung lyric is not written down in the log.

The marker comes back in the package's subtitle and display block. Its header is `// 02 still compiling`, and inside it are three Chorus lines, two Bridge lines and three Outro lines, in Korean. There `// 그래도 괜찮아`, `// TODO: 좀 쉬어도 돼` and `ipe(); // be still` come back with their `//`. The last line, `rest was written into the code`, which the draft wrote without a comment mark, appears in the subtitle with `//` in front. A comment that disappears from the sung lyric and shows only in the text on screen: that is how this song reads as using `//`. The same thing happened in [the comparison of the first single's draft](/journal/en/from-draft-c-to-good-morning-world/).

## What changes in the English

The most visible change in the English version is the Bridge. The draft opens it with "// TODO: 좀 쉬어도 돼", while the English version has "it's alright to rest", then "even unfinished, the world won't stop". The last line is "you did enough today — 충분히 수고했어", which turns to Korean once at the end of an English sentence. The Chorus's "아직 끝나지 않아" and "그래도 괜찮아" also stay in Korean. In the English-led version Korean sits in three places: the first and third lines of the Chorus, and the last line of the Bridge.

## The Outro's first line, be still

The first line of the Outro was `ipe(); // be still` in the draft and is "be still" in the entered lyrics. The English version carries the direction (whispered) and the Korean version (속삭이듯). The section header in the draft is also "Outro — 속삭이듯". The log's memo says the song's signature `ipe. be still` is included in the Outro, and that this song is the reference track applied from N-001 onward. After it comes "process, you can rest now" ("process, 이제 좀 쉬어" in Korean), and the last line is, in English in both versions, "rest was written into the code". The last line is the same in both versions.

## What is not on record

In the log, the fields for the AI draft, the revision history and the music-generation details are empty. So that part was not kept on record. Specifically, what the first lyric looked like, which lines were changed by a person, why words were added in the English, and what was chosen on what basis among several generations are things this post cannot say. How the entered lyrics differ from the draft is only the result of reading the two files against each other, as above.

## Listen

- N-001 still compiling — [English version](https://youtu.be/O0PkHQYi2PE) · [Korean version](https://youtu.be/Pq0nMvQrwIo)

The general order in which a song gets made is in [How a Song Gets Made](/journal/en/how-a-song-gets-made/). Once more, plainly: the music is produced with AI (Suno). Lyrics are AI-drafted and reviewed by a person. You can also listen on the [idle() home page](/).
