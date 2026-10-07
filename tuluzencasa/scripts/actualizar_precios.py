"""Cambia los precios de referencia en toda la web de una vez. Por defecto SOLO SIMULA.

Uso:
  python3 scripts/actualizar_precios.py [--precios scripts/precios_referencia_propuesta.json]
      -> simulación: recalcula todo en una copia aparte y deja en revision-precios/ lo que cambiaría
  python3 scripts/actualizar_precios.py --aplicar
      -> solo si la simulación no deja dudas sin resolver (revision-precios/decisiones.json):
         copia de cada entrada y página, comprueba «modified», sube el contenido nuevo y
         copia el nuevo precios_referencia.json al repositorio. No cambia el estado de nada.

Cómo funciona (trabaja sobre el contenido PUBLICADO, no sobre src/, porque hay retoques hechos en vivo):
  1. Copia el proyecto a una carpeta temporal, pone ahí los precios nuevos y ejecuta todos los scripts de cálculo.
  2. Tablas: cada tabla publicada que coincide con una tabla de los scripts (tablas*.json) se sustituye entera.
  3. Texto: cada importe «N,NN €» (y precios «N,NNN €/kWh») se cambia con la correspondencia antiguo → nuevo
     sacada de calculos/<artículo>.md y de calculos/factura/salida/*.json. Si un importe antiguo tiene dos valores
     nuevos posibles, o ninguno, se apunta en revision-precios/resumen.md para decidirlo a mano.
  4. «Cálculos con precios de <mes>» pasa al mes nuevo.
Lee WP_USER y WP_APP_PASSWORD (nunca los imprime).
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from collections import defaultdict
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
from subir2 import req  # noqa: E402

TMP = Path(os.environ.get("TL_TMP", tempfile.gettempdir())) / "tuluzencasa-precios"
REV = BASE / "revision-precios"
CALC = ["calculos.py", "calculos_calefaccion.py", "calculos_calefaccion2.py"] + [f"calculos_tanda{i}.py" for i in range(3, 9)] + ["calculos_comunidades_a.py", "calculos_tanda9.py"]
FACT = ["como_leer_la_factura.py", "pvpc_o_mercado_libre.py", "pvpc_factura_ejemplo.py", "que_potencia_contratar.py"]
# entrada publicada -> archivos de cálculo que la explican
MD = {
    "bomba-calor-radiadores-electricos": ["bomba-de-calor-o-radiadores-electricos"],
    "cuanto-consume-deshumidificador": ["cuanto-consume-un-deshumidificador"],
    "cuanto-consume-estufa-electrica": ["cuanto-consume-una-estufa-electrica"],
    "cuanto-consume-manta-electrica": ["cuanto-consume-una-manta-electrica"],
    "cuanto-consumen-emisores-termicos": ["cuanto-consumen-los-emisores-termicos"],
    "radiador-aceite-convector-calefactor": ["radiador-de-aceite-convector-o-calefactor"],
    "metodologia": ["metodologia"],
}
SALIDA = {
    "como-leer-factura-luz": ["como-leer-la-factura-de-la-luz"],
    "pvpc-mercado-libre": ["pvpc-o-mercado-libre", "pvpc-factura-ejemplo"],
    "que-potencia-contratar": ["que-potencia-contratar"],
}
IMPORTE = re.compile(r"(?<![\d,.])(\d{1,3}(?:\.\d{3})*,\d{2,3})(?=\s?€)")


def fmt(x, dec):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def recalcular(precios):
    if TMP.exists():
        shutil.rmtree(TMP)
    shutil.copytree(BASE, TMP, ignore=shutil.ignore_patterns(".git", "imagenes-destacadas", "rediseno", "capturas", "revision-precios", "__pycache__", "*.pdf"))
    shutil.copy(precios, TMP / "scripts" / "precios_referencia.json")
    for f in CALC:
        subprocess.run([sys.executable, f], cwd=TMP / "scripts", check=True, capture_output=True)
    for f in FACT:
        subprocess.run([sys.executable, f], cwd=TMP / "calculos" / "factura", check=True, capture_output=True)


def tablas(raiz):
    t = {}
    for f in sorted((raiz / "scripts").glob("tablas*.json")):
        t.update(json.loads(f.read_text(encoding="utf-8")))
    return t


def html_tabla(t):
    head = "".join(f"<th>{escape(c)}</th>" for c in t["headers"])
    body = "".join("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in r) + "</tr>" for r in t["rows"])
    return "<table><thead><tr>" + head + "</tr></thead><tbody>" + body + "</tbody></table>"


def pares_texto(viejo, nuevo):
    """Alinea los números de dos textos con la misma estructura: devuelve [(antiguo, nuevo)] de los importes en €."""
    num = re.compile(r"\d[\d.]*,\d+(?=\s?€)|\d[\d.]*,\d+")
    a, b = num.findall(viejo), num.findall(nuevo)
    if len(a) != len(b):
        return None
    return [(x, y) for x, y in zip(a, b)]


def pares_json(viejo, nuevo, out):
    if isinstance(viejo, dict):
        for k in viejo:
            if k in nuevo:
                pares_json(viejo[k], nuevo[k], out)
    elif isinstance(viejo, list):
        for x, y in zip(viejo, nuevo):
            pares_json(x, y, out)
    elif isinstance(viejo, (int, float)) and not isinstance(viejo, bool) and isinstance(nuevo, (int, float)):
        for d in (2, 3):
            out.append((fmt(viejo, d), fmt(nuevo, d)))


def correspondencias(slug):
    pares, avisos = [], []
    for m in MD.get(slug, [slug]):
        a, b = BASE / "calculos" / f"{m}.md", TMP / "calculos" / f"{m}.md"
        if a.exists():
            p = pares_texto(a.read_text(), b.read_text())
            if p is None:
                avisos.append(f"{m}.md: estructura distinta, no se puede alinear")
            else:
                pares += p
    for m in SALIDA.get(slug, []):
        a, b = BASE / "calculos" / "factura" / "salida" / f"{m}.json", TMP / "calculos" / "factura" / "salida" / f"{m}.json"
        pares_json(json.loads(a.read_text()), json.loads(b.read_text()), pares)
    mapa = defaultdict(set)
    for x, y in pares:
        mapa[x].add(y)
    return mapa, avisos


def mapa_global():
    g = defaultdict(set)
    for a in (BASE / "calculos").glob("*.md"):
        p = pares_texto(a.read_text(), (TMP / "calculos" / a.name).read_text())
        for x, y in p or []:
            g[x].add(y)
    return g


def procesar(doc, viejo_t, nuevo_t, g, ref_v, ref_n, decisiones):
    slug, raw = doc["slug"], doc["raw"]
    nuevo, notas = raw, []
    # 1. tablas enteras
    n_tab = 0
    for k, t in viejo_t.items():
        h = html_tabla(t)
        if h in nuevo and k in nuevo_t and html_tabla(nuevo_t[k]) != h:
            nuevo = nuevo.replace(h, html_tabla(nuevo_t[k]))
            n_tab += 1
    p2 = lambda x: fmt(x, 2) if abs(round(x, 2) - x) < 1e-9 else fmt(x, 3)
    n_lit = 0
    # 2a. textos de precios que no van seguidos de «€» y la fecha de los precios
    lit = [(f"Cálculos con precios de {ref_v['mes_precios']}", f"Cálculos con precios de {ref_n['mes_precios']}")]
    tv, tn = ref_v["tramos"], ref_n["tramos"]
    lit.append((f"{p2(tv['punta'])}, {p2(tv['llano'])} y {p2(tv['valle'])}", f"{p2(tn['punta'])}, {p2(tn['llano'])} y {p2(tn['valle'])}"))
    for a, b in lit:
        if a != b and a in nuevo:
            nuevo = nuevo.replace(a, b)
            n_lit += 1
    # 2. importes en el texto (fuera de las tablas ya cambiadas)
    mapa, avisos = correspondencias(slug)
    notas += avisos
    dec = decisiones.get(slug, {})
    # precios unitarios de referencia: se cambian por su valor nuevo cuando van seguidos de €/kWh, € de energía o € por kW
    unit = {p2(ref_v["energia"]): p2(ref_n["energia"]), fmt(ref_v["precio_con_impuestos"], 3): fmt(ref_n["precio_con_impuestos"], 3),
            p2(ref_v["pot_dia"]): p2(ref_n["pot_dia"])}
    fv, fn = ref_v["factor_redondeado"], ref_n["factor_redondeado"]
    for k in ref_v["tramos"]:
        unit[p2(ref_v["tramos"][k])] = p2(ref_n["tramos"][k])
        unit[fmt(ref_v["tramos"][k] * fv, 3)] = fmt(ref_n["tramos"][k] * fn, 3)
    UNIT = re.compile(r"(?<![\d,.])(\d,\d{2,3})(?=\s?€(?:/kWh| de energía| por kW|/kW| el kWh| con el impuesto))")
    nuevos_unit = set(unit.values())
    ratio = ref_n["precio_con_impuestos"] / ref_v["precio_con_impuestos"]
    a_num = lambda v: float(v.replace(".", "").replace(",", "."))
    trozos = re.split(r"(<table>.*?</table>)", nuevo, flags=re.S)
    cambios, dudas, elegidos = n_lit, [], []
    for i, tr in enumerate(trozos):
        if tr.startswith("<table>"):
            continue

        def cambia(m):
            nonlocal cambios
            v = m.group(1)
            ctx = re.sub(r"<[^>]+>", "", tr[max(0, m.start() - 90):m.end() + 40]).replace("\n", " ")
            if v in dec:
                cambios += dec[v] != v
                return dec[v]
            if UNIT.match(tr, m.start()) and v in nuevos_unit and n_lit:
                return v  # ya cambiado por la frase de los tramos
            if UNIT.match(tr, m.start()) and v in unit:
                cambios += unit[v] != v
                return unit[v]
            dec_v = len(v.split(",")[1])
            cand = {c for c in (mapa.get(v) or g.get(v) or set()) if len(c.split(",")[1]) == dec_v}
            if len(cand) == 1:
                c = cand.pop()
                cambios += c != v
                return c
            if cand:
                c = min(cand, key=lambda x: abs(a_num(x) - a_num(v) * ratio))
                elegidos.append(f"«{v} €» → «{c} €» (el más cercano a la proporción de {fmt(ratio, 3)} entre {sorted(cand)}): …{ctx}…")
                cambios += c != v
                return c
            dudas.append(f"«{v} €» sin correspondencia; con la proporción serían {fmt(a_num(v) * ratio, 2)} €: …{ctx}…")
            return v
        trozos[i] = IMPORTE.sub(cambia, tr)
    nuevo = "".join(trozos)
    # 3. porcentajes que cambian con el precio: solo se avisan
    for m_ in MD.get(slug, [slug]):
        a_, b_ = BASE / "calculos" / f"{m_}.md", TMP / "calculos" / f"{m_}.md"
        if not a_.exists():
            continue
        pa, pb = re.findall(r"(\d+(?:,\d+)?) ?%", a_.read_text()), re.findall(r"(\d+(?:,\d+)?) ?%", b_.read_text())
        if len(pa) == len(pb):
            for x, y in sorted({(x, y) for x, y in zip(pa, pb) if x != y}):
                if re.search(rf"(?<![\d,]){re.escape(x)} ?%", re.sub(r"<table>.*?</table>", "", nuevo, flags=re.S)):
                    notas.append(f"Porcentaje que cambia: «{x} %» → «{y} %» (revisar el texto a mano)")
    for m_ in SALIDA.get(slug, []):
        ja = json.loads((BASE / "calculos" / "factura" / "salida" / f"{m_}.json").read_text())
        jb = json.loads((TMP / "calculos" / "factura" / "salida" / f"{m_}.json").read_text())
        for k, x in ja.items():
            if any(w in k for w in ("pct", "peso", "equilibrio")) and isinstance(x, float) and round(x * 100) != round(jb[k] * 100):
                notas.append(f"Porcentaje que cambia ({k}): «{round(x * 100)} %» → «{round(jb[k] * 100)} %» (revisar el texto a mano)")
    return nuevo, n_tab, cambios, dudas, notas + elegidos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--precios", default=str(BASE / "scripts" / "precios_referencia_propuesta.json"))
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()
    ref_v = json.loads((BASE / "scripts" / "precios_referencia.json").read_text())
    ref_n = json.loads(Path(a.precios).read_text())
    recalcular(a.precios)
    viejo_t, nuevo_t, g = tablas(BASE), tablas(TMP), mapa_global()
    REV.mkdir(exist_ok=True)
    dec_p = REV / "decisiones.json"
    decisiones = json.loads(dec_p.read_text()) if dec_p.exists() else {}

    docs = []
    for tipo in ("posts", "pages"):
        c, lista = req("GET", f"/wp/v2/{tipo}?per_page=100&status=publish,draft&context=edit&_fields=id,slug,modified,content,excerpt")
        if c == 403:
            sys.exit("403: posible firewall/HackGuardian. Paro.")
        docs += [dict(tipo=tipo, id=d["id"], slug=d["slug"], modified=d["modified"], raw=d["content"]["raw"],
                     extracto=(d.get("excerpt") or {}).get("raw", "")) for d in lista]

    resumen = [f"# Simulación del cambio de precios\n\nDe {ref_v['precio_con_impuestos']} a {ref_n['precio_con_impuestos']} €/kWh con impuestos "
               f"(energía {ref_v['energia']} → {ref_n['energia']}; potencia {ref_v['pot_dia']} → {ref_n['pot_dia']} €/kW y día).\n"]
    total_dudas, cambiados = 0, []
    for d in docs:
        nuevo, n_tab, n_cam, dudas, notas = procesar(d, viejo_t, nuevo_t, g, ref_v, ref_n, decisiones)
        ext, _, _, dudas_e, _ = procesar(dict(d, raw=d["extracto"]), {}, {}, g, ref_v, ref_n, decisiones)
        dudas += [f"(extracto) {x}" for x in dudas_e]
        d["extracto_nuevo"] = ext
        if nuevo == d["raw"] and ext == d["extracto"] and not dudas:
            continue
        (REV / f"{d['slug']}.html").write_text(nuevo)
        resumen.append(f"## {d['slug']} ({d['tipo']} {d['id']})\n\n- Tablas sustituidas: {n_tab} · importes y textos cambiados: {n_cam}")
        if ext != d["extracto"]:
            resumen.append(f"- Extracto: «{d['extracto']}» → «{ext}»")
        resumen += [f"- {x}" for x in notas] + [f"- **DUDA** {x}" for x in dudas]
        resumen.append("")
        total_dudas += len(dudas)
        cambiados.append((d, nuevo))
    resumen.insert(1, f"Documentos con cambios: {len(cambiados)} · dudas por resolver: {total_dudas}\n")
    (REV / "resumen.md").write_text("\n".join(resumen), encoding="utf-8")
    print(f"Simulación: {len(cambiados)} documentos con cambios, {total_dudas} dudas. Ver {REV.relative_to(BASE)}/resumen.md")

    if not a.aplicar:
        return
    if total_dudas:
        sys.exit("Hay dudas sin resolver: añádelas a revision-precios/decisiones.json y vuelve a simular.")
    copia = BASE / "rediseno" / "copia-seguridad" / f"precios-{ref_n['mes_precios'].replace(' ', '-')}"
    copia.mkdir(parents=True, exist_ok=True)
    for d, nuevo in cambiados:
        (copia / f"{d['tipo']}-{d['id']}-{d['slug']}-antes.html").write_text(d["raw"])
        c, chk = req("GET", f"/wp/v2/{d['tipo']}/{d['id']}?context=edit&_fields=modified")
        if chk["modified"] != d["modified"]:
            print(f"{d['slug']}: ha cambiado durante la simulación; no lo toco"); continue
        cuerpo = {"content": nuevo}
        if d["extracto_nuevo"] != d["extracto"]:
            cuerpo["excerpt"] = d["extracto_nuevo"]
        c, _ = req("POST", f"/wp/v2/{d['tipo']}/{d['id']}", cuerpo)
        if "excerpt" in cuerpo:  # en esta web la descripción de Rank Math es el extracto
            req("POST", "/rankmath/v1/updateMeta", {"objectType": "post", "objectID": d["id"], "meta": {"rank_math_description": d["extracto_nuevo"]}})
        print(f"{d['slug']}: {c}")
    shutil.copy(a.precios, BASE / "scripts" / "precios_referencia.json")
    for f in CALC:
        subprocess.run([sys.executable, f], cwd=BASE / "scripts", check=True, capture_output=True)
    for f in FACT:
        subprocess.run([sys.executable, f], cwd=BASE / "calculos" / "factura", check=True, capture_output=True)
    print("Hecho. Falta: calculadoras (WPCode), frase del pie (plantilla) y src/ de cada artículo.")


if __name__ == "__main__":
    main()
