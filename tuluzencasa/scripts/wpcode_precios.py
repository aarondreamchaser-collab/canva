"""Prepara los fragmentos de WPCode con los precios nuevos, para pegarlos a mano. No toca la web.

Uso: python3 scripts/wpcode_precios.py [--precios scripts/precios_referencia_propuesta.json]
Deja en revision-precios/wpcode/: consumo3.min.js y potencia3.min.js (calculadoras) y
2-plantilla-tuluzencasa.php (frase del pie). Compara siempre con los actuales antes de pegar.
"""
import argparse, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("--precios", default=str(BASE / "scripts" / "precios_referencia_propuesta.json"))
a = ap.parse_args()
v = json.loads((BASE / "scripts" / "precios_referencia.json").read_text())
n = json.loads(Path(a.precios).read_text())
fmt = lambda x, d: f"{x:.{d}f}".replace(".", ",")
p2 = lambda x: fmt(x, 2) if abs(round(x, 2) - x) < 1e-9 else fmt(x, 3)
out = BASE / "revision-precios" / "wpcode"
out.mkdir(parents=True, exist_ok=True)

tmp = Path(tempfile.mkdtemp()) / "calculadoras-v3"
shutil.copytree(BASE / "calculadoras-v3", tmp, ignore=shutil.ignore_patterns("capturas", "pruebas", "respaldo-antiguas"))
js_v = lambda x: repr(round(x, 4)).rstrip("0").rstrip(".") if "." in repr(x) else repr(x)
for f in ("consumo3.src.js", "potencia3.src.js"):
    s = (tmp / f).read_text()
    s = s.replace(f"IVA={1 + v['iva']:g}", f"IVA={1 + n['iva']:g}").replace(f"IMP={1 + v['iva']:g}*{1 + v['impuesto_electrico']:g}", f"IMP={1 + n['iva']:g}*{1 + n['impuesto_electrico']:g}")
    s = s.replace(f"POT_DIA={v['pot_dia']:g}", f"POT_DIA={n['pot_dia']:g}").replace(f"CONTADOR={v['contador_mes']:g}", f"CONTADOR={n['contador_mes']:g}")
    s = s.replace(f"pu:{v['energia']:g},pp:{v['tramos']['punta']:g},pl:{v['tramos']['llano']:g},pv:{v['tramos']['valle']:g}",
                  f"pu:{n['energia']:g},pp:{n['tramos']['punta']:g},pl:{n['tramos']['llano']:g},pv:{n['tramos']['valle']:g}")
    s = s.replace(f"{p2(v['energia'])} €/kWh sin impuestos ({fmt(v['precio_con_impuestos'], 3)} €", f"{p2(n['energia'])} €/kWh sin impuestos ({fmt(n['precio_con_impuestos'], 3)} €")
    t_v, t_n = v["tramos"], n["tramos"]
    s = s.replace(f"punta {p2(t_v['punta'])}, llano {p2(t_v['llano'])} y valle {p2(t_v['valle'])}", f"punta {p2(t_n['punta'])}, llano {p2(t_n['llano'])} y valle {p2(t_n['valle'])}")
    s = s.replace(f"impuesto eléctrico del {fmt(v['impuesto_electrico'] * 100, 2)} % e IVA del {v['iva'] * 100:g} %",
                  f"impuesto eléctrico del {fmt(n['impuesto_electrico'] * 100, 2)} % e IVA del {n['iva'] * 100:g} %")
    (tmp / f).write_text(s)
r = subprocess.run([sys.executable, "construir.py"], cwd=tmp, capture_output=True, text=True)
if r.returncode:
    sys.exit(r.stdout + r.stderr)
for f in ("consumo3.min.js", "potencia3.min.js"):
    shutil.copy(tmp / f, out / f)
pl = (BASE / "rediseno" / "v2" / "para-pegar" / "2-plantilla-tuluzencasa.php").read_text()
pl = pl.replace(f"Precio de referencia: {fmt(v['precio_con_impuestos'], 3)} €/kWh", f"Precio de referencia: {fmt(n['precio_con_impuestos'], 3)} €/kWh")
(out / "2-plantilla-tuluzencasa.php").write_text(pl)
for f in ("consumo3.src.js", "potencia3.src.js"):
    a_, b_ = (BASE / "calculadoras-v3" / f).read_text(), (tmp / f).read_text()
    print(f, "cambios:", sum(1 for x, y in zip(a_.splitlines(), b_.splitlines()) if x != y))
print("Listo en", out.relative_to(BASE))
