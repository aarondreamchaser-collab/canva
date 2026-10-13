"""Enlaces internos hacia los artículos de la tanda 10 (374-381). Máximo 2 nuevos por artículo.

Uso: python3 scripts/enlaces_tanda10.py            -> simulación
     python3 scripts/enlaces_tanda10.py --aplicar
Copia previa en rediseno/copia-seguridad/2026-10-13-enlaces-tanda10/. Comprueba «modified» antes de escribir.
También aplica el cambio a articulos/<slug>.html y src/<slug>.txt si contienen el mismo texto.
"""
import json, sys
from pathlib import Path
from subir2 import req

BASE = Path(__file__).resolve().parent.parent
D = BASE / "rediseno" / "copia-seguridad" / "2026-10-13-enlaces-tanda10"
U = "https://tuluzencasa.com"
A = lambda slug, txt: f'<a href="{U}/{slug}/">{txt}</a>'
CAMBIOS = {  # id: (slug, [(texto actual, texto nuevo), …])
    286: ("luz-en-aragon", [(
        "Te comparamos todos los sistemas eléctricos en <a href=\"https://tuluzencasa.com/calefaccion-electrica-mas-barata/\">calefacción eléctrica más barata</a>.",
        "Te comparamos todos los sistemas eléctricos en <a href=\"https://tuluzencasa.com/calefaccion-electrica-mas-barata/\">calefacción eléctrica más barata</a>. "
        f"Lo mismo pasa en Castilla y León, con cuatro capitales en zona E1: lo tienes en {A('luz-en-castilla-y-leon', 'luz en Castilla y León')}.")]),
    315: ("bono-social-termico", [(
        f'o <a href="{U}/luz-en-comunidad-valenciana/">luz en la Comunidad Valenciana</a>.',
        f'o <a href="{U}/luz-en-comunidad-valenciana/">luz en la Comunidad Valenciana</a>. Para zonas muy frías, mira {A("luz-en-castilla-y-leon", "luz en Castilla y León")}, '
        f'y para la más suave, la α, {A("luz-en-canarias", "luz en Canarias")}.')]),
    92: ("como-leer-factura-luz", [(
        "es el precio que de verdad te cuesta cada kWh una vez sumados el impuesto eléctrico y el IVA.</p>",
        "es el precio que de verdad te cuesta cada kWh una vez sumados el impuesto eléctrico y el IVA. "
        f"En Canarias no hay IVA: la luz de casa lleva IGIC, con un tipo del 0 % hasta 10 kW, y te lo explicamos en {A('luz-en-canarias', 'luz en Canarias')}.</p>")]),
    137: ("cuanto-cuesta-cargar-coche-electrico-casa", [(
        "Sí. Si tu plaza es individual, solo tienes que comunicarlo antes a la comunidad. El coste de la instalación y la electricidad que consumas los pagas tú.",
        "Sí. Si tu plaza es individual, solo tienes que comunicarlo antes a la comunidad. El coste de la instalación y la electricidad que consumas los pagas tú. "
        f"Los esquemas de conexión y la deducción del IRPF los contamos en {A('punto-recarga-garaje-normativa', 'punto de recarga en casa y en garaje comunitario')}.")]),
    96: ("bomba-calor-radiadores-electricos", [(
        "Si además la usas como aire acondicionado en verano, parte de la inversión la habrías hecho igualmente.</p>",
        "Si además la usas como aire acondicionado en verano, parte de la inversión la habrías hecho igualmente. "
        f"Y si la obra mejora la calificación energética de tu vivienda, y lo acredita el certificado, puede darte una deducción en la renta: lo explicamos en {A('deducciones-irpf-eficiencia-energetica', 'deducciones del IRPF por eficiencia energética')}.</p>")]),
    136: ("placas-solares-en-casa", [(
        "En Bilbao, cada kWp produce alrededor de un 30 % menos que en Sevilla.",
        f"En Bilbao, cada kWp produce alrededor de un 30 % menos que en Sevilla: lo calculamos para las tres capitales vascas en {A('luz-en-pais-vasco', 'luz en el País Vasco')}, "
        f"y para todas las comunidades en {A('placas-solares-produccion-comunidad', 'cuánto producen las placas solares en cada comunidad')}.")]),
    358: ("compensacion-excedentes-placas", [(
        "En el año son 77,24 € que la casa de ejemplo regala a la red.",
        f"En el año son 77,24 € que la casa de ejemplo regala a la red. Cómo cambia la producción de una comunidad a otra lo tienes en {A('placas-solares-produccion-comunidad', 'cuánto producen las placas solares en cada comunidad')}.")]),
    337: ("luz-en-madrid", [(
        "Cada kWp produce unos 1.622 kWh al año en la capital: más que en Barcelona y casi tanto como en Sevilla.",
        f"Cada kWp produce unos 1.622 kWh al año en la capital: más que en Barcelona y casi tanto como en Sevilla. En el norte, mucho menos: en A Coruña, unos 1.298, como contamos en {A('luz-en-galicia', 'luz en Galicia')}.")]),
    19: ("cuanto-consume-termo-electrico", [(
        "Más potencia calienta antes, pero gasta lo mismo por litro calentado.</p>",
        f"Más potencia calienta antes, pero gasta lo mismo por litro calentado. Si quieres gastar menos con la misma agua caliente, mira {A('termo-aerotermico-consumo', 'cuánto consume un termo aerotérmico')}.</p>")]),
    284: ("cuanto-consume-aerotermia", [(
        "El termo y sus trucos para gastar menos están en <a href=\"https://tuluzencasa.com/cuanto-consume-termo-electrico/\">cuánto consume un termo eléctrico</a>.</p>",
        "El termo y sus trucos para gastar menos están en <a href=\"https://tuluzencasa.com/cuanto-consume-termo-electrico/\">cuánto consume un termo eléctrico</a>, "
        f"y si solo quieres cambiar el agua caliente, sin tocar la calefacción, en {A('termo-aerotermico-consumo', 'cuánto consume un termo aerotérmico')}.</p>")]),
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
