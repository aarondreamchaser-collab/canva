"""PVGIS 5.2 (JRC) para las capitales de provincia de la tanda A, con la misma configuración que
el artículo de placas solares: 1 kWp, 30° de inclinación, orientación sur, 14 % de pérdidas. Sin clave."""
import json, time, urllib.request
from pathlib import Path
CAP = {  # coordenadas del centro de cada capital
    "almeria": (36.834, -2.464), "cadiz": (36.527, -6.289), "cordoba": (37.888, -4.779), "granada": (37.177, -3.599),
    "huelva": (37.261, -6.945), "jaen": (37.779, -3.785), "malaga": (36.721, -4.421), "sevilla": (37.389, -5.984),
    "barcelona": (41.385, 2.173), "girona": (41.979, 2.821), "lleida": (41.617, 0.620), "tarragona": (41.119, 1.245),
    "madrid": (40.417, -3.704), "alicante": (38.345, -0.481), "castellon": (39.986, -0.051), "valencia": (39.470, -0.376),
}
D = Path(__file__).parent / "pvgis"
for k, (la, lo) in CAP.items():
    f = D / f"{k}.json"
    if f.exists():
        continue
    u = f"https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?lat={la}&lon={lo}&peakpower=1&loss=14&angle=30&aspect=0&outputformat=json"
    f.write_text(urllib.request.urlopen(u, timeout=60).read().decode())
    time.sleep(1.5)
for k in CAP:
    d = json.loads((D / f"{k}.json").read_text())
    print(k, round(d["outputs"]["totals"]["fixed"]["E_y"]), d["inputs"]["location"]["elevation"])
