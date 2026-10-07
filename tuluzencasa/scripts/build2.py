"""Monta artículos nuevos: src/<slug>.txt -> articulos/<slug>.html (bloques de Gutenberg).

Formato de src (igual que build.py, con anclas):
  cabecera "clave: valor" (title, title_seo, excerpt, category, keyword) hasta "---"
  "## Título {#ancla}" -> H2 con ancla, "### " -> H3, "- " -> lista,
  "{{T:clave}}" -> tabla (tablas.json + tablas_calefaccion.json), resto párrafos.

Añade solo:
  - el índice «En este artículo:» tras el segundo párrafo, con un enlace a cada H2;
  - la línea «Cálculos con precios de octubre de 2026» bajo la primera tabla
    (salvo con «linea_fecha: no» en la cabecera, para artículos cuyas tablas no llevan precios).
Comprueba: extracto <= 155, importes presentes en calculos/*.md, anclas únicas,
palabra clave en la primera frase y en un H2, marcas pendientes.
"""
import json
import re
import sys
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TABLAS = {}
for f in ("tablas.json", "tablas_calefaccion.json", "tablas_calefaccion2.json", "tablas_tanda3.json", "tablas_tanda4.json", "tablas_tanda5.json", "tablas_tanda6.json", "tablas_tanda7.json", "tablas_tanda8.json"):
    TABLAS.update(json.loads((BASE / "scripts" / f).read_text(encoding="utf-8")))
LINEA_FECHA = "Cálculos con precios de octubre de 2026"
IMG_P = BASE / "scripts" / "wp_imagenes_articulos.json"
IMAGENES = json.loads(IMG_P.read_text(encoding="utf-8")) if IMG_P.exists() else {}


def p(html):
    return f"<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->"


def h2(text, anchor):
    return (f'<!-- wp:heading {{"anchor":"{anchor}"}} -->\n'
            f'<h2 id="{anchor}" class="wp-block-heading">{text}</h2>\n<!-- /wp:heading -->')


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def ul(items):
    lis = "\n\n".join(f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{lis}</ul>\n<!-- /wp:list -->'


def table(key):
    t = TABLAS[key]
    head = "".join(f"<th>{escape(c)}</th>" for c in t["headers"])
    body = "".join("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in r) + "</tr>" for r in t["rows"])
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table><thead><tr>' + head +
            "</tr></thead><tbody>" + body + "</tbody></table></figure>\n<!-- /wp:table -->")


def caja(titulo, cuerpo):
    """Caja «Dato clave» / «Actualizado»: grupo .tl-dato (estilo en el fragmento «Efectos tuluzencasa»)."""
    t = (f'<!-- wp:paragraph {{"className":"tl-dato-t"}} -->\n<p class="tl-dato-t">{titulo}</p>\n<!-- /wp:paragraph -->')
    return ('<!-- wp:group {"className":"tl-dato","layout":{"type":"default"}} -->\n<div class="wp-block-group tl-dato">'
            + "\n\n".join([t] + cuerpo) + '</div>\n<!-- /wp:group -->')


def imagen(key):
    i = IMAGENES[key]
    cap = f'<figcaption class="wp-element-caption">{i["pie"]}</figcaption>' if i.get("pie") else ""
    return (f'<!-- wp:image {{"id":{i["id"]},"sizeSlug":"full","linkDestination":"none"}} -->\n'
            f'<figure class="wp-block-image size-full"><img src="{i["url"]}" alt="{escape(i["alt"])}" class="wp-image-{i["id"]}"/>{cap}</figure>\n<!-- /wp:image -->')


def build(slug):
    raw = (BASE / "src" / f"{slug}.txt").read_text(encoding="utf-8")
    header, body = raw.split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in header.strip().splitlines())
    blocks, para, items, toc = [], [], [], []
    n_par, toc_pos, tabla_vista = 0, None, False

    def flush():
        nonlocal n_par, toc_pos
        if para:
            blocks.append(p(" ".join(para)))
            para.clear()
            n_par += 1
            if n_par == 2 and toc_pos is None:
                toc_pos = len(blocks)
        if items:
            blocks.append(ul(list(items)))
            items.clear()

    caja_abierta = None
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("{{CAJA:"):
            flush(); caja_abierta = (s[7:-2], len(blocks)); continue
        if s == "{{/CAJA}}":
            flush(); tit, ini = caja_abierta; cuerpo = blocks[ini:]; del blocks[ini:]
            blocks.append(caja(tit, cuerpo)); caja_abierta = None; continue
        if s.startswith("{{IMG:"):
            flush(); blocks.append(imagen(s[6:-2])); continue
        if not s:
            flush()
        elif s.startswith("### "):
            flush(); blocks.append(h3(s[4:]))
        elif s.startswith("## "):
            flush()
            m = re.match(r"## (.+?) \{#([a-z0-9-]+)\}$", s)
            assert m, f"H2 sin ancla: {s}"
            blocks.append(h2(m.group(1), m.group(2))); toc.append((m.group(1), m.group(2)))
        elif s.startswith("- "):
            if para:
                flush()
            items.append(s[2:])
        elif s.startswith("{{T:"):
            flush(); blocks.append(table(s[4:-2]))
            if not tabla_vista and meta.get("linea_fecha") != "no":
                blocks.append(p(LINEA_FECHA)); tabla_vista = True
        else:
            if items:
                blocks.append(ul(list(items))); items.clear()
            para.append(s)
    flush()
    indice = [p("En este artículo:"), ul([f'<a href="#{a}">{re.sub("<[^>]+>", "", t)}</a>' for t, a in toc])]
    blocks[toc_pos:toc_pos] = indice
    html = "\n\n".join(blocks) + "\n"
    (BASE / "articulos" / f"{slug}.html").write_text(html, encoding="utf-8")

    text = re.sub(r"<!--.*?-->|<[^>]+>", " ", html)
    calc = "".join(f.read_text(encoding="utf-8") for f in (BASE / "calculos").glob("*.md"))
    anclas = [a for _, a in toc]
    primera = re.sub(r"<[^>]+>", "", re.search(r"<p>(.*?)</p>", html).group(1))
    kw = meta["keyword"].lower()
    meta.update(
        words=len([w for w in text.split() if re.search(r"\w", w)]),
        excerpt_len=len(meta["excerpt"]),
        h2=len(toc),
        anclas_unicas=len(set(anclas)) == len(anclas),
        kw_primera_frase=kw in re.split(r"(?<=[?.])\s", primera)[0].lower(),
        kw_en_h2=any(kw in t.lower() for t, _ in toc),
        importes_sin_calculo=sorted({i for i in re.findall(r"\d[\d.]*,\d{2} €", text) if i not in calc}),
        marcas=re.findall(r"\[(?:VERIFICAR|CONFIRMAR|AFILIADO)[^\]]*\]", html),
        enlaces=re.findall(r'href="(https?://[^"]+)"', html),
    )
    return meta


if __name__ == "__main__":
    out = {}
    for s in sys.argv[1:]:
        m = build(s)
        out[s] = m
        print(f"{s}: {m['words']} palabras · {m['h2']} H2 · extracto {m['excerpt_len']} · kw 1.ª frase {m['kw_primera_frase']} · kw en H2 {m['kw_en_h2']} · anclas únicas {m['anclas_unicas']}")
        if m["importes_sin_calculo"]:
            print("   ¡IMPORTES SIN CÁLCULO!:", m["importes_sin_calculo"])
        for x in m["marcas"]:
            print("  ", x)
    prev = BASE / "scripts" / "build2_meta.json"
    allm = json.loads(prev.read_text(encoding="utf-8")) if prev.exists() else {}
    allm.update(out)
    prev.write_text(json.dumps(allm, ensure_ascii=False, indent=1), encoding="utf-8")
