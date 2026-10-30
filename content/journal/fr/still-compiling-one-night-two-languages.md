---
title: still compiling — Une nuit, deux langues
date: 2026-10-30
time: "10:22"
slug: still-compiling-one-night-two-languages
lang: fr
description: Nous comparons le brouillon de « still compiling », première chanson de late_night.lofi, aux paroles de ses deux versions et suivons ses 3 commentaires //.
category: behind-the-music
draft: false
translation_of: en
keywords: still compiling, N-001, late_night.lofi, lo-fi, brouillon des paroles, commentaires de code, be still, idle(), ipe(), musique IA, Suno
---

« still compiling » est la première chanson de la série `late_night.lofi`, la chanson numéro N-001. C'est une chanson pour quelqu'un qui est encore devant son écran à deux heures du matin, à attendre la fin d'un build. Cette chanson a elle aussi ses paroles en deux couches. L'une est la parole coréenne du fichier de brouillon. L'autre est celle qui a été réellement saisie dans l'outil de musique, en une version anglaise et une version coréenne. Cet article lit les deux côte à côte. Ce qu'il faut observer, c'est ce que sont devenues les trois lignes de commentaire `//` du brouillon une fois les paroles saisies.

D'abord, le périmètre. Ce que nous avons lu : le brouillon des paroles, le journal de création, le document du dossier de production et le fichier de description du dossier qui contient les captures d'écran de la production. Nous ne décrivons pas le son à partir de l'écoute, et les réglages de style du dossier sont des entrées, pas ce que l'enregistrement donne à entendre. Et, comme toujours : la musique est produite avec l'IA (Suno). Les paroles sont rédigées en brouillon par l'IA et relues par une personne.

## Où se situe la chanson, et ses deux versions

L'en-tête du fichier de brouillon présente la chanson comme lo-fi, sur le thème « la peine d'un développeur », et comme la deuxième sortie. La façon de lire le nom de la série est dans [Les six séries d'idle()](/journal/fr/six-series-of-idle/). Les dates du journal sont les suivantes : le brouillon des paroles a été terminé le 2026-06-29, la musique a été générée le 2026-06-30 (d'après la trace du dossier de captures d'écran) et la date de sortie est le 2026-07-06.

Il y a deux versions. Le dossier de production sépare la version A, menée en anglais avec du coréen mêlé çà et là, de la version B, menée en coréen avec de l'anglais mêlé, et dit que celle qui va sur la page d'accueil est la A. Le journal indique la version anglaise comme la version coréenne avec une voix masculine.

## Vingt lignes et vingt et une

La parole du fichier de brouillon compte six sections et vingt lignes : quatre dans le Verse 1, deux dans le Pre-Chorus, quatre dans le Chorus, quatre dans le Verse 2, trois dans le Bridge et trois dans l'Outro. Les paroles saisies ajoutent une ligne d'Intro, ce qui en fait vingt et une. L'Intro anglaise est « two a.m. — still compiling » et la coréenne « 새벽 두 시, still compiling ». Dans les deux versions, c'est une ligne que le brouillon n'avait pas, et une indication entre crochets demande qu'elle commence doucement. Les vingt autres lignes gardent l'ordre des sections et le nombre de lignes du brouillon.

La version coréenne est presque intacte. Les seules différences sont que « 롤백 » dans le Verse 2 est écrit rollback, et le traitement de `//`, que nous verrons plus bas. La version anglaise est une paraphrase. Le « 빨간 줄 하나에 무너진 하루 » du brouillon devient "one red line, and the day falls apart", et le « 한 줄 고치면 두 줄이 우는데 » devient "fix one line and two more cry". Le sens passe ligne à ligne, mais quelques mots ont été ajoutés dans le passage à l'anglais : "tonight" dans le Pre-Chorus, "but I go on" à la fin du Verse 2 et "we wrote for you" à la fin du Chorus. Le journal ne dit pas pourquoi ils ont été ajoutés.

## Une nuit écrite en termes de build

La scène de cette chanson n'est faite que de vocabulaire de build : deux heures du matin, un curseur qui clignote, une ligne rouge, deux autres lignes qui pleurent quand on en corrige une, une spécification qui a changé. Le refrain s'ouvre sur « still compiling, 아직 끝나지 않아 » et court jusqu'à « 무한 루프 같은 이 밤을 도는 중 ». Dans le Verse 2, un doigt est posé sur le bouton de déploiement, un voyant vert passe au rouge et, après un rollback et des excuses, l'aube revient. Le mot burnout fait trop peur pour être dit. La parole se lit comme le journal de build d'une nuit, et ce journal ne se termine pas par un succès. Ce n'est que dans le Bridge que la voix change : « 다 못 끝내도 세상은 안 멈춰 / 충분히 수고했어, 오늘도 ».

## Les trois commentaires `//`

Le brouillon a trois lignes qui commencent par `//` :

- Chorus : `// 그래도 괜찮아`
- Bridge : `// TODO: 좀 쉬어도 돼`
- Outro : `ipe(); // be still`

Dans les paroles saisies, les trois perdent leur `//`. Mais tous les mots ne sont pas perdus. La ligne du Chorus devient « but it's okay — 그래도 괜찮아 » dans la version anglaise et « 그래도 괜찮아 » dans la coréenne. La ligne du Bridge perd son `TODO:` et devient « it's alright to rest » en anglais et « 좀 쉬어도 돼 » en coréen. La ligne de l'Outro perd `ipe();` et le `//` et ne garde que « be still ». La note du journal dit que la chanson traite son message chrétien non pas en le nommant directement, mais avec douceur, par les seules lignes de commentaire `//`. Ce que signifie le fait que la marque de commentaire ait quitté la parole chantée n'est pas écrit dans le journal.

La marque revient dans le bloc de sous-titres et d'affichage du dossier. Son en-tête est `// 02 still compiling`, et il contient trois lignes du Chorus, deux du Bridge et trois de l'Outro, en coréen. Là, `// 그래도 괜찮아`, `// TODO: 좀 쉬어도 돼` et `ipe(); // be still` reviennent avec leur `//`. La dernière ligne, `rest was written into the code`, que le brouillon écrivait sans marque de commentaire, apparaît dans les sous-titres précédée de `//`. Un commentaire qui disparaît de la parole chantée et ne se montre que dans le texte à l'écran : c'est ainsi que se lit l'usage que cette chanson fait de `//`. La même chose s'est produite dans [la comparaison du brouillon du premier single](/journal/fr/from-draft-c-to-good-morning-world/).

## Ce qui change en anglais

Le changement le plus visible de la version anglaise est dans le Bridge. Le brouillon l'ouvre par « // TODO: 좀 쉬어도 돼 », alors que la version anglaise a "it's alright to rest", puis "even unfinished, the world won't stop". La dernière ligne est "you did enough today — 충분히 수고했어", qui passe au coréen une fois à la fin d'une phrase anglaise. Le « 아직 끝나지 않아 » et le « 그래도 괜찮아 » du Chorus restent aussi en coréen. Dans la version menée en anglais, le coréen se trouve à trois endroits : les première et troisième lignes du Chorus, et la dernière ligne du Bridge.

## La première ligne de l'Outro, be still

La première ligne de l'Outro était `ipe(); // be still` dans le brouillon et c'est « be still » dans les paroles saisies. La version anglaise porte l'indication (whispered) et la version coréenne (속삭이듯). L'en-tête de section du brouillon est aussi « Outro — 속삭이듯 ». La note du journal dit que la signature de la chanson, `ipe. be still`, est incluse dans l'Outro, et que cette chanson est la piste de référence appliquée à partir de N-001. Vient ensuite « process, you can rest now » (« process, 이제 좀 쉬어 » en coréen), et la dernière ligne est, en anglais dans les deux versions, « rest was written into the code ». La dernière ligne est la même dans les deux versions.

## Ce qui n'est pas consigné

Dans le journal, les champs du brouillon de l'IA, de l'historique des révisions et des détails de génération musicale sont vides. Cette partie n'a donc pas été consignée. Concrètement, ce à quoi ressemblait la première parole, quelles lignes ont été modifiées par une personne, pourquoi des mots ont été ajoutés en anglais, et ce qui a été choisi sur quelle base parmi plusieurs générations, cet article ne peut pas le dire. La façon dont les paroles saisies diffèrent du brouillon n'est que le résultat de la lecture des deux fichiers l'un contre l'autre, comme ci-dessus.

## Écouter

- N-001 still compiling — [version anglaise](https://youtu.be/O0PkHQYi2PE) · [version coréenne](https://youtu.be/Pq0nMvQrwIo)

L'ordre général dans lequel une chanson se fait est dans [Comment se fait une chanson](/journal/fr/how-a-song-gets-made/). Encore une fois, simplement : la musique est produite avec l'IA (Suno). Les paroles sont rédigées en brouillon par l'IA et relues par une personne. Vous pouvez aussi écouter sur la [page d'accueil d'idle()](/).
