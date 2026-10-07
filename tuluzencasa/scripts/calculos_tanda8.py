"""Cálculos de la tanda 1 del plan estratégico (tanda 8 de la web) y de la página «Metodología».

Artículos: tarifa fija o indexada, bono social térmico, consumo por horas con Datadis y suelo radiante eléctrico.
Criterios de CLAUDE.md: 0,165 €/kWh con impuestos; mes de 30,4 días; invierno de 4 meses.
Fuentes (consultadas el 7/10/2026, textos en fuentes/tanda8/ y fuentes/tanda7/):
- OMIE, ficheros diarios marginalpdbc (precio marginal del mercado diario, sistema español, €/MWh):
  media simple de todos los periodos del mes (horarios hasta el 30/9/2025, cuartohorarios desde el 1/10/2025).
- RD 88/2026 (arts. 2.j, 6.y, 6.af, 13.n, 17.2, 28.3, 30.1.i y 30.1.w); RD 216/2014 (art. 7, coeficiente B = 0,55).
- RDL 15/2018 (arts. 5–10 y anexo I) y RDL 7/2026 (arts. 1, 2 y 3); RD 897/2017 (art. 6.3).
- Fichas de Danfoss DEVI (máx. 80–200 W/m² según el suelo) y Salvador Escoda (mantas de 60, 120 y 180 W/m²).
Genera calculos/<slug>.md y scripts/tablas_tanda8.json.
"""
import json
from pathlib import Path
from calculos import PRECIO, DIAS_MES, FACTOR_IMP, TRAMOS, REF, eur, num, pr as fpr, cabecera
ENE, POT, CONT = REF["energia"], REF["pot_dia"], REF["contador_mes"]
IEE, IVA = REF["impuesto_electrico"], REF["iva"]

BASE = Path(__file__).resolve().parent.parent
OMIE = BASE / "fuentes" / "tanda8" / "omie"
INV = 4  # meses de invierno
tablas, md = {}, {}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def kwh(x, d=2):
    return num(x, d) + " kWh"


# ------------------------------------------------------------------ OMIE: medias mensuales
precios = {}  # (año, mes) -> lista de precios del sistema español
for f in sorted(OMIE.glob("marginalpdbc_*.1")):
    for line in f.read_text(encoding="latin-1").splitlines():
        c = line.split(";")
        if len(c) >= 6 and c[0].isdigit():
            precios.setdefault((int(c[0]), int(c[1])), []).append(float(c[5]))
media = {k: sum(v) / len(v) for k, v in precios.items()}
ULT12 = [(2025, m) for m in range(10, 13)] + [(2026, m) for m in range(1, 10)]
assert all(k in media for k in ULT12)
dias = {k: len({f.name[13:21] for f in OMIE.glob(f"marginalpdbc_{k[0]}{k[1]:02d}*.1")}) for k in ULT12}


def mes(k):
    return f"{MESES[k[1] - 1].capitalize()} {k[0]}"


# ------------------------------------------------------------------ 1. tarifa fija o indexada
CONS = 250  # kWh al mes, hogar de ejemplo
rows = []
for k in ULT12:
    eurkwh = media[k] / 1000
    rows.append([mes(k), num(media[k], 2) + " €/MWh", num(eurkwh, 3) + " €/kWh", eur(CONS * eurkwh * FACTOR_IMP)])
med12 = sum(media[k] for k in ULT12) / 12
rows.append(["Media de los 12 meses", num(med12, 2) + " €/MWh", num(med12 / 1000, 3) + " €/kWh",
             eur(CONS * med12 / 1000 * FACTOR_IMP)])
t1 = tabla("fi_omie", ["Mes", "Precio medio del mercado diario", "En €/kWh", f"Solo esa parte, para {CONS} kWh al mes, con impuestos"], rows)
barato = min(ULT12, key=lambda k: media[k])
caro = max(ULT12, key=lambda k: media[k])
rows = []
for c in (150, 250, 400):
    lo, hi = c * media[barato] / 1000 * FACTOR_IMP, c * media[caro] / 1000 * FACTOR_IMP
    rows.append([kwh(c, 0), eur(lo), eur(hi), eur(hi - lo)])
t2 = tabla("fi_riesgo", ["Consumo al mes", f"Mes más barato ({mes(barato).lower()})", f"Mes más caro ({mes(caro).lower()})", "Diferencia en un mes"], rows)
SALTO = 50  # €/MWh de subida del mercado
rows = [[kwh(c, 0), eur(c * SALTO / 1000 * FACTOR_IMP), eur(c * SALTO / 1000 * FACTOR_IMP * 12)] for c in (150, 250, 400)]
t3 = tabla("fi_sensibilidad", ["Consumo al mes", f"Si el mercado sube {SALTO} €/MWh: al mes", "Si dura un año entero"], rows)
t4 = tabla("fi_comparar", ["", "Precio fijo (mercado libre)", "Precio indexado (mercado libre)", "PVPC (tarifa regulada)"], [
    ["Precio del kWh", "El mismo durante el contrato", "Sigue el mercado, hora a hora o cuarto a cuarto, más un margen", "Fórmula oficial: 45 % mercado diario e intradiario y 55 % futuros"],
    ["Quién pone el margen", "La comercializadora, dentro del precio", "La comercializadora, que debe explicar la fórmula", "Lo fija la normativa"],
    ["¿Pueden subirte el precio?", "No: no caben cláusulas de revisión", "Sube y baja con el mercado", "Sube y baja con el mercado"],
    ["Penalización si te vas", "Posible antes de la primera prórroga anual (máx. 5 % de la energía pendiente)", "Ninguna (2.0TD)", "Ninguna"],
    ["Para quién", "Quien quiere saber lo que pagará", "Quien puede mover consumo a horas baratas y aguanta los meses caros", "Quien quiere el precio regulado o el bono social"],
])
md["tarifa-fija-o-indexada"] = cabecera(
    "tarifa fija o indexada",
    f"- OMIE marginalpdbc, media simple de todos los periodos de cada mes (columna del sistema español). {len(list(OMIE.glob('*.1')))} ficheros diarios.\n"
    f"- Solo la parte de la energía que sigue al mercado: kWh × precio medio × {num(FACTOR_IMP, 3)} (impuesto eléctrico 5,11 % e IVA 21 %). "
    "No incluye peajes, cargos, servicios de ajuste, margen de la comercializadora ni término de potencia.\n"
    f"- Hogar de ejemplo: {CONS} kWh al mes. Mes más barato de los 12: {mes(barato)} ({num(media[barato])} €/MWh); más caro: {mes(caro)} ({num(media[caro])} €/MWh).\n"
    f"- Días por mes en los ficheros: {', '.join(f'{mes(k)} {dias[k]}' for k in ULT12)}.\n"
    f"- Octubre de 2026 (días 1 a 6): {num(media.get((2026, 10), 0))} €/MWh.\n"
    f"- Media de los últimos 12 meses (oct. 2025–sep. 2026): {num(med12)} €/MWh.\n")
md["tarifa-fija-o-indexada"] += "## OMIE\n\n" + t1 + "\n## Riesgo\n\n" + t2 + "\n## Sensibilidad\n\n" + t3 + "\n## Comparar\n\n" + t4

# ------------------------------------------------------------------ 2. bono social térmico
MIN = 50
t1 = tabla("bst_cuantia", ["Tu situación", "Ayuda mínima", "Si en tu zona el vulnerable cobra el mínimo", "Cómo varía"], [
    ["Consumidor vulnerable", eur(MIN), eur(MIN), "Más cuanto más frío es tu clima (zonas α a E)"],
    ["Vulnerable severo o en riesgo de exclusión social", eur(MIN), eur(MIN * 1.6), "Un 60 % más que el vulnerable de tu misma zona"],
])
t2 = tabla("bst_comparar", ["", "Bono social eléctrico", "Bono social térmico"], [
    ["Qué es", "Descuento en la factura de la luz", "Ayuda en dinero, un pago único al año"],
    ["Para qué", "La electricidad", "Calefacción, agua caliente o cocina, con cualquier energía"],
    ["Cómo se pide", "Solicitud a una comercializadora de referencia", "Sin solicitud aparte en la norma estatal: lo reciben quienes tienen el bono eléctrico a 31 de diciembre"],
    ["Quién paga", "Las comercializadoras de electricidad", "Los Presupuestos Generales del Estado; lo abona tu comunidad autónoma"],
    ["Cuánto", "42,5 % o 57,5 % de descuento en 2026", "Según tu zona climática y tu grado de vulnerabilidad; mínimo 50 €"],
])
# Ejemplo del artículo del bono social eléctrico: 3,45 kW, 0,09 €/kW·día, 132,25 kWh al mes, 0,13 €/kWh.
base_si = 3.45 * POT * DIAS_MES + 132.25 * ENE
IMP_EX = (1 + IEE) * (1 + IVA)  # factor exacto, como en el artículo del bono social eléctrico
rows = [["Sin bono social", eur(base_si * IMP_EX), eur(0)]]
for nom, d in (("Vulnerable, descuento habitual (35 %)", .35), ("Vulnerable en 2026 (42,5 %)", .425),
               ("Vulnerable severo, descuento habitual (50 %)", .5), ("Vulnerable severo en 2026 (57,5 %)", .575)):
    rows.append([nom, eur(base_si * (1 - d) * IMP_EX), eur(base_si * d * IMP_EX)])
t3 = tabla("bst_descuentos", ["Situación", "Potencia y energía al mes, con impuestos", "Descuento al mes"], rows)
md["bono-social-termico"] = cabecera(
    "bono social térmico",
    "- RDL 15/2018, anexo I.3 (redacción del RDL 7/2026, art. 2): ayuda mínima 50 €. Anexo I.4: severo o en riesgo de exclusión = vulnerable de su zona × 1,6.\n"
    "- RDL 7/2026, art. 3: suplemento de 90 M€ para 2026; el preámbulo dice que complementa la previsión de 335 M€ (total 425 M€).\n"
    "- Descuentos: RD 897/2017, art. 6.3 (35 % y 50 %); RDL 7/2026, art. 1 (42,5 % y 57,5 % del 1/1 al 31/12/2026).\n"
    f"- Ejemplo de descuentos: el del artículo del bono social eléctrico (3,45 kW, {fpr(POT)} €/kW·día, 132,25 kWh al mes a {fpr(ENE)} €/kWh): "
    f"{num(base_si, 4)} € sin impuestos, impuestos con el factor exacto 1,0511 × 1,21 (igual que ese artículo). Descuento sobre potencia y energía, impuestos después; sin alquiler del contador.\n")
md["bono-social-termico"] += "## Cuantía\n\n" + t1 + "\n## Comparar\n\n" + t2 + "\n## Descuentos\n\n" + t3

# ------------------------------------------------------------------ 3. consumo por horas y Datadis
t1 = tabla("dd_donde", ["Dónde", "Qué ves", "Qué necesitas"], [
    ["Datadis (datadis.es)", "Consumo hora a hora de todos tus suministros, aunque sean de distribuidoras distintas, y descarga del fichero", "Registrarte; es gratis"],
    ["Web o app de tu distribuidora", "Consumo horario y lecturas de tu contador", "Registrarte en su web"],
    ["Área de clientes de tu comercializadora", "El consumo de tus facturas", "Ser su cliente"],
    ["La factura", "Consumo del periodo, separado en punta, llano y valle", "Nada"],
    ["La pantalla del contador", "Lecturas acumuladas", "Acceso al contador"],
])
P, L, V = TRAMOS["punta"], TRAMOS["llano"], TRAMOS["valle"]
rows = []
for k in (1, 2, 3):
    rows.append([kwh(k, 0) + " al día", eur(k * (P - V) * DIAS_MES), eur(k * (P - V) * DIAS_MES * 12)])
t2 = tabla("dd_mover", ["Consumo que pasas de punta a valle", "Ahorro al mes", "Ahorro al año"], rows)
rows = []
for w in (50, 100, 150):
    k = w / 1000 * 24 * DIAS_MES
    rows.append([f"{w} W", kwh(k, 1), eur(k * PRECIO), eur(k * PRECIO * 12)])
t3 = tabla("dd_base", ["Consumo de fondo (de madrugada)", "kWh al mes", "Coste al mes", "Coste al año"], rows)
md["ver-consumo-por-horas-datadis"] = cabecera(
    "consumo por horas y Datadis",
    f"- Mover consumo: kWh/día × (punta − valle) × 30,4 días = kWh × ({num(P, 3)} − {num(V, 3)}) × 30,4. Año = 12 meses.\n"
    "- Consumo de fondo: W / 1000 × 24 h × 30,4 días × 0,165 €/kWh.\n"
    "- RD 88/2026, art. 6.y (acceso gratuito a los datos de consumo) y art. 17.2 (curva de carga, autorización a terceros renovable cada 6 meses).\n"
    "- CNMC, nota de prensa de 21/10/2020: 99,22 % de los consumidores domésticos (< 15 kW) con contador inteligente integrado a finales de 2019.\n")
md["ver-consumo-por-horas-datadis"] += "## Dónde\n\n" + t1 + "\n## Mover consumo\n\n" + t2 + "\n## Consumo de fondo\n\n" + t3

# ------------------------------------------------------------------ 4. suelo radiante eléctrico
F, H = 0.6, 5  # factor de uso (emisor térmico en CLAUDE.md) y horas al día (igual que emisores)
rows = []
for d in (60, 100, 150):
    w = d * 20
    k = w / 1000 * F
    rows.append([f"{d} W/m²", f"{num(w, 0)} W", eur(k * PRECIO), eur(k * H * PRECIO), eur(k * H * DIAS_MES * PRECIO), eur(k * H * DIAS_MES * INV * PRECIO)])
t1 = tabla("sr_potencias", ["Potencia por m²", "Potencia en 20 m²", "Por hora", "Por día (5 h)", "Por mes", "Invierno (4 meses)"], rows)
CASA = [("Salón", 20, 100, 5), ("Dormitorio principal", 12, 100, 3), ("Segundo dormitorio", 10, 100, 2), ("Baño", 5, 150, 2)]
rows, tot_d = [], 0
for nom, m2, d, h in CASA:
    w = m2 * d
    k = w / 1000 * F * h
    tot_d += k
    rows.append([nom, f"{m2} m² × {d} W/m² = {num(w, 0)} W", f"{h} h", kwh(k), eur(k * PRECIO), eur(k * DIAS_MES * PRECIO), eur(k * DIAS_MES * INV * PRECIO)])
rows.append(["Total", f"{num(sum(m * d for _, m, d, _ in CASA), 0)} W", "", kwh(tot_d), eur(tot_d * PRECIO), eur(tot_d * DIAS_MES * PRECIO), eur(tot_d * DIAS_MES * INV * PRECIO)])
t2 = tabla("sr_casa", ["Estancia", "Potencia instalada", "Horas al día", "kWh al día (real)", "Por día", "Por mes", "Invierno (4 meses)"], rows)
k_salon = 20 * 100 / 1000 * F * H
rows = [["Precio único de referencia", num(PRECIO, 3) + " €/kWh", eur(k_salon * PRECIO * DIAS_MES)]]
for nom, pr in (("Todo en punta", P), ("Todo en llano", L), ("Todo en valle", V)):
    rows.append([nom, num(pr, 3) + " €/kWh", eur(k_salon * pr * DIAS_MES)])
t3 = tabla("sr_tramos", ["Si el salón (2.000 W, 5 h) calienta…", "Precio con impuestos", "Coste al mes"], rows)
SCOP = 3.5
calor = 20 * 100 / 1000 * F * H  # kWh de calor al día del salón
t4 = tabla("sr_comparar", ["Mismo calor para el salón", "Electricidad al día", "Coste al mes", "Invierno (4 meses)"], [
    ["Suelo radiante eléctrico", kwh(calor), eur(calor * PRECIO * DIAS_MES), eur(calor * PRECIO * DIAS_MES * INV)],
    ["Emisor térmico o radiador eléctrico", kwh(calor), eur(calor * PRECIO * DIAS_MES), eur(calor * PRECIO * DIAS_MES * INV)],
    [f"Bomba de calor (SCOP {num(SCOP, 1)}, ejemplo)", kwh(calor / SCOP), eur(calor / SCOP * PRECIO * DIAS_MES), eur(calor / SCOP * PRECIO * DIAS_MES * INV)],
])
md["cuanto-consume-suelo-radiante-electrico"] = cabecera(
    "suelo radiante eléctrico",
    f"- Factor de uso {num(F, 1)} (termostato; el de emisor térmico en CLAUDE.md). {H} h al día como en los emisores. Invierno de {INV} meses.\n"
    "- Potencias por m²: Salvador Escoda (mantas de 60 W/m² para casas nuevas bien aisladas, 120 W/m² y 180 W/m² para baños); "
    "Danfoss DEVI (máx. 200 W/m² en hormigón con baldosa, 150 W/m² sobre capa aislante, 100 W/m² bajo madera, 80 W/m² entre viguetas de madera).\n"
    "- Casa de ejemplo: superficies, potencias y horas orientativas, no son un dimensionado.\n"
    f"- Bomba de calor: mismo calor ÷ SCOP {num(SCOP, 1)} (valor de ejemplo, igual que en el artículo de emisores).\n")
md["cuanto-consume-suelo-radiante-electrico"] += ("## Potencias\n\n" + t1 + "\n## Casa\n\n" + t2 + "\n## Tramos\n\n" + t3 + "\n## Comparar\n\n" + t4)

# ------------------------------------------------------------------ página «Metodología»
W, HD = 2000, 5  # radiador de aceite de ejemplo
k_dia = W / 1000 * 0.6 * HD
t1 = tabla("met_ejemplo", ["Paso", "Cálculo", "Resultado"], [
    ["1. Potencia de la etiqueta", "2.000 W = 2 kW", "2 kW"],
    ["2. Factor de uso real (termostato)", "2 kW × 0,6", "1,2 kWh por hora"],
    ["3. Horas al día", "1,2 kWh × 5 h", kwh(k_dia, 1) + " al día"],
    ["4. Precio con impuestos", f"{kwh(k_dia, 1)} × 0,165 €/kWh", eur(k_dia * PRECIO) + " al día"],
    ["5. Mes de 30,4 días", f"{eur(k_dia * PRECIO)} × 30,4", eur(k_dia * PRECIO * DIAS_MES) + " al mes"],
])
t2 = tabla("met_precios", ["Concepto", "Valor que usamos", "Con impuestos"], [
    ["Energía, precio único", fpr(ENE) + " €/kWh", num(PRECIO, 3) + " €/kWh"],
    ["Energía en punta (10–14 h y 18–22 h, laborables)", fpr(REF["tramos"]["punta"]) + " €/kWh", num(P, 3) + " €/kWh"],
    ["Energía en llano (8–10 h, 14–18 h y 22–24 h, laborables)", fpr(REF["tramos"]["llano"]) + " €/kWh", num(L, 3) + " €/kWh"],
    ["Energía en valle (0–8 h y fines de semana)", fpr(REF["tramos"]["valle"]) + " €/kWh", num(V, 3) + " €/kWh"],
    ["Término de potencia (calculadoras)", fpr(POT) + " €/kW y día", num(POT * FACTOR_IMP, 3) + " €/kW y día"],
    ["Alquiler del contador (calculadora de consumo)", num(CONT, 2) + " € al mes", num(CONT * (1 + IVA), 2) + " € al mes (solo IVA)"],
    ["Impuesto eléctrico e IVA", f"{num(IEE * 100, 2)} % y {num(IVA * 100, 0)} %", f"Factor {num(1 + IEE, 4)} × {num(1 + IVA, 2)} = " + num((1 + IEE) * (1 + IVA), 4)],
])
t3 = tabla("met_factores", ["Aparato", "Factor de uso real", "Por qué"], [
    ["Nevera y congelador", "0,2 (sobre 150 W)", "El compresor arranca y para durante el día"],
    ["Aire acondicionado", "0,6", "El compresor baja de potencia al llegar a la temperatura"],
    ["Radiador de aceite y emisor térmico", "0,6", "El termostato corta y vuelve a conectar"],
    ["Estufa eléctrica", "0,85", "Termostato más simple: está encendida más tiempo"],
    ["Termo eléctrico", "0,7", "La resistencia solo funciona mientras recupera temperatura"],
    ["Horno", "0,6", "Precalienta a tope y después mantiene"],
    ["Inducción y vitrocerámica", "0,7 y 0,75", "Rara vez se usa a la potencia máxima"],
    ["Secadora y lavavajillas", "0,8 y 0,55", "La resistencia no calienta todo el ciclo"],
    ["Freidora de aire, deshumidificador y manta", "0,7 · 0,8 · 0,5", "Funcionan a ciclos"],
    ["Resto de aparatos", "1", "Se toma la potencia de la etiqueta"],
])
md["metodologia"] = cabecera(
    "página Metodología",
    f"- Factor de impuestos: {num(1 + IEE, 4)} × {num(1 + IVA, 2)} = {num((1 + IEE) * (1 + IVA), 6)}, redondeado a {num(FACTOR_IMP, 3)}. {fpr(ENE)} × {num(FACTOR_IMP, 3)} = {num(ENE * FACTOR_IMP, 5)} → {num(PRECIO, 3)} €/kWh.\n"
    f"- Potencia y alquiler del contador: valores de las calculadoras (POT_DIA {fpr(POT)} y CONTADOR {num(CONT, 2)} en consumo3.src.js y potencia3.src.js); "
    "el contador solo lleva IVA en la calculadora (CONTADOR × IVA).\n")
md["metodologia"] += "## Ejemplo\n\n" + t1 + "\n## Precios\n\n" + t2 + "\n## Factores\n\n" + t3

if __name__ == "__main__":
    (BASE / "scripts" / "tablas_tanda8.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
    for slug, txt in md.items():
        (BASE / "calculos" / f"{slug}.md").write_text(txt, encoding="utf-8")
    for k, t in tablas.items():
        print(k)
        for r in t["rows"]:
            print("   ", " | ".join(r))
