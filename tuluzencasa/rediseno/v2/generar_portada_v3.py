"""Portada futurista (propuesta): la portada v2 con una cabecera oscura tipo «sala de control»
y una casa isométrica 3D animada solo con SVG y CSS (sin JavaScript ni <script> en el contenido).

Mismos textos, enlaces y cifras que la v2 (comprobadas en generar_portada_v2.py). Salida: portada-v3.html. No sube nada.
"""
import math
import pathlib
import re

import generar_portada_v2 as v2

AQUI = pathlib.Path(__file__).resolve().parent

# ---------- casa isométrica ----------
U, H, OX, OY = 92, 40, 250, 70
IX, IY = math.cos(math.pi / 6), math.sin(math.pi / 6)


def P(x, y, z=0.0):
    return (OX + (x - y) * IX * U, OY + (x + y) * IY * U - z * U)


def pts(a):
    return ' '.join(f'{p[0]:.1f},{p[1]:.1f}' for p in a)


# habitación: (col, fila, nombre, color, intensidad 0-1)
SALAS = [
    (0, 0, 'Cocina', '#F2C230', .55),
    (1, 0, 'Salón', '#FF5D6C', .95),
    (2, 0, 'Dormitorio', '#3BE0FF', .25),
    (0, 1, 'Baño', '#F2C230', .7),
    (1, 1, 'Lavadero', '#3BE0FF', .35),
    (2, 1, 'Garaje', '#9b8cff', .3),
]


def casa():
    hz = H / U
    s = ['<svg class="tl3d-casa" viewBox="0 0 560 420" role="img" aria-label="Casa en 3D con el gasto de luz de cada habitación">',
         '<defs><filter id="tl3d-gl" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>'
         '<linearGradient id="tl3d-pa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a4470"/><stop offset="1" stop-color="#132238"/></linearGradient>'
         '<radialGradient id="tl3d-sue" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#3BE0FF" stop-opacity=".35"/><stop offset="1" stop-color="#3BE0FF" stop-opacity="0"/></radialGradient></defs>']
    c = P(1.5, 1, 0)
    s.append(f'<ellipse cx="{c[0]:.1f}" cy="{c[1] + 40:.1f}" rx="250" ry="120" fill="url(#tl3d-sue)"/>')
    # losa
    s.append(f'<polygon points="{pts([P(-.12, -.12, -.08), P(3.12, -.12, -.08), P(3.12, 2.12, -.08), P(-.12, 2.12, -.08)])}" fill="#0e1a2d" stroke="#3BE0FF" stroke-opacity=".35"/>')
    s.append(f'<polygon points="{pts([P(-.12, 2.12, -.08), P(3.12, 2.12, -.08), P(3.12, 2.12, -.22), P(-.12, 2.12, -.22)])}" fill="#0a1322"/>')
    s.append(f'<polygon points="{pts([P(3.12, -.12, -.08), P(3.12, 2.12, -.08), P(3.12, 2.12, -.22), P(3.12, -.12, -.22)])}" fill="#081020"/>')
    m = P(3.42, 2.42, 0)
    # cables
    for i, (x, y, _n, col, k) in enumerate(SALAS):
        a = P(x + .5, y + .5, 0)
        mid = ((a[0] + m[0]) / 2, max(a[1], m[1]) + 26)
        s.append(f'<path class="tl3d-cable" style="animation-duration:{3.4 - 2.4 * k:.2f}s" d="M{a[0]:.1f} {a[1]:.1f} Q{mid[0]:.1f} {mid[1]:.1f} {m[0]:.1f} {m[1] - 14:.1f}" stroke="{col}"/>')
    # habitaciones
    for i, (x, y, n, col, k) in enumerate(SALAS):
        g = []
        g.append(f'<polygon class="tl3d-suelo" points="{pts([P(x + .05, y + .05), P(x + .95, y + .05), P(x + .95, y + .95), P(x + .05, y + .95)])}" fill="{col}" fill-opacity="{.25 + .55 * k:.2f}" stroke="{col}" stroke-opacity=".9"/>')
        if y == 0:
            g.append(f'<polygon points="{pts([P(x + .05, y + .05), P(x + .95, y + .05), P(x + .95, y + .05, hz), P(x + .05, y + .05, hz)])}" fill="url(#tl3d-pa)"/>')
            g.append(f'<polyline points="{pts([P(x + .05, y + .05, hz), P(x + .95, y + .05, hz)])}" stroke="{col}" stroke-opacity=".8" fill="none"/>')
        if x == 0:
            g.append(f'<polygon points="{pts([P(x + .05, y + .05), P(x + .05, y + .95), P(x + .05, y + .95, hz), P(x + .05, y + .05, hz)])}" fill="#1a2c49"/>')
            g.append(f'<polyline points="{pts([P(x + .05, y + .05, hz), P(x + .05, y + .95, hz)])}" stroke="{col}" stroke-opacity=".8" fill="none"/>')
        a = P(x + .5, y + .5, 0)
        g.append(f'<circle class="tl3d-halo" cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="{18 + 26 * k:.0f}" fill="{col}" filter="url(#tl3d-gl)" style="animation-delay:{i * .45:.2f}s"/>')
        g.append(f'<text x="{a[0]:.1f}" y="{a[1] + 4:.1f}" text-anchor="middle">{n}</text>')
        s.append('<g>' + ''.join(g) + '</g>')
    # contador
    s.append(f'<g class="tl3d-cont"><rect x="{m[0] - 17:.1f}" y="{m[1] - 34:.1f}" width="34" height="44" rx="6" fill="#0b1524" stroke="#3BE0FF"/>'
             f'<path d="M{m[0] + 1:.1f} {m[1] - 25:.1f}l-6 10h6l-2 8 8-11h-6z" fill="#F2C230"/>'
             f'<text x="{m[0]:.1f}" y="{m[1] + 26:.1f}" text-anchor="middle" class="tl3d-pq">CONTADOR</text></g>')
    s.append('</svg>')
    return ''.join(s)


CSS = r"""
/* ===== Portada futurista (cabecera oscura con casa 3D). Solo afecta a la portada. ===== */
.tl-hero3{position:relative;color:#E8F0FA;background:radial-gradient(520px 360px at 65% 18%,#1d3a66 0,transparent 70%),radial-gradient(300px 240px at 20% 100%,#2b2350 0,transparent 70%),#070D18;box-shadow:0 0 0 100vmax #070D18;clip-path:inset(0 -100vmax);padding:56px 0 48px!important;isolation:isolate}
.tl-hero3::before{content:"";position:absolute;inset:0;background-image:linear-gradient(#ffffff0a 1px,transparent 1px),linear-gradient(90deg,#ffffff0a 1px,transparent 1px);background-size:36px 36px;mask-image:radial-gradient(70% 90% at 60% 40%,#000,transparent);-webkit-mask-image:radial-gradient(70% 90% at 60% 40%,#000,transparent);z-index:-1;pointer-events:none}
.tl-hero3 h1{color:#fff!important;text-shadow:0 0 40px #3be0ff33}
.tl-hero3 h1 .tlb-clave,.tl-hero3 h1 strong{color:#F2C230}
.tl-hero3 p{color:#B8C7DA!important}
.tl-hero3 .tl-kicker{color:#3BE0FF!important}
.tl-hero3 .tl-kicker::before{background:#3BE0FF;box-shadow:0 0 12px #3BE0FF}
.tl-hero3 .tl-chips{color:#9DB0C8!important}
.tl-hero3 .tl-chips a{background:#ffffff0d;border-color:#ffffff26;color:#E8F0FA}
.tl-hero3 .tl-chips a:hover{background:#F2C230;border-color:#F2C230;color:#070D18}
.tl-hero3 .tl-buscador .wp-block-search__inside-wrapper{background:#0c1626;border-color:#3BE0FF66;box-shadow:0 0 0 1px #3be0ff22,0 12px 40px -18px #3BE0FF}
.tl-hero3 .tl-buscador .wp-block-search__input{color:#fff}
.tl-hero3 .tl-buscador .wp-block-search__input::placeholder{color:#7f93ad}
.tl-hero3 .tl-buscador .wp-block-search__button{background:#F2C230;color:#070D18}
.tl-hero3 .tl-botones .wp-block-button:not(:first-child) .wp-block-button__link{background:#ffffff12;box-shadow:inset 0 0 0 1px #ffffff33;color:#fff}
.tl-hero3 .tl-botones .wp-block-button:first-child .wp-block-button__link{box-shadow:0 10px 30px -10px #F2C230}
.tl-hero-vis{position:relative;display:flex;flex-direction:column;align-items:center}
.tl3d-casa{display:block;width:100%;max-width:560px;height:auto;margin:-10px auto -70px;filter:drop-shadow(0 30px 40px #000a)}
.tl3d-casa text{font:700 13px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;fill:#fff;paint-order:stroke;stroke:#070D18;stroke-width:3px}
.tl3d-casa .tl3d-pq{font-size:9px;fill:#9DB0C8;stroke:none;letter-spacing:.1em}
.tl3d-cable{fill:none;stroke-width:2;stroke-linecap:round;stroke-dasharray:4 11;opacity:.85}
.tl3d-halo{opacity:.35}
@media (prefers-reduced-motion:no-preference){
  .tl3d-cable{animation:tl3d-flujo linear infinite}
  .tl3d-halo{animation:tl3d-pulso 3.2s ease-in-out infinite}
  .tl3d-casa{animation:tl3d-flota 7s ease-in-out infinite}
}
@keyframes tl3d-flujo{to{stroke-dashoffset:-60}}
@keyframes tl3d-pulso{50%{opacity:.7}}
@keyframes tl3d-flota{50%{transform:translateY(-8px)}}
.tl-hero3 .tl-ejemplo{position:relative;z-index:1;width:min(100%,430px);background:#0c1626cc;border:1px solid #ffffff22;box-shadow:0 30px 60px -30px #000,inset 0 1px 0 #ffffff1a;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);color:#E8F0FA}
.tl-hero3 .tl-ejemplo h2{color:#fff!important}
.tl-hero3 .tl-ejemplo>p{color:#9DB0C8!important}
.tl-hero3 .tl-ej-lista li{border-bottom-color:#ffffff1f;color:#E8F0FA}
.tl-hero3 .tl-ej-lista small{color:#9DB0C8}
.tl-hero3 .tl-ej-lista strong{color:#F2C230}
.tl-hero3 .tl-ej-pie a{color:#3BE0FF}
@media (max-width:1024px){.tl3d-casa{max-width:460px;margin-bottom:-60px}}
@media (max-width:768px){.tl-hero3{padding:32px 0 28px!important}.tl3d-casa{margin:-6px auto -40px}}
"""


def portada():
    base = v2.portada()
    # 1. la cabecera pasa a ser oscura
    base = base.replace('"className":"tl-hero tl-hero2"', '"className":"tl-hero tl-hero2 tl-hero3"', 1)
    base = base.replace('class="wp-block-group tl-hero tl-hero2"', 'class="wp-block-group tl-hero tl-hero2 tl-hero3"', 1)
    # 2. la tarjeta de ejemplo va dentro de un bloque visual con la casa 3D encima
    i = base.index('<!-- wp:group {"className":"tl-ejemplo"')
    j = base.index('<!-- /wp:group -->', base.index('tl-ej-pie', i)) + len('<!-- /wp:group -->')
    ejemplo = base[i:j]
    vis = ('<!-- wp:group {"className":"tl-hero-vis","layout":{"type":"default"}} -->\n<div class="wp-block-group tl-hero-vis">'
           '<!-- wp:html -->\n' + casa() + '\n<!-- /wp:html -->\n\n' + ejemplo + '</div>\n<!-- /wp:group -->')
    base = base[:i] + vis + base[j:]
    # 3. estilos en el mismo bloque <style> que ya lleva la portada
    base = base.replace('<style id="tl-portada-arreglo">.tl-home .wp-block-group__inner-container{display:contents}</style>',
                        '<style id="tl-portada-arreglo">.tl-home .wp-block-group__inner-container{display:contents}' + re.sub(r'\s*\n\s*', '', CSS) + '</style>', 1)
    assert '<script' not in base
    return base


if __name__ == '__main__':
    out = AQUI / 'portada-v3.html'
    out.write_text(portada(), encoding='utf-8')
    print(out, len(out.read_text()))
