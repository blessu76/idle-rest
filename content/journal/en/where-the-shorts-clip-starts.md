---
title: Where a Shorts Clip Starts in the Song
date: 2026-11-12
time: "15:16"
slug: where-the-shorts-clip-starts
lang: en
translation_of: ko
description: Of 21 Shorts clips for dear(you); vol.1, 18 start exactly at 30% of the song length, rounded down. Three exceptions are listed too.
category: behind-the-music
draft: false
keywords: dear(you);, Shorts, clip, 30%, S1A1, subtitles, song length, idle(), ipe(), AI music, Suno, lo-fi
album: dear(you); vol.1 @ https://idle.ipe.rest/#album
songs: You're Not Alone. @ https://youtu.be/-ubb0jO9j6A
---

[한국어로 읽기 →](/journal/ko/where-the-shorts-clip-starts/)

[82 Draft Lines, 15 Cues: What a Clip Keeps](/journal/en/how-much-of-the-draft-reaches-the-screen/) covered the fact that a Shorts clip is 58 seconds. The new question here is a single one: where in the song do those 58 seconds start? For most clips, at about 30% of the song's length.

The scope and method first. In a file name, `clipA-B` means seconds A to B of the song, and for every clip in the table B minus A is 58. The start ratio is the start second in the file name divided by the song length. Song lengths are the master values measured with ffprobe (durs.txt). Subtitle cues were counted by splitting each clip's SRT file on blank lines. Clips from other series, such as `N-001` and `U-001`, are left out. The music is made with AI (Suno); the lyrics are drafted by AI and reviewed by a person.

## Twenty-one clips

| Song | Lang | Clip | Song length (s) | Start ratio | Equals floor of 30% | Subtitle cues |
|---|---|---|---|---|---|---|
| 01 | EN | clip90-148 | 192.68 | 46.7% | No (57) | 13 |
| 02 | EN | clip41-99 | 137.20 | 29.9% | Yes | 15 |
| 02 | KO | clip60-118 | 201.84 | 29.7% | Yes | 8 |
| 02 | KO | clip61-119 | 201.84 | 30.2% | No (60) | 8 |
| 03 | EN | clip70-128 | 234.56 | 29.8% | Yes | 15 |
| 03 | KO | clip70-128 | 253.24 | 27.6% | No (75) | 10 |
| 03 | KO | clip75-133 | 253.24 | 29.6% | Yes | 12 |
| 04 | EN | clip68-126 | 228.32 | 29.8% | Yes | 18 |
| 04 | KO | clip71-129 | 236.84 | 30.0% | Yes | 9 |
| 05 | EN | clip68-126 | 228.80 | 29.7% | Yes | 6 |
| 05 | KO | clip68-126 | 228.00 | 29.8% | Yes | 8 |
| 06 | EN | clip62-120 | 206.88 | 30.0% | Yes | 8 |
| 06 | KO | clip73-131 | 244.96 | 29.8% | Yes | 11 |
| 07 | EN | clip57-115 | 193.32 | 29.5% | Yes | 17 |
| 07 | KO | clip71-129 | 239.68 | 29.6% | Yes | 13 |
| 08 | EN | clip61-119 | 203.52 | 30.0% | Yes | 11 |
| 08 | KO | clip69-127 | 233.20 | 29.6% | Yes | 7 |
| 09 | EN | clip60-118 | 202.16 | 29.7% | Yes | 13 |
| 09 | KO | clip71-129 | 238.40 | 29.8% | Yes | 7 |
| 10 | EN | clip60-118 | 201.32 | 29.8% | Yes | 12 |
| 10 | KO | clip83-141 | 278.00 | 29.9% | Yes | 8 |

"Equals floor of 30%" checks whether the start second in the file name equals floor(0.30 × song length). Of the 21 clips, 18 match and 3 do not.

## The three exceptions

- The English clip for song 01 starts at 90 seconds, which is 46.7% of the song. Floor of 30% would give 57. It is by far the largest exception in the table.
- Song 02 in Korean has two clips (60 and 61 seconds). The 60-second one matches, and the 61-second one, at 30.2%, does not (floor of 30% is 60).
- Song 03 in Korean also has two clips (70 and 75 seconds). The 75-second one matches, and the 70-second one is at 27.6% (floor of 30% is 75).

Judged by ratio alone, two of the exceptions (song 02 Korean at 61 seconds, song 03 Korean at 70 seconds) are not far from 30%, and only song 01 English is far away. Leave out song 01 and the other twenty clips start between 27.6% and 30.2%.

## What we are not claiming

- Whether the clips were chosen with this rule on purpose, or by some other standard, we could not confirm in the documents. The match is something we observed, not an explanation.
- The lengths are those of the English and Korean masters, not of the clip videos.
- That this position is a good one, or anything about how a listener will feel. No medical or other effect is claimed.

## Listen

- 06 You're Not Alone. (혼자가 아니야.) — [English version](https://youtu.be/-ubb0jO9j6A) · [Korean version](https://youtu.be/nvsak4qaAW0)
- 10 You Did So Well Today. (오늘도... 정말 고생했어.) — [English version](https://youtu.be/lvyLfiBzMLg) · [Korean version](https://youtu.be/I_3pxFG_1Ug)

Once more, plainly: the music is made with AI (Suno); the lyrics are drafted by AI and reviewed by a person. You can also listen on the [idle() home page](/).

## Related

- The 58-second window: [82 Draft Lines, 15 Cues: What a Clip Keeps](/journal/en/how-much-of-the-draft-reaches-the-screen/)
- The two versions: [English by a Woman, Korean by a Man](/journal/en/english-female-korean-male/)
