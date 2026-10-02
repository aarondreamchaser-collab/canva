"""Auditoría mensual de tuluzencasa.com (Fase 7 de TAREAS.md). Solo lectura: no necesita credenciales.

Uso: python3 auditoria/auditar.py  -> escribe auditoria/salida/<fecha>.json
Necesita: requests y beautifulsoup4.
"""
import datetime as dt, json, os, re, sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup

SITIO = 'https://tuluzencasa.com'
HOY = dt.date.today()
UA = {'User-Agent': 'Mozilla/5.0 (auditoria tuluzencasa.com)'}
S = requests.Session(); S.headers.update(UA)


def get(url, **kw):
    return S.get(url, timeout=30, **kw)


def urls_sitemap():
    out = []
    idx = get(SITIO + '/sitemap_index.xml').text
    for sm in re.findall(r'<loc>([^<]+)</loc>', idx):
        out += re.findall(r'<loc>([^<]+)</loc>', get(sm).text)
    return [u for u in out if not re.search(r'\.(webp|jpe?g|png|gif|svg)$', u)]


def rest(tipo):
    return get(f'{SITIO}/wp-json/wp/v2/{tipo}?per_page=100&_fields=id,link,slug,modified,date,featured_media,categories,title').json()


def analizar(url):
    r = get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    meta = lambda **a: (soup.find('meta', attrs=a) or {}).get('content')
    canon = soup.find('link', rel='canonical')
    contenido = soup.select_one('.entry-content') or soup
    imgs = [dict(src=i.get('src'), alt=i.get('alt')) for i in contenido.find_all('img')]
    enlaces = []
    for a in contenido.find_all('a', href=True):
        h = urldefrag(urljoin(url, a['href']))[0]
        if h.startswith('http'): enlaces.append(dict(href=h, texto=a.get_text(' ', strip=True)[:80], rel=a.get('rel')))
    todos = {urldefrag(urljoin(url, a['href']))[0] for a in soup.find_all('a', href=True) if urljoin(url, a['href']).startswith('http')}
    ld = [s.string for s in soup.find_all('script', type='application/ld+json')]
    tipos = []
    for x in ld:
        try:
            d = json.loads(x); g = d.get('@graph', [d])
            tipos += [t if isinstance(t, str) else '/'.join(t) for t in (n.get('@type') for n in g) if t]
        except Exception:
            tipos.append('JSON-LD inválido')
    return dict(
        url=url, estado=r.status_code, title=(soup.title.string or '').strip() if soup.title else '',
        description=meta(name='description'), robots=meta(name='robots'), canonical=canon.get('href') if canon else None,
        og_image=meta(property='og:image'), h1=[h.get_text(' ', strip=True) for h in soup.find_all('h1')],
        imgs=imgs, enlaces_contenido=enlaces, enlaces_todos=sorted(todos), schema=tipos,
        palabras=len(contenido.get_text(' ', strip=True).split()), bytes=len(r.content),
        rank_math='Rank Math' in r.text)


def comprobar(url):
    try:
        r = S.head(url, timeout=20, allow_redirects=True)
        if r.status_code in (403, 405, 400) or r.status_code >= 500:
            r = S.get(url, timeout=25, allow_redirects=True, stream=True)
        return url, r.status_code, r.url if r.url != url else None
    except Exception as e:
        return url, f'error: {type(e).__name__}', None


def main():
    os.makedirs(os.path.join(os.path.dirname(__file__), 'salida'), exist_ok=True)
    posts, pages = rest('posts'), rest('pages')
    sm = urls_sitemap()
    urls = sorted(set(sm) | {p['link'] for p in posts + pages})
    with ThreadPoolExecutor(6) as ex:
        paginas = list(ex.map(analizar, urls))
    enlaces = sorted({e for p in paginas for e in p['enlaces_todos']})
    with ThreadPoolExecutor(8) as ex:
        estados = {u: dict(estado=s, redirige=f) for u, s, f in ex.map(comprobar, enlaces)}
    media = get(f'{SITIO}/wp-json/wp/v2/media?per_page=100&_fields=id,source_url,alt_text,media_details').json()
    res = dict(fecha=str(HOY), sitemap=sm, posts=posts, pages=pages, paginas=paginas, enlaces=estados,
               media=[dict(id=m['id'], url=m['source_url'], alt=m['alt_text'],
                           kb=round((m.get('media_details') or {}).get('filesize', 0) / 1024),
                           ancho=(m.get('media_details') or {}).get('width')) for m in media])
    out = os.path.join(os.path.dirname(__file__), 'salida', f'{HOY}.json')
    json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
    print('escrito', out, len(paginas), 'páginas,', len(enlaces), 'enlaces')


if __name__ == '__main__':
    main()
