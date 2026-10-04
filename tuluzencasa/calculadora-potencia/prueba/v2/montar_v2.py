"""Monta las páginas de prueba de la v2 a partir del HTML publicado (no toca WordPress).
Uso: python3 montar_v2.py DIR   -> escribe en DIR t_102_v2.html, t_102_marcado_viejo_js_nuevo.html,
t_home_fix.html, t_art_fix.html y t_cat_fix.html. Después: python3 -m http.server 8765 en DIR y
PORT=8765 NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt node prueba_v2.mjs (desde DIR)."""
import re, sys, urllib.request
from pathlib import Path
T = Path(__file__).resolve().parents[3]
D = Path(sys.argv[1])
def pub(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 tlc-prueba'}), timeout=60).read().decode()
def base(h): return h.replace('<head>', '<head><base href="https://tuluzencasa.com/">', 1)
def swap_js(h, js):
    ms = [m for m in re.finditer(r'(<script\b[^>]*>)(.*?)(</script>)', h, re.S) if "getElementById('tlp-app')" in m.group(2)]
    assert len(ms) == 1
    return h[:ms[0].start(2)] + js + h[ms[0].end(2):]
js = (T / 'calculadora-potencia/calculadora-potencia.js').read_text()
a = swap_js(pub('https://tuluzencasa.com/calculadora-potencia-contratada/'), js)
(D / 't_102_marcado_viejo_js_nuevo.html').write_text(base(a))
i = a.find('<div class="tlp">'); j = a.find('</div>', a.find('</section>', i)) + 6
b = a[:i] + (T / 'calculadora-potencia/bloque-v2-marcado.html').read_text() + a[j:]
k = b.find('@media(max-width:900px){', b.find('.tlp{--pared'))
b = b[:k] + (T / 'calculadora-potencia/bloque-v2-css.css').read_text() + b[k:]
(D / 't_102_v2.html').write_text(base(b))
hh = pub('https://tuluzencasa.com/')
(D / 't_home_fix.html').write_text(base(hh.replace('.home .entry-content{margin-top:0!important}', '.home .entry-content{margin-top:0!important}\n@media(max-width:768px){.tlc{padding-left:16px;padding-right:16px}}', 1)))
css = '<style>' + (T / 'mejoras-movil/wpcode-css-articulos-movil.css').read_text() + '</style></head>'
(D / 't_art_fix.html').write_text(base(pub('https://tuluzencasa.com/que-potencia-contratar/').replace('</head>', css, 1)))
(D / 't_cat_fix.html').write_text(base(pub('https://tuluzencasa.com/climatizacion/').replace('</head>', css, 1)))
print('ok')
