"""Genera la portada del rediseño 2 en bloques de WordPress: v2/portada-v2.html (para la página 23).

Las cifras de la tarjeta de ejemplo salen de calculos/*.md (se comprueba al generar). No sube nada.
"""
import pathlib
import re

AQUI = pathlib.Path(__file__).resolve().parent
BASE = AQUI.parent.parent
W = 'https://tuluzencasa.com'
CC = W + '/calculadora-consumo-electrico/'
CP = W + '/calculadora-potencia-contratada/'
UP = W + '/wp-content/uploads/2026/10/'


def p(t, cls=None):
    if cls:
        return f'<!-- wp:paragraph {{"className":"{cls}"}} -->\n<p class="{cls}">{t}</p>\n<!-- /wp:paragraph -->'
    return f'<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->'


def h(t, n=2):
    a = '' if n == 2 else f' {{"level":{n}}}'
    return f'<!-- wp:heading{a} -->\n<h{n} class="wp-block-heading">{t}</h{n}>\n<!-- /wp:heading -->'


def g(cls, inner, tag='div'):
    a = (f'"tagName":"{tag}",' if tag != 'div' else '') + f'"className":"{cls}","layout":{{"type":"default"}}'
    return f'<!-- wp:group {{{a}}} -->\n<{tag} class="wp-block-group {cls}">' + '\n'.join(inner) + f'</{tag}>\n<!-- /wp:group -->'


def lista(items, cls, ordenada=False):
    tag = 'ol' if ordenada else 'ul'
    a = ('"ordered":true,' if ordenada else '') + f'"className":"{cls}"'
    li = '\n'.join(f'<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->' for i in items)
    return f'<!-- wp:list {{{a}}} -->\n<{tag} class="wp-block-list {cls}">{li}</{tag}>\n<!-- /wp:list -->'


def botones(bs, cls='tl-botones'):
    inner = '\n'.join(f'<!-- wp:button -->\n<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="{u}">{t}</a></div>\n<!-- /wp:button -->' for t, u in bs)
    return f'<!-- wp:buttons {{"className":"{cls}"}} -->\n<div class="wp-block-buttons {cls}">{inner}</div>\n<!-- /wp:buttons -->'


# Cifras de la tarjeta: (aparato, detalle, importe, archivo de cálculos donde debe aparecer)
EJEMPLO = [
    ('Aire acondicionado', '3.000 frigorías, 8 h al día', '24,08 €', 'cuanto-consume-aire-acondicionado'),
    ('Termo eléctrico', '1.500 W, 3 h de resistencia al día', '15,80 €', 'cuanto-consume-termo-electrico'),
    ('Nevera', 'nevera tipo, encendida todo el día', '3,61 €', 'cuanto-consume-una-nevera'),
    ('Iluminación LED', '10 bombillas, 5 h al día', '2,26 €', 'bombillas-led-cuanto-ahorran'),
    ('Lavadora', '12 lavados a 40 °C', '1,58 €', 'cuanto-consume-lavadora'),
]
for _, _, eur, slug in EJEMPLO:
    md = (BASE / 'calculos' / f'{slug}.md')
    txt = md.read_text() if md.exists() else ''
    art = (BASE / 'src' / f'{slug}.txt')
    txt += art.read_text() if art.exists() else ''
    assert eur in txt, (slug, eur)

GUIAS = [
    ('que-potencia-contratar', 'Qué potencia contratar', 'Cómo calcularla con lo que enciendes a la vez y cuánto ahorras si la bajas.'),
    ('como-leer-factura-luz', 'Cómo leer la factura de la luz', 'Potencia, energía, impuestos y contador, línea a línea con un ejemplo.'),
    ('pvpc-mercado-libre', 'PVPC o mercado libre', 'Qué tarifa te conviene según a qué horas consumes.'),
    ('bono-social-electrico', 'Bono social eléctrico', 'Requisitos, descuentos y cómo pedirlo paso a paso.'),
    ('tramos-horarios-luz', 'Tramos horarios de la luz', 'Horas punta, llano y valle, y qué aparatos compensa mover.'),
    ('se-ha-ido-la-luz', 'Se ha ido la luz', 'Qué mirar en el cuadro, a quién llamar y cómo reclamar.'),
]


def portada():
    texto = g('tl-hero-txt', [
        p('Guías y calculadoras de la luz en casa', 'tl-kicker'),
        h('Cuánto gastas en luz y cómo pagar menos', 1),
        p('Calcula el consumo de tus aparatos y la potencia que necesitas, y entiende cada línea de tu factura. Con cálculos propios y fuentes oficiales.'),
        '<!-- wp:search {"label":"Buscar en Tu luz en casa","showLabel":false,"placeholder":"Busca: lavadora, potencia, bono social…","buttonText":"Buscar","className":"tl-buscador"} /-->',
        p('Lo más buscado: ' + ' '.join(f'<a href="{W}/{s}/">{t}</a>' for s, t in [
            ('cuanto-consume-aire-acondicionado', 'Aire acondicionado'), ('cuanto-consume-lavadora', 'Lavadora'),
            ('que-potencia-contratar', 'Potencia'), ('bono-social-electrico', 'Bono social'), ('como-leer-factura-luz', 'Factura')]), 'tl-chips'),
        botones([('Calcular mi consumo', CC), ('Calcular mi potencia', CP)]),
    ])
    ejemplo = g('tl-ejemplo', [
        h('Lo que cuesta cada aparato al mes'),
        p('Ejemplos de nuestras guías, a 0,165 €/kWh con impuestos.'),
        lista([f'<span>{a}<small>{d}</small></span><strong>{e}</strong>' for a, d, e, _ in EJEMPLO], 'tl-ej-lista'),
        p(f'<a href="{CC}">Calcula los de tu casa →</a>', 'tl-ej-pie'),
    ])
    hero = g('tl-hero tl-hero2', [texto, ejemplo], 'section')

    calcs = g('tl-sec', [
        g('tl-sec-cab', [h('Calculadoras gratis'), p('Sin registro: pon tus datos y ves el resultado al momento.', 'tl-sub')]),
        g('tl-calcs', [
            g('tl-calc tl-calc-consumo', [
                h('Calculadora de consumo eléctrico', 3),
                p('Añade tus aparatos, cuántas horas los usas y tu tarifa. Te dice cuánto pagas al mes y al año.'),
                lista(['Precio único o tarifa por horas', 'Coste por aparato, al mes y al año', 'Comparte tu cálculo con un enlace'], 'tl-calc-pts'),
                p(f'<a href="{CC}">Abrir la calculadora</a>', 'tl-ir'),
            ]),
            g('tl-calc tl-calc-potencia', [
                h('Calculadora de potencia contratada', 3),
                p('Marca los aparatos que pueden funcionar a la vez y te dice qué potencia te conviene contratar.'),
                lista(['Pensada para no pasarte ni quedarte corto', 'Con los aparatos más habituales de una casa', 'Gratis y sin registro'], 'tl-calc-pts'),
                p(f'<a href="{CP}">Abrir la calculadora</a>', 'tl-ir'),
            ]),
        ]),
    ], 'section')

    temas = g('tl-sec', [
        g('tl-sec-cab', [h('Explora por temas'), p('Todo sobre la luz de una vivienda, ordenado por temas.', 'tl-sub')]),
        '<!-- wp:shortcode -->\n[tl_categorias]\n<!-- /wp:shortcode -->',
    ], 'section')

    s0, t0, d0 = GUIAS[0]
    destacadas = g('tl-sec', [
        g('tl-sec-cab', [h('Guías imprescindibles'), p('Lo primero que conviene leer para entender y bajar tu factura.', 'tl-sub')]),
        g('tl-destacadas', [
            g('tl-dest-prin', [
                f'<!-- wp:image {{"sizeSlug":"medium_large","linkDestination":"custom"}} -->\n<figure class="wp-block-image size-medium_large"><a href="{W}/{s0}/"><img src="{UP}{s0}-768x432.jpg" alt=""/></a></figure>\n<!-- /wp:image -->',
                g('tl-dest-txt', [p('Guía básica', 'tl-dest-et'), h(f'<a href="{W}/{s0}/">{t0}</a>', 3), p(d0)]),
            ]),
            lista([f'<a href="{W}/{s}/">{t}</a>{d}' for s, t, d in GUIAS[1:]], 'tl-dest-lista'),
        ]),
    ], 'section')

    ultimos = g('tl-sec', [
        g('tl-sec-cab', [h('Últimos artículos')]),
        '<!-- wp:query {"queryId":1,"query":{"perPage":6,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"exclude","inherit":false},"className":"tl-ultimos"} -->\n'
        '<div class="wp-block-query tl-ultimos"><!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->\n'
        '<!-- wp:post-featured-image {"isLink":true,"aspectRatio":"16/9","sizeSlug":"medium_large"} /-->\n\n'
        '<!-- wp:post-terms {"term":"category"} /-->\n\n'
        '<!-- wp:post-title {"level":3,"isLink":true} /-->\n'
        '<!-- /wp:post-template --></div>\n<!-- /wp:query -->',
    ], 'section')

    metodo = g('tl-sec', [
        g('tl-sec-cab', [h('Cómo hacemos los cálculos'), p(f'<a href="{W}/sobre-nosotros/">Más sobre cómo trabajamos</a>', 'tl-ver')]),
        lista([
            '<strong>Partimos de la norma</strong>Leemos el BOE, los reglamentos europeos y las guías del IDAE, y enlazamos cada fuente en el artículo.',
            '<strong>El mismo precio en toda la web</strong>Todas las cifras usan 0,165 €/kWh con impuestos y los mismos supuestos que nuestra calculadora.',
            '<strong>Calculado, no a ojo</strong>Cada tabla sale de un cálculo con script, redondeado a dos decimales, para que las cifras cuadren entre guías.',
        ], 'tl-metodo', ordenada=True),
    ], 'section')

    cta = g('tl-cta', [
        g('tl-cta-txt', [h('¿Cuánto te cuesta a ti la luz?'), p('Pon tus aparatos, las horas de uso y el precio de tu factura, y mira qué pesa más.')]),
        botones([('Calcular mi consumo', CC)], 'tl-cta-bt'),
    ], 'section')

    cuerpo = '\n\n'.join([hero, calcs, temas, destacadas, ultimos, metodo, cta])
    return ('<!-- wp:html -->\n<style id="tl-portada-arreglo">.tl-home .wp-block-group__inner-container{display:contents}</style>\n<!-- /wp:html -->\n\n'
            + g('tl-home', [cuerpo]))


if __name__ == '__main__':
    out = AQUI / 'portada-v2.html'
    out.write_text(portada(), encoding='utf-8')
    print(out, len(out.read_text()))
