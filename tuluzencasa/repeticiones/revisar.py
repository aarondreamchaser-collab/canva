"""Simula los cambios de cambios_publicados.py: comprueba que cada texto aparece una vez, valida bloques y
escribe repeticiones/cambios-publicados.md. Con --aplicar, hace copia y los aplica (solo contenido)."""
import json, os, subprocess, sys, tempfile, datetime, requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cambios_publicados import CAMBIOS
BASE = Path(__file__).resolve().parent.parent
API = "https://tuluzencasa.com/wp-json/wp/v2"
AUTH = (os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"])
VAL = os.environ["VALIDADOR"]
aplicar = "--aplicar" in sys.argv
if "--hasta" in sys.argv: CAMBIOS = CAMBIOS[:int(sys.argv[sys.argv.index("--hasta") + 1])]
por = {}
for c in CAMBIOS: por.setdefault(c[0], []).append(c)
md = [(Path(__file__).parent / "cabecera.md").read_text(encoding="utf-8")]
copia = BASE / "rediseno" / "copia-seguridad" / f"{datetime.date.today()}-repeticiones"
for pid, lista in por.items():
    post = requests.get(f"{API}/posts/{pid}?context=edit", auth=AUTH, timeout=60).json()
    assert post["status"] == "publish", (pid, post["status"])
    c = post["content"]["raw"]; n = c
    md.append(f"\n## {pid} · {post['title']['raw']}\n")
    for _, motivo, viejo, nuevo in lista:
        k = n.count(viejo)
        assert k == 1, (pid, k, viejo[:60])
        n = n.replace(viejo, nuevo)
        md.append(f"- **{motivo}**\n  - Antes: {viejo}\n  - Después: {nuevo}\n")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f: f.write(n)
    ok = "no válidos: 0" in subprocess.run(["node", VAL, f.name], capture_output=True, text=True).stdout
    print(pid, post["slug"], len(lista), "cambios · bloques válidos:", ok)
    assert ok
    if aplicar:
        copia.mkdir(parents=True, exist_ok=True)
        (copia / f"entrada-{pid}.json").write_text(json.dumps(post, ensure_ascii=False, indent=1), encoding="utf-8")
        chk = requests.get(f"{API}/posts/{pid}?context=edit&_fields=modified", auth=AUTH, timeout=60).json()
        assert chk["modified"] == post["modified"], f"{pid} cambió mientras trabajaba"
        r = requests.post(f"{API}/posts/{pid}", auth=AUTH, json={"content": n}, timeout=60)
        d = requests.get(f"{API}/posts/{pid}?context=edit", auth=AUTH, timeout=60).json()
        print("   aplicado:", r.status_code, d["status"], d["content"]["raw"] == n)
(Path(__file__).parent / "cambios-publicados.md").write_text("\n".join(md).replace("<strong>", "**").replace("</strong>", "**").replace("</p>", ""), encoding="utf-8")
