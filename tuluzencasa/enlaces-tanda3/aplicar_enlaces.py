"""Añade enlaces a los artículos nuevos (134–137) desde artículos ya publicados.
Uso: python3 aplicar_enlaces.py            -> prueba: muestra los cambios y valida los bloques, no toca nada
     python3 aplicar_enlaces.py aplicar    -> aplica (solo si los artículos de destino están publicados)
No cambia el estado de ninguna entrada. Lee WP_USER y WP_APP_PASSWORD (nunca los imprime)."""
import base64, json, os, subprocess, sys, tempfile, urllib.request, urllib.error
API = "https://tuluzencasa.com/wp-json"
AUTH = "Basic " + base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
VALIDADOR = os.environ.get("VALIDADOR", "/tmp/claude-0/-home-user-canva/557847bc-71e6-5871-a563-54935582d0d3/scratchpad/validador/validar.js")
T = "https://tuluzencasa.com/"
CAMBIOS = [  # (ID de la entrada publicada, texto que ya existe, texto nuevo, slugs de destino)
    (92, 'mira <a href="https://tuluzencasa.com/cuanto-consume-termo-electrico/">cuánto consume un termo eléctrico y cómo programarlo</a>.</p>',
         'mira <a href="https://tuluzencasa.com/cuanto-consume-termo-electrico/">cuánto consume un termo eléctrico y cómo programarlo</a>. Tienes los horarios de cada tramo y qué aparatos compensa mover en <a href="' + T + 'tramos-horarios-luz/">tramos horarios de la luz</a>.</p>',
         ["tramos-horarios-luz"]),
    (94, 'Si estás en mercado libre y cumples los requisitos, tienes que pasarte al PVPC para pedirlo.</p>',
         'Si estás en mercado libre y cumples los requisitos, tienes que pasarte al PVPC para pedirlo. Te explicamos los requisitos y cómo pedirlo en <a href="' + T + 'bono-social-electrico/">bono social eléctrico</a>.</p>',
         ["bono-social-electrico"]),
    (94, 'Compáralo con la tabla de arriba: por encima del punto de equilibrio, los tramos te salen más baratos.</p>',
         'Compáralo con la tabla de arriba: por encima del punto de equilibrio, los tramos te salen más baratos. Qué horas son valle y qué aparatos mover lo tienes en <a href="' + T + 'tramos-horarios-luz/">tramos horarios de la luz</a>.</p>',
         ["tramos-horarios-luz"]),
    (93, 'puedes necesitar más potencia en valle que durante el día.</p>',
         'puedes necesitar más potencia en valle que durante el día. Lo calculamos en <a href="' + T + 'cuanto-cuesta-cargar-coche-electrico-casa/">cuánto cuesta cargar un coche eléctrico en casa</a>.</p>',
         ["cuanto-cuesta-cargar-coche-electrico-casa"]),
    (19, 'frente a uno que lo hace en punta, de 13,40 €.</p>',
         'frente a uno que lo hace en punta, de 13,40 €. Los horarios de cada tramo están en <a href="' + T + 'tramos-horarios-luz/">tramos horarios de la luz</a>.</p>',
         ["tramos-horarios-luz"]),
]


def req(method, path, data=None):
    r = urllib.request.Request(API + path, method=method, data=json.dumps(data).encode() if data is not None else None,
                               headers={"Authorization": AUTH, "Content-Type": "application/json", "User-Agent": "tuluzencasa-enlaces/1.0"})
    try:
        with urllib.request.urlopen(r, timeout=60) as f:
            return f.status, json.loads(f.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


aplicar = sys.argv[1:] == ["aplicar"]
_, posts = req("GET", "/wp/v2/posts?status=any&per_page=100&context=edit&_fields=id,slug,status")
estado = {p["slug"]: p["status"] for p in posts}
por_id = {}
for pid, viejo, nuevo, destinos in CAMBIOS:
    por_id.setdefault(pid, []).append((viejo, nuevo, destinos))
for pid, cambios in por_id.items():
    s, p = req("GET", f"/wp/v2/posts/{pid}?context=edit")
    raw, mod = p["content"]["raw"], p["modified"]
    new = raw
    for viejo, nuevo, destinos in cambios:
        assert new.count(viejo) == 1, (pid, viejo[:60])
        pend = [d for d in destinos if estado.get(d) != "publish"]
        if aplicar and pend:
            sys.exit(f"{pid}: el destino {pend} no está publicado; no aplico nada.")
        new = new.replace(viejo, nuevo)
        print(f"\n{pid} ({p['slug']}, {p['status']})\n  ANTES: …{viejo}\n  AHORA: …{nuevo}")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(new)
    v = subprocess.run(["node", VALIDADOR, f.name], capture_output=True, text=True).stdout.strip().splitlines()[-1]
    print("  bloques:", v)
    assert "no válidos: 0" in v
    if aplicar:
        s2, q = req("GET", f"/wp/v2/posts/{pid}?context=edit")
        assert q["modified"] == mod
        s, r = req("POST", f"/wp/v2/posts/{pid}", {"content": new})
        s, q = req("GET", f"/wp/v2/posts/{pid}?context=edit")
        print("  aplicado:", q["content"]["raw"] == new, "· estado", q["status"])
