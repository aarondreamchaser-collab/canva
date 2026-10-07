# Rediseño 2 de tuluzencasa (propuesta, 7-10-2026)

**Estado: vista previa. No se ha aplicado nada en la web.** Las capturas están hechas sobre el HTML real publicado, con el CSS, la plantilla, los fragmentos y la portada nuevos.

## Referencias
Webs profesionales del sector, revisadas el 7-10-2026: NerdWallet, EnergySage y Kelisto (portada y artículo), y Rastreator. Se copia la **organización**, no el diseño ni los textos:
- **Portada:** primero un buscador y las acciones principales, luego las cifras de confianza, las herramientas, los temas, una guía destacada con una lista al lado, los últimos artículos, cómo trabajamos y una llamada final.
- **Artículo:** cabecera con título, subtítulo, autor, fecha y tiempo de lectura; índice lateral fijo «En esta página»; tablas y cajas cuidadas.
- **Categoría:** cabecera de color y cuadrícula de tarjetas sin barra lateral.
- **Pie:** oscuro, con columnas.

## Qué cambia

| Zona | Cambio |
|---|---|
| Cabecera | Fija al bajar, sin cambiar de tamaño (no mueve nada). «Calculadoras» como botón en escritorio. |
| Portada | Hero en dos columnas: buscador, búsquedas frecuentes y botones a la izquierda; tarjeta «Lo que cuesta cada aparato al mes» a la derecha, con cifras que salen de `calculos/`. Después: cifras de confianza, calculadoras con sus ventajas, temas, guías imprescindibles (una destacada con imagen y una lista), últimos artículos, «Cómo hacemos los cálculos» y llamada final. |
| Artículo | La imagen pasa debajo del título. Subtítulo (el extracto), tiempo de lectura y sello «Cifras calculadas con fuentes oficiales». Índice lateral fijo que marca la sección que lees; el de dentro del texto se oculta en escritorio y tablet y sigue en móvil. H2 más marcados. Tablas con cabecera azul y filas alternas. El párrafo final «Calcula tu caso exacto» se convierte en una caja. En la barra lateral de las entradas se ocultan el buscador (ya está en la cabecera) y «Artículos recientes». |
| Categorías, búsqueda | Cabecera azul con el nº de guías. Cuadrícula de tarjetas (3 en escritorio, 2 en tablet, 1 en móvil), sin barra lateral. |
| Pie | Oscuro, con 4 columnas: marca, temas, calculadoras y guías, y la web (páginas legales). Sustituye al menú legal y a «Creado con GeneratePress». |
| Fragmento de banners | Arreglado el fallo que quitaba el fondo a los botones «Abrir la calculadora» de la portada: el subrayado amarillo de los enlaces solo se aplica dentro de las entradas. Nuevo: el índice lateral marca la sección que estás leyendo. |

**Pruebas:** portada, artículo, categoría y calculadora en escritorio (1280 px), tablet (820 px) y móvil (390 px).
- **CLS:** 0 en las 12 combinaciones.
- **Desbordes horizontales:** ninguno.
- **Bloques de la portada:** 87, todos válidos.
- **PHP:** sin errores de sintaxis, ejecutado con WordPress simulado.

## Archivos

| Archivo | Para qué |
|---|---|
| `wpcode-diseno-v2.css` | Sustituye entero al CSS «Diseño tuluzencasa». Es el CSS publicado de hoy con el bloque «Rediseño 2» al final. |
| `wpcode-plantilla-v2.php` | Sustituye entero al PHP «Plantilla tuluzencasa». Es la plantilla actual con los apartados 7 a 10 al final. |
| `../banners/banners-tuluzencasa.min.html` | Sustituye al código del fragmento «Banners y efectos tuluzencasa». |
| `portada-v2.html` | Contenido nuevo de la página 23. Lo sube Claude por la API. |
| `generar_portada_v2.py` | Genera la portada y comprueba que las cifras de la tarjeta están en `calculos/`. |
| `preview/` | Vista previa: `construir_preview.py`, `harness.php` (WordPress simulado). |
| `capturas/` | `comparar-*`: ahora frente a propuesta. `propuesta-*`: página completa en los 3 anchos. |

## Orden para aplicar (cuando se apruebe)

| # | Quién | Paso |
|---|---|---|
| 1 | Titular | WPCode › «Diseño tuluzencasa»: borrar el código y pegar `wpcode-diseno-v2.css`. |
| 2 | Titular | WPCode › «Plantilla tuluzencasa»: borrar el código y pegar `wpcode-plantilla-v2.php`, sin la primera línea `<?php`. |
| 3 | Titular | WPCode › «Banners y efectos tuluzencasa»: pegar el código nuevo y activarlo (cabecera). Volver a activar «Efectos tuluzencasa» (pie). |
| 4 | Claude | Página 23: subir `portada-v2.html`, con copia previa (ya guardada en `copia-seguridad/2026-10-07-rediseno2/`). Comprobar la web publicada en los 3 anchos. |

Los pasos 1 a 3 primero: con el CSS antiguo, la portada nueva se vería sin estilos.

## Deshacer
- **CSS, PHP y banners:** pegar las copias de `copia-seguridad/2026-10-07-rediseno2/` o el código anterior de cada fragmento.
- **Portada:** volver a subir `copia-seguridad/2026-10-07-rediseno2/pagina-23-portada.html`.
