"""Cálculos de las páginas de comunidad, tanda B: Galicia, Castilla y León, País Vasco y Canarias.

Mismos criterios que «Luz en Aragón» y «Placas solares en casa»:
- Zonas climáticas: CTE DB-HE (2019), tabla a del anejo B, leída del PDF oficial con sus rangos de altitud
  (fuentes/comunidades-a/cte_zonas.json; las provincias de la tanda B se leyeron con fuentes/comunidades-a/cte_zonas_b.py,
  que antes comprueba que reproduce las 19 ya usadas).
- Agua fría de red y altitud de cada capital: CTE DB-HE, tabla a del anejo G (fuentes/tanda7/cte_dbhe.txt).
- Agua caliente: 3 personas × 28 l/día a 60 °C (CTE HE4); energía = l × 4,186 × (60 − T) / 3.600; sin pérdidas.
- Placas: PVGIS 5.2, 1 kWp, 30° sur, 14 % de pérdidas (fuentes/comunidades-a/pvgis/); casa de 3.000 kWh al año,
  3 kWp, 40 % de la producción usada al momento y excedentes compensados a 0,06 €/kWh sin impuestos, con el tope
  mensual del RD 244/2019 (igual que el artículo de placas solares).
- Canarias: IGIC 0 % en la luz de la vivienda con 10 kW o menos (Ley 4/2012 de Canarias, art. 52.r) e impuesto eléctrico
  como en toda España (Ley 38/1992, art. 91): precio = energía × (1 + impuesto eléctrico), sin IVA.
Genera calculos/luz-en-<comunidad>.md y scripts/tablas_comunidades_b.json.
"""
import json, re
from pathlib import Path
from calculos import PRECIO, DIAS_MES, FACTOR_IMP, REF, eur, num, pr, cabecera

BASE = Path(__file__).resolve().parent.parent
F = BASE / "fuentes" / "comunidades-a"
PRECIO_CAN = REF["energia"] * (1 + REF["impuesto_electrico"])  # Canarias: sin IVA ni IGIC
FACTOR_CAN = 1 + REF["impuesto_electrico"]
NOMBRE_CAP = {"Bilbao/Bilbo": "Bilbao", "Vitoria-Gasteiz": "Vitoria-Gasteiz", "Las Palmas de Gran Canaria": "Las Palmas de G. C."}
ZONAS = json.loads((F / "cte_zonas.json").read_text())
CTE = (BASE / "fuentes" / "tanda7" / "cte_dbhe.txt").read_text()
PERS, LITROS, T_ACS, CP = 3, 28, 60, 4.186
KWP, CONSUMO_MES, DIRECTO, P_COMP = 3, 250.0, 0.40, 0.06
tablas, md = {}, {}

REGIONES = {  # provincia (tabla de zonas del CTE), capital (anejo G), archivo PVGIS
    "galicia": ("Galicia", [("A Coruña", "A Coruña", "a-coruna"), ("Lugo", "Lugo", "lugo"), ("Ourense", "Ourense", "ourense"),
                            ("Pontevedra", "Pontevedra", "pontevedra")]),
    "castilla-y-leon": ("Castilla y León", [("Ávila", "Ávila", "avila"), ("Burgos", "Burgos", "burgos"), ("León", "León", "leon"),
                                            ("Palencia", "Palencia", "palencia"), ("Salamanca", "Salamanca", "salamanca"),
                                            ("Segovia", "Segovia", "segovia"), ("Soria", "Soria", "soria"),
                                            ("Valladolid", "Valladolid", "valladolid"), ("Zamora", "Zamora", "zamora")]),
    "pais-vasco": ("País Vasco", [("Araba/Álava", "Vitoria-Gasteiz", "vitoria"), ("Bizkaia", "Bilbao/Bilbo", "bilbao"),
                                  ("Gipuzkoa", "San Sebastián", "san-sebastian")]),
    "canarias": ("Canarias", [("Las Palmas", "Las Palmas de Gran Canaria", "las-palmas"),
                              ("Santa Cruz de Tenerife", "Santa Cruz de Tenerife", "santa-cruz-tenerife")]),
}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def agua(capital_cte):
    m = re.search(rf"^{re.escape(capital_cte)} ((?:\d+ ){{12}}\d+) ?$", CTE, re.M)
    v = [int(x) for x in m.group(1).split()]
    return v[0], v[1:]


def zona_de(prov, alt):
    for z in ZONAS[prov]:
        if z["desde"] <= alt <= (z["hasta"] or 99999):
            return z["zona"]


def rangos(prov):
    zs = ZONAS[prov]
    if len(zs) == 1:
        return f"{zs[0]['zona']} en toda la provincia"
    out = []
    for i, z in enumerate(zs):
        if i == 0:
            out.append(f"{z['zona']} hasta {num(z['hasta'], 0)} m")
        elif z["hasta"] is None:
            out.append(f"{z['zona']} por encima de {num(z['desde'] - 1, 0)} m")
        else:
            out.append(f"{z['zona']} de {num(z['desde'], 0)} a {num(z['hasta'], 0)} m")
    return " · ".join(out)


def acs_dia(tf):
    return PERS * LITROS * CP * (T_ACS - tf) / 3600


def simula(meses, precio=PRECIO, factor=FACTOR_IMP):
    ahorro = comp = 0.0
    for e in meses:
        prod = e * KWP
        a = min(prod * DIRECTO, CONSUMO_MES)
        x = prod - a
        c = min(x * P_COMP, (CONSUMO_MES - a) * REF["energia"])
        ahorro += a * precio
        comp += c * factor
    return ahorro + comp


for slug, (nombre, provs) in REGIONES.items():
    precio, factor = (PRECIO_CAN, FACTOR_CAN) if slug == "canarias" else (PRECIO, FACTOR_IMP)
    r_z, r_a, r_s = [], [], []
    for prov, cap, pv in provs:
        alt, t = agua(cap)
        cn = NOMBRE_CAP.get(cap, cap)
        r_z.append([prov.split("/")[0] if prov != "Araba/Álava" else "Álava", f"{cn}, {num(alt, 0)} m", zona_de(prov, alt), rangos(prov)])
        ene, jul = acs_dia(t[0]), acs_dia(t[6])
        ano = sum(acs_dia(x) * DIAS_MES for x in t)
        r_a.append([cn, f"{t[0]} °C", f"{t[6]} °C", eur(ene * DIAS_MES * precio), eur(jul * DIAS_MES * precio), eur(ano * precio)])
        art = BASE / "fuentes" / f"pvgis_{pv}.json"  # misma consulta que el artículo de placas solares, si existe
        d = json.loads((art if art.exists() else F / "pvgis" / f"{pv}.json").read_text())
        anual = d["outputs"]["totals"]["fixed"]["E_y"]
        meses = [m["E_m"] for m in d["outputs"]["monthly"]["fixed"]]
        r_s.append([cn, num(anual, 0), num(anual * KWP, 0), eur(anual * KWP * precio), eur(simula(meses, precio, factor))])
    k = slug.replace("-", "_")
    t1 = tabla(f"{k}_zonas", ["Provincia", "Capital y altitud (CTE)", "Zona de la capital", "Zonas según la altitud del municipio"], r_z)
    t2 = tabla(f"{k}_acs", ["Capital", "Agua fría en enero", "Agua fría en julio", "Coste en enero", "Coste en julio", "Coste al año"], r_a)
    t3 = tabla(f"{k}_solar", ["Capital", "kWh al año por kWp", "Producción de 3 kWp", f"Esa producción a {num(precio, 3)} €/kWh", "Ahorro al año (3 kWp, 40 %)"], r_s)
    extra = ""
    if slug == "canarias":
        extra = (f"- Canarias: {pr(REF['energia'])} €/kWh × (1 + {num(REF['impuesto_electrico'] * 100, 2)} % de impuesto eléctrico), sin IVA y con IGIC 0 % "
                 f"= **{num(precio, 3)} €/kWh** (frente a {num(PRECIO, 3)} en la península); factor {num(factor, 4)}.\n"
                 f"- Diferencia: {num((1 - factor / FACTOR_IMP) * 100, 1)} % menos por kWh; con la casa de 3.000 kWh al año, "
                 f"{eur(3000 * PRECIO)} frente a {eur(3000 * precio)} de energía ({eur(3000 * (PRECIO - precio))} menos).\n")
    md[f"luz-en-{slug}"] = cabecera(
        f"luz en {nombre}",
        extra +
        f"- Agua caliente: {PERS} personas × {LITROS} l/día a {T_ACS} °C (CTE HE4); energía = l × {num(CP, 3)} × (60 − T agua fría) / 3.600; sin pérdidas; año = 12 meses de 30,4 días.\n"
        "- Zonas: CTE DB-HE, anejo B, tabla a; altitud y agua fría de la capital: anejo G.\n"
        f"- Placas: PVGIS 5.2, 1 kWp, 30° sur, 14 % de pérdidas; casa de {num(CONSUMO_MES * 12, 0)} kWh/año, {KWP} kWp, {num(DIRECTO * 100, 0)} % al momento, "
        f"excedentes a {num(P_COMP, 2)} €/kWh sin impuestos × {num(factor, 3)} con el tope mensual del RD 244/2019 (como en «Placas solares en casa»).\n"
    ) + "## Zonas\n\n" + t1 + "\n## Agua caliente\n\n" + t2 + "\n## Placas\n\n" + t3

DONDE = {  # trámites y organismos, de las fuentes oficiales de fuentes/comunidades-b/ (consultadas el 12-10-2026)
    "galicia": [
        ["Avisar de una avería o un corte", "Tu distribuidora", "Teléfono gratuito de 24 horas que figura en tu factura"],
        ["Registrar el boletín de una instalación nueva", "Xunta de Galicia, procedimiento IN614C", "Lo presenta la empresa instaladora; el justificante sirve para pedir el suministro"],
        ["Registrar placas de autoconsumo de menos de 100 kW", "Xunta de Galicia, procedimiento IN407B", "Comunicación electrónica y gratuita"],
        ["Reclamar si la compañía no te da la razón", "Xunta Arbitral de Consumo de Galicia", "Antes, reclama a la empresa; tienes un año desde esa reclamación"],
    ],
    "castilla-y-leon": [
        ["Avisar de una avería o un corte", "Tu distribuidora", "Teléfono gratuito de 24 horas que figura en tu factura"],
        ["Registrar el boletín de una instalación", "Junta de Castilla y León, Registro de Instalaciones Eléctricas de Baja Tensión", "Lo presenta el instalador; por internet si no necesita proyecto"],
        ["Reclamar si la compañía no te da la razón", "Junta Arbitral de Consumo de Castilla y León", "Solicitud en la sede electrónica; laudo en 90 días naturales desde el inicio"],
    ],
    "pais-vasco": [
        ["Avisar de una avería o un corte", "Tu distribuidora", "Teléfono gratuito de 24 horas que figura en tu factura"],
        ["Poner en servicio una instalación nueva", "Gobierno Vasco, delegación territorial de Administración Industrial", "Declaración responsable; el titular guarda el boletín y la memoria"],
        ["Comunicar la baja o el cambio de titular de la instalación", "Gobierno Vasco, «otras comunicaciones» de baja tensión", "Con el documento que justifica el cambio"],
        ["Reclamar si la compañía no te da la razón", "Junta Arbitral de Consumo de Euskadi (Kontsumobide)", "Avenida Santiago, 11, Vitoria-Gasteiz; laudo en 90 días como máximo"],
    ],
    "canarias": [
        ["Avisar de una avería o un corte", "Tu distribuidora", "Teléfono gratuito de 24 horas que figura en tu factura"],
        ["Poner en servicio una instalación nueva", "Gobierno de Canarias, comunicación previa (trámite 3158)", "Por internet; basta el certificado de instalación diligenciado"],
        ["Añadir placas a una vivienda que ya tiene luz", "Gobierno de Canarias, trámite 6782", "Comunicación de modificación de la instalación"],
        ["Reclamar si la compañía no te da la razón", "Junta Arbitral de Consumo de Canarias", "Sedes en Las Palmas de Gran Canaria y Santa Cruz de Tenerife"],
    ],
}
for slug, filas in DONDE.items():
    t = tabla(f"{slug.replace('-', '_')}_donde", ["Para…", "Dónde", "Cómo"], filas)
    md[f"luz-en-{slug}"] += "\n## Dónde\n\n" + t

if __name__ == "__main__":
    (BASE / "scripts" / "tablas_comunidades_b.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
    for s, t in md.items():
        (BASE / "calculos" / f"{s}.md").write_text(t, encoding="utf-8")
    for k, t in tablas.items():
        print(k)
        for r in t["rows"]:
            print("   ", " | ".join(r))
