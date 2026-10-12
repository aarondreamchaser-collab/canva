"""Zonas climáticas por provincia y altitud: CTE DB-HE (2019), anejo B, tabla a (DBHE.pdf, página 46).
Lee los separadores de celda de cada fila y los asigna a las bandas de altitud de la cabecera.
Se comprueba con las 19 provincias de cte_zonas.json (tanda A y Aragón) antes de escribir las nuevas."""
import json, sys
import pdfplumber
from pathlib import Path
F = Path(__file__).parent
p = pdfplumber.open(F / "DBHE.pdf").pages[45]
words = p.extract_words()
# bordes de las bandas de altitud de la cabecera (x) y su altitud inicial (m)
EDGES = [168, 199, 217, 231, 245, 260, 274, 288, 302, 317, 331, 345, 359, 373, 388, 402, 416, 431, 445, 459, 476, 491, 507, 522, 538]
DESDE = [0, 51, 101, 151, 201, 251, 301, 351, 401, 451, 501, 551, 601, 651, 701, 751, 801, 851, 901, 951, 1001, 1051, 1251, 1301]
def banda(x):
    return min(range(len(EDGES)), key=lambda i: abs(EDGES[i] - x))
def fila(nombre_top):
    top = nombre_top
    seps = sorted({round(r["x0"]) for r in p.rects if r["top"] - 3 <= top <= r["bottom"] + 1 and r["width"] <= 2 and 160 <= r["x0"] <= 540} | {168, 538})
    seps = [s for i, s in enumerate(seps) if i == 0 or s - seps[i - 1] > 3]
    ws = [w for w in words if abs(w["top"] - top) < 2 and w["x0"] >= 160]
    out = []
    for w in ws:
        c = (w["x0"] + w["x1"]) / 2
        a = max(s for s in seps if s <= c); b = min(s for s in seps if s > c)
        i, j = banda(a), banda(b)
        out.append({"zona": w["text"], "desde": DESDE[i], "hasta": None if j == len(EDGES) - 1 else DESDE[j] - 1})
    return out
NOMBRES = {"Coruña,": "A Coruña", "Palmas,": "Las Palmas", "Santa": "Santa Cruz de Tenerife"}
filas = {}
for w in words:
    if w["x0"] < 60 and 235 < w["top"] < 750:
        filas[NOMBRES.get(w["text"], w["text"])] = w["top"]
prev = json.loads((F / "cte_zonas.json").read_text())
mal = [k for k in prev if fila(filas[k.split("/")[0] if k.split("/")[0] in filas else k]) != prev[k]]
print("comprobación con las 19 ya usadas:", "OK" if not mal else mal)
if mal: sys.exit(1)
NUEVAS = ["A Coruña", "Lugo", "Ourense", "Pontevedra", "Ávila", "Burgos", "León", "Palencia", "Salamanca", "Segovia", "Soria",
          "Valladolid", "Zamora", "Araba/Álava", "Bizkaia", "Gipuzkoa", "Las Palmas", "Santa Cruz de Tenerife"]
nuevo = {k: fila(filas[k]) for k in NUEVAS}
for k, v in nuevo.items(): print(k, v)
(F / "cte_zonas.json").write_text(json.dumps({**prev, **nuevo}, ensure_ascii=False, indent=1))
