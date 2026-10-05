import re, json, html as H
D=json.load(open('datos.json')); P={p['id']:p for p in D['posts']}
CAT={c['id']:c for c in D['cats']}
R='/home/user/canva/tuluzencasa/rediseno/'
CSS=open(R+'wpcode-diseno.css').read()
PREV_CSS='''/* SOLO VISTA PREVIA: muestra dónde irán los anuncios (en la web real estos huecos no ocupan nada) */
.tl-hueco{display:block!important;min-height:90px;border:2px dashed #B3412F;border-radius:8px;background:repeating-linear-gradient(45deg,#fff,#fff 8px,#fbeeea 8px,#fbeeea 16px);position:relative}
.tl-hueco::after{content:"Hueco para anuncio (" attr(data-hueco) ") — vacío";position:absolute;inset:0;display:grid;place-items:center;font:600 13px system-ui;color:#B3412F}
/* SOLO VISTA PREVIA: aproximación del buscador de GeneratePress (lo pone el tema al activarlo) */
.navigation-search{position:absolute;left:-99999px;visibility:hidden;opacity:0;top:0;width:100%;z-index:20}
.navigation-search.nav-search-active{left:0;right:0;visibility:visible;opacity:1}
.navigation-search input[type=search]{width:100%;height:60px;border:0;background:#fff;box-shadow:0 2px 0 #18222E22;padding:0 20px}
.main-navigation .inside-navigation{position:relative}
.tl-banner{position:sticky;top:0;z-index:999;background:#B3412F;color:#fff;font:600 13px system-ui;text-align:center;padding:6px}'''
ARROW='<span role="presentation" class="dropdown-menu-toggle"><span class="gp-icon icon-arrow"><svg viewBox="0 0 330 512" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"><path d="M305.913 197.085c0 2.266-1.133 4.815-2.833 6.514L171.087 335.593c-1.7 1.7-4.249 2.832-6.515 2.832s-4.815-1.133-6.515-2.832L26.064 203.599c-1.7-1.7-2.832-4.248-2.832-6.514s1.132-4.816 2.832-6.515l14.162-14.163c1.7-1.699 3.966-2.832 6.515-2.832 2.266 0 4.815 1.133 6.515 2.832l111.316 111.317 111.316-111.317c1.7-1.699 4.249-2.832 6.515-2.832s4.815 1.133 6.515 2.832l14.162 14.163c1.7 1.7 2.833 4.249 2.833 6.515z" /></svg></span></span>'
W='https://tuluzencasa.com'
def li(id_,txt,url,cur=False): return f'<li id="menu-item-{id_}" class="menu-item menu-item-{id_}{" current-menu-item" if cur else ""}"><a href="{url}">{txt}</a></li>'
def lip(id_,txt,kids): return f'<li id="menu-item-{id_}" class="menu-item menu-item-type-custom menu-item-has-children menu-item-{id_}"><a href="#">{txt}{ARROW}</a>\n<ul class="sub-menu">'+''.join(kids)+'</ul>\n</li>'
MENU=('<ul id="menu-principal" class=" menu sf-menu">'+li(38,'Consumo de aparatos',W+'/consumo/')+li(132,'Factura y tarifas',W+'/factura-luz/')
 +li(78,'Calefacción y aire',W+'/climatizacion/')
 +lip(151,'Más temas',[li(152,'Ahorrar luz',W+'/ahorro/'),li(153,'Placas solares',W+'/placas-solares/'),li(154,'Coche eléctrico',W+'/coche-electrico/'),li(37,'Averías e instalación',W+'/instalacion/')])
 +lip(900,'Calculadoras',[li(901,'Calculadora de consumo eléctrico',W+'/calculadora-consumo-electrico/'),li(902,'Calculadora de potencia contratada',W+'/calculadora-potencia-contratada/')])
 +'</ul>')
LUPA='<span class="gp-icon icon-search"><svg viewBox="0 0 512 512" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"><path fill-rule="evenodd" clip-rule="evenodd" d="M208 48c-88.366 0-160 71.634-160 160s71.634 160 160 160 160-71.634 160-160S296.366 48 208 48zM0 208C0 93.125 93.125 0 208 0s208 93.125 208 208c0 48.741-16.765 93.566-44.843 129.024l133.826 134.018c9.366 9.379 9.355 24.575-.025 33.941-9.379 9.366-24.575 9.355-33.941-.025L337.238 370.987C301.747 399.167 256.839 416 208 416 93.125 416 0 322.875 0 208z" /></svg></span>'
BARRA=f'<div class="menu-bar-items"><span class="menu-bar-item search-item"><a aria-label="Abrir la barra de búsqueda" href="#" onclick="tlBusca(event)">{LUPA}</a></span></div>'
FORM=f'<form method="get" class="search-form navigation-search" action="{W}/"><input type="search" class="search-field" value="" name="s" title="Buscar" placeholder="Buscar en Tu luz en casa" /></form>'
JS='<script>function tlBusca(e){e.preventDefault();document.querySelectorAll(".navigation-search").forEach(f=>{f.classList.toggle("nav-search-active");if(f.classList.contains("nav-search-active"))f.querySelector("input").focus()})}</script>'

def cabecera(h):
    h=re.sub(r'<ul id="menu-principal".*?</ul>\n?</li>\n?.*?</ul>', MENU, h, count=1, flags=re.S)
    assert 'menu-item-900' in h and 'menu-item-32"' not in h
    # buscador de GeneratePress (navegación): icono en la barra y en el control móvil
    h=h.replace('<div id="primary-menu" class="main-nav">', FORM+'<div id="primary-menu" class="main-nav">',1)
    i=h.index('<div id="primary-menu" class="main-nav">'); j=h.index('</ul></div>',i)+len('</ul></div>')
    h=h[:j]+BARRA+h[j:]
    h=h.replace('<nav class="main-navigation mobile-menu-control-wrapper" id="mobile-menu-control-wrapper" aria-label="Cambiar a móvil">',
                '<nav class="main-navigation mobile-menu-control-wrapper" id="mobile-menu-control-wrapper" aria-label="Cambiar a móvil">'+BARRA,1)
    return h

def comun(h, quitar_calc_consumo=True, titulo=None):
    h=cabecera(h)
    # Simula el ajuste del Personalizador «Punto de corte del menú móvil» = 1024 px
    h=h.replace('@media (max-width:768px){.main-navigation .menu-toggle','@media (max-width:1024px){.main-navigation .menu-toggle',1)
    h=h.replace('@media (max-width:768px){.main-navigation .menu-bar-item:hover','@media (max-width:1024px){.main-navigation .menu-bar-item:hover',1)
    # Ambas calculadoras dejan de cargarse en todo el sitio
    h=re.sub(r'<script>/\* Calculadora de potencia contratada.*?\}\)\(\);</script>','',h,count=1,flags=re.S)
    if quitar_calc_consumo:
        h=re.sub(r'<script>/\* Calculadora de la home de tuluzencasa.*?\}\)\(\);</script>','',h,count=1,flags=re.S)
    assert 'Calculadora de potencia contratada de tuluzencasa' not in h, 'potencia sigue'
    h=h.replace('</head>','<style id="wpcode-diseno">'+CSS+'</style><style>'+PREV_CSS+'</style>'+JS+'</head>',1)
    h=re.sub(r'(<body[^>]*>)',r'\1<div class="tl-banner">VISTA PREVIA LOCAL — no es la web publicada</div>',h,count=1)
    if titulo: h=re.sub(r'<title>.*?</title>',f'<title>{titulo}</title>',h,count=1)
    return h

def contenido(h, nuevo):
    a=h.index('<div class="entry-content" itemprop="text">')+len('<div class="entry-content" itemprop="text">')
    b=h.index('\t\t</div>',a) if False else None
    # fin del entry-content: el </div> que precede al cierre del article
    m=re.search(r'\n\t\t</div>\n',h[a:]); b=a+m.start()
    return h[:a]+nuevo+h[b:]

# ---------- Portada ----------
def tarjeta(p):
    img=p['img']['sizes'].get('medium_large',p['img']['full']); c=CAT[p['cat'][0]]
    return (f'<li class="wp-block-post post-{p["id"]} post type-post status-publish"><figure style="aspect-ratio:16/9;" class="wp-block-post-featured-image"><a href="{W}/{p["slug"]}/" target="_self"  ><img width="768" height="432" src="{img}" class="attachment-medium_large size-medium_large wp-post-image" alt="" style="width:100%;height:100%;object-fit:cover;" loading="lazy" decoding="async" /></a></figure>'
            f'<div class="taxonomy-category wp-block-post-terms"><a href="{W}/{c["slug"]}/" rel="tag">{c["name"]}</a></div>'
            f'<h3 class="wp-block-post-title"><a href="{W}/{p["slug"]}/" target="_self" >{p["t"]}</a></h3></li>')
port=open(R+'portada.html').read()
ult=sorted([p for p in D['posts'] if p['st']=='publish'],key=lambda p:(p['d'],p['id']),reverse=True)[:6]
grid='<div class="wp-block-query tl-ultimos"><ul class="wp-block-post-template is-layout-grid wp-block-post-template-is-layout-grid">'+''.join(tarjeta(p) for p in ult)+'</ul></div>'
port=re.sub(r'<!-- wp:query .*?<!-- /wp:query -->',grid,port,flags=re.S)
port=port.replace('<!-- wp:shortcode -->\n[tl_categorias]\n<!-- /wp:shortcode -->',open('out_cats.html').read())
port=re.sub(r'<!-- /?wp:[^>]*-->','',port)
h=open('live_home.html').read()
h=comun(h,titulo='Tu luz en casa: consumo, factura y ahorro de luz (vista previa)')
h=contenido(h,port)
open('p_home.html','w').write(h)

# ---------- Página de la calculadora ----------
calc=open(R+'pagina-calculadora-consumo.html').read().replace('<!-- wp:html -->','').replace('<!-- /wp:html -->','')
h=open('live_home.html').read()
h=comun(h,quitar_calc_consumo=False,titulo='Calculadora de consumo eléctrico (vista previa)')
h=h.replace('<body class="home wp-singular page-template-default page page-id-23','<body class="wp-singular page-template-default page page-id-999',1)
h=contenido(h,calc)
open('p_calc.html','w').write(h)

# ---------- Artículo ----------
def articulo(src,pid,out):
    h=open(src).read(); p=P[pid]; c=CAT[p['cat'][0]]
    h=comun(h)
    bc=(f'<nav aria-label="breadcrumbs" class="rank-math-breadcrumb"><p><a href="{W}/">Inicio</a><span class="separator"> › </span>'
        f'<a href="{W}/{c["slug"]}/">{c["name"]}</a><span class="separator"> › </span><span class="last">{p["t"]}</span></p></nav>')
    i=h.index('<div class="featured-image'); h=h[:i]+bc+h[i:]
    m=re.search(r'<span class="posted-on">.*?</span> ',h,re.S)
    mod=re.search(r'<time class="updated" datetime="([^"]+)"[^>]*>([^<]+)</time>',m.group()) or re.search(r'<time class="entry-date published" datetime="([^"]+)"[^>]*>([^<]+)</time>',m.group())
    h=h.replace(m.group(),f'<span class="posted-on">Actualizado el <time class="entry-date updated-date" datetime="{mod.group(1)}" itemprop="dateModified">{mod.group(2)}</time></span> ',1)
    h=contenido(h,open(f'out_{pid}.html').read())
    h=re.sub(r'<nav id="nav-below".*?</nav>','',h,count=1,flags=re.S)
    h=h.replace(f'<a href="{W}/">Calculadora de consumo eléctrico por aparato</a>',f'<a href="{W}/calculadora-consumo-electrico/">Calculadora de consumo eléctrico</a>')
    open(out,'w').write(h)
articulo('live_art.html',134,'p_art.html')
articulo('live_art_old.html',20,'p_art_old.html')
print('ok')
