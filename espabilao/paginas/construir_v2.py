import json, re
I = {
 'escudo':'<path d="M12 3.5 19 6v5.6c0 4.3-2.9 7.6-7 8.9-4.1-1.3-7-4.6-7-8.9V6z"/><path d="m8.8 12 2.2 2.2 4.3-4.4"/>',
 'libro':'<path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5z"/><path d="M20 5.5A1.5 1.5 0 0 0 18.5 4H13v16h5.5a1.5 1.5 0 0 0 1.5-1.5z"/>',
 'reloj':'<circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3 2"/>',
 'no':'<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
 'si':'<path d="m5 12.5 4.5 4.5L19 7.5"/>',
 'carta':'<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/>',
 'lupa':'<path d="M6 3.5h7l4 4V11"/><path d="M13 3.5v4h4"/><path d="M6 3.5v16h5"/><circle cx="16" cy="16" r="3.2"/><path d="m18.4 18.4 2.3 2.3"/>',
 'balanza':'<path d="M12 4v16M7 20h10"/><path d="M5 7h14"/><path d="M5 7l-2.5 6a2.8 2.8 0 0 0 5 0z"/><path d="M19 7l-2.5 6a2.8 2.8 0 0 0 5 0z"/>',
 'galleta':'<path d="M20.5 12.5A8.5 8.5 0 1 1 11.5 3.5a3 3 0 0 0 4 3.5 3 3 0 0 0 5 5.5z"/><path d="M8.5 9.5h.01M12 15h.01M8 14h.01M15.5 13h.01"/>',
 'candado':'<rect x="5" y="10.5" width="14" height="10" rx="2.2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><path d="M12 14.5v2.5"/>',
 'usuario':'<circle cx="12" cy="8" r="3.6"/><path d="M5 20c.8-3.8 3.6-6 7-6s6.2 2.2 7 6"/>',
 'alerta':'<path d="M12 4 21 19.5H3z"/><path d="M12 10v4.2M12 17h.01"/>',
 'chispa':'<path d="M12 3.5 13.8 10.2 20.5 12 13.8 13.8 12 20.5 10.2 13.8 3.5 12 10.2 10.2z"/>',
 'escalera':'<path d="M4 19.5h5v-5h5v-5h6"/><path d="M17 6.5 20 9.5 17 12.5"/>',
 'bombilla':'<path d="M9 17.5h6M9.8 20.5h4.4"/><path d="M12 3.5a5.5 5.5 0 0 0-3.3 9.9c.7.5 1.1 1.3 1.1 2.1v.5h4.4v-.5c0-.8.4-1.6 1.1-2.1A5.5 5.5 0 0 0 12 3.5z"/>',
 'calendario':'<rect x="3.5" y="5" width="17" height="15.5" rx="2.2"/><path d="M3.5 9.8h17M8 3v4M16 3v4"/>',
 'copiar':'<rect x="8.5" y="8.5" width="11" height="11" rx="2"/><path d="M15.5 8.5V6a1.5 1.5 0 0 0-1.5-1.5H6A1.5 1.5 0 0 0 4.5 6v8A1.5 1.5 0 0 0 6 15.5h2.5"/>',
 'euro':'<path d="M17.5 6.5A6.5 6.5 0 1 0 17.5 17.5"/><path d="M4.5 10.5h8M4.5 13.5h8"/>',
 'flecha':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'navegador':'<rect x="3" y="4.5" width="18" height="15" rx="2.2"/><path d="M3 9h18M6.5 6.8h.01M9 6.8h.01"/>',
 'gavel':'<path d="m14.5 4.5 5 5M12 7l5 5M9.5 9.5l5 5-2 2-5-5zM7.5 13.5l-4 4 2 2 4-4"/>',
}
def ic(n,t=24): return '<svg class="pg-ic" width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'%(t,t,I[n])
MAIL='<a href="mailto:[EMAIL]">[EMAIL]</a>'

CSS = r"""
<style id="pg-estilos">
/* Espabilao · páginas institucionales */
body:has(.pg) .articulo__cabecera--simple{display:none}
.pg{--pg-ancho:min(1120px,calc(100vw - 36px));width:var(--pg-ancho);margin-left:calc(50% - var(--pg-ancho)/2);font-size:1.05rem;line-height:1.65}
.pg *{box-sizing:border-box}
.pg-hero{position:relative;overflow:hidden;border-radius:28px;background:radial-gradient(520px 300px at 92% 0,rgba(255,106,43,.28),transparent 65%),radial-gradient(420px 260px at 0 100%,rgba(90,62,194,.12),transparent 60%),#fff3ea;padding:34px 22px 30px;margin:8px 0 34px}
.pg-hero__marca{position:absolute;right:-10px;bottom:-34px;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:clamp(6rem,24vw,15rem);line-height:.8;letter-spacing:-.06em;color:transparent;-webkit-text-stroke:2px rgba(26,26,31,.12);pointer-events:none;user-select:none;white-space:nowrap}
.pg-supra{display:inline-flex;align-items:center;gap:8px;font-size:.78rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#bf3f0a;margin:0 0 14px}
.pg-hero h1{position:relative;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:clamp(2.4rem,9vw,4.6rem);line-height:.98;letter-spacing:-.045em;color:#1a1a1f;margin:0 0 18px;max-width:16ch}
.pg-hero h1 em{font-style:normal;background-image:linear-gradient(#ff6a2b,#ff6a2b);background-repeat:no-repeat;background-size:100% 100%;padding:0 .12em;border-radius:.16em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.pg-hero__lead{position:relative;font-size:1.18rem;line-height:1.5;color:#2a2a30;max-width:58ch;margin:0 0 20px}
.pg-chips{position:relative;display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}
.pg-chips li{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid #e8e3dc;border-radius:999px;padding:6px 12px;font-size:.85rem;font-weight:600;color:#2a2a30}
.pg-chips .pg-ic{width:16px;height:16px;color:#bf3f0a}
.pg-rejilla{display:grid;gap:30px}
.pg-indice{display:none}
.pg-indice p{font-size:.78rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#5f5d66;margin:0 0 10px}
.pg-indice ol{list-style:none;margin:0;padding:0 0 0 14px;border-left:2px solid #e8e3dc;counter-reset:pgi}
.pg-indice li{counter-increment:pgi;margin:0}
.pg-indice a{display:block;padding:6px 0;text-decoration:none;color:#5f5d66;font-weight:600;font-size:.94rem}
.pg-indice a::before{content:counter(pgi,decimal-leading-zero) "  ";font-family:"Bricolage Grotesque",sans-serif;color:#bf3f0a;font-weight:800}
.pg-indice a:hover,.pg-indice a.is-activo{color:#1a1a1f}
.pg-resumen{position:relative;background:#1a1a1f;color:#e9e7e3;border-radius:22px;padding:22px 22px 18px;margin:0 0 30px;overflow:hidden}
.pg-resumen::after{content:"";position:absolute;right:-50px;top:-50px;width:160px;height:160px;border-radius:50%;background:rgba(255,106,43,.25)}
.pg-resumen h2{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:.82rem!important;letter-spacing:.1em;text-transform:uppercase;color:#ff6a2b!important;margin:0 0 12px!important;border:0!important;padding:0!important}
.pg-resumen ul{position:relative;z-index:1;list-style:none;margin:0;padding:0;display:grid;gap:10px}
.pg-resumen li{display:flex;gap:10px;align-items:flex-start;color:#fff;font-weight:500}
.pg-resumen li .pg-ic{flex:none;width:22px;height:22px;color:#ff6a2b;margin-top:1px}
.pg-bloque{position:relative;padding:26px 0 8px;border-top:1px solid #e8e3dc;scroll-margin-top:100px}
.pg-bloque:first-of-type{border-top:0}
.pg-num{display:block;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:3.4rem;line-height:.9;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:2px #1a1a1f;margin-bottom:6px}
.pg-bloque h2{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:clamp(1.55rem,4.8vw,2rem);letter-spacing:-.03em;line-height:1.1;color:#1a1a1f;margin:0 0 14px;border:0;padding:0}
.pg-bloque h3{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:1.2rem;color:#1a1a1f;margin:22px 0 8px}
.pg-bloque p{margin:0 0 14px}
.pg-bloque a{color:#bf3f0a;font-weight:600}
.pg-datos{display:grid;grid-template-columns:1fr;gap:10px;margin:6px 0 14px;padding:0}
.pg-datos div{background:#fff;border:1px solid #e8e3dc;border-radius:16px;padding:12px 16px}
.pg-datos dt{font-size:.74rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#5f5d66}
.pg-datos dd{margin:4px 0 0;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:1.15rem;color:#1a1a1f;overflow-wrap:anywhere}
.pg-datos dd a{color:#1a1a1f}
.pg-tarjetas{display:grid;gap:12px;margin:8px 0 16px;padding:0;list-style:none}
.pg-tarjeta{position:relative;display:flex;gap:14px;align-items:flex-start;background:#fff;border:1px solid #e8e3dc;border-radius:18px;padding:16px 18px;transition:transform .2s,box-shadow .2s,border-color .2s}
.pg-tarjeta:hover{transform:translateY(-2px);border-color:#ff6a2b;box-shadow:0 8px 28px rgba(26,26,31,.08)}
.pg-tarjeta__ic{flex:none;display:grid;place-items:center;width:46px;height:46px;border-radius:14px;background:#fff3ea;color:#bf3f0a}
.pg-tarjeta strong{display:block;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:1.08rem;color:#1a1a1f;margin-bottom:2px}
.pg-tarjeta span{color:#5f5d66;font-size:.96rem}
.pg-tarjeta--no .pg-tarjeta__ic{background:#fde3df;color:#b42318}
.pg-tarjeta--si .pg-tarjeta__ic{background:#ddf3e6;color:#0f6b3d}
.pg-tarjeta--lila .pg-tarjeta__ic{background:#efeafd;color:#5a3ec2}
.pg-tarjeta--menta .pg-tarjeta__ic{background:#e2f5ec;color:#126b45}
.pg-tarjeta--amarillo .pg-tarjeta__ic{background:#fff3c9;color:#7c5600}
.pg-cifras{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:0 0 30px}
.pg-cifra{background:#fff;border:1px solid #e8e3dc;border-radius:18px;padding:16px}
.pg-cifra b{display:block;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:2.3rem;line-height:1;letter-spacing:-.04em;color:#1a1a1f}
.pg-cifra span{font-size:.88rem;font-weight:600;color:#5f5d66}
.pg-cifra--naranja{background:#ff6a2b;border-color:#ff6a2b}
.pg-cifra--naranja b,.pg-cifra--naranja span{color:#1a1a1f}
.pg-cita{font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:clamp(1.5rem,5vw,2.2rem);line-height:1.12;letter-spacing:-.03em;color:#1a1a1f;border-left:6px solid #ff6a2b;padding:4px 0 4px 18px;margin:8px 0 22px}
.pg-sello{display:inline-block;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:1.05rem;letter-spacing:.08em;text-transform:uppercase;color:#b42318;border:3px solid currentColor;border-radius:10px;padding:6px 14px;transform:rotate(-6deg);margin:4px 0 14px}
.pg-sello--si{color:#0f6b3d}
.pg-aviso{display:flex;gap:12px;align-items:flex-start;background:#fff3c9;color:#4d3600;border-radius:16px;padding:14px 16px;margin:6px 0 16px;font-size:.96rem}
.pg-aviso .pg-ic{flex:none;color:#7c5600;margin-top:2px}
.pg-pasos{list-style:none;margin:6px 0 16px;padding:0;display:grid;gap:10px;counter-reset:pgp}
.pg-pasos li{counter-increment:pgp;position:relative;background:#f6f4f1;border-radius:16px;padding:14px 16px 14px 62px}
.pg-pasos li::before{content:counter(pgp);position:absolute;left:14px;top:12px;display:grid;place-items:center;width:34px;height:34px;border-radius:10px;background:#ff6a2b;color:#1a1a1f;font-family:"Bricolage Grotesque",sans-serif;font-weight:800}
.pg-pasos strong{color:#1a1a1f}
.pg-tabla{width:100%;border-collapse:separate;border-spacing:0;margin:8px 0 18px;font-size:.93rem;border:1px solid #e8e3dc;border-radius:16px;overflow:hidden}
.pg-tabla th,.pg-tabla td{padding:11px 12px;text-align:left;vertical-align:top;border-bottom:1px solid #e8e3dc}
.pg-tabla th{background:#f6f4f1;font-size:.74rem;letter-spacing:.07em;text-transform:uppercase;color:#5f5d66}
.pg-tabla tr:last-child td{border-bottom:0}
.pg-tabla code{background:#f6f4f1;border-radius:6px;padding:1px 5px;font-size:.86em}
.pg-tabla-envoltorio{overflow-x:auto}
.pg-etq{display:inline-block;border-radius:999px;padding:2px 9px;font-size:.75rem;font-weight:700}
.pg-etq--si{background:#ddf3e6;color:#0f6b3d}.pg-etq--no{background:#fff3c9;color:#7c5600}
.pg-correo{position:relative;overflow:hidden;background:#1a1a1f;color:#fff;border-radius:26px;padding:28px 22px;margin:0 0 30px}
.pg-correo::before{content:"@";position:absolute;right:-6px;top:-40px;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:13rem;line-height:1;color:transparent;-webkit-text-stroke:2px rgba(255,106,43,.35)}
.pg-correo p{position:relative;color:#cfccc6;margin:0 0 10px}
.pg-correo a.pg-correo__dir{position:relative;display:inline-block;font-family:"Bricolage Grotesque",sans-serif;font-weight:800;font-size:clamp(1.5rem,6vw,2.6rem);letter-spacing:-.03em;color:#fff;text-decoration:none;border-bottom:4px solid #ff6a2b;margin:4px 0 18px;overflow-wrap:anywhere}
.pg-botones{position:relative;display:flex;flex-wrap:wrap;gap:10px}
.pg-boton{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:12px 18px;font:700 1rem "Figtree",sans-serif;text-decoration:none;cursor:pointer;border:0}
.pg-boton--naranja{background:#ff6a2b;color:#1a1a1f!important}
.pg-boton--borde{background:transparent;color:#fff!important;border:1.5px solid #5a5a63}
.pg-boton.is-ok{background:#0f6b3d;color:#fff!important}
.pg-final{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;background:#f6f4f1;border-radius:20px;padding:18px 20px;margin:26px 0 10px;font-size:.92rem;color:#5f5d66}
.pg-final a{color:#1a1a1f;font-weight:700}
@media (min-width:700px){
 .pg-hero{padding:56px 52px 50px;margin-top:14px}
 .pg-datos{grid-template-columns:repeat(2,1fr)}
 .pg-tarjetas--dos{grid-template-columns:repeat(2,1fr)}
 .pg-cifras{grid-template-columns:repeat(4,1fr)}
 .pg-correo{padding:42px 40px}
}
@media (min-width:1000px){
 .pg-rejilla{grid-template-columns:230px minmax(0,1fr);gap:60px;align-items:start}
 .pg-indice{display:block;position:sticky;top:100px}
 .pg-cuerpo{max-width:760px}
}
/* Efectos (respetan «reducir movimiento») */
@media (prefers-reduced-motion:no-preference){
 .pg-js .pg-hero h1 em{animation:pg-pintar 1s cubic-bezier(.6,.1,.2,1) .3s both}
 .pg-js .pg-hero__marca{animation:pg-deriva 14s ease-in-out infinite alternate}
 .pg-js .pg-anim{opacity:0;transform:translateY(26px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1);transition-delay:var(--pg-d,0ms)}
 .pg-js .pg-anim.is-v{opacity:1;transform:none}
 .pg-js .pg-num{background:linear-gradient(90deg,#ff6a2b 50%,transparent 50%) right/200% 100% no-repeat;-webkit-background-clip:text;background-clip:text;transition:background-position 1.1s cubic-bezier(.6,.1,.2,1) .15s}
 .pg-js .pg-bloque.is-v .pg-num{background-position:left}
 .pg-js .pg-sello{opacity:0}
 .pg-js .is-v .pg-sello,.pg-js .pg-sello.is-v{animation:pg-sello .6s cubic-bezier(.3,1.4,.5,1) .2s both}
}
@keyframes pg-pintar{from{background-size:0 100%}to{background-size:100% 100%}}
@keyframes pg-deriva{from{transform:translateX(0)}to{transform:translateX(-60px)}}
@keyframes pg-sello{0%{opacity:0;transform:scale(1.9) rotate(-14deg)}60%{opacity:1;transform:scale(.94) rotate(-4deg)}100%{opacity:1;transform:rotate(-6deg)}}
@media print{.pg-indice,.pg-hero__marca{display:none}.pg{width:auto;margin:0}}
</style>
"""
JS = r"""
<script id="pg-script">
(function(){var d=document,raiz=d.querySelector('.pg');if(!raiz)return;var reducir=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!reducir&&'IntersectionObserver' in window){d.documentElement.classList.add('pg-js');var els=raiz.querySelectorAll('.pg-bloque,.pg-tarjeta,.pg-cifra,.pg-resumen,.pg-datos>div,.pg-pasos>li,.pg-correo,.pg-final,.pg-sello');
var alto=window.innerHeight;Array.prototype.forEach.call(els,function(el){var h=el.parentNode?Array.prototype.indexOf.call(el.parentNode.children,el):0;el.style.setProperty('--pg-d',(h%5)*70+'ms');if(el.getBoundingClientRect().top>alto*.9||el.classList.contains('pg-bloque')){el.classList.add('pg-anim');}});
var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-v');o.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:.1});Array.prototype.forEach.call(els,function(el){o.observe(el);});}
var enl=raiz.querySelectorAll('.pg-indice a');if(enl.length&&'IntersectionObserver' in window){var o2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){Array.prototype.forEach.call(enl,function(a){a.classList.toggle('is-activo',a.getAttribute('href')==='#'+e.target.id);});}});},{rootMargin:'-30% 0px -60% 0px'});Array.prototype.forEach.call(raiz.querySelectorAll('.pg-bloque[id]'),function(s){o2.observe(s);});}
Array.prototype.forEach.call(raiz.querySelectorAll('[data-pg-copiar]'),function(b){b.addEventListener('click',function(){var t=b.getAttribute('data-pg-copiar'),et=b.querySelector('span');var ok=function(){et.textContent='¡Copiado!';b.classList.add('is-ok');setTimeout(function(){et.textContent='Copiar dirección';b.classList.remove('is-ok');},2000);};if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(ok);}else{window.prompt('Copia la dirección:',t);}});});
})();
</script>
"""

def html_block(h): return "<!-- wp:html -->\n%s\n<!-- /wp:html -->\n\n" % h.strip()

def pagina(slug, supra_ic, supra, titulo_html, lead, chips, marca, resumen, bloques, final=True):
    indice = ''.join('<li><a href="#%s">%s</a></li>' % (b[0], b[1]) for b in bloques)
    cuerpo = ''
    for n,(bid, bt, bhtml) in enumerate(bloques, 1):
        cuerpo += '<section class="pg-bloque" id="%s"><span class="pg-num" aria-hidden="true">%02d</span><h2>%s</h2>%s</section>' % (bid, n, bt, bhtml)
    res = ''
    if resumen:
        res = '<aside class="pg-resumen" aria-label="En pocas palabras"><h2>En 20 segundos</h2><ul>%s</ul></aside>' % ''.join('<li>%s<span>%s</span></li>' % (ic(i,22), t) for i,t in resumen)
    fin = ''
    if final:
        fin = '<div class="pg-final"><span>¿Dudas o algo que corregir? Escríbenos a %s</span><span><a href="/aviso-legal/">Aviso legal</a> · <a href="/politica-de-privacidad/">Privacidad</a> · <a href="/politica-de-cookies/">Cookies</a></span></div>' % MAIL
    h = '<div class="pg pg--%s">' % slug
    h += '<header class="pg-hero"><span class="pg-hero__marca" aria-hidden="true">%s</span><p class="pg-supra">%s %s</p><h1>%s</h1><p class="pg-hero__lead">%s</p><ul class="pg-chips">%s</ul></header>' % (marca, ic(supra_ic,18), supra, titulo_html, lead, ''.join('<li>%s %s</li>' % (ic(i,16), t) for i,t in chips))
    h += '<div class="pg-rejilla"><nav class="pg-indice" aria-label="En esta página"><p>En esta página</p><ol>%s</ol></nav><div class="pg-cuerpo">%s%s%s</div></div></div>' % (indice, res, cuerpo, fin)
    return html_block(CSS) + html_block(h) + html_block(JS)

def tarjetas(items, clase='pg-tarjetas pg-tarjetas--dos'):
    return '<ul class="%s">%s</ul>' % (clase, ''.join('<li class="pg-tarjeta %s"><span class="pg-tarjeta__ic">%s</span><div><strong>%s</strong><span>%s</span></div></li>' % (mod, ic(i), t, d) for i,t,d,mod in items))
def datos(pares): return '<dl class="pg-datos">%s</dl>' % ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % p for p in pares)
def ul(items): return '<ul>%s</ul>' % ''.join('<li>%s</li>' % i for i in items)
def pasos(items): return '<ol class="pg-pasos">%s</ol>' % ''.join('<li>%s</li>' % i for i in items)
def aviso(t): return '<p class="pg-aviso">%s<span>%s</span></p>' % (ic('alerta',20), t)
TIT = [('Titular','[NOMBRE]'),('NIF','[NIF]'),('Domicilio','[CIUDAD] (España)'),('Correo electrónico',MAIL)]
ACT = ('calendario','Actualizado: [FECHA]')

P = {}
P['sobre-nosotros'] = ('Sobre nosotros', pagina('sobre-nosotros','chispa','Sobre nosotros','Que no te la cuelen <em>con tu seguro.</em>',
 'Espabilao explica qué cubren de verdad las pólizas, cuenta casos reales con su desenlace y te da herramientas para reclamar cuando la aseguradora dice que no.',
 [('escudo','Independientes'),('libro','Fuentes oficiales'),('no','Sin formularios')], '¡!',
 [('si','Información sobre seguros en España, clara y con fuentes.'),('no','No vendemos seguros ni cobramos de aseguradoras.'),('euro','Nos financiamos con publicidad, siempre señalada.')],
 [('quien','Quién hay detrás', '<p class="pg-cita">Una web hecha para estar de tu lado cuando llega el siniestro.</p><p>Espabilao es un proyecto de [NOMBRE], con sede en [CIUDAD]. [Añade aquí unas líneas sobre ti: tu experiencia con seguros, por qué empezaste la web y qué te mueve.]</p>'),
  ('que-hacemos','Qué hacemos', tarjetas([('escudo','¿Pagó o no pagó?','Casos reales de siniestros con veredicto: pagó, no pagó o a medias.',''),('lupa','Pólizas al desnudo','Las condiciones de cada aseguradora, en lenguaje claro.','pg-tarjeta--lila'),('escalera','Qué hacer si…','Guías paso a paso, con plazos legales y cartas.','pg-tarjeta--menta'),('bombilla','Trucos de espabilao','Consejos rápidos que ahorran disgustos.','pg-tarjeta--amarillo')])+'<p>Y además, <a href="/herramientas/">herramientas gratuitas</a>: calculadora de plazos, generador de cartas, detector de letra pequeña y calculadora de infraseguro. Funcionan en tu navegador y no guardan nada.</p>'),
  ('no-hacemos','Lo que no hacemos', '<span class="pg-sello">Prohibido</span>'+tarjetas([('no','No vendemos seguros','No somos aseguradora, corredor ni agente: no somos mediador de seguros.','pg-tarjeta--no'),('no','No cobramos de aseguradoras','Ni comisiones, ni pagos por aparecer, ni por recomendar.','pg-tarjeta--no'),('no','No pedimos tus datos','Ni presupuestos, ni formularios, ni llamadas.','pg-tarjeta--no'),('no','No asesoramos casos concretos','No revisamos pólizas ni gestionamos reclamaciones en tu nombre.','pg-tarjeta--no')])),
  ('financiacion','Cómo nos financiamos', '<div class="pg-cifras"><div class="pg-cifra pg-cifra--naranja"><b>0 €</b><span>de aseguradoras</span></div><div class="pg-cifra"><b>0</b><span>formularios</span></div><div class="pg-cifra"><b>4</b><span>herramientas gratis</span></div><div class="pg-cifra"><b>BOE</b><span>como fuente</span></div></div><p>La web se mantiene con publicidad de Google AdSense, siempre señalada como «Publicidad». Los anuncios los selecciona Google de forma automática: que aparezca el anuncio de una aseguradora no significa que la recomendemos, y los anunciantes no influyen en lo que publicamos. Lee cómo trabajamos en nuestra <a href="/politica-editorial/">política editorial</a>.</p>'),
  ('hablemos','Habla con nosotros', '<p>¿Has detectado un error, quieres proponernos un caso o tienes una duda sobre la web? Escríbenos a %s o visita la página de <a href="/contacto/">contacto</a>.</p>' % MAIL)]))

P['politica-editorial'] = ('Política editorial', pagina('politica-editorial','balanza','Política editorial','Cómo trabajamos para que <em>puedas fiarte.</em>',
 'Las reglas que seguimos para elegir fuentes, contar casos, revisar cada artículo y mantenernos lejos del dinero de las aseguradoras.',
 [('escudo','Independencia'),('libro','Fuentes primarias'),('reloj','Revisión con fecha')], 'BOE',
 [('escudo','No vendemos seguros ni cobramos de aseguradoras, corredores ni comparadores.'),('libro','Citamos fuentes oficiales: BOE, DGSFP y las propias pólizas.'),('reloj','Cada artículo dice quién lo escribe y cuándo se revisó.')],
 [('independencia','Independencia', tarjetas([('no','No somos mediador','Ni aseguradora, ni corredor, ni agente, ni banca-seguros.','pg-tarjeta--no'),('no','No cobramos de aseguradoras','Ni comisiones, ni artículos patrocinados, ni pagos por aparecer o recomendar.','pg-tarjeta--no'),('no','Sin afiliación','No usamos enlaces de afiliación hacia productos de seguros.','pg-tarjeta--no'),('euro','Publicidad separada','AdSense, siempre marcado como «Publicidad». Lo elige Google y no influye en el contenido.','')])+'<p>Si un anuncio de una aseguradora aparece junto a un artículo crítico con ella, es pura casualidad del sistema de anuncios.</p>'),
  ('fuentes','Cómo elegimos las fuentes', '<p>Priorizamos siempre fuentes primarias y oficiales, y las enlazamos al final de cada artículo:</p>'+tarjetas([('balanza','Legislación en el BOE','Texto consolidado: Ley de Contrato de Seguro, Ley 44/2002, Ley 10/2025, Ley de Enjuiciamiento Civil…',''),('escudo','DGSFP','Criterios de su Servicio de Reclamaciones, guías y memorias anuales.','pg-tarjeta--lila'),('lupa','Las propias pólizas','Condiciones generales, particulares y especiales: producto, edición y apartado. Las cláusulas, literales.','pg-tarjeta--menta'),('gavel','Resoluciones judiciales','Sentencias publicadas por el CENDOJ cuando ayudan a entender una norma.','pg-tarjeta--amarillo')])+aviso('No usamos como fuente única foros, opiniones sin respaldo ni notas de prensa comerciales.')),
  ('casos','Cómo contamos los casos', '<span class="pg-sello pg-sello--si">Verificado</span>'+pasos(['<strong>Solo con documentación.</strong> Publicamos casos de los que hemos visto documentación suficiente: respuestas de la compañía, peritajes o cartas.','<strong>Sin datos personales.</strong> Eliminamos o cambiamos cualquier dato que permita identificar a las personas.','<strong>Veredicto honesto.</strong> «Pagó», «No pagó» o «A medias» describe lo que ocurrió en ese caso, no lo que pasará en el tuyo.','<strong>Las tres versiones.</strong> Qué decía la póliza, qué alegó la aseguradora y cómo terminó.'])),
  ('revision','Cómo revisamos', pasos(['Cada artículo indica quién lo ha escrito y su <strong>fecha de revisión</strong>: el último día en que comprobamos que seguía vigente.','Revisamos cuando cambia la normativa y, de forma periódica, los contenidos más consultados.','Los plazos y artículos legales se comprueban contra el <strong>texto consolidado del BOE</strong>.','Las plantillas de cartas son modelos orientativos: te decimos qué adaptar a tu caso.'])),
  ('errores','Errores y correcciones', '<p>Si encuentras un error, escríbenos a %s indicando el artículo y, si puedes, la fuente correcta. Lo revisaremos y, si procede, corregiremos el contenido y actualizaremos su fecha de revisión.</p>' % MAIL),
  ('limites','Lo que no somos', aviso('Espabilao ofrece información general. No es asesoramiento jurídico ni financiero personalizado. Si tu caso es complejo o hay mucho dinero en juego, consulta con un profesional o con una asociación de consumidores.'))]))

P['contacto'] = ('Contacto', pagina('contacto','carta','Contacto','Escríbenos. <em>Te leemos.</em>',
 'La forma de hablar con Espabilao es el correo electrónico. Sin formularios y sin teléfono: así no pedimos más datos de los necesarios.',
 [('carta','Solo por correo'),('no','Sin formularios'),('escudo','Tus datos, solo para responderte')], '@',
 None,
 [('correo','Nuestro correo', '<div class="pg-correo"><p>Escríbenos a</p><a class="pg-correo__dir" href="mailto:[EMAIL]">[EMAIL]</a><div class="pg-botones"><a class="pg-boton pg-boton--naranja" href="mailto:[EMAIL]">%s Escribir un correo</a><button type="button" class="pg-boton pg-boton--borde" data-pg-copiar="[EMAIL]">%s<span>Copiar dirección</span></button></div></div>' % (ic('carta',20), ic('copiar',20))),
  ('para-que','Escríbenos si…', tarjetas([('alerta','Has visto un error','Dinos el artículo y, si puedes, la fuente correcta.',''),('escudo','Tienes un caso','Para «¿Pagó o no pagó?»: qué pasó y qué respondió la aseguradora. Te pediremos permiso y quitaremos tus datos.','pg-tarjeta--lila'),('bombilla','Tienes una idea','Un tema, una guía o una herramienta que te gustaría ver.','pg-tarjeta--amarillo'),('candado','Quieres ejercer tus derechos','Acceso, rectificación, supresión… de tus datos personales.','pg-tarjeta--menta')])),
  ('no-podemos','Lo que no podemos hacer', '<span class="pg-sello">No asesoramos</span><p>No somos asesoría ni mediador de seguros: no podemos revisar tu póliza de forma personalizada, recomendarte una aseguradora ni gestionar tu reclamación.</p><p>Para empezar por tu cuenta: la guía <a href="/seccion/que-hacer-si/">Qué hacer si…</a>, la <a href="/herramientas/calculadora-de-plazos/">calculadora de plazos</a> y el <a href="/herramientas/generador-de-cartas/">generador de cartas</a>. Si tu caso es complejo, consulta con un profesional o una asociación de consumidores.</p>'),
  ('responsable','Datos del responsable', datos(TIT)+'<p>Al escribirnos, tratamos tus datos solo para responderte. Más información en la <a href="/politica-de-privacidad/">política de privacidad</a>.</p>')], final=False))

P['aviso-legal'] = ('Aviso legal', pagina('aviso-legal','balanza','Aviso legal','Las reglas del juego, <em>sin letra pequeña.</em>',
 'Datos del titular y condiciones de uso de espabilao.com, como exige la Ley 34/2002 de servicios de la sociedad de la información (LSSI-CE).',
 [ACT,('balanza','LSSI-CE, art. 10')], '§',
 [('si','Web de información general sobre seguros en España.'),('no','No somos aseguradora ni mediador, ni cobramos comisiones.'),('alerta','La información no sustituye a tu póliza ni a un profesional.')],
 [('titular','Datos del titular', datos(TIT+[('Sitio web','espabilao.com')])),
  ('objeto','Objeto', '<p>Espabilao es un sitio web de información general sobre seguros en España. El titular no es entidad aseguradora ni mediador de seguros, no comercializa seguros ni percibe comisiones de aseguradoras.</p>'),
  ('uso','Condiciones de uso', '<p>El acceso es gratuito y no requiere registro. Al navegar aceptas este aviso legal y te comprometes a hacer un uso adecuado de los contenidos, sin emplearlos para actividades ilícitas o que perjudiquen a terceros o al funcionamiento de la web.</p>'),
  ('responsabilidad','Información general, no asesoramiento', aviso('Los contenidos son informativos y generales. No son asesoramiento jurídico, financiero ni de seguros personalizado, y no sustituyen la lectura de tu póliza ni la consulta a un profesional. Lo que cubre un seguro depende de cada contrato.')+'<p>Las herramientas (calculadoras, generador de cartas y detector de letra pequeña) ofrecen resultados orientativos. El titular procura que la información sea exacta y actualizada, e indica la fecha de revisión de cada artículo, pero no garantiza la ausencia de errores ni se responsabiliza de las decisiones tomadas a partir de ella.</p>'),
  ('propiedad','Propiedad intelectual e industrial', '<p>Los textos, diseños, logotipos, herramientas y demás elementos de la web son titularidad de [NOMBRE] o se usan con autorización. Puedes compartir enlaces y citar fragmentos breves indicando la fuente. Las plantillas de cartas pueden usarse libremente para tus reclamaciones personales. Queda prohibida la reproducción total o parcial con fines comerciales sin autorización.</p><p>Las marcas de terceros (por ejemplo, de aseguradoras) pertenecen a sus titulares y se mencionan solo con fines informativos.</p>'),
  ('enlaces','Enlaces y publicidad', '<p>La web enlaza a sitios de terceros, como el BOE o la DGSFP, y muestra anuncios de Google AdSense identificados como «Publicidad». El titular no se responsabiliza del contenido de esos sitios ni de los anuncios, cuya aparición no supone recomendación. Más información en la <a href="/politica-de-cookies/">política de cookies</a>.</p>'),
  ('datos','Protección de datos', '<p>El tratamiento de datos personales se explica en la <a href="/politica-de-privacidad/">política de privacidad</a>.</p>'),
  ('ley','Legislación aplicable', '<p>Este aviso legal se rige por la legislación española. Si eres consumidor, para cualquier controversia serán competentes los juzgados y tribunales de tu domicilio, conforme a la normativa de consumidores y usuarios.</p>')]))

P['politica-de-privacidad'] = ('Política de privacidad', pagina('politica-de-privacidad','candado','Política de privacidad','Tus datos, <em>lo justo y necesario.</em>',
 'Qué datos tratamos en espabilao.com, para qué y cómo ejercer tus derechos, según el RGPD y la Ley Orgánica 3/2018 (LOPDGDD).',
 [ACT,('candado','RGPD · LOPDGDD')], 'RGPD',
 [('no','Sin formularios de captación: no pedimos tu teléfono ni vendemos datos.'),('navegador','Las herramientas funcionan en tu navegador: no guardamos lo que escribes.'),('galleta','Publicidad de Google solo con tu consentimiento.')],
 [('responsable','Responsable del tratamiento', datos(TIT)),
  ('datos','Qué datos tratamos y para qué', '<h3>Si nos escribes por correo</h3><p>Tu dirección de correo, tu nombre si lo indicas y el contenido de tu mensaje (y la documentación que decidas enviarnos), para responderte. <strong>Base jurídica:</strong> tu consentimiento y nuestro interés legítimo en atender tu consulta (art. 6.1.a y 6.1.f RGPD). <strong>Conservación:</strong> lo necesario para responderte y, después, durante los plazos legales.</p><h3>Cuando navegas</h3><p>El servidor registra datos técnicos (IP, navegador, fecha, página visitada) para la seguridad y el buen funcionamiento de la web, por ejemplo para bloquear accesos no autorizados. <strong>Base jurídica:</strong> interés legítimo (art. 6.1.f RGPD). Se conservan durante un tiempo limitado.</p><h3>Publicidad</h3><p>Si das tu consentimiento, Google y sus socios usan cookies e identificadores para mostrar anuncios y medir su rendimiento. <strong>Base jurídica:</strong> tu consentimiento (art. 6.1.a RGPD), que puedes retirar cuando quieras. Más información en la <a href="/politica-de-cookies/">política de cookies</a> y en <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">cómo usa Google la información de los sitios que usan sus servicios</a>.</p><h3>Herramientas de la web</h3>'+aviso('La calculadora de plazos, el generador de cartas, el detector de letra pequeña y la calculadora de infraseguro funcionan en tu navegador: lo que escribes <strong>no se envía ni se guarda</strong> en nuestros servidores.')),
  ('no','Qué no hacemos', tarjetas([('no','Sin captación','No tenemos formularios ni pedimos tu teléfono.','pg-tarjeta--no'),('no','Sin venta de datos','No cedemos tus datos a aseguradoras ni a terceros con fines comerciales.','pg-tarjeta--no'),('no','Sin decisiones automáticas','No tomamos decisiones automatizadas que te afecten.','pg-tarjeta--no'),('si','Lo mínimo','Solo tratamos lo necesario para cada finalidad.','pg-tarjeta--si')])),
  ('destinatarios','Destinatarios', ul(['<strong>Alojamiento web:</strong> Namecheap, Inc., como encargado del tratamiento.','<strong>Correo electrónico:</strong> [indica tu proveedor de correo].','<strong>Publicidad:</strong> Google Ireland Limited y sus socios, si das tu consentimiento.','<strong>Autoridades públicas</strong>, cuando exista una obligación legal.'])),
  ('transferencias','Transferencias internacionales', '<p>Algunos proveedores (como Namecheap o Google) pueden tratar datos fuera del Espacio Económico Europeo, en particular en Estados Unidos. Esas transferencias se amparan en las garantías del RGPD, como el Marco de Privacidad de Datos UE-EE. UU. cuando el proveedor esté adherido, o las cláusulas contractuales tipo de la Comisión Europea.</p>'),
  ('derechos','Tus derechos', pasos(['<strong>Escríbenos</strong> a %s indicando qué derecho quieres ejercer: acceso, rectificación, supresión, oposición, limitación o portabilidad, o retirar tu consentimiento.' % MAIL,'<strong>Te respondemos</strong> en el plazo legal (un mes, ampliable en casos complejos).','<strong>Si no estás conforme</strong>, puedes reclamar ante la <a href="https://www.aepd.es" target="_blank" rel="noopener">Agencia Española de Protección de Datos</a>.'])),
  ('menores','Menores', '<p>La web no está dirigida a menores de 14 años. Si eres menor, no nos envíes datos personales.</p>'),
  ('cambios','Cambios', '<p>Podemos actualizar esta política para adaptarla a cambios legales o del funcionamiento de la web. Aquí estará siempre la versión vigente, con su fecha. Última actualización: [FECHA].</p>')]))

P['politica-de-cookies'] = ('Política de cookies', pagina('politica-de-cookies','galleta','Política de cookies','Cookies, <em>explicadas sin trampa.</em>',
 'Qué cookies usa espabilao.com, incluidas las de Google AdSense, y cómo aceptarlas, rechazarlas o borrarlas cuando quieras.',
 [ACT,('balanza','LSSI-CE, art. 22.2'),('escudo','Guía de cookies de la AEPD')], '{ }',
 [('si','Las necesarias funcionan sin pedirte permiso.'),('galleta','Las de publicidad de Google, solo si las aceptas.'),('no','Rechazar es tan fácil como aceptar, y puedes cambiar de opinión.')],
 [('que-son','¿Qué son las cookies?', '<p>Pequeños archivos que una web guarda en tu navegador para recordar información sobre tu visita. Esta política también se aplica a tecnologías parecidas, como el almacenamiento local o los identificadores de publicidad.</p>'),
  ('cuales','Cookies que usamos', '<div class="pg-tabla-envoltorio"><table class="pg-tabla"><thead><tr><th>Tipo</th><th>Para qué</th><th>Quién</th><th>¿Pide permiso?</th></tr></thead><tbody><tr><td><strong>Preferencias de consentimiento</strong></td><td>Recordar si aceptaste o rechazaste las cookies</td><td>Espabilao / herramienta de consentimiento</td><td><span class="pg-etq pg-etq--si">No, es necesaria</span></td></tr><tr><td><strong>Sesión de WordPress</strong> <code>wordpress_logged_in_*</code></td><td>Solo para quien entra en el panel de administración</td><td>Espabilao</td><td><span class="pg-etq pg-etq--si">No, es necesaria</span></td></tr><tr><td><strong>Seguridad</strong></td><td>Impedir accesos no autorizados</td><td>Espabilao</td><td><span class="pg-etq pg-etq--si">No, es necesaria</span></td></tr><tr><td><strong>Publicidad</strong> <code>__gads</code>, <code>__gpi</code>, <code>IDE</code>, <code>DSID</code>…</td><td>Mostrar anuncios (personalizados si lo aceptas), limitar repeticiones, medir y prevenir fraude</td><td>Google y sus socios</td><td><span class="pg-etq pg-etq--no">Sí</span></td></tr></tbody></table></div><p>El diseño de la web y sus herramientas no instalan cookies propias de seguimiento.</p>'),
  ('adsense','Google AdSense', '<p>Usamos <strong>Google AdSense</strong>, el servicio de publicidad de Google Ireland Limited. Si no das tu consentimiento, Google puede mostrar anuncios no personalizados, que también pueden usar cookies para frecuencia, medición y prevención del fraude, según tu configuración.</p>'+tarjetas([('libro','Cómo usa Google tu información','<a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">En sitios que usan sus servicios</a>',''),('galleta','Cookies en la publicidad','<a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Política de Google</a>','pg-tarjeta--lila'),('usuario','Mi Centro de Anuncios','<a href="https://myadcenter.google.com" target="_blank" rel="noopener">Gestiona la personalización</a>','pg-tarjeta--menta')])),
  ('analitica','Analítica', aviso('[Si instalas una herramienta de analítica (por ejemplo, Google Analytics), indícala aquí con sus cookies y finalidad. Si no usas ninguna, borra este apartado.]')),
  ('consentimiento','Cómo das o retiras tu consentimiento', pasos(['<strong>Al entrar</strong> te mostramos un aviso para aceptar, rechazar o configurar las cookies que no son necesarias. El aviso de Google cumple el Marco de Transparencia y Consentimiento (TCF) de IAB Europe.','<strong>Rechazar es tan fácil como aceptar</strong>, y puedes navegar por la web aunque no aceptes las cookies de publicidad.','<strong>Puedes cambiar de opinión</strong> cuando quieras: vuelve a abrir el aviso de consentimiento o borra las cookies de tu navegador, y te volveremos a preguntar.'])),
  ('navegador','Bloquear o borrar cookies en tu navegador', tarjetas([('navegador','Google Chrome','<a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener">Ver instrucciones</a>',''),('navegador','Mozilla Firefox','<a href="https://support.mozilla.org/es/kb/Borrar%20cookies" target="_blank" rel="noopener">Ver instrucciones</a>','pg-tarjeta--lila'),('navegador','Safari','<a href="https://support.apple.com/es-es/guide/safari/sfri11471/mac" target="_blank" rel="noopener">Ver instrucciones</a>','pg-tarjeta--menta'),('navegador','Microsoft Edge','<a href="https://support.microsoft.com/es-es/microsoft-edge" target="_blank" rel="noopener">Ver instrucciones</a>','pg-tarjeta--amarillo')])+'<p>Si bloqueas todas las cookies, algunas funciones de la web pueden no funcionar bien.</p>'),
  ('responsable','Responsable y contacto', datos(TIT)+'<p>Consulta también la <a href="/politica-de-privacidad/">política de privacidad</a>. Última actualización: [FECHA].</p>')]))

for slug,(t,c) in P.items():
    open('v2/%s.html'%slug,'w').write(c)
json.dump([{'slug':s,'title':t,'archivo':'v2/%s.html'%s} for s,(t,c) in P.items()],open('v2/paginas.json','w'),ensure_ascii=False,indent=1)
print({s:len(c) for s,(t,c) in P.items()})
