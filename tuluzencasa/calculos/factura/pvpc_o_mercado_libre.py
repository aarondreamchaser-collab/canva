"""Cifras del artículo «PVPC o mercado libre».

Compara, con el piso de 3 personas de nuestra calculadora de consumo, el precio fijo (0,13 €/kWh) con
el precio por tramos (0,19 / 0,12 / 0,08 €/kWh), antes y después de mover el termo
y el lavavajillas a la madrugada. Todo con impuesto eléctrico e IVA.
Uso: python3 calculos/pvpc_o_mercado_libre.py
"""
import json, os
from comun import *


def energia(cambios=None):
    cambios = cambios or {}
    tot = p = l = v = 0
    for k, (n, w, h, d, f, r) in EJEMPLO.items():
        f = cambios.get(k, f)
        e = kwh_mes(w, h, d, r)
        rp = reparto(f)
        tot += e; p += e * rp['p']; l += e * rp['l']; v += e * rp['v']
    fijo = tot * PRECIO_UNICO * IMP
    tramos = (p * PRECIO_PUNTA + l * PRECIO_LLANO + v * PRECIO_VALLE) * IMP
    return dict(kwh=tot, pct_valle=v / tot, pct_punta=p / tot, fijo_mes=fijo, tramos_mes=tramos,
                fijo_anio=fijo * 12, tramos_anio=tramos * 12, precio_medio_tramos=tramos / tot)


actual = energia()
movido = energia({'ter': 'madrugada', 'lvv': 'madrugada'})

# Precio medio por tramos según el % de consumo en valle (resto repartido como el ejemplo: punta/llano)
ratio_pl = actual['pct_punta'] / (1 - actual['pct_valle'])
curva = []
for pv in (0.3, 0.4, 0.5, 0.6, 0.7):
    pp = (1 - pv) * ratio_pl
    pl = (1 - pv) - pp
    precio = (pp * PRECIO_PUNTA + pl * PRECIO_LLANO + pv * PRECIO_VALLE) * IMP
    curva.append(dict(pct_valle=pv, precio=precio))
# Punto de equilibrio
lo, hi = 0.0, 1.0
for _ in range(60):
    mid = (lo + hi) / 2
    pp = (1 - mid) * ratio_pl; pl = (1 - mid) - pp
    if (pp * PRECIO_PUNTA + pl * PRECIO_LLANO + mid * PRECIO_VALLE) > PRECIO_UNICO: lo = mid
    else: hi = mid
equilibrio = hi

anual_fijo = {c: c * 12 * PRECIO_UNICO * IMP for c in (150, 250, 350)}

r = dict(sobrecoste_tramos_actual_anio=actual['tramos_anio'] - actual['fijo_anio'], actual=actual, movido=movido, curva=curva, equilibrio_valle=equilibrio,
         ahorro_mover_anio=actual['tramos_anio'] - movido['tramos_anio'],
         ventaja_tramos_movido_anio=movido['fijo_anio'] - movido['tramos_anio'],
         precio_fijo_con_imp=PRECIO_UNICO * IMP, anual_fijo=anual_fijo)

if __name__ == '__main__':
    json.dump(r, open(os.path.join(os.path.dirname(__file__), 'salida', 'pvpc-o-mercado-libre.json'), 'w'), indent=1)
    for n, e in (('Uso actual', actual), ('Termo y lavavajillas de madrugada', movido)):
        print(f"{n}: {eur(e['kwh'],1)} kWh/mes, valle {eur(100*e['pct_valle'],0)} %, punta {eur(100*e['pct_punta'],0)} %")
        print(f"   fijo {eur(e['fijo_mes'])} €/mes ({eur(e['fijo_anio'])} €/año) · tramos {eur(e['tramos_mes'])} €/mes ({eur(e['tramos_anio'])} €/año) · precio medio tramos {eur(e['precio_medio_tramos'],3)} €/kWh")
    print(f"\nMover termo y lavavajillas ahorra con tramos {eur(r['ahorro_mover_anio'])} €/año; con ese uso, tramos frente a fijo: {eur(r['ventaja_tramos_movido_anio'])} €/año")
    print(f"Con el uso actual, tramos cuesta {eur(r['sobrecoste_tramos_actual_anio'])} €/año más que fijo")
    print(f"Precio fijo con impuestos: {eur(r['precio_fijo_con_imp'],3)} €/kWh")
    for c in curva: print(f"  valle {eur(100*c['pct_valle'],0)} % -> {eur(c['precio'],3)} €/kWh")
    print(f"Equilibrio: {eur(100*equilibrio,0)} % en valle")
    for c, v in anual_fijo.items(): print(f"  {c} kWh/mes a precio fijo: {eur(v)} €/año (solo energía)")
