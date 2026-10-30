---
title: still compiling — Eine Nacht, zwei Sprachen
date: 2026-10-30
time: "10:22"
slug: still-compiling-one-night-two-languages
lang: de
description: Der Textentwurf von „still compiling“, dem ersten Song von late_night.lofi, neben den eingegebenen Texten beider Fassungen — und seine drei //-Kommentare.
category: behind-the-music
draft: false
translation_of: en
keywords: still compiling, N-001, late_night.lofi, Lo-fi, Textentwurf, Code-Kommentare, be still, idle(), ipe(), KI-Musik, Suno
---

„still compiling“ ist der erste Song der Serie `late_night.lofi`, Songnummer N-001. Es ist ein Lied für jemanden, der um zwei Uhr nachts noch am Monitor sitzt und darauf wartet, dass ein Build durchläuft. Auch dieser Song hat seinen Text in zwei Schichten. Die eine ist der koreanische Text in der Entwurfsdatei. Die andere sind die Texte, die tatsächlich ins Musikwerkzeug eingegeben wurden, als englische und als koreanische Fassung. Dieser Beitrag liest beide nebeneinander. Worauf es ankommt: was aus den drei `//`-Kommentarzeilen des Entwurfs wurde, nachdem der Text eingegeben war.

Zuerst der Umfang. Gelesen haben wir: den Textentwurf, das Entstehungsprotokoll, das Produktionspaket-Dokument und die Beschreibungsdatei des Ordners mit den Screenshots der Produktion. Wir beschreiben nicht, wie etwas klingt, nach Höreindruck, und die Stileinstellungen im Paket sind Eingaben, nicht der Klang der Aufnahme. Und wie immer: Die Musik wird mit KI (Suno) produziert. Die Texte werden von der KI entworfen und von einem Menschen geprüft.

## Wo der Song steht, und seine zwei Fassungen

Der Kopf der Entwurfsdatei führt den Song als Lo-fi, mit dem Thema „der Kummer eines Entwicklers“, und als zweite Veröffentlichung. Wie der Serienname zu lesen ist, steht in [Die sechs Serien von idle()](/journal/de/six-series-of-idle/). Die Daten im Protokoll sind diese: Der Textentwurf wurde am 2026-06-29 fertig, die Musik wurde am 2026-06-30 generiert (laut Eintrag im Screenshot-Ordner), und der Veröffentlichungstermin ist der 2026-07-06.

Es gibt zwei Fassungen. Das Produktionspaket trennt Version A, englisch geführt mit koreanischen Einsprengseln, von Version B, koreanisch geführt mit englischen Einsprengseln, und sagt, dass die auf der Startseite A ist. Das Protokoll führt sowohl die englische als auch die koreanische Fassung mit männlichem Gesang.

## Zwanzig Zeilen und einundzwanzig

Der Text in der Entwurfsdatei hat sechs Abschnitte und zwanzig Zeilen: vier in Verse 1, zwei im Pre-Chorus, vier im Chorus, vier in Verse 2, drei in der Bridge und drei im Outro. Die eingegebenen Texte fügen eine Intro-Zeile hinzu, sie kommen also auf einundzwanzig. Das englische Intro lautet „two a.m. — still compiling“, das koreanische „새벽 두 시, still compiling“. In beiden Fassungen ist es eine Zeile, die der Entwurf nicht hatte, und eine Regieanweisung in Klammern bittet darum, dass sie leise beginnt. Die übrigen zwanzig Zeilen behalten Abschnittsfolge und Zeilenzahl des Entwurfs.

Die koreanische Fassung ist fast unangetastet. Die einzigen Unterschiede sind, dass „롤백“ in Verse 2 als rollback geschrieben wird, und der Umgang mit `//`, zu dem wir weiter unten kommen. Die englische Fassung ist eine Paraphrase. Aus dem „빨간 줄 하나에 무너진 하루“ des Entwurfs wird „one red line, and the day falls apart“, aus „한 줄 고치면 두 줄이 우는데“ wird „fix one line and two more cry“. Der Sinn bleibt Zeile für Zeile erhalten, doch beim Wechsel ins Englische kamen einige Wörter hinzu: „tonight“ im Pre-Chorus, „but I go on“ am Ende von Verse 2 und „we wrote for you“ am Ende des Chorus. Das Protokoll sagt nicht, warum sie hinzugefügt wurden.

## Eine Nacht in der Sprache des Builds

Die Szene dieses Songs besteht nur aus Build-Vokabular: zwei Uhr nachts, ein blinkender Cursor, eine rote Zeile, zwei weitere Zeilen, die weinen, wenn man eine repariert, eine Spezifikation, die sich geändert hat. Der Chorus beginnt mit „still compiling, 아직 끝나지 않아“ und läuft weiter bis „무한 루프 같은 이 밤을 도는 중“. In Verse 2 liegt eine Fingerspitze auf dem Deploy-Knopf, ein grünes Licht wird rot, und nach einem Rollback und einer Entschuldigung kommt die Dämmerung wieder. Das Wort Burnout ist zu beängstigend, um es auszusprechen. Der Text liest sich wie das Build-Log einer Nacht, und dieses Log endet nicht im Erfolg. Nur in der Bridge ändert sich die Stimme: „다 못 끝내도 세상은 안 멈춰 / 충분히 수고했어, 오늘도“.

## Die drei `//`-Kommentare

Der Entwurf hat drei Zeilen, die mit `//` beginnen:

- Chorus: `// 그래도 괜찮아`
- Bridge: `// TODO: 좀 쉬어도 돼`
- Outro: `ipe(); // be still`

In den eingegebenen Texten verlieren alle drei ihr `//`. Aber nicht alle Wörter gehen verloren. Die Chorus-Zeile wird in der englischen Fassung zu „but it's okay — 그래도 괜찮아“ und in der koreanischen zu „그래도 괜찮아“. Die Bridge-Zeile verliert ihr `TODO:` und wird englisch zu „it's alright to rest“ und koreanisch zu „좀 쉬어도 돼“. Die Outro-Zeile verliert `ipe();` und das `//` und behält nur „be still“. Die Notiz im Protokoll sagt, der Song behandle seine christliche Botschaft nicht, indem er sie direkt benennt, sondern sanft, allein durch die `//`-Kommentarzeilen. Was es bedeutet, dass das Kommentarzeichen den gesungenen Text verlassen hat, ist im Protokoll nicht festgehalten.

Das Zeichen kehrt im Untertitel- und Anzeigeblock des Pakets zurück. Seine Kopfzeile lautet `// 02 still compiling`, und darin stehen drei Chorus-Zeilen, zwei Bridge-Zeilen und drei Outro-Zeilen, auf Koreanisch. Dort kehren `// 그래도 괜찮아`, `// TODO: 좀 쉬어도 돼` und `ipe(); // be still` mit ihrem `//` zurück. Die letzte Zeile, `rest was written into the code`, die der Entwurf ohne Kommentarzeichen schrieb, erscheint im Untertitel mit `//` davor. Ein Kommentar, der aus dem gesungenen Text verschwindet und nur im Text auf dem Bildschirm auftaucht: So liest sich der Umgang dieses Songs mit `//`. Dasselbe geschah im [Vergleich des Entwurfs der ersten Single](/journal/de/from-draft-c-to-good-morning-world/).

## Was sich im Englischen ändert

Die sichtbarste Änderung in der englischen Fassung ist die Bridge. Der Entwurf eröffnet sie mit „// TODO: 좀 쉬어도 돼“, die englische Fassung hat „it's alright to rest“, dann „even unfinished, the world won't stop“. Die letzte Zeile ist „you did enough today — 충분히 수고했어“, die am Ende eines englischen Satzes einmal ins Koreanische wechselt. Auch „아직 끝나지 않아“ und „그래도 괜찮아“ im Chorus bleiben koreanisch. In der englisch geführten Fassung steht Koreanisch an drei Stellen: in der ersten und dritten Zeile des Chorus und in der letzten Zeile der Bridge.

## Die erste Zeile des Outros, be still

Die erste Zeile des Outros war im Entwurf `ipe(); // be still` und ist in den eingegebenen Texten „be still“. Die englische Fassung trägt die Anweisung (whispered), die koreanische (속삭이듯). Auch die Abschnittsüberschrift im Entwurf lautet „Outro — 속삭이듯“. Die Notiz im Protokoll sagt, die Signatur des Songs `ipe. be still` sei im Outro enthalten, und dieser Song sei der Referenztrack, der ab N-001 angewendet wird. Danach folgt „process, you can rest now“ („process, 이제 좀 쉬어“ auf Koreanisch), und die letzte Zeile lautet in beiden Fassungen auf Englisch „rest was written into the code“. Die letzte Zeile ist in beiden Fassungen dieselbe.

## Was nicht festgehalten ist

Im Protokoll sind die Felder für den KI-Entwurf, den Überarbeitungsverlauf und die Details der Musikgenerierung leer. Dieser Teil wurde also nicht festgehalten. Konkret kann dieser Beitrag nicht sagen, wie der erste Text aussah, welche Zeilen von einem Menschen geändert wurden, warum im Englischen Wörter hinzukamen und was bei mehreren Generierungen aus welchem Grund ausgewählt wurde. Wie sich die eingegebenen Texte vom Entwurf unterscheiden, ist nur das Ergebnis des Lesens der beiden Dateien gegeneinander, wie oben.

## Anhören

- N-001 still compiling — [Englische Fassung](https://youtu.be/O0PkHQYi2PE) · [Koreanische Fassung](https://youtu.be/Pq0nMvQrwIo)

Die allgemeine Reihenfolge, in der ein Song entsteht, steht in [Wie ein Song entsteht](/journal/de/how-a-song-gets-made/). Noch einmal, schlicht: Die Musik wird mit KI (Suno) produziert. Die Texte werden von der KI entworfen und von einem Menschen geprüft. Du kannst auch auf der [idle()-Startseite](/) zuhören.
