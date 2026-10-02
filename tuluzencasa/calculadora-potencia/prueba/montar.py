"""Monta prueba/prueba.html: el HTML real de una página de tuluzencasa.com con la calculadora inyectada.
Uso: python3 prueba/montar.py
Necesita prueba/shell.html (curl -sS https://tuluzencasa.com/aviso-legal/ -o prueba/shell.html) y prueba/art.html
(curl -sS https://tuluzencasa.com/cuanto-consume-termo-electrico/ -o prueba/art.html), del que copia el CSS de los
bloques que el aviso legal no usa (tabla), porque WordPress solo carga el CSS de los bloques presentes en la página."""
import re, os
d = os.path.dirname(os.path.abspath(__file__)); raiz = os.path.dirname(d)
h = open(os.path.join(d, 'shell.html')).read()
page = re.sub(r'<!--.*?-->', '', open(os.path.join(raiz, 'pagina.html')).read(), flags=re.S)
js = open(os.path.join(raiz, 'calculadora-potencia.js')).read()
i = h.index('<div class="entry-content" itemprop="text">') + len('<div class="entry-content" itemprop="text">')
fin = h.index('</article>', i)
k = h.rindex('</div>', i, h.rindex('</div>', i, fin))
out = h[:i] + page + h[k:]
art = open(os.path.join(d, 'art.html')).read()
for m in re.finditer(r'<style id="(wp-block-[a-z-]+-inline-css)"[^>]*>.*?</style>', art, re.S):
    if m.group(1) not in out:
        out = out.replace('</head>', m.group(0) + '</head>', 1)
out = out.replace('<title>', '<base href="https://tuluzencasa.com/"><title>', 1)
out = re.sub(r'<h1 class="entry-title"[^>]*>.*?</h1>', '<h1 class="entry-title" itemprop="headline">Calculadora de potencia contratada</h1>', out, flags=re.S)
out = out.replace('</body>', '<script>' + js + '</script></body>')
open(os.path.join(d, 'prueba.html'), 'w').write(out)
