"""Cálculos de la tanda 3 de 4: inducción o vitrocerámica, ordenador, bombillas LED y ventilador o aire acondicionado.

Criterios de CLAUDE.md: 0,165 €/kWh con impuestos; tramos 0,19 / 0,12 / 0,08 €/kWh sin impuestos; mes de 30,4 días;
año de 12 meses (364,8 días); verano de 3 meses; semanas al mes 4,345 (como la calculadora).
Valores de nuestra calculadora de consumo (calculadora.js):
- Placa de inducción, un fuego: 1.800 W, 1 h/día, factor 0,7. Vitrocerámica: 1.800 W, 1 h/día, factor 0,75.
  Sustitución de vitrocerámica por inducción: k = 0,75 (la inducción gasta el 75 % para cocinar lo mismo).
- Ordenador gaming: 400 W, 4 h/día, 7 días, factor 0,7. Portátil: 60 W, 6 h/día, 5 días/semana, factor 0,7.
- Iluminación LED (10 bombillas): 90 W, 5 h/día. Halógena (10 bombillas): 500 W, 5 h/día. Factor 1.
- Aire acondicionado 3.000 frigorías: 1.000 W, factor 0,6. Ventilador: 50 W, factor 1. 8 h/día.
Fuentes de datos externos (consultadas el 6/10/2026, textos en fuentes/tanda6/):
- Reglamento (UE) 66/2014, anexo I, cuadro 2: placas eléctricas < 195 Wh/kg desde el 20/2/2019.
- Reglamento (UE) 617/2013, anexo II: E_TEC de categoría A desde el 1/1/2016: sobremesa 94 kWh/año, portátil 27 kWh/año.
- Reglamento Delegado (UE) 2019/2015, cuadro 1: clases de fuentes luminosas por lm/W; etiqueta en kWh/1 000 h.
- Reglamento Delegado (UE) 626/2011, anexo VII, cuadro 4: 350 horas equivalentes de refrigeración al año.
Genera calculos/<slug>.md y scripts/tablas_tanda6.json.
"""
import json
from pathlib import Path
from calculos import PRECIO, DIAS_MES, TRAMOS, eur, num, cabecera

BASE = Path(__file__).resolve().parent.parent
DIAS_ANO = DIAS_MES * 12
SEM = 4.345
tablas, md = {}, {}


def tabla(key, headers, rows):
    tablas[key] = {"headers": headers, "rows": rows}
    out = "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n"
    return out + "".join("| " + " | ".join(r) + " |\n" for r in rows)


def kwh(x, d=2):
    return num(x, d) + " kWh"


def w(x):
    return num(x, 0) + " W"


# ------------------------------------------------------------------ 1. inducción o vitrocerámica
rows = []
for watts in (1200, 1800, 2300):
    for nombre, f in (("Vitrocerámica", 0.75), ("Inducción", 0.7)):
        k = watts / 1000 * f
        rows.append([f"{nombre}, fuego de {w(watts)}", kwh(k), eur(k * PRECIO), eur(k * DIAS_MES * PRECIO), eur(k * DIAS_ANO * PRECIO)])
t1 = tabla("placa_potencias", ["Fuego encendido 1 hora al día", "Energía por hora", "Coste por hora", "Coste al mes",
                               "Coste al año"], rows)
VIT = 1.8 * 1 * 0.75
IND_EQ = VIT * 0.75
rows = []
for horas in (0.5, 1, 1.5, 2):
    v = VIT * horas; i = IND_EQ * horas
    rows.append([num(horas, 1) + " h al día", eur(v * DIAS_ANO * PRECIO), eur(i * DIAS_ANO * PRECIO), eur((v - i) * DIAS_ANO * PRECIO)])
t2 = tabla("placa_ahorro", ["Uso de la placa (fuego de 1.800 W)", "Vitrocerámica al año", "Inducción al año (25 % menos)",
                            "Ahorro al año"], rows)
rows = []
for nombre, k in (("Vitrocerámica: 1 hora de fuego de 1.800 W", VIT), ("Inducción: lo mismo cocinado, con un 25 % menos de energía", IND_EQ)):
    p, ll, v = (k * TRAMOS[t] for t in ("punta", "llano", "valle"))
    rows.append([nombre, eur(p), eur(ll), eur(v)])
t3 = tabla("placa_tramos", ["Cocinar", "En punta", "En llano", "En valle (fin de semana)"], rows)
md["induccion-o-vitroceramica"] = cabecera(
    "inducción o vitrocerámica",
    f"- Calculadora: fuego de 1.800 W, 1 h/día; factor 0,75 (vitro) y 0,7 (inducción) por hora encendida.\n"
    f"- Para cocinar lo mismo, la calculadora supone que la inducción gasta el 75 % de la vitro (k = 0,75): "
    f"{kwh(VIT)} frente a {kwh(IND_EQ, 3)} al día.\n"
    f"- Ahorro con 1 h/día: {eur((VIT - IND_EQ) * DIAS_ANO * PRECIO)} al año.\n"
) + "## Potencias\n\n" + t1 + "\n## Ahorro\n\n" + t2 + "\n## Tramos\n\n" + t3

# ------------------------------------------------------------------ 2. ordenador
GAM = 0.4 * 0.7
POR = 0.06 * 0.7
rows = [
    ["Portátil de 60 W", kwh(POR, 3), eur(POR * PRECIO), eur(POR * 6 * 5 * SEM * PRECIO), eur(POR * 6 * 5 * SEM * 12 * PRECIO), "6 h al día, 5 días a la semana"],
    ["Ordenador para juegos de 400 W", kwh(GAM), eur(GAM * PRECIO), eur(GAM * 4 * 7 * SEM * PRECIO), eur(GAM * 4 * 7 * SEM * 12 * PRECIO), "4 h al día, todos los días"],
]
t1 = tabla("ordenador_tipos", ["Equipo", "Energía por hora", "Coste por hora", "Coste al mes", "Coste al año", "Uso supuesto"], rows)
rows = []
for horas in (2, 4, 8):
    rows.append([f"{horas} h al día", eur(POR * horas * DIAS_MES * PRECIO), eur(GAM * horas * DIAS_MES * PRECIO)])
t2 = tabla("ordenador_horas", ["Uso todos los días", "Portátil de 60 W al mes", "Ordenador para juegos de 400 W al mes"], rows)
rows = [["Sobremesa", "94 kWh", eur(94 * PRECIO)], ["Portátil", "27 kWh", eur(27 * PRECIO)]]
t3 = tabla("ordenador_limites", ["Ordenador básico (categoría A)", "Máximo al año desde 2016", "Coste al año en ese máximo"], rows)
rows = []
for kw in (20, 30, 50, 80):
    rows.append([f"{kw} kWh/1 000 h", eur(kw * PRECIO), eur(kw / 1000 * 6 * DIAS_ANO * PRECIO)])
t4 = tabla("monitor_etiqueta", ["Lo que pone la etiqueta del monitor", "Coste de 1.000 horas", "Coste al año (6 h al día)"], rows)
md["cuanto-consume-ordenador"] = cabecera(
    "cuánto consume un ordenador",
    f"- Calculadora: ordenador gaming 400 W × 0,7 = {kwh(GAM)} por hora; portátil 60 W × 0,7 = {kwh(POR, 3)} por hora.\n"
    f"- Semanas al mes: {num(SEM, 3)}.\n"
    "- Límites E_TEC: Reglamento (UE) 617/2013, anexo II, puntos 1.2.1 y 1.4.1 (categoría A).\n"
    f"- Encendido 24 h: portátil {kwh(POR * 24)} = {eur(POR * 24 * PRECIO)}; juegos {kwh(GAM * 24)} = {eur(GAM * 24 * PRECIO)}.\n"
) + "## Tipos\n\n" + t1 + "\n## Horas\n\n" + t2 + "\n## Límites\n\n" + t3 + "\n## Monitor\n\n" + t4

# ------------------------------------------------------------------ 3. bombillas LED
rows = []
for nombre, watts in (("Bombilla LED de 9 W", 9), ("Bombilla halógena de 50 W", 50)):
    for h in (1, 3, 5):
        k = watts / 1000 * h * DIAS_ANO
        rows.append([nombre, f"{h} h al día", kwh(k, 1), eur(k * PRECIO)])
t1 = tabla("led_bombilla", ["Bombilla", "Uso", "Energía al año", "Coste al año"], rows)
LEDC = 0.09 * 5
HALC = 0.5 * 5
rows = [["10 bombillas LED (90 W)", kwh(LEDC), eur(LEDC * DIAS_MES * PRECIO), eur(LEDC * DIAS_ANO * PRECIO)],
        ["10 bombillas halógenas (500 W)", kwh(HALC), eur(HALC * DIAS_MES * PRECIO), eur(HALC * DIAS_ANO * PRECIO)],
        ["Diferencia", kwh(HALC - LEDC), eur((HALC - LEDC) * DIAS_MES * PRECIO), eur((HALC - LEDC) * DIAS_ANO * PRECIO)]]
t2 = tabla("led_casa", ["Casa con 10 puntos de luz, 5 h al día", "Energía al día", "Coste al mes", "Coste al año"], rows)
t3 = tabla("led_clases", ["Clase", "Eficacia (lúmenes por vatio)"], [
    ["A", "210 o más"], ["B", "De 185 a menos de 210"], ["C", "De 160 a menos de 185"], ["D", "De 135 a menos de 160"],
    ["E", "De 110 a menos de 135"], ["F", "De 85 a menos de 110"], ["G", "Menos de 85"]])
rows = []
for kw in (5, 9, 12, 50):
    rows.append([f"{kw} kWh/1 000 h", eur(kw * PRECIO), eur(kw / 1000 * 3 * DIAS_ANO * PRECIO)])
t4 = tabla("led_etiqueta", ["Lo que pone la etiqueta", "Coste de 1.000 horas", "Coste al año (3 h al día)"], rows)
ahorro_b = (50 - 9) / 1000 * 3 * DIAS_ANO * PRECIO
md["bombillas-led-cuanto-ahorran"] = cabecera(
    "cuánto ahorran las bombillas LED",
    "- Calculadora: 10 bombillas LED = 90 W (9 W cada una); 10 halógenas = 500 W (50 W cada una); 5 h/día; factor 1.\n"
    f"- Ahorro por bombilla a 3 h/día: {eur(ahorro_b)} al año; casa de 10 puntos a 5 h/día: {eur((HALC - LEDC) * DIAS_ANO * PRECIO)}.\n"
    "- Una bombilla consume su potencia en vatios durante 1.000 horas = esa cifra en kWh/1 000 h.\n"
    f"- LED de 9 W, 10 h: {kwh(0.09)} = {eur(0.09 * PRECIO)}; todos los días del año: {eur(0.09 * DIAS_ANO * PRECIO)}.\n"
    f"- Ejemplo de eficacia: 1.000 lm / 9 W = {num(1000 / 9, 0)} lm/W.\n"
) + "## Por bombilla\n\n" + t1 + "\n## Casa\n\n" + t2 + "\n## Clases\n\n" + t3 + "\n## Etiqueta\n\n" + t4

# ------------------------------------------------------------------ 4. ventilador o aire acondicionado
AC = 1.0 * 0.6
VEN = 0.05
rows = []
for nombre, k in (("Ventilador de 50 W", VEN), ("Aire acondicionado de 3.000 frigorías (1.000 W)", AC)):
    rows.append([nombre, kwh(k, 2), eur(k * PRECIO), eur(k * 8 * PRECIO), eur(k * 8 * DIAS_MES * PRECIO), eur(k * 8 * DIAS_MES * 3 * PRECIO)])
t1 = tabla("vent_ac", ["Aparato", "Energía por hora", "Por hora", "Por día (8 h)", "Por mes", "Verano (3 meses)"], rows)
rows = []
for watts in (30, 50, 75, 100):
    k = watts / 1000
    rows.append([w(watts), eur(k * 8 * PRECIO), eur(k * 8 * DIAS_MES * PRECIO), eur(k * 8 * DIAS_MES * 3 * PRECIO)])
t2 = tabla("vent_potencias", ["Ventilador", "Por día (8 h)", "Por mes", "Verano (3 meses)"], rows)
rows = []
for v_h, ac_h in ((8, 0), (6, 2), (4, 4), (0, 8)):
    c = (VEN * v_h + AC * ac_h) * DIAS_MES * PRECIO
    rows.append([f"{v_h} h de ventilador y {ac_h} h de aire", eur(c), eur(c * 3)])
t3 = tabla("vent_combinar", ["Cada día de verano", "Coste al mes", "Coste del verano"], rows)
rows = []
for k in (150, 200, 300, 400):
    rows.append([f"{k} kWh/año", num(k / 350, 2) + " kWh", eur(k / 350 * PRECIO), eur(k * PRECIO)])
t4 = tabla("ac_etiqueta", ["Lo que pone la etiqueta del aire", "Energía por hora de uso equivalente", "Coste por hora",
                          "Coste de las 350 horas de la etiqueta"], rows)
md["ventilador-o-aire-acondicionado"] = cabecera(
    "ventilador o aire acondicionado",
    f"- Calculadora: aire 1.000 W × 0,6 = {kwh(AC)} por hora; ventilador 50 W × 1 = {kwh(VEN)} por hora; 8 h/día.\n"
    f"- El aire gasta {num(AC / VEN, 0)} veces más por hora que un ventilador de 50 W.\n"
    "- Etiqueta del aire: kWh/año calculados con 350 horas equivalentes (Reglamento Delegado 626/2011, anexo VII, cuadro 4).\n"
) + "## Comparativa\n\n" + t1 + "\n## Ventiladores\n\n" + t2 + "\n## Combinar\n\n" + t3 + "\n## Etiqueta\n\n" + t4

for slug, text in md.items():
    (BASE / "calculos" / f"{slug}.md").write_text(text, encoding="utf-8")
(BASE / "scripts" / "tablas_tanda6.json").write_text(json.dumps(tablas, ensure_ascii=False, indent=1), encoding="utf-8")
if __name__ == "__main__":
    print("\n\n".join(md[s] for s in md))
