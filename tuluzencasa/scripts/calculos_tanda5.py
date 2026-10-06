"""Cálculos de la tanda 2 de 4: lavadora, secadora, lavavajillas y horno eléctrico.

Criterios de CLAUDE.md: 0,165 €/kWh con impuestos (0,13 € × 1,272); tramos 0,19 / 0,12 / 0,08 €/kWh sin
impuestos; mes de 30,4 días y año de 12 meses; semanas al mes 4,345 (como la calculadora).
Valores de nuestra calculadora de consumo: lavadora 800 W × 1 h (factor 1); lavavajillas 1.200 W × 1,5 h
(factor 0,55); horno 2.200 W × 45 min (factor 0,6); secadora factor 0,8. Lo que va por usos: 12 al mes.
Fuentes de datos externos (consultadas el 6/10/2026, textos en fuentes/tanda5/):
- Lavadoras: Reglamento Delegado (UE) 2019/2014 (etiqueta, cuadro 1 de clases) y Reglamento (UE) 2019/2023
  (diseño ecológico, anexo II, punto 3: IEE < 105 desde 1/3/2021 y < 91 desde 1/3/2024 si > 3 kg).
- Lavavajillas: Reglamento Delegado (UE) 2019/2017 (cuadro 1 de clases) y Reglamento (UE) 2019/2022
  (anexo II, punto 2: IEE < 63 desde 1/3/2021; < 56 desde 1/3/2024 si ≤ 10 cubiertos).
- Secadoras: Reglamento Delegado (UE) 2023/2534 (cuadro 1 de clases, aplicable desde 1/7/2025) y
  Reglamento (UE) 2023/2533 (anexo II, punto 2: IEE ≤ 85; anexo V: valores de referencia de 7 kg).
- Hornos: Reglamento Delegado (UE) 65/2014 (clases A+++ a D) y Reglamento (UE) 66/2014
  (anexo I, cuadro 1: EEI < 96 cinco años después de la entrada en vigor, 20/2/2019).
Genera calculos/<slug>.md y scripts/tablas_tanda5.json.
"""
import json
from pathlib import Path
from calculos import PRECIO, FACTOR_IMP, DIAS_MES, TRAMOS, eur, num, cabecera

BASE = Path(__file__).resolve().parent.parent
SEM = 4.345
USOS_MES = 12
tablas, md = {}, {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def kwh(x, d=2):
    return num(x, d) + " kWh"


def frecuencia(key, kwh_uso, nombre):
    rows = []
    for veces in (3, 5, 7):
        mes = kwh_uso * veces * SEM
        rows.append([f"{veces} {nombre} a la semana", kwh(mes, 1), eur(mes * PRECIO), eur(mes * 12 * PRECIO)])
    return tabla(key, ["Uso", "Energía al mes", "Coste al mes", "Coste al año"], rows)


def etiqueta(key, valores, nombre):
    rows = []
    for v in valores:
        c = v / 100
        rows.append([f"{v} kWh/100 ciclos", kwh(c), eur(c * PRECIO), eur(v * PRECIO), eur(c * USOS_MES * 12 * PRECIO)])
    return tabla(key, ["Lo que pone la etiqueta", f"Energía por {nombre}", f"Coste por {nombre}",
                       "Coste de 100 ciclos", "Coste al año (12 al mes)"], rows)


def tramos(key, filas):
    rows = []
    for nombre, k in filas:
        p, ll, v = (k * TRAMOS[t] for t in ("punta", "llano", "valle"))
        rows.append([nombre, kwh(k), eur(p), eur(ll), eur(v), eur((p - v) * USOS_MES)])
    return tabla(key, ["Aparato", "Energía por uso", "En punta", "En llano", "En valle",
                       "Ahorro al mes de punta a valle (12 usos)"], rows)


def basico(kwh_uso):
    return eur(kwh_uso * PRECIO), eur(kwh_uso * USOS_MES * PRECIO), eur(kwh_uso * USOS_MES * 12 * PRECIO)


# ------------------------------------------------------------------ 1. lavadora
LAV = 0.8 * 1 * 1.0
t1 = frecuencia("lavadora_frecuencia", LAV, "lavados")
t2 = etiqueta("lavadora_etiqueta", (40, 50, 60, 70, 80), "lavado")
t3 = tabla("lavadora_clases", ["Clase", "Índice de eficiencia energética", "¿Se puede vender nueva?"], [
    ["A", "52 o menos", "Sí"], ["B", "Más de 52 y hasta 60", "Sí"], ["C", "Más de 60 y hasta 69", "Sí"],
    ["D", "Más de 69 y hasta 80", "Sí"], ["E", "Más de 80 y hasta 91", "Sí, por debajo de 91"],
    ["F", "Más de 91 y hasta 102", "No, desde marzo de 2024 (más de 3 kg)"], ["G", "Más de 102", "No"]])
t4 = tramos("lavadora_tramos", [("Lavadora a 40 °C (800 W, 1 h)", LAV)])
c, m, a = basico(LAV)
md["cuanto-consume-lavadora"] = cabecera(
    "cuánto consume una lavadora",
    f"- Lavado de referencia (calculadora): 800 W × 1 h × factor 1 = {kwh(LAV)} → {c} por lavado; "
    f"12 al mes: {m}; al año: {a}.\n"
    f"- Semanas al mes: {num(SEM, 3)}.\n"
    "- Etiqueta: kWh por 100 ciclos del programa eco 40-60 (Reglamento Delegado 2019/2014, anexo III).\n"
    f"- Esquema de etiqueta de ejemplo (datos inventados): 52 kWh/100 ciclos → {kwh(0.52)} por lavado → "
    f"{eur(0.52 * PRECIO)} por lavado; 12 al mes: {eur(0.52 * 12 * PRECIO)}; al año: {eur(0.52 * 144 * PRECIO)}.\n"
) + "## Frecuencia\n\n" + t1 + "\n## Etiqueta\n\n" + t2 + "\n## Clases\n\n" + t3 + "\n## Tramos\n\n" + t4

# ------------------------------------------------------------------ 2. secadora
REF = [("De evacuación (ventilación)", 2.58, 76), ("De condensación con resistencia", 2.73, 76),
       ("Con bomba de calor", 0.85, 134)]
rows = [[t, kwh(k), f"{m_} min", *basico(k)] for t, k, m_ in REF]
t1 = tabla("secadora_tipos", ["Secadora de 7 kg, programa eco", "Energía por ciclo", "Duración",
                              "Coste por ciclo", "Coste al mes (12 ciclos)", "Coste al año"], rows)
ahorro = (2.58 - 0.85) * USOS_MES * 12 * PRECIO
ahorro_c = (2.73 - 0.85) * USOS_MES * 12 * PRECIO
t2 = etiqueta("secadora_etiqueta", (60, 100, 150, 200, 250), "secado")
t3 = tabla("secadora_clases", ["Clase", "Índice de eficiencia energética", "¿Se puede vender nueva?"], [
    ["A", "43 o menos", "Sí"], ["B", "Más de 43 y hasta 50", "Sí"], ["C", "Más de 50 y hasta 60", "Sí"],
    ["D", "Más de 60 y hasta 70", "Sí"], ["E", "Más de 70 y hasta 85", "Sí"],
    ["F", "Más de 85 y hasta 100", "No, desde julio de 2025"], ["G", "Más de 100", "No, desde julio de 2025"]])
t4 = tramos("secadora_tramos", [("Secadora de evacuación", 2.58), ("Secadora con bomba de calor", 0.85)])
# comprobación del modelo de la calculadora con la duración del reglamento
modelo_evac = 2500 / 1000 * 76 / 60 * 0.8
md["cuanto-consume-secadora"] = cabecera(
    "cuánto consume una secadora",
    "- Energía por ciclo: valores de referencia del Reglamento (UE) 2023/2533, anexo V (mejor tecnología disponible "
    "en 2023, 7 kg, media ponderada 0,24 carga completa + 0,76 carga parcial).\n"
    f"- Ahorro al año de bomba de calor frente a evacuación (144 ciclos): {eur(ahorro)}; frente a condensación: {eur(ahorro_c)}.\n"
    f"- Contraste con el modelo de la calculadora: 2.500 W × 76 min × 0,8 = {kwh(modelo_evac)} (reglamento: 2,58 kWh).\n"
) + "## Tipos\n\n" + t1 + "\n## Etiqueta\n\n" + t2 + "\n## Clases\n\n" + t3 + "\n## Tramos\n\n" + t4

# ------------------------------------------------------------------ 3. lavavajillas
LVV = 1.2 * 1.5 * 0.55
t1 = frecuencia("lavavajillas_frecuencia", LVV, "lavados")
t2 = etiqueta("lavavajillas_etiqueta", (50, 65, 80, 95, 110), "lavado")
t3 = tabla("lavavajillas_clases", ["Clase", "Índice de eficiencia energética"], [
    ["A", "Menos de 32"], ["B", "De 32 a menos de 38"], ["C", "De 38 a menos de 44"], ["D", "De 44 a menos de 50"],
    ["E", "De 50 a menos de 56"], ["F", "De 56 a menos de 62"], ["G", "62 o más"]])
t4 = tramos("lavavajillas_tramos", [("Lavavajillas, programa eco (1.200 W, 1,5 h)", LVV)])
c, m, a = basico(LVV)
md["cuanto-consume-lavavajillas"] = cabecera(
    "cuánto consume un lavavajillas",
    f"- Lavado de referencia (calculadora): 1.200 W × 1,5 h × 0,55 = {kwh(LVV, 3)} → {c} por lavado; "
    f"12 al mes: {m}; al año: {a}.\n"
    "- Etiqueta: kWh por 100 ciclos del programa eco (Reglamento Delegado 2019/2017, anexo III).\n"
) + "## Frecuencia\n\n" + t1 + "\n## Etiqueta\n\n" + t2 + "\n## Clases\n\n" + t3 + "\n## Tramos\n\n" + t4

# ------------------------------------------------------------------ 4. horno
F_HORNO = 0.6
rows = []
for w in (2000, 2200, 2500, 3000):
    uso = w / 1000 * 0.75 * F_HORNO
    rows.append([num(w, 0) + " W", eur(w / 1000 * F_HORNO * PRECIO), kwh(uso), *basico(uso)])
t1 = tabla("horno_potencias", ["Potencia del horno", "Coste por hora", "Energía por uso (45 min)",
                               "Coste por uso", "Coste al mes (12 usos)", "Coste al año"], rows)
rows = []
for mins in (20, 30, 40, 45, 60, 90, 120):
    k = 2.2 * mins / 60 * F_HORNO
    rows.append([f"{mins} min", kwh(k), eur(k * PRECIO)])
t2 = tabla("horno_minutos", ["Tiempo de horno (con precalentado)", "Energía", "Coste"], rows)
t3 = tabla("horno_clases", ["Clase", "Índice de eficiencia energética", "¿Se puede vender nuevo?"], [
    ["A+++", "Menos de 45", "Sí"], ["A++", "De 45 a menos de 62", "Sí"], ["A+", "De 62 a menos de 82", "Sí"],
    ["A", "De 82 a menos de 107", "Solo por debajo de 96, desde febrero de 2019"],
    ["B", "De 107 a menos de 132", "No"], ["C", "De 132 a menos de 159", "No"], ["D", "159 o más", "No"]])
HOR = 2.2 * 0.75 * F_HORNO
t4 = tramos("horno_tramos", [("Horno de 2.200 W, 45 min", HOR)])
c, m, a = basico(HOR)
md["cuanto-consume-horno-electrico"] = cabecera(
    "cuánto consume un horno eléctrico",
    f"- Uso de referencia (calculadora): 2.200 W × 45 min × 0,6 = {kwh(HOR)} → {c} por uso; 12 al mes: {m}; al año: {a}.\n"
    f"- Coste por hora con el factor 0,6: 2.200 W → {eur(2.2 * F_HORNO * PRECIO)}.\n"
    "- Clases: Reglamento Delegado 65/2014, anexo II; límite EEI < 96 desde el 20/2/2019 (Reglamento 66/2014, en vigor el 20/2/2014).\n"
) + "## Potencias\n\n" + t1 + "\n## Minutos\n\n" + t2 + "\n## Clases\n\n" + t3 + "\n## Tramos\n\n" + t4

for slug, text in md.items():
    (BASE / "calculos" / f"{slug}.md").write_text(text, encoding="utf-8")
(BASE / "scripts" / "tablas_tanda5.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
if __name__ == "__main__":
    print("\n\n".join(md.values()))
