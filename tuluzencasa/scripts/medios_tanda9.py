"""Sube las imágenes destacadas de la tanda 9 (355-358) y las asigna. No cambia el estado de ninguna entrada.

Uso: python3 scripts/medios_tanda9.py [slug …]   -> simulación (todos o solo esos slugs)
     python3 scripts/medios_tanda9.py --aplicar
Lee WP_USER y WP_APP_PASSWORD (nunca los imprime). Guarda los IDs en scripts/wp_medios_tanda9.json.
"""
import base64, json, os, sys, urllib.request, urllib.error
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
API = "https://tuluzencasa.com/wp-json"
AUTH = "Basic " + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
POSTS = {"cambiar-potencia-contratada": 355, "alta-luz-vivienda": 356, "cambio-titular-luz": 357, "compensacion-excedentes-placas": 358}


def req(method, path, data=None, raw=None, headers=None):
    h = {"Authorization": AUTH, "User-Agent": "tuluzencasa-media/1.0"}
    if raw is None:
        h["Content-Type"] = "application/json"
    h.update(headers or {})
    body = raw if raw is not None else (json.dumps(data).encode() if data is not None else None)
    r = urllib.request.Request(API + path, data=body, method=method, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.status, json.loads(resp.read() or b"null")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            sys.exit("403: posible firewall/HackGuardian. Paro.")
        return e.code, e.read().decode(errors="replace")[:300]


aplicar = "--aplicar" in sys.argv
solo = [a for a in sys.argv[1:] if not a.startswith("--")]
if solo:
    POSTS = {k: v for k, v in POSTS.items() if k in solo}
meta = json.loads((BASE / "imagenes-destacadas" / "tanda9.json").read_text())
reg_p = BASE / "scripts" / "wp_medios_tanda9.json"
reg = json.loads(reg_p.read_text()) if reg_p.exists() else {}
for slug, pid in POSTS.items():
    s, post = req("GET", f"/wp/v2/posts/{pid}?context=edit&_fields=id,slug,status,featured_media,modified")
    assert post["slug"] == slug, (pid, post["slug"])
    print(f"{pid} {slug}: estado {post['status']}, destacada actual {post['featured_media']}")
    if not aplicar:
        continue
    if slug in reg:
        mid = reg[slug]["id"]
    else:
        f = BASE / "imagenes-destacadas" / f"{slug}.jpg"
        s, m = req("POST", "/wp/v2/media", raw=f.read_bytes(),
                   headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{slug}.jpg"'})
        assert s == 201, (s, m)
        mid = m["id"]
        req("POST", f"/wp/v2/media/{mid}", {"alt_text": meta[slug]["alt"], "title": slug, "post": pid})
        reg[slug] = {"id": mid, "url": m["source_url"], "alt": meta[slug]["alt"]}
        reg_p.write_text(json.dumps(reg, ensure_ascii=False, indent=1))
    s, chk = req("GET", f"/wp/v2/posts/{pid}?context=edit&_fields=modified")
    if chk["modified"] != post["modified"]:
        print("   ha cambiado mientras trabajaba; no lo toco"); continue
    s, r = req("POST", f"/wp/v2/posts/{pid}", {"featured_media": mid})
    s, fin = req("GET", f"/wp/v2/posts/{pid}?context=edit&_fields=status,featured_media")
    print(f"   medio {mid} · destacada {fin['featured_media']} · estado {fin['status']}")
