"""Comprueba los artículos de articulos/ antes de subirlos.

- Cada cifra con decimales del texto sale de calculos/salida/<slug>.json o de las constantes de comun.py.
- Palabra clave en el título, la primera frase y algún H2.
- Metadescripción = extracto y longitudes (título SEO <= 60, descripción <= 155).
- Índice con anclas que existen, enlaces internos (>= 3), enlace externo oficial (>= 1) y [VERIFICAR] pendientes.
Uso: python3 calculos/verificar_articulos.py
"""
import json, os, re, html, sys
import comun

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFICIALES = ('boe.es', 'cnmc.es', 'cnmc.gob.es', 'ree.es', 'miteco.gob.es', 'idae.es')


def valores(obj, out):
    if isinstance(obj, dict):
        for v in obj.values(): valores(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj: valores(v, out)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        for x in (obj, obj * 100):
            for d in (0, 1, 2, 3):
                out.add(comun.eur(x, d))
    return out


def norm(s):
    return s.lower().replace('¿', '').replace('?', '')


ok_global = True
for f in sorted(os.listdir(os.path.join(RAIZ, 'articulos'))):
    if not f.endswith('.html'): continue
    slug = f[:-5]
    h = open(os.path.join(RAIZ, 'articulos', f)).read()
    meta = json.load(open(os.path.join(RAIZ, 'articulos', slug + '.json')))
    calc = json.load(open(os.path.join(RAIZ, 'calculos', 'salida', slug + '.json')))
    permitidos = valores(calc, set()) | valores({k: getattr(comun, k) for k in dir(comun) if k.isupper()}, set())
    texto = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<!--.*?-->', '', h, flags=re.S)))
    problemas = []

    cifras = sorted(set(re.findall(r'\d{1,3}(?:\.\d{3})*,\d+', texto)))
    fuera = [c for c in cifras if c not in permitidos]
    if fuera: problemas.append(f'cifras sin origen en los cálculos: {fuera}')

    kw = norm(meta['palabra_clave'])
    primera = norm(re.split(r'(?<=[.?!])\s', texto.strip(), 1)[0] + ' ' + texto.strip()[:200])
    h2 = [norm(html.unescape(re.sub(r'<[^>]+>', '', x))) for x in re.findall(r'<h2[^>]*>(.*?)</h2>', h)]
    if kw not in norm(meta['titulo']): problemas.append('palabra clave no está en el título')
    if kw not in primera: problemas.append('palabra clave no está en la primera frase')
    if not any(kw in x for x in h2): problemas.append('palabra clave no está en ningún H2')
    if meta['descripcion'] != meta['extracto']: problemas.append('metadescripción y extracto distintos')
    if len(meta['titulo_seo']) > 60: problemas.append('título SEO > 60')
    if len(meta['descripcion']) > 155: problemas.append('metadescripción > 155')

    anclas = re.findall(r'href="#([^"]+)"', h)
    ids = set(re.findall(r'id="([^"]+)"', h))
    rotas = [a for a in anclas if a not in ids]
    if not anclas: problemas.append('sin índice')
    if rotas: problemas.append(f'anclas sin destino: {rotas}')

    enlaces = re.findall(r'href="(https?://[^"]+)"', h)
    internos = sorted({e for e in enlaces if 'tuluzencasa.com' in e})
    externos = sorted({e for e in enlaces if 'tuluzencasa.com' not in e})
    oficiales = [e for e in externos if any(d in e for d in OFICIALES)]
    if len(internos) < 3: problemas.append('menos de 3 enlaces internos')
    if not oficiales: problemas.append('sin enlace externo oficial')
    pend = re.findall(r'\[VERIFICAR[^\]]*\]', texto)

    palabras = len(texto.split())
    print(f'\n== {slug}: {palabras} palabras · {len(cifras)} cifras · {len(internos)} internos · {len(externos)} externos ({len(oficiales)} oficiales) · {len(pend)} [VERIFICAR]')
    for e in internos: print('   int', e)
    for e in externos: print('   ext', e)
    for p in pend: print('   PENDIENTE', p[:150])
    for p in problemas: print('   ERROR', p)
    ok_global &= not problemas

sys.exit(0 if ok_global else 1)
