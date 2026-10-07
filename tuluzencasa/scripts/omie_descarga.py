"""Descarga los precios marginales del mercado diario de OMIE (marginalpdbc), un archivo por día.
Fuente: https://www.omie.es (Resultados de mercado). Guarda en fuentes/tanda8/omie/. Con pausa entre peticiones."""
import datetime as dt, pathlib, time, urllib.request, sys
D=pathlib.Path(__file__).resolve().parent.parent/'fuentes'/'tanda8'/'omie'; D.mkdir(parents=True,exist_ok=True)
ini=dt.date.fromisoformat(sys.argv[1]); fin=dt.date.fromisoformat(sys.argv[2])
d=ini
while d<=fin:
    f=D/f'marginalpdbc_{d:%Y%m%d}.1'
    if not f.exists():
        u=f'https://www.omie.es/es/file-download?parents=marginalpdbc&filename=marginalpdbc_{d:%Y%m%d}.1'
        for intento in range(3):
            try:
                b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 tuluzencasa-datos'}),timeout=60).read()
                if b.startswith(b'MARGINALPDBC'): f.write_bytes(b); break
            except Exception as e: time.sleep(3)
        time.sleep(0.4)
    d+=dt.timedelta(days=1)
print(len(list(D.glob('*.1'))),'archivos')
