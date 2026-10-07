# Propuesta de nuevos precios de referencia

Generada por `scripts/precio_nuevo.py` (impuesto eléctrico 5,11 %, IVA 21 %). No aplicada.

| Concepto | Ahora | Propuesta |
| --- | --- | --- |
| Energía, sin impuestos | 0,130 €/kWh | 0,146 €/kWh |
| Energía, con impuestos | 0,165 €/kWh | 0,186 €/kWh |
| Punta / llano / valle, sin impuestos | 0,190 / 0,120 / 0,080 | 0,206 / 0,136 / 0,096 |
| Término de potencia, sin impuestos | 0,090 €/kW y día | 0,090 €/kW y día (oficial 2026: 0,0864) |
| Factor de impuestos | 1,272 | 1,272 |

- **Potencia 2026**: peajes 23,768722 + cargos 4,661114 + comercialización 3,113 = 31,542836 €/kW y año → 0,08642 €/kW y día.
- **Energía**: precio final del PVPC de la CNMC (0,2056 €/kWh, todo incluido) menos la potencia del consumidor medio (3,79 kW, 2104 kWh/año).
- **Tramos**: se mantiene la diferencia actual entre punta, llano y valle y se suben en la misma cantidad que el precio único (0,016 €/kWh).
  Peajes y cargos de energía 2026 por tramo, para comparar: punta 0,097553, llano 0,029267, valle 0,003292 €/kWh.
- **Alquiler del contador**: sin cambio (0,81 € al mes).
