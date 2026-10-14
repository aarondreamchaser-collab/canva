#!/usr/bin/env python3
"""Crea las páginas legales como BORRADORES en WordPress y las añade al menú del pie.
Uso: WP_USER='usuario' WP_APP_PASS='xxxx xxxx ...' python3 subir.py
"""
import base64, json, os, sys, urllib.request, urllib.error

BASE = 'https://espabilao.com/wp-json/wp/v2'
AQUI = os.path.dirname(os.path.abspath(__file__))
token = base64.b64encode(('%s:%s' % (os.environ['WP_USER'], os.environ['WP_APP_PASS'])).encode()).decode()

def api(metodo, ruta, datos=None):
    req = urllib.request.Request(BASE + ruta, method=metodo, headers={'Authorization': 'Basic ' + token, 'Content-Type': 'application/json', 'User-Agent': 'espabilao-setup'})
    if datos is not None:
        req.data = json.dumps(datos).encode()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode() or 'null')
    except urllib.error.HTTPError as e:
        sys.exit('Error %s en %s %s: %s' % (e.code, metodo, ruta, e.read().decode()[:400]))

yo = api('GET', '/users/me?context=edit')
print('Conectado como:', yo.get('name'), '| roles:', yo.get('roles'))

paginas = json.load(open(os.path.join(AQUI, 'paginas.json')))
existentes = api('GET', '/pages?per_page=100&status=publish,draft,pending,private&context=edit&_fields=id,slug,status,title')
por_slug = {p['slug']: p for p in existentes}
ids = []
for p in paginas:
    if p['slug'] in por_slug:
        e = por_slug[p['slug']]
        print('Ya existe, no se toca:', p['slug'], '(%s, id %s)' % (e['status'], e['id']))
        ids.append((e['id'], p['title']))
        continue
    contenido = open(os.path.join(AQUI, p['archivo'])).read()
    nueva = api('POST', '/pages', {'title': p['title'], 'slug': p['slug'], 'status': 'draft', 'content': contenido})
    print('Borrador creado:', nueva['id'], nueva['slug'])
    ids.append((nueva['id'], p['title']))

# Menú del pie: se reutiliza si ya existe uno asignado a la ubicación «pie».
menus = api('GET', '/menus?context=edit&per_page=100')
menu = next((m for m in menus if 'pie' in (m.get('locations') or [])), None)
if not menu:
    menu = api('POST', '/menus', {'name': 'Pie de página', 'locations': ['pie']})
    print('Menú creado y asignado al pie:', menu['id'])
else:
    print('Usando menú del pie existente:', menu['id'], menu['name'])
items = api('GET', '/menu-items?context=edit&per_page=100&menus=%d' % menu['id'])
ya = {int(i.get('object_id') or 0) for i in items}
for orden, (pid, titulo) in enumerate(ids, start=1):
    if pid in ya:
        print('Ya estaba en el menú:', titulo)
        continue
    api('POST', '/menu-items', {'title': titulo, 'type': 'post_type', 'object': 'page', 'object_id': pid, 'menus': menu['id'], 'menu_order': orden, 'status': 'publish'})
    print('Añadida al menú:', titulo)
print('Listo.')
