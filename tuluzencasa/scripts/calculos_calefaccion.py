"""Cálculos del bloque de calefacción (prioridad 2 de PLAN.md).

Mismos criterios que scripts/calculos.py (CLAUDE.md): 0,165 €/kWh con impuestos,
2.0TD con factor 1,272, mes de 30,4 días, invierno de 4 meses, factores de uso.
La bomba de calor se calcula con valores de SCOP de ejemplo (el lector debe usar
el de su etiqueta); no se usan precios de instalación inventados: la amortización
se da para varias inversiones posibles.

Genera calculos/<slug>.md y scripts/tablas_calefaccion.json.
"""
import json
from pathlib import Path
from calculos import (PRECIO, TRAMOS, FACTORES, DIAS_MES, eur, num, watts, cabecera)

BASE = Path(__file__).resolve().parent.parent
INVIERNO = 4 * DIAS_MES
tablas, md = {}, {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


# --------------------------------------------------------------- calefacción eléctrica más barata
# Escenario: una habitación que necesita 1 kW de calor durante 5 horas al día (5 kWh de calor).
CALOR_H, H_DIA = 1.0, 5
sistemas = [
    ("Resistencia (radiador, convector, calefactor, emisor) a precio fijo", 1.0, PRECIO),
    ("Resistencia con la tarifa por horas, todo en valle", 1.0, TRAMOS["valle"]),
    ("Resistencia con la tarifa por horas, todo en punta", 1.0, TRAMOS["punta"]),
    ("Bomba de calor con SCOP 3 (ejemplo), precio fijo", 3.0, PRECIO),
    ("Bomba de calor con SCOP 4 (ejemplo), precio fijo", 4.0, PRECIO),
]
rows = []
for nombre, cop, p in sistemas:
    kwh_e = CALOR_H / cop
    rows.append([nombre, eur(kwh_e * p), eur(kwh_e * H_DIA * p),
                 eur(kwh_e * H_DIA * DIAS_MES * p), eur(kwh_e * H_DIA * INVIERNO * p)])
t1 = tabla("cal_sistemas", ["Sistema", "Por hora (1 kWh de calor)", "Por día (5 h)", "Por mes", "Invierno (4 meses)"], rows)
md["calefaccion-electrica-mas-barata"] = cabecera(
    "calefacción eléctrica más barata",
    f"- Escenario: {num(CALOR_H, 0)} kW de calor durante {H_DIA} h/día = {num(CALOR_H * H_DIA, 0)} kWh de calor al día; mes {num(DIAS_MES, 1)} días; invierno 4 meses.\n"
    "- Una resistencia convierte 1 kWh de electricidad en 1 kWh de calor. Una bomba de calor da SCOP kWh de calor por kWh eléctrico.\n"
    "- SCOP 3 y 4 son valores de ejemplo: el lector debe usar el de la etiqueta de su equipo.\n"
) + "## Coste de calentar la misma habitación\n\n" + t1

# --------------------------------------------------------------- bomba de calor o radiadores
# Mismo calor que el radiador de 2.000 W del artículo publicado: 2 kW × 0,6 × 5 h = 6 kWh de calor al día.
f_rad = FACTORES["radiador"]
calor_dia = 2.0 * f_rad * H_DIA
rows = []
coste_rad_inv = calor_dia * INVIERNO * PRECIO
for nombre, cop in [("Radiador eléctrico de 2.000 W", 1.0), ("Bomba de calor, SCOP 3 (ejemplo)", 3.0),
                    ("Bomba de calor, SCOP 3,5 (ejemplo)", 3.5), ("Bomba de calor, SCOP 4 (ejemplo)", 4.0)]:
    e = calor_dia / cop
    rows.append([nombre, num(e), eur(e * PRECIO), eur(e * DIAS_MES * PRECIO), eur(e * INVIERNO * PRECIO)])
t1 = tabla("bdc_comparativa", ["Equipo", "kWh eléctricos al día", "Por día", "Por mes", "Invierno (4 meses)"], rows)
ahorro_35 = coste_rad_inv - calor_dia / 3.5 * INVIERNO * PRECIO
rows = []
for inv in [600, 900, 1200, 1500]:
    rows.append([eur(inv), eur(ahorro_35), num(inv / ahorro_35, 1) + " inviernos"])
t2 = tabla("bdc_amortizacion", ["Si la bomba de calor te cuesta", "Ahorro por invierno (SCOP 3,5)", "Se paga en"], rows)
rows = []
for nombre, p in [("Precio fijo", PRECIO), ("Valle", TRAMOS["valle"]), ("Llano", TRAMOS["llano"]), ("Punta", TRAMOS["punta"])]:
    rows.append([nombre, num(p, 3) + " €/kWh", eur(calor_dia * p), eur(calor_dia / 3.5 * p)])
t3 = tabla("bdc_tramos", ["Tramo", "Precio con impuestos", "Radiador, por día", "Bomba de calor SCOP 3,5, por día"], rows)
md["bomba-de-calor-o-radiadores-electricos"] = cabecera(
    "bomba de calor o radiadores eléctricos",
    f"- Calor necesario: el del radiador de 2.000 W del artículo publicado: 2 kW × {num(f_rad, 1)} × {H_DIA} h = {num(calor_dia, 1)} kWh de calor al día.\n"
    "- Bomba de calor: kWh eléctricos = kWh de calor ÷ SCOP. SCOP 3; 3,5 y 4 son valores de ejemplo.\n"
    "- Amortización: inversión ÷ ahorro por invierno, para varias inversiones posibles (no son precios reales).\n"
) + "## Mismo calor, distinto consumo\n\n" + t1 + "\n## Amortización\n\n" + t2 + "\n## Según el tramo horario\n\n" + t3

# --------------------------------------------------------------- radiador, convector o calefactor
rows = []
for w in [1000, 1500, 2000, 2500]:
    k = w / 1000
    rows.append([watts(w), eur(k * PRECIO), eur(k * H_DIA * PRECIO), eur(k * H_DIA * DIAS_MES * PRECIO)])
t1 = tabla("rcc_plena", ["Potencia", "Por hora a plena potencia", "Por día (5 h)", "Por mes (5 h/día)"], rows)
rows = []
for nombre, fa in [("Radiador de aceite", FACTORES["radiador"]), ("Calefactor o estufa", FACTORES["estufa"])]:
    k = 2.0 * fa
    rows.append([nombre + " de 2.000 W", num(fa, 2).rstrip("0").rstrip(","), eur(k * PRECIO), eur(k * H_DIA * DIAS_MES * PRECIO)])
t2 = tabla("rcc_factor", ["Aparato", "Factor de uso real", "Por hora", "Por mes (5 h/día)"], rows)
md["radiador-de-aceite-convector-o-calefactor"] = cabecera(
    "radiador de aceite, convector o calefactor",
    "- A igual potencia y tiempo con la resistencia encendida, los tres consumen lo mismo (1 kWh de electricidad = 1 kWh de calor).\n"
    f"- Factores de uso de CLAUDE.md: radiador de aceite {num(FACTORES['radiador'], 1)}, estufa/calefactor {num(FACTORES['estufa'], 2)}. El convector no tiene factor propio en CLAUDE.md: no se usa.\n"
) + "## A plena potencia\n\n" + t1 + "\n## Con el factor de uso real\n\n" + t2

# --------------------------------------------------------------- estufa eléctrica
f = FACTORES["estufa"]
H_EST = 3
rows = []
for w in [800, 1200, 1500, 2000, 2500]:
    k = w / 1000 * f
    rows.append([watts(w), num(k), eur(k * PRECIO), eur(k * H_EST * PRECIO), eur(k * H_EST * DIAS_MES * PRECIO), eur(k * H_EST * INVIERNO * PRECIO)])
t1 = tabla("estufa_potencias", ["Potencia", "kWh por hora (real)", "Por hora", "Por día (3 h)", "Por mes", "Invierno (4 meses)"], rows)
k = 2.0 * f
rows = []
for nombre, p in [("Punta", TRAMOS["punta"]), ("Llano", TRAMOS["llano"]), ("Valle", TRAMOS["valle"]), ("Precio fijo", PRECIO)]:
    rows.append([nombre, num(p, 3) + " €/kWh", eur(k * p), eur(k * H_EST * p), eur(k * H_EST * DIAS_MES * p)])
t2 = tabla("estufa_tramos", ["Tramo", "Precio con impuestos", "Por hora", "Por día (3 h)", "Por mes"], rows)
rows = []
for h in [1, 2, 3, 5]:
    rows.append([f"{h} h", num(k * h), eur(k * h * PRECIO), eur(k * h * DIAS_MES * PRECIO)])
t3 = tabla("estufa_horas", ["Horas al día", "kWh al día", "Por día", "Por mes"], rows)
md["cuanto-consume-una-estufa-electrica"] = cabecera(
    "estufa eléctrica",
    f"- Factor de uso real: {num(f, 2)} (estufa en CLAUDE.md). Uso tipo {H_EST} h/día (como la calculadora), mes {num(DIAS_MES, 1)} días, invierno 4 meses.\n"
) + "## Coste por potencia\n\n" + t1 + "\n## Estufa de 2.000 W según el tramo (3 h/día)\n\n" + t2 + "\n## Estufa de 2.000 W según las horas\n\n" + t3

for slug, text in md.items():
    (BASE / "calculos" / f"{slug}.md").write_text(text, encoding="utf-8")
(BASE / "scripts" / "tablas_calefaccion.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n\n".join(md.values()))
