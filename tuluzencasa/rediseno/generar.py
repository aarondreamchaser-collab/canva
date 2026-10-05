"""Genera el contenido en bloques de la portada nueva y de la página «Calculadora de consumo eléctrico».

Salida: portada.html (para la página 23) y pagina-calculadora-consumo.html (página nueva).
No sube nada a WordPress.
"""
import os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
WEB = 'https://tuluzencasa.com'
CALC_CONSUMO = WEB + '/calculadora-consumo-electrico/'
CALC_POTENCIA = WEB + '/calculadora-potencia-contratada/'

# Guías más útiles: pilares + bono social (slug, título corto, descripción)
GUIAS = [
    ('que-potencia-contratar', 'Qué potencia contratar', 'Cómo calcularla con lo que enciendes a la vez y cuánto ahorras si la bajas.'),
    ('como-leer-factura-luz', 'Cómo leer la factura de la luz', 'Potencia, energía, impuestos y contador, línea a línea con un ejemplo.'),
    ('pvpc-mercado-libre', 'PVPC o mercado libre', 'Qué tarifa te conviene según a qué horas consumes.'),
    ('bono-social-electrico', 'Bono social eléctrico', 'Requisitos, descuentos del 35 % y el 50 % y cómo pedirlo paso a paso.'),
    ('tramos-horarios-luz', 'Tramos horarios de la luz', 'Horas punta, llano y valle, y qué aparatos compensa mover.'),
    ('calefaccion-electrica-mas-barata', 'Calefacción eléctrica más barata', 'Qué sistema gasta menos para el mismo calor y cuánto cuesta al mes.'),
]


def p(txt, cls=None):
    if cls:
        return f'<!-- wp:paragraph {{"className":"{cls}"}} -->\n<p class="{cls}">{txt}</p>\n<!-- /wp:paragraph -->'
    return f'<!-- wp:paragraph -->\n<p>{txt}</p>\n<!-- /wp:paragraph -->'


def h(txt, nivel=2):
    attrs = '' if nivel == 2 else f' {{"level":{nivel}}}'
    return f'<!-- wp:heading{attrs} -->\n<h{nivel} class="wp-block-heading">{txt}</h{nivel}>\n<!-- /wp:heading -->'


def grupo(cls, interior, tag='div'):
    attrs = f'"tagName":"{tag}","className":"{cls}","layout":{{"type":"default"}}' if tag != 'div' else f'"className":"{cls}","layout":{{"type":"default"}}'
    return f'<!-- wp:group {{{attrs}}} -->\n<{tag} class="wp-block-group {cls}">' + '\n'.join(interior) + f'</{tag}>\n<!-- /wp:group -->'


def boton(txt, url):
    return f'<!-- wp:button -->\n<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{url}">{txt}</a></div>\n<!-- /wp:button -->'


def portada():
    hero = grupo('tl-hero', [
        h('Cuánto gastas en luz y cómo pagar menos', 1),
        p('Calcula el consumo de tus aparatos y la potencia que necesitas, y entiende cada línea de tu factura. Con cálculos propios y fuentes oficiales.'),
        '<!-- wp:buttons {"className":"tl-botones"} -->\n<div class="wp-block-buttons tl-botones">'
        + boton('Calcular mi consumo', CALC_CONSUMO) + '\n' + boton('Calcular mi potencia', CALC_POTENCIA)
        + '</div>\n<!-- /wp:buttons -->',
    ], 'section')
    calcs = grupo('tl-sec', [
        h('Calculadoras'),
        grupo('tl-calcs', [
            grupo('tl-calc tl-calc-consumo', [
                h('Calculadora de consumo eléctrico', 3),
                p('Añade tus aparatos, cuántas horas los usas y tu tarifa. Te dice cuánto pagas al mes y al año, con la factura completa.'),
                p(f'<a href="{CALC_CONSUMO}">Abrir la calculadora</a>', 'tl-ir'),
            ]),
            grupo('tl-calc tl-calc-potencia', [
                h('Calculadora de potencia contratada', 3),
                p('Marca los aparatos que pueden funcionar a la vez y te dice qué potencia te conviene contratar.'),
                p(f'<a href="{CALC_POTENCIA}">Abrir la calculadora</a>', 'tl-ir'),
            ]),
        ]),
    ], 'section')
    cats = grupo('tl-sec', [
        h('Temas'),
        p('Todo sobre la luz de una vivienda, ordenado por temas.', 'tl-sub'),
        '<!-- wp:shortcode -->\n[tl_categorias]\n<!-- /wp:shortcode -->',
    ], 'section')
    ultimos = grupo('tl-sec', [
        h('Últimos artículos'),
        '<!-- wp:query {"queryId":1,"query":{"perPage":6,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"exclude","inherit":false},"className":"tl-ultimos"} -->\n'
        '<div class="wp-block-query tl-ultimos"><!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->\n'
        '<!-- wp:post-featured-image {"isLink":true,"aspectRatio":"16/9","sizeSlug":"medium_large"} /-->\n\n'
        '<!-- wp:post-terms {"term":"category"} /-->\n\n'
        '<!-- wp:post-title {"level":3,"isLink":true} /-->\n'
        '<!-- /wp:post-template --></div>\n<!-- /wp:query -->',
    ], 'section')
    items = '\n\n'.join(
        f'<!-- wp:list-item -->\n<li><a href="{WEB}/{s}/">{t}</a>{d}</li>\n<!-- /wp:list-item -->' for s, t, d in GUIAS)
    guias = grupo('tl-sec', [
        h('Guías más útiles'),
        p('Lo primero que conviene leer para entender y bajar tu factura.', 'tl-sub'),
        '<!-- wp:list {"className":"tl-guias"} -->\n<ul class="wp-block-list tl-guias">' + items + '</ul>\n<!-- /wp:list -->',
    ], 'section')
    # Arreglo temporal mientras el fragmento «Diseño tuluzencasa» no lleve la regla .wp-block-group__inner-container
    estilo = '<!-- wp:html -->\n<style id="tl-portada-arreglo">.tl-home .wp-block-group__inner-container{display:contents}</style>\n<!-- /wp:html -->\n\n'
    return estilo + grupo('tl-home', [hero, calcs, cats, ultimos, guias]) + '\n'


def pagina_calculadora():
    """La calculadora de la portada actual, tal cual, en su propia página.
    Cambios: estilos que dependían de .home, H1 y sin el bloque «Elige un tema» (pasa a la portada)."""
    h_ = open(os.path.join(RAIZ, 'home-sin-script.html'), encoding='utf-8').read()
    h_ = h_.replace('<!-- HOME TULUZENCASA v2 (sin script) — el JavaScript se carga desde WPCode (calculadora.js) -->',
                    '<!-- CALCULADORA DE CONSUMO (antes en la portada) — el JavaScript se carga desde WPCode (calculadora.js), solo en esta página -->')
    h_ = h_.replace('body.home{', 'body:has(#tlc-app){')
    h_ = re.sub(r'(?m)^\.home ', 'body:has(#tlc-app) ', h_)
    assert '.home' not in h_, 'quedan selectores .home'
    h_ = h_.replace('</style>', '@media (max-width:768px){body:has(#tlc-app) .inside-article{padding-left:16px!important;padding-right:16px!important}}\n</style>', 1)
    h_ = h_.replace('<p class="tlc-eyebrow">Calculadora de consumo eléctrico</p>', '<p class="tlc-eyebrow">Gratis y sin registro</p>')
    h_ = h_.replace('<h1>¿Cuánto te cuesta la luz de tu casa, aparato por aparato?</h1>',
                    '<h1>Calculadora de consumo eléctrico: cuánto te cuesta la luz, aparato por aparato</h1>')
    i = h_.index('<section class="tlc-sec">\n    <h2>Elige un tema</h2>')
    j = h_.index('</section>', i) + len('</section>')
    h_ = h_[:i].rstrip() + '\n\n  ' + h_[j:].lstrip()
    return '<!-- wp:html -->\n' + h_.strip() + '\n<!-- /wp:html -->\n'


if __name__ == '__main__':
    open(os.path.join(AQUI, 'portada.html'), 'w', encoding='utf-8').write(portada())
    open(os.path.join(AQUI, 'pagina-calculadora-consumo.html'), 'w', encoding='utf-8').write(pagina_calculadora())
    print('ok')
