---
title: still compiling — Una noche, dos idiomas
date: 2026-10-30
time: "10:22"
slug: still-compiling-one-night-two-languages
lang: es
description: Ponemos el borrador de "still compiling", primera canción de late_night.lofi, junto a las letras de sus dos versiones y seguimos sus tres comentarios //.
category: behind-the-music
draft: false
translation_of: en
keywords: still compiling, N-001, late_night.lofi, lo-fi, borrador de letra, comentarios de código, be still, idle(), ipe(), música con IA, Suno
---

"still compiling" es la primera canción de la serie `late_night.lofi`, la canción número N-001. Es una canción para quien sigue frente al monitor a las dos de la madrugada, esperando a que termine una compilación. Esta canción también tiene su letra en dos capas. Una es la letra en coreano del archivo de borrador. La otra es la letra que se introdujo de verdad en la herramienta de música, en una versión en inglés y otra en coreano. Esta entrada lee las dos lado a lado. Lo que hay que mirar es qué fue de las tres líneas de comentario `//` del borrador una vez introducida la letra.

Primero, el alcance. Lo que leímos: el borrador de la letra, el registro de creación, el documento del paquete de producción y el archivo de descripción de la carpeta que guarda las capturas de pantalla de la producción. No describimos cómo suena nada a partir de la escucha, y los ajustes de estilo del paquete son entradas, no cómo suena la grabación. Y, como siempre: la música se produce con IA (Suno). Las letras las redacta la IA como borrador y las revisa una persona.

## Dónde se sitúa la canción y sus dos versiones

El encabezado del archivo de borrador presenta la canción como lo-fi, con el tema "la tristeza de un desarrollador", y como el segundo lanzamiento. Cómo leer el nombre de la serie está en [Las seis series de idle()](/journal/es/six-series-of-idle/). Las fechas del registro son estas: el borrador de la letra se terminó el 2026-06-29, la música se generó el 2026-06-30 (según el registro de la carpeta de capturas) y la fecha de lanzamiento es el 2026-07-06.

Hay dos versiones. El paquete de producción separa la versión A, con el inglés como eje y algo de coreano mezclado aquí y allá, de la versión B, con el coreano como eje y algo de inglés mezclado, y dice que la que va en la página de inicio es la A. El registro anota tanto la versión en inglés como la versión en coreano con voz masculina.

## Veinte líneas y veintiuna

La letra del archivo de borrador tiene seis secciones y veinte líneas: cuatro en el Verse 1, dos en el Pre-Chorus, cuatro en el Chorus, cuatro en el Verse 2, tres en el Bridge y tres en el Outro. La letra introducida añade una línea de Intro, así que suma veintiuna. El Intro en inglés es "two a.m. — still compiling" y el coreano, "새벽 두 시, still compiling". En ambas versiones es una línea que el borrador no tenía, y una indicación entre corchetes pide que empiece con suavidad. Las otras veinte líneas conservan el orden de secciones y el número de líneas del borrador.

La versión en coreano está casi intacta. Las únicas diferencias son que "롤백" en el Verse 2 se escribe rollback, y el tratamiento de `//`, que veremos más abajo. La versión en inglés es una paráfrasis. El "빨간 줄 하나에 무너진 하루" del borrador pasa a "one red line, and the day falls apart", y el "한 줄 고치면 두 줄이 우는데" pasa a "fix one line and two more cry". El sentido se mantiene línea por línea, pero al pasar al inglés se añadieron algunas palabras: "tonight" en el Pre-Chorus, "but I go on" al final del Verse 2 y "we wrote for you" al final del Chorus. El registro no dice por qué se añadieron.

## Una noche escrita en términos de compilación

La escena de esta canción está hecha solo de vocabulario de compilación: las dos de la madrugada, un cursor parpadeante, una línea roja, otras dos líneas que lloran cuando arreglas una, una especificación que cambió. El estribillo abre con "still compiling, 아직 끝나지 않아" y sigue hasta "무한 루프 같은 이 밤을 도는 중". En el Verse 2 hay un dedo sobre el botón de despliegue, una luz verde se vuelve roja y, tras un rollback y una disculpa, vuelve a llegar el amanecer. La palabra burnout da demasiado miedo para decirla. La letra se lee como el registro de compilación de una noche, y ese registro no termina en éxito. Solo en el Bridge cambia la voz: "다 못 끝내도 세상은 안 멈춰 / 충분히 수고했어, 오늘도".

## Los tres comentarios `//`

El borrador tiene tres líneas que empiezan con `//`:

- Chorus: `// 그래도 괜찮아`
- Bridge: `// TODO: 좀 쉬어도 돼`
- Outro: `ipe(); // be still`

En la letra introducida, las tres pierden su `//`. Pero no se pierden todas las palabras. La línea del Chorus pasa a ser "but it's okay — 그래도 괜찮아" en la versión en inglés y "그래도 괜찮아" en la coreana. La línea del Bridge pierde su `TODO:` y queda como "it's alright to rest" en inglés y "좀 쉬어도 돼" en coreano. La línea del Outro pierde `ipe();` y el `//` y conserva solo "be still". La nota del registro dice que la canción trata su mensaje cristiano no nombrándolo directamente, sino con suavidad, solo a través de las líneas de comentario `//`. Qué significa que la marca de comentario saliera de la letra cantada no está escrito en el registro.

La marca vuelve en el bloque de subtítulos y pantalla del paquete. Su encabezado es `// 02 still compiling`, y dentro hay tres líneas del Chorus, dos del Bridge y tres del Outro, en coreano. Allí `// 그래도 괜찮아`, `// TODO: 좀 쉬어도 돼` e `ipe(); // be still` vuelven con su `//`. La última línea, `rest was written into the code`, que el borrador escribió sin marca de comentario, aparece en los subtítulos con `//` delante. Un comentario que desaparece de la letra cantada y solo se muestra en el texto de la pantalla: así se lee el uso que esta canción hace de `//`. Lo mismo ocurrió en [la comparación del borrador del primer sencillo](/journal/es/from-draft-c-to-good-morning-world/).

## Qué cambia en el inglés

El cambio más visible de la versión en inglés está en el Bridge. El borrador lo abre con "// TODO: 좀 쉬어도 돼", mientras que la versión en inglés tiene "it's alright to rest" y luego "even unfinished, the world won't stop". La última línea es "you did enough today — 충분히 수고했어", que pasa al coreano una vez al final de una frase en inglés. El "아직 끝나지 않아" y el "그래도 괜찮아" del Chorus también se quedan en coreano. En la versión con el inglés como eje, el coreano aparece en tres lugares: la primera y la tercera línea del Chorus y la última línea del Bridge.

## La primera línea del Outro, be still

La primera línea del Outro era `ipe(); // be still` en el borrador y es "be still" en la letra introducida. La versión en inglés lleva la indicación (whispered) y la versión en coreano, (속삭이듯). El encabezado de sección del borrador también es "Outro — 속삭이듯". La nota del registro dice que la firma de la canción, `ipe. be still`, está incluida en el Outro y que esta canción es la pista de referencia que se aplica desde N-001 en adelante. Después viene "process, you can rest now" ("process, 이제 좀 쉬어" en coreano), y la última línea es, en inglés en ambas versiones, "rest was written into the code". La última línea es la misma en las dos versiones.

## Lo que no consta

En el registro, los campos del borrador de la IA, del historial de revisiones y de los detalles de generación musical están vacíos. Así que esa parte no quedó registrada. En concreto, cómo era la primera letra, qué líneas cambió una persona, por qué se añadieron palabras en el inglés y qué se eligió, con qué criterio, entre varias generaciones son cosas que esta entrada no puede decir. Cómo difiere la letra introducida del borrador es solo el resultado de leer los dos archivos uno contra otro, como se ha visto.

## Escucha

- N-001 still compiling — [versión en inglés](https://youtu.be/O0PkHQYi2PE) · [versión en coreano](https://youtu.be/Pq0nMvQrwIo)

El orden general en que se hace una canción está en [Cómo se hace una canción](/journal/es/how-a-song-gets-made/). Una vez más, con claridad: la música se produce con IA (Suno). Las letras las redacta la IA como borrador y las revisa una persona. También puedes escuchar en la [página de inicio de idle()](/).
