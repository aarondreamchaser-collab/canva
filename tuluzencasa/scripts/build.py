"""Convierte src/<slug>.txt en articulos/<slug>.html (bloques de Gutenberg).

Formato de src:
  cabecera "clave: valor" (title, excerpt, category, keyword) hasta una línea "---"
  "## " -> H2, "### " -> H3, "- " -> lista, "{{T:clave}}" -> tabla de tablas.json,
  el resto, párrafos separados por línea en blanco (se admite HTML en línea).

Comprobaciones: extracto <= 155 caracteres, palabras, enlaces internos y que cada
importe "X,XX €" del texto aparezca en calculos/<slug>.md.
"""
import json
import re
import sys
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TABLAS = json.loads((BASE / "scripts" / "tablas.json").read_text(encoding="utf-8"))


def p(html):
    return f"<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->"


def h(level, text):
    attrs = "" if level == 2 else f' {{"level":{level}}}'
    return f'<!-- wp:heading{attrs} -->\n<h{level} class="wp-block-heading">{text}</h{level}>\n<!-- /wp:heading -->'


def ul(items):
    lis = "".join(f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->\n" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{lis}</ul>\n<!-- /wp:list -->'


def table(key):
    t = TABLAS[key]
    head = "".join(f"<th>{escape(c)}</th>" for c in t["headers"])
    body = "".join("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in r) + "</tr>" for r in t["rows"])
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table><thead><tr>' + head +
            "</tr></thead><tbody>" + body + "</tbody></table></figure>\n<!-- /wp:table -->")


def build(slug):
    raw = (BASE / "src" / f"{slug}.txt").read_text(encoding="utf-8")
    header, body = raw.split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in header.strip().splitlines())
    blocks, para, items = [], [], []

    def flush():
        if para:
            blocks.append(p(" ".join(para)))
            para.clear()
        if items:
            blocks.append(ul(list(items)))
            items.clear()

    for line in body.splitlines():
        s = line.strip()
        if not s:
            flush()
        elif s.startswith("### "):
            flush(); blocks.append(h(3, s[4:]))
        elif s.startswith("## "):
            flush(); blocks.append(h(2, s[3:]))
        elif s.startswith("- "):
            if para:
                blocks.append(p(" ".join(para))); para.clear()
            items.append(s[2:])
        elif s.startswith("{{T:"):
            flush(); blocks.append(table(s[4:-2]))
        else:
            if items:
                blocks.append(ul(list(items))); items.clear()
            para.append(s)
    flush()
    html = "\n\n".join(blocks) + "\n"
    (BASE / "articulos" / f"{slug}.html").write_text(html, encoding="utf-8")

    text = re.sub(r"<!--.*?-->|<[^>]+>", " ", html)
    words = len(re.findall(r"[\wáéíóúüñÁÉÍÓÚÜÑ€%.,]+", text))
    words = len([w for w in text.split() if re.search(r"\w", w)])
    links = re.findall(r'href="(https://tuluzencasa\.com/[^"]*)"', html)
    calc = "".join(f.read_text(encoding="utf-8") for f in (BASE / "calculos").glob("*.md"))
    importes = set(re.findall(r"\d[\d.]*,\d{2} €", re.sub(r"<[^>]+>", " ", html)))
    faltan = sorted(i for i in importes if i not in calc)
    verificar = re.findall(r"\[VERIFICAR:[^\]]*\]", html)
    meta.update(words=words, links=links, importes_sin_calculo=faltan, verificar=verificar,
                excerpt_len=len(meta["excerpt"]))
    return meta


if __name__ == "__main__":
    slugs = sys.argv[1:] or [f.stem for f in sorted((BASE / "src").glob("*.txt"))]
    out = {}
    for s in slugs:
        m = build(s)
        out[s] = m
        print(f"{s}: {m['words']} palabras · extracto {m['excerpt_len']} car. · enlaces {m['links']}")
        if m["importes_sin_calculo"]:
            print("   ¡IMPORTES QUE NO ESTÁN EN LOS CÁLCULOS!:", m["importes_sin_calculo"])
        for v in m["verificar"]:
            print("  ", v)
    (BASE / "scripts" / "build_meta.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
