"""Sube una página de build2.py como BORRADOR (sin menú), con Rank Math (título, descripción y palabra clave).

Uso: python3 scripts/subir_pagina.py slug
Lee las credenciales de WP_USER y WP_APP_PASSWORD (nunca las imprime). Si el slug ya existe, no lo toca.
"""
import json
import sys
from pathlib import Path
from subir2 import req

BASE = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    slug = sys.argv[1]
    m = json.loads((BASE / "scripts" / "build2_meta.json").read_text(encoding="utf-8"))[slug]
    code, found = req("GET", f"/wp/v2/pages?slug={slug}&status=any&context=edit&_fields=id,status")
    if code == 403:
        sys.exit("403 al consultar: posible firewall/HackGuardian. Paro.")
    if found:
        sys.exit(f"{slug}: ya existe (ID {found[0]['id']}, {found[0]['status']}); no lo toco")
    content = (BASE / "articulos" / f"{slug}.html").read_text(encoding="utf-8")
    code, page = req("POST", "/wp/v2/pages", {"title": m["title"], "slug": slug, "status": "draft", "content": content,
                                               "excerpt": m["excerpt"], "comment_status": "closed", "ping_status": "closed"})
    if code == 403:
        sys.exit("403 al crear: posible firewall/HackGuardian. Paro.")
    if code not in (200, 201):
        sys.exit(f"ERROR {code} {page}")
    pid = page["id"]
    _, chk = req("GET", f"/wp/v2/pages/{pid}?context=edit")
    print(f"{slug}: página creada ID {pid} ({chk['status']}), contenido igual: {chk['content']['raw'] == content}")
    rcode, _ = req("POST", "/rankmath/v1/updateMeta", {"objectType": "post", "objectID": pid, "meta": {
        "rank_math_focus_keyword": m["keyword"], "rank_math_description": m["excerpt"], "rank_math_title": m["title_seo"]}})
    print(f"   Rank Math meta: {rcode}")
    p = BASE / "scripts" / "wp_ids.json"
    ids = json.loads(p.read_text())
    ids[slug] = {"id": pid, "tipo": "pagina", "rankmath_status": rcode}
    p.write_text(json.dumps(ids, ensure_ascii=False, indent=1))
