---
title: One Entry, Twelve Languages
date: 2026-11-04
time: "21:11"
slug: one-entry-twelve-languages
lang: en
translation_of: ko
description: How an idle() journal entry becomes twelve pages: two languages written by hand, ten AI translations, and a few things we deliberately leave untranslated.
category: behind-the-music
draft: false
keywords: multilingual, translation, journal, hreflang, 12 languages, idle(), ipe(), AI music, Suno
---

[한국어로 읽기 →](/journal/ko/one-entry-twelve-languages/)

The idle() site is available in twelve languages. This entry explains how one journal entry becomes up to twelve pages, and where we stop translating on purpose. It describes how the site is built and published; we measured nothing about readers or listeners for it. The music is made with AI (Suno); the lyrics are drafted by AI and reviewed by a person.

## Two written, ten translated

Every entry starts in two languages that we write and review ourselves: Korean and English. The other ten (Japanese, Simplified Chinese, Spanish, French, German, Portuguese, Russian, Arabic, Hindi and Indonesian) are AI translations of those originals.

You can tell the two kinds apart on the page:

- An AI translation carries an "AI" badge and a short notice, with a link back to the original it was translated from.
- The Korean and English pages carry no such badge, because they are the originals.
- The link goes to the Korean or English original the translation was made from.

## What stays as it is

Some words are not translated in any language:

- Song and album titles, such as *dear(you); vol.1* and the ten track titles.
- The names idle() and ipe().
- Code and URLs.

The reason is practical. A title is the name of a thing, and a reader who finds a song by its English title should be able to find the same string on every page. Translating the ten titles would also change what this journal says about them; the entries [Ten Titles, Read as Sentences](/journal/en/ten-titles-as-sentences/) and [Who Speaks in the Ten Titles?](/journal/en/who-speaks-in-ten-titles/) both read the English wording itself.

## One address per language

Each language has its own address, so a search engine and a reader can both land on the right one:

- The Korean and English originals live at `/journal/ko/…` and `/journal/en/…`.
- Every language has its own list at `/journal/<language code>/`.
- Every language version of an entry shares the same short name (the slug), so `ja`, `de` and the rest differ only in the language code.
- Each page points to the other language versions of the same entry, and to one default version, so the versions are read as one entry, not as twelve copies.

Language switching on a page that has no language in its address follows a simple order: an explicit `?lang=` first, then the language you chose last time on this device, then your browser's language list, and English if none of those match.

## What a missing translation looks like

An entry does not always exist in all twelve languages. The two most recent entries before this one, [The Tempo Ladder of Ten Songs](/journal/en/tempo-ladder-of-ten-songs/) and [Who Speaks in the Ten Titles?](/journal/en/who-speaks-in-ten-titles/), are published in Korean and English only so far.

When a translation does not exist, the site does not create an empty page or show another language in its place. That language's list simply does not include the entry, and the entry's own pages do not point to it. So a missing translation is quiet on the site, and we say it here instead.

## What we do not claim

- We do not claim the ten translations read as naturally as the originals. They are produced by AI and are marked as such.
- We do not claim twelve languages means twelve audiences; we have not measured which languages are read.
- We do not promise that every entry will be translated, or when.

If you read one of the translations and find a line that is wrong, tell us through the [contact page](/contact/); a factual correction is made in all the language versions together.

## Read together

- How a song is made in the first place: [How an AI Lo-Fi Song Gets Made](/journal/en/how-a-song-gets-made/)
- The album's two language versions: [Whispers in the Other Language — How dear(you); vol.1 Pairs Its Two Versions](/journal/en/whispers-in-the-other-language/)
- How the English lines were paraphrased rather than translated word for word: [English by a Woman, Korean by a Man — The Rule That Splits the Two Versions, and How the English Was Paraphrased](/journal/en/english-female-korean-male/)
