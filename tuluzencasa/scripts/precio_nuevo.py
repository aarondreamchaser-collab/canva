"""Propone los nuevos precios de referencia a partir de fuentes oficiales. No cambia nada en la web.

Uso: python3 scripts/precio_nuevo.py [--iee 0.0511] [--iva 0.21] [--mes "octubre de 2026"]
Escribe scripts/precios_referencia_propuesta.json y estrategia/precio-nuevo-propuesta.md.

Fuentes (fuentes/pvpc y fuentes/precios2026):
- CNMC, Boletín de indicadores eléctricos IS/DE/012/26: PVPC del consumidor medio, abr. 2025 – mar. 2026,
  20,56 c€/kWh sin impuestos (peaje de acceso 8,53 + margen 1,03 + energía 11,00); consumidor medio COR 2.104 kWh/año y 3,79 kW.
- Peajes 2026: Resolución de la CNMC de 18/12/2025 (BOE-A-2025-26348), 2.0TD.
- Cargos 2026: Orden TED/1524/2025 (BOE-A-2025-26705), segmento 1.
- Término fijo de comercialización del PVPC: Orden ETU/1948/2016 (BOE-A-2016-12274), 3,113 €/kW y año.
"""
import argparse, json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("--iee", type=float, default=0.0511)
ap.add_argument("--iva", type=float, default=0.21)
ap.add_argument("--mes", default="octubre de 2026")
a = ap.parse_args()

PEAJES = {"pot": (23.324952, 0.443770), "ene": (0.033261, 0.016409, 0.000077)}
CARGOS = {"pot": (4.379461, 0.281653), "ene": (0.064292, 0.012858, 0.003215)}
CCF = 3.113
FINAL_SI, KWH, KW = 0.2056, 2104, 3.79
actual = json.loads((BASE / "scripts" / "precios_referencia.json").read_text())

pot_ano = sum(PEAJES["pot"]) + sum(CARGOS["pot"]) + CCF          # €/kW y año (misma potencia en P1 y P2)
pot_dia = round(pot_ano / 365, 2)                                 # 2 decimales, como en las calculadoras
energia = round(FINAL_SI - KW * pot_dia * 365 / KWH, 3)           # €/kWh sin impuestos que iguala el dato de la CNMC
delta = energia - actual["energia"]
tramos = {k: round(v + delta, 3) for k, v in actual["tramos"].items()}  # se mantiene la diferencia entre tramos
fac = round((1 + a.iee) * (1 + a.iva), 3)
nuevo = dict(actual, mes_precios=a.mes, energia=energia, tramos=tramos, pot_dia=pot_dia,
             impuesto_electrico=a.iee, iva=a.iva, factor_redondeado=fac, precio_con_impuestos=round(energia * fac, 3))
nuevo["_nota"] = actual["_nota"]
(BASE / "scripts" / "precios_referencia_propuesta.json").write_text(json.dumps(nuevo, ensure_ascii=False, indent=1))

pc = [PEAJES["ene"][i] + CARGOS["ene"][i] for i in range(3)]
f = lambda x, d=3: f"{x:.{d}f}".replace(".", ",")
md = f"""# Propuesta de nuevos precios de referencia

Generada por `scripts/precio_nuevo.py` (impuesto eléctrico {f(a.iee * 100, 2)} %, IVA {f(a.iva * 100, 0)} %). No aplicada.

| Concepto | Ahora | Propuesta |
| --- | --- | --- |
| Energía, sin impuestos | {f(actual['energia'])} €/kWh | {f(energia)} €/kWh |
| Energía, con impuestos | {f(actual['precio_con_impuestos'])} €/kWh | {f(nuevo['precio_con_impuestos'])} €/kWh |
| Punta / llano / valle, sin impuestos | {' / '.join(f(v) for v in actual['tramos'].values())} | {' / '.join(f(v) for v in tramos.values())} |
| Término de potencia, sin impuestos | {f(actual['pot_dia'])} €/kW y día | {f(pot_dia)} €/kW y día (oficial 2026: {f(pot_ano / 365, 4)}) |
| Factor de impuestos | {f(actual['factor_redondeado'])} | {f(fac)} |

- **Potencia 2026**: peajes {f(sum(PEAJES['pot']), 6)} + cargos {f(sum(CARGOS['pot']), 6)} + comercialización {f(CCF)} = {f(pot_ano, 6)} €/kW y año → {f(pot_ano / 365, 5)} €/kW y día.
- **Energía**: precio final del PVPC de la CNMC ({f(FINAL_SI, 4)} €/kWh, todo incluido) menos la potencia del consumidor medio ({f(KW, 2)} kW, {KWH} kWh/año).
- **Tramos**: se mantiene la diferencia actual entre punta, llano y valle y se suben en la misma cantidad que el precio único ({f(delta)} €/kWh).
  Peajes y cargos de energía 2026 por tramo, para comparar: punta {f(pc[0], 6)}, llano {f(pc[1], 6)}, valle {f(pc[2], 6)} €/kWh.
- **Alquiler del contador**: sin cambio ({f(actual['contador_mes'], 2)} € al mes).
"""
(BASE / "estrategia" / "precio-nuevo-propuesta.md").write_text(md, encoding="utf-8")
print(md)
