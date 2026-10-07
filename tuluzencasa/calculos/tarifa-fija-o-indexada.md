# Cálculos — tarifa fija o indexada

- Precio de la energía: 0,13 €/kWh sin impuestos × 1,272 = **0,165 €/kWh con impuestos**.
- 2.0TD con impuestos: punta 0,242 · llano 0,153 · valle 0,102 €/kWh.
- Euros redondeados a 2 decimales (redondeo comercial).
- OMIE marginalpdbc, media simple de todos los periodos de cada mes (columna del sistema español). 734 ficheros diarios.
- Solo la parte de la energía que sigue al mercado: kWh × precio medio × 1,272 (impuesto eléctrico 5,11 % e IVA 21 %). No incluye peajes, cargos, servicios de ajuste, margen de la comercializadora ni término de potencia.
- Hogar de ejemplo: 250 kWh al mes. Mes más barato de los 12: Febrero 2026 (16,41 €/MWh); más caro: Septiembre 2026 (143,25 €/MWh).
- Días por mes en los ficheros: Octubre 2025 30, Noviembre 2025 29, Diciembre 2025 31, Enero 2026 31, Febrero 2026 28, Marzo 2026 31, Abril 2026 30, Mayo 2026 31, Junio 2026 30, Julio 2026 31, Agosto 2026 31, Septiembre 2026 30.
- Octubre de 2026 (días 1 a 6): 177,84 €/MWh.
- Media de los últimos 12 meses (oct. 2025–sep. 2026): 72,77 €/MWh.

## OMIE

| Mes | Precio medio del mercado diario | En €/kWh | Solo esa parte, para 250 kWh al mes, con impuestos |
| --- | --- | --- | --- |
| Octubre 2025 | 75,30 €/MWh | 0,075 €/kWh | 23,94 € |
| Noviembre 2025 | 57,71 €/MWh | 0,058 €/kWh | 18,35 € |
| Diciembre 2025 | 77,90 €/MWh | 0,078 €/kWh | 24,77 € |
| Enero 2026 | 71,67 €/MWh | 0,072 €/kWh | 22,79 € |
| Febrero 2026 | 16,41 €/MWh | 0,016 €/kWh | 5,22 € |
| Marzo 2026 | 41,77 €/MWh | 0,042 €/kWh | 13,28 € |
| Abril 2026 | 42,44 €/MWh | 0,042 €/kWh | 13,50 € |
| Mayo 2026 | 54,23 €/MWh | 0,054 €/kWh | 17,24 € |
| Junio 2026 | 69,59 €/MWh | 0,070 €/kWh | 22,13 € |
| Julio 2026 | 104,75 €/MWh | 0,105 €/kWh | 33,31 € |
| Agosto 2026 | 118,24 €/MWh | 0,118 €/kWh | 37,60 € |
| Septiembre 2026 | 143,25 €/MWh | 0,143 €/kWh | 45,55 € |
| Media de los 12 meses | 72,77 €/MWh | 0,073 €/kWh | 23,14 € |

## Riesgo

| Consumo al mes | Mes más barato (febrero 2026) | Mes más caro (septiembre 2026) | Diferencia en un mes |
| --- | --- | --- | --- |
| 150 kWh | 3,13 € | 27,33 € | 24,20 € |
| 250 kWh | 5,22 € | 45,55 € | 40,34 € |
| 400 kWh | 8,35 € | 72,89 € | 64,54 € |

## Sensibilidad

| Consumo al mes | Si el mercado sube 50 €/MWh: al mes | Si dura un año entero |
| --- | --- | --- |
| 150 kWh | 9,54 € | 114,48 € |
| 250 kWh | 15,90 € | 190,80 € |
| 400 kWh | 25,44 € | 305,28 € |

## Comparar

|  | Precio fijo (mercado libre) | Precio indexado (mercado libre) | PVPC (tarifa regulada) |
| --- | --- | --- | --- |
| Precio del kWh | El mismo durante el contrato | Sigue el mercado, hora a hora o cuarto a cuarto, más un margen | Fórmula oficial: 45 % mercado diario e intradiario y 55 % futuros |
| Quién pone el margen | La comercializadora, dentro del precio | La comercializadora, que debe explicar la fórmula | Lo fija la normativa |
| ¿Pueden subirte el precio? | No: no caben cláusulas de revisión | Sube y baja con el mercado | Sube y baja con el mercado |
| Penalización si te vas | Posible antes de la primera prórroga anual (máx. 5 % de la energía pendiente) | Ninguna (2.0TD) | Ninguna |
| Para quién | Quien quiere saber lo que pagará | Quien puede mover consumo a horas baratas y aguanta los meses caros | Quien quiere el precio regulado o el bono social |
