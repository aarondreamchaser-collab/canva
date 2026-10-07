/* Calculadora de potencia v3 de tuluzencasa.com: «Cuadro eléctrico virtual».
   WPCode: fragmento JavaScript nuevo, pie de todo el sitio. Sale sin hacer nada si la página no tiene #tl3-potencia.
   Mismos aparatos, margen (10 %) y precio del término de potencia que la calculadora anterior. Sin librerías. */
(function(){
  var app=document.getElementById('tl3-potencia'); if(!app||app.getAttribute('data-listo')) return;
  app.setAttribute('data-listo','1');
  var W=window, D=document;
  var RM=W.matchMedia&&W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var IMP=1.21*1.0511, POT_DIA=0.09, MES=30.4, MARGEN=1.1, DEF_KW=4.6;
  var POT=[2.3,3.45,4.6,5.75,6.9,8.05,9.2], MAX_KW=POT[POT.length-1], ESCALA=10;
  var GRUPOS=['Climatización','Agua caliente','Cocina','Lavado','Ocio, luz y otros','Movilidad'];
  var A=[
    {id:'ac',g:'Climatización',n:'Aire acondicionado 3.000 frigorías',w:1000},
    {id:'rad',g:'Climatización',n:'Radiador de aceite',w:2000},
    {id:'est',g:'Climatización',n:'Estufa o calefactor',w:2000},
    {id:'bdc',g:'Climatización',n:'Bomba de calor (calefacción)',w:900},
    {id:'ter',g:'Agua caliente',n:'Termo eléctrico',w:1500},
    {id:'ind',g:'Cocina',n:'Placa de inducción (un fuego)',w:1800},
    {id:'vit',g:'Cocina',n:'Vitrocerámica (un fuego)',w:1800},
    {id:'hor',g:'Cocina',n:'Horno eléctrico',w:2200},
    {id:'mic',g:'Cocina',n:'Microondas',w:1000},
    {id:'her',g:'Cocina',n:'Hervidor de agua',w:2000},
    {id:'fre',g:'Cocina',n:'Freidora de aire',w:1500},
    {id:'caf',g:'Cocina',n:'Cafetera',w:1000},
    {id:'nev',g:'Cocina',n:'Nevera combi',w:150,on:1},
    {id:'con',g:'Cocina',n:'Congelador',w:150},
    {id:'lav',g:'Lavado',n:'Lavadora (calentando agua)',w:2000},
    {id:'sev',g:'Lavado',n:'Secadora de evacuación',w:2500},
    {id:'seb',g:'Lavado',n:'Secadora con bomba de calor',w:900},
    {id:'lvv',g:'Lavado',n:'Lavavajillas',w:1200},
    {id:'pla',g:'Lavado',n:'Plancha',w:2200},
    {id:'tv',g:'Ocio, luz y otros',n:'Televisión',w:100,on:1},
    {id:'pc',g:'Ocio, luz y otros',n:'Ordenador gaming',w:400},
    {id:'led',g:'Ocio, luz y otros',n:'Iluminación LED (10 bombillas)',w:90,on:1},
    {id:'asp',g:'Ocio, luz y otros',n:'Aspiradora',w:800},
    {id:'sec',g:'Ocio, luz y otros',n:'Secador de pelo',w:1800},
    {id:'car',g:'Movilidad',n:'Cargador de coche eléctrico 7,4 kW',w:7400}
  ];
  var byId={}; A.forEach(function(a){byId[a.id]=a;});
  var ICONO={'Climatización':'M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1 19.1 4.9','Agua caliente':'M12 2s6 7 6 12a6 6 0 0 1-12 0c0-5 6-12 6-12z','Cocina':'M4 10h16v10H4zM8 6h8M9 3h6','Lavado':'M5 3h14v18H5zM12 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6z','Ocio, luz y otros':'M9 18h6M10 21h4M12 3a6 6 0 0 0-3 11v2h6v-2a6 6 0 0 0-3-11z','Movilidad':'M5 16h14l-2-6H7zM7 16v2M17 16v2M9 8l1-3h4l1 3'};
  var SITUACIONES=[
    {n:'Cena entre semana',i:{nev:1,ind:1,hor:1,lvv:1,tv:1,led:1}},
    {n:'Mañana con prisa',i:{nev:1,ter:1,caf:1,mic:1,sec:1,led:1}},
    {n:'Tarde de verano',i:{nev:1,ac:2,tv:1,lav:1,led:1}},
    {n:'Noche de invierno',i:{nev:1,rad:1,est:1,ter:1,tv:1,led:1}},
    {n:'Cargando el coche',i:{nev:1,car:1,lvv:1,tv:1,led:1}}
  ];
  var S={kw:DEF_KW,sel:{},otro:0}; A.forEach(function(a){if(a.on)S.sel[a.id]=1;});
  var saltado=false, demo=null;

  function nf(n,a,b){return n.toLocaleString('es-ES',{minimumFractionDigits:a,maximumFractionDigits:b});}
  function eur(n){return nf(n,2,2);}
  function kwf(n){return nf(n,0,2);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function anual(kw){return kw*POT_DIA*365*IMP;}
  function suma(){var w=0;A.forEach(function(a){if(S.sel[a.id])w+=a.w*S.sel[a.id];});return w+(S.otro>0?S.otro:0);}
  function recomendada(kw){var need=kw*MARGEN;for(var i=0;i<POT.length;i++)if(POT[i]>=need-1e-9)return POT[i];return null;}

  if(!D.getElementById('tl3p-css')){
    var css=D.createElement('style');css.id='tl3p-css';
    css.textContent=[
'.tl3p{--n0:#070D18;--n1:#0C1626;--n2:#122036;--n3:#1B2D49;--lin:#2A4166;--tx:#E8F0FA;--tx2:#9DB0C8;--am:#F2C230;--ci:#3BE0FF;--ro:#FF5D6C;--ve:#3DDC97;',
' position:relative;color:var(--tx);background:radial-gradient(1000px 420px at 85% -10%,#1d3a66 0,transparent 60%),radial-gradient(700px 380px at 0% 110%,#2b2350 0,transparent 55%),var(--n0);border-radius:24px;padding:22px;margin:0 0 2em;overflow:hidden;font-size:15px;line-height:1.45;isolation:isolate;box-shadow:0 30px 60px -30px #050a14cc,inset 0 0 0 1px #ffffff10}',
'.tl3p::before{content:"";position:absolute;inset:0;background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px);background-size:32px 32px;mask-image:linear-gradient(180deg,#000 0,transparent 70%);-webkit-mask-image:linear-gradient(180deg,#000 0,transparent 70%);pointer-events:none;z-index:-1}',
'.tl3p *{box-sizing:border-box}.tl3p button{font:inherit;cursor:pointer}',
'.tl3p h2,.tl3p h3,.tl3p h4{color:var(--tx);margin:0;letter-spacing:-.01em}',
'.tl3p-cab{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;margin:0 0 14px}',
'.tl3p-cab h2{font-size:1.25rem;font-weight:800;display:flex;align-items:center;gap:10px}',
'.tl3p-cab h2::before{content:"";width:10px;height:10px;border-radius:50%;background:var(--ve);box-shadow:0 0 0 4px #3ddc9733,0 0 14px var(--ve)}',
'.tl3p.is-saltado .tl3p-cab h2::before{background:var(--ro);box-shadow:0 0 0 4px #ff5d6c33,0 0 14px var(--ro)}',
'.tl3p-sit{display:flex;flex-wrap:wrap;gap:6px}',
'.tl3p .tl3p-chip{background:#ffffff0d;border:1px solid var(--lin);color:var(--tx2);border-radius:999px;padding:6px 12px;font-size:.85rem;font-weight:600;transition:all .2s}',
'.tl3p .tl3p-chip:hover,.tl3p .tl3p-chip[aria-pressed="true"]{color:var(--n0);background:var(--am);border-color:var(--am)}',
'.tl3p-top{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:16px;align-items:stretch}',
'.tl3p-c{background:linear-gradient(180deg,#ffffff0f,#ffffff05);border:1px solid #ffffff17;border-radius:18px;padding:16px;position:relative;overflow:hidden}',
'.tl3p-l{display:block;font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--tx2)}',
'.tl3p-gauge svg{display:block;width:100%;height:auto;overflow:visible}',
'.tl3p-gauge text{font:700 12px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;fill:var(--tx2)}',
'.tl3p-aguja{transition:transform .9s cubic-bezier(.2,1.4,.4,1);transform-origin:200px 200px}',
'.tl3p-lect{text-align:center;margin-top:-6px}',
'.tl3p-lect strong{display:block;font-size:2.6rem;line-height:1;font-weight:800;font-variant-numeric:tabular-nums;color:var(--ci);text-shadow:0 0 24px #3be0ff55}',
'.tl3p.is-saltado .tl3p-lect strong{color:var(--ro);text-shadow:0 0 24px #ff5d6c88}',
'.tl3p-lect span{color:var(--tx2);font-size:.85rem}',
'.tl3p-cuadro{display:flex;flex-direction:column;gap:12px}',
'.tl3p-icp{display:flex;gap:14px;align-items:center;background:#0b1524;border:1px solid #ffffff1c;border-radius:14px;padding:12px 14px}',
'.tl3p-icp svg{flex:none;width:58px;height:84px}',
'.tl3p-pal{transition:transform .35s cubic-bezier(.3,1.6,.5,1);transform-origin:29px 42px}',
'.tl3p.is-saltado .tl3p-pal{transform:rotate(180deg)}',
'.tl3p-icp-t h3{font-size:1rem;font-weight:800}',
'.tl3p-icp-t p{margin:2px 0 0;font-size:.85rem;color:var(--tx2)}',
'.tl3p-led{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--ve);box-shadow:0 0 10px var(--ve);margin-right:6px;vertical-align:1px}',
'.tl3p.is-saltado .tl3p-led{background:var(--ro);box-shadow:0 0 10px var(--ro);animation:tl3p-parp .6s steps(2) infinite}',
'@keyframes tl3p-parp{50%{opacity:.2}}',
'.tl3p-res{display:grid;grid-template-columns:1fr 1fr;gap:10px}',
'.tl3p-res div{background:#ffffff08;border:1px solid #ffffff14;border-radius:12px;padding:10px 12px}',
'.tl3p-res strong{display:block;font-size:1.35rem;font-weight:800;font-variant-numeric:tabular-nums}',
'.tl3p-res .rec strong{color:var(--am);text-shadow:0 0 18px #f2c23055}',
'.tl3p-res small{color:var(--tx2);font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em}',
'.tl3p-res .tl3p-dif{grid-column:1/-1}',
'.tl3p-ctl{display:flex;flex-wrap:wrap;gap:8px;align-items:end}',
'.tl3p-ctl label{flex:1;min-width:140px;font-size:.78rem;color:var(--tx2);font-weight:700;display:flex;flex-direction:column;gap:4px}',
'.tl3p select,.tl3p input[type=number]{width:100%;background:var(--n1);color:#fff;border:1px solid var(--lin);border-radius:10px;padding:9px 10px;font:inherit}',
'.tl3p select:focus-visible,.tl3p input:focus-visible,.tl3p button:focus-visible{outline:2px solid var(--ci);outline-offset:2px}',
'.tl3p .tl3p-bt{background:var(--am);color:var(--n0);border:0;border-radius:10px;padding:10px 14px;font-weight:800;box-shadow:0 8px 20px -10px var(--am)}',
'.tl3p .tl3p-bt2{background:#ffffff10;color:var(--tx);border:1px solid #ffffff26;border-radius:10px;padding:9px 12px;font-weight:700}',
'.tl3p .tl3p-bt2:hover{border-color:var(--ci)}',
'.tl3p-pan{margin-top:16px}',
'.tl3p-pan-cab{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px;margin:0 0 10px}',
'.tl3p-pan-cab h3{font-size:1.05rem;font-weight:800}',
'.tl3p-pan-cab p{margin:0;color:var(--tx2);font-size:.85rem}',
'.tl3p-g{margin:12px 0 6px;font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--tx2)}',
'.tl3p-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:8px}',
'.tl3p-grid>div{min-width:0}',
'.tl3p .tl3p-br{display:flex;align-items:center;gap:10px;background:linear-gradient(180deg,#16263f,#0e1a2d);border:1px solid #ffffff17;border-radius:12px;padding:10px;text-align:left;color:var(--tx);position:relative;transition:transform .15s,border-color .2s,box-shadow .2s;width:100%;padding-right:40px}',
'.tl3p .tl3p-br:hover{border-color:#ffffff3a}',
'.tl3p .tl3p-br:active{transform:translateY(1px)}',
'.tl3p .tl3p-br[aria-pressed="true"]{border-color:#f2c230aa;box-shadow:0 0 0 1px #f2c23055,0 10px 24px -14px var(--am)}',
'.tl3p-pal2{flex:none;width:22px;height:38px;border-radius:6px;background:#070d18;border:1px solid #ffffff22;position:relative}',
'.tl3p-pal2::after{content:"";position:absolute;left:3px;right:3px;height:16px;bottom:3px;border-radius:4px;background:#5d6f88;transition:all .2s}',
'.tl3p .tl3p-br[aria-pressed="true"] .tl3p-pal2::after{bottom:17px;background:var(--am);box-shadow:0 0 10px var(--am)}',
'.tl3p .tl3p-br svg{flex:none;width:18px;height:18px;fill:none;stroke:var(--tx2);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}',
'.tl3p .tl3p-br[aria-pressed="true"] svg{stroke:var(--am)}',
'.tl3p .tl3p-br .n{flex:1;min-width:0;overflow-wrap:break-word;font-weight:700;font-size:.88rem;line-height:1.2}',
'.tl3p .tl3p-br .n small{display:block;color:var(--tx2);font-weight:600;font-size:.76rem;margin-top:2px}',
'.tl3p .tl3p-x{position:absolute;top:6px;right:6px;background:#ffffff14;border:0;color:var(--tx);border-radius:6px;font-size:.72rem;font-weight:800;padding:2px 6px}',
'.tl3p-otro{display:flex;gap:8px;align-items:center;margin-top:10px;background:#ffffff08;border:1px dashed #ffffff26;border-radius:12px;padding:10px}',
'.tl3p-otro label{flex:1;font-size:.85rem;color:var(--tx2);font-weight:600}',
'.tl3p-otro input{max-width:150px}',
'.tl3p-tabla{width:100%;border-collapse:collapse;margin-top:8px;font-size:.88rem}',
'.tl3p-tabla th,.tl3p-tabla td{padding:8px 10px;border-bottom:1px solid #ffffff14;text-align:right;font-variant-numeric:tabular-nums}',
'.tl3p-tabla th:first-child,.tl3p-tabla td:first-child{text-align:left}',
'.tl3p-tabla th{color:var(--tx2);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em}',
'.tl3p-tabla tr.rec td{color:var(--am);font-weight:800}',
'.tl3p-tabla tr.cur td:first-child::after{content:" · la tuya";color:var(--ci);font-weight:700}',
'.tl3p-tabla tr.corta td{color:#ff5d6c99}',
'.tl3p-msg{min-height:1.3em;font-size:.88rem;color:var(--ve);margin-top:10px}',
'.tl3p.is-saltado .tl3p-msg{color:var(--ro)}',
'.tl3p-apagon{position:absolute;inset:0;background:#000;opacity:0;pointer-events:none;z-index:5}',
'.tl3p-apagon.on{animation:tl3p-ap 1s ease-out}',
'@keyframes tl3p-ap{0%{opacity:.75}15%{opacity:.1}25%{opacity:.6}100%{opacity:0}}',
'.tl3p-pie{display:flex;flex-wrap:wrap;gap:8px;justify-content:flex-end;margin-top:14px;padding-top:12px;border-top:1px solid #ffffff14}',
'@media (max-width:900px){.tl3p-top{grid-template-columns:1fr}}',
'@media (max-width:600px){.tl3p{padding:14px;border-radius:18px;margin-left:-4px;margin-right:-4px}.tl3p-grid{grid-template-columns:1fr;gap:6px}.tl3p .tl3p-br{padding:8px 44px 8px 10px;gap:10px}.tl3p .tl3p-br svg{display:none}.tl3p-lect strong{font-size:2.1rem}.tl3p-res strong{font-size:1.15rem}}',
'@media (prefers-reduced-motion:reduce){.tl3p-aguja,.tl3p-pal{transition:none}.tl3p-apagon.on{animation:none}}'
    ].join('\n');
    D.head.appendChild(css);
  }

  app.classList.add('tl3p');
  /* esfera del medidor: 0..10 kW en un arco de 180º */
  function ang(kw){return -90+Math.min(ESCALA,Math.max(0,kw))/ESCALA*180;}
  function punto(kw,r){var a=(ang(kw)-90)*Math.PI/180;return [200+r*Math.cos(a),200+r*Math.sin(a)];}
  function arco(k0,k1,r){var p0=punto(k0,r),p1=punto(k1,r);return 'M'+p0[0].toFixed(1)+' '+p0[1].toFixed(1)+' A'+r+' '+r+' 0 '+((k1-k0)/ESCALA*180>180?1:0)+' 1 '+p1[0].toFixed(1)+' '+p1[1].toFixed(1);}
  var marcas='';for(var k=0;k<=ESCALA;k++){var a1=punto(k,170),a2=punto(k,k%2?160:154),t=punto(k,136);marcas+='<line x1="'+a1[0].toFixed(1)+'" y1="'+a1[1].toFixed(1)+'" x2="'+a2[0].toFixed(1)+'" y2="'+a2[1].toFixed(1)+'" stroke="#9DB0C8" stroke-width="'+(k%2?1:2)+'"/>'+(k%2?'':'<text x="'+t[0].toFixed(1)+'" y="'+(t[1]+4).toFixed(1)+'" text-anchor="middle">'+k+'</text>');}

  app.innerHTML=
   '<div class="tl3p-apagon" aria-hidden="true"></div>'+
   '<div class="tl3p-cab"><h2>Cuadro eléctrico virtual</h2><div class="tl3p-sit" role="group" aria-label="Situaciones típicas"></div></div>'+
   '<div class="tl3p-top">'+
     '<div class="tl3p-c tl3p-gauge"><span class="tl3p-l">Potencia encendida a la vez</span>'+
       '<svg viewBox="0 0 400 230" role="img" aria-label="Medidor de potencia"><defs><linearGradient id="tl3p-gr" x1="0" x2="1"><stop offset="0" stop-color="#3DDC97"/><stop offset=".55" stop-color="#F2C230"/><stop offset="1" stop-color="#FF5D6C"/></linearGradient>'+
       '<filter id="tl3p-gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'+
       '<path d="'+arco(0,ESCALA,180)+'" stroke="#ffffff14" stroke-width="18" fill="none" stroke-linecap="round"/>'+
       '<path data-carga d="'+arco(0,0.01,180)+'" stroke="url(#tl3p-gr)" stroke-width="18" fill="none" stroke-linecap="round" filter="url(#tl3p-gl)"/>'+
       '<path data-zona d="" stroke="#FF5D6C" stroke-width="5" fill="none" opacity=".8"/>'+
       marcas+
       '<g data-contr></g>'+
       '<g class="tl3p-aguja" data-aguja style="transform:rotate(-90deg)"><path d="M197 200 L200 46 L203 200 Z" fill="#fff" filter="url(#tl3p-gl)"/></g><circle cx="200" cy="200" r="12" fill="#0b1524" stroke="#fff" stroke-width="3"/>'+
       '</svg><div class="tl3p-lect" aria-live="polite"><strong data-v="kw">0 kW</strong><span data-v="n">0 aparatos encendidos</span></div></div>'+
     '<div class="tl3p-cuadro">'+
       '<div class="tl3p-icp"><svg viewBox="0 0 58 84" aria-hidden="true"><rect x="1" y="1" width="56" height="82" rx="8" fill="#0b1524" stroke="#3BE0FF" stroke-opacity=".6"/><rect x="17" y="20" width="24" height="44" rx="5" fill="#070d18" stroke="#ffffff33"/><g class="tl3p-pal"><rect x="20" y="22" width="18" height="18" rx="4" fill="#F2C230"/></g><text x="29" y="78" text-anchor="middle" style="font:800 8px system-ui;fill:#9DB0C8">ICP</text><text x="29" y="14" text-anchor="middle" style="font:800 8px system-ui;fill:#9DB0C8" data-v="icpkw">4,6 kW</text></svg>'+
         '<div class="tl3p-icp-t"><h3><span class="tl3p-led"></span><span data-v="estado">Todo funciona</span></h3><p data-v="estado2">Enciende lo que pueda coincidir en el peor momento del día.</p></div></div>'+
       '<div class="tl3p-res" aria-live="polite"><div class="rec"><small>Recomendada</small><strong data-v="rec">–</strong></div><div><small>Con margen del 10 %</small><strong data-v="mar">0 kW</strong></div><div class="tl3p-dif"><small data-v="difl">Comparación anual</small><strong data-v="dif">–</strong></div></div>'+
       '<div class="tl3p-ctl"><label>Tu potencia contratada<select data-kw></select></label><button type="button" class="tl3p-bt" data-acc="demo">Encender uno a uno</button><button type="button" class="tl3p-bt2" data-acc="reset">Rearmar y vaciar</button></div>'+
     '</div>'+
   '</div>'+
   '<div class="tl3p-msg" role="status"></div>'+
   '<div class="tl3p-pan tl3p-c"><div class="tl3p-pan-cab"><h3>¿Qué puede coincidir?</h3><p>Pulsa cada interruptor. Toca ×1 para poner dos iguales.</p></div><div data-lista></div>'+
     '<div class="tl3p-otro"><label for="tl3p-otro">Otro aparato que no está en la lista (W)</label><input id="tl3p-otro" type="number" min="0" step="10" inputmode="numeric" placeholder="Ej. 1200" data-otro></div></div>'+
   '<div class="tl3p-pan tl3p-c"><div class="tl3p-pan-cab"><h3>Lo que cuesta cada potencia al año</h3><p>Término de potencia con impuesto eléctrico (5,11 %) e IVA (21 %).</p></div><div style="overflow-x:auto"><table class="tl3p-tabla"><thead><tr><th>Potencia</th><th>Al mes</th><th>Al año</th><th>Frente a la tuya</th></tr></thead><tbody data-tabla></tbody></table></div></div>'+
   '<div class="tl3p-pie"><button type="button" class="tl3p-bt2" data-acc="enlace">Copiar enlace</button></div>';

  function q(s){return app.querySelector(s);}
  function qa(s){return Array.prototype.slice.call(app.querySelectorAll(s));}
  var V={};qa('[data-v]').forEach(function(e){V[e.getAttribute('data-v')]=e;});
  var sel=q('[data-kw]');POT.forEach(function(p){sel.add(new Option(kwf(p)+' kW',String(p)));});sel.value=String(S.kw);

  /* lista de interruptores */
  var html='';
  GRUPOS.forEach(function(g){
    html+='<p class="tl3p-g">'+g+'</p><div class="tl3p-grid">';
    A.filter(function(a){return a.g===g;}).forEach(function(a){
      html+='<div style="position:relative"><button type="button" class="tl3p-br" data-id="'+a.id+'" aria-pressed="false"><span class="tl3p-pal2"></span><svg viewBox="0 0 24 24"><path d="'+(ICONO[g]||ICONO['Cocina'])+'"/></svg><span class="n">'+esc(a.n)+'<small>'+nf(a.w,0,0)+' W</small></span></button><button type="button" class="tl3p-x" data-x="'+a.id+'" aria-label="Cantidad de '+esc(a.n)+'">×1</button></div>';
    });
    html+='</div>';
  });
  q('[data-lista]').innerHTML=html;
  var sit=q('.tl3p-sit');
  SITUACIONES.forEach(function(s,i){var b=D.createElement('button');b.type='button';b.className='tl3p-chip';b.textContent=s.n;b.setAttribute('data-sit',i);b.setAttribute('aria-pressed','false');sit.appendChild(b);});

  var msgT;
  function msg(t){var m=q('.tl3p-msg');m.textContent=t;clearTimeout(msgT);if(t)msgT=setTimeout(function(){m.textContent='';},5000);}
  function apagon(){var a=q('.tl3p-apagon');a.classList.remove('on');void a.offsetWidth;if(!RM)a.classList.add('on');}

  function pintar(){
    var w=suma(), kw=w/1000, rec=w>0?recomendada(kw):null, n=0;
    A.forEach(function(a){if(S.sel[a.id])n+=S.sel[a.id];});if(S.otro>0)n++;
    var antes=saltado; saltado=kw>S.kw+1e-9;
    app.classList.toggle('is-saltado',saltado);
    if(saltado&&!antes)apagon();
    /* medidor */
    q('[data-aguja]').style.transform='rotate('+ang(kw).toFixed(1)+'deg)';
    q('[data-carga]').setAttribute('d',arco(0,Math.max(0.01,Math.min(ESCALA,kw)),180));
    q('[data-zona]').setAttribute('d',arco(Math.min(ESCALA-0.01,S.kw),ESCALA,196));
    var pc=punto(S.kw,198),pc2=punto(S.kw,150),pt=punto(S.kw,214);
    q('[data-contr]').innerHTML='<line x1="'+pc[0].toFixed(1)+'" y1="'+pc[1].toFixed(1)+'" x2="'+pc2[0].toFixed(1)+'" y2="'+pc2[1].toFixed(1)+'" stroke="#fff" stroke-width="3" stroke-dasharray="4 3"/><text x="'+pt[0].toFixed(1)+'" y="'+(pt[1]+4).toFixed(1)+'" text-anchor="middle" style="fill:#fff">'+kwf(S.kw)+'</text>';
    V.kw.textContent=kwf(kw)+' kW';
    V.n.textContent=n===1?'1 aparato encendido':n+' aparatos encendidos';
    V.icpkw.textContent=kwf(S.kw)+' kW';
    V.mar.textContent=kwf(kw*MARGEN)+' kW';
    if(saltado){V.estado.textContent='¡Ha saltado el limitador!';V.estado2.textContent='Con '+kwf(kw)+' kW encendidos y '+kwf(S.kw)+' kW contratados te quedarías sin luz. Apaga algo o sube la potencia.';}
    else if(w){V.estado.textContent='Todo funciona';V.estado2.textContent='Te quedan '+kwf(S.kw-kw)+' kW libres antes de que salte.';}
    else {V.estado.textContent='Todo apagado';V.estado2.textContent='Enciende lo que pueda coincidir en el peor momento del día.';}
    /* recomendación */
    if(!w){V.rec.textContent='–';V.difl.textContent='Comparación anual';V.dif.textContent='Enciende aparatos';V.dif.style.color='';}
    else if(rec===null){V.rec.textContent='> '+kwf(MAX_KW)+' kW';V.difl.textContent='Fuera de la escala';V.dif.textContent='Consulta a tu comercializadora o a un instalador autorizado';V.dif.style.color='var(--ro)';V.dif.style.fontSize='.95rem';}
    else {
      V.dif.style.fontSize='';
      V.rec.textContent=kwf(rec)+' kW';
      var d=anual(S.kw)-anual(rec);
      if(Math.abs(d)<0.005){V.difl.textContent='Tu potencia es la recomendada';V.dif.textContent='Bien ajustada';V.dif.style.color='var(--ve)';}
      else if(d>0){V.difl.textContent='Bajando a '+kwf(rec)+' kW ahorrarías';V.dif.textContent=eur(d)+' € al año';V.dif.style.color='var(--ve)';}
      else {V.difl.textContent='Subir a '+kwf(rec)+' kW te costaría';V.dif.textContent=eur(-d)+' € más al año';V.dif.style.color='var(--am)';}
    }
    /* interruptores */
    qa('.tl3p-br').forEach(function(b){var id=b.getAttribute('data-id'),c=S.sel[id]||0;b.setAttribute('aria-pressed',c>0);});
    qa('[data-x]').forEach(function(b){var c=S.sel[b.getAttribute('data-x')]||0;b.textContent='×'+(c>1?c:1);b.hidden=!c;});
    qa('[data-sit]').forEach(function(b){var s=SITUACIONES[+b.getAttribute('data-sit')].i,ig=true;A.forEach(function(a){if((S.sel[a.id]||0)!==(s[a.id]||0))ig=false;});b.setAttribute('aria-pressed',ig&&!S.otro);});
    /* tabla */
    var t='';POT.forEach(function(p){var dd=anual(p)-anual(S.kw);t+='<tr class="'+(p===rec?'rec ':'')+(p===S.kw?'cur ':'')+(w&&p<kw-1e-9?'corta':'')+'"><td>'+kwf(p)+' kW'+(w&&p<kw-1e-9?' · saltaría':'')+'</td><td>'+eur(anual(p)/12)+' €</td><td>'+eur(anual(p))+' €</td><td>'+(Math.abs(dd)<0.005?'–':(dd>0?'+':'')+eur(dd)+' €')+'</td></tr>';});
    q('[data-tabla]').innerHTML=t;
  }

  function pararDemo(){if(demo){clearTimeout(demo);demo=null;q('[data-acc="demo"]').textContent='Encender uno a uno';}}
  app.addEventListener('click',function(e){
    var b=e.target.closest('button');if(!b||!app.contains(b))return;
    if(b.hasAttribute('data-id')){pararDemo();var id=b.getAttribute('data-id');if(S.sel[id])delete S.sel[id];else S.sel[id]=1;pintar();
      var a=byId[id];msg(S.sel[id]?(saltado?'Al encender '+a.n.toLowerCase()+' ha saltado el limitador.':a.n+' encendido: '+kwf(suma()/1000)+' kW en total.'):a.n+' apagado.');return;}
    if(b.hasAttribute('data-x')){var id2=b.getAttribute('data-x');S.sel[id2]=(S.sel[id2]||1)%3+1;pintar();return;}
    if(b.hasAttribute('data-sit')){pararDemo();var s=SITUACIONES[+b.getAttribute('data-sit')];S.sel={};for(var k in s.i)S.sel[k]=s.i[k];S.otro=0;q('[data-otro]').value='';pintar();msg(s.n+': '+kwf(suma()/1000)+' kW a la vez.'+(saltado?' Con tu potencia, saltaría.':''));return;}
    var acc=b.getAttribute('data-acc');
    if(acc==='reset'){pararDemo();S.sel={};S.otro=0;q('[data-otro]').value='';pintar();msg('Limitador rearmado. Empieza de nuevo.');}
    else if(acc==='demo'){
      if(demo){pararDemo();return;}
      var lista=[];A.forEach(function(a){if(S.sel[a.id])lista.push([a.id,S.sel[a.id]]);});
      if(!lista.length){var s0=SITUACIONES[0].i;for(var k2 in s0)lista.push([k2,s0[k2]]);}
      lista.sort(function(x,y){return byId[x[0]].w-byId[y[0]].w;});
      S.sel={};pintar();b.textContent='Parar';var i=0;
      (function paso(){if(i>=lista.length){pararDemo();msg(saltado?'Con todo encendido a la vez, salta. Repártelo o sube la potencia.':'Todo encendido y no salta: tu potencia aguanta.');return;}
        S.sel[lista[i][0]]=lista[i][1];pintar();msg('Enciendes '+byId[lista[i][0]].n.toLowerCase()+' → '+kwf(suma()/1000)+' kW'+(saltado?'. ¡Saltó!':''));i++;
        if(saltado){pararDemo();return;}
        demo=setTimeout(paso,RM?250:900);})();
    }
    else if(acc==='enlace')compartir();
  });
  sel.addEventListener('change',function(){S.kw=parseFloat(sel.value);pintar();});
  q('[data-otro]').addEventListener('input',function(e){var v=parseFloat(String(e.target.value).replace(',','.'));S.otro=isFinite(v)&&v>0?Math.min(20000,v):0;pintar();});

  function compartir(){
    var o={kw:S.kw,s:S.sel,o:S.otro};var url=location.href.split('#')[0]+'#cuadro='+encodeURIComponent(JSON.stringify(o));
    try{history.replaceState(null,'',url);}catch(e){}
    var ok=function(){msg('Enlace copiado: quien lo abra verá tu cuadro tal cual.');},ko=function(){msg('Copia la dirección de la barra del navegador.');};
    if(navigator.clipboard&&W.isSecureContext)navigator.clipboard.writeText(url).then(ok,ko);else ko();
  }
  (function desdeEnlace(){var m=location.hash.match(/#cuadro=(.+)$/);if(!m)return;try{var o=JSON.parse(decodeURIComponent(m[1]));if(POT.indexOf(+o.kw)>=0)S.kw=+o.kw;S.sel={};for(var k in o.s)if(byId[k])S.sel[k]=Math.min(3,Math.max(1,+o.s[k]||1));S.otro=Math.max(0,Math.min(20000,+o.o||0));sel.value=String(S.kw);if(S.otro)q('[data-otro]').value=S.otro;}catch(e){}})();
  pintar();
})();
