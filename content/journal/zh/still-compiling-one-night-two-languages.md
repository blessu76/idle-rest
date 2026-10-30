---
title: still compiling — 一夜,两种语言
date: 2026-10-30
time: "10:22"
slug: still-compiling-one-night-two-languages
lang: zh
description: 我们把 late_night.lofi 的第一首歌《still compiling》的歌词草稿,与两个版本实际输入的歌词并排对照,追踪草稿中三行 // 注释的去向。
category: behind-the-music
draft: false
translation_of: en
keywords: still compiling, N-001, late_night.lofi, 低保真, 歌词草稿, 代码注释, be still, idle(), ipe(), AI音乐, Suno
---

“still compiling”是 `late_night.lofi` 系列的第一首歌,曲号 N-001。这首歌写给凌晨两点还守在显示器前、等待构建完成的人。这首歌的歌词同样有两层。一层是草稿文件里的韩语歌词。另一层是实际输入音乐工具的歌词,有英语版和韩语版。本文把这两层并排来读。要看的是:草稿里的三行 `//` 注释,在歌词输入之后变成了什么。

先说范围。我们读了:歌词草稿、制作日志、制作包文档,以及存放制作界面截图的文件夹里的说明文件。我们不凭聆听来描述声音,制作包里的风格设置是输入,不是录音听起来的样子。还有,照例要说明:音乐由 AI(Suno)制作。歌词由 AI 起草,再由人审阅。

## 这首歌的位置,与它的两个版本

草稿文件的开头把这首歌列为低保真,主题是“开发者的悲伤”,第二首发行。系列名称怎么读,见[idle() 的六个系列](/journal/zh/six-series-of-idle/)。日志里的日期如下:歌词草稿完成于 2026-06-29,音乐生成于 2026-06-30(依据截图文件夹里的记录),发行日是 2026-07-06。

共有两个版本。制作包把以英语为主、偶尔夹杂韩语的 A 版,与以韩语为主、夹杂英语的 B 版区分开,并说明放在首页上的是 A 版。日志把英语版和韩语版都记为男声。

## 二十行与二十一行

草稿文件里的歌词有六个段落、二十行:Verse 1 四行,Pre-Chorus 两行,Chorus 四行,Verse 2 四行,Bridge 三行,Outro 三行。输入的歌词多了一行 Intro,共二十一行。英语的 Intro 是“two a.m. — still compiling”,韩语的是“새벽 두 시, still compiling”。两个版本里,这都是草稿没有的一行,并带有一条方括号提示,要求轻柔地开始。其余二十行保持了草稿的段落顺序和行数。

韩语版几乎没有改动。差别只有:Verse 2 里的“롤백”写成了 rollback,以及下面要讲的 `//` 的处理。英语版是意译。草稿里的“빨간 줄 하나에 무너진 하루”变成 "one red line, and the day falls apart",“한 줄 고치면 두 줄이 우는데”变成 "fix one line and two more cry"。意思逐行延续,但转成英语时添了几个词:Pre-Chorus 里的 "tonight",Verse 2 末尾的 "but I go on",以及 Chorus 末尾的 "we wrote for you"。日志没有说明为什么添加。

## 用构建术语写成的一夜

这首歌的场景只由构建的词汇构成:凌晨两点、闪烁的光标、一行红线、改一行就哭出来的另外两行、改了的需求。副歌以“still compiling, 아직 끝나지 않아”开头,一路唱到“무한 루프 같은 이 밤을 도는 중”。Verse 2 里,指尖落在部署按钮上,绿灯变成红灯,回滚和道歉之后,黎明再次到来。倦怠(burnout)这个词太吓人,说不出口。这段歌词读起来像一夜的构建日志,而这份日志并没有以成功收尾。只有在 Bridge,声音变了:“다 못 끝내도 세상은 안 멈춰 / 충분히 수고했어, 오늘도”。

## 三行 `//` 注释

草稿里有三行以 `//` 开头:

- Chorus:`// 그래도 괜찮아`
- Bridge:`// TODO: 좀 쉬어도 돼`
- Outro:`ipe(); // be still`

在输入的歌词里,这三行都失去了 `//`。但并非所有的字都丢了。Chorus 那一行在英语版里变成“but it's okay — 그래도 괜찮아”,在韩语版里是“그래도 괜찮아”。Bridge 那一行去掉了 `TODO:`,英语版是“it's alright to rest”,韩语版是“좀 쉬어도 돼”。Outro 那一行丢掉了 `ipe();` 和 `//`,只留下“be still”。日志里的备注说,这首歌处理它的基督教信息时,没有直接点明,而是只通过 `//` 注释行,温和地带出。注释标记离开了演唱的歌词,这意味着什么,日志里没有写。

这个标记在制作包的字幕与显示块里又回来了。它的标题是 `// 02 still compiling`,里面有三行 Chorus、两行 Bridge 和三行 Outro,都是韩语。在那里,`// 그래도 괜찮아`、`// TODO: 좀 쉬어도 돼` 和 `ipe(); // be still` 带着 `//` 回来了。草稿里没有注释标记的最后一行 `rest was written into the code`,在字幕里也出现在 `//` 之后。一条在演唱歌词里消失、只出现在屏幕文字里的注释:这首歌对 `//` 的用法读起来就是这样。[第一支单曲草稿的对照](/journal/zh/from-draft-c-to-good-morning-world/)里也发生了同样的事。

## 英语里变了什么

英语版最明显的变化在 Bridge。草稿以“// TODO: 좀 쉬어도 돼”开头,而英语版是 "it's alright to rest",接着是 "even unfinished, the world won't stop"。最后一行是 "you did enough today — 충분히 수고했어",在一句英语的末尾转成一次韩语。Chorus 里的“아직 끝나지 않아”和“그래도 괜찮아”也保持韩语。在以英语为主的版本里,韩语出现在三处:Chorus 的第一行和第三行,以及 Bridge 的最后一行。

## Outro 的第一行,be still

Outro 的第一行在草稿里是 `ipe(); // be still`,在输入的歌词里是“be still”。英语版带有 (whispered) 提示,韩语版带有 (속삭이듯)。草稿里的段落标题也是“Outro — 속삭이듯”。日志里的备注说,这首歌的标志 `ipe. be still` 包含在 Outro 里,而这首歌是从 N-001 起沿用的参考曲目。随后是“process, you can rest now”(韩语版为“process, 이제 좀 쉬어”),最后一行在两个版本里都是英语的 "rest was written into the code"。最后一行在两个版本里相同。

## 没有记录的部分

日志里,AI 草稿、修改历史和音乐生成细节这几栏是空的。所以这部分没有留下记录。具体来说,最初的歌词是什么样、哪些行被人改过、英语里为什么添词、在多次生成中依据什么选了哪一个,这些本文都无从说起。输入的歌词与草稿有何不同,只是把两个文件对照来读的结果,如上所述。

## 试听

- N-001 still compiling — [英语版](https://youtu.be/O0PkHQYi2PE) · [韩语版](https://youtu.be/Pq0nMvQrwIo)

一首歌通常怎样被做出来,见[一首歌是怎么做出来的](/journal/zh/how-a-song-gets-made/)。再直白地说一遍:音乐由 AI(Suno)制作。歌词由 AI 起草,再由人审阅。你也可以在 [idle() 首页](/)试听。
