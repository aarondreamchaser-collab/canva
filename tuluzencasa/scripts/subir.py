"""Crea los artículos como BORRADOR en WordPress e intenta guardar los campos de Rank Math.

Lee las credenciales de WP_USER y WP_APP_PASSWORD (nunca las imprime).
Si un slug ya existe, no lo toca. Guarda los IDs en scripts/wp_ids.json.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
API = "https://tuluzencasa.com/wp-json"
AUTH = "Basic " + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()


def req(method, path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(API + path, data=body, method=method,
                               headers={"Authorization": AUTH, "Content-Type": "application/json",
                                        "User-Agent": "tuluzencasa-drafts/1.0"})
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, json.loads(resp.read() or b"null")
    except urllib.error.HTTPError as e:
        txt = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(txt)
        except ValueError:
            return e.code, txt[:300]


meta = json.loads((BASE / "scripts" / "build_meta.json").read_text(encoding="utf-8"))
_, cats = req("GET", "/wp/v2/categories?per_page=100")
cat_id = {c["slug"]: c["id"] for c in cats}
ids_path = BASE / "scripts" / "wp_ids.json"
ids = json.loads(ids_path.read_text()) if ids_path.exists() else {}

for slug, m in meta.items():
    code, found = req("GET", f"/wp/v2/posts?slug={slug}&status=any&context=edit&_fields=id,status")
    if code == 403:
        sys.exit("403 al consultar: posible firewall/HackGuardian. Paro.")
    if found:
        print(f"{slug}: ya existe (ID {found[0]['id']}, {found[0]['status']}); no lo toco")
        ids.setdefault(slug, {})["id"] = found[0]["id"]
        continue
    content = (BASE / "articulos" / f"{slug}.html").read_text(encoding="utf-8")
    code, post = req("POST", "/wp/v2/posts", {
        "title": m["title"], "slug": slug, "status": "draft", "content": content,
        "excerpt": m["excerpt"], "categories": [cat_id[m["category"]]],
    })
    if code == 403:
        sys.exit(f"{slug}: 403 al crear: posible firewall/HackGuardian. Paro.")
    if code not in (200, 201):
        print(f"{slug}: ERROR {code} {post}")
        continue
    pid = post["id"]
    print(f"{slug}: creado ID {pid} ({post['status']})")
    rcode, rres = req("POST", "/rankmath/v1/updateMeta", {
        "objectType": "post", "objectID": pid,
        "meta": {"rank_math_focus_keyword": m["keyword"], "rank_math_description": m["excerpt"]},
    })
    print(f"   Rank Math updateMeta: {rcode} {str(rres)[:200]}")
    ids[slug] = {"id": pid, "rankmath_status": rcode}

ids_path.write_text(json.dumps(ids, ensure_ascii=False, indent=1))
