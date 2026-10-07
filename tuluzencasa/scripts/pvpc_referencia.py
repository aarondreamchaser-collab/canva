"""Compara el precio de referencia de la web (0,165 €/kWh) con el precio final medio oficial del PVPC.

Fuente oficial: CNMC, Boletín de indicadores eléctricos IS/DE/012/26 (20/7/2026), fuentes/pvpc/:
- p. 65: facturación estimada del consumidor medio acogido al PVPC, últimos 12 meses (abr. 2025 – mar. 2026),
  sin impuestos ni alquiler del contador: peaje de acceso 8,53 + margen 1,03 + energía 11,00 = 20,56 c€/kWh.
  Incluye el término de potencia (va dentro del peaje y del margen), repartido por kWh consumido.
- p. 4.1 (marzo 2026): consumidor medio de las comercializadoras de referencia (COR): 2.104 kWh/año y 3,79 kW.
OMIE: medias mensuales simples (fuentes/tanda8/omie) para estimar el efecto de los meses posteriores a marzo de 2026.
"""
from pathlib import Path
from calculos import DIAS_MES, num

BASE = Path(__file__).resolve().parent.parent
IMP = 1.0511 * 1.21                     # impuesto eléctrico 5,11 % e IVA 21 %
CNMC = {"peaje": 8.53, "margen": 1.03, "energia": 11.00}
FINAL_SI = sum(CNMC.values()) / 100    # €/kWh sin impuestos, todo incluido
KWH, KW = 2104, 3.79                    # consumidor medio COR
POT_DIA, ENE = 0.09, 0.13               # valores de la web
ANO = 12 * DIAS_MES

# 1. La web aplicada al consumidor medio del PVPC
web_si = (KW * POT_DIA * ANO + KWH * ENE) / KWH
# 2. Precio de la energía que haría falta en la web para igualar el dato oficial (misma potencia)
ene_eq = FINAL_SI - KW * POT_DIA * ANO / KWH

# 3. OMIE: abr. 2025 – mar. 2026 frente a oct. 2025 – sep. 2026
precios = {}
for f in sorted((BASE / "fuentes" / "tanda8" / "omie").glob("marginalpdbc_*.1")):
    for line in f.read_text(encoding="latin-1").splitlines():
        c = line.split(";")
        if len(c) >= 6 and c[0].isdigit():
            precios.setdefault((int(c[0]), int(c[1])), []).append(float(c[5]))
media = {k: sum(v) / len(v) for k, v in precios.items()}
def periodo(ini):
    y, m = ini; out = []
    for _ in range(12):
        out.append((y, m)); m += 1
        if m == 13: y, m = y + 1, 1
    return sum(media[k] for k in out) / 12
om_cnmc, om_ult = periodo((2025, 4)), periodo((2025, 10))
delta = (om_ult - om_cnmc) / 1000      # €/kWh
est_lo, est_hi = ene_eq + 0.45 * delta, ene_eq + delta   # 45 % mercado diario (RD 216/2014) … todo

out = f"""# Precio de referencia de la web frente al PVPC real

Cálculo del {Path(__file__).name}. Precios en €/kWh.

| Concepto | Sin impuestos | Con impuestos (× {num(IMP, 4)}) |
| --- | --- | --- |
| PVPC real, consumidor medio, abr. 2025 – mar. 2026 (CNMC), todo incluido | {num(FINAL_SI, 4)} | {num(FINAL_SI * IMP, 4)} |
| La web aplicada a ese consumidor ({num(KWH, 0)} kWh/año, {num(KW, 2)} kW), todo incluido | {num(web_si, 4)} | {num(web_si * IMP, 4)} |
| Diferencia | {num((web_si / FINAL_SI - 1) * 100, 1)} % | |
| Precio de la energía de la web (solo energía) | {num(ENE, 4)} | {num(ENE * 1.272, 3)} |
| Precio de la energía que igualaría el dato de la CNMC | {num(ene_eq, 4)} | {num(ene_eq * 1.272, 3)} |
| Estimación para oct. 2025 – sep. 2026 (OMIE +{num(delta * 1000, 2)} €/MWh) | {num(est_lo, 4)} – {num(est_hi, 4)} | {num(est_lo * 1.272, 3)} – {num(est_hi * 1.272, 3)} |

- OMIE, media simple: abr. 2025 – mar. 2026 = {num(om_cnmc, 2)} €/MWh; oct. 2025 – sep. 2026 = {num(om_ult, 2)} €/MWh.
- La estimación supone que la subida del mercado diario pasa al PVPC entre un 45 % (su peso en la fórmula de 2026) y un 100 %. No es un dato oficial.
- Componentes CNMC (c€/kWh): peaje de acceso {num(CNMC['peaje'])}, margen {num(CNMC['margen'])}, energía {num(CNMC['energia'])}.
"""
(BASE / "estrategia" / "pvpc-vs-referencia-2026-10.md").write_text(out, encoding="utf-8")
print(out)
