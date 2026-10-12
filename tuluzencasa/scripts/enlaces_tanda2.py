"""Enlaces internos hacia los artículos de la tanda 2 (355-358). Máximo 2 nuevos por artículo.

Uso: python3 scripts/enlaces_tanda2.py            -> simulación
     python3 scripts/enlaces_tanda2.py --aplicar
Copia previa en rediseno/copia-seguridad/2026-10-08-enlaces-tanda2/. Comprueba «modified» antes de escribir.
También aplica el cambio a articulos/<slug>.html y src/<slug>.txt si contienen el mismo texto.
"""
import json, sys
from pathlib import Path
from subir2 import req

BASE = Path(__file__).resolve().parent.parent
D = BASE / "rediseno" / "copia-seguridad" / "2026-10-08-enlaces-tanda2"
U = "https://tuluzencasa.com"
A = lambda slug, txt: f'<a href="{U}/{slug}/">{txt}</a>'
CAMBIOS = {  # id: (slug, [(texto actual, texto nuevo), …])
    93: ("que-potencia-contratar", [(
        "Si salta todas las semanas a la misma hora, sí: o separas esos aparatos o necesitas un escalón más.",
        "Si salta todas las semanas a la misma hora, sí: o separas esos aparatos o necesitas un escalón más. "
        f"Cómo pedirlo, cuánto cuesta y en qué plazo lo tienes en {A('cambiar-potencia-contratada', 'cambiar la potencia contratada')}.")]),
    316: ("ver-consumo-por-horas-datadis", [(
        "Por eso, antes de bajar la potencia, comprueba también qué aparatos usas a la vez.",
        "Por eso, antes de bajar la potencia, comprueba también qué aparatos usas a la vez. "
        f"Lo que cuesta el cambio y lo que ahorras lo explicamos en {A('cambiar-potencia-contratada', 'cambiar la potencia contratada')}.")]),
    283: ("boletin-electrico", [(
        "Te lo piden para dar de alta la luz en una vivienda nueva o después de una reforma, pero no para poner el contrato a tu nombre si no cambias nada.",
        f"Te lo piden para {A('alta-luz-vivienda', 'dar de alta la luz')} en una vivienda nueva o después de una reforma, "
        f"pero no para {A('cambio-titular-luz', 'poner el contrato a tu nombre')} si no cambias nada.")]),
    205: ("que-es-el-cups", [(
        "No. El CUPS va unido al punto de suministro, no a la empresa que te vende la luz ni al titular del contrato.",
        "No. El CUPS va unido al punto de suministro, no a la empresa que te vende la luz ni al titular del contrato. "
        f"Por eso es el dato que te pedirán para el {A('cambio-titular-luz', 'cambio de titular de la luz')}.")]),
    204: ("cambiar-compania-luz", [(
        "Si vas a cambiar también de titular, por ejemplo al alquilar una vivienda, díselo a la nueva comercializadora para que lo tramite.",
        "Si vas a cambiar también de titular, por ejemplo al alquilar una vivienda, díselo a la nueva comercializadora para que lo tramite. "
        f"Es gratis: te lo contamos en {A('cambio-titular-luz', 'cambio de titular de la luz')}.")]),
    136: ("placas-solares-en-casa", [(
        "Por eso en verano, cuando sobra mucho, parte de los excedentes no te reporta nada.",
        "Por eso en verano, cuando sobra mucho, parte de los excedentes no te reporta nada. "
        f"Lo calculamos mes a mes, con la batería virtual, en {A('compensacion-excedentes-placas', 'compensación de excedentes')}.")]),
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
