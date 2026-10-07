"""Cálculos de las páginas de comunidad, tanda A: Andalucía, Cataluña, Comunidad de Madrid y Comunitat Valenciana.

Mismos criterios que «Luz en Aragón» y «Placas solares en casa»:
- Zonas climáticas: CTE DB-HE (2019), tabla a del anejo B, leída del PDF oficial con sus rangos de altitud
  (fuentes/comunidades-a/cte_zonas.json, comprobado con las tres provincias de Aragón ya publicadas).
- Agua fría de red y altitud de cada capital: CTE DB-HE, tabla a del anejo G (fuentes/tanda7/cte_dbhe.txt).
- Agua caliente: 3 personas × 28 l/día a 60 °C (CTE HE4); energía = l × 4,186 × (60 − T) / 3.600; sin pérdidas.
- Placas: PVGIS 5.2, 1 kWp, 30° sur, 14 % de pérdidas (fuentes/comunidades-a/pvgis/); casa de 3.000 kWh al año,
  3 kWp, 40 % de la producción usada al momento y excedentes compensados a 0,06 €/kWh sin impuestos, con el tope
  mensual del RD 244/2019 (igual que el artículo de placas solares).
Genera calculos/luz-en-<comunidad>.md y scripts/tablas_comunidades_a.json.
"""
import json, re
from pathlib import Path
from calculos import PRECIO, DIAS_MES, FACTOR_IMP, REF, eur, num, cabecera

BASE = Path(__file__).resolve().parent.parent
F = BASE / "fuentes" / "comunidades-a"
ZONAS = json.loads((F / "cte_zonas.json").read_text())
CTE = (BASE / "fuentes" / "tanda7" / "cte_dbhe.txt").read_text()
PERS, LITROS, T_ACS, CP = 3, 28, 60, 4.186
KWP, CONSUMO_MES, DIRECTO, P_COMP = 3, 250.0, 0.40, 0.06
tablas, md = {}, {}

REGIONES = {
    "andalucia": ("Andalucía", [("Almería", "Almería", "almeria"), ("Cádiz", "Cádiz", "cadiz"), ("Córdoba", "Córdoba", "cordoba"),
                                ("Granada", "Granada", "granada"), ("Huelva", "Huelva", "huelva"), ("Jaén", "Jaén", "jaen"),
                                ("Málaga", "Málaga", "malaga"), ("Sevilla", "Sevilla", "sevilla")]),
    "cataluna": ("Cataluña", [("Barcelona", "Barcelona", "barcelona"), ("Girona", "Girona", "girona"),
                              ("Lleida", "Lleida", "lleida"), ("Tarragona", "Tarragona", "tarragona")]),
    "madrid": ("Comunidad de Madrid", [("Madrid", "Madrid", "madrid")]),
    "comunidad-valenciana": ("Comunitat Valenciana", [("Alicante/Alacant", "Alicante", "alicante"), ("Castellón/Castelló", "Castellón", "castellon"),
                                                      ("Valencia/València", "Valencia", "valencia")]),
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


def simula(meses):
    ahorro = comp = 0.0
    for e in meses:
        prod = e * KWP
        a = min(prod * DIRECTO, CONSUMO_MES)
        x = prod - a
        c = min(x * P_COMP, (CONSUMO_MES - a) * REF["energia"])
        ahorro += a * PRECIO
        comp += c * FACTOR_IMP
    return ahorro + comp


for slug, (nombre, provs) in REGIONES.items():
    r_z, r_a, r_s = [], [], []
    for prov, cap, pv in provs:
        alt, t = agua(prov if prov != "Valencia/València" else "Valencia")
        r_z.append([prov.split("/")[0], f"{cap}, {num(alt, 0)} m", zona_de(prov, alt), rangos(prov)])
        ene, jul = acs_dia(t[0]), acs_dia(t[6])
        ano = sum(acs_dia(x) * DIAS_MES for x in t)
        r_a.append([cap, f"{t[0]} °C", f"{t[6]} °C", eur(ene * DIAS_MES * PRECIO), eur(jul * DIAS_MES * PRECIO), eur(ano * PRECIO)])
        art = BASE / "fuentes" / f"pvgis_{pv}.json"  # misma consulta que el artículo de placas solares, si existe
        d = json.loads((art if art.exists() else F / "pvgis" / f"{pv}.json").read_text())
        anual = d["outputs"]["totals"]["fixed"]["E_y"]
        meses = [m["E_m"] for m in d["outputs"]["monthly"]["fixed"]]
        r_s.append([cap, num(anual, 0), num(anual * KWP, 0), eur(anual * KWP * PRECIO), eur(simula(meses))])
    k = slug.replace("-", "_")
    t1 = tabla(f"{k}_zonas", ["Provincia", "Capital y altitud (CTE)", "Zona de la capital", "Zonas según la altitud del municipio"], r_z)
    t2 = tabla(f"{k}_acs", ["Capital", "Agua fría en enero", "Agua fría en julio", "Coste en enero", "Coste en julio", "Coste al año"], r_a)
    t3 = tabla(f"{k}_solar", ["Capital", "kWh al año por kWp", "Producción de 3 kWp", f"Esa producción a {num(PRECIO, 3)} €/kWh", "Ahorro al año (3 kWp, 40 %)"], r_s)
    md[f"luz-en-{slug}"] = cabecera(
        f"luz en {nombre}",
        f"- Agua caliente: {PERS} personas × {LITROS} l/día a {T_ACS} °C (CTE HE4); energía = l × {num(CP, 3)} × (60 − T agua fría) / 3.600; sin pérdidas; año = 12 meses de 30,4 días.\n"
        "- Zonas: CTE DB-HE, anejo B, tabla a; altitud y agua fría de la capital: anejo G.\n"
        f"- Placas: PVGIS 5.2, 1 kWp, 30° sur, 14 % de pérdidas; casa de {num(CONSUMO_MES * 12, 0)} kWh/año, {KWP} kWp, {num(DIRECTO * 100, 0)} % al momento, "
        f"excedentes a {num(P_COMP, 2)} €/kWh sin impuestos × {num(FACTOR_IMP, 3)} con el tope mensual del RD 244/2019 (como en «Placas solares en casa»).\n"
    ) + "## Zonas\n\n" + t1 + "\n## Agua caliente\n\n" + t2 + "\n## Placas\n\n" + t3

DONDE = {  # trámites y organismos, de las fuentes oficiales de fuentes/comunidades-a/
    "andalucia": [
        ["Avisar de una avería o un corte", "Tu distribuidora", "Teléfono gratuito de 24 horas que figura en tu factura"],
        ["Registrar el boletín de una vivienda", "Junta de Andalucía, aplicación TECI", "Lo presenta la empresa instaladora; si la obra necesita proyecto, por PUES"],
        ["Registrar placas de hasta 10 kW", "Junta de Andalucía, aplicación PUES", "Lo presenta la empresa instaladora"],
        ["Dudas y reclamaciones de consumo", "Consumo Responde", "Teléfono gratuito 900 215 080"],
        ["Reclamar si la compañía no te da la razón", "Junta Arbitral de Consumo de Andalucía", "Arbitraje gratuito"],
    ],
    "cataluna": [
        ["Avisar de una avería o un corte", "Tu distribuidora", "Teléfono gratuito de 24 horas que figura en tu factura"],
        ["Registrar el boletín, ampliar la instalación o cambiar el titular", "Generalitat, trámite 11428 en Canal Empresa", "Declaración responsable, solo en línea"],
        ["Dudas y reclamaciones de consumo", "Agència Catalana del Consum", "Oficinas de consumo y web de la Agència"],
        ["Reclamar si la compañía no te da la razón", "Junta Arbitral de Consum de Catalunya", "Arbitraje gratuito y voluntario"],
    ],
    "madrid": [
        ["Avisar de una avería o un corte", "Tu distribuidora", "Teléfono gratuito de 24 horas que figura en tu factura"],
        ["Registrar el boletín de una instalación", "Una Entidad de Inspección y Control Industrial (EICI)", "La tramita la empresa instaladora (Orden 9344/2003)"],
        ["Reclamar por lecturas, contador o acceso a la red", "Comunidad de Madrid, área de industria", "Reclamaciones técnicas sobre el suministro"],
        ["Reclamar si la compañía no te da la razón", "Junta Arbitral de Consumo de la Comunidad de Madrid", "Arbitraje gratuito; en línea o en Ramírez de Prado 5 bis"],
    ],
    "comunidad-valenciana": [
        ["Avisar de una avería o un corte", "Tu distribuidora", "Teléfono gratuito de 24 horas que figura en tu factura"],
        ["Registrar el boletín de una instalación nueva", "Generalitat Valenciana, trámite 436", "Lo presenta la empresa instaladora"],
        ["Saber si tu instalación está registrada", "Portal de Industria de la Generalitat", "Búsqueda por CUPS o por dirección"],
        ["Pedir una copia de tu boletín", "Generalitat Valenciana, trámite 22198", "Duplicado del certificado de instalación"],
        ["Reclamar si la compañía no te da la razón", "Junta Arbitral de Consumo de la Comunitat Valenciana", "Arbitraje gratuito, en línea (trámite 2290)"],
    ],
}
for slug, filas in DONDE.items():
    t = tabla(f"{slug.replace('-', '_')}_donde", ["Para…", "Dónde", "Cómo"], filas)
    md[f"luz-en-{slug}"] += "\n## Dónde\n\n" + t

if __name__ == "__main__":
    (BASE / "scripts" / "tablas_comunidades_a.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
    for s, t in md.items():
        (BASE / "calculos" / f"{s}.md").write_text(t, encoding="utf-8")
    for k, t in tablas.items():
        print(k)
        for r in t["rows"]:
            print("   ", " | ".join(r))
