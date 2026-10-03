"""Sube artículos de build2.py como BORRADOR, con comentarios cerrados, Rank Math y schema BlogPosting.

Uso: python3 scripts/subir2.py slug1 slug2 …
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

# Schema que Rank Math guarda al elegir «Artículo» → BlogPosting en el editor. Los campos
# rank_math_rich_snippet / rank_math_snippet_article_type por sí solos dejan "@type" vacío.
SCHEMA = {
    "@type": "BlogPosting",
    "metadata": {"title": "Article", "type": "template", "shortcode": "", "isPrimary": True,
                 "reviewLocationShortcode": "[rank_math_rich_snippet]", "name": "Article"},
    "headline": "%seo_title%", "description": "%seo_description%", "keywords": "%keywords%",
    "datePublished": "%date(Y-m-dTH:i:sP)%", "dateModified": "%modified(Y-m-dTH:i:sP)%",
    "articleSection": "%primary_taxonomy_terms%",
    "author": {"@type": "Person", "name": "%name%"},
    "image": {"@type": "ImageObject", "url": "%post_thumbnail%"},
}


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


def schema(pid):
    return req("POST", "/rankmath/v1/updateSchemas", {"objectType": "post", "objectID": pid, "schemas": {"new-9999": SCHEMA}})


if __name__ == "__main__":
    meta = json.loads((BASE / "scripts" / "build2_meta.json").read_text(encoding="utf-8"))
    _, cats = req("GET", "/wp/v2/categories?per_page=100")
    cat_id = {c["slug"]: c["id"] for c in cats}
    ids_path = BASE / "scripts" / "wp_ids.json"
    ids = json.loads(ids_path.read_text()) if ids_path.exists() else {}

    for slug in sys.argv[1:]:
        m = meta[slug]
        code, found = req("GET", f"/wp/v2/posts?slug={slug}&status=any&context=edit&_fields=id,status")
        if code == 403:
            sys.exit("403 al consultar: posible firewall/HackGuardian. Paro.")
        if found:
            print(f"{slug}: ya existe (ID {found[0]['id']}, {found[0]['status']}); no lo toco")
            continue
        content = (BASE / "articulos" / f"{slug}.html").read_text(encoding="utf-8")
        code, post = req("POST", "/wp/v2/posts", {
            "title": m["title"], "slug": slug, "status": "draft", "content": content,
            "excerpt": m["excerpt"], "categories": [cat_id[m["category"]]],
            "comment_status": "closed", "ping_status": "closed",
        })
        if code == 403:
            sys.exit(f"{slug}: 403 al crear: posible firewall/HackGuardian. Paro.")
        if code not in (200, 201):
            print(f"{slug}: ERROR {code} {post}")
            continue
        pid = post["id"]
        _, chk = req("GET", f"/wp/v2/posts/{pid}?context=edit")
        print(f"{slug}: creado ID {pid} ({chk['status']}), contenido igual: {chk['content']['raw'] == content}")
        rcode, _ = req("POST", "/rankmath/v1/updateMeta", {
            "objectType": "post", "objectID": pid,
            "meta": {"rank_math_focus_keyword": m["keyword"], "rank_math_description": m["excerpt"],
                     "rank_math_title": m["title_seo"]},
        })
        scode, _ = schema(pid)
        print(f"   Rank Math meta: {rcode} · schema: {scode}")
        ids[slug] = {"id": pid, "rankmath_status": rcode}

    ids_path.write_text(json.dumps(ids, ensure_ascii=False, indent=1))
