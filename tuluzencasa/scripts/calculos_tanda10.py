"""Cálculos de la tanda 3 del plan (tanda 10 de la web): punto de recarga, deducciones del IRPF,
placas solares por comunidad y termo aerotérmico.

Fuentes (consultadas el 12/10/2026, textos en fuentes/tanda10/ y fuentes/comunidades-a/):
- RD 1053/2014, ITC-BT-52, tabla 1 (potencias normalizadas del circuito de recarga) e ITC-BT-04 (cuándo hace falta proyecto).
- Ley 35/2006 del IRPF, texto consolidado a 7/10/2026: DA 50.ª (eficiencia energética), DA 58.ª (vehículo y punto de recarga)
  y DA 62.ª (autoconsumo), en la redacción del Real Decreto-ley 7/2026, art. 36.
- PVGIS 5.2, 1 kWp, 30° sur, 14 % de pérdidas, capital de cada comunidad; casa de 3.000 kWh/año, 3 kWp, 40 % al momento,
  excedentes a 0,06 €/kWh con el tope mensual del RD 244/2019 (igual que «Placas solares en casa»).
  Canarias con IGIC 0 % (Ley 4/2012, art. 52.r); Ceuta y Melilla fuera del IVA (Ley 37/1992, art. 3): sin ahorro calculado.
- Reglamento (UE) 814/2013: eficiencia de caldeo de agua (ηwh) = energía útil / energía primaria, con CC = 2,5;
  mínimo desde 26/9/2017: 36 % en el perfil M y 37 % en el L.
- Agua caliente: 3 personas × 28 l/día a 60 °C (CTE HE4) con el agua fría de cada capital (CTE DB-HE, anejo G); sin pérdidas.
Genera calculos/<slug>.md y scripts/tablas_tanda10.json.
"""
import json, re
from pathlib import Path
from calculos import PRECIO, DIAS_MES, FACTOR_IMP, REF, eur, num, pr, cabecera

BASE = Path(__file__).resolve().parent.parent
F = BASE / "fuentes" / "comunidades-a" / "pvgis"
CTE = (BASE / "fuentes" / "tanda7" / "cte_dbhe.txt").read_text()
tablas, md = {}, {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def w(x):
    return num(x, 0) + " W" if x < 10000 else num(x / 1000, 2) + " kW"


# ------------------------------------------------------------------ 1. punto de recarga
CONS = 15  # kWh cada 100 km, como «Cuánto cuesta cargar un coche eléctrico en casa»
VALLE = REF["tramos"]["valle"] * FACTOR_IMP
rows = []
for amp, p in ((10, 2300), (16, 3680), (20, 4600), (32, 7360), (40, 9200)):
    rows.append([f"{amp} A", w(p), num(p / 1000 / CONS * 100, 0) + " km", num(CONS / (p / 1000), 1) + " h", num(30 / (p / 1000), 1) + " h"])
t1 = tabla("pr_potencias", ["Interruptor del circuito (230 V)", "Potencia", "Autonomía por hora de carga", "Horas para 100 km", "Horas para 30 kWh"], rows)
rows = []
for coste in (1000, 2000, 3000, 4000, 5000):
    d = 0.15 * min(coste, 4000)
    rows.append([eur(coste), eur(min(coste, 4000)), eur(d), eur(coste - d)])
t2 = tabla("pr_deduccion", ["Lo que pagas por la instalación", "Base de la deducción (máx. 4.000 €)", "Deducción del 15 %", "Coste final"], rows)
md["punto-recarga-garaje-normativa"] = cabecera(
    "punto de recarga en casa y en garaje comunitario",
    f"- Autonomía: potencia (kW) / {CONS} kWh cada 100 km × 100; horas = kWh / potencia (sin pérdidas de carga).\n"
    f"- Coste de 100 km: {CONS} kWh × {num(PRECIO, 3)} = {eur(CONS * PRECIO)}; en valle {CONS} × {num(VALLE, 3)} = {eur(CONS * VALLE)}.\n"
    f"- Una noche de 8 h a 3.680 W: {num(8 * 3.68, 2)} kWh, unos {num(8 * 3.68 / CONS * 100, 0)} km.\n"
    "- Deducción: 15 % de lo pagado, base máxima 4.000 € (LIRPF, DA 58.ª.3); instalación terminada como tarde en 2026.\n"
) + "## Potencias\n\n" + t1 + "\n## Deducción\n\n" + t2

# ------------------------------------------------------------------ 2. deducciones del IRPF
DED = [  # (qué, %, base máxima anual, hasta, requisito)
    ("Obras que reducen la demanda de calefacción y refrigeración de tu vivienda", 0.20, 5000, "Pagadas hasta el 31-12-2026", "Al menos un 7 % menos de demanda"),
    ("Obras que reducen el consumo de energía primaria no renovable de tu vivienda", 0.40, 7500, "Pagadas hasta el 31-12-2026", "Un 30 % menos, o letra A o B"),
    ("Rehabilitación energética de todo el edificio", 0.60, 5000, "Pagadas hasta el 31-12-2027", "Un 30 % menos, o letra A o B; base acumulada máx. 15.000 €"),
    ("Placas de autoconsumo en un inmueble tuyo", 0.10, 5000, "Instalación terminada en 2026", "Certificado de instalación eléctrica"),
    ("Placas de autoconsumo en un edificio residencial", 0.20, 5000, "Instalación terminada en 2026", "Certificado de instalación eléctrica"),
    ("Punto de recarga en un inmueble tuyo", 0.15, 4000, "Instalación terminada en 2026", "No afecto a una actividad económica"),
]
rows = [[q, num(p * 100, 0) + " %", eur(b), eur(p * b), h, r] for q, p, b, h, r in DED]
t1 = tabla("irpf_tipos", ["Qué", "Deducción", "Base máxima al año", "Deducción máxima al año", "Plazo", "Requisito"], rows)
rows = []
for coste in (3000, 6000, 10000):
    rows.append([eur(coste)] + [eur(p * min(coste, b)) for _, p, b, _, _ in DED[:2]] + [eur(DED[3][1] * min(coste, DED[3][2])), eur(DED[5][1] * min(coste, DED[5][2]))])
t2 = tabla("irpf_ejemplos", ["Lo que pagas", "Obra de demanda (20 %)", "Obra de consumo (40 %)", "Placas en tu casa (10 %)", "Punto de recarga (15 %)"], rows)
# edificio: 60 % con base 5.000 al año y 15.000 acumulada
cuota = 24000
anos, resto, deds = [], cuota, []
for i in range(4):
    b = min(resto, 5000)
    if b <= 0:
        break
    deds.append([f"Año {i + 1}", eur(b), eur(0.6 * b)])
    resto -= b
deds.append(["Total", eur(min(cuota, 15000)), eur(0.6 * min(cuota, 15000))])
t3 = tabla("irpf_edificio", ["Ejercicio", "Base de la deducción", "Deducción del 60 %"], deds[:3] + deds[-1:])
md["deducciones-irpf-eficiencia-energetica"] = cabecera(
    "deducciones del IRPF por eficiencia energética, placas y punto de recarga",
    "- LIRPF, DA 50.ª, 58.ª y 62.ª (texto consolidado del BOE a 7/10/2026). Deducción = % × mín(lo pagado, base máxima).\n"
    f"- Edificio: tu parte de la obra, {eur(cuota)}; base máxima {eur(5000)} al año y {eur(15000)} acumulada (DA 50.ª.3).\n"
) + "## Tipos\n\n" + t1 + "\n## Ejemplos\n\n" + t2 + "\n## Edificio\n\n" + t3

# ------------------------------------------------------------------ 3. placas por comunidad
KWP, CONSUMO_MES, DIRECTO, P_COMP = 3, 250.0, 0.40, 0.06


def simula(meses, precio, factor):
    tot = 0.0
    for e in meses:
        prod = e * KWP
        a = min(prod * DIRECTO, CONSUMO_MES)
        c = min((prod - a) * P_COMP, (CONSUMO_MES - a) * REF["energia"])
        tot += a * precio + c * factor
    return tot


def pv(k):
    f = BASE / "fuentes" / f"pvgis_{k}.json"
    return json.loads((f if f.exists() else F / f"{k}.json").read_text())


COM = [("Andalucía", "Sevilla", "sevilla"), ("Aragón", "Zaragoza", "zaragoza"), ("Asturias", "Oviedo", "oviedo"),
       ("Illes Balears", "Palma", "palma"), ("Canarias", "Santa Cruz de Tenerife", "santa-cruz-tenerife"),
       ("Canarias", "Las Palmas de G. C.", "las-palmas"), ("Cantabria", "Santander", "santander"),
       ("Castilla-La Mancha", "Toledo", "toledo"), ("Castilla y León", "Valladolid", "valladolid"), ("Cataluña", "Barcelona", "barcelona"),
       ("Comunitat Valenciana", "Valencia", "valencia"), ("Extremadura", "Mérida", "merida"), ("Galicia", "Santiago de Compostela", "santiago"),
       ("Comunidad de Madrid", "Madrid", "madrid"), ("Región de Murcia", "Murcia", "murcia"), ("Navarra", "Pamplona", "pamplona"),
       ("País Vasco", "Vitoria-Gasteiz", "vitoria"), ("La Rioja", "Logroño", "logrono"), ("Ceuta", "Ceuta", "ceuta"), ("Melilla", "Melilla", "melilla")]
PRECIO_CAN, FACTOR_CAN = REF["energia"] * (1 + REF["impuesto_electrico"]), 1 + REF["impuesto_electrico"]
datos = []
for com, cap, k in COM:
    d = pv(k)
    anual = d["outputs"]["totals"]["fixed"]["E_y"]
    meses = [m["E_m"] for m in d["outputs"]["monthly"]["fixed"]]
    if com in ("Ceuta", "Melilla"):
        ah = None
    elif com == "Canarias":
        ah = simula(meses, PRECIO_CAN, FACTOR_CAN)
    else:
        ah = simula(meses, PRECIO, FACTOR_IMP)
    datos.append((anual, com, cap, ah, meses))
datos.sort(key=lambda x: -x[0])
rows = [[com, cap, num(a, 0), num(a * KWP, 0), eur(ah) if ah is not None else "—"] for a, com, cap, ah, _ in datos]
t1 = tabla("pc_comunidades", ["Comunidad", "Capital", "kWh al año por kWp", "Producción de 3 kWp", "Ahorro al año (3 kWp, 40 %)"], rows)
mx, mn = datos[0], datos[-1]
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
sel = [x for x in datos if x[2] in ("Santa Cruz de Tenerife", "Madrid", "Oviedo")]
rows = [[MESES[i]] + [num(x[4][i] * KWP, 0) + " kWh" for x in sel] for i in range(12)]
t2 = tabla("pc_meses", ["Mes"] + [f"{x[2]} (3 kWp)" for x in sel], rows)
pen = [x for x in datos if x[1] not in ("Canarias", "Ceuta", "Melilla")]
md["placas-solares-produccion-comunidad"] = cabecera(
    "cuánto producen las placas solares en cada comunidad",
    "- PVGIS 5.2 (JRC), 1 kWp, 30° de inclinación, orientación sur, 14 % de pérdidas, en la capital de cada comunidad.\n"
    f"- Ahorro: casa de {num(CONSUMO_MES * 12, 0)} kWh/año, {KWP} kWp, {num(DIRECTO * 100, 0)} % al momento, excedentes a {num(P_COMP, 2)} €/kWh "
    f"con tope mensual (RD 244/2019). Canarias a {num(PRECIO_CAN, 3)} €/kWh (IGIC 0 %). Ceuta y Melilla sin IVA: no se calcula.\n"
    f"- Máxima: {mx[2]} {num(mx[0], 0)}; mínima: {mn[2]} {num(mn[0], 0)}; diferencia {num((mx[0] / mn[0] - 1) * 100, 0)} %.\n"
    f"- Península: de {pen[-1][2]} {num(pen[-1][0], 0)} a {pen[0][2]} {num(pen[0][0], 0)} kWh/kWp; ahorro de {eur(pen[-1][3])} a {eur(pen[0][3])}; "
    f"diferencia de producción {num((pen[0][0] / pen[-1][0] - 1) * 100, 0)} %, de ahorro {num((pen[0][3] / pen[-1][3] - 1) * 100, 0)} %.\n"
) + "## Comunidades\n\n" + t1 + "\n## Meses\n\n" + t2

# ------------------------------------------------------------------ 4. termo aerotérmico
CC, ETA_MIN = 2.5, 0.36
PERS, LITROS, T_ACS, CP = 3, 28, 60, 4.186


def agua(cap):
    m = re.search(rf"^{re.escape(cap)} ((?:\d+ ){{12}}\d+) ?$", CTE, re.M)
    return [int(x) for x in m.group(1).split()][1:]


def q_ano(cap):
    return sum(PERS * LITROS * CP * (T_ACS - t) / 3600 * DIAS_MES for t in agua(cap))


Q = q_ano("Madrid")
ETAS = [("Termo eléctrico (mínimo legal, 36 %)", ETA_MIN), ("Termo eléctrico ideal, sin pérdidas (40 %)", 1 / CC),
        ("Termo aerotérmico con ηwh 100 %", 1.0), ("Termo aerotérmico con ηwh 125 %", 1.25), ("Termo aerotérmico con ηwh 150 %", 1.5)]
base = Q / (ETA_MIN * CC)
rows = []
for n, e in ETAS:
    kwh = Q / (e * CC)
    rows.append([n, num(e * CC, 2), num(kwh, 0) + " kWh", eur(kwh * PRECIO / 12), eur(kwh * PRECIO), eur((base - kwh) * PRECIO) if e > ETA_MIN else "—"])
t1 = tabla("ta_madrid", ["Equipo", "kWh de agua caliente por kWh de luz", "Luz al año", "Al mes", "Al año", "Ahorro al año frente al mínimo legal"], rows)
rows = []
for cap, cn in (("Burgos", "Burgos"), ("Madrid", "Madrid"), ("Sevilla", "Sevilla"), ("Las Palmas de Gran Canaria", "Las Palmas de G. C.")):
    q = q_ano(cap)
    pr_ = PRECIO_CAN if cap.startswith("Las Palmas") else PRECIO
    a, b = q / (ETA_MIN * CC), q / (1.25 * CC)
    rows.append([cn, num(q, 0) + " kWh", eur(a * pr_), eur(b * pr_), eur((a - b) * pr_)])
t2 = tabla("ta_ciudades", ["Capital", "Agua caliente al año", "Termo eléctrico (36 %)", "Aerotérmico (125 %)", "Ahorro al año"], rows)
VALLE_P = REF["tramos"]["valle"] * FACTOR_IMP
kwh125 = Q / (1.25 * CC)
md["termo-aerotermico-consumo"] = cabecera(
    "cuánto consume un termo aerotérmico",
    f"- Agua caliente: {PERS} personas × {LITROS} l/día a {T_ACS} °C (CTE HE4) con el agua fría de la capital (anejo G); "
    f"Madrid: {num(Q, 0)} kWh útiles al año; meses de 30,4 días.\n"
    f"- Luz = energía útil / (ηwh × CC), CC = {num(CC, 1)} (Reglamento UE 814/2013). Mínimo legal desde 2017: {num(ETA_MIN * 100, 0)} % (perfil M).\n"
    f"- Un termo de resistencia sin pérdidas daría como mucho 1 / {num(CC, 1)} = {num(100 / CC, 0)} %.\n"
    f"- Valle: aerotérmico 125 % en Madrid, {num(kwh125, 0)} kWh × {num(VALLE_P, 3)} = {eur(kwh125 * VALLE_P)} al año.\n"
    f"- Canarias a {num(PRECIO_CAN, 3)} €/kWh (IGIC 0 %).\n"
    f"- Entre ηwh 100 % y 150 % en Madrid: {eur((Q / (1.0 * CC) - Q / (1.5 * CC)) * PRECIO)} al año.\n"
    f"- Aerotérmico frente al mínimo legal: consume el {num(ETA_MIN / 1.5 * 100, 0)} % (ηwh 150 %) o el {num(ETA_MIN / 1.0 * 100, 0)} % (ηwh 100 %).\n"
) + "## Madrid\n\n" + t1 + "\n## Ciudades\n\n" + t2

if __name__ == "__main__":
    (BASE / "scripts" / "tablas_tanda10.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
    for s, t in md.items():
        (BASE / "calculos" / f"{s}.md").write_text(t, encoding="utf-8")
    for k, t in tablas.items():
        print(k)
        for r in t["rows"]:
            print("   ", " | ".join(r))
    for s in md:
        print("\n".join(l for l in md[s].splitlines() if l.startswith("- ") and ("Máxima" in l or "Península" in l or "Madrid:" in l or "Valle" in l or "Coste de 100" in l)))
