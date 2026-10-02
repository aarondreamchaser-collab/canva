"""Cifras del artículo «Cómo leer la factura de la luz».

Factura de ejemplo: el piso de 3 personas de la calculadora de la portada,
4,6 kW contratados, un mes de 30,4 días, con precio único y con discriminación horaria.
Uso: python3 calculos/como_leer_la_factura.py  (escribe calculos/salida/como-leer-la-factura-de-la-luz.json)
"""
import json, os
from comun import *

KW = 4.6

kwh = {k: kwh_mes(w, h, d, r) for k, (n, w, h, d, f, r) in EJEMPLO.items()}
total_kwh = sum(kwh.values())
p = sum(kwh[k] * reparto(EJEMPLO[k][4])['p'] for k in kwh)
l = sum(kwh[k] * reparto(EJEMPLO[k][4])['l'] for k in kwh)
v = sum(kwh[k] * reparto(EJEMPLO[k][4])['v'] for k in kwh)


def factura(energia):
    pot = termino_potencia_mes(KW)
    base_ie = pot + energia
    ie = base_ie * IMPUESTO_ELECTRICO
    cont = CONTADOR_MES
    base_iva = base_ie + ie + cont
    iva = base_iva * IVA
    return dict(potencia=pot, energia=energia, impuesto_electrico=ie, contador=cont,
                base_iva=base_iva, iva=iva, total=base_iva + iva)


unico = factura(total_kwh * PRECIO_UNICO)
tramos = factura(p * PRECIO_PUNTA + l * PRECIO_LLANO + v * PRECIO_VALLE)

r = dict(
    kw=KW, dias=MES, kwh_total=total_kwh, kwh_punta=p, kwh_llano=l, kwh_valle=v,
    pct_punta=p / total_kwh, pct_llano=l / total_kwh, pct_valle=v / total_kwh,
    factura_unico=unico, factura_tramos=tramos,
    peso_potencia_unico=(unico['potencia'] * (1 + IMPUESTO_ELECTRICO) * (1 + IVA)) / unico['total'],
    potencia_dia=POT_DIA, potencia_mes_sin_imp=termino_potencia_mes(KW),
    precio_unico_con_imp=PRECIO_UNICO * IMP,
)

if __name__ == '__main__':
    os.makedirs(os.path.join(os.path.dirname(__file__), 'salida'), exist_ok=True)
    json.dump(r, open(os.path.join(os.path.dirname(__file__), 'salida', 'como-leer-la-factura-de-la-luz.json'), 'w'), indent=1)
    print(f"Consumo: {eur(total_kwh,1)} kWh/mes  (punta {eur(p,1)} · llano {eur(l,1)} · valle {eur(v,1)})")
    print(f"Reparto: punta {eur(100*p/total_kwh,0)} % · llano {eur(100*l/total_kwh,0)} % · valle {eur(100*v/total_kwh,0)} %")
    for nombre, f in (('Precio único', unico), ('Por tramos', tramos)):
        print(f"\n{nombre}")
        print(f"  Potencia {KW} kW x {MES} días x {POT_DIA} €/kW día = {eur(f['potencia'])} €")
        print(f"  Energía                                  = {eur(f['energia'])} €")
        print(f"  Impuesto eléctrico 5,11 %                = {eur(f['impuesto_electrico'])} €")
        print(f"  Alquiler del contador                    = {eur(f['contador'])} €")
        print(f"  Base del IVA                             = {eur(f['base_iva'])} €")
        print(f"  IVA 21 %                                 = {eur(f['iva'])} €")
        print(f"  TOTAL                                    = {eur(f['total'])} €")
    print(f"\nPeso de la potencia (con impuestos) en la factura de precio único: {eur(100*r['peso_potencia_unico'],0)} %")
