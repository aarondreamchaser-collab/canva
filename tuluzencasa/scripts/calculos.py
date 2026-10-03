"""Cálculos de consumo y coste para los artículos de tuluzencasa.com.

Criterios (CLAUDE.md):
- Energía 0,13 €/kWh sin impuestos; factor impuestos 1,272 -> 0,165 €/kWh con impuestos.
- 2.0TD orientativa sin impuestos: punta 0,19 · llano 0,12 · valle 0,08 €/kWh.
- Factores de uso real por aparato.
- Euros redondeados a 2 decimales (ROUND_HALF_UP).

Genera calculos/<slug>.md (para revisión) y scripts/tablas.json (tablas que
build.py inserta en los artículos).
"""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PRECIO = 0.165  # €/kWh con impuestos
FACTOR_IMP = 1.272
DIAS_MES = 30.4  # días por mes, igual que la calculadora de la home
DIAS_ANO = 12 * DIAS_MES  # 364,8 días
TRAMOS = {"punta": 0.19 * FACTOR_IMP, "llano": 0.12 * FACTOR_IMP, "valle": 0.08 * FACTOR_IMP}

FACTORES = {
    "aire": 0.6, "radiador": 0.6, "estufa": 0.85, "nevera": 0.2, "termo": 0.7,
    "horno": 0.6, "induccion": 0.7, "vitro": 0.75, "lavavajillas": 0.55,
    "secadora": 0.8, "freidora": 0.7, "emisor": 0.6, "manta": 0.5,
    "deshumidificador": 0.8, "resto": 1.0,
}


def eur(x):
    if 0 < x < 0.005:
        return "< 0,01 €"
    d = Decimal(str(round(x, 9))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{d:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"


def num(x, dec=2):
    d = Decimal(str(round(x, 9))).quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_UP)
    s = f"{d:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def watts(w):
    return num(w, 0) + " W"


tablas = {}
md = {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    out += "".join("| " + " | ".join(r) + " |\n" for r in rows)
    return out


def cabecera(titulo, extra=""):
    return (f"# Cálculos — {titulo}\n\n"
            f"- Precio de la energía: 0,13 €/kWh sin impuestos × {num(FACTOR_IMP, 3)} = **{num(PRECIO, 3)} €/kWh con impuestos**.\n"
            f"- 2.0TD con impuestos: punta {num(TRAMOS['punta'], 3)} · llano {num(TRAMOS['llano'], 3)} · valle {num(TRAMOS['valle'], 3)} €/kWh.\n"
            f"- Euros redondeados a 2 decimales (redondeo comercial).\n{extra}\n")


# ---------------------------------------------------------------- aire acondicionado
f = FACTORES["aire"]
H_DIA, DIAS_VERANO = 8, 3 * DIAS_MES
rows = []
for w in [800, 1000, 1500, 2000, 2500]:
    kwh_h = w / 1000 * f
    rows.append([watts(w), num(kwh_h), eur(kwh_h * PRECIO), eur(kwh_h * H_DIA * PRECIO),
                 eur(kwh_h * H_DIA * DIAS_MES * PRECIO), eur(kwh_h * H_DIA * DIAS_VERANO * PRECIO)])
t1 = tabla("aire_potencias",
           ["Potencia eléctrica", "kWh por hora (real)", "Por hora", "Por día (8 h)", "Por mes (30,4 días)", "Verano (3 meses)"], rows)

EER = 3.5
rows = []
for fr in [2250, 3000, 4500, 5500]:
    kw_term = fr / 860
    w_elec = kw_term / EER * 1000
    kwh_h = w_elec / 1000 * f
    rows.append([num(fr, 0) + " frigorías/h", num(kw_term) + " kW", watts(round(w_elec)), eur(kwh_h * PRECIO),
                 eur(kwh_h * H_DIA * DIAS_MES * PRECIO)])
t2 = tabla("aire_frigorias",
           ["Equipo", "Potencia de frío", "Potencia eléctrica (EER 3,5)", "Por hora", "Por mes (8 h/día)"], rows)

rows = []
kwh_h = 1.0 * f
for tramo, p in TRAMOS.items():
    rows.append([tramo.capitalize(), num(p, 3) + " €/kWh", eur(kwh_h * p), eur(kwh_h * 4 * p), eur(kwh_h * 4 * DIAS_MES * p)])
rows.append(["Precio fijo", num(PRECIO, 3) + " €/kWh", eur(kwh_h * PRECIO), eur(kwh_h * 4 * PRECIO), eur(kwh_h * 4 * DIAS_MES * PRECIO)])
t3 = tabla("aire_tramos", ["Tramo", "Precio con impuestos", "Por hora", "4 horas", "Mes (4 h/día)"], rows)

md["cuanto-consume-aire-acondicionado"] = cabecera(
    "aire acondicionado",
    f"- Factor de uso real: {num(f, 2)} (el compresor no funciona al 100 % todo el tiempo).\n"
    f"- Uso tipo: {H_DIA} h/día, {num(DIAS_MES, 1)} días/mes, temporada de 3 meses ({num(DIAS_VERANO, 1)} días).\n"
    f"- Frigorías → kW: frigorías/h ÷ 860. Potencia eléctrica = kW de frío ÷ EER (EER supuesto {num(EER, 1)}).\n"
) + "## Coste por potencia eléctrica\n\n" + t1 + "\n## De frigorías a coste\n\n" + t2 + \
    "\n## Equipo de 1.000 W según tramo horario (2.0TD)\n\n" + t3

# ---------------------------------------------------------------- radiador de aceite
f = FACTORES["radiador"]
H_DIA, DIAS_INV = 5, 4 * DIAS_MES
rows = []
for w in [1000, 1500, 2000, 2500]:
    kwh_h = w / 1000 * f
    rows.append([watts(w), num(kwh_h), eur(kwh_h * PRECIO), eur(kwh_h * H_DIA * PRECIO),
                 eur(kwh_h * H_DIA * DIAS_MES * PRECIO), eur(kwh_h * H_DIA * DIAS_INV * PRECIO)])
t1 = tabla("radiador_potencias",
           ["Potencia", "kWh por hora (real)", "Por hora", "Por día (5 h)", "Por mes (30,4 días)", "Invierno (4 meses)"], rows)
rows = []
kwh_h = 2.0 * f
for tramo, p in TRAMOS.items():
    rows.append([tramo.capitalize(), num(p, 3) + " €/kWh", eur(kwh_h * p), eur(kwh_h * H_DIA * p), eur(kwh_h * H_DIA * DIAS_MES * p)])
rows.append(["Precio fijo", num(PRECIO, 3) + " €/kWh", eur(kwh_h * PRECIO), eur(kwh_h * H_DIA * PRECIO), eur(kwh_h * H_DIA * DIAS_MES * PRECIO)])
t2 = tabla("radiador_tramos", ["Tramo", "Precio con impuestos", "Por hora", "Por día (5 h)", "Por mes"], rows)
rows = []
for h in [2, 4, 6, 8]:
    kwh = 2.0 * f * h
    rows.append([f"{h} h", num(kwh), eur(kwh * PRECIO), eur(kwh * DIAS_MES * PRECIO)])
t3 = tabla("radiador_horas", ["Horas al día", "kWh al día", "Por día", "Por mes"], rows)
md["cuanto-consume-radiador-de-aceite"] = cabecera(
    "radiador de aceite",
    f"- Factor de uso real: {num(f, 2)} (el termostato corta y reconecta la resistencia).\n"
    f"- Uso tipo: {H_DIA} h/día, {num(DIAS_MES, 1)} días/mes, invierno de 4 meses ({num(DIAS_INV, 1)} días).\n"
) + "## Coste por potencia\n\n" + t1 + "\n## Radiador de 2.000 W según tramo (5 h/día)\n\n" + t2 + \
    "\n## Radiador de 2.000 W según horas de uso\n\n" + t3

# ---------------------------------------------------------------- freidora de aire vs horno
f_fr, f_ho = FACTORES["freidora"], FACTORES["horno"]
MIN_FR, MIN_HO, USOS_MES = 20, 45, 12
rows = []
for w in [1200, 1500, 1800]:
    kwh_h = w / 1000 * f_fr
    kwh_uso = kwh_h * MIN_FR / 60
    rows.append(["Freidora " + watts(w), eur(kwh_h * PRECIO), num(kwh_uso), eur(kwh_uso * PRECIO),
                 eur(kwh_uso * USOS_MES * PRECIO), eur(kwh_uso * USOS_MES * 12 * PRECIO)])
for w in [2000, 2200, 3000]:
    kwh_h = w / 1000 * f_ho
    kwh_uso = kwh_h * MIN_HO / 60
    rows.append(["Horno " + watts(w), eur(kwh_h * PRECIO), num(kwh_uso), eur(kwh_uso * PRECIO),
                 eur(kwh_uso * USOS_MES * PRECIO), eur(kwh_uso * USOS_MES * 12 * PRECIO)])
t1 = tabla("freidora_comparativa",
           ["Aparato", "Por hora", "kWh por uso", "Por uso", "Por mes (12 usos)", "Por año"], rows)
# ahorro freidora 1500 vs horno 2200 (mismos valores que la calculadora de la home)
fr_uso = 1.5 * f_fr * MIN_FR / 60 * PRECIO
ho_uso = 2.2 * f_ho * MIN_HO / 60 * PRECIO
rows = [["Freidora de 1.500 W, 20 min", eur(fr_uso), eur(fr_uso * USOS_MES), eur(fr_uso * USOS_MES * 12)],
        ["Horno de 2.200 W, 45 min", eur(ho_uso), eur(ho_uso * USOS_MES), eur(ho_uso * USOS_MES * 12)],
        ["Diferencia", eur(ho_uso - fr_uso), eur((ho_uso - fr_uso) * USOS_MES), eur((ho_uso - fr_uso) * USOS_MES * 12)]]
t2 = tabla("freidora_ahorro", ["Caso", "Por uso", "Por mes (12 usos)", "Por año"], rows)
rows = []
for m in [10, 15, 20, 30, 40]:
    kwh = 1.5 * f_fr * m / 60
    rows.append([f"{m} min", num(kwh, 3), eur(kwh * PRECIO)])
t3 = tabla("freidora_minutos", ["Tiempo", "kWh", "Coste"], rows)
md["cuanto-consume-freidora-de-aire"] = cabecera(
    "freidora de aire frente a horno",
    f"- Freidora: factor {num(f_fr, 1)} (el termostato corta la resistencia a ratos). Uso tipo {MIN_FR} min.\n"
    f"- Horno: factor {num(f_ho, 1)}. Uso tipo {MIN_HO} min (incluye ~10 min de precalentado).\n"
    f"- {USOS_MES} usos al mes (unas 3 por semana), 12 meses.\n"
) + "## Comparativa\n\n" + t1 + "\n## Freidora de 1.500 W frente a horno de 2.200 W\n\n" + t2 + \
    "\n## Freidora de 1.500 W según minutos\n\n" + t3

# ---------------------------------------------------------------- termo eléctrico
f = FACTORES["termo"]
H_DIA = 3
rows = []
for w in [1200, 1500, 2000, 2500]:
    kwh_h = w / 1000 * f
    rows.append([watts(w), num(kwh_h), eur(kwh_h * PRECIO), eur(kwh_h * H_DIA * PRECIO),
                 eur(kwh_h * H_DIA * DIAS_MES * PRECIO), eur(kwh_h * H_DIA * DIAS_ANO * PRECIO)])
t1 = tabla("termo_potencias",
           ["Potencia", "kWh por hora (real)", "Por hora", "Por día (3 h)", "Por mes", "Por año"], rows)
rows = []
for litros in [50, 80, 100]:
    kwh = litros * (60 - 15) * 1.163 / 1000
    rows.append([f"{litros} L", num(kwh), eur(kwh * PRECIO), eur(kwh * TRAMOS["valle"]), eur(kwh * TRAMOS["punta"])])
t2 = tabla("termo_litros",
           ["Depósito", "kWh (de 15 a 60 °C)", "Precio fijo", "En valle", "En punta"], rows)
kwh_dia = 1.5 * f * H_DIA
rows = []
for nombre, p in [("Sin programar, repartido en punta", TRAMOS["punta"]),
                  ("Sin programar, repartido en llano", TRAMOS["llano"]),
                  ("Programado en valle (0–8 h)", TRAMOS["valle"]),
                  ("Precio fijo (cualquier hora)", PRECIO)]:
    rows.append([nombre, eur(kwh_dia * p), eur(kwh_dia * DIAS_MES * p), eur(kwh_dia * DIAS_ANO * p)])
t3 = tabla("termo_programar", ["Termo de 1.500 W, 3 h/día", "Por día", "Por mes", "Por año"], rows)
ahorro_mes = kwh_dia * DIAS_MES * (TRAMOS["punta"] - TRAMOS["valle"])
ahorro_mes_llano = kwh_dia * DIAS_MES * (TRAMOS["llano"] - TRAMOS["valle"])
md["cuanto-consume-termo-electrico"] = cabecera(
    "termo eléctrico",
    f"- Factor de uso real: {num(f, 2)}. Uso tipo {H_DIA} h de resistencia al día.\n"
    f"- Energía para calentar agua: litros × ΔT × 1,163 Wh (calor específico del agua). ΔT = 60 − 15 = 45 °C.\n"
    f"- Ahorro al mes por programar en valle (1.500 W, 3 h/día): frente a punta {eur(ahorro_mes)}, frente a llano {eur(ahorro_mes_llano)}.\n"
) + "## Coste por potencia\n\n" + t1 + "\n## Calentar el depósito entero\n\n" + t2 + \
    "\n## Programar o no programar\n\n" + t3

# ---------------------------------------------------------------- nevera
f = FACTORES["nevera"]
W_NOM = 150
kwh_h = W_NOM / 1000 * f
rows = [["Nevera tipo (150 W × 0,2)", num(kwh_h, 3), eur(kwh_h * PRECIO), eur(kwh_h * 24 * PRECIO),
         eur(kwh_h * 24 * DIAS_MES * PRECIO), eur(kwh_h * 24 * DIAS_ANO * PRECIO)]]
t1 = tabla("nevera_tipo", ["Caso", "kWh por hora", "Por hora", "Por día", "Por mes", "Por año"], rows)
rows = []
for anual in [100, 150, 200, 250, 300, 400]:
    rows.append([f"{anual} kWh/año", num(anual / 365, 2), eur(anual / 365 * PRECIO), eur(anual / 12 * PRECIO), eur(anual * PRECIO)])
t2 = tabla("nevera_etiqueta", ["Consumo en la etiqueta", "kWh al día", "Por día", "Por mes", "Por año"], rows)
rows = []
for vieja, nueva in [(450, 250), (350, 200), (250, 180)]:
    d = (vieja - nueva) * PRECIO
    rows.append([f"{vieja} kWh/año", f"{nueva} kWh/año", eur(d), eur(d * 10)])
t3 = tabla("nevera_cambio", ["Nevera actual", "Nevera nueva", "Ahorro al año", "Ahorro en 10 años"], rows)
md["cuanto-consume-una-nevera"] = cabecera(
    "nevera",
    f"- Estimación genérica: {W_NOM} W nominales × factor {num(f, 1)} = {num(kwh_h, 3)} kWh por hora, funcionando 24 h.\n"
    f"- Con etiqueta: kWh/año ÷ 365 (día) y ÷ 12 (mes). Estimación genérica: {num(DIAS_MES, 1)} días/mes y 12 meses/año.\n"
) + "## Nevera tipo\n\n" + t1 + "\n## Según el consumo de la etiqueta\n\n" + t2 + \
    "\n## Cambiar de nevera\n\n" + t3

# ---------------------------------------------------------------- diferencial
rows = []
for ma in [5, 10, 20, 29]:
    w = 230 * ma / 1000
    kwh_h = w / 1000
    rows.append([f"{ma} mA", num(w, 1) + " W", eur(kwh_h * PRECIO), eur(kwh_h * 24 * PRECIO),
                 eur(kwh_h * 24 * DIAS_MES * PRECIO), eur(kwh_h * 24 * DIAS_ANO * PRECIO)])
t1 = tabla("dif_fugas", ["Fuga continua", "Potencia (230 V)", "Por hora", "Por día", "Por mes", "Por año"], rows)
aparatos = [("Termo eléctrico", 1500, FACTORES["termo"]), ("Lavadora (calentando agua)", 2000, 1.0),
            ("Horno", 2500, FACTORES["horno"]), ("Aire acondicionado", 1000, FACTORES["aire"]),
            ("Radiador de aceite", 2000, FACTORES["radiador"])]
rows = []
for n, w, fa in aparatos:
    rows.append([n, watts(w), num(fa, 2).rstrip("0").rstrip(","), eur(w / 1000 * fa * PRECIO)])
t2 = tabla("dif_aparatos", ["Aparato", "Potencia típica", "Factor de uso", "Coste por hora"], rows)
md["por-que-salta-el-diferencial"] = cabecera(
    "diferencial",
    "- Potencia de una fuga: P = 230 V × I. Se supone fuga continua 24 h (caso peor).\n"
    "- Un diferencial de 30 mA puede disparar a partir de 15 mA (la norma exige que no dispare por debajo de la mitad de su sensibilidad) [VERIFICAR: rango de disparo 0,5–1 IΔn según UNE-EN 61008].\n"
) + "## Lo que cuesta una fuga que no llega a disparar\n\n" + t1 + "\n## Aparatos que suelen estar detrás\n\n" + t2

for slug, text in md.items():
    (BASE / "calculos" / f"{slug}.md").write_text(text, encoding="utf-8")
(BASE / "scripts" / "tablas.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n\n".join(md.values()))
