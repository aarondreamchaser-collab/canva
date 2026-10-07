# Cálculos — página Metodología

- Precio de la energía: 0,13 €/kWh sin impuestos × 1,272 = **0,165 €/kWh con impuestos**.
- 2.0TD con impuestos: punta 0,242 · llano 0,153 · valle 0,102 €/kWh.
- Euros redondeados a 2 decimales (redondeo comercial).
- Factor de impuestos: 1,0511 × 1,21 = 1,271831, redondeado a 1,272. 0,13 × 1,272 = 0,16536 → 0,165 €/kWh.
- Potencia y alquiler del contador: valores de las calculadoras (POT_DIA 0,09 y CONTADOR 0,81 en consumo3.src.js y potencia3.src.js); el contador solo lleva IVA en la calculadora (CONTADOR × IVA).

## Ejemplo

| Paso | Cálculo | Resultado |
| --- | --- | --- |
| 1. Potencia de la etiqueta | 2.000 W = 2 kW | 2 kW |
| 2. Factor de uso real (termostato) | 2 kW × 0,6 | 1,2 kWh por hora |
| 3. Horas al día | 1,2 kWh × 5 h | 6,0 kWh al día |
| 4. Precio con impuestos | 6,0 kWh × 0,165 €/kWh | 0,99 € al día |
| 5. Mes de 30,4 días | 0,99 € × 30,4 | 30,10 € al mes |

## Precios

| Concepto | Valor que usamos | Con impuestos |
| --- | --- | --- |
| Energía, precio único | 0,13 €/kWh | 0,165 €/kWh |
| Energía en punta (10–14 h y 18–22 h, laborables) | 0,19 €/kWh | 0,242 €/kWh |
| Energía en llano (8–10 h, 14–18 h y 22–24 h, laborables) | 0,12 €/kWh | 0,153 €/kWh |
| Energía en valle (0–8 h y fines de semana) | 0,08 €/kWh | 0,102 €/kWh |
| Término de potencia (calculadoras) | 0,09 €/kW y día | 0,114 €/kW y día |
| Alquiler del contador (calculadora de consumo) | 0,81 € al mes | 0,98 € al mes (solo IVA) |
| Impuesto eléctrico e IVA | 5,11 % y 21 % | Factor 1,0511 × 1,21 = 1,2718 |

## Factores

| Aparato | Factor de uso real | Por qué |
| --- | --- | --- |
| Nevera y congelador | 0,2 (sobre 150 W) | El compresor arranca y para durante el día |
| Aire acondicionado | 0,6 | El compresor baja de potencia al llegar a la temperatura |
| Radiador de aceite y emisor térmico | 0,6 | El termostato corta y vuelve a conectar |
| Estufa eléctrica | 0,85 | Termostato más simple: está encendida más tiempo |
| Termo eléctrico | 0,7 | La resistencia solo funciona mientras recupera temperatura |
| Horno | 0,6 | Precalienta a tope y después mantiene |
| Inducción y vitrocerámica | 0,7 y 0,75 | Rara vez se usa a la potencia máxima |
| Secadora y lavavajillas | 0,8 y 0,55 | La resistencia no calienta todo el ciclo |
| Freidora de aire, deshumidificador y manta | 0,7 · 0,8 · 0,5 | Funcionan a ciclos |
| Resto de aparatos | 1 | Se toma la potencia de la etiqueta |
