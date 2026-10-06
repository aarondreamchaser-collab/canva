"""Cálculos de la tanda 4 de 4: boletín eléctrico, aerotermia, se ha ido la luz y luz en Aragón.

Criterios de CLAUDE.md: 0,165 €/kWh con impuestos; mes de 30,4 días; año de 12 meses (364,8 días); invierno de 4 meses.
Valores de nuestra calculadora de consumo (calculadora.js):
- Termo eléctrico 80 L: 1.500 W, 3 h/día, factor 0,7 -> 3,15 kWh/día.
Fuentes de datos externos (consultadas el 6/10/2026, textos en fuentes/tanda7/):
- REBT (RD 842/2002), ITC-BT-04 (proyecto/memoria), ITC-BT-05 (inspecciones), ITC-BT-10 (5.750 W y 9.200 W),
  ITC-BT-25 (IGA de 25 A como mínimo; la potencia prevista es la del IGA).
- RD 1955/2000, art. 99.4 (zonas), art. 104.2.b (límites de baja tensión), art. 105.3 (descuentos).
- RD 88/2026, arts. 38.7, 39.6 y 51.4 (contratos de más de 20 años), art. 6 y art. 55 (reclamaciones).
- Reglamento Delegado (UE) 811/2013, anexo II, cuadros 1 y 2 (clases a 55 °C y a 35 °C).
- Reglamento (UE) 813/2013, anexo II (mínimos desde el 26/9/2017: 110 % y 125 %).
- CTE DB-HE (2019): anejo B (zonas climáticas), anejo G (agua fría de red), HE4 (28 l/día·persona a 60 °C).
Genera calculos/<slug>.md y scripts/tablas_tanda7.json.
"""
import json
from pathlib import Path
from calculos import PRECIO, DIAS_MES, eur, num, cabecera

BASE = Path(__file__).resolve().parent.parent
DIAS_ANO = DIAS_MES * 12
tablas, md = {}, {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def kwh(x, d=2):
    return num(x, d) + " kWh"


# ------------------------------------------------------------------ 1. boletín eléctrico
t1 = tabla("boletin_cuando", ["Lo que quieres hacer", "¿Te piden boletín?", "Lo que dice la norma"], [
    ["Dar de alta la luz en una vivienda nueva", "Sí", "La distribuidora no puede conectar sin el certificado registrado (REBT, art. 18.3)"],
    ["Reformar la instalación: circuitos nuevos, ampliación o cambio del cuadro", "Sí, uno nuevo", "Toda ampliación o modificación lleva certificado (ITC-BT-04)"],
    ["Cambiar el contrato a tu nombre sin tocar nada", "No", "RD 88/2026, art. 39.6, también con más de 20 años"],
    ["Bajar la potencia contratada", "No", "Solo se pide si hay obra en la instalación"],
    ["Subir la potencia sin pasar de la que admite tu boletín", "No, si el contrato tiene 20 años o menos", "La potencia contratada debe quedar por debajo de la del boletín"],
    ["Subir la potencia con un contrato de más de 20 años", "La distribuidora revisa la instalación", "Si no cumple, exige adaptarla y un boletín nuevo (RD 88/2026, art. 38.7)"],
    ["Subir por encima de la potencia que admite tu boletín", "Sí, uno nuevo", "Hace falta adaptar la instalación a la nueva potencia"],
])
rows = []
for amp in (25, 32, 40, 50, 63):
    rows.append([f"{amp} A", num(230 * amp / 1000, 2) + " kW",
                 {25: "Mínimo para cualquier vivienda nueva (electrificación básica)",
                  40: "Mínimo para electrificación elevada"}.get(amp, "")])
t2 = tabla("boletin_iga", ["Interruptor general (IGA)", "Potencia máxima de la instalación", "Qué dice el reglamento"], rows)
t3 = tabla("boletin_documentacion", ["Instalación", "Documentación técnica", "Inspección de un organismo de control"], [
    ["Vivienda en un piso", "Memoria técnica de diseño", "No"],
    ["Vivienda unifamiliar de hasta 50 kW", "Memoria técnica de diseño", "No"],
    ["Vivienda unifamiliar de más de 50 kW", "Proyecto de un técnico titulado", "No"],
    ["Edificio de viviendas de más de 100 kW por caja general de protección", "Proyecto de un técnico titulado", "Zonas comunes de más de 100 kW: cada 10 años"],
    ["Local de pública concurrencia", "Proyecto de un técnico titulado", "Inicial y cada 5 años"],
])
md["boletin-electrico"] = cabecera(
    "boletín eléctrico",
    "- Potencia máxima = 230 V × intensidad del IGA (ITC-BT-10 y ITC-BT-25).\n")
md["boletin-electrico"] += "## Cuándo\n\n" + t1 + "\n## IGA\n\n" + t2 + "\n## Documentación\n\n" + t3

# ------------------------------------------------------------------ 2. aerotermia
INV = 4  # meses de invierno
rows = []
for q in (500, 1000, 1500):
    rad = q * PRECIO
    s3 = q / 3 * PRECIO
    s4 = q / 4 * PRECIO
    rows.append([kwh(q, 0), eur(rad), eur(s3), eur(s4), eur((rad - s3) * INV)])
t1 = tabla("aero_calefaccion", ["Calor que necesita la casa al mes", "Con radiadores eléctricos", "Aerotermia con SCOP 3",
                                "Aerotermia con SCOP 4", "Ahorro por invierno con SCOP 3 (4 meses)"], rows)
TERMO = 1.5 * 3 * 0.7
rows = [["Termo eléctrico (nuestra calculadora)", kwh(TERMO), eur(TERMO * DIAS_MES * PRECIO), eur(TERMO * DIAS_ANO * PRECIO)]]
for cop in (2.5, 3):
    k = TERMO / cop
    rows.append([f"Aerotermia para agua caliente, COP {num(cop, 1)}", kwh(k), eur(k * DIAS_MES * PRECIO), eur(k * DIAS_ANO * PRECIO)])
t2 = tabla("aero_acs", ["Agua caliente para la misma familia", "Electricidad al día", "Coste al mes", "Coste al año"], rows)
t3 = tabla("aero_clases", ["Clase", "Radiadores (salida a 55 °C)", "Suelo radiante o fancoils (salida a 35 °C)"], [
    ["A+++", "150 % o más", "175 % o más"],
    ["A++", "125–149 %", "150–174 %"],
    ["A+", "98–124 %", "123–149 %"],
    ["Mínimo para venderse desde 2017", "110 %", "125 %"],
])
md["cuanto-consume-aerotermia"] = cabecera(
    "aerotermia",
    f"- Calefacción: electricidad = calor / SCOP; radiadores eléctricos 1 kWh de calor por kWh. Invierno de {INV} meses.\n"
    f"- Agua caliente: termo de la calculadora {kwh(TERMO)} al día; aerotermia = termo / COP (2,5 y 3, ejemplos).\n"
    f"- Ahorro al año en agua caliente: COP 2,5 {eur(TERMO * (1 - 1 / 2.5) * DIAS_ANO * PRECIO)}; COP 3 {eur(TERMO * (1 - 1 / 3) * DIAS_ANO * PRECIO)}.\n"
    "- Clases: Reglamento Delegado (UE) 811/2013, anexo II; mínimos: Reglamento (UE) 813/2013, anexo II.\n")
md["cuanto-consume-aerotermia"] += "## Calefacción\n\n" + t1 + "\n## Agua caliente\n\n" + t2 + "\n## Clases\n\n" + t3

# ------------------------------------------------------------------ 3. se ha ido la luz
t1 = tabla("corte_limites", ["Zona", "Municipios de la provincia con…", "Horas de corte al año", "Número de cortes al año"], [
    ["Urbana", "más de 20.000 suministros, y todas las capitales de provincia", "5", "10"],
    ["Semiurbana", "entre 2.000 y 20.000 suministros", "9", "13"],
    ["Rural concentrada", "entre 200 y 2.000 suministros", "14", "16"],
    ["Rural dispersa", "menos de 200 suministros, o fuera de los núcleos de población", "19", "22"],
])
rows = []
for pot in (3.45, 4.6, 5.75):
    for exc in (2, 5):
        k = pot * exc * 5
        rows.append([num(pot, 2) + " kW", f"{exc} horas", kwh(k, 1), eur(k * PRECIO)])
t2 = tabla("corte_descuento", ["Potencia", "Horas por encima del límite", "kWh que se descuentan (× 5)", "Referencia a 0,165 €/kWh"], rows)
md["se-ha-ido-la-luz"] = cabecera(
    "se ha ido la luz",
    "- RD 1955/2000, art. 104.2.b: límites individuales en baja tensión. Art. 105.3: descuento = potencia media × horas de "
    "exceso × 5 × precio del kWh, con tope del 10 % de la facturación anual.\n")
md["se-ha-ido-la-luz"] += "## Límites\n\n" + t1 + "\n## Descuento\n\n" + t2

# ------------------------------------------------------------------ 4. luz en Aragón
AGUA = {  # CTE DB-HE, anejo G: altitud y agua fría de red (°C) de enero a diciembre
    "Huesca": (488, [7, 8, 10, 11, 14, 16, 19, 18, 17, 13, 9, 7], "D2"),
    "Teruel": (912, [6, 7, 8, 10, 12, 15, 18, 17, 15, 12, 8, 6], "D2"),
    "Zaragoza": (199, [8, 9, 10, 12, 15, 17, 20, 19, 17, 14, 10, 8], "C3"),
}
PERS, LITROS, T_ACS, CP = 3, 28, 60, 4.186  # personas, l/día·persona a 60 °C (HE4), kJ/(kg·K)


def acs_dia(tf):
    return PERS * LITROS * CP * (T_ACS - tf) / 3600


t1 = tabla("aragon_zonas", ["Capital", "Altitud (CTE)", "Zona climática", "Agua fría en enero", "Agua fría en julio"],
           [[c, f"{a} m", z, f"{t[0]} °C", f"{t[6]} °C"] for c, (a, t, z) in AGUA.items()])
rows = []
for c, (a, t, z) in AGUA.items():
    ene, jul = acs_dia(t[0]), acs_dia(t[6])
    ano = sum(acs_dia(x) * DIAS_MES for x in t)
    rows.append([c, kwh(ene), eur(ene * DIAS_MES * PRECIO), eur(jul * DIAS_MES * PRECIO), eur(ano * PRECIO)])
t2 = tabla("aragon_acs", ["Capital", "Energía al día en enero", "Coste en enero", "Coste en julio", "Coste al año"], rows)
t3 = tabla("aragon_donde", ["Para…", "Dónde", "Cómo"], [
    ["Avisar de una avería o un corte", "Tu distribuidora (casi siempre e-distribución)", "Teléfono gratuito de 24 horas que figura en tu factura"],
    ["Registrar el boletín de una instalación", "Gobierno de Aragón, trámite n.º 26", "Lo presenta la empresa instaladora, por vía electrónica"],
    ["Dudas de seguridad industrial", "Servicio Provincial de Industria", "Huesca 974 293 141 · Teruel 978 641 110 · Zaragoza 976 714 081"],
    ["Reclamar si la empresa no te da la razón", "Junta Arbitral de Consumo de Aragón", "Solicitud de arbitraje, en línea o con cita previa"],
])
md["luz-en-aragon"] = cabecera(
    "luz en Aragón",
    f"- Agua caliente: {PERS} personas × {LITROS} l/día a {T_ACS} °C (CTE HE4); energía = l × {num(CP, 3)} kJ/(kg·K) × (60 − T agua fría) / 3.600.\n"
    "- Sin pérdidas del termo ni de las tuberías: es la energía mínima para calentar el agua. Año = 12 meses de 30,4 días.\n"
    "- Zonas climáticas leídas en la tabla a del anejo B del CTE DB-HE para la altitud de cada capital (anejo G).\n")
md["luz-en-aragon"] += "## Zonas\n\n" + t1 + "\n## Agua caliente\n\n" + t2 + "\n## Dónde\n\n" + t3

if __name__ == "__main__":
    (BASE / "scripts" / "tablas_tanda7.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
    for slug, txt in md.items():
        (BASE / "calculos" / f"{slug}.md").write_text(txt, encoding="utf-8")
    for k, t in tablas.items():
        print(k)
        for r in t["rows"]:
            print("   ", " | ".join(r))
