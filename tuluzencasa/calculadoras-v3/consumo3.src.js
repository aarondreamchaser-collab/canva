/* Calculadora de consumo v3 de tuluzencasa.com: «Tu casa en 3D».
   WPCode: fragmento JavaScript nuevo, pie de todo el sitio. Sale sin hacer nada si la página no tiene #tl3-consumo.
   Mismos precios y factores que la calculadora anterior (calculadora.js) y que los artículos. Sin librerías. */
(function(){
  var app=document.getElementById('tl3-consumo'); if(!app||app.getAttribute('data-listo')) return;
  app.setAttribute('data-listo','1');
  var W=window, D=document;
  var RM=W.matchMedia&&W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var IVA=1.21, IMP=1.21*1.0511, POT_DIA=0.09, CONTADOR=0.81, SEM=4.345, MES=30.4;
  var DEF={pu:0.13,pp:0.19,pl:0.12,pv:0.08,kw:4.6};
  var POT=[2.3,3.45,4.6,5.75,6.9,8.05,9.2];
  /* Tramos 2.0TD de lunes a viernes: p punta, l llano, v valle. Fines de semana, todo valle. */
  var TRAMO=[];for(var h0=0;h0<24;h0++)TRAMO.push(h0<8?'v':(h0<10||(h0>=14&&h0<18)||h0>=22)?'l':'p');
  var NTRAMO={p:'Punta',l:'Llano',v:'Valle'};
  /* Hora de inicio por defecto según la franja de la calculadora anterior */
  var INICIO={madrugada:2,manana:9,tarde:15,punta:19,noche:22,todo:-1};

  var BOMBA='una bomba de calor (split inverter)';
/*APARATOS*/

  var SALA={cocina:'Cocina',salon:'Salón',dormitorio:'Dormitorio',bano:'Baño',lavadero:'Lavadero',garaje:'Garaje'};
  var SALA_ORDEN=['cocina','salon','dormitorio','bano','lavadero','garaje'];
  var EN_SALA={hor:'cocina',fre:'cocina',ind:'cocina',vit:'cocina',mic:'cocina',her:'cocina',caf:'cocina',nev:'cocina',con:'cocina',lvv:'cocina',
    ac:'salon',rad:'salon',est:'salon',bdc:'salon',ven:'salon',tv:'salon',vid:'salon',rou:'salon',sby:'salon',led:'salon',hal:'salon',
    man:'dormitorio',pc:'dormitorio',por:'dormitorio',des:'dormitorio',
    ter:'bano',sec:'bano',
    lav:'lavadero',sev:'lavadero',seb:'lavadero',pla:'lavadero',asp:'lavadero',
    car:'garaje'};
  var byId={}; A.forEach(function(a){byId[a.id]=a;a.z=EN_SALA[a.id]||'salon';});

  var PERFILES=[
    {id:'p1',n:'Piso, 1 persona',i:[['nev'],['ter',{h:2}],['ind'],['mic'],['lav',{d:2}],['tv'],['por'],['led'],['rou'],['sby']]},
    {id:'p3',n:'Piso, 3 personas',i:[['nev'],['ter'],['ind'],['hor'],['lav'],['lvv'],['tv'],['led'],['rou'],['sby']]},
    {id:'aero',n:'Con bomba de calor',i:[['nev'],['ter'],['ind'],['hor'],['lav'],['lvv'],['tv'],['led'],['rou'],['sby'],['bdc']]},
    {id:'coche',n:'Con coche eléctrico',i:[['nev'],['ter'],['ind'],['hor'],['lav'],['lvv'],['tv'],['led'],['rou'],['sby'],['car']]}
  ];

  var S={t:'u',pu:DEF.pu,pp:DEF.pp,pl:DEF.pl,pv:DEF.pv,kw:DEF.kw,rl:1,items:[]};
  var sala='todas', abierto=-1, escA=null, factura={kwh:'',dias:''};

  /* ---------- utilidades ---------- */
  function nf(n,a,b){return n.toLocaleString('es-ES',{minimumFractionDigits:a,maximumFractionDigits:b});}
  function eur(n){return nf(n,2,2);}
  function eur0(n){return nf(Math.round(n),0,0);}
  function kwf(n){return nf(n,0,2);}
  function lc(s){return s.charAt(0).toLowerCase()+s.slice(1);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function num(v,def){v=parseFloat(String(v).replace(',','.'));return isFinite(v)?v:def;}
  function hh(x){x=((x%24)+24)%24;var hI=Math.floor(x),m=Math.round((x-hI)*60);if(m===60){hI=(hI+1)%24;m=0;}return hI+':'+(m<10?'0':'')+m;}
  function plazo(m){if(m<1)return 'menos de un mes';if(m<24)return Math.ceil(m)+' meses';return nf(m/12,0,1)+' años';}
  function nuevo(id,o){var a=byId[id];o=o||{};var it={id:id,w:a.w,h:a.h,d:a.d,s:INICIO[a.f],n:1};for(var k in o)it[k]=o[k];if(a.h>=24)it.s=-1;return it;}

  /* ---------- modelo hora a hora ---------- */
  /* Reparto de las horas de uso de un aparato en las 24 h de un día de uso (fracción de cada hora). */
  function horas(it){
    var r=[],i;for(i=0;i<24;i++)r.push(0);
    if(it.s<0||it.h>=24){for(i=0;i<24;i++)r[i]=Math.min(it.h,24)/24;return r;}
    var t=it.s,rest=it.h;
    while(rest>1e-9){var slot=Math.floor(t)%24,dentro=Math.min(1-(t-Math.floor(t)),rest);r[slot]+=dentro;rest-=dentro;t+=dentro;}
    return r;
  }
  function precioHora(hr,st,finde){
    if(st.t!=='h')return st.pu;
    if(finde)return st.pv;
    var tr=TRAMO[hr];return tr==='p'?st.pp:tr==='l'?st.pl:st.pv;
  }
  function factorUso(it){return S.rl?byId[it.id].r:1;}
  function kwhMes(it){return it.w/1000*it.h*factorUso(it)*it.d*SEM*it.n;}
  function precioMedio(it,st){
    var r=horas(it),tot=0,acc=0,i;
    for(i=0;i<24;i++){if(!r[i])continue;tot+=r[i];acc+=r[i]*(5/7*precioHora(i,st,0)+2/7*precioHora(i,st,1));}
    return tot?acc/tot:st.pu;
  }
  function coste(it,st){return kwhMes(it)*precioMedio(it,st||S)*IMP;}
  function potenciaFija(kw){return kw*POT_DIA*MES*IMP+CONTADOR*IVA;}
  /* Potencia que ve el limitador cada hora de un día laborable: suma de potencias nominales encendidas. */
  function curva(items){
    var c=[],i;for(i=0;i<24;i++)c.push(0);
    (items||S.items).forEach(function(it){var r=horas(it);for(var x=0;x<24;x++){if(r[x]>0)c[x]+=it.w*it.n;}});
    return c;
  }
  function picoDe(items){var c=curva(items),mx=0,hm=0;c.forEach(function(v,i){if(v>mx){mx=v;hm=i;}});return {kw:mx/1000,h:hm};}
  function totales(st,items){
    st=st||S;items=items||S.items;
    var costs=items.map(function(it){return coste(it,st);});
    var ene=costs.reduce(function(s,c){return s+c;},0);
    var kwh=items.reduce(function(s,it){return s+kwhMes(it);},0);
    var pot=potenciaFija(st.kw);
    return {costs:costs,ene:ene,kwh:kwh,pot:pot,fac:ene+pot};
  }
  function normalizada(kw){for(var i=0;i<POT.length;i++){if(POT[i]>=kw-1e-9)return POT[i];}return null;}

  /* ---------- asistente de ahorro ---------- */
  function optimizar(){
    var st=S.t==='h'?S:{t:'h',pp:S.pp||DEF.pp,pl:S.pl||DEF.pl,pv:S.pv||DEF.pv,pu:S.pu};
    var items=S.items.map(function(it){var c={};for(var k in it)c[k]=it[k];return c;});
    var cambios=[];
    items.forEach(function(it,j){
      var a=byId[it.id]; if(!a.m||it.h>=24) return;
      function nota(x){var copia=items.slice();copia[j]=x;var over=Math.max(0,picoDe(copia).kw-S.kw);return {c:coste(x,st),o:over,v:over*1000+coste(x,st)};}
      var base=nota(it), mejor=null, mv=base.v;
      for(var s=0;s<24;s++){
        var prueba={};for(var k in it)prueba[k]=it[k];prueba.s=s;
        var n=nota(prueba); if(n.v<mv-0.005){mv=n.v;mejor={s:s,n:n};}
      }
      if(mejor&&(mejor.n.o<base.o-1e-9||mejor.n.c<base.c-0.01)){cambios.push({j:j,de:it.s,a:mejor.s,ah:(base.c-mejor.n.c)*12,pico:mejor.n.o<base.o-1e-9});it.s=mejor.s;}
    });
    var antes=totales(S).fac, despues=totales(st,items).fac;
    return {cambios:cambios,items:items,st:st,antes:antes,despues:despues,ah:(antes-despues)*12,picoAntes:picoDe().kw,picoDespues:picoDe(items).kw};
  }
  function consejos(){
    var out=[]; if(!S.items.length) return out;
    var T=totales(), pk=picoDe(), i;
    if(pk.kw>S.kw){
      var sig=normalizada(pk.kw);
      out.push({c:'aviso',k:'Aviso',t:'Tu limitador puede saltar a las '+hh(pk.h),x:'A esa hora coinciden '+kwf(pk.kw)+' kW y tienes '+kwf(S.kw)+' kW contratados. Separa esos aparatos'+(sig?' o sube a '+kwf(sig)+' kW':'')+'. Puedes moverlos en la línea del día.'});
    } else {
      var rec=normalizada(pk.kw*1.1);
      if(rec&&rec<S.kw){var ahp=(S.kw-rec)*POT_DIA*365*IMP;if(ahp>=8)out.push({c:'ahorro',k:'Ahorro',s:ahp,t:'Te sobra potencia',x:'Tu pico es de '+kwf(pk.kw)+' kW. Con '+kwf(rec)+' kW (pico más un 10 % de margen) seguirías sin cortes.'});}
    }
    var alts=[];
    S.items.forEach(function(it,j){var a=byId[it.id];if(!a.alt)return;var ahm=T.costs[j]*(1-a.alt.k);if(ahm*12<5)return;alts.push({a:a,ah:ahm*12,me:a.alt.c/ahm});});
    alts.sort(function(x,y){return y.ah-x.ah;});
    alts.slice(0,2).forEach(function(o){
      if(o.me<=36) out.push({c:'ahorro',k:'Cambio que compensa',s:o.ah,t:'Sustituye: '+lc(o.a.n),x:'Pasar a '+o.a.alt.n+' cuesta unos '+eur0(o.a.alt.c)+' € y se paga solo en '+plazo(o.me)+'.'+(o.a.alt.nota?' '+o.a.alt.nota:'')});
      else out.push({c:'dato',k:'No compensa',t:'Cambiar '+lc(o.a.n),x:'Ahorrarías unos '+eur0(o.ah)+' € al año, pero tardarías '+plazo(o.me)+' en recuperar los '+eur0(o.a.alt.c)+' € que cuesta.'});
    });
    if(T.ene>0){var im=0;T.costs.forEach(function(c,j){if(c>T.costs[im])im=j;});
      out.push({c:'dato',k:'Dato',t:'Tu mayor gasto: '+lc(byId[S.items[im].id].n),x:'Es el '+Math.round(T.costs[im]/T.ene*100)+' % de lo que pagas por tus aparatos: '+eur(T.costs[im])+' € al mes.'});}
    return out.slice(0,4);
  }

  /* ---------- estilos (solo dentro de .tl3) ---------- */
  if(!D.getElementById('tl3-css')){
    var css=D.createElement('style');css.id='tl3-css';
    css.textContent=[
'.tl3{--n0:#070D18;--n1:#0C1626;--n2:#122036;--n3:#1B2D49;--lin:#2A4166;--tx:#E8F0FA;--tx2:#9DB0C8;--am:#F2C230;--ci:#3BE0FF;--ro:#FF5D6C;--ve:#3DDC97;--r:18px;',
' position:relative;color:var(--tx);background:radial-gradient(1200px 500px at 80% -10%,#1d3a66 0,transparent 60%),radial-gradient(800px 400px at 0% 110%,#2b2350 0,transparent 55%),var(--n0);border-radius:24px;padding:22px;margin:0 0 2em;overflow:hidden;font-size:15px;line-height:1.45;isolation:isolate;box-shadow:0 30px 60px -30px #050a14cc,inset 0 0 0 1px #ffffff10}',
'.tl3::before{content:"";position:absolute;inset:0;background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px);background-size:32px 32px;mask-image:linear-gradient(180deg,#000 0,transparent 70%);-webkit-mask-image:linear-gradient(180deg,#000 0,transparent 70%);pointer-events:none;z-index:-1}',
'.tl3 *{box-sizing:border-box}',
'.tl3 button{font:inherit;cursor:pointer}',
'.tl3 h2,.tl3 h3{color:var(--tx);margin:0;letter-spacing:-.01em}',
'.tl3-cab{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;margin:0 0 16px}',
'.tl3-cab h2{font-size:1.25rem;font-weight:800;display:flex;align-items:center;gap:10px}',
'.tl3-cab h2::before{content:"";width:10px;height:10px;border-radius:50%;background:var(--ve);box-shadow:0 0 0 4px #3ddc9733,0 0 14px var(--ve)}',
'.tl3-perf{display:flex;flex-wrap:wrap;gap:6px}',
'.tl3 .tl3-chip{background:#ffffff0d;border:1px solid var(--lin);color:var(--tx2);border-radius:999px;padding:6px 12px;font-size:.85rem;font-weight:600;transition:all .2s}',
'.tl3 .tl3-chip:hover,.tl3 .tl3-chip[aria-pressed="true"]{color:var(--n0);background:var(--am);border-color:var(--am)}',
'.tl3-hud{display:grid;grid-template-columns:1.3fr 1fr 1fr 1.2fr;gap:12px;margin:0 0 16px}',
'.tl3-c{background:linear-gradient(180deg,#ffffff0f,#ffffff05);border:1px solid #ffffff17;border-radius:var(--r);padding:14px 16px;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);position:relative;overflow:hidden}',
'.tl3-c .tl3-l{display:block;font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--tx2)}',
'.tl3-big{font-size:2.5rem;font-weight:800;line-height:1.05;font-variant-numeric:tabular-nums;color:var(--am);text-shadow:0 0 24px #f2c23055;margin-top:4px}',
'.tl3-big small{font-size:.9rem;color:var(--tx2);font-weight:700;margin-left:6px;text-shadow:none}',
'.tl3-med{font-size:1.5rem;font-weight:800;font-variant-numeric:tabular-nums;margin-top:6px}',
'.tl3-sub{font-size:.8rem;color:var(--tx2);margin-top:2px}',
'.tl3-gauge{height:10px;border-radius:99px;background:#ffffff14;margin-top:10px;position:relative;overflow:visible}',
'.tl3-gauge i{position:absolute;inset:0 auto 0 0;border-radius:99px;background:linear-gradient(90deg,var(--ve),var(--am));transition:width .5s}',
'.tl3-gauge b{position:absolute;top:-4px;bottom:-4px;width:2px;background:#fff;box-shadow:0 0 8px #fff}',
'.tl3-c.is-over .tl3-gauge i{background:linear-gradient(90deg,var(--am),var(--ro))}',
'.tl3-c.is-over .tl3-med{color:var(--ro)}',
'.tl3-main{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:16px;align-items:start}',
'.tl3-casa{position:relative;perspective:1200px}',
'.tl3-casa svg{display:block;width:100%;height:auto;transform-style:preserve-3d;transition:transform .4s ease-out;filter:drop-shadow(0 30px 30px #00000066)}',
'.tl3-sala{cursor:pointer}',
'.tl3-sala .suelo{transition:fill .5s}',
'.tl3-sala:hover .suelo,.tl3-sala.is-sel .suelo{stroke:var(--am);stroke-width:2.5}',
'.tl3-sala text{font:700 13px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;fill:#fff;pointer-events:none}',
'.tl3-sala text.e{font-size:12px;fill:var(--am);font-weight:800}',
'.tl3-cable{fill:none;stroke-width:2;stroke-linecap:round;stroke-dasharray:4 10}',
'.tl3-anim .tl3-cable{animation:tl3-flujo linear infinite}',
'@keyframes tl3-flujo{to{stroke-dashoffset:-56}}',
'.tl3-ley{display:flex;justify-content:center;gap:14px;font-size:.78rem;color:var(--tx2);margin-top:6px;flex-wrap:wrap}',
'.tl3-ley i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}',
'.tl3-pan{background:#0b1524cc;border:1px solid #ffffff17;border-radius:var(--r);padding:14px;min-height:100%}',
'.tl3-tabs{display:flex;gap:4px;background:#ffffff0a;border-radius:12px;padding:4px;margin:0 0 12px}',
'.tl3-tabs button{flex:1;background:none;border:0;color:var(--tx2);font-weight:700;font-size:.88rem;padding:8px 6px;border-radius:9px}',
'.tl3-tabs button[aria-selected="true"]{background:var(--n3);color:#fff;box-shadow:inset 0 0 0 1px #ffffff1f}',
'.tl3-salas{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}',
'.tl3-lista{display:flex;flex-direction:column;gap:6px;max-height:520px;overflow:auto;padding-right:4px;scrollbar-width:thin}',
'.tl3-ap{border:1px solid #ffffff14;border-radius:12px;background:#ffffff06;transition:border-color .2s,background .2s}',
'.tl3-ap.is-on{border-color:#f2c23066;background:#f2c2300d}',
'.tl3-ap-top{display:flex;align-items:center;gap:10px;padding:9px 10px}',
'.tl3 .tl3-sw{flex:none;width:40px;height:22px;border-radius:99px;background:#ffffff1f;border:0;position:relative;padding:0;transition:background .2s}',
'.tl3 .tl3-sw::after{content:"";position:absolute;top:3px;left:3px;width:16px;height:16px;border-radius:50%;background:#fff;transition:transform .2s}',
'.tl3 .tl3-sw[aria-checked="true"]{background:var(--am);box-shadow:0 0 12px #f2c23088}',
'.tl3 .tl3-sw[aria-checked="true"]::after{transform:translateX(18px);background:var(--n0)}',
'.tl3-ap-n{flex:1;min-width:0;font-weight:700;font-size:.92rem;line-height:1.25}',
'.tl3-ap-n small{display:block;color:var(--tx2);font-weight:500;font-size:.78rem}',
'.tl3-ap-c{text-align:right;font-weight:800;font-variant-numeric:tabular-nums;white-space:nowrap}',
'.tl3-ap-c small{display:block;color:var(--tx2);font-weight:600;font-size:.72rem}',
'.tl3 .tl3-ed{background:none;border:1px solid #ffffff26;color:var(--tx2);border-radius:8px;width:30px;height:30px;flex:none;display:grid;place-items:center}',
'.tl3 .tl3-ed[aria-expanded="true"]{color:var(--n0);background:var(--ci);border-color:var(--ci)}',
'.tl3-form{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;padding:0 10px 10px}',
'.tl3-form label{font-size:.72rem;color:var(--tx2);font-weight:700;display:flex;flex-direction:column;gap:3px}',
'.tl3 input[type=number],.tl3 select{width:100%;background:var(--n1);color:#fff;border:1px solid var(--lin);border-radius:8px;padding:7px 8px;font:inherit;font-size:.92rem}',
'.tl3 input:focus-visible,.tl3 select:focus-visible,.tl3 button:focus-visible{outline:2px solid var(--ci);outline-offset:2px}',
'.tl3-hora{grid-column:1/-1}',
'.tl3-hora input[type=range]{width:100%;accent-color:var(--am)}',
'.tl3-mini{display:grid;grid-template-columns:repeat(24,1fr);gap:1px;height:12px;border-radius:4px;overflow:hidden;margin-top:4px}',
'.tl3-mini i{display:block;background:#ffffff10}',
'.tl3-mini i.p{background:#ff5d6c33}.tl3-mini i.l{background:#f2c23033}.tl3-mini i.v{background:#3ddc9733}',
'.tl3-mini i.on{background:var(--ci);box-shadow:0 0 8px var(--ci)}',
'.tl3-f{display:grid;gap:10px}',
'.tl3-f label{font-size:.8rem;color:var(--tx2);font-weight:700;display:flex;flex-direction:column;gap:4px}',
'.tl3-seg{display:flex;background:#ffffff0a;border-radius:10px;padding:3px}',
'.tl3-seg button{flex:1;background:none;border:0;color:var(--tx2);font-weight:700;padding:8px;border-radius:8px}',
'.tl3-seg button[aria-pressed="true"]{background:var(--am);color:var(--n0)}',
'.tl3-row3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}',
'.tl3-chk{flex-direction:row!important;align-items:flex-start;gap:8px!important;color:var(--tx)!important;font-weight:600!important}',
'.tl3-chk input{margin-top:3px;accent-color:var(--am)}',
'.tl3-nota{font-size:.78rem;color:var(--tx2);margin:0}',
'.tl3-dia{margin-top:16px}',
'.tl3-dia-cab{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;align-items:baseline;margin:0 0 8px}',
'.tl3-dia-cab h3{font-size:1.05rem;font-weight:800}',
'.tl3-dia svg{display:block;width:100%;height:auto;touch-action:pan-y}',
'.tl3-dia text{font:600 10px system-ui,-apple-system,sans-serif;fill:var(--tx2)}',
'.tl3-lec{font-size:.85rem;color:var(--tx);min-height:1.4em;font-variant-numeric:tabular-nums}',
'.tl3-ia{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:16px}',
'.tl3-t{border-radius:var(--r);padding:14px 16px;background:#ffffff08;border:1px solid #ffffff17;position:relative}',
'.tl3-t .k{font-size:.68rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}',
'.tl3-t h4{margin:4px 0 6px;font-size:.98rem;line-height:1.25;color:#fff}',
'.tl3-t p{margin:0;font-size:.85rem;color:var(--tx2)}',
'.tl3-t .s{display:block;margin-top:8px;font-weight:800;color:var(--ve)}',
'.tl3-t.aviso{border-color:#ff5d6c66;background:#ff5d6c12}.tl3-t.aviso .k{color:var(--ro)}',
'.tl3-t.ahorro .k{color:var(--ve)}.tl3-t.dato .k{color:var(--ci)}',
'.tl3-opt{grid-column:span 2;background:linear-gradient(135deg,#3be0ff1f,#f2c23014);border-color:#3be0ff55}',
'.tl3-opt .k{color:var(--ci)}',
'.tl3-opt ul{margin:8px 0;padding:0;list-style:none;font-size:.85rem;color:var(--tx)}',
'.tl3-opt li{margin:0 0 3px}',
'.tl3-cmp{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}',
'.tl3-cmp div{background:#ffffff0a;border-radius:10px;padding:8px 10px;font-size:.8rem;color:var(--tx2)}',
'.tl3-cmp strong{display:block;font-size:1.1rem;color:#fff;font-variant-numeric:tabular-nums}',
'.tl3-cmp .gana{outline:2px solid var(--ve);color:var(--ve)}',
'.tl3 .tl3-bt{background:var(--am);color:var(--n0);border:0;border-radius:10px;padding:9px 14px;font-weight:800;box-shadow:0 8px 20px -10px var(--am)}',
'.tl3 .tl3-bt:hover{filter:brightness(1.08)}',
'.tl3 .tl3-bt2{background:#ffffff10;color:var(--tx);border:1px solid #ffffff26;border-radius:10px;padding:8px 12px;font-weight:700}',
'.tl3 .tl3-bt2:hover{border-color:var(--ci);color:#fff}',
'.tl3-pie{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;margin-top:16px;padding-top:14px;border-top:1px solid #ffffff14}',
'.tl3-pie .g{display:flex;flex-wrap:wrap;gap:8px}',
'.tl3-msg{font-size:.85rem;color:var(--ve);min-height:1.2em}',
'.tl3-esc{font-size:.85rem;color:var(--tx2)}',
'.tl3-esc strong{color:#fff}',
'.tl3-num{display:inline-block}',
'.tl3-fac{display:grid;gap:10px}',
'.tl3-fac .res{background:#ffffff0a;border-radius:12px;padding:12px;font-size:.88rem}',
'.tl3-barra2{height:12px;border-radius:99px;background:#ffffff14;overflow:hidden;margin:8px 0 4px;display:flex}',
'.tl3-barra2 i{display:block;height:100%;background:var(--ci)}.tl3-barra2 b{display:block;height:100%;background:var(--ro);opacity:.7}',
'.tl3-vacia{color:var(--tx2);font-size:.9rem;text-align:center;padding:20px}',
'@media (max-width:1024px){.tl3-hud{grid-template-columns:1fr 1fr}.tl3-main{grid-template-columns:1fr}.tl3-ia{grid-template-columns:1fr 1fr}.tl3-lista{max-height:none}}',
'@media (max-width:600px){.tl3-hud>.tl3-c:first-child,.tl3-hud>[data-pico]{grid-column:1/-1}.tl3-casa{margin:0 -10px}.tl3{padding:14px;border-radius:18px;margin-left:-4px;margin-right:-4px}.tl3-big{font-size:2rem}.tl3-med{font-size:1.2rem}.tl3-ia{grid-template-columns:1fr}.tl3-opt{grid-column:auto}.tl3-form{grid-template-columns:1fr 1fr}.tl3-hud{gap:8px}.tl3-c{padding:12px}}',
'@media print{.tl3{background:#fff!important;color:#000;box-shadow:none}.tl3 *{color:#000!important;text-shadow:none!important;box-shadow:none!important}.tl3-casa,.tl3-pie,.tl3-tabs,.tl3-perf,.tl3 .tl3-sw,.tl3 .tl3-ed{display:none!important}.tl3-lista{max-height:none}}'
    ].join('\n');
    D.head.appendChild(css);
  }

  /* ---------- estructura ---------- */
  app.classList.add('tl3');
  app.innerHTML=
   '<div class="tl3-cab"><h2>Tu casa en 3D</h2><div class="tl3-perf" role="group" aria-label="Cargar un hogar tipo"></div></div>'+
   '<div class="tl3-hud" aria-live="polite">'+
     '<div class="tl3-c"><span class="tl3-l">Factura estimada</span><div class="tl3-big"><span data-v="fac">0,00</span><small>€/mes</small></div><div class="tl3-sub">con potencia, impuestos y contador</div></div>'+
     '<div class="tl3-c"><span class="tl3-l">Al año</span><div class="tl3-med"><span data-v="ano">0</span> €</div><div class="tl3-sub"><span data-v="ene">0</span> € son tus aparatos</div></div>'+
     '<div class="tl3-c"><span class="tl3-l">Consumo</span><div class="tl3-med"><span data-v="kwh">0</span> kWh</div><div class="tl3-sub">al mes</div></div>'+
     '<div class="tl3-c" data-pico><span class="tl3-l">Pico a la vez</span><div class="tl3-med"><span data-v="pico">0</span> kW <small style="font-size:.8rem;color:var(--tx2)">de <span data-v="kw">4,6</span></small></div><div class="tl3-gauge"><i style="width:0"></i><b></b></div></div>'+
   '</div>'+
   '<div class="tl3-main">'+
     '<div><div class="tl3-casa"></div><div class="tl3-ley"><span><i style="background:#2b4a75"></i>Poco gasto</span><span><i style="background:#F2C230"></i>Medio</span><span><i style="background:#FF5D6C"></i>Mucho</span><span>Toca una habitación</span></div></div>'+
     '<div class="tl3-pan">'+
       '<div class="tl3-tabs" role="tablist"><button type="button" role="tab" data-tab="ap" aria-selected="true">Aparatos</button><button type="button" role="tab" data-tab="ta" aria-selected="false">Tarifa</button><button type="button" role="tab" data-tab="fa" aria-selected="false">Tu factura</button></div>'+
       '<div data-panel="ap"><div class="tl3-salas" role="group" aria-label="Filtrar por habitación"></div><div class="tl3-lista"></div></div>'+
       '<div data-panel="ta" hidden><div class="tl3-f">'+
         '<div class="tl3-seg" role="group" aria-label="Tipo de tarifa"><button type="button" data-t="u" aria-pressed="true">Precio único</button><button type="button" data-t="h" aria-pressed="false">Por horas (2.0TD)</button></div>'+
         '<label data-box="u">Precio del kWh sin impuestos (€)<input type="number" min="0" step="0.001" inputmode="decimal" data-k="pu"></label>'+
         '<div class="tl3-row3" data-box="h" hidden><label>Punta<input type="number" min="0" step="0.001" inputmode="decimal" data-k="pp"></label><label>Llano<input type="number" min="0" step="0.001" inputmode="decimal" data-k="pl"></label><label>Valle<input type="number" min="0" step="0.001" inputmode="decimal" data-k="pv"></label></div>'+
         '<label>Potencia contratada<select data-k="kw"></select></label>'+
         '<label class="tl3-chk"><input type="checkbox" data-k="rl" checked><span>Consumo realista<br><small class="tl3-nota">Neveras, aires y radiadores funcionan a ciclos: no gastan su potencia máxima todo el rato.</small></span></label>'+
         '<p class="tl3-nota">Precio por defecto: 0,13 €/kWh sin impuestos (0,165 € con impuesto eléctrico del 5,11 % e IVA del 21 %). Tarifa por horas orientativa: punta 0,19, llano 0,12 y valle 0,08 €/kWh. Pon los de tu factura.</p>'+
       '</div></div>'+
       '<div data-panel="fa" hidden><div class="tl3-fac">'+
         '<p class="tl3-nota">Pon el consumo y los días de tu última factura y te decimos cuánto explica tu lista de aparatos.</p>'+
         '<div class="tl3-row3"><label>kWh de la factura<input type="number" min="0" step="1" inputmode="numeric" data-fa="kwh" placeholder="Ej. 250"></label><label>Días facturados<input type="number" min="1" max="62" step="1" inputmode="numeric" data-fa="dias" placeholder="Ej. 30"></label><span></span></div>'+
         '<div class="res" data-fa-res>Rellena los dos datos.</div>'+
       '</div></div>'+
     '</div>'+
   '</div>'+
   '<div class="tl3-dia tl3-c"><div class="tl3-dia-cab"><h3>Tu día, hora a hora</h3><span class="tl3-lec" data-lec>Pasa el dedo o el ratón por la gráfica.</span></div><div data-graf></div>'+
     '<div class="tl3-ley"><span><i style="background:#ff5d6c55"></i>Punta</span><span><i style="background:#f2c23055"></i>Llano</span><span><i style="background:#3ddc9755"></i>Valle</span><span><i style="background:#fff"></i>Tu potencia contratada</span><span><i style="background:transparent;border:1px dashed #9DB0C8"></i>Funciona a ratos</span></div></div>'+
   '<div class="tl3-ia" aria-live="polite"></div>'+
   '<div class="tl3-pie"><div class="g"><button type="button" class="tl3-bt2" data-acc="A">Guardar como escenario A</button><span class="tl3-esc" data-esc></span></div>'+
     '<div class="g"><button type="button" class="tl3-bt2" data-acc="vaciar">Vaciar</button><button type="button" class="tl3-bt2" data-acc="enlace">Copiar enlace</button><button type="button" class="tl3-bt" data-acc="imprimir">Imprimir informe</button></div></div>'+
   '<div class="tl3-msg" role="status"></div>';

  function q(s){return app.querySelector(s);}
  function qa(s){return Array.prototype.slice.call(app.querySelectorAll(s));}
  var V={};qa('[data-v]').forEach(function(e){V[e.getAttribute('data-v')]=e;});

  /* ---------- casa isométrica en SVG ---------- */
  var NS='http://www.w3.org/2000/svg';
  var ISO={x:Math.cos(Math.PI/6),y:Math.sin(Math.PI/6)}, U=100, H=38, OX=205, OY=52;
  function P(x,y,z){return [OX+(x-y)*ISO.x*U,OY+(x+y)*ISO.y*U-(z||0)*U];}
  function pts(a){return a.map(function(p){return p[0].toFixed(1)+','+p[1].toFixed(1);}).join(' ');}
  /* 3 columnas x 2 filas */
  var POS={cocina:[0,0],salon:[1,0],dormitorio:[2,0],bano:[0,1],lavadero:[1,1],garaje:[2,1]};
  var svgCasa;
  function dibujarCasa(){
    var hz=H/U, s='';
    s+='<defs><filter id="tl3-gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'+
       '<linearGradient id="tl3-pared" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a4470"/><stop offset="1" stop-color="#16263f"/></linearGradient></defs>';
    /* losa base */
    s+='<polygon points="'+pts([P(-.12,-.12,-.08),P(3.12,-.12,-.08),P(3.12,2.12,-.08),P(-.12,2.12,-.08)])+'" fill="#0e1a2d" stroke="#2A4166"/>';
    s+='<polygon points="'+pts([P(-.12,2.12,-.08),P(3.12,2.12,-.08),P(3.12,2.12,-.2),P(-.12,2.12,-.2)])+'" fill="#0a1322"/>';
    s+='<polygon points="'+pts([P(3.12,-.12,-.08),P(3.12,2.12,-.08),P(3.12,2.12,-.2),P(3.12,-.12,-.2)])+'" fill="#081020"/>';
    /* contador en la esquina delantera */
    var m=P(3.35,2.35,0);
    s+='<g class="tl3-cont"><rect x="'+(m[0]-16)+'" y="'+(m[1]-30)+'" width="32" height="40" rx="5" fill="#0b1524" stroke="#3BE0FF"/><circle cx="'+m[0]+'" cy="'+(m[1]-12)+'" r="8" fill="none" stroke="#3BE0FF"/><path d="M'+(m[0]+1)+' '+(m[1]-18)+'l-4 7h4l-1 5 5-7h-4z" fill="#F2C230"/><text x="'+m[0]+'" y="'+(m[1]+24)+'" text-anchor="middle" style="font:700 10px system-ui;fill:#9DB0C8">CONTADOR</text></g>';
    s+='<g data-cables></g>';
    SALA_ORDEN.forEach(function(k){
      var x=POS[k][0],y=POS[k][1],g='';
      g+='<polygon class="suelo" points="'+pts([P(x+.04,y+.04),P(x+.96,y+.04),P(x+.96,y+.96),P(x+.04,y+.96)])+'" fill="#1b2d49" stroke="#ffffff22"/>';
      /* paredes traseras solo en la fila de atrás y la columna izquierda */
      if(y===0)g+='<polygon points="'+pts([P(x+.04,y+.04,0),P(x+.96,y+.04,0),P(x+.96,y+.04,hz),P(x+.04,y+.04,hz)])+'" fill="url(#tl3-pared)" opacity=".9"/>';
      if(x===0)g+='<polygon points="'+pts([P(x+.04,y+.04,0),P(x+.04,y+.96,0),P(x+.04,y+.96,hz),P(x+.04,y+.04,hz)])+'" fill="#1a2c49" opacity=".95"/>';
      var c=P(x+.5,y+.5,0);
      g+='<circle class="halo" cx="'+c[0]+'" cy="'+c[1]+'" r="0" fill="#F2C230" opacity=".0" filter="url(#tl3-gl)"/>';
      g+='<text x="'+c[0]+'" y="'+(c[1]-4)+'" text-anchor="middle">'+SALA[k]+'</text><text class="e" x="'+c[0]+'" y="'+(c[1]+12)+'" text-anchor="middle"></text>';
      s+='<g class="tl3-sala" data-sala="'+k+'" tabindex="0" role="button" aria-label="'+SALA[k]+'">'+g+'</g>';
    });
    q('.tl3-casa').innerHTML='<svg viewBox="0 0 515 372" role="img" aria-label="Casa con el gasto de cada habitación">'+s+'</svg>';
    svgCasa=q('.tl3-casa svg');
    if(!RM)app.classList.add('tl3-anim');
  }
  function colorGasto(t){/* 0..1 -> azul, amarillo, rojo */
    function mix(a,b,k){return a.map(function(v,i){return Math.round(v+(b[i]-v)*k);});}
    var c=t<.5?mix([43,74,117],[242,194,48],t*2):mix([242,194,48],[255,93,108],(t-.5)*2);
    return 'rgb('+c.join(',')+')';
  }
  function pintarCasa(T){
    var porSala={};SALA_ORDEN.forEach(function(k){porSala[k]=0;});
    S.items.forEach(function(it,j){porSala[byId[it.id].z]+=T.costs[j];});
    var mx=Math.max.apply(null,SALA_ORDEN.map(function(k){return porSala[k];}).concat([0.01]));
    var cab='', m=P(3.35,2.35,0);
    SALA_ORDEN.forEach(function(k){
      var g=q('[data-sala="'+k+'"]'), v=porSala[k], t=v/mx;
      g.classList.toggle('is-sel',sala===k);
      g.querySelector('.suelo').setAttribute('fill',v>0?colorGasto(t):'#1b2d49');
      var halo=g.querySelector('.halo');halo.setAttribute('r',v>0?(18+t*26).toFixed(0):'0');halo.setAttribute('opacity',v>0?(.15+t*.35).toFixed(2):'0');halo.setAttribute('fill',colorGasto(t));
      g.querySelector('text.e').textContent=v>0?eur(v)+' €/mes':'';
      var claro=v>0&&t>0.22;Array.prototype.forEach.call(g.querySelectorAll('text'),function(tx){tx.style.fill=claro?'#0B1220':'';});
      g.setAttribute('aria-label',SALA[k]+': '+(v>0?eur(v)+' € al mes':'sin aparatos'));
      if(v>0){
        var c=P(POS[k][0]+.5,POS[k][1]+.5,0), mid=[(c[0]+m[0])/2,Math.max(c[1],m[1])+20];
        var dur=(3.2-2.6*t).toFixed(2);
        cab+='<path class="tl3-cable" d="M'+c[0].toFixed(1)+' '+c[1].toFixed(1)+' Q'+mid[0].toFixed(1)+' '+mid[1].toFixed(1)+' '+m[0].toFixed(1)+' '+(m[1]-12).toFixed(1)+'" stroke="'+colorGasto(t)+'" style="animation-duration:'+dur+'s" opacity=".85"/>';
      }
    });
    q('[data-cables]').innerHTML=cab;
  }

  /* ---------- gráfica de 24 h ---------- */
  var GW=720, GH=200, GL=34, GR=10, GT=12, GB=24;
  function dibujarDia(){
    var cw=q('[data-graf]').clientWidth||720; GW=Math.max(300,Math.min(900,Math.round(cw))); GH=GW<520?220:200;
    var c=curva(), mx=Math.max(S.kw*1000*1.15,Math.max.apply(null,c)*1.1,1000), bw=(GW-GL-GR)/24, s='', i;
    function Y(v){return GT+(GH-GT-GB)*(1-v/mx);}
    for(i=0;i<24;i++){var tr=TRAMO[i];s+='<rect x="'+(GL+i*bw).toFixed(1)+'" y="'+GT+'" width="'+bw.toFixed(1)+'" height="'+(GH-GT-GB)+'" fill="'+(tr==='p'?'#ff5d6c':tr==='l'?'#f2c230':'#3ddc97')+'" opacity=".08"/>';}
    for(var k=0;k<=mx/1000;k+=mx>6000?2:1){var y=Y(k*1000);s+='<line x1="'+GL+'" x2="'+(GW-GR)+'" y1="'+y+'" y2="'+y+'" stroke="#ffffff12"/><text x="'+(GL-6)+'" y="'+(y+3)+'" text-anchor="end">'+k+' kW</text>';}
    /* barras apiladas por aparato */
    var base=[];for(i=0;i<24;i++)base.push(0);
    var cols=['#3BE0FF','#F2C230','#9b8cff','#3DDC97','#ff9f5a','#ff5d6c','#5aa9ff','#e07bff'];
    S.items.forEach(function(it,j){
      var r=horas(it), col=cols[j%cols.length];
      var rep=it.s<0&&it.h<24;
      for(i=0;i<24;i++){if(r[i]<=0)continue;var v=it.w*it.n;var y1=Y(base[i]+v),y0=Y(base[i]);
        s+='<rect x="'+(GL+i*bw+1).toFixed(1)+'" y="'+y1.toFixed(1)+'" width="'+(bw-2).toFixed(1)+'" height="'+Math.max(0.5,y0-y1).toFixed(1)+'" rx="2" fill="'+col+'" opacity="'+(rep?.16:(.35+.6*Math.min(1,r[i]))).toFixed(2)+'"'+(rep?' stroke="'+col+'" stroke-dasharray="3 3" stroke-opacity=".7"':'')+'><title>'+esc(byId[it.id].n)+(rep?': funciona a ratos durante el día; puede coincidir con otros':'')+'</title></rect>';
        base[i]+=v;}
    });
    var yk=Y(S.kw*1000);
    s+='<line x1="'+GL+'" x2="'+(GW-GR)+'" y1="'+yk+'" y2="'+yk+'" stroke="#fff" stroke-dasharray="6 4" stroke-width="1.5"/><text x="'+(GW-GR)+'" y="'+(yk-5)+'" text-anchor="end" style="fill:#fff">'+kwf(S.kw)+' kW contratados</text>';
    for(i=0;i<24;i+=(GW<520?6:3))s+='<text x="'+(GL+i*bw+bw/2)+'" y="'+(GH-8)+'" text-anchor="middle">'+i+' h</text>';
    for(i=0;i<24;i++)if(c[i]>S.kw*1000)s+='<circle cx="'+(GL+i*bw+bw/2)+'" cy="'+(Y(c[i])-8)+'" r="4" fill="#FF5D6C"><title>Aquí puede saltar el limitador</title></circle>';
    s+='<rect data-cursor x="0" y="'+GT+'" width="'+bw.toFixed(1)+'" height="'+(GH-GT-GB)+'" fill="#ffffff" opacity="0"/>';
    q('[data-graf]').innerHTML='<svg viewBox="0 0 '+GW+' '+GH+'" role="img" aria-label="Potencia encendida a lo largo del día">'+s+'</svg>';
    var svg=q('[data-graf] svg'), cur=svg.querySelector('[data-cursor]');
    function leer(ev){
      var r=svg.getBoundingClientRect(), x=(ev.clientX-r.left)/r.width*GW, hI=Math.floor((x-GL)/bw);
      if(hI<0||hI>23)return;
      cur.setAttribute('x',(GL+hI*bw).toFixed(1));cur.setAttribute('opacity','.08');
      var on=S.items.filter(function(it){return horas(it)[hI]>0;}).map(function(it){return byId[it.id].n;});
      var pr=S.t==='h'?precioHora(hI,S,0):S.pu;
      q('[data-lec]').textContent=hI+':00–'+(hI+1)+':00 · '+NTRAMO[TRAMO[hI]]+' ('+nf(pr*IMP,3,3)+' €/kWh con impuestos) · '+kwf(c[hI]/1000)+' kW'+(on.length?' · '+on.slice(0,3).join(', ')+(on.length>3?' y '+(on.length-3)+' más':''):'');
    }
    svg.addEventListener('pointermove',leer);svg.addEventListener('pointerdown',leer);
    svg.addEventListener('pointerleave',function(){cur.setAttribute('opacity','0');});
  }

  /* ---------- lista de aparatos ---------- */
  function idxDe(id){for(var i=0;i<S.items.length;i++)if(S.items[i].id===id)return i;return -1;}
  function pintarSalas(){
    var b='<button type="button" class="tl3-chip" data-s="todas" aria-pressed="'+(sala==='todas')+'">Todas</button><button type="button" class="tl3-chip" data-s="mias" aria-pressed="'+(sala==='mias')+'">Las mías ('+S.items.length+')</button>';
    SALA_ORDEN.forEach(function(k){b+='<button type="button" class="tl3-chip" data-s="'+k+'" aria-pressed="'+(sala===k)+'">'+SALA[k]+'</button>';});
    q('.tl3-salas').innerHTML=b;
  }
  function pintarLista(T){
    var html='', lista=A.filter(function(a){return sala==='todas'||(sala==='mias'?idxDe(a.id)>=0:a.z===sala);});
    if(!lista.length)html='<p class="tl3-vacia">Todavía no has encendido ningún aparato. Elige un hogar tipo arriba o activa los tuyos.</p>';
    lista.forEach(function(a){
      var j=idxDe(a.id), on=j>=0, it=on?S.items[j]:nuevo(a.id), c=on?T.costs[j]:coste(it,S);
      html+='<div class="tl3-ap'+(on?' is-on':'')+'" data-id="'+a.id+'"><div class="tl3-ap-top">'+
        '<button type="button" class="tl3-sw" role="switch" aria-checked="'+on+'" aria-label="'+esc(a.n)+'" data-sw></button>'+
        '<div class="tl3-ap-n">'+esc(a.n)+'<small>'+nf(it.w,0,0)+' W'+(it.n>1?' ×'+it.n:'')+' · '+nf(it.h,0,2)+' h/día · '+it.d+' d/sem'+(it.h<24?' · '+(it.s<0?'repartido':'desde '+hh(it.s)):'')+'</small></div>'+
        '<div class="tl3-ap-c">'+eur(c)+' €<small>'+(on?'al mes':'si lo activas')+'</small></div>'+
        (on?'<button type="button" class="tl3-ed" data-ed aria-expanded="'+(abierto===j)+'" aria-label="Ajustar '+esc(a.n)+'"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/></svg></button>':'')+
        '</div>';
      if(on&&abierto===j){
        var r=horas(it), mini='';for(var x=0;x<24;x++)mini+='<i class="'+TRAMO[x]+(r[x]>0?' on':'')+'"></i>';
        html+='<div class="tl3-form">'+
          '<label>Potencia (W)<input type="number" min="1" step="1" data-f="w" value="'+it.w+'"></label>'+
          '<label>Horas/día<input type="number" min="0.05" max="24" step="0.05" data-f="h" value="'+it.h+'"></label>'+
          '<label>Días/semana<input type="number" min="1" max="7" step="1" data-f="d" value="'+it.d+'"></label>'+
          '<label>Cuántos<input type="number" min="1" max="9" step="1" data-f="n" value="'+it.n+'"></label>'+
          (it.h<24?'<label class="tl3-hora">Empieza a las <strong data-hlab>'+(it.s<0?'(repartido en el día)':hh(it.s))+'</strong><input type="range" min="-1" max="23.5" step="0.5" data-f="s" value="'+it.s+'" aria-label="Hora de inicio"><span class="tl3-mini">'+mini+'</span></label>':'')+
          '</div>';
      }
      html+='</div>';
    });
    q('.tl3-lista').innerHTML=html;
  }

  /* ---------- asistente ---------- */
  var ultimaOpt=null;
  function pintarIA(){
    var box=q('.tl3-ia'), html='';
    if(!S.items.length){box.innerHTML='';return;}
    var o=optimizar(); ultimaOpt=o;
    var uni=totales({t:'u',pu:S.pu,kw:S.kw}).fac, hor=totales({t:'h',pp:S.pp,pl:S.pl,pv:S.pv,kw:S.kw}).fac;
    html+='<div class="tl3-t tl3-opt"><span class="k">Asistente de ahorro</span>';
    var bajaPico=o.picoDespues<o.picoAntes-1e-9&&o.picoAntes>S.kw;
    if(o.cambios.length&&(o.ah>=1||bajaPico)){
      html+='<h4>'+(bajaPico?'Reparte '+o.cambios.length+(o.cambios.length>1?' aparatos':' aparato')+' para que no salte el limitador':'Mueve '+o.cambios.length+(o.cambios.length>1?' aparatos':' aparato')+' a horas más baratas'+(S.t==='h'?'':' con una tarifa por horas'))+'</h4><ul>'+
        o.cambios.map(function(c){var it=S.items[c.j];return '<li>'+esc(byId[it.id].n)+': de '+(c.de<0?'repartido':hh(c.de))+' a <strong>'+hh(c.a)+'</strong></li>';}).join('')+
        '</ul><p>'+(bajaPico?'El pico baja de '+kwf(o.picoAntes)+' a '+kwf(o.picoDespues)+' kW'+(o.picoDespues>S.kw?' (aún por encima de tus '+kwf(S.kw)+' kW)':'')+'.':'Sin pasar de tu potencia contratada.')+(o.ah>=1?' <span class="s">≈ '+eur0(o.ah)+' € menos al año</span>':o.ah<=-1?' <span class="s" style="color:var(--am)">Cuesta unos '+eur0(-o.ah)+' € más al año</span>':'')+'</p><p style="margin-top:8px"><button type="button" class="tl3-bt" data-acc="optimizar">Aplicar horarios'+(S.t==='h'?'':' y tarifa por horas')+'</button></p>';
    } else html+='<h4>Tus horarios ya están bien</h4><p>No hay ningún aparato programable que ahorre moviéndolo de hora sin pasarte de potencia.</p>';
    html+='<div class="tl3-cmp"><div class="'+(uni<=hor?'gana':'')+'">Precio único<strong>'+eur(uni)+' €/mes</strong></div><div class="'+(hor<uni?'gana':'')+'">Por horas<strong>'+eur(hor)+' €/mes</strong></div></div></div>';
    consejos().slice(0,2).forEach(function(t){
      html+='<div class="tl3-t '+t.c+'"><span class="k">'+t.k+'</span><h4>'+esc(t.t)+'</h4><p>'+esc(t.x)+'</p>'+(t.s?'<span class="s">≈ '+eur0(t.s)+' € menos al año</span>':'')+'</div>';
    });
    box.innerHTML=html;
  }

  /* ---------- tu factura ---------- */
  function pintarFactura(T){
    var k=num(factura.kwh,0), d=num(factura.dias,0), box=q('[data-fa-res]');
    if(!(k>0&&d>0)){box.textContent='Rellena los dos datos.';return;}
    var real=k/d*MES, est=T.kwh, pct=Math.min(100,est/real*100);
    var txt=est<=real?
      'Tu lista explica el <strong>'+Math.round(est/real*100)+' %</strong> de tu consumo real ('+nf(est,0,0)+' de '+nf(real,0,0)+' kWh al mes). Faltan <strong>'+nf(real-est,0,0)+' kWh</strong>: aparatos que no has puesto, más horas de uso o consumo en espera.':
      'Tu lista suma <strong>'+nf(est-real,0,0)+' kWh más</strong> de lo que marca tu factura ('+nf(real,0,0)+' kWh al mes). Probablemente usas algunos aparatos menos horas de las que has puesto.';
    box.innerHTML='<div class="tl3-barra2"><i style="width:'+(est<=real?pct:100*real/est).toFixed(1)+'%"></i>'+(est<=real?'<b style="width:'+(100-pct).toFixed(1)+'%"></b>':'')+'</div>'+txt;
  }

  /* ---------- pintar todo ---------- */
  var animar={};
  function contar(el,a,b,fmt){
    if(RM||!W.requestAnimationFrame||a===b){el.textContent=fmt(b);return;}
    var t0=null;cancelAnimationFrame(animar[el.getAttribute('data-v')]);
    function paso(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/450),e=1-Math.pow(1-k,3);el.textContent=fmt(a+(b-a)*e);if(k<1)animar[el.getAttribute('data-v')]=requestAnimationFrame(paso);}
    animar[el.getAttribute('data-v')]=requestAnimationFrame(paso);
  }
  var prev={fac:0,ano:0,ene:0,kwh:0,pico:0};
  function render(){
    var T=totales(), pk=picoDe();
    contar(V.fac,prev.fac,T.fac,eur);contar(V.ano,prev.ano,T.fac*12,eur0);contar(V.ene,prev.ene,T.ene*12,eur0);contar(V.kwh,prev.kwh,T.kwh,function(v){return nf(v,0,0);});contar(V.pico,prev.pico,pk.kw,kwf);
    prev={fac:T.fac,ano:T.fac*12,ene:T.ene*12,kwh:T.kwh,pico:pk.kw};
    V.kw.textContent=kwf(S.kw);
    var pc=q('[data-pico]'), esc2=Math.max(pk.kw,S.kw)*1.15;
    pc.classList.toggle('is-over',pk.kw>S.kw);
    pc.querySelector('.tl3-gauge i').style.width=Math.min(100,pk.kw/esc2*100)+'%';
    pc.querySelector('.tl3-gauge b').style.left='calc('+(S.kw/esc2*100)+'% - 1px)';
    pintarCasa(T);pintarSalas();pintarLista(T);dibujarDia();pintarIA();pintarFactura(T);pintarEsc(T);
  }
  function pintarEsc(T){
    var e=q('[data-esc]');
    if(!escA){e.textContent='Guarda tu casa como A, cambia lo que quieras y compara.';return;}
    var dif=T.fac-escA.fac;
    e.innerHTML='Escenario A: <strong>'+eur(escA.fac)+' €/mes</strong> · ahora: <strong>'+eur(T.fac)+' €/mes</strong> · diferencia: <strong style="color:'+(dif<=0?'var(--ve)':'var(--ro)')+'">'+(dif>0?'+':'')+eur(dif*12)+' € al año</strong> <button type="button" class="tl3-bt2" data-acc="volverA" style="padding:4px 10px;margin-left:6px">Volver a A</button>';
  }

  /* ---------- tarifa ---------- */
  function sync(){
    qa('[data-k]').forEach(function(i){var k=i.getAttribute('data-k');if(k==='rl')i.checked=!!S.rl;else i.value=String(S[k]);});
    qa('[data-t]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-t')===S.t);});
    q('[data-box="u"]').hidden=S.t==='h';q('[data-box="h"]').hidden=S.t!=='h';
  }
  var selKw=q('select[data-k="kw"]');POT.forEach(function(p){selKw.add(new Option(kwf(p)+' kW',String(p)));});

  /* ---------- eventos ---------- */
  var msgT;
  function msg(t){var m=q('.tl3-msg');m.textContent=t;clearTimeout(msgT);msgT=setTimeout(function(){m.textContent='';},4000);}
  function perfil(p){S.items=p.i.map(function(x){return nuevo(x[0],x[1]);});abierto=-1;sala='mias';}
  var pf=q('.tl3-perf');
  PERFILES.forEach(function(p){var b=D.createElement('button');b.type='button';b.className='tl3-chip';b.textContent=p.n;b.addEventListener('click',function(){perfil(p);render();msg('Cargado: '+p.n.toLowerCase()+'. Cambia lo que no encaje con tu casa.');});pf.appendChild(b);});

  app.addEventListener('click',function(e){
    var t=e.target.closest('button,[data-sala]');if(!t||!app.contains(t))return;
    if(t.hasAttribute('data-sala')){var k=t.getAttribute('data-sala');sala=sala===k?'todas':k;abierto=-1;selTab('ap');render();return;}
    if(t.hasAttribute('data-s')){sala=t.getAttribute('data-s');abierto=-1;render();return;}
    if(t.hasAttribute('data-tab')){selTab(t.getAttribute('data-tab'));return;}
    if(t.hasAttribute('data-t')){S.t=t.getAttribute('data-t');sync();render();return;}
    var ap=t.closest('.tl3-ap');
    if(ap&&t.hasAttribute('data-sw')){
      var id=ap.getAttribute('data-id'),j=idxDe(id);
      if(j>=0){S.items.splice(j,1);if(abierto===j)abierto=-1;else if(abierto>j)abierto--;msg(byId[id].n+' apagado.');}
      else{S.items.push(nuevo(id));msg(byId[id].n+' encendido.');}
      render();var b=q('.tl3-ap[data-id="'+id+'"] [data-sw]');if(b)b.focus();return;
    }
    if(ap&&t.hasAttribute('data-ed')){var j2=idxDe(ap.getAttribute('data-id'));abierto=abierto===j2?-1:j2;render();var b2=q('.tl3-ap[data-id="'+ap.getAttribute('data-id')+'"] [data-ed]');if(b2)b2.focus();return;}
    var acc=t.getAttribute('data-acc');
    if(acc==='optimizar'&&ultimaOpt){var n=ultimaOpt.cambios.length,ah=ultimaOpt.ah;S.items=ultimaOpt.items;if(S.t!=='h'){S.t='h';S.pp=ultimaOpt.st.pp;S.pl=ultimaOpt.st.pl;S.pv=ultimaOpt.st.pv;}sync();render();msg('Horarios aplicados a '+n+(n>1?' aparatos':' aparato')+': ≈ '+eur0(ah)+' € menos al año.');}
    else if(acc==='vaciar'){S.items=[];abierto=-1;render();msg('Casa vacía. Enciende tus aparatos.');}
    else if(acc==='A'){escA={fac:totales().fac,S:JSON.parse(JSON.stringify(S))};render();msg('Guardado como escenario A. Ahora cambia lo que quieras.');}
    else if(acc==='volverA'&&escA){var g=JSON.parse(JSON.stringify(escA.S));for(var kk in g)S[kk]=g[kk];abierto=-1;sync();render();msg('Has vuelto al escenario A.');}
    else if(acc==='enlace')compartir();
    else if(acc==='imprimir')W.print();
  });
  app.addEventListener('keydown',function(e){var g=e.target.closest&&e.target.closest('[data-sala]');if(g&&(e.key==='Enter'||e.key===' ')){e.preventDefault();g.dispatchEvent(new MouseEvent('click',{bubbles:true}));}});
  function selTab(k){qa('[data-tab]').forEach(function(b){b.setAttribute('aria-selected',b.getAttribute('data-tab')===k);});qa('[data-panel]').forEach(function(p){p.hidden=p.getAttribute('data-panel')!==k;});}
  app.addEventListener('input',function(e){
    var i=e.target;
    if(i.hasAttribute('data-k')){var k=i.getAttribute('data-k');if(k==='kw')S.kw=parseFloat(i.value);else if(k==='rl')S.rl=i.checked?1:0;else S[k]=Math.max(0,num(i.value,0));render();return;}
    if(i.hasAttribute('data-fa')){factura[i.getAttribute('data-fa')]=i.value;pintarFactura(totales());return;}
    if(i.hasAttribute('data-f')){
      var ap=i.closest('.tl3-ap'),j=idxDe(ap.getAttribute('data-id')),it=S.items[j],f=i.getAttribute('data-f'),v=num(i.value,NaN);
      if(!isFinite(v))return;
      if(f==='w')it.w=Math.max(1,v);else if(f==='h')it.h=Math.min(24,Math.max(0.05,v));else if(f==='d')it.d=Math.min(7,Math.max(1,Math.round(v)));else if(f==='n')it.n=Math.min(9,Math.max(1,Math.round(v)));else if(f==='s')it.s=v<0?-1:v;
      if(f==='s'){/* repintado ligero mientras se arrastra */
        var lab=ap.querySelector('[data-hlab]');if(lab)lab.textContent=it.s<0?'(repartido en el día)':hh(it.s);
        var r=horas(it);Array.prototype.forEach.call(ap.querySelectorAll('.tl3-mini i'),function(m,x){m.classList.toggle('on',r[x]>0);});
        clearTimeout(i._t);i._t=setTimeout(function(){render();var n2=q('.tl3-ap[data-id="'+ap.getAttribute('data-id')+'"] [data-f="s"]');if(n2)n2.focus();},120);
        return;
      }
      clearTimeout(i._t);i._t=setTimeout(function(){var foco=f;render();var n3=q('.tl3-ap[data-id="'+ap.getAttribute('data-id')+'"] [data-f="'+foco+'"]');if(n3){n3.focus();try{var L=n3.value.length;n3.setSelectionRange&&n3.type==='text'&&n3.setSelectionRange(L,L);}catch(x){}}},350);
    }
  });
  app.addEventListener('change',function(e){if(e.target.hasAttribute('data-k')&&e.target.tagName==='SELECT'){S.kw=parseFloat(e.target.value);render();}});

  /* Inclinación 3D de la casa con el ratón (no en táctil ni con «reducir movimiento») */
  if(!RM&&W.matchMedia&&W.matchMedia('(hover:hover) and (pointer:fine)').matches){
    var casa=q('.tl3-casa');
    casa.addEventListener('pointermove',function(e){var r=casa.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;svgCasa.style.transform='rotateX('+(-y*8).toFixed(2)+'deg) rotateY('+(x*10).toFixed(2)+'deg)';});
    casa.addEventListener('pointerleave',function(){svgCasa.style.transform='';});
  }

  /* ---------- compartir ---------- */
  function copiar(txt,ok,ko){
    if(navigator.clipboard&&W.isSecureContext){navigator.clipboard.writeText(txt).then(ok,function(){viejo();});}else viejo();
    function viejo(){try{var ta=D.createElement('textarea');ta.value=txt;ta.style.position='fixed';ta.style.opacity='0';D.body.appendChild(ta);ta.select();var r=D.execCommand('copy');D.body.removeChild(ta);r?ok():ko();}catch(e){ko();}}
  }
  function compartir(){
    var o={v:3,t:S.t,pu:S.pu,pp:S.pp,pl:S.pl,pv:S.pv,kw:S.kw,rl:S.rl,i:S.items.map(function(it){return [it.id,it.w,it.h,it.d,it.s,it.n];})};
    var url=location.href.split('#')[0]+'#casa='+encodeURIComponent(JSON.stringify(o));
    try{history.replaceState(null,'',url);}catch(e){}
    copiar(url,function(){msg('Enlace copiado: quien lo abra verá tu casa tal cual.');},function(){msg('No se pudo copiar. Copia la dirección de la barra del navegador.');});
  }
  function desdeEnlace(){
    var m=location.hash.match(/#casa=(.+)$/), viejo=location.hash.match(/#calc=(.+)$/);
    try{
      if(m){var o=JSON.parse(decodeURIComponent(m[1]));
        S.t=o.t==='h'?'h':'u';['pu','pp','pl','pv'].forEach(function(k){if(isFinite(o[k]))S[k]=Math.max(0,+o[k]);});
        if(POT.indexOf(+o.kw)>=0)S.kw=+o.kw;S.rl=o.rl?1:0;
        S.items=(o.i||[]).filter(function(x){return byId[x[0]];}).map(function(x){return {id:x[0],w:Math.max(1,+x[1]||1),h:Math.min(24,Math.max(0.05,+x[2]||1)),d:Math.min(7,Math.max(1,+x[3]||7)),s:(+x[4]>=0&&+x[4]<24)?+x[4]:-1,n:Math.min(9,Math.max(1,+x[5]||1))};});
        return true;}
      if(viejo){/* enlaces de la calculadora anterior */
        var o2=JSON.parse(decodeURIComponent(viejo[1]));S.t=o2.t==='h'?'h':'u';['pu','pp','pl','pv'].forEach(function(k){if(isFinite(o2[k]))S[k]=+o2[k];});
        if(POT.indexOf(+o2.kw)>=0)S.kw=+o2.kw;S.rl=o2.rl?1:0;
        S.items=(o2.i||[]).filter(function(x){return byId[x[0]];}).map(function(x){var it=nuevo(x[0],{w:+x[1]||1,h:Math.min(24,+x[2]||1),d:Math.min(7,Math.max(1,+x[3]||7))});if(INICIO[x[4]]!==undefined&&it.h<24)it.s=INICIO[x[4]];return it;});
        return true;}
    }catch(e){}
    return false;
  }

  var anchoG=0;W.addEventListener('resize',function(){var c=q('[data-graf]').clientWidth;if(Math.abs(c-anchoG)>40){anchoG=c;dibujarDia();}},{passive:true});
  dibujarCasa();
  if(!desdeEnlace())perfil(PERFILES[1]);
  sala=S.items.length?'mias':'todas';
  sync();render();
})();
