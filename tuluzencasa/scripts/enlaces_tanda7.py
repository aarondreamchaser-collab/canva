"""Enlaces desde artículos publicados hacia los de la tanda 4 de 4 (283-286).

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
    (93, "boletin-electrico",
     "certificado de instalación eléctrica (el «boletín»)",
     f'certificado de instalación eléctrica (el «<a href="{W}/boletin-electrico/">boletín</a>»)'),
    (136, "boletin-electrico",
     "una empresa instaladora habilitada, que debe legalizarla según",
     f'una empresa instaladora habilitada, que debe <a href="{W}/boletin-electrico/">legalizarla</a> según'),
    (137, "boletin-electrico",
     "que prepara la documentación técnica antes de ejecutarla.",
     f'que prepara <a href="{W}/boletin-electrico/">la documentación técnica</a> antes de ejecutarla.'),
    (96, "cuanto-consume-aerotermia",
     "En la mayoría de las casas, la bomba de calor es un split de aire acondicionado con modo calor. Si ya",
     f'En la mayoría de las casas, la bomba de calor es un split de aire acondicionado con modo calor; la que calienta el agua de radiadores o suelo radiante es la <a href="{W}/cuanto-consume-aerotermia/">aerotermia</a>. Si ya'),
    (104, "cuanto-consume-aerotermia",
     "el único sistema eléctrico que da más calor que la electricidad que consume es la bomba de calor.",
     f'el único sistema eléctrico que da más calor que la electricidad que consume es la bomba de calor, sea un split o un equipo de <a href="{W}/cuanto-consume-aerotermia/">aerotermia</a>.'),
    (204, "se-ha-ido-la-luz",
     "ni el teléfono de averías de tu zona.",
     f'ni <a href="{W}/se-ha-ido-la-luz/">el teléfono de averías</a> de tu zona.'),
    (205, "se-ha-ido-la-luz",
     "como un cambio de potencia, una avería o una reclamación.",
     f'como un cambio de potencia, <a href="{W}/se-ha-ido-la-luz/">una avería</a> o una reclamación.'),
    (94, "se-ha-ido-la-luz",
     "el servicio técnico (averías, cortes, contador)",
     f'el servicio técnico (<a href="{W}/se-ha-ido-la-luz/">averías, cortes</a>, contador)'),
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
    copia = BASE / "rediseno" / "copia-seguridad" / f"{datetime.date.today()}-enlaces-tanda4"
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
