# Banners y efectos tuluzencasa

Segundo fragmento de WPCode, independiente de «Efectos tuluzencasa». Sin librerías ni archivos externos.

| Archivo | Para qué | Peso | Con gzip |
|---|---|---|---|
| `banners-tuluzencasa.min.html` | **El que se pega en WPCode** | 18.977 bytes | 6.815 bytes |
| `banners-tuluzencasa.html` | Versión legible y comentada, para editar | 21.456 bytes | 7.614 bytes |

## Cómo instalarlo
1. WPCode › Añadir fragmento › **Añade tu código personalizado** › tipo **Fragmento HTML** (no «JavaScript»).
2. Título: «Banners y efectos tuluzencasa». Pega el contenido entero de `banners-tuluzencasa.min.html`.
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

## Fuera de este fragmento
La portada publicada no tiene margen lateral entre 769 y 1024 px: el texto toca el borde (se ve en `capturas/1-portada-tablet.jpg` y también sin el fragmento). Se arregla en «Diseño tuluzencasa» con un margen interior para `.tl-home` en tablet.
