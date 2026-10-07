# Calculadoras v3 (propuesta, 7-10-2026)

**Estado: probadas en vista previa sobre la web publicada. No se ha aplicado nada.**

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

## Cómo aplicarlo sin que se rompa nada
| # | Quién | Paso |
|---|---|---|
| 0 | Titular | **Antes de nada:** añadir `</script>` al final de «Efectos tuluzencasa». Si no, se traga el siguiente fragmento del pie, que podría ser el de una calculadora. |
| 1 | Titular | WPCode › Añadir fragmento › JavaScript: «Calculadora consumo v3», pegar `consumo3.min.js`, pie de todo el sitio, activar. Igual con «Calculadora potencia v3» y `potencia3.min.js`. No hacen nada hasta el paso 2. |
| 2 | Claude | Subir `pagina-consumo3.html` a la página 156 y `pagina-potencia3.html` a la 102, con copia previa. Comprobar las dos en la web. |
| 3 | Titular | Desactivar los fragmentos antiguos 31 y 109: ya no encuentran su calculadora y no hacen nada. |

**Deshacer:** Claude vuelve a subir las copias de las páginas 156 y 102. Los fragmentos antiguos siguen guardados en WPCode.
