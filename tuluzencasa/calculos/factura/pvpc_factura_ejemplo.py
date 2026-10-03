"""Factura mensual completa del piso de 3 personas con precio fijo y con precio por tramos.

Amplía «PVPC o mercado libre». Usa las mismas constantes que la calculadora (comun.py)
y el mismo consumo que pvpc_o_mercado_libre.py. El PVPC no se calcula: su precio cambia
cada hora y no hay un valor fijo que usar sin inventarlo.
Uso: python3 pvpc_factura_ejemplo.py
"""
import json, os
from comun import *
from pvpc_o_mercado_libre import energia, actual, movido

KW = 4.6


def factura(energia_sin_imp):
    pot = termino_potencia_mes(KW)
    base = pot + energia_sin_imp
    ie = base * IMPUESTO_ELECTRICO
    iva = (base + ie + CONTADOR_MES) * IVA
    return dict(potencia=pot, energia=energia_sin_imp, impuesto=ie, contador=CONTADOR_MES, iva=iva,
                total=base + ie + CONTADOR_MES + iva)


casos = {
    'fijo': factura(actual['fijo_mes'] / IMP),
    'tramos': factura(actual['tramos_mes'] / IMP),
    'tramos_movido': factura(movido['tramos_mes'] / IMP),
}
if __name__ == '__main__':
    json.dump(casos, open(os.path.join(os.path.dirname(__file__), 'salida', 'pvpc-factura-ejemplo.json'), 'w'), indent=1)
    print(f"Consumo {eur(actual['kwh'],1)} kWh/mes; potencia {eur(KW)} kW")
    for k, c in casos.items():
        print(k, {x: eur(y) for x, y in c.items()})
    # Diferencias entre los totales ya redondeados, para que cuadren con la tabla del artículo
    r2 = {k: round(c['total'], 2) for k, c in casos.items()}
    print("diferencia tramos - fijo (totales redondeados):", eur(r2['tramos'] - r2['fijo']))
    print("diferencia fijo - tramos movido (totales redondeados):", eur(r2['fijo'] - r2['tramos_movido']))
