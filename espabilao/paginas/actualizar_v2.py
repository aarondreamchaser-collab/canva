#!/usr/bin/env python3
"""Sustituye el contenido de los borradores por la versión diseñada (v2). No los publica."""
import base64, json, os, sys, urllib.request, urllib.error
BASE='https://espabilao.com/wp-json/wp/v2'
AQUI=os.path.dirname(os.path.abspath(__file__))
tok=base64.b64encode(('%s:%s'%(os.environ['WP_USER'],os.environ['WP_APP_PASS'])).encode()).decode()
def api(m,r,d=None):
    q=urllib.request.Request(BASE+r,method=m,headers={'Authorization':'Basic '+tok,'Content-Type':'application/json','User-Agent':'espabilao-setup'})
    if d is not None: q.data=json.dumps(d).encode()
    try:
        with urllib.request.urlopen(q,timeout=90) as x: return json.loads(x.read().decode())
    except urllib.error.HTTPError as e: sys.exit('Error %s %s: %s'%(e.code,r,e.read().decode()[:300]))
pags={p['slug']:p for p in api('GET','/pages?per_page=100&status=draft,publish&context=edit&_fields=id,slug,status')}
for p in json.load(open(os.path.join(AQUI,'v2/paginas.json'))):
    e=pags.get(p['slug'])
    if not e: print('No existe:',p['slug']); continue
    c=open(os.path.join(AQUI,p['archivo'])).read()
    r=api('POST','/pages/%d'%e['id'],{'content':c,'title':p['title']})
    raw=r['content']['raw']
    print(p['slug'],r['status'],'estilos conservados' if 'id="pg-estilos"' in raw and 'id="pg-script"' in raw else 'ATENCIÓN: se han filtrado estilos o script')
