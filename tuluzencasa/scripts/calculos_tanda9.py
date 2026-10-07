"""Cálculos de la tanda 2 del plan (tanda 9 de la web): cambiar la potencia, alta de luz, cambio de titular
y compensación de excedentes.

Fuentes (consultadas el 7/10/2026, textos en fuentes/tanda9/ y fuentes/tanda7/):
- Orden ITC/3519/2009, anexo V (BOE-A-2009-21173, texto consolidado, sin derogar): baja tensión,
  extensión 17,374714 €/kW, acceso 19,703137 €/kW, enganche 9,044760 €, verificación 8,011716 €.
- RD 1048/2013, arts. 25, 28 y 29 (cuándo se pagan); RD 88/2026, arts. 31, 38 y 39; RD 1955/2000, arts. 103 y 105.6.
- RD 244/2019, arts. 4 y 14 (compensación simplificada, tope mensual).
- Potencia: 0,09 €/kW y día con impuesto eléctrico e IVA, por 365 días, igual que «Qué potencia contratar».
- Los derechos de acometida llevan IVA (21 %), no impuesto eléctrico.
Genera calculos/<slug>.md y scripts/tablas_tanda9.json.
"""
import json
from pathlib import Path
from calculos import PRECIO, DIAS_MES, FACTOR_IMP, REF, eur, num, cabecera

BASE = Path(__file__).resolve().parent.parent
EXT, ACC, ENG, VER = 17.374714, 19.703137, 9.044760, 8.011716
IVA = 1 + REF["iva"]
IMP_POT = (1 + REF["iva"]) * (1 + REF["impuesto_electrico"])
KW_ANO = REF["pot_dia"] * 365 * IMP_POT
tablas, md = {}, {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def kw(x):
    return num(x, 2) + " kW"


# ------------------------------------------------------------------ 1. cambiar la potencia
rows = []
for de, a in ((3.45, 4.6), (4.6, 5.75), (5.75, 6.9), (3.45, 5.75)):
    d = a - de
    ext, acc = EXT * d, ACC * d
    con = (ext + acc + ENG) * IVA
    sin_ext = (acc + ENG) * IVA
    rows.append([f"De {kw(de)} a {kw(a)}", eur(ext), eur(acc), eur(ENG), eur(con), eur(sin_ext)])
t1 = tabla("cp_subir", ["Subida", "Extensión", "Acceso", "Enganche", "Total con IVA", "Total con IVA si ya tienes la extensión"], rows)
rows = []
for de, a in ((5.75, 4.6), (4.6, 3.45), (6.9, 5.75)):
    ah = (de - a) * KW_ANO
    rows.append([f"De {kw(de)} a {kw(a)}", eur(ENG * IVA), eur(ah / 12), eur(ah)])
t2 = tabla("cp_bajar", ["Bajada", "Coste máximo (enganche, con IVA)", "Ahorro al mes", "Ahorro al año"], rows)
md["cambiar-potencia-contratada"] = cabecera(
    "cambiar la potencia contratada",
    f"- Orden ITC/3519/2009, anexo V: extensión {num(EXT, 6)} €/kW, acceso {num(ACC, 6)} €/kW, enganche {num(ENG, 6)} €; + IVA {num(REF['iva'] * 100, 0)} %.\n"
    f"- Ahorro de bajar: kW de menos × {num(REF['pot_dia'], 2)} €/kW·día × 365 × {num(IMP_POT, 4)} = {eur(KW_ANO)} por kW y año (igual que «Qué potencia contratar»).\n"
    f"- Verificación ({num(VER, 6)} €) solo si el contrato tiene más de 20 años (RD 88/2026, art. 38.7): {eur(VER * IVA)} con IVA.\n"
) + "## Subir\n\n" + t1 + "\n## Bajar\n\n" + t2

# ------------------------------------------------------------------ 2. alta de luz
rows = []
for p in (3.45, 4.6, 5.75, 6.9, 9.2):
    base = (EXT + ACC) * p + ENG
    rows.append([kw(p), eur(EXT * p), eur(ACC * p), eur(ENG), eur(VER), eur(base * IVA), eur((base + VER) * IVA)])
t1 = tabla("al_derechos", ["Potencia", "Extensión", "Acceso", "Enganche", "Verificación", "Total con IVA", "Total con IVA y verificación"], rows)
t2 = tabla("al_plazos", ["Paso", "Plazo máximo de la distribuidora", "Norma"], [
    ["Darte las condiciones técnicas y económicas (hasta 15 kW, sin obras de extensión)", "5 días hábiles", "RD 1955/2000, art. 103.2.A"],
    ["Ídem, cuando no hace falta centro de transformación", "10 días hábiles", "RD 1955/2000, art. 103.2.A"],
    ["Hacer la conexión si no hay que ampliar la red de baja tensión", "5 días hábiles desde que pagas", "RD 1955/2000, art. 103.2.B"],
    ["Hacer la conexión si hay que ampliar la red de baja tensión", "30 días hábiles", "RD 1955/2000, art. 103.2.B"],
    ["Hacer la conexión si hace falta un centro de transformación", "60 días hábiles", "RD 1955/2000, art. 103.2.B"],
    ["Enganchar e instalar el contador", "5 días hábiles desde el contrato", "RD 1955/2000, art. 103.2.C"],
])
md["alta-luz-vivienda"] = cabecera(
    "alta de luz en una vivienda",
    "- Orden ITC/3519/2009, anexo V (baja tensión) + IVA. Extensión solo si la distribuidora hace la extensión en suelo urbanizado "
    "(RD 1048/2013, art. 25.1); vigente 3 años tras la baja (art. 28.1). Verificación solo si no hubo proyecto (art. 29.1).\n"
    f"- Incumplimiento de plazos: la mayor de 30,050605 € ({eur(30.050605)}) o el 10 % de la primera factura (RD 1955/2000, art. 105.6).\n"
) + "## Derechos\n\n" + t1 + "\n## Plazos\n\n" + t2

# ------------------------------------------------------------------ 3. cambio de titular
t1 = tabla("ct_casos", ["Tu situación", "Qué haces", "Qué cuesta"], [
    ["Compras o heredas una vivienda con luz", "Cambio de titular con la comercializadora, presentando tu título", "0 € por el contrato nuevo"],
    ["Alquilas una vivienda y quieres la luz a tu nombre", "Cambio de titular; no es una baja y un alta nueva", "0 €"],
    ["El contrato tiene más de 20 años", "Cambio de titular sin boletín nuevo ni verificación, si no cambias la potencia ni el peaje", "0 €"],
    ["Además quieres subir la potencia", "Cambio de titular y, aparte, modificación de potencia", "Derechos de extensión y acceso de los kW de más"],
    ["El titular anterior tenía bono social", "El bono no pasa al nuevo titular: hay que pedirlo de nuevo", "0 €"],
])
md["cambio-titular-luz"] = cabecera(
    "cambio de titular de la luz",
    "- RD 88/2026, art. 31 (PVPC) y art. 39 (acceso a la red): sin coste por el nuevo contrato (31.5 y 39.5); el usuario con justo título "
    "puede cambiarlo a su nombre (31.3 y 39.3); más de 20 años sin boletín (39.6); el bono social no se traspasa (31.1).\n"
    "- Sin cálculos de precio de la energía.\n"
) + "## Casos\n\n" + t1

# ------------------------------------------------------------------ 4. compensación de excedentes
d = json.loads((BASE / "fuentes" / "pvgis_madrid.json").read_text())
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
KWP, CONSUMO_MES, DIRECTO, PC = 3, 250.0, 0.40, 0.06
rows, tot = [], dict(prod=0, auto=0, exc=0, comp=0, perdido=0, tope=0)
for i, m in enumerate(d["outputs"]["monthly"]["fixed"]):
    prod = m["E_m"] * KWP
    a = min(prod * DIRECTO, CONSUMO_MES)
    x = prod - a
    red = CONSUMO_MES - a
    valor = x * PC
    tope = red * REF["energia"]
    c = min(valor, tope)
    perdido = valor - c
    tot["prod"] += prod; tot["auto"] += a; tot["exc"] += x; tot["comp"] += c * FACTOR_IMP; tot["perdido"] += perdido * FACTOR_IMP
    rows.append([MESES[i], num(prod, 0) + " kWh", num(x, 0) + " kWh", eur(c * FACTOR_IMP), eur(perdido * FACTOR_IMP)])
rows.append(["Año", num(tot["prod"], 0) + " kWh", num(tot["exc"], 0) + " kWh", eur(tot["comp"]), eur(tot["perdido"])])
t1 = tabla("ex_meses", ["Mes (Madrid, 3 kWp)", "Producción", "Excedentes", "Compensación en la factura", "Excedentes que no se compensan"], rows)
rows = []
for pc in (0.04, 0.06, 0.08):
    comp = per = 0.0
    for m in d["outputs"]["monthly"]["fixed"]:
        prod = m["E_m"] * KWP
        a = min(prod * DIRECTO, CONSUMO_MES)
        x = prod - a
        c = min(x * pc, (CONSUMO_MES - a) * REF["energia"])
        comp += c * FACTOR_IMP; per += (x * pc - c) * FACTOR_IMP
    rows.append([num(pc, 2) + " €/kWh", eur(comp), eur(per)])
t2 = tabla("ex_precio", ["Precio de los excedentes (sin impuestos)", "Compensación al año", "Lo que se queda sin compensar al año"], rows)
sol, todo = [], []
for f in sorted((BASE / "fuentes" / "tanda8" / "omie").glob("marginalpdbc_*.1")):
    if not ("20251001" <= f.name[13:21] <= "20260930"):
        continue
    filas = [l.split(";") for l in f.read_text(encoding="latin-1").splitlines() if l[:1].isdigit()]
    for r in filas:
        h = (int(r[3]) - 1) * 24 / len(filas)
        todo.append(float(r[5]))
        if 11 <= h < 16:
            sol.append(float(r[5]))
OMIE_SOL, OMIE_TODO = sum(sol) / len(sol), sum(todo) / len(todo)
md["compensacion-excedentes-placas"] = cabecera(
    "compensación de excedentes",
    f"- PVGIS 5.2, Madrid, 1 kWp a 30° sur, 14 % de pérdidas (fuentes/pvgis_madrid.json), × {KWP} kWp; casa de {num(CONSUMO_MES * 12, 0)} kWh/año, "
    f"{num(DIRECTO * 100, 0)} % de la producción al momento (como «Placas solares en casa»).\n"
    f"- Compensación mensual = mín(excedentes × precio, energía de la red × {num(REF['energia'], 2)} €/kWh) (RD 244/2019, art. 14.3); "
    f"se descuenta antes de impuestos, × {num(FACTOR_IMP, 3)}.\n"
    "- «No compensado»: valor de los excedentes por encima del tope, con impuestos; es lo que un saldo acumulable podría guardar.\n"
    f"- OMIE, mercado diario, oct. 2025 – sep. 2026: media de 11 a 16 h {num(OMIE_SOL, 2)} €/MWh; media de todas las horas {num(OMIE_TODO, 2)} €/MWh.\n"
) + "## Meses\n\n" + t1 + "\n## Precio\n\n" + t2

if __name__ == "__main__":
    (BASE / "scripts" / "tablas_tanda9.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
    for s, t in md.items():
        (BASE / "calculos" / f"{s}.md").write_text(t, encoding="utf-8")
    for k, t in tablas.items():
        print(k)
        for r in t["rows"]:
            print("   ", " | ".join(r))
