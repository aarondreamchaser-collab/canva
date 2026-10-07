# Calculadoras v3 (propuesta, 7-10-2026)

**Estado: publicadas el 7-10-2026** (fragmentos 309 y 310; páginas 102 y 156).

## Qué hay de nuevo

### Consumo: «Tu casa en 3D» (`consumo3.min.js`, 46 KB; 16 KB comprimido)
- **Casa isométrica 3D:** cada habitación se ilumina de azul a rojo según lo que gasta, con «cables» de energía animados hasta el contador. Al tocar una habitación se filtran sus aparatos. En escritorio, la casa se inclina con el ratón.
- **Interruptores por aparato:** se ajustan potencia, horas, días, cuántos hay y la hora a la que empieza, con una barra de 24 h coloreada por tramos.
- **«Tu día, hora a hora»:** gráfica de la potencia encendida cada hora sobre los tramos punta, llano y valle, con la línea de tu potencia contratada. Puntos rojos donde puede saltar el limitador. Al pasar el dedo, dice la hora, el tramo, el precio y qué está encendido.
- **Asistente de ahorro:**
  - Busca la mejor hora para lo que se puede programar (lavadora, lavavajillas, secadora, termo y coche). Primero evita que salte el limitador y después elige la hora más barata.
  - Dice cuánto ahorras y lo aplica con un botón.
  - Compara precio único y tarifa por horas con tus horarios.
  - Mantiene los consejos de la calculadora anterior: te sobra potencia, sustituciones que compensan o no, y tu mayor gasto.
- **Tu factura:** con los kWh y los días de tu factura, dice qué parte explica tu lista y cuánto falta.
- **Escenarios A/B:** guardas tu casa, cambias cosas y ves la diferencia al año.
- **Hogares tipo:**
  - Piso de 1 persona.
  - Piso de 3 personas (el mismo ejemplo de antes: 58,78 €/mes).
  - Con bomba de calor.
  - Con coche eléctrico.
- **Más:**
  - Enlace para compartir (también abre los enlaces de la calculadora anterior).
  - Informe para imprimir.
  - Cifras que cuentan al cambiar.
  - Respeta «reducir movimiento».

### Potencia: «Cuadro eléctrico virtual» (`potencia3.min.js`, 24 KB; 8 KB comprimido)
- **Medidor de aguja de 0 a 10 kW:** marca tu potencia contratada y la zona roja.
- **Limitador (ICP) animado:** si te pasas, la palanca baja, el piloto parpadea y la pantalla hace un pequeño «apagón».
- **Interruptores por aparato:** los mismos 25 aparatos de antes, con ×1, ×2 y ×3, y «Otro aparato».
- **Situaciones típicas:** cena entre semana, mañana con prisa, tarde de verano, noche de invierno y cargando el coche.
- **«Encender uno a uno»:** enciende los aparatos de menor a mayor hasta ver cuándo salta.
- **Resultados:** potencia recomendada con el 10 % de margen, cuánto ahorras o pagas de más al año, y tabla de lo que cuesta cada potencia, con las que «saltarían».
- **Enlace para compartir.**

## Mismas cifras que antes
- Mismos precios, factores de uso, término de potencia (0,09 €/kW y día), impuestos, contador y lista de aparatos que las calculadoras actuales. Los aparatos se copian al montar desde `calculadora.js` y el fragmento 109.
- **Comprobado:**
  - Ejemplo de 3 personas a precio único: **58,78 €/mes** y pico de **5,27 kW**, igual que hoy.
  - Potencia con nevera, tele y LED: **0,34 kW**; recomienda **2,3 kW** y un ahorro de **96,09 €/año**, igual que hoy.
- Con la tarifa por horas, la v3 calcula hora a hora (más preciso que las franjas de antes). Por eso esos importes pueden variar unos céntimos frente a la calculadora anterior.

## Pruebas (vista previa sobre la página publicada)
- **Anchos:** escritorio 1280 px y móvil 390 px.
- **Funciones probadas:** todas (encender, ajustar, hora, tarifa, optimizar, escenarios, habitación, factura, hogares tipo, situaciones, ×2, «Encender uno a uno», otro aparato, rearmar).
- **Errores de JavaScript:** 0.
- **Desbordes horizontales:** ninguno.
- **CLS:** 0,0015 y 0 (antes de reservar el hueco era 0,27 y 0,31).

## Archivos
| Archivo | Para qué |
|---|---|
| `consumo3.min.js` | Fragmento JavaScript nuevo «Calculadora consumo v3» (pie de todo el sitio). |
| `potencia3.min.js` | Fragmento JavaScript nuevo «Calculadora potencia v3» (pie de todo el sitio). |
| `pagina-consumo3.html` | Contenido nuevo de la página 156: el mismo texto, con la calculadora vieja cambiada por `#tl3-consumo` y el hueco reservado. |
| `pagina-potencia3.html` | Contenido nuevo de la página 102, igual con `#tl3-potencia`. |
| `*.src.js`, `construir.py` | Código legible; `python3 construir.py` monta los `.js` y los `.min.js`. |
| `reserva.css` | Hueco reservado (ya incluido en las dos páginas). |
| `pruebas/`, `capturas/` | Pruebas con Playwright y capturas. |

## Estado (7-10-2026)
- **Fragmentos:** el titular crea en WPCode «Calculadora consumo v3» y «Calculadora potencia v3» (JavaScript, pie de todo el sitio), **inactivos**.
- **Calendario:** se activan después de la aprobación de AdSense.
- **Páginas 156 y 102:** no se tocan hasta que el titular avise.

## Día de la activación (orden exacto)
| # | Quién | Paso | Comprobación |
|---|---|---|---|
| 0 | Claude | Comprobar en la web que «Efectos» sigue cerrado con `</script>` y que las dos calculadoras actuales funcionan. | Si algo falla, se para aquí. |
| 1 | Titular | Activar «Calculadora consumo v3» y «Calculadora potencia v3». Todavía no hacen nada: salen si la página no tiene `#tl3-consumo` / `#tl3-potencia`. | — |
| 2 | Claude | Comprobar en la web que los dos fragmentos se cargan y no dan errores, y que las calculadoras actuales siguen funcionando. | — |
| 3 | Claude | Página 102 (potencia): copia del contenido actual en `copia-seguridad/`. Rehacer `pagina-potencia3.html` a partir de ese contenido, por si ha cambiado. Comprobar `modified`. Subir solo el contenido: la página sigue publicada. | Probar en la web a 1280, 820 y 390 px: interruptores, situaciones, ×2, «Encender uno a uno», cambio de potencia, otro aparato, CLS, desbordes y errores. |
| 4 | Claude | Página 156 (consumo): lo mismo con `pagina-consumo3.html`. | Probar en la web: hogares tipo, interruptores, ajustes y hora, tarifa, asistente, escenarios, tu factura, gráfica, CLS, desbordes y errores. Confirmar 58,78 €/mes en el ejemplo. |
| 5 | Titular | Desactivar (no borrar) los fragmentos antiguos 31 y 109. | Claude repite las comprobaciones de los pasos 3 y 4. |
| 6 | Claude | Actualizar `CLAUDE.md` (dónde viven las calculadoras) y hacer commit. | — |

Si la web no muestra el cambio, se vacía la caché de EasyWP y se vuelve a comprobar.

## Volver atrás
- **Falla en el paso 2** (antes de tocar páginas): el titular desactiva los fragmentos v3. Nada más.
- **Falla en el paso 3 o 4:**
  1. Claude vuelve a subir la copia de esa página. La calculadora antigua vuelve al momento, porque los fragmentos 31 y 109 siguen activos.
  2. Si fallan las dos, se restauran las dos.
  3. Después, el titular desactiva los fragmentos v3.
- **Falla después del paso 5:**
  1. El titular reactiva 31 y 109.
  2. Claude restaura las copias de las páginas 156 y 102.
  3. El titular desactiva los fragmentos v3.
- **Enlaces compartidos:** los guardados con la calculadora antigua (`#calc=…`) siguen abriendo en la v3.


## Activación (7-10-2026)
- **Paso 0 y 2:**
  - «Efectos» cerrado y fragmentos 309 y 310 cargados, idénticos a los `.min.js` y sin errores.
  - **Incidencia:** los fragmentos antiguos 31 y 109 no se cargaban en ninguna página, aunque figuraban como activos. Las dos calculadoras antiguas salían vacías.
  - El titular eligió seguir sin esperar (opción 2).
- **Página 102 (potencia):** copia en `rediseno/copia-seguridad/2026-10-07-calculadoras-v3/`, rehecha desde el contenido del día (era idéntico al preparado) y subida; sigue publicada. Probada en la web a 1280, 820 y 390 px:
  - Funciones: 25 interruptores, 7 potencias, marcar, ×2, cambio de potencia, situaciones, otro aparato, rearmar y «Encender uno a uno».
  - Cifras: 0,34 kW recomienda 2,3 kW (96,09 €/año).
  - Calidad: CLS 0, sin errores y sin desbordes.
- **Página 156 (consumo):** igual. Probada en la web a 1280, 820 y 390 px:
  - Ejemplo: 58,78 €/mes y pico de 5,27 kW.
  - Funciones: encender, ajustar y hora, tarifa por horas, asistente (3 aparatos, unos 84 €/año), escenarios, habitación, tu factura y hogares tipo.
  - Calidad: CLS 0,005 o menos, sin errores y sin desbordes.
- **Respaldo:** el código original de 31 y 109, tal como lo servía la web esa mañana, está en `respaldo-antiguas/`. El de 31 es idéntico a `calculadora.js`.
- **Volver atrás:**
  1. Activar los respaldos.
  2. Subir las copias de las páginas.
  3. Desactivar 309 y 310.
