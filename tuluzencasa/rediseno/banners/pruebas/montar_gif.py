"""Monta los GIF a partir de los fotogramas grabados a cámara lenta (gif.mjs). Uso: python3 montar_gif.py DIR_FOTOGRAMAS DIR_SALIDA"""
import json, sys, pathlib
from PIL import Image
src=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
for d in sorted(p for p in src.iterdir() if p.is_dir()):
    meta=json.loads((d/'meta.json').read_text()); fr=sorted(d.glob('*.png'))
    paso=50 if d.name.startswith('5-') else 40
    sel=[];t=0
    while t<=meta[-1]:
        i=min(range(len(meta)),key=lambda k:abs(meta[k]-t)); sel.append(i); t+=paso
    ims=[]
    for i in sel:
        im=Image.open(fr[i]).convert('RGB')
        if im.width>900: im=im.resize((900,round(im.height*900/im.width)),Image.LANCZOS)
        ims.append(im)
    pal=ims[len(ims)//2].quantize(colors=128,method=Image.Quantize.MEDIANCUT)
    q=[im.quantize(palette=pal,dither=Image.Dither.NONE) for im in ims]
    dur=[paso]*len(q); dur[-1]=1200
    f=out/(d.name+'.gif'); q[0].save(f,save_all=True,append_images=q[1:],duration=dur,loop=0,optimize=True,disposal=1)
    print(f.name,len(q),'fotogramas',f.stat().st_size//1024,'KB')
