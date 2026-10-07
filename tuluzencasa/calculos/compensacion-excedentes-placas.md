# Cálculos — compensación de excedentes

- Precio de la energía: 0,13 €/kWh sin impuestos × 1,272 = **0,165 €/kWh con impuestos**.
- 2.0TD con impuestos: punta 0,242 · llano 0,153 · valle 0,102 €/kWh.
- Euros redondeados a 2 decimales (redondeo comercial).
- PVGIS 5.2, Madrid, 1 kWp a 30° sur, 14 % de pérdidas (fuentes/pvgis_madrid.json), × 3 kWp; casa de 3.000 kWh/año, 40 % de la producción al momento (como «Placas solares en casa»).
- Compensación mensual = mín(excedentes × precio, energía de la red × 0,13 €/kWh) (RD 244/2019, art. 14.3); se descuenta antes de impuestos, × 1,272.
- «No compensado»: valor de los excedentes por encima del tope, con impuestos; es lo que un saldo acumulable podría guardar.
- OMIE, mercado diario, oct. 2025 – sep. 2026: media de 11 a 16 h 23,99 €/MWh; media de todas las horas 73,22 €/MWh.

## Meses

| Mes (Madrid, 3 kWp) | Producción | Excedentes | Compensación en la factura | Excedentes que no se compensan |
| --- | --- | --- | --- | --- |
| Enero | 304 kWh | 182 kWh | 13,90 € | 0,00 € |
| Febrero | 330 kWh | 198 kWh | 15,13 € | 0,00 € |
| Marzo | 417 kWh | 250 kWh | 13,76 € | 5,33 € |
| Abril | 432 kWh | 259 kWh | 12,74 € | 7,06 € |
| Mayo | 472 kWh | 283 kWh | 10,13 € | 11,47 € |
| Junio | 483 kWh | 290 kWh | 9,42 € | 12,68 € |
| Julio | 521 kWh | 313 kWh | 6,87 € | 16,99 € |
| Agosto | 503 kWh | 302 kWh | 8,08 € | 14,95 € |
| Septiembre | 442 kWh | 265 kWh | 12,09 € | 8,16 € |
| Octubre | 375 kWh | 225 kWh | 16,56 € | 0,60 € |
| Noviembre | 292 kWh | 175 kWh | 13,35 € | 0,00 € |
| Diciembre | 295 kWh | 177 kWh | 13,49 € | 0,00 € |
| Año | 4.865 kWh | 2.919 kWh | 145,53 € | 77,24 € |

## Precio

| Precio de los excedentes (sin impuestos) | Compensación al año | Lo que se queda sin compensar al año |
| --- | --- | --- |
| 0,04 €/kWh | 120,74 € | 27,77 € |
| 0,06 €/kWh | 145,53 € | 77,24 € |
| 0,08 €/kWh | 163,46 € | 133,55 € |
