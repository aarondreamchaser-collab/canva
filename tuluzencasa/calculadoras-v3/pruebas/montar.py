import re,pathlib,sys
V3=pathlib.Path('/home/user/canva/tuluzencasa/calculadoras-v3')
def arreglar_efectos(h):
    # simula el arreglo del titular: cierra el script de Efectos antes del siguiente <script>
    i=h.index('<script id="tl-efectos-js">'); j=h.index('<script>',i); k=h.index('</script>',i)
    if j<k: h=h[:j]+'</script>\n'+h[j:]
    return h
h=arreglar_efectos(open('con_live.html').read())
a=h.index('<section class="tlc-app"'); q=h.index('<section class="tlc-sec">',a); b=h.index('</section>',q)+10
h=h[:a]+'<div id="tl3-consumo" class="tl3-sitio" aria-label="Calculadora de consumo eléctrico"><p class="tl3-sinjs">La calculadora necesita JavaScript.</p></div>'+h[b:]
h=h.replace('body:has(#tlc-app)','body:has(#tl3-consumo)')
h=h.replace('</body>','<script>'+(V3/'consumo3.min.js').read_text()+'</script></body>',1)
h=h.replace('</style>',(V3/'reserva.css').read_text()+'</style>',1)
open('con3.html','w').write(h)
print('ok',len(h))
h=arreglar_efectos(open('pot_live.html').read())
a=h.index('<section class="tlp-app"'); b=h.index('</section>',a)+10
# la sección contiene secciones anidadas? comprobar
assert h[a:b].count('<section')==1
h=h[:a]+'<div id="tl3-potencia" aria-label="Calculadora de potencia contratada"><p class="tl3-sinjs">La calculadora necesita JavaScript.</p></div>'+h[b:]
h=h.replace('</body>','<script>'+(V3/'potencia3.min.js').read_text()+'</script></body>',1)
h=h.replace('</style>',(V3/'reserva.css').read_text()+'</style>',1)
open('pot3.html','w').write(h); print('pot3 ok')
