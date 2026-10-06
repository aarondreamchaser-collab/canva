"""Enlaces desde artículos publicados hacia los de la tanda 1 de 4 (203-206).

Uso: python3 scripts/enlaces_tanda4.py            -> simulación: dice qué cambiaría
     python3 scripts/enlaces_tanda4.py --aplicar  -> aplica SOLO los enlaces cuyo destino ya está publicado

Antes de escribir guarda una copia de cada entrada en rediseno/copia-seguridad/<fecha>-enlaces/,
comprueba que el texto original aparece una sola vez, valida los bloques y vuelve a leer la entrada.
No cambia el estado de ninguna entrada. Credenciales en WP_USER y WP_APP_PASSWORD (nunca se imprimen).
"""
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent.parent
API = "https://tuluzencasa.com/wp-json/wp/v2"
AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
VALIDADOR = os.environ.get("VALIDADOR", "")  # ruta a validar.js (opcional)
W = "https://tuluzencasa.com"

# (ID origen, slug destino, texto original exacto, texto nuevo). Máximo 2 por artículo (PLAN.md).
ENLACES = [
    (92, "que-es-el-cups",
     "el CUPS (el código que identifica tu punto de suministro)",
     f'el CUPS (el <a href="{W}/que-es-el-cups/">código que identifica tu punto de suministro</a>)'),
    (92, "cambiar-compania-luz",
     "Antes de cambiar de compañía, revisa",
     f'Antes de <a href="{W}/cambiar-compania-luz/">cambiar de compañía</a>, revisa'),
    (94, "cambiar-compania-luz",
     "Antes de cambiar, revisa si tu contrato actual tiene permanencia.</p>",
     f'Antes de cambiar, revisa si tu contrato actual tiene permanencia. Te lo explicamos paso a paso en <a href="{W}/cambiar-compania-luz/">cómo cambiar de compañía de luz</a>.</p>'),
    (21, "diferencia-magnetotermico-diferencial",
     "Saltan por sobrecarga o por cortocircuito en ese circuito concreto.</li>",
     f'Saltan por sobrecarga o por cortocircuito en ese circuito concreto. Te contamos la <a href="{W}/diferencia-magnetotermico-diferencial/">diferencia entre magnetotérmico y diferencial</a>.</li>'),
    (17, "consumo-fantasma",
     "desenchufarla o apagar la regleta cuando no la usas elimina ese gasto del todo.</p>",
     f'desenchufarla o apagar la regleta cuando no la usas elimina ese gasto del todo. Es lo que se llama <a href="{W}/consumo-fantasma/">consumo fantasma</a>.</p>'),
]


def get(path):
    r = requests.get(API + path, auth=AUTH, timeout=60)
    if r.status_code == 403:
        sys.exit("403: posible firewall/HackGuardian. Paro.")
    return r.json()


def publicado(slug):
    return any(p["status"] == "publish" for p in get(f"/posts?slug={slug}&status=any&_fields=id,status"))


def valida(html):
    if not VALIDADOR:
        return True
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
    out = subprocess.run(["node", VALIDADOR, f.name], capture_output=True, text=True).stdout
    return "no válidos: 0" in out


if __name__ == "__main__":
    aplicar = "--aplicar" in sys.argv
    copia = BASE / "rediseno" / "copia-seguridad" / f"{datetime.date.today()}-enlaces"
    destinos = {s: publicado(s) for s in {e[1] for e in ENLACES}}
    por_origen = {}
    for e in ENLACES:
        por_origen.setdefault(e[0], []).append(e)
    for pid, lista in por_origen.items():
        post = get(f"/posts/{pid}?context=edit")
        c = post["content"]["raw"]
        nuevo, hechos = c, []
        for _, slug, viejo, repl in lista:
            if f"/{slug}/" in c:
                print(f"{pid} {post['slug']} -> {slug}: ya enlaza, nada que hacer"); continue
            if nuevo.count(viejo) != 1:
                print(f"{pid} {post['slug']} -> {slug}: el texto original aparece {nuevo.count(viejo)} veces; no lo toco"); continue
            if not destinos[slug]:
                print(f"{pid} {post['slug']} -> {slug}: preparado (el destino aún no está publicado)"); continue
            nuevo = nuevo.replace(viejo, repl); hechos.append(slug)
        if not hechos:
            continue
        if not aplicar:
            print(f"{pid} {post['slug']}: se añadirían {hechos}"); continue
        if not valida(nuevo):
            print(f"{pid}: bloques no válidos tras el cambio; no lo toco"); continue
        copia.mkdir(parents=True, exist_ok=True)
        (copia / f"entrada-{pid}.json").write_text(json.dumps(post, ensure_ascii=False, indent=1), encoding="utf-8")
        if get(f"/posts/{pid}?context=edit&_fields=modified")["modified"] != post["modified"]:
            print(f"{pid}: ha cambiado mientras trabajaba; no lo toco"); continue
        r = requests.post(f"{API}/posts/{pid}", auth=AUTH, json={"content": nuevo}, timeout=60)
        chk = get(f"/posts/{pid}?context=edit")
        print(f"{pid} {post['slug']}: {r.status_code}, estado {chk['status']}, contenido igual {chk['content']['raw'] == nuevo}, añadidos {hechos}")
