# Banners y efectos tuluzencasa

Segundo fragmento de WPCode, independiente de «Efectos tuluzencasa». Sin librerías ni archivos externos.

| Archivo | Para qué | Peso | Con gzip |
|---|---|---|---|
| `banners-tuluzencasa.min.html` | **El que se pega en WPCode** | 26.984 bytes | 8.644 bytes |
| `banners-tuluzencasa.html` | Versión legible y comentada, para editar | 30.279 bytes | 9.799 bytes |

## Cómo instalarlo
1. WPCode › Añadir fragmento › **Añade tu código personalizado** › tipo **Fragmento HTML** (no «JavaScript»).
2. Título: «Banners y efectos tuluzencasa». Pega el contenido entero de `banners-tuluzencasa.min.html`. Si ya lo tenías instalado, sustituye todo el código anterior por este.
3. Inserción: **Automática** · Ubicación: **Cabecera de todo el sitio** (Site Wide Header).
4. Activar y guardar. Para quitarlo todo, desactívalo.

**Por qué en la cabecera y no en el pie.** La barra de anuncio, la cinta y la franja van arriba del todo. Si el código está en el pie, llega cuando el navegador ya puede haber pintado la cabecera, y meterlas después empujaría la página (saltos de diseño, CLS). Desde la cabecera, el código crea cada pieza en el mismo momento en que el navegador crea la cabecera, antes de pintarla. Así ocupan su sitio desde el principio y no mueven nada. Todo lo demás espera a que la página esté lista (`DOMContentLoaded`) y no retrasa la carga. Si se pusiera en el pie, la barra, la cinta y la franja no aparecerían; el resto funcionaría.

## Qué hace
| # | Pieza | Dónde | Detalles |
|---|---|---|---|
| 1 | Barra de anuncio | Todo el sitio, encima de la cabecera | Azul oscuro, rayo amarillo, 3 mensajes con enlace (calculadora de consumo, de potencia y bono social). Cambian cada 5 s con fundido y se paran con el ratón encima o con el foco del teclado. La X la cierra durante la visita (`sessionStorage`). En móvil, textos cortos. |
| 2 | Cinta deslizante | Portada, bajo la cabecera | Datos en bucle. Se para al pasar el ratón. |
| 3 | Tarjeta de calculadora | Entradas con 3 o más H2, hacia el 60 % del texto | Antes de un H2 que no tenga cerca ningún hueco de anuncio (`tl-hueco`), ni la caja de autor o los relacionados, y nunca en las preguntas frecuentes. Factura y tarifas y Averías e instalación enlazan a la calculadora de potencia; el resto, a la de consumo. Lleva «Herramienta gratis de tuluzencasa.com» para que no parezca un anuncio. |
| 4 | Botón fijo «Calcular mi consumo» | Entradas, a partir de la mitad | Abajo a la derecha en escritorio y tablet; barra fina de 48 px abajo en móvil. Se oculta si hay a la vista un anuncio (huecos de la plantilla o anuncios automáticos de AdSense, que se vigilan cada 2 s), la tarjeta, la caja de autor, los relacionados o el pie. En móvil también se oculta si hay un anuncio anclado de AdSense. |
| 5 | Franja de confianza | Portada, tras la cabecera de la página | Fuentes oficiales, cálculos propios, actualizado, sin registro. El nº de guías y el mes de la última actualización salen de la API de WordPress: una petición pequeña por visita, guardada 1 hora en la sesión. Las cifras cuentan al verse. |
| 6 | Tarjetas al pasar el ratón | Calculadoras y temas de la portada, últimos artículos, guías, relacionados, franja y tarjeta | Suben 4 px con sombra y borde amarillo. Solo con ratón (`hover: hover`). |
| 7 | Aparición suave | Secciones de la portada; títulos, tablas, imágenes, listas y cajas de las entradas | Solo lo que aún no se ve al cargar. Usa opacidad y desplazamiento (`transform`), que no mueven nada. |
| 8 | Preguntas frecuentes en acordeón | Entradas con `h2#preguntas-frecuentes` | La primera abierta. El texto sigue en la página (Google lo lee), con botón accesible (`aria-expanded`). La última respuesta no arrastra las «Fuentes oficiales» ni el cierre. Si la sección ya se ve al cargar, no se toca. |
| 9 | Volver arriba | Todo el sitio, al bajar 1,5 pantallas | Círculo azul con flecha amarilla. Sube por encima del botón fijo cuando este aparece. |

**Con «reducir movimiento»:** la barra no rota, la cinta no se mueve, las cifras no cuentan, no hay apariciones, brillo ni rayo animado, las tarjetas no suben y el acordeón se abre sin animación.

**En móvil:** sin efectos de ratón; barra fija fina; textos cortos en la barra.

### Efectos añadidos (7-10-2026)
| # | Efecto | Dónde | Detalles |
|---|---|---|---|
| 10 | Logo que se enciende | Todo el sitio | Encima del PNG va un rayo SVG calcado al píxel, invisible y sin ocupar sitio. Al cargar el logo, destella una vez con un halo amarillo. Al pasar el ratón, parpadea y se queda brillando. Si se cambia el archivo del logo (el nombre deja de contener «logo»), no se añade. |
| 11 | H1 con fundido | Todas las páginas (`h1.entry-title`, `h1.page-title`, portada) | Sube 14 px y aparece en 0,7 s. Es solo CSS: sin JavaScript termina igual, visible. |
| 12 | H2 con línea amarilla | Entradas | Fundido al llegar y una línea de 64 px que se dibuja de izquierda a derecha. Sin JavaScript, la línea se ve entera desde el principio. |
| 13 | Brillo en «luz» | Título de la portada | Un brillo amarillo recorre la palabra una vez. Va pintado por encima: el texto real no cambia y Google y los lectores de pantalla leen lo mismo. |
| 14 | Botones | Portada, tarjetas de calculadora, calculadoras, barra lateral, tarjeta del artículo | Con el ratón: suben 2 px, se ponen amarillos, los cruza un destello y la flecha → se desplaza. Al pulsar: se hunden. La flecha va en el CSS desde la primera pintura (no mueve nada). Los botones secundarios de las calculadoras («Cargar ejemplo», «Copiar enlace», la X…) solo suben y marcan el borde en amarillo; no cambian de color para no confundirse con los principales. |
| 15 | Latido de los 2 botones de la portada | Portada | Un halo amarillo suave cada 4,5 s, sin parpadeo. Se para al pasar el ratón. |
| 16 | Bloques destacados | Entradas | Cajas «Dato clave», tablas, imágenes y tarjeta de calculadora aparecen con fundido al llegar. Al rayo de «Dato clave» le salta una chispa. Los párrafos y las listas no se animan. |
| 17 | Enlaces del texto | Párrafos, listas y tablas de las entradas | Al pasar el ratón, un subrayado amarillo se dibuja de izquierda a derecha. |
| 18 | Menú | Escritorio (más de 1024 px) | Al pasar el ratón, una línea amarilla se dibuja bajo cada opción, y la sección actual la lleva fija. Los desplegables bajan con un fundido. En tablet y móvil, el menú hamburguesa se abre con un fundido corto. |
| 19 | Extras | Todo el sitio | Selección de texto en amarillo. Contorno amarillo al navegar con el teclado. Desplazamiento suave al pulsar el índice, y el H2 de destino se ilumina un momento. Filas de las tablas resaltadas al pasar el ratón. Zoom suave en las imágenes de «Últimos artículos» y de los relacionados. |

**En móvil y tablet** (pantalla táctil) no hay ningún efecto de ratón. Quedan los ligeros: fundidos, línea de los H2, destello del logo, brillo del título, latido de los botones y efecto de pulsar.

**Con «reducir movimiento»**, los efectos nuevos tampoco se mueven. Solo cambian los colores al pasar el ratón.

**Sin JavaScript**, todos los títulos, párrafos, tablas y cajas se ven (opacidad 1 comprobada en portada y dos artículos), y la línea de los H2 sale completa.

## Pruebas (6-10-2026)
Se probó con el HTML real de la web (portada, «Cuánto consume una lavadora» y «Qué potencia contratar»), con el fragmento añadido al final de `<head>` y sin anuncios cargados. Escritorio 1280 px, tablet 820 px y móvil 390 px; con y sin «reducir movimiento».

- **CLS: 0 en las 36 mediciones.**
- Tiempo del código al cargar: 1–13 ms en la mayoría de cargas, con picos de 19–42 ms en alguna primera carga.
- Tareas largas: una de 50 ms en una prueba de móvil; sin el fragmento salen tareas parecidas (53–88 ms), así que no se puede atribuir al fragmento.
- Primera pintura: igual con y sin el fragmento (~90–120 ms en local).
- La barra rota (mensaje 1 → 2 → 3), se para con el ratón encima, la X la cierra y sigue cerrada al recargar.
- Errores de JavaScript nuevos: ninguno. El aviso «Unexpected token '<'» sale igual sin el fragmento.
- Lighthouse no se puede ejecutar contra la web desde este entorno (Chromium no acepta el certificado del proxy).

Capturas en `capturas/`; scripts de prueba en `pruebas/`.

## Pruebas de los efectos añadidos (7-10-2026)
Se probaron sobre el HTML real de la portada, «Cuánto consume una lavadora», «Qué potencia contratar» y las dos calculadoras, en escritorio 1280 px, tablet 820 px y móvil 390 px, con y sin «reducir movimiento». Las pruebas se hicieron sin anuncios. Resultados en `pruebas/resultados2.txt`.

- **CLS: 0 en las 30 cargas con el fragmento.** Con «reducir movimiento», 0 también.
- Tiempo del código al cargar: 1–14 ms en la mayoría, con picos de 19–35 ms en alguna primera carga de artículo.
- Tareas largas: dos de 52–53 ms; sin el fragmento salen tareas iguales (50–65 ms).
- Primera pintura y LCP: iguales con y sin el fragmento (~80–150 ms en local). En escritorio, el LCP de la portada pasa del H1 al párrafo, con el mismo tiempo, porque el H1 empieza transparente.
- Una medición de LCP salió en 1,4 s en la portada en tablet. Es un efecto de la prueba: al bajar con `scrollTo`, Chrome cuenta como LCP la imagen de «Últimos artículos» cuando aparece. Bajando con la rueda del ratón, como un lector, el LCP se queda en 124 ms.
- Errores de JavaScript nuevos: ninguno.

GIF de cada efecto en `capturas/gif/` (grabados a cámara lenta y montados a velocidad real). El script de grabación es `pruebas/gif.mjs` y el de montaje, `pruebas/montar_gif.py`. Para regenerar el código mínimo y las páginas de prueba: `python3 pruebas/construir.py`.

## Fuera de este fragmento
La portada publicada no tiene margen lateral entre 769 y 1024 px: el texto toca el borde (se ve en `capturas/1-portada-tablet.jpg` y también sin el fragmento). Se arregla en «Diseño tuluzencasa» con un margen interior para `.tl-home` en tablet.
