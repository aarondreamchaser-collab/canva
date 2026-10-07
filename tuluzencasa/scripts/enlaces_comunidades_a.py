"""Enlaces internos hacia las páginas de comunidades (335-338). Máximo 2 nuevos por artículo.

Uso: python3 scripts/enlaces_comunidades_a.py            -> simulación
     python3 scripts/enlaces_comunidades_a.py --aplicar
Copia previa en rediseno/copia-seguridad/2026-10-07-enlaces-comunidades/. Comprueba «modified» antes de escribir.
También aplica el cambio a articulos/<slug>.html y src/<slug>.txt si contienen el mismo texto.
"""
import json, sys
from pathlib import Path
from subir2 import req

BASE = Path(__file__).resolve().parent.parent
D = BASE / "rediseno" / "copia-seguridad" / "2026-10-07-enlaces-comunidades"
U = "https://tuluzencasa.com"
A = lambda slug, txt: f'<a href="{U}/{slug}/">{txt}</a>'
CAMBIOS = {  # id: (slug, [(texto actual, texto nuevo), …])
    286: ("luz-en-aragon", [(
        "Para el autoconsumo, la instalación también se registra ante el Gobierno de Aragón, como cualquier instalación eléctrica.",
        "Para el autoconsumo, la instalación también se registra ante el Gobierno de Aragón, como cualquier instalación eléctrica. "
        f"En las comunidades vecinas cambian el trámite y la producción: lo tienes en {A('luz-en-cataluna', 'luz en Cataluña')} "
        f"y en {A('luz-en-comunidad-valenciana', 'luz en la Comunidad Valenciana')}.")]),
    136: ("placas-solares-en-casa", [(
        "Y cómo cambia el ahorro de la misma instalación según la ciudad:",
        f"Y cómo cambia el ahorro de la misma instalación según la ciudad. Tienes el cálculo de cada capital andaluza en {A('luz-en-andalucia', 'luz en Andalucía')} "
        f"y el de Madrid, con sus trámites, en {A('luz-en-madrid', 'luz en la Comunidad de Madrid')}:")]),
    135: ("bono-social-electrico", [(
        "reclamar ante los servicios de consumo de tu comunidad.",
        "reclamar ante los servicios de consumo de tu comunidad. Los organismos de cada una los recogemos en nuestras páginas por comunidades, "
        f"por ejemplo {A('luz-en-cataluna', 'luz en Cataluña')} o {A('luz-en-madrid', 'luz en la Comunidad de Madrid')}.")]),
    315: ("bono-social-termico", [(
        f'Te explicamos cómo leerla con el ejemplo de las capitales de Aragón en <a href="{U}/luz-en-aragon/">luz en Aragón</a>.',
        f'Te explicamos cómo leerla con el ejemplo de las capitales de Aragón en <a href="{U}/luz-en-aragon/">luz en Aragón</a>, '
        f"y las de otras provincias en {A('luz-en-andalucia', 'luz en Andalucía')} o {A('luz-en-comunidad-valenciana', 'luz en la Comunidad Valenciana')}.")]),
}

if __name__ == "__main__":
    aplicar = "--aplicar" in sys.argv
    mods = json.loads((D / "modified.json").read_text())
    for pid, (slug, reps) in CAMBIOS.items():
        raw = (D / f"post-{pid}-{slug}-antes.html").read_text()
        new = raw
        for a, b in reps:
            assert new.count(a) == 1, (pid, a[:50])
            new = new.replace(a, b)
        n = new.count('href="https://tuluzencasa.com/') - raw.count('href="https://tuluzencasa.com/')
        assert n <= 2, (pid, n)
        print(f"{pid} {slug}: +{n} enlaces")
        locales = []
        for f in (BASE / "articulos" / f"{slug}.html", BASE / "src" / f"{slug}.txt"):
            if f.exists():
                t = f.read_text()
                if all(t.count(a) == 1 for a, _ in reps):
                    for a, b in reps:
                        t = t.replace(a, b)
                    locales.append((f, t))
                else:
                    print(f"   {f.name}: no coincide, no lo toco")
        if not aplicar:
            continue
        c, p = req("GET", f"/wp/v2/posts/{pid}?context=edit&_fields=modified,status")
        if p["modified"] != str(mods[str(pid)]):
            print("   ha cambiado desde la copia; no lo toco"); continue
        c, _ = req("POST", f"/wp/v2/posts/{pid}", {"content": new})
        c2, p = req("GET", f"/wp/v2/posts/{pid}?context=edit&_fields=status,content")
        print(f"   {c} · estado {p['status']} · igual {p['content']['raw'] == new}")
        (D / f"post-{pid}-{slug}-despues.html").write_text(new)
        for f, t in locales:
            f.write_text(t); print(f"   actualizado {f.relative_to(BASE)}")
