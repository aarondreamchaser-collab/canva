"""Cálculos del segundo lote de climatización: emisores térmicos, manta eléctrica y deshumidificador.

Mismos criterios que scripts/calculos.py (CLAUDE.md): 0,165 €/kWh con impuestos,
2.0TD con factor 1,272, mes de 30,4 días, invierno de 4 meses, año de 12 meses.
Factores de uso: emisor térmico 0,6 · manta eléctrica 0,5 · deshumidificador 0,8.
Usos tipo de la calculadora de la home: manta 100 W, 8 h, de madrugada;
deshumidificador 250 W, 8 h, todo el día. El emisor no está en la calculadora:
se usan 5 h/día, como el radiador de aceite.

Genera calculos/<slug>.md y scripts/tablas_calefaccion2.json.
"""
import json
from pathlib import Path
from calculos import (PRECIO, TRAMOS, FACTORES, DIAS_MES, eur, num, watts, cabecera)

BASE = Path(__file__).resolve().parent.parent
INVIERNO = 4 * DIAS_MES
ANO = 12 * DIAS_MES
tablas, md = {}, {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def horas(h):
    return (num(h, 1).rstrip("0").rstrip(",") if h % 1 else str(int(h))) + " h"


# Precio medio de «todo el día» en la calculadora: entre semana 1/3 punta, 1/3 llano, 1/3 valle;
# fin de semana todo valle.
WD, WE = 5 / 7, 2 / 7
PRECIO_TODO_DIA = WD * (TRAMOS["punta"] + TRAMOS["llano"] + TRAMOS["valle"]) / 3 + WE * TRAMOS["valle"]

# --------------------------------------------------------------- emisores térmicos
f = FACTORES["emisor"]
H_EM = 5
rows = []
for w in [500, 750, 1000, 1500, 2000]:
    k = w / 1000 * f
    rows.append([watts(w), num(k), eur(k * PRECIO), eur(k * H_EM * PRECIO),
                 eur(k * H_EM * DIAS_MES * PRECIO), eur(k * H_EM * INVIERNO * PRECIO)])
t1 = tabla("emisor_potencias", ["Potencia", "kWh por hora (real)", "Por hora", "Por día (5 h)", "Por mes", "Invierno (4 meses)"], rows)

casa = [("Salón", 1500, 5), ("Dormitorio principal", 1000, 2), ("Segundo dormitorio", 1000, 2), ("Baño", 500, 1)]
rows, tot_w, tot_k = [], 0, 0
for nombre, w, h in casa:
    k = w / 1000 * f * h
    tot_w += w; tot_k += k
    rows.append([nombre, watts(w), horas(h), num(k), eur(k * PRECIO), eur(k * DIAS_MES * PRECIO), eur(k * INVIERNO * PRECIO)])
rows.append(["Total", watts(tot_w), "", num(tot_k), eur(tot_k * PRECIO), eur(tot_k * DIAS_MES * PRECIO), eur(tot_k * INVIERNO * PRECIO)])
t2 = tabla("emisor_casa", ["Estancia", "Emisor", "Horas al día", "kWh al día (real)", "Por día", "Por mes", "Invierno (4 meses)"], rows)

k = 1.0 * f * H_EM
rows = []
for nombre, p in [("Precio fijo", PRECIO), ("Valle", TRAMOS["valle"]), ("Llano", TRAMOS["llano"]), ("Punta", TRAMOS["punta"])]:
    rows.append([nombre, num(p, 3) + " €/kWh", eur(k * p), eur(k * DIAS_MES * p), eur(k * INVIERNO * p)])
t3 = tabla("emisor_tramos", ["Tramo", "Precio con impuestos", "Por día (5 h)", "Por mes", "Invierno (4 meses)"], rows)

rows = []
for nombre, cop in [("Emisor térmico de 1.000 W", 1.0), ("Bomba de calor, SCOP 3,5 (ejemplo)", 3.5)]:
    e = k / cop
    rows.append([nombre, num(e), eur(e * PRECIO), eur(e * DIAS_MES * PRECIO), eur(e * INVIERNO * PRECIO)])
t4 = tabla("emisor_bdc", ["Equipo (mismo calor)", "kWh eléctricos al día", "Por día", "Por mes", "Invierno (4 meses)"], rows)
md["cuanto-consumen-los-emisores-termicos"] = cabecera(
    "emisores térmicos",
    f"- Factor de uso real: {num(f, 1)} (emisor térmico en CLAUDE.md). Uso tipo {H_EM} h/día (como el radiador de aceite), mes {num(DIAS_MES, 1)} días, invierno 4 meses.\n"
    f"- Casa de ejemplo: potencias y horas orientativas, no son una recomendación de dimensionado. Potencia total {watts(tot_w)}.\n"
    f"- Bomba de calor: mismo calor que el emisor de 1.000 W ({num(k, 1)} kWh de calor al día) ÷ SCOP 3,5 (valor de ejemplo).\n"
) + ("## Coste por potencia\n\n" + t1 + "\n## Casa de ejemplo\n\n" + t2 +
     "\n## Emisor de 1.000 W según el tramo\n\n" + t3 + "\n## Frente a la bomba de calor\n\n" + t4)

# --------------------------------------------------------------- manta eléctrica
f = FACTORES["manta"]
H_MANTA = 8
rows = []
for w in [60, 100, 150]:
    k = w / 1000 * f
    rows.append([watts(w), num(k, 3), eur(k * PRECIO), eur(k * H_MANTA * PRECIO),
                 eur(k * H_MANTA * DIAS_MES * PRECIO), eur(k * H_MANTA * INVIERNO * PRECIO)])
t1 = tabla("manta_potencias", ["Potencia", "kWh por hora (real)", "Por hora", "Por noche (8 h)", "Por mes", "Invierno (4 meses)"], rows)

rows = []
for h in [0.5, 1, 2, 8]:
    k = 0.1 * f * h
    rows.append([horas(h), num(k, 3), eur(k * PRECIO), eur(k * DIAS_MES * PRECIO), eur(k * INVIERNO * PRECIO)])
t2 = tabla("manta_horas", ["Uso cada noche", "kWh por noche", "Por noche", "Por mes", "Invierno (4 meses)"], rows)

comp = [
    ("Manta de 100 W, 8 h, precio fijo", 0.1 * f * 8, PRECIO),
    ("Manta de 100 W, 8 h, en valle", 0.1 * f * 8, TRAMOS["valle"]),
    ("Radiador de aceite de 2.000 W, 2 h antes de dormir", 2.0 * FACTORES["radiador"] * 2, PRECIO),
    ("Estufa de 2.000 W, 1 h antes de dormir", 2.0 * FACTORES["estufa"] * 1, PRECIO),
]
rows = []
for nombre, kd, p in comp:
    rows.append([nombre, num(kd), eur(kd * p), eur(kd * DIAS_MES * p), eur(kd * INVIERNO * p)])
t3 = tabla("manta_comparativa", ["Opción", "kWh por noche", "Por noche", "Por mes", "Invierno (4 meses)"], rows)
md["cuanto-consume-una-manta-electrica"] = cabecera(
    "manta eléctrica",
    f"- Factor de uso real: {num(f, 1)} (manta eléctrica en CLAUDE.md). Uso tipo de la calculadora: 100 W, {H_MANTA} h, de madrugada (valle). Mes {num(DIAS_MES, 1)} días, invierno 4 meses.\n"
    f"- Comparativa: radiador de aceite con factor {num(FACTORES['radiador'], 1)} y estufa con factor {num(FACTORES['estufa'], 2)}, a precio fijo.\n"
) + ("## Coste por potencia\n\n" + t1 + "\n## Manta de 100 W según las horas\n\n" + t2 +
     "\n## Frente a calentar el dormitorio\n\n" + t3)

# --------------------------------------------------------------- deshumidificador
f = FACTORES["deshumidificador"]
H_DES = 8
rows = []
for w in [150, 250, 400, 600]:
    k = w / 1000 * f
    rows.append([watts(w), num(k), eur(k * PRECIO), eur(k * H_DES * PRECIO),
                 eur(k * H_DES * DIAS_MES * PRECIO), eur(k * H_DES * ANO * PRECIO)])
t1 = tabla("desh_potencias", ["Potencia", "kWh por hora (real)", "Por hora", "Por día (8 h)", "Por mes", "Año entero (12 meses)"], rows)

rows = []
for h in [4, 8, 12, 24]:
    k = 0.25 * f * h
    rows.append([horas(h), num(k), eur(k * PRECIO), eur(k * DIAS_MES * PRECIO)])
t2 = tabla("desh_horas", ["Horas al día", "kWh al día", "Por día", "Por mes"], rows)

k = 0.25 * f * H_DES
rows = []
for nombre, p in [("Precio fijo", PRECIO), ("Tarifa por horas, repartido todo el día", PRECIO_TODO_DIA),
                  ("Tarifa por horas, todo en valle", TRAMOS["valle"]), ("Tarifa por horas, todo en punta", TRAMOS["punta"])]:
    rows.append([nombre, num(p, 3) + " €/kWh", eur(k * p), eur(k * DIAS_MES * p)])
t3 = tabla("desh_tramos", ["Cómo lo usas", "Precio con impuestos", "Por día (8 h)", "Por mes"], rows)

COLADAS = 12
ropa = [
    ("Deshumidificador de 250 W, 6 h (ejemplo)", 0.25 * f * 6),
    ("Secadora de evacuación de 2.500 W, 1 h", 2.5 * FACTORES["secadora"] * 1),
    ("Secadora con bomba de calor de 900 W, 1,5 h", 0.9 * FACTORES["secadora"] * 1.5),
]
rows = []
for nombre, kc in ropa:
    rows.append([nombre, num(kc), eur(kc * PRECIO), eur(kc * COLADAS * PRECIO)])
t4 = tabla("desh_ropa", ["Cómo secas la colada", "kWh por colada", "Por colada", f"Al mes ({COLADAS} coladas)"], rows)
md["cuanto-consume-un-deshumidificador"] = cabecera(
    "deshumidificador",
    f"- Factor de uso real: {num(f, 1)} (deshumidificador en CLAUDE.md). Uso tipo de la calculadora: 250 W, {H_DES} h, todo el día. Mes {num(DIAS_MES, 1)} días, año 12 meses.\n"
    f"- «Repartido todo el día» = precio medio de la calculadora: entre semana 1/3 punta, 1/3 llano, 1/3 valle; fin de semana valle = {num(PRECIO_TODO_DIA, 3)} €/kWh.\n"
    f"- Colada: horas de ejemplo; secadoras con los valores de la calculadora (factor {num(FACTORES['secadora'], 1)}). Se cuenta por usos ({COLADAS} coladas al mes).\n"
) + ("## Coste por potencia\n\n" + t1 + "\n## Deshumidificador de 250 W según las horas\n\n" + t2 +
     "\n## Según el tramo\n\n" + t3 + "\n## Secar la ropa\n\n" + t4)

for slug, text in md.items():
    (BASE / "calculos" / f"{slug}.md").write_text(text, encoding="utf-8")
(BASE / "scripts" / "tablas_calefaccion2.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n\n".join(md.values()))
