"""Enlaces internos hacia la tanda 8 (314-317) desde artículos publicados. Máximo 2 nuevos por artículo.

Uso: python3 scripts/enlaces_tanda8.py            -> simulación
     python3 scripts/enlaces_tanda8.py --aplicar
Copia previa en rediseno/copia-seguridad/2026-10-07-enlaces-tanda8/. Comprueba «modified» antes de escribir.
También aplica el cambio a articulos/<slug>.html y src/<slug>.txt si contienen el mismo texto.
"""
import json, sys
from pathlib import Path
from subir2 import req

BASE = Path(__file__).resolve().parent.parent
D = BASE / "rediseno" / "copia-seguridad" / "2026-10-07-enlaces-tanda8"
U = "https://tuluzencasa.com"
A = lambda slug, txt: f'<a href="{U}/{slug}/">{txt}</a>'
CAMBIOS = {  # id: (slug, [(texto actual, texto nuevo), …])
    94: ("pvpc-mercado-libre", [(
        "lo que marca la diferencia es lo que consigas mover de lunes a viernes.",
        "lo que marca la diferencia es lo que consigas mover de lunes a viernes. Si dudas entre un precio fijo y uno que siga al mercado, "
        f"lo comparamos con los precios reales de los últimos 12 meses en {A('tarifa-fija-o-indexada', 'tarifa fija o indexada')}.")]),
    204: ("cambiar-compania-luz", [(
        f'Te lo explicamos en <a href="{U}/pvpc-mercado-libre/">PVPC o mercado libre</a>.',
        f'Te lo explicamos en <a href="{U}/pvpc-mercado-libre/">PVPC o mercado libre</a>, y lo que te juegas con cada uno en '
        f"{A('tarifa-fija-o-indexada', 'tarifa fija o indexada')}.")]),
    135: ("bono-social-electrico", [(
        "El alquiler del contador no tiene descuento.",
        "El alquiler del contador no tiene descuento. Y si tienes el bono a 31 de diciembre, al año siguiente recibes también el "
        f"{A('bono-social-termico', 'bono social térmico')}, una ayuda en dinero para la calefacción y el agua caliente.")]),
    95: ("calefaccion-electrica-mas-barata", [
        ("convierte cada kWh de electricidad en un kWh de calor, ni más ni menos.",
         f"convierte cada kWh de electricidad en un kWh de calor, ni más ni menos. También el {A('cuanto-consume-suelo-radiante-electrico', 'suelo radiante eléctrico')}."),
        ("<li><strong>Revisa la potencia contratada</strong>.",
         f"<li><strong>Si tienes el bono social eléctrico</strong>, recibes también el {A('bono-social-termico', 'bono social térmico')}, una ayuda anual para la calefacción.</li>\n"
         "<!-- /wp:list-item -->\n\n<!-- wp:list-item -->\n<li><strong>Revisa la potencia contratada</strong>.")]),
    134: ("tramos-horarios-luz", [(
        "También puedes verlo hora a hora en la web de tu distribuidora con tu contador digital.",
        "También puedes verlo hora a hora en la web de tu distribuidora o en Datadis: te explicamos cómo en "
        f"{A('ver-consumo-por-horas-datadis', 'ver tu consumo por horas')}.")]),
    203: ("consumo-fantasma", [(
        "multiplícalos por esa cifra.",
        "multiplícalos por esa cifra. O mira tu consumo de madrugada en la curva horaria de tu distribuidora: lo explicamos en "
        f"{A('ver-consumo-por-horas-datadis', 'ver tu consumo por horas')}.")]),
    104: ("cuanto-consumen-emisores-termicos", [(
        "pero la diferencia depende del modelo y de cómo lo uses.",
        "pero la diferencia depende del modelo y de cómo lo uses. Lo mismo pasa con el "
        f"{A('cuanto-consume-suelo-radiante-electrico', 'suelo radiante eléctrico')}: cambia cómo reparte el calor, no lo que cuesta cada kWh.")]),
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
