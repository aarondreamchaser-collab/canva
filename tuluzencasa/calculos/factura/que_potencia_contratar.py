"""Cifras del artículo «Qué potencia contratar».

- Coste del término de potencia de cada potencia normalizada (con impuesto eléctrico e IVA).
- Ahorro al bajar un escalón.
- Tres casos de aparatos encendidos a la vez, con el margen del 10 % de la calculadora.
Uso: python3 calculos/que_potencia_contratar.py
"""
import json, os
from comun import *

tabla = []
for kw in POTENCIAS:
    anio = termino_potencia_anio(kw) * IMP
    tabla.append(dict(kw=kw, amperios=round(kw * 1000 / TENSION), mes=termino_potencia_mes(kw) * IMP, anio=anio))

escalones = [dict(de=a['kw'], a=b['kw'], ahorro_anio=b['anio'] - a['anio']) for a, b in zip(tabla, tabla[1:])]
por_kw_anio = POT_DIA * 365 * IMP


def recomendar(w):
    need = w / 1000 * MARGEN
    return next((k for k in POTENCIAS if k >= need), None), need


CASOS = {
    'gas': ('Piso con cocina y calefacción de gas', [
        ('Lavadora calentando agua', 2000), ('Microondas', 1000), ('Nevera', 150),
        ('Televisión', 100), ('Iluminación LED', 90)]),
    'gas_sin_micro': ('El mismo piso sin el microondas a la vez', [
        ('Lavadora calentando agua', 2000), ('Nevera', 150),
        ('Televisión', 100), ('Iluminación LED', 90)]),
    'electrico': ('Piso con cocina eléctrica y termo', [
        ('Placa de inducción (un fuego)', 1800), ('Horno', 2200), ('Termo eléctrico', 1500),
        ('Nevera', 150), ('Televisión', 100), ('Iluminación LED', 90)]),
    'electrico_termo_noche': ('El mismo piso con el termo programado de madrugada', [
        ('Placa de inducción (un fuego)', 1800), ('Horno', 2200),
        ('Nevera', 150), ('Televisión', 100), ('Iluminación LED', 90)]),
}
casos = {}
for k, (n, ap) in CASOS.items():
    w = sum(x for _, x in ap)
    rec, need = recomendar(w)
    casos[k] = dict(nombre=n, aparatos=ap, w=w, kw=w / 1000, con_margen=need, recomendada=rec)

r = dict(tabla=tabla, escalon_kw=POTENCIAS[1] - POTENCIAS[0], escalones=escalones, por_kw_anio=por_kw_anio, casos=casos,
         ahorro_46_a_345=next(e for e in escalones if e['de'] == 3.45)['ahorro_anio'],
         ahorro_575_a_46=next(e for e in escalones if e['de'] == 4.6)['ahorro_anio'])

if __name__ == '__main__':
    json.dump(r, open(os.path.join(os.path.dirname(__file__), 'salida', 'que-potencia-contratar.json'), 'w'), indent=1)
    print('Potencia | A | €/mes | €/año (con impuestos)')
    for t in tabla:
        print(f"{eur(t['kw'])} kW | {t['amperios']} A | {eur(t['mes'])} | {eur(t['anio'])}")
    print(f"\nCada kW cuesta {eur(por_kw_anio)} € al año. Cada escalón de 1,15 kW: {eur(escalones[0]['ahorro_anio'])} €/año")
    for k, c in casos.items():
        print(f"\n{c['nombre']}: {eur(c['w']/1000)} kW a la vez -> x1,10 = {eur(c['con_margen'])} kW -> {eur(c['recomendada'])} kW")
