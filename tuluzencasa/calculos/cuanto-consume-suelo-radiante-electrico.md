# Cálculos — suelo radiante eléctrico

- Precio de la energía: 0,13 €/kWh sin impuestos × 1,272 = **0,165 €/kWh con impuestos**.
- 2.0TD con impuestos: punta 0,242 · llano 0,153 · valle 0,102 €/kWh.
- Euros redondeados a 2 decimales (redondeo comercial).
- Factor de uso 0,6 (termostato; el de emisor térmico en CLAUDE.md). 5 h al día como en los emisores. Invierno de 4 meses.
- Potencias por m²: Salvador Escoda (mantas de 60 W/m² para casas nuevas bien aisladas, 120 W/m² y 180 W/m² para baños); Danfoss DEVI (máx. 200 W/m² en hormigón con baldosa, 150 W/m² sobre capa aislante, 100 W/m² bajo madera, 80 W/m² entre viguetas de madera).
- Casa de ejemplo: superficies, potencias y horas orientativas, no son un dimensionado.
- Bomba de calor: mismo calor ÷ SCOP 3,5 (valor de ejemplo, igual que en el artículo de emisores).

## Potencias

| Potencia por m² | Potencia en 20 m² | Por hora | Por día (5 h) | Por mes | Invierno (4 meses) |
| --- | --- | --- | --- | --- | --- |
| 60 W/m² | 1.200 W | 0,12 € | 0,59 € | 18,06 € | 72,23 € |
| 100 W/m² | 2.000 W | 0,20 € | 0,99 € | 30,10 € | 120,38 € |
| 150 W/m² | 3.000 W | 0,30 € | 1,49 € | 45,14 € | 180,58 € |

## Casa

| Estancia | Potencia instalada | Horas al día | kWh al día (real) | Por día | Por mes | Invierno (4 meses) |
| --- | --- | --- | --- | --- | --- | --- |
| Salón | 20 m² × 100 W/m² = 2.000 W | 5 h | 6,00 kWh | 0,99 € | 30,10 € | 120,38 € |
| Dormitorio principal | 12 m² × 100 W/m² = 1.200 W | 3 h | 2,16 kWh | 0,36 € | 10,83 € | 43,34 € |
| Segundo dormitorio | 10 m² × 100 W/m² = 1.000 W | 2 h | 1,20 kWh | 0,20 € | 6,02 € | 24,08 € |
| Baño | 5 m² × 150 W/m² = 750 W | 2 h | 0,90 kWh | 0,15 € | 4,51 € | 18,06 € |
| Total | 4.950 W |  | 10,26 kWh | 1,69 € | 51,46 € | 205,86 € |

## Tramos

| Si el salón (2.000 W, 5 h) calienta… | Precio con impuestos | Coste al mes |
| --- | --- | --- |
| Precio único de referencia | 0,165 €/kWh | 30,10 € |
| Todo en punta | 0,242 €/kWh | 44,08 € |
| Todo en llano | 0,153 €/kWh | 27,84 € |
| Todo en valle | 0,102 €/kWh | 18,56 € |

## Comparar

| Mismo calor para el salón | Electricidad al día | Coste al mes | Invierno (4 meses) |
| --- | --- | --- | --- |
| Suelo radiante eléctrico | 6,00 kWh | 30,10 € | 120,38 € |
| Emisor térmico o radiador eléctrico | 6,00 kWh | 30,10 € | 120,38 € |
| Bomba de calor (SCOP 3,5, ejemplo) | 1,71 kWh | 8,60 € | 34,40 € |
