"""Minifica el fragmento (esbuild) y genera las páginas de prueba *_fx.html (fragmento al final de <head>)."""
import re, subprocess, pathlib
D=pathlib.Path(__file__).resolve().parent; R=D.parent
s=(R/'banners-tuluzencasa.html').read_text()
css=re.search(r'<style id="tlb-css">(.*?)</style>',s,re.S).group(1)
js=re.search(r'<script id="tlb-js">(.*?)</script>',s,re.S).group(1)
m=lambda src,ld: subprocess.run(['esbuild','--minify','--loader='+ld],input=src,capture_output=True,text=True,check=True).stdout.strip()
mini='<!-- Banners y efectos tuluzencasa · WPCode › Fragmento HTML › Cabecera de todo el sitio -->\n<style id="tlb-css">'+m(css,'css')+'</style>\n<script id="tlb-js">'+m(js,'js')+'</script>\n'
(R/'banners-tuluzencasa.min.html').write_text(mini)
for k in ['home','art','art2','calc','pot']:
    b=(D/f'{k}_base.html').read_text()
    (D/f'{k}_fx.html').write_text(b.replace('</head>',mini+'</head>',1))
import gzip
for f in ['banners-tuluzencasa.html','banners-tuluzencasa.min.html']:
    data=(R/f).read_bytes(); print(f,len(data),len(gzip.compress(data,9)))
