"""Sube imágenes de imagenes-destacadas/ a la biblioteca de medios y las asigna como imagen destacada.

Uso: python3 scripts/imagenes_destacadas.py ID [ID …]   (los ID deben estar en ALT)
Lee WP_USER y WP_APP_PASSWORD (nunca los imprime). No cambia el estado de ninguna entrada.
"""
import base64, json, os, sys, urllib.request, urllib.error
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
API = "https://tuluzencasa.com/wp-json"
AUTH = "Basic " + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
ALT = {
    92: "Contador eléctrico digital con la lectura de kWh, visto a través de la mirilla del armario",
    104: "Emisor térmico eléctrico instalado en la pared de una vivienda",
    93: "Cuadro eléctrico de una vivienda con interruptores magnetotérmicos y diferencial",
    94: "Teclado de una calculadora, para comparar lo que cuesta la luz",
    95: "Comedor luminoso con un radiador eléctrico de zócalo bajo la ventana",
    96: "Unidad interior de una bomba de calor tipo split en la pared",
    97: "Radiador de aceite eléctrico junto a un ventilador en un rincón de casa",
    98: "Estufa eléctrica cerámica encendida, con el piloto rojo iluminado",
    105: "Dormitorio con cama de matrimonio y manta para dormir caliente en invierno",
    106: "Cristal de una ventana empañado por la condensación de la humedad",
}


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
        return e.code, e.read().decode(errors="replace")[:300]


ids = {v["id"]: k for k, v in json.loads((BASE / "scripts/wp_ids.json").read_text()).items()}
registro_p = BASE / "scripts/wp_destacadas.json"
registro = json.loads(registro_p.read_text()) if registro_p.exists() else {}
for pid in map(int, sys.argv[1:]):
    slug = ids[pid]
    f = BASE / "imagenes-destacadas" / f"{slug}.jpg"
    s, post = req("GET", f"/wp/v2/posts/{pid}?context=edit")
    if s == 403:
        sys.exit("403: posible firewall/HackGuardian. Paro.")
    estado = post["status"]
    s, ya = req("GET", f"/wp/v2/media?search={slug}&per_page=20&context=edit")
    previa = [m for m in ya if m["slug"] == slug or m["source_url"].rsplit("/", 1)[-1].startswith(slug + ".")] if isinstance(ya, list) else []
    if previa:
        mid = previa[0]["id"]; print(pid, "ya estaba en medios:", mid)
    else:
        s, m = req("POST", "/wp/v2/media", raw=f.read_bytes(),
                   headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{slug}.jpg"'})
        if s not in (200, 201):
            print(pid, "ERROR al subir", s, m); continue
        mid = m["id"]
    s, m = req("POST", f"/wp/v2/media/{mid}", {"alt_text": ALT[pid], "title": ALT[pid], "post": pid})
    s2, p2 = req("POST", f"/wp/v2/posts/{pid}", {"featured_media": mid})
    s3, chk = req("GET", f"/wp/v2/posts/{pid}?context=edit")
    ok = chk["featured_media"] == mid and chk["status"] == estado
    registro[str(pid)] = {"slug": slug, "media": mid, "url": m.get("source_url") if isinstance(m, dict) else None, "alt": ALT[pid]}
    print(pid, slug, "media", mid, "| destacada", ok, "| estado", chk["status"], "|", m.get("media_details", {}).get("width") if isinstance(m, dict) else "")
registro_p.write_text(json.dumps(registro, ensure_ascii=False, indent=1))
