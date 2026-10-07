"""Cálculos de la tanda 4 (1.ª de 4): consumo fantasma, cambiar de compañía, CUPS y
magnetotérmico frente a diferencial.

Criterios de CLAUDE.md: 0,165 €/kWh con impuestos (0,13 € sin impuestos × 1,272); mes de 30,4 días;
año de 12 meses. Término de potencia con impuesto eléctrico e IVA (1,21 × 1,0511), como las calculadoras.
Fuentes de datos externos (consultadas el 6/10/2026):
- Reglamento (UE) 2023/826 (DO L 103 de 18/4/2023), anexo III: límites de los modos desactivado,
  preparado y preparado en red; aplicable desde el 9/5/2025.
- Ley 24/2013 del Sector Eléctrico (BOE-A-2013-13645), arts. 43 y 44, texto consolidado.
- Resolución de 16/11/2009 de la Secretaría de Estado de Energía (BOE-A-2009-19040), P.O. 10.8:
  estructura del CUPS y cálculo de las letras de control (módulo 529 y 23).
- REBT, Real Decreto 842/2002 (BOE-A-2002-18099), ITC-BT-25, tabla 1: interruptor automático de cada circuito.
Genera calculos/<slug>.md y scripts/tablas_tanda4.json.
"""
import json
from pathlib import Path
from calculos import PRECIO, FACTOR_IMP, DIAS_MES, eur, num, cabecera

BASE = Path(__file__).resolve().parent.parent
DIAS_ANO = DIAS_MES * 12
from calculos import REF
IMP_POT = (1 + REF["iva"]) * (1 + REF["impuesto_electrico"])
tablas, md = {}, {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def kwh_ano(w):
    return w * 24 * DIAS_ANO / 1000


# ------------------------------------------------------------------ 1. consumo fantasma
rows = []
for w in (0.5, 1, 2, 5, 10, 20, 30):
    rows.append([num(w, 1 if w < 1 else 0) + " W", num(kwh_ano(w), 1) + " kWh",
                 eur(w * 24 * DIAS_MES / 1000 * PRECIO), eur(kwh_ano(w) * PRECIO)])
t1 = tabla("fantasma_watios", ["Consumo en espera, las 24 horas", "Energía al año", "Coste al mes", "Coste al año"], rows)
limites = [
    ("Modo desactivado (apagado, pero enchufado)", 0.50, "0,30 W desde el 9 de mayo de 2027"),
    ("Modo preparado (solo para poder encenderlo)", 0.50, "—"),
    ("Modo preparado con pantalla o reloj", 0.80, "1,00 W en secadoras"),
    ("Preparado en red (se enciende por wifi o por cable)", 2.00, "Equipos de alta disponibilidad de red: 8,00 W, 7,00 W desde 2027"),
]
t2 = tabla("fantasma_limites", ["Estado del aparato", "Máximo para un aparato nuevo", "Coste al año en ese máximo", "Observaciones"],
           [[e, num(w, 2) + " W", eur(kwh_ano(w) * PRECIO), o] for e, w, o in limites])
ej = [("5 aparatos apagados pero enchufados", 5, 0.50), ("3 aparatos en espera con reloj o piloto", 3, 0.80),
      ("2 aparatos conectados en red esperando una orden", 2, 2.00)]
total_w = sum(n * w for _, n, w in ej)
t3 = tabla("fantasma_casa", ["Ejemplo de casa con aparatos nuevos", "Potencia en espera", "Coste al año"],
           [[d, num(n * w, 2) + " W", eur(kwh_ano(n * w) * PRECIO)] for d, n, w in ej] +
           [["Total", num(total_w, 2) + " W", eur(kwh_ano(total_w) * PRECIO)]])
md["consumo-fantasma"] = cabecera(
    "consumo fantasma",
    f"- Consumo continuo las 24 horas, {num(DIAS_MES, 1)} días al mes y {num(DIAS_ANO, 1)} días al año.\n"
    f"- 1 W todo el año = {num(kwh_ano(1), 4)} kWh = {eur(kwh_ano(1) * PRECIO)}.\n"
    f"- Ejemplo de la casa: {num(total_w, 2)} W en total = {num(kwh_ano(total_w), 1)} kWh al año.\n"
    f"- Ahorro de quitar 10 W en espera: {eur(kwh_ano(10) * PRECIO)} al año; 20 W: {eur(kwh_ano(20) * PRECIO)}.\n"
) + "## Coste por vatio\n\n" + t1 + "\n## Límites del Reglamento (UE) 2023/826\n\n" + t2 + "\n## Ejemplo de casa\n\n" + t3

# ------------------------------------------------------------------ 2. cambiar de compañía
rows = []
for kwh in (1500, 2500, 3500, 4500):
    rows.append([num(kwh, 0) + " kWh", eur(kwh * 0.01 * FACTOR_IMP), eur(kwh * 0.02 * FACTOR_IMP), eur(kwh * 0.03 * FACTOR_IMP)])
t1 = tabla("cambio_energia", ["Consumo al año", "1 céntimo menos por kWh", "2 céntimos menos", "3 céntimos menos"], rows)
rows = []
for kw in (3.45, 4.6, 5.75):
    rows.append([num(kw, 2) + " kW", eur(kw * 0.01 * DIAS_ANO * IMP_POT), eur(kw * 0.02 * DIAS_ANO * IMP_POT)])
t2 = tabla("cambio_potencia", ["Potencia contratada", "1 céntimo menos por kW y día", "2 céntimos menos"], rows)
md["cambiar-compania-luz"] = cabecera(
    "cambiar de compañía de luz",
    "- Diferencias de precio sin impuestos; se les aplica el impuesto eléctrico y el IVA "
    f"(× {num(FACTOR_IMP, 3)} en la energía, × {num(IMP_POT, 4)} en la potencia).\n"
    f"- Año de {num(DIAS_ANO, 1)} días para la potencia.\n"
    f"- Ejemplo del texto: 2.500 kWh y 2 céntimos menos = {eur(2500 * 0.02 * FACTOR_IMP)} al año.\n"
) + "## Energía\n\n" + t1 + "\n## Potencia\n\n" + t2

# ------------------------------------------------------------------ 3. CUPS
LETRAS = "TRWAGMYFPDXBNJZSQVHLCKE"


def control(dieciseis):
    r0 = int(dieciseis) % 529
    c, r = divmod(r0, 23)
    return r0, c, r, LETRAS[c] + LETRAS[r]


ejemplo = "0987543210987654"  # ejemplo publicado en el propio BOE: ES 0987 5432 1098 7654 ZF
r0, c, r, ee = control(ejemplo)
assert ee == "ZF", ee
for d16, esperado in (("1234123456789012", "JY"), ("9750210987654321", "CQ"), ("0999110012345678", "EK")):
    assert control(d16)[3] == esperado, (d16, control(d16))
t1 = tabla("cups_partes", ["Parte", "Caracteres", "Qué indica", "En el ejemplo"], [
    ["País", "2 letras", "ES en España", "ES"],
    ["Distribuidora", "4 números", "La distribuidora a la que está conectada la vivienda cuando se asignó el código", "0987"],
    ["Punto de suministro", "12 números", "El número que la distribuidora da a tu suministro", "5432 1098 7654"],
    ["Control", "2 letras", "Sirven para detectar errores al copiar el código", "ZF"],
    ["Opcional", "1 número y 1 letra", "Distinguen varios puntos de medida de un mismo cliente; en casa no suelen aparecer", "—"],
])
md["que-es-el-cups"] = cabecera(
    "qué es el CUPS",
    "- Estructura: P.O. 10.8, Resolución de 16/11/2009 (BOE-A-2009-19040).\n"
    f"- Letras de control del ejemplo del BOE ES 0987 5432 1098 7654: {int(ejemplo)} mod 529 = {r0}; "
    f"{r0} entre 23 = {c} y resto {r}; tabla del BOE: {c} → {LETRAS[c]}, {r} → {LETRAS[r]} = {ee}.\n"
    "- Comprobados también los otros ejemplos del BOE: JY, CQ y EK.\n"
) + "## Partes del CUPS\n\n" + t1

# ------------------------------------------------------------------ 4. magnetotérmico y diferencial
circ = [("C1", "Iluminación", 10), ("C2", "Enchufes de uso general y frigorífico", 16), ("C3", "Cocina y horno", 25),
        ("C4", "Lavadora, lavavajillas y termo", 20), ("C5", "Enchufes del baño y auxiliares de la cocina", 16),
        ("C8", "Calefacción (si está prevista)", 25), ("C9", "Aire acondicionado (si está previsto)", 25),
        ("C10", "Secadora (si es independiente)", 16)]
t1 = tabla("rebt_circuitos", ["Circuito", "Para qué es", "Magnetotérmico", "Potencia máxima a 230 V"],
           [[c, u, f"{a} A", num(a * 230, 0) + " W"] for c, u, a in circ])
md["diferencia-magnetotermico-diferencial"] = cabecera(
    "magnetotérmico y diferencial",
    "- Interruptor automático de cada circuito: REBT, ITC-BT-25, tabla 1 (BOE-A-2002-18099).\n"
    "- Potencia máxima = intensidad del magnetotérmico × 230 V (tensión entre fase y neutro de la tabla).\n"
    "- Diferencial: intensidad diferencial-residual máxima de 30 mA; al menos uno por cada cinco circuitos (ITC-BT-25, 2.1 y 2.3).\n"
    "- Interruptor general automático: 25 A como mínimo (ITC-BT-25, 2.1).\n"
) + "## Circuitos de una vivienda\n\n" + t1

for slug, text in md.items():
    (BASE / "calculos" / f"{slug}.md").write_text(text, encoding="utf-8")
(BASE / "scripts" / "tablas_tanda4.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
if __name__ == "__main__":
    print("\n\n".join(md.values()))
