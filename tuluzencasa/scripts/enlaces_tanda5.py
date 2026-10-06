"""Enlaces desde artículos publicados hacia los de la tanda 2 de 4 (214-217).

Uso: python3 scripts/enlaces_tanda5.py            -> simulación: dice qué cambiaría
     python3 scripts/enlaces_tanda5.py --aplicar  -> aplica SOLO los enlaces cuyo destino ya está publicado

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
    (17, "cuanto-consume-horno-electrico",
     "comparando con un horno de 2.200 W, el mismo",
     f'comparando con <a href="{W}/cuanto-consume-horno-electrico/">un horno de 2.200 W</a>, el mismo'),
    (20, "cuanto-consume-horno-electrico",
     "lo contrario de la freidora o el horno:",
     f'lo contrario de la freidora o <a href="{W}/cuanto-consume-horno-electrico/">el horno eléctrico</a>:'),
    (94, "cuanto-consume-lavadora",
     "el lavavajillas o la lavadora de madrugada",
     f'el lavavajillas o <a href="{W}/cuanto-consume-lavadora/">la lavadora</a> de madrugada'),
    (106, "cuanto-consume-secadora",
     "si tarda 6 horas, frente a 0,33 € de una secadora de evacuación.",
     f'si tarda 6 horas, frente a 0,33 € de <a href="{W}/cuanto-consume-secadora/">una secadora de evacuación</a>.'),
    (134, "cuanto-consume-lavavajillas",
     "de la lavadora y el lavavajillas:",
     f'de la lavadora y <a href="{W}/cuanto-consume-lavavajillas/">el lavavajillas</a>:'),
    (134, "cuanto-consume-secadora",
     "La secadora le sigue, con 3,36 € al mes si haces 12 coladas.",
     f'La secadora le sigue, con 3,36 € al mes si haces 12 coladas; te contamos <a href="{W}/cuanto-consume-secadora/">cuánto consume una secadora</a> según su tipo.'),
    (136, "cuanto-consume-lavadora",
     "lavadora con sol.",
     f'<a href="{W}/cuanto-consume-lavadora/">lavadora</a> con sol.'),
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
    copia = BASE / "rediseno" / "copia-seguridad" / f"{datetime.date.today()}-enlaces-tanda2"
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
