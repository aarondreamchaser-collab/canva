# Rediseño 2 de tuluzencasa (aprobado, 7-10-2026)

**Estado: aprobado con cambios (sin subtítulo). Pendiente de pegar en WPCode, paso a paso.** Las capturas están hechas sobre el HTML real publicado, con el CSS, la plantilla, los fragmentos y la portada nuevos.

## Referencias
Webs profesionales del sector, revisadas el 7-10-2026: NerdWallet, EnergySage y Kelisto (portada y artículo), y Rastreator. Se copia la **organización**, no el diseño ni los textos:
- **Portada:** primero un buscador y las acciones principales, luego las cifras de confianza, las herramientas, los temas, una guía destacada con una lista al lado, los últimos artículos, cómo trabajamos y una llamada final.
- **Artículo:** cabecera con título, autor, fecha y tiempo de lectura; índice lateral fijo «En esta página»; tablas y cajas cuidadas.
- **Categoría:** cabecera de color y cuadrícula de tarjetas sin barra lateral.
- **Pie:** oscuro, con columnas.

## Qué cambia

| Zona | Cambio |
|---|---|
| Cabecera | Fija al bajar, sin cambiar de tamaño (no mueve nada). «Calculadoras» como botón en escritorio. |
| Portada | Hero en dos columnas: buscador, búsquedas frecuentes y botones a la izquierda; tarjeta «Lo que cuesta cada aparato al mes» a la derecha, con cifras que salen de `calculos/`. Después: cifras de confianza, calculadoras con sus ventajas, temas, guías imprescindibles (una destacada con imagen y una lista), últimos artículos, «Cómo hacemos los cálculos» y llamada final. |
| Artículo | La imagen pasa debajo del título. Tiempo de lectura (sin subtítulo: el titular pidió quitarlo) y sello «Cifras calculadas con fuentes oficiales». Índice lateral fijo que marca la sección que lees; el de dentro del texto se oculta en escritorio y tablet y sigue en móvil. H2 más marcados. Tablas con cabecera azul y filas alternas. El párrafo final «Calcula tu caso exacto» se convierte en una caja. En la barra lateral de las entradas se ocultan el buscador (ya está en la cabecera) y «Artículos recientes». |
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
| `para-pegar/1-banners-y-efectos-tuluzencasa.html` | Código final del fragmento «Banners y efectos tuluzencasa». Copia de `../banners/banners-tuluzencasa.min.html`. |
| `para-pegar/2-plantilla-tuluzencasa.php` | Código final de «Plantilla tuluzencasa», ya sin la etiqueta de apertura de PHP. Igual a `wpcode-plantilla-v2.php`. |
| `para-pegar/3-diseno-tuluzencasa.css` | Código final de «Diseño tuluzencasa». Igual a `wpcode-diseno-v2.css`. |
| `diseno-v2-anadido.css`, `plantilla-v2-anadido.php` | Solo lo nuevo, para revisar los cambios. |
| `portada-v2.html` | Contenido nuevo de la página 23. Lo sube Claude por la API. |
| `generar_portada_v2.py` | Genera la portada y comprueba que las cifras de la tarjeta están en `calculos/`. |
| `preview/` | Vista previa: `construir_preview.py`, `harness.php` (WordPress simulado). |
| `capturas/` | `comparar-*`: ahora frente a propuesta. `propuesta-*`: página completa en los 3 anchos. |

## Fallo de la calculadora de potencia con los banners activos (7-10-2026)
- **Síntoma:** al activar «Banners y efectos tuluzencasa», la calculadora de potencia salía sin lista de aparatos y con el desplegable vacío.
- **Causa (corregida tras revisar la web el 7-10-2026):** al fragmento «Efectos tuluzencasa» publicado le falta el `</script>` final. El navegador sigue leyendo como parte de ese script el fragmento siguiente del pie, que es el de la calculadora de potencia (109). Los dos fallan con «Unexpected token '<'», la lista de aparatos queda vacía y el desplegable sin opciones. Por eso la copia de la portada de aquel día parecía no llevar el fragmento 109: estaba dentro del script de Efectos. La primera explicación («el 109 no se imprimía») era incorrecta.
- **Arreglo:** en WPCode › «Efectos tuluzencasa», añadir `</script>` al final, o pegar entero `../efectos/efectos-tuluzencasa.html`.
- **Prueba con los 3 códigos finales y el fragmento 109 presente:** las dos calculadoras dan los mismos resultados que hoy en escritorio (1280 px) y móvil (390 px). Potencia: lista de 25 aparatos, 7 potencias, marcar, cambiar potencia, «Otro aparato» y «Vaciar». Consumo: 33 aparatos, 7 potencias, vaciar, añadir, ejemplo, cambiar potencia, tarifa por horas y botones rápidos. Sin errores de JavaScript.
- **Arreglo añadido:** con la cabecera fija, al pulsar un botón rápido la calculadora de consumo subía y su parte de arriba quedaba debajo de la cabecera. Se añade `scroll-margin-top:96px` a las dos calculadoras.

## Orden para pegar (paso a paso; Claude comprueba la web publicada después de cada uno)

| # | Quién | Paso |
|---|---|---|
| 0 | Titular | En WPCode › «Efectos tuluzencasa», comprobar que el código termina en `</script>`. |
| 1 | Titular | Editar el fragmento **existente** «Banners y efectos tuluzencasa» (HTML, cabecera de todo el sitio): borrar su código, pegar `1-banners-y-efectos-tuluzencasa.html`, guardar y activar. Volver a activar «Efectos tuluzencasa» (pie). |
| 2 | Titular | Editar «Plantilla tuluzencasa» (PHP): borrar el código y pegar `2-plantilla-tuluzencasa.php` entero. Guardar. |
| 3 | Titular | Editar «Diseño tuluzencasa» (CSS): borrar el código y pegar `3-diseno-tuluzencasa.css` entero. Guardar. |
| 4 | Claude | Página 23: subir `portada-v2.html`, con copia previa (ya guardada en `copia-seguridad/2026-10-07-rediseno2/`). Comprobar la web publicada en los 3 anchos. |

- La plantilla va antes que el CSS porque el CSS nuevo oculta el pie antiguo (con los enlaces legales). Si se pega antes que la plantilla, la web se queda un rato sin pie.
- Entre el paso 2 y el 3, el pie nuevo y el índice lateral se ven sin estilo unos minutos. Es normal.
- En cada comprobación, Claude mira que las dos calculadoras cargan su código y funcionan, además del diseño.

## Deshacer
- **CSS, PHP y banners:** pegar las copias de `copia-seguridad/2026-10-07-rediseno2/` (`banners-antes.html`, `plantilla-antes.php`, `diseno-publicado.css`) o el código anterior de cada fragmento.
- **Portada:** volver a subir `copia-seguridad/2026-10-07-rediseno2/pagina-23-portada.html`.
