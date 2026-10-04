# Mejoras de claridad, móvil y calculadoras (5 de octubre de 2026)

Revisión hecha en la web publicada con Chromium a 390, 360 y 1280 px. Nada de esto está aplicado en WordPress todavía.

## Los cinco problemas

| # | Dónde | Qué le pasa al visitante | Cambio propuesto | Archivo |
|---|---|---|---|---|
| 1 | Portada en móvil | El título, la entradilla y las tarjetas tocan los bordes de la pantalla (0 px de margen): cuesta leer y parece roto. | Recuperar 16 px de margen lateral solo en móvil. | `home-sin-script.propuesta.html` (una línea de CSS) |
| 2 | Calculadora de potencia, al abrirla | Con solo nevera, tele y luces (marcadas por defecto) ya dice «Pagas de más 96,09 €/año / Ahorrarías…» a todo el mundo. En móvil el detalle queda a 3.569 px, tras 25 aparatos. | No dar importes hasta que el visitante marque algo; tocar la barra fija lleva al resultado. | `calculadora-potencia.js` |
| 3 | Calculadora de potencia, datos | Solo potencias normalizadas, precio fijo 0,09 € y «Otro aparato» que recorta 25.000 W a 20.000 sin avisar, ignora «abc» y lee «1.200» como 1,2 W. | Potencia exacta, precio editable, hipótesis visibles, avisos de error sin cambiar lo escrito y lectura de «1.200». | `calculadora-potencia.js` + `bloque-html-personalizado-v2.html` |
| 4 | Calculadora de potencia, mensajes | «Puede saltar el limitador» sirve para dos casos distintos; la instrucción de marcar solo lo simultáneo es un texto pequeño. | «Los aparatos superan tu potencia contratada» frente a «Tienes potencia suficiente, pero poco margen»; aviso destacado; botón «Copiar resultado». | Ídem |
| 5 | Artículos y categorías en móvil | Títulos de 42 px (5–6 líneas): el texto empieza a ~700 px. Tablas de hasta 504 px en 330 px: la última columna queda oculta sin pista. | Títulos a 30 px, tablas a 14 px con sombra que indica que hay más a la derecha. | `wpcode-css-articulos-movil.css` |

Ya estaban aplicadas en la web (no se duplican): «Pagas de más al año», «Ahorrarías … €/año», «Coste adicional al año» y la marca «>9,2» en la escala y la barra cuando la potencia con margen supera 9,2 kW.

## Cómo se prueba

`calculadora-potencia/prueba/v2/montar_v2.py` monta las páginas con el HTML publicado y `prueba_v2.mjs` comprueba ahorro, coste adicional (supera y poco margen), igualdad, exceso de 9,2 kW, regreso al rango, potencia exacta, precio, «Otro aparato», copiar, barra móvil y reinicio a 1280, 390 y 360 px, más el JS nuevo con el marcado actual. Resultado: 84 comprobaciones correctas.
