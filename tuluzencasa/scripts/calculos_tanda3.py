"""Cálculos de la tanda de artículos informativos (1.ª parte): tramos horarios, bono social,
placas solares y coche eléctrico.

Criterios de CLAUDE.md: 0,165 €/kWh con impuestos; 2.0TD con impuestos punta 0,242 · llano 0,153 ·
valle 0,102; mes de 30,4 días; año de 12 meses. Término de potencia 0,09 €/kW y día con impuesto
eléctrico e IVA (1,21 × 1,0511), igual que las calculadoras.
Fuentes de datos externos (comprobadas el 5/10/2026):
- Horarios 2.0TD: Circular 3/2020 de la CNMC (BOE-A-2020-1066), texto consolidado.
- Bono social: Real Decreto 897/2017 (BOE-A-2017-11505), texto consolidado: art. 3 (umbrales en
  múltiplos del IPREM), art. 6 (descuentos del 35 % y 50 %) y anexo I (límites de kWh al año).
- Producción fotovoltaica: PVGIS 5.2 de la Comisión Europea (fuentes/pvgis_*.json), 1 kWp,
  30° de inclinación, orientación sur, 14 % de pérdidas.
- Recarga: ITC-BT-52 (Real Decreto 1053/2014): recarga lenta de referencia a 16 A.
Genera calculos/<slug>.md y scripts/tablas_tanda3.json.
"""
import json
from pathlib import Path
from calculos import PRECIO, TRAMOS, FACTOR_IMP, DIAS_MES, eur, num, cabecera

BASE = Path(__file__).resolve().parent.parent
IMP_POT, POT_DIA = 1.21 * 1.0511, 0.09
ENERGIA_SIN = 0.13
tablas, md = {}, {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def pct(x, dec=1):
    return num(x * 100, dec) + " %"


P, L, V = TRAMOS["punta"], TRAMOS["llano"], TRAMOS["valle"]

# ------------------------------------------------------------------ 1. tramos horarios
t1 = tabla("tramos_horario", ["Tramo", "De lunes a viernes", "Sábados, domingos y festivos nacionales", "Precio con impuestos"], [
    ["Punta (P1)", "De 10 a 14 h y de 18 a 22 h", "—", num(P, 3) + " €/kWh"],
    ["Llano (P2)", "De 8 a 10 h, de 14 a 18 h y de 22 a 24 h", "—", num(L, 3) + " €/kWh"],
    ["Valle (P3)", "De 0 a 8 h", "Todo el día", num(V, 3) + " €/kWh"],
])
horas = {"Punta": 8 * 5, "Llano": 8 * 5, "Valle": 8 * 5 + 48}
t2 = tabla("tramos_semana", ["Tramo", "Horas a la semana", "Parte de la semana"],
           [[k, str(v), pct(v / 168)] for k, v in horas.items()])
usos = [  # nombre, kWh por uso (valores de la calculadora de la portada), usos al mes
    ("Lavadora a 40 °C (800 W, 1 h)", 0.8 * 1 * 1.0, 12),
    ("Lavavajillas eco (1.200 W, 1,5 h)", 1.2 * 1.5 * 0.55, 12),
    ("Secadora de evacuación (2.500 W, 1 h)", 2.5 * 1 * 0.8, 12),
    ("Horno (2.200 W, 45 min)", 2.2 * 0.75 * 0.6, 12),
    ("Termo de 80 L (1.500 W, 3 h al día)", 1.5 * 3 * 0.7, DIAS_MES),
]
rows = []
for n, k, u in usos:
    rows.append([n, num(k), eur(k * P), eur(k * V), eur(k * (P - V)), eur(k * u * (P - V)), eur(k * u * (P - V) * 12)])
t3 = tabla("tramos_aparatos", ["Aparato", "kWh por uso", "En punta", "En valle", "Ahorro por uso", "Ahorro al mes", "Ahorro al año"], rows)
KWH_MES = 252.7  # consumo del piso de ejemplo de «Cómo leer la factura de la luz»
rows = []
for v in (0.20, 0.30, 0.40, 0.50, 0.60):
    p = l = (1 - v) / 2
    c = KWH_MES * (p * P + l * L + v * V)
    dif = KWH_MES * PRECIO - c
    rows.append([pct(v, 0), pct(p, 0), eur(c), eur(KWH_MES * PRECIO), eur(abs(dif)) + (" menos" if dif > 0 else " más")])
t4 = tabla("tramos_reparto", ["En valle", "En punta y en llano (cada uno)", "Energía con tramos", "Energía a precio fijo", "Con tramos pagas al mes"], rows)
# punto de empate con precio fijo, con punta = llano
v_emp = ((P + L) / 2 - PRECIO) / ((P + L) / 2 - V)
md["tramos-horarios-luz"] = cabecera(
    "tramos horarios de la luz",
    "- Horarios: Circular 3/2020 de la CNMC (BOE-A-2020-1066), apartado de discriminación horaria de tres periodos.\n"
    f"- Usos al mes: 12 para lavadora, lavavajillas, secadora y horno; el termo, {num(DIAS_MES, 1)} días.\n"
    f"- Reparto de ejemplo sobre {num(KWH_MES, 1)} kWh al mes (piso de «Cómo leer la factura de la luz»). Solo término de energía.\n"
    f"- Con punta y llano a partes iguales, la tarifa por horas empata con el precio fijo cuando el {pct(v_emp)} del consumo cae en valle.\n"
) + "## Horarios\n\n" + t1 + "\n## Horas a la semana\n\n" + t2 + "\n## Aparatos\n\n" + t3 + "\n## Reparto del consumo\n\n" + t4

# ------------------------------------------------------------------ 2. bono social
def umbral(adultos, menores):
    return 1.5 + 0.3 * (adultos - 1) + 0.5 * menores


hogares = [("Una persona", 1, 0, False), ("Dos adultos", 2, 0, False), ("Dos adultos y un menor", 2, 1, False),
           ("Dos adultos y dos menores", 2, 2, False), ("Un adulto y un menor (monoparental)", 1, 1, True)]
rows = []
for n, a, m, mono in hogares:
    u = umbral(a, m)
    ue = u + 1  # circunstancia especial (art. 3.3); la monoparental ya lo es
    if mono:
        rows.append([n, "—", num(ue, 2) + " veces", num(ue / 2, 2) + " veces"])
    else:
        rows.append([n, num(u, 2) + " veces", num(ue, 2) + " veces", num(u / 2, 2) + " veces"])
t1 = tabla("bono_umbrales", ["Unidad de convivencia", "Vulnerable", "Vulnerable con circunstancia especial", "Vulnerable severo"], rows)
limites = [("Una persona o dos personas", 1587), ("Tres personas, pensionistas con pensión mínima, o dos personas siendo una menor", 2222),
           ("Cuatro personas, o tres siendo dos menores", 2698), ("Cinco o más personas, cuatro siendo tres menores, o familia numerosa", 4761)]
t2 = tabla("bono_limites", ["Hogar", "kWh al año con descuento", "Equivale a unos kWh al mes"],
           [[n, num(k, 0), num(k / 12, 0)] for n, k in limites])
# ejemplo: dos personas, 3,45 kW, consumo igual al límite (1.587 kWh/año)
kw, kwh = 3.45, 1587 / 12
pot, ene = kw * POT_DIA * DIAS_MES, kwh * ENERGIA_SIN
rows = []
for n, d in [("Sin bono social", 0), ("Vulnerable (35 %)", 0.35), ("Vulnerable severo (50 %)", 0.50)]:
    tot = (pot + ene) * (1 - d) * IMP_POT
    rows.append([n, eur(tot), eur((pot + ene) * IMP_POT - tot), eur(((pot + ene) * IMP_POT - tot) * 12)])
t3 = tabla("bono_ejemplo", ["Situación", "Potencia y energía al mes, con impuestos", "Descuento al mes", "Descuento al año"], rows)
md["bono-social-electrico"] = cabecera(
    "bono social eléctrico",
    "- Umbrales de renta: RD 897/2017, art. 3.2.a y 3.3 (1,5 veces el IPREM de 14 pagas, +0,3 por adulto adicional, +0,5 por menor, +1 con circunstancia especial). Severo: art. 3.4 (renta ≤ 50 % del umbral).\n"
    "- Descuentos: art. 6.3 (35 % vulnerable, 50 % severo), en vigor tras la derogación del RDL 16/2025 (Resolución de 27/01/2026).\n"
    "- Límites de energía: anexo I del RD 897/2017.\n"
    f"- Ejemplo orientativo con los precios de referencia de la web: {num(kw, 2)} kW, {num(POT_DIA, 2)} €/kW y día, {num(ENERGIA_SIN, 2)} €/kWh sin impuestos, {num(kwh, 2)} kWh al mes (el límite de dos personas). "
    "Descuento sobre potencia y energía; impuesto eléctrico e IVA después. No incluye el alquiler del contador.\n"
) + "## Umbrales de renta (veces el IPREM de 14 pagas)\n\n" + t1 + "\n## Límites de energía\n\n" + t2 + "\n## Ejemplo\n\n" + t3

# ------------------------------------------------------------------ 3. placas solares
pv = {}
for c in ("sevilla", "madrid", "zaragoza", "barcelona", "bilbao"):
    d = json.loads((BASE / "fuentes" / f"pvgis_{c}.json").read_text())
    pv[c] = {"anual": d["outputs"]["totals"]["fixed"]["E_y"], "mes": [m["E_m"] for m in d["outputs"]["monthly"]["fixed"]]}
nombres = {"sevilla": "Sevilla", "madrid": "Madrid", "zaragoza": "Zaragoza", "barcelona": "Barcelona", "bilbao": "Bilbao"}
t1 = tabla("placas_produccion", ["Ciudad", "kWh al año por cada kWp", "Instalación de 3 kWp", "Instalación de 4 kWp"],
           [[nombres[c], num(v["anual"], 0), num(v["anual"] * 3, 0), num(v["anual"] * 4, 0)] for c, v in pv.items()])
KWP, CONSUMO_MES = 3, 250.0  # casa de ejemplo: 3.000 kWh al año repartidos por igual


def simula(ciudad, directo, p_comp):
    """Mes a mes: lo que se usa en el momento ahorra a precio fijo; los excedentes se compensan
    a p_comp (€/kWh sin impuestos) sin superar lo que cuesta la energía tomada de la red ese mes."""
    ahorro_dir = comp = autoc = exc = 0.0
    for e in pv[ciudad]["mes"]:
        prod = e * KWP
        a = min(prod * directo, CONSUMO_MES)
        x = prod - a
        red = CONSUMO_MES - a
        c = min(x * p_comp, red * ENERGIA_SIN)
        autoc += a; exc += x; ahorro_dir += a * PRECIO; comp += c * FACTOR_IMP
    return autoc, exc, ahorro_dir, comp


rows = []
for directo in (0.30, 0.40, 0.50):
    a, x, s, c = simula("madrid", directo, 0.06)
    rows.append([pct(directo, 0), num(a, 0), eur(s), num(x, 0), eur(c), eur(s + c)])
t2 = tabla("placas_ahorro", ["Producción que usas al momento", "kWh que dejas de comprar", "Ahorro por autoconsumo", "Excedentes (kWh)", "Compensación a 0,06 €/kWh", "Ahorro total al año"], rows)
rows = []
for pc in (0.04, 0.06, 0.08):
    a, x, s, c = simula("madrid", 0.40, pc)
    rows.append([num(pc, 2) + " €/kWh", eur(c), eur(s + c)])
t3 = tabla("placas_compensacion", ["Precio de compensación (ejemplo)", "Compensación al año", "Ahorro total al año"], rows)
a, x, s, c = simula("madrid", 0.40, 0.06)
ahorro_ref = s + c
rows = [[eur(inv), eur(ahorro_ref), num(inv / ahorro_ref, 1) + " años"] for inv in (3000, 4500, 6000)]
t4 = tabla("placas_amortizacion", ["Si la instalación te cuesta", "Ahorro al año (Madrid, 40 %, 0,06 €/kWh)", "Se paga en"], rows)
rows = []
for c in pv:
    a, x, s, cc = simula(c, 0.40, 0.06)
    rows.append([nombres[c], eur(s + cc)])
t5 = tabla("placas_ciudades", ["Ciudad", "Ahorro al año (3 kWp, 40 %, 0,06 €/kWh)"], rows)
md["placas-solares-en-casa"] = cabecera(
    "placas solares en casa",
    "- Producción: PVGIS 5.2 (Comisión Europea), base SARAH2 2005-2020, 1 kWp, 30° sur, 14 % de pérdidas (fuentes/pvgis_*.json).\n"
    f"- Casa de ejemplo: {num(CONSUMO_MES * 12, 0)} kWh al año ({num(CONSUMO_MES, 0)} al mes), instalación de {KWP} kWp, sin baterías.\n"
    "- «Producción que usas al momento»: porcentaje de ejemplo (depende de los hábitos); nunca más que el consumo del mes.\n"
    f"- Autoconsumo: ahorra {num(PRECIO, 3)} €/kWh con impuestos. Excedentes: precio de compensación de ejemplo sin impuestos, ×{num(FACTOR_IMP, 3)}; "
    "cada mes no puede superar el coste de la energía tomada de la red (RD 244/2019, art. 14.3).\n"
    "- Inversiones de la amortización: valores posibles, no precios reales. No incluye cambios en el término de potencia.\n"
) + "## Producción\n\n" + t1 + "\n## Ahorro según el autoconsumo\n\n" + t2 + "\n## Según el precio de compensación\n\n" + t3 + "\n## Amortización\n\n" + t4 + "\n## Por ciudad\n\n" + t5

# ------------------------------------------------------------------ 4. coche eléctrico
rows = []
for c in (12, 15, 18):
    rows.append([num(c, 0) + " kWh", eur(c * PRECIO), eur(c * V), eur(c * L), eur(c * P)])
t1 = tabla("coche_100km", ["Consumo cada 100 km", "Precio fijo", "En valle", "En llano", "En punta"], rows)
rows = []
for km in (500, 1000, 1500):
    k = 15 * km / 100
    rows.append([num(km, 0) + " km", num(k, 0) + " kWh", eur(k * PRECIO), eur(k * V), eur(k * PRECIO * 12), eur(k * V * 12)])
t2 = tabla("coche_mes", ["Kilómetros al mes", "Energía", "Al mes, precio fijo", "Al mes, en valle", "Al año, precio fijo", "Al año, en valle"], rows)
rows = []
for n, kwc in [("Toma de 16 A (3,7 kW)", 230 * 16 / 1000), ("Cargador de 32 A (7,4 kW)", 230 * 32 / 1000)]:
    rows.append([n, num(kwc, 2) + " kW", num(30 / kwc, 1) + " h", num(kwc / 15 * 100, 0) + " km"])
t3 = tabla("coche_tiempo", ["Punto de carga (monofásico)", "Potencia", "Horas para cargar 30 kWh", "Km que recuperas por hora"], rows)
rows = []
for sube in (1.15, 2.3, 3.45):
    rows.append(["+" + num(sube, 2) + " kW", eur(sube * POT_DIA * DIAS_MES * IMP_POT), eur(sube * POT_DIA * 365 * IMP_POT)])
t4 = tabla("coche_potencia", ["Subir la potencia", "Coste al mes", "Coste al año"], rows)
md["cuanto-cuesta-cargar-coche-electrico-casa"] = cabecera(
    "cargar un coche eléctrico en casa",
    "- Consumos de 12, 15 y 18 kWh cada 100 km: ejemplos; el real está en la ficha técnica del coche.\n"
    "- Kilómetros al mes con un consumo de 15 kWh/100 km. No incluye las pérdidas de la carga.\n"
    "- Potencia de carga: amperios × 230 V. La ITC-BT-52 toma como referencia la recarga lenta a 16 A durante 8 h.\n"
    f"- Potencia: {num(POT_DIA, 2)} €/kW y día, con impuesto eléctrico e IVA, en todos los periodos (igual que las calculadoras).\n"
    f"- 1.000 km al mes en valle frente a precio fijo: {eur(150 * (PRECIO - V))} al mes, {eur(150 * (PRECIO - V) * 12)} al año.\n"
    f"- Cargar 30 kWh: {eur(30 * PRECIO)} a precio fijo, {eur(30 * V)} en valle; con 16 A durante 8 h entran {num(230 * 16 / 1000 * 8, 1)} kWh ({num(230 * 16 / 1000 * 8 / 15 * 100, 0)} km a 15 kWh/100 km).\n"
) + "## Cada 100 km\n\n" + t1 + "\n## Al mes y al año\n\n" + t2 + "\n## Tiempo de carga\n\n" + t3 + "\n## Subir la potencia\n\n" + t4

for slug, text in md.items():
    (BASE / "calculos" / f"{slug}.md").write_text(text, encoding="utf-8")
(BASE / "scripts" / "tablas_tanda3.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
if __name__ == "__main__":
    print("\n\n".join(md.values()))
