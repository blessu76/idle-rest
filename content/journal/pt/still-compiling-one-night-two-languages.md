---
title: still compiling — Uma noite, dois idiomas
date: 2026-10-30
time: "10:22"
slug: still-compiling-one-night-two-languages
lang: pt
description: O rascunho da letra de "still compiling", primeira canção de late_night.lofi, ao lado das letras das duas versões, e o destino de seus três comentários //.
category: behind-the-music
draft: false
translation_of: en
keywords: still compiling, N-001, late_night.lofi, lo-fi, rascunho da letra, comentários de código, be still, idle(), ipe(), música com IA, Suno
---

"still compiling" é a primeira canção da série `late_night.lofi`, canção número N-001. É uma canção para quem ainda está diante do monitor às duas da manhã, esperando um build terminar. Esta canção também tem a letra em duas camadas. Uma é a letra em coreano no arquivo de rascunho. A outra são as letras realmente inseridas na ferramenta de música, em uma versão em inglês e uma versão em coreano. Este texto lê as duas lado a lado. O que importa observar é o que aconteceu com as três linhas de comentário `//` do rascunho depois que a letra foi inserida.

Primeiro, o escopo. O que lemos: o rascunho da letra, o registro de criação, o documento do pacote de produção e o arquivo de descrição da pasta com as capturas de tela da produção. Não descrevemos como algo soa a partir da audição, e as configurações de estilo no pacote são entradas, não o som da gravação. E, como sempre: a música é produzida com IA (Suno). As letras são rascunhadas por IA e revisadas por uma pessoa.

## Onde a canção se situa, e suas duas versões

O cabeçalho do arquivo de rascunho lista a canção como lo-fi, com o tema "a tristeza de um desenvolvedor", e como o segundo lançamento. Como ler o nome da série está em [As seis séries de idle()](/journal/pt/six-series-of-idle/). As datas no registro são estas: o rascunho da letra foi concluído em 2026-06-29, a música foi gerada em 2026-06-30 (pelo registro na pasta de capturas de tela) e a data de lançamento é 2026-07-06.

Há duas versões. O pacote de produção separa a versão A, conduzida em inglês com coreano misturado aqui e ali, da versão B, conduzida em coreano com inglês misturado, e diz que a que vai para a página inicial é a A. O registro lista tanto a versão em inglês quanto a em coreano com voz masculina.

## Vinte linhas e vinte e uma

A letra no arquivo de rascunho tem seis seções e vinte linhas: quatro no Verse 1, duas no Pre-Chorus, quatro no Chorus, quatro no Verse 2, três na Bridge e três no Outro. As letras inseridas acrescentam uma linha de Intro, e chegam a vinte e uma. O Intro em inglês é "two a.m. — still compiling" e o em coreano é "새벽 두 시, still compiling". Nas duas versões é uma linha que o rascunho não tinha, e uma indicação entre colchetes pede que comece suave. As outras vinte linhas mantêm a ordem das seções e o número de linhas do rascunho.

A versão em coreano está quase intacta. As únicas diferenças são que "롤백" no Verse 2 está escrito como rollback, e o tratamento do `//`, a que chegamos abaixo. A versão em inglês é uma paráfrase. O "빨간 줄 하나에 무너진 하루" do rascunho vira "one red line, and the day falls apart", e "한 줄 고치면 두 줄이 우는데" vira "fix one line and two more cry". O sentido passa linha por linha, mas algumas palavras foram acrescentadas na passagem para o inglês: "tonight" no Pre-Chorus, "but I go on" no fim do Verse 2 e "we wrote for you" no fim do Chorus. O registro não diz por que foram acrescentadas.

## Uma noite escrita em termos de build

A cena desta canção é feita só de vocabulário de build: duas da manhã, um cursor piscando, uma linha vermelha, duas outras linhas que choram quando se corrige uma, uma especificação que mudou. O refrão abre com "still compiling, 아직 끝나지 않아" e segue até "무한 루프 같은 이 밤을 도는 중". No Verse 2 há uma ponta de dedo sobre o botão de deploy, uma luz verde fica vermelha e, depois de um rollback e de um pedido de desculpas, o amanhecer volta. A palavra burnout é assustadora demais para ser dita. A letra se lê como o log de build de uma noite, e esse log não termina em sucesso. Só na Bridge a voz muda: "다 못 끝내도 세상은 안 멈춰 / 충분히 수고했어, 오늘도".

## Os três comentários `//`

O rascunho tem três linhas que começam com `//`:

- Chorus: `// 그래도 괜찮아`
- Bridge: `// TODO: 좀 쉬어도 돼`
- Outro: `ipe(); // be still`

Nas letras inseridas, as três perdem o `//`. Mas nem todas as palavras se perdem. A linha do Chorus vira "but it's okay — 그래도 괜찮아" na versão em inglês e "그래도 괜찮아" na em coreano. A linha da Bridge perde o `TODO:` e vira "it's alright to rest" em inglês e "좀 쉬어도 돼" em coreano. A linha do Outro perde `ipe();` e o `//` e guarda só "be still". A anotação do registro diz que a canção trata sua mensagem cristã não nomeando-a diretamente, mas com suavidade, só por meio das linhas de comentário `//`. O que significa o marcador de comentário ter saído da letra cantada não está escrito no registro.

O marcador volta no bloco de legendas e de exibição do pacote. Seu cabeçalho é `// 02 still compiling`, e dentro dele estão três linhas do Chorus, duas da Bridge e três do Outro, em coreano. Ali `// 그래도 괜찮아`, `// TODO: 좀 쉬어도 돼` e `ipe(); // be still` voltam com o `//`. A última linha, `rest was written into the code`, que o rascunho escrevia sem marca de comentário, aparece na legenda com `//` na frente. Um comentário que desaparece da letra cantada e só aparece no texto na tela: é assim que esta canção parece usar o `//`. O mesmo aconteceu na [comparação do rascunho do primeiro single](/journal/pt/from-draft-c-to-good-morning-world/).

## O que muda no inglês

A mudança mais visível na versão em inglês é a Bridge. O rascunho a abre com "// TODO: 좀 쉬어도 돼", enquanto a versão em inglês tem "it's alright to rest", depois "even unfinished, the world won't stop". A última linha é "you did enough today — 충분히 수고했어", que passa uma vez para o coreano no fim de uma frase em inglês. O "아직 끝나지 않아" e o "그래도 괜찮아" do Chorus também ficam em coreano. Na versão conduzida em inglês, o coreano aparece em três lugares: a primeira e a terceira linhas do Chorus e a última linha da Bridge.

## A primeira linha do Outro, be still

A primeira linha do Outro era `ipe(); // be still` no rascunho e é "be still" nas letras inseridas. A versão em inglês traz a indicação (whispered) e a em coreano (속삭이듯). O cabeçalho da seção no rascunho também é "Outro — 속삭이듯". A anotação do registro diz que a assinatura da canção, `ipe. be still`, está incluída no Outro, e que esta canção é a faixa de referência aplicada a partir de N-001. Depois dela vem "process, you can rest now" ("process, 이제 좀 쉬어" em coreano), e a última linha é, em inglês nas duas versões, "rest was written into the code". A última linha é a mesma nas duas versões.

## O que não está registrado

No registro, os campos do rascunho de IA, do histórico de revisões e dos detalhes da geração de música estão vazios. Então essa parte não foi guardada. Em concreto, como era a primeira letra, quais linhas uma pessoa mudou, por que palavras foram acrescentadas no inglês e o que foi escolhido, com base em quê, entre várias gerações são coisas que este texto não pode dizer. Como as letras inseridas diferem do rascunho é apenas o resultado de ler os dois arquivos um contra o outro, como acima.

## Ouvir

- N-001 still compiling — [Versão em inglês](https://youtu.be/O0PkHQYi2PE) · [Versão em coreano](https://youtu.be/Pq0nMvQrwIo)

A ordem geral em que uma canção é feita está em [Como uma canção é feita](/journal/pt/how-a-song-gets-made/). Mais uma vez, com simplicidade: a música é produzida com IA (Suno). As letras são rascunhadas por IA e revisadas por uma pessoa. Você também pode ouvir na [página inicial de idle()](/).
