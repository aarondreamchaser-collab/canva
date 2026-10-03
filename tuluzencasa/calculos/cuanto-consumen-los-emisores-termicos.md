# Cálculos — emisores térmicos

- Precio de la energía: 0,13 €/kWh sin impuestos × 1,272 = **0,165 €/kWh con impuestos**.
- 2.0TD con impuestos: punta 0,242 · llano 0,153 · valle 0,102 €/kWh.
- Euros redondeados a 2 decimales (redondeo comercial).
- Factor de uso real: 0,6 (emisor térmico en CLAUDE.md). Uso tipo 5 h/día (como el radiador de aceite), mes 30,4 días, invierno 4 meses.
- Casa de ejemplo: potencias y horas orientativas, no son una recomendación de dimensionado. Potencia total 4.000 W.
- Bomba de calor: mismo calor que el emisor de 1.000 W (3,0 kWh de calor al día) ÷ SCOP 3,5 (valor de ejemplo).

## Coste por potencia

| Potencia | kWh por hora (real) | Por hora | Por día (5 h) | Por mes | Invierno (4 meses) |
| --- | --- | --- | --- | --- | --- |
| 500 W | 0,30 | 0,05 € | 0,25 € | 7,52 € | 30,10 € |
| 750 W | 0,45 | 0,07 € | 0,37 € | 11,29 € | 45,14 € |
| 1.000 W | 0,60 | 0,10 € | 0,50 € | 15,05 € | 60,19 € |
| 1.500 W | 0,90 | 0,15 € | 0,74 € | 22,57 € | 90,29 € |
| 2.000 W | 1,20 | 0,20 € | 0,99 € | 30,10 € | 120,38 € |

## Casa de ejemplo

| Estancia | Emisor | Horas al día | kWh al día (real) | Por día | Por mes | Invierno (4 meses) |
| --- | --- | --- | --- | --- | --- | --- |
| Salón | 1.500 W | 5 h | 4,50 | 0,74 € | 22,57 € | 90,29 € |
| Dormitorio principal | 1.000 W | 2 h | 1,20 | 0,20 € | 6,02 € | 24,08 € |
| Segundo dormitorio | 1.000 W | 2 h | 1,20 | 0,20 € | 6,02 € | 24,08 € |
| Baño | 500 W | 1 h | 0,30 | 0,05 € | 1,50 € | 6,02 € |
| Total | 4.000 W |  | 7,20 | 1,19 € | 36,12 € | 144,46 € |

## Emisor de 1.000 W según el tramo

| Tramo | Precio con impuestos | Por día (5 h) | Por mes | Invierno (4 meses) |
| --- | --- | --- | --- | --- |
| Precio fijo | 0,165 €/kWh | 0,50 € | 15,05 € | 60,19 € |
| Valle | 0,102 €/kWh | 0,31 € | 9,28 € | 37,12 € |
| Llano | 0,153 €/kWh | 0,46 € | 13,92 € | 55,68 € |
| Punta | 0,242 €/kWh | 0,73 € | 22,04 € | 88,16 € |

## Frente a la bomba de calor

| Equipo (mismo calor) | kWh eléctricos al día | Por día | Por mes | Invierno (4 meses) |
| --- | --- | --- | --- | --- |
| Emisor térmico de 1.000 W | 3,00 | 0,50 € | 15,05 € | 60,19 € |
| Bomba de calor, SCOP 3,5 (ejemplo) | 0,86 | 0,14 € | 4,30 € | 17,20 € |
