"""Vista previa del rediseño 2 sobre el HTML real publicado (no toca la web).

Uso: python3 construir_preview.py DIR_BASE DIR_SALIDA
DIR_BASE tiene home.html, art.html, art2.html, cat.html y calc.html descargados de la web.
Necesita WP_USER y WP_APP_PASSWORD para leer el contenido de las entradas (solo lectura).
"""
import json, os, re, subprocess, sys, pathlib, base64, urllib.request

V2 = pathlib.Path(__file__).resolve().parent.parent
REDIS = V2.parent
BASE, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
AUTH = 'Basic ' + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()


def api(path):
    r = urllib.request.Request('https://tuluzencasa.com/wp-json/wp/v2' + path, headers={'Authorization': AUTH, 'User-Agent': 'tl-preview'})
    return json.loads(urllib.request.urlopen(r, timeout=60).read())


CSS = (V2 / 'wpcode-diseno-v2.css').read_text()
BANNERS = (REDIS / 'banners' / 'banners-tuluzencasa.min.html').read_text()
EFECTOS = (REDIS / 'efectos' / 'efectos-tuluzencasa.html').read_text()
CATS = [{'slug': c['slug'], 'name': c['name'], 'count': c['count']} for c in api('/categories?per_page=100') if c['count'] > 0]
PHP = V2 / 'preview' / 'plantilla-para-harness.php'


def php(ctx):
    f = OUT / '_ctx.json'
    f.write_text(json.dumps(ctx))
    r = subprocess.run(['php', str(V2 / 'preview' / 'harness.php'), str(f), str(PHP)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def comun(h, salida):
    i = h.index('<style class="wpcode-css-snippet">') + len('<style class="wpcode-css-snippet">')
    h = h[:i] + CSS + h[h.index('</style>', i):]
    if '<script id="tlb-js">' in h:
        a = h.index('<!-- Banners y efectos tuluzencasa') if '<!-- Banners y efectos tuluzencasa' in h else h.index('<style id="tlb-css">')
        b = h.index('</script>', h.index('<script id="tlb-js">')) + len('</script>')
        h = h[:a] + BANNERS + h[b:]
    else:
        h = h.replace('</head>', BANNERS + '</head>', 1)
    h = h.replace('<div class="site-footer">', salida['generate_before_footer'] + '<div class="site-footer">', 1)
    if 'tl-efectos-css' not in h:
        h = h.replace('</body>', EFECTOS + '</body>', 1)
    return h


def render_bloques(b, home_base):
    b = re.sub(r'<!-- wp:search .*?/-->', lambda m: (
        '<form role="search" method="get" action="https://tuluzencasa.com/" class="wp-block-search__button-outside wp-block-search__text-button tl-buscador wp-block-search">'
        '<label class="wp-block-search__label screen-reader-text" for="wp-block-search__input-9">Buscar en Tu luz en casa</label>'
        '<div class="wp-block-search__inside-wrapper"><input class="wp-block-search__input" id="wp-block-search__input-9" placeholder="Busca: lavadora, potencia, bono social…" value="" type="search" name="s" required />'
        '<button aria-label="Buscar" class="wp-block-search__button wp-element-button" type="submit">Buscar</button></div></form>'), b, flags=re.S)
    cats = re.search(r'<ul class="tl-cats">.*?</ul>', home_base, re.S).group(0)
    b = b.replace('[tl_categorias]', cats)
    q0 = home_base.index('<div class="wp-block-query tl-ultimos')
    q = home_base[q0:home_base.index('</ul></div>', q0) + len('</ul></div>')]
    b = re.sub(r'<div class="wp-block-query tl-ultimos">.*?<!-- /wp:query -->', lambda m: q, b, flags=re.S)
    b = re.sub(r'<!-- /?wp:[^>]*?-->', '', b)
    return b


home = (BASE / 'home.html').read_text()
s = php({'tipo': 'page', 'slug': 'inicio', 'cats': CATS})
portada = render_bloques((V2 / 'portada-v2.html').read_text(), home)
a = home.index('<div class="entry-content" itemprop="text">') + len('<div class="entry-content" itemprop="text">')
b = home.index('</article>', a)
fin = home.rfind('</div>', a, b)
fin = home.rfind('</div>', a, fin)
h = home[:a] + portada + home[fin:]
(OUT / 'home.html').write_text(comun(h, s))

for nombre, slug in (('art', 'cuanto-consume-lavadora'), ('art2', 'que-potencia-contratar')):
    post = api(f'/posts?slug={slug}&context=edit&_fields=id,content,excerpt')[0]
    s = php({'tipo': 'post', 'id': post['id'], 'contenido': post['content']['raw'], 'extracto': post['excerpt']['raw'], 'cats': CATS})
    h = (BASE / f'{nombre}.html').read_text()
    t = s['generate_after_entry_title']
    k = t.index('<div class="tl-art-extra"')
    sub, extra = t[:k], t[k:]
    h = h.replace('<div class="entry-meta">', sub + '<div class="entry-meta">', 1)
    m = h.index('<div class="entry-meta">')
    e = h.index('</div>', m) + len('</div>')
    h = h[:e] + extra + h[e:]
    h = h.replace('<div class="inside-right-sidebar">', '<div class="inside-right-sidebar">' + s['generate_before_right_sidebar_content'], 1)
    (OUT / f'{nombre}.html').write_text(comun(h, s))

cat = api('/categories?slug=consumo')[0]
s = php({'tipo': 'cat', 'cat': {'count': cat['count']}, 'cats': CATS})
h = (BASE / 'cat.html').read_text()
assert s['sidebar'] == 'no-sidebar'
h = re.sub(r'(<body[^>]*class="[^"]*)\bright-sidebar\b', r'\1no-sidebar', h, count=1)
i = h.index('<div class="widget-area sidebar is-right-sidebar"')
prof, k = 0, i
for m in re.finditer(r'<div\b|</div>', h[i:]):
    prof += 1 if m.group(0) == '<div' else -1
    if prof == 0:
        k = i + m.end()
        break
h = h[:i] + h[k:]
h = h.replace('</div>\t\t</header>', '</div>' + s['generate_after_archive_description'] + '\t\t</header>', 1)
(OUT / 'cat.html').write_text(comun(h, s))

s = php({'tipo': 'page', 'slug': 'calculadora-consumo-electrico', 'cats': CATS})
(OUT / 'calc.html').write_text(comun((BASE / 'calc.html').read_text(), s))
print('ok', sorted(p.name for p in OUT.glob('*.html')))
