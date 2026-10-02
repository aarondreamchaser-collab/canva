"""Constantes y utilidades compartidas por los cálculos de tuluzencasa.com.

Los valores son los mismos que usa la calculadora de la portada (fragmento de
WPCode «calculadora.js»). Si cambian allí, hay que cambiarlos aquí.
"""

# Impuestos
IVA = 0.21
IMPUESTO_ELECTRICO = 0.0511          # la calculadora usa 1,0511 (tipo legal: 5,11269632 %)
IMP = (1 + IVA) * (1 + IMPUESTO_ELECTRICO)   # factor que se aplica a energía y potencia

# Precios orientativos sin impuestos
PRECIO_UNICO = 0.13                  # €/kWh, precio fijo
PRECIO_PUNTA, PRECIO_LLANO, PRECIO_VALLE = 0.19, 0.12, 0.08   # €/kWh, discriminación horaria
POT_DIA = 0.09                       # €/kW y día, término de potencia
CONTADOR_MES = 0.81                  # €/mes, alquiler del contador (lleva IVA, no impuesto eléctrico)

MES = 30.4                           # días por mes
SEM = 4.345                          # semanas por mes
POTENCIAS = [2.3, 3.45, 4.6, 5.75, 6.9, 8.05, 9.2]   # kW normalizadas (monofásico, 230 V)
MARGEN = 1.10                        # margen que aplica la calculadora al recomendar potencia
TENSION = 230                        # V

# Reparto de cada franja de uso entre punta, llano y valle (igual que la calculadora)
FRANJAS = {
    'madrugada': dict(p=0, l=0, v=1),
    'manana': dict(p=4/6, l=2/6, v=0),
    'tarde': dict(p=0, l=1, v=0),
    'punta': dict(p=1, l=0, v=0),
    'noche': dict(p=0, l=1, v=0),
    'todo': dict(p=1/3, l=1/3, v=1/3),
}

# Aparatos del «ejemplo de un piso de 3 personas» de la portada:
# id: (nombre, W, horas/día, días/semana, franja, factor de uso real)
EJEMPLO = {
    'nev': ('Nevera combi', 150, 24, 7, 'todo', 0.2),
    'ter': ('Termo eléctrico 80 L', 1500, 3, 7, 'todo', 0.7),
    'ind': ('Placa de inducción (un fuego)', 1800, 1, 7, 'manana', 0.7),
    'hor': ('Horno eléctrico', 2200, 0.75, 4, 'punta', 0.6),
    'lav': ('Lavadora (lavado a 40 °C)', 800, 1, 4, 'manana', 1),
    'lvv': ('Lavavajillas (programa eco)', 1200, 1.5, 5, 'punta', 0.55),
    'tv': ('Televisión de 55 pulgadas', 100, 4, 7, 'punta', 1),
    'led': ('Iluminación LED (10 bombillas)', 90, 5, 7, 'punta', 1),
    'rou': ('Router wifi', 10, 24, 7, 'todo', 1),
    'sby': ('Aparatos en espera (standby)', 15, 24, 7, 'todo', 1),
}


def kwh_mes(w, h, d, r):
    return w / 1000 * h * r * d * SEM


def reparto(franja):
    """Fracción del consumo en punta, llano y valle (laborables 5/7, finde 2/7 en valle)."""
    f = FRANJAS[franja]
    wd, we = 5 / 7, 2 / 7
    return dict(p=wd * f['p'], l=wd * f['l'], v=we + wd * f['v'])


def eur(x, dec=2):
    """Formato español: 1.234,56"""
    s = f'{x:,.{dec}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def termino_potencia_mes(kw):
    return kw * POT_DIA * MES


def termino_potencia_anio(kw):
    return kw * POT_DIA * 365
