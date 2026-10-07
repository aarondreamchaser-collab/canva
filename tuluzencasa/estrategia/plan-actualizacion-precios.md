# Plan: actualizar el precio de referencia (una sola vez, con el dato del INE)

Preparado el 7-10-2026. **No se ha cambiado nada en la web.** Se ejecuta cuando el titular dé el aviso, tras el IPC definitivo de septiembre (INE, 14-15 de octubre).

## 1. Valores propuestos

Generados con `python3 scripts/precio_nuevo.py` → `scripts/precios_referencia_propuesta.json` y `estrategia/precio-nuevo-propuesta.md`.

| Concepto | Ahora | Propuesta | De dónde sale |
| --- | --- | --- | --- |
| Energía, sin impuestos | 0,13 €/kWh | 0,146 €/kWh | Precio final medio del PVPC (CNMC, abr. 2025 – mar. 2026: 20,56 c€/kWh con todo, sin impuestos) menos la potencia del consumidor medio (3,79 kW, 2.104 kWh/año) |
| Energía, con impuestos | 0,165 €/kWh | **0,186 €/kWh** | × 1,272 (impuesto eléctrico 5,11 % e IVA 21 %) |
| Punta / llano / valle, sin impuestos | 0,19 / 0,12 / 0,08 | 0,206 / 0,136 / 0,096 | Misma subida que el precio único (+0,016), así se mantiene el punto de equilibrio de los tramos |
| Término de potencia, sin impuestos | 0,09 €/kW y día | 0,09 €/kW y día (sin cambio) | 2026: peajes 23,768722 + cargos 4,661114 + comercialización 3,113 = 31,54 €/kW y año = 0,0864 €/kW y día; con dos decimales, 0,09 |
| Alquiler del contador | 0,81 € al mes | sin cambio | — |

Fuentes: CNMC, Boletín de indicadores eléctricos IS/DE/012/26 (20-7-2026), págs. 63-66 y 4.1 (`fuentes/pvpc/`); Resolución de la CNMC de 18-12-2025, peajes 2026 (BOE-A-2025-26348); Orden TED/1524/2025, cargos 2026 (BOE-A-2025-26705); Orden ETU/1948/2016, término fijo de comercialización (BOE-A-2016-12274) (`fuentes/precios2026/`).

Notas:
- Si la CNMC publica antes del cambio un boletín con datos más recientes, se actualiza `FINAL_SI` en `precio_nuevo.py` y se repite.
- El término de comercialización de 3,113 €/kW y año es el último valor que figura en la Orden ETU/1948/2016 (para 2016-2018); no he encontrado una orden posterior que lo cambie.
- Con la potencia oficial de 2026 sin redondear (0,086), la energía equivalente saldría a 0,149 → 0,190 €/kWh. Proponemos mantener 0,09 por simplicidad y coherencia con las calculadoras.

## 2. Impuestos: dos escenarios

- **Si el IPC eléctrico de septiembre NO activa la rebaja**: se aplica la tabla de arriba tal cual.
- **Si la activa (IVA 10 % e impuesto eléctrico 0,5 %, temporal)**: propuesta: seguir calculando con los impuestos generales (21 % y 5,11 %), porque la rebaja dura poco, y añadir una caja «Actualizado» en los artículos de factura con el periodo y la norma. Si el titular prefiere calcular con los rebajados: `python3 scripts/precio_nuevo.py --iee 0.005 --iva 0.10` y se repite todo (el factor pasaría a 1,106).

## 3. Pasos del día del cambio

| Paso | Quién | Qué |
| --- | --- | --- |
| 1 | Claude | Comprobar el dato del INE y la norma; fijar los impuestos con el titular |
| 2 | Claude | `python3 scripts/precio_nuevo.py [--iee … --iva …] --mes "octubre de 2026"` |
| 3 | Claude | `python3 scripts/actualizar_precios.py` (simulación) y revisar `revision-precios/resumen.md`: 0 dudas, los importes elegidos «por proporción» y los porcentajes |
| 4 | Titular | Dar el OK a la simulación |
| 5 | Claude | `python3 scripts/actualizar_precios.py --aplicar`: copia de cada documento en `rediseno/copia-seguridad/precios-<mes>/`, comprueba «modified», sube contenido, extracto y descripción de Rank Math |
| 6 | Claude | Retocar a mano lo que el script avisa (hoy: «27 %» → «25 %» de peso de la potencia en «Cómo leer la factura», también en su extracto) |
| 7 | Claude | `python3 scripts/wpcode_precios.py` → `revision-precios/wpcode/` |
| 8 | Titular | Pegar en WPCode: `consumo3.min.js` (fragmento 309), `potencia3.min.js` (310, hoy sin cambios) y la plantilla (frase del pie «Precio de referencia») |
| 9 | Claude | Comprobar la web publicada: muestra de artículos, portada, Metodología, las dos calculadoras y el pie |
| 10 | Claude | Actualizar CLAUDE.md (criterios de precios), `calculadora.js`, `src/` y commit |

**Volver atrás**: las copias de cada documento quedan en `rediseno/copia-seguridad/precios-<mes>/` (subirlas igual que se suben los cambios) y `scripts/precios_referencia.json` está en git.

## 4. Lo que cambia (simulación del 7-10-2026)

38 documentos: 36 entradas, la portada y la página Metodología. 0 dudas sin resolver tras dos decisiones (`revision-precios/decisiones.json`: 5,84 € y 41,78 € no cambian). 14 importes redondos se eligen «por proporción» entre dos valores posibles y están listados en el resumen para revisarlos. El resumen se regenera en cada simulación.

## 5. Cómo funcionan los scripts

- `scripts/precios_referencia.json`: única fuente de los precios. La leen `calculos.py`, `calculos/factura/comun.py` y los scripts de cada tanda. Con los valores actuales, todos los cálculos salen idénticos a los publicados (comprobado).
- `scripts/actualizar_precios.py` trabaja sobre el contenido **publicado** (en 23 entradas hay retoques hechos en vivo que no están en `src/`): sustituye las tablas enteras, cambia los importes del texto con la correspondencia antiguo → nuevo de los cálculos y avisa de lo que no puede decidir.
- `scripts/wpcode_precios.py` prepara los fragmentos de WPCode para pegar.
