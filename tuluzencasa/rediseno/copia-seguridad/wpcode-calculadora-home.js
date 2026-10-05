/* Calculadora de la home de tuluzencasa.com. Se carga en el pie con WPCode; sale sin hacer nada si la página no tiene #tlc-app. */
(function(){
  var app=document.getElementById('tlc-app'); if(!app) return;
  var IVA=1.21, IMP=1.21*1.0511, POT_DIA=0.09, CONTADOR=0.81, SEM=4.345, MES=30.4;
  var DEF={pu:0.13,pp:0.19,pl:0.12,pv:0.08,kw:4.6};
  var POT=[2.3,3.45,4.6,5.75,6.9,8.05,9.2];
  var FR={
    madrugada:{n:'Madrugada (0–8 h)',c:'de madrugada',h:[0,8],p:0,l:0,v:1},
    manana:{n:'Mañana (8–14 h)',c:'por la mañana',h:[8,14],p:4/6,l:2/6,v:0},
    tarde:{n:'Tarde (14–18 h)',c:'por la tarde',h:[14,18],p:0,l:1,v:0},
    punta:{n:'Tarde-noche (18–22 h)',c:'de 18 a 22 h',h:[18,22],p:1,l:0,v:0},
    noche:{n:'Noche (22–24 h)',c:'por la noche',h:[22,24],p:0,l:1,v:0},
    todo:{n:'Todo el día',c:'todo el día',h:[0,24],p:1/3,l:1/3,v:1/3}
  };
  var FR_ORDEN=['madrugada','manana','tarde','punta','noche','todo'];
  var GRUPOS=['Climatización','Agua caliente','Cocina','Lavado','Ocio y oficina','Iluminación','Movilidad','Otros'];
  var BOMBA='una bomba de calor (split inverter)';
  var A=[
    {id:'ac',g:'Climatización',n:'Aire acondicionado 3.000 frigorías',w:1000,h:6,d:7,f:'tarde',r:0.6},
    {id:'rad',g:'Climatización',n:'Radiador de aceite 2.000 W',w:2000,h:4,d:7,f:'punta',r:0.6,alt:{n:BOMBA,k:0.35,c:700}},
    {id:'est',g:'Climatización',n:'Estufa o calefactor 2.000 W',w:2000,h:3,d:7,f:'punta',r:0.85,alt:{n:BOMBA,k:0.3,c:700}},
    {id:'bdc',g:'Climatización',n:'Bomba de calor (calefacción)',w:900,h:6,d:7,f:'punta',r:0.7},
    {id:'des',g:'Climatización',n:'Deshumidificador',w:250,h:8,d:7,f:'todo',r:0.8},
    {id:'ven',g:'Climatización',n:'Ventilador',w:50,h:8,d:7,f:'tarde',r:1},
    {id:'man',g:'Climatización',n:'Manta eléctrica',w:100,h:8,d:7,f:'madrugada',r:0.5},
    {id:'ter',g:'Agua caliente',n:'Termo eléctrico 80 L',s:'el termo',w:1500,h:3,d:7,f:'todo',r:0.7,m:1},
    {id:'hor',g:'Cocina',n:'Horno eléctrico',w:2200,h:0.75,d:4,f:'punta',r:0.6,alt:{n:'una freidora de aire (para raciones pequeñas)',k:0.5,c:90}},
    {id:'fre',g:'Cocina',n:'Freidora de aire',w:1500,h:0.33,d:5,f:'punta',r:0.7},
    {id:'ind',g:'Cocina',n:'Placa de inducción (un fuego)',w:1800,h:1,d:7,f:'manana',r:0.7},
    {id:'vit',g:'Cocina',n:'Vitrocerámica (un fuego)',w:1800,h:1,d:7,f:'manana',r:0.75,alt:{n:'una placa de inducción',k:0.75,c:400}},
    {id:'mic',g:'Cocina',n:'Microondas',w:1000,h:0.25,d:7,f:'manana',r:1},
    {id:'her',g:'Cocina',n:'Hervidor de agua',w:2000,h:0.1,d:7,f:'manana',r:1},
    {id:'caf',g:'Cocina',n:'Cafetera',w:1000,h:0.15,d:7,f:'manana',r:1},
    {id:'nev',g:'Cocina',n:'Nevera combi',w:150,h:24,d:7,f:'todo',r:0.2,alt:{n:'una nevera nueva de clase A o B',k:0.5,c:650,nota:'Solo si la tuya tiene más de 12 años.'}},
    {id:'con',g:'Cocina',n:'Congelador vertical',w:150,h:24,d:7,f:'todo',r:0.2},
    {id:'lav',g:'Lavado',n:'Lavadora (lavado a 40 °C)',s:'la lavadora',w:800,h:1,d:4,f:'manana',r:1,m:1},
    {id:'sev',g:'Lavado',n:'Secadora de evacuación',s:'la secadora',w:2500,h:1,d:3,f:'tarde',r:0.8,m:1,alt:{n:'una secadora con bomba de calor',k:0.45,c:550}},
    {id:'seb',g:'Lavado',n:'Secadora con bomba de calor',s:'la secadora',w:900,h:1.5,d:3,f:'tarde',r:0.8,m:1},
    {id:'lvv',g:'Lavado',n:'Lavavajillas (programa eco)',s:'el lavavajillas',w:1200,h:1.5,d:5,f:'punta',r:0.55,m:1},
    {id:'pla',g:'Lavado',n:'Plancha',w:2200,h:0.5,d:2,f:'tarde',r:0.5},
    {id:'tv',g:'Ocio y oficina',n:'Televisión de 55 pulgadas',w:100,h:4,d:7,f:'punta',r:1},
    {id:'pc',g:'Ocio y oficina',n:'Ordenador gaming',w:400,h:4,d:7,f:'tarde',r:0.7},
    {id:'por',g:'Ocio y oficina',n:'Portátil',w:60,h:6,d:5,f:'manana',r:0.7},
    {id:'vid',g:'Ocio y oficina',n:'Videoconsola',w:150,h:2,d:7,f:'punta',r:1},
    {id:'rou',g:'Ocio y oficina',n:'Router wifi',w:10,h:24,d:7,f:'todo',r:1},
    {id:'sby',g:'Ocio y oficina',n:'Aparatos en espera (standby)',w:15,h:24,d:7,f:'todo',r:1,alt:{n:'regletas con interruptor',k:0.3,c:25}},
    {id:'led',g:'Iluminación',n:'Iluminación LED (10 bombillas)',w:90,h:5,d:7,f:'punta',r:1},
    {id:'hal',g:'Iluminación',n:'Iluminación halógena (10 bombillas)',w:500,h:5,d:7,f:'punta',r:1,alt:{n:'bombillas LED equivalentes',k:0.15,c:40}},
    {id:'car',g:'Movilidad',n:'Cargador de coche eléctrico 7,4 kW',s:'la carga del coche',w:7400,h:2,d:5,f:'madrugada',r:1,m:1},
    {id:'asp',g:'Otros',n:'Aspiradora',w:800,h:0.5,d:3,f:'manana',r:1},
    {id:'sec',g:'Otros',n:'Secador de pelo',w:1800,h:0.2,d:7,f:'manana',r:1}
  ];
  var byId={}; A.forEach(function(a){byId[a.id]=a;});
  var EJEMPLO=['nev','ter','ind','hor','lav','lvv','tv','led','rou','sby'];

  var S={t:'u',pu:DEF.pu,pp:DEF.pp,pl:DEF.pl,pv:DEF.pv,kw:DEF.kw,rl:1,items:[]};
  var editIdx=-1, nuevoIdx=-1;
  function $(id){return document.getElementById(id);}
  var el={ap:$('tlc-ap'),fr:$('tlc-fr'),w:$('tlc-w'),h:$('tlc-h'),d:$('tlc-d'),add:$('tlc-add'),cancel:$('tlc-cancel'),lista:$('tlc-lista'),vacio:$('tlc-vacio'),tips:$('tlc-tips'),msg:$('tlc-msg'),
    pu:$('tlc-pu'),pp:$('tlc-pp'),pl:$('tlc-pl'),pv:$('tlc-pv'),kw:$('tlc-kw'),rl:$('tlc-rl'),tu:$('tlc-t-u'),th:$('tlc-t-h'),boxU:$('tlc-box-u'),boxH:$('tlc-box-h')};

  function nf(n,min,max){return n.toLocaleString('es-ES',{minimumFractionDigits:min,maximumFractionDigits:max});}
  function eur(n){return nf(n,2,2);}
  function eur0(n){return nf(Math.round(n),0,0);}
  function kwf(n){return nf(n,0,2);}
  function num(input,def){var v=parseFloat(String(input.value).replace(',','.'));return isFinite(v)?v:def;}
  function lc(s){return s.charAt(0).toLowerCase()+s.slice(1);}
  function listar(a){return a.length<2?a[0]:a.slice(0,-1).join(', ')+' y '+a[a.length-1];}
  function plazo(m){if(m<1)return 'menos de un mes';if(m<24)return Math.ceil(m)+' meses';return nf(m/12,0,1)+' años';}

  function kwhMes(it){var a=byId[it.id];return it.w/1000*it.h*(S.rl?a.r:1)*it.d*SEM;}
  function precio(f,st){
    if(st.t!=='h') return st.pu;
    var fr=FR[f], wd=5/7, we=2/7;
    return wd*fr.p*st.pp+wd*fr.l*st.pl+(we+wd*fr.v)*st.pv;
  }
  function coste(it,st){return kwhMes(it)*precio(it.f,st||S)*IMP;}
  function pico(){
    var arr=[],h,mx=0,hm=0,f='todo';
    for(h=0;h<24;h++)arr.push(0);
    S.items.forEach(function(it){var r=FR[it.f].h;for(var x=r[0];x<r[1];x++)arr[x]+=it.w;});
    arr.forEach(function(v,i){if(v>mx){mx=v;hm=i;}});
    ['madrugada','manana','tarde','punta','noche'].forEach(function(k){var r=FR[k].h;if(hm>=r[0]&&hm<r[1])f=k;});
    return {kw:mx/1000,f:f};
  }

  function diagnostico(costs){
    var out=[]; if(!S.items.length) return out;
    var tot=costs.reduce(function(s,c){return s+c;},0);
    var pk=pico(), i;
    if(pk.kw>S.kw){
      var sig=null; for(i=0;i<POT.length;i++){if(POT[i]>=pk.kw){sig=POT[i];break;}}
      out.push({p:0,k:'Aviso',c:'aviso',t:'Tu limitador puede saltar',x:'Si coinciden los aparatos que usas '+FR[pk.f].c+', sumarían '+kwf(pk.kw)+' kW y tienes '+kwf(S.kw)+' kW contratados. Evita encenderlos a la vez'+(sig?' o sube la potencia a '+kwf(sig)+' kW':'')+'.'});
    } else {
      var rec=null; for(i=0;i<POT.length;i++){if(POT[i]>=pk.kw*1.1){rec=POT[i];break;}}
      if(rec&&rec<S.kw){
        var ahp=(S.kw-rec)*POT_DIA*365*IMP;
        if(ahp>=8) out.push({p:1,s:ahp,k:'Ahorro',c:'ahorro',t:'Te sobra potencia contratada',x:'Aunque coincidan todos tus aparatos no pasarías de '+kwf(pk.kw)+' kW. Bajando a '+kwf(rec)+' kW pagarías menos cada mes sin notar nada.'});
      }
    }
    var mov=S.items.filter(function(it){return byId[it.id].m&&it.f!=='madrugada';});
    var ref=S.t==='h'?S:{t:'h',pp:DEF.pp,pl:DEF.pl,pv:DEF.pv};
    var despues=S.items.reduce(function(s,it){var f=byId[it.id].m?'madrugada':it.f;return s+coste({id:it.id,w:it.w,h:it.h,d:it.d,f:f},ref);},0);
    var ahh=(tot-despues)*12;
    if(ahh>=10&&(mov.length||S.t==='u')){
      var nombres=[]; mov.forEach(function(it){var a=byId[it.id],nm=a.s||lc(a.n);if(nombres.indexOf(nm)<0)nombres.push(nm);});
      var x;
      if(S.t==='h') x='Programando '+listar(nombres)+' entre las 0 y las 8 h, en horario valle, tu factura bajaría sin cambiar lo que consumes.';
      else if(nombres.length) x='Con una tarifa por horas y programando '+listar(nombres)+' entre las 0 y las 8 h, pagarías menos por la misma energía.';
      else x='Con tus horarios, una tarifa por horas te saldría más barata que el precio único.';
      out.push({p:1,s:ahh,k:'Ahorro',c:'ahorro',t:S.t==='h'?'Programa lo que puedas de madrugada':'Una tarifa por horas te saldría más barata',x:x});
    } else if(S.t==='u'&&despues>tot){
      out.push({p:2,k:'Dato',c:'dato',t:'Te conviene el precio único',x:'Con tus horarios, una tarifa por horas te saldría más cara. Mantén una tarifa de precio fijo.'});
    }
    var alts=[];
    S.items.forEach(function(it,j){var a=byId[it.id];if(!a.alt)return;var ahm=costs[j]*(1-a.alt.k);if(ahm*12<5)return;alts.push({a:a,ah:ahm*12,me:a.alt.c/ahm});});
    alts.sort(function(x,y){return y.ah-x.ah;});
    var noComp=0;
    alts.slice(0,2).forEach(function(o){
      if(o.me<=36) out.push({p:1,s:o.ah,k:'Ahorro',c:'ahorro',t:'Sustituye: '+lc(o.a.n),x:'Pasar a '+o.a.alt.n+' cuesta unos '+eur0(o.a.alt.c)+' € y se paga solo en '+plazo(o.me)+'.'+(o.a.alt.nota?' '+o.a.alt.nota:'')});
      else if(!noComp++) out.push({p:3,k:'Dato',c:'dato',t:'Cambiar '+lc(o.a.n)+' no compensa solo por ahorro',x:'Pasar a '+o.a.alt.n+' te ahorraría unos '+eur0(o.ah)+' € al año, pero tardarías '+plazo(o.me)+' en recuperar los '+eur0(o.a.alt.c)+' € que cuesta.'});
    });
    if(tot>0){
      var im=0; costs.forEach(function(c,j){if(c>costs[im])im=j;});
      out.push({p:2,k:'Dato',c:'dato',t:'Tu mayor gasto: '+lc(byId[S.items[im].id].n),x:'Supone el '+Math.round(costs[im]/tot*100)+' % de lo que pagas por tus aparatos: '+eur(costs[im])+' € al mes.'});
    }
    out.sort(function(a,b){return a.p-b.p||(b.s||0)-(a.s||0);});
    return out.slice(0,4);
  }

  function render(){
    var costs=S.items.map(function(it){return coste(it,S);});
    var maxC=Math.max.apply(null,costs.concat([0.0001]));
    el.lista.innerHTML='';
    S.items.forEach(function(it,i){
      var a=byId[it.id], li=document.createElement('li');
      li.className='tlc-it'+(i===editIdx?' is-edit':'')+(i===nuevoIdx?' is-new':'');
      li.innerHTML='<div class="tlc-it-top"><div><div class="tlc-it-n"></div><div class="tlc-it-m"></div></div><div class="tlc-it-c"><strong></strong><span>€/mes</span></div></div><div class="tlc-it-b"><div class="tlc-bar"><i></i></div><div class="tlc-it-act"><button type="button" data-ed="'+i+'">Editar</button><button type="button" data-rm="'+i+'">Quitar</button></div></div>';
      li.querySelector('.tlc-it-n').textContent=a.n;
      li.querySelector('.tlc-it-m').textContent=nf(it.w,0,0)+' W · '+nf(it.h,0,2)+' h/día · '+it.d+' días/semana · '+FR[it.f].c;
      li.querySelector('strong').textContent=eur(costs[i]);
      li.querySelector('.tlc-bar i').style.width=Math.max(2,costs[i]/maxC*100)+'%';
      el.lista.appendChild(li);
    });
    nuevoIdx=-1;
    el.vacio.hidden=S.items.length>0;

    var ene=costs.reduce(function(s,c){return s+c;},0);
    var kwh=S.items.reduce(function(s,it){return s+kwhMes(it);},0);
    var pot=S.kw*POT_DIA*MES*IMP+CONTADOR*IVA;
    var fac=ene+pot;
    $('tlc-fac').textContent=eur(fac);
    $('tlc-ene').textContent=eur(ene)+' €';
    $('tlc-pot').textContent=eur(pot)+' €';
    $('tlc-ano').textContent=eur0(fac*12)+' €';
    $('tlc-kwh').textContent=nf(kwh,0,0)+' kWh/mes';

    var pk=pico(), box=$('tlc-pico'), escala=Math.max(pk.kw,S.kw)*1.15;
    box.classList.toggle('is-over',pk.kw>S.kw);
    $('tlc-pico-l').textContent=S.items.length?'Pico si coinciden ('+FR[pk.f].c+')':'Pico de potencia';
    $('tlc-pico-v').textContent=S.items.length?kwf(pk.kw)+' / '+kwf(S.kw)+' kW':'–';
    $('tlc-pico-i').style.width=(S.items.length?Math.min(100,pk.kw/escala*100):0)+'%';
    $('tlc-pico-b').style.left='calc('+(S.kw/escala*100)+'% - 1px)';

    var tips=diagnostico(costs);
    el.tips.innerHTML='';
    if(!tips.length){var p=document.createElement('p');p.className='tlc-tips-vacio';p.textContent='Añade aparatos y aquí verás qué te está costando más y qué cambios te ahorran dinero de verdad.';el.tips.appendChild(p);}
    tips.forEach(function(t){
      var ar=document.createElement('article');ar.className='tlc-tip tlc-tip--'+t.c;
      ar.innerHTML='<span class="tlc-tip-k"></span><h3></h3><p></p>';
      ar.querySelector('.tlc-tip-k').textContent=t.k;
      ar.querySelector('h3').textContent=t.t;
      ar.querySelector('p').textContent=t.x;
      if(t.s){var s=document.createElement('span');s.className='tlc-tip-s';s.textContent='≈ '+eur0(t.s)+' € menos al año';ar.appendChild(s);}
      el.tips.appendChild(ar);
    });

    document.querySelectorAll('.tlc [data-q]').forEach(function(sp){
      var a=byId[sp.getAttribute('data-q')], u=sp.getAttribute('data-u');
      var porHora=a.w/1000*(S.rl?a.r:1)*precio(a.f,S)*IMP;
      if(u==='h') sp.textContent='≈ '+eur(porHora)+' €/hora';
      else if(u==='uso') sp.textContent='≈ '+eur(porHora*a.h)+' € por uso';
      else sp.textContent='≈ '+eur(coste({id:a.id,w:a.w,h:a.h,d:a.d,f:a.f},S))+' €/mes';
    });
  }

  function msg(t){el.msg.textContent=t;clearTimeout(msg._t);msg._t=setTimeout(function(){el.msg.textContent='';},3500);}
  function cargarForm(a){el.w.value=a.w;el.h.value=a.h;el.d.value=a.d;el.fr.value=a.f;}
  function salirEdicion(){editIdx=-1;el.add.textContent='Añadir';el.cancel.hidden=true;}
  function sync(){
    el.pu.value=S.pu;el.pp.value=S.pp;el.pl.value=S.pl;el.pv.value=S.pv;el.kw.value=String(S.kw);el.rl.checked=!!S.rl;
    el.tu.setAttribute('aria-pressed',S.t==='u');el.th.setAttribute('aria-pressed',S.t==='h');
    el.boxU.hidden=S.t==='h';el.boxH.hidden=S.t!=='h';
  }
  function ejemplo(){S.items=EJEMPLO.map(function(id){var a=byId[id];return {id:id,w:a.w,h:a.h,d:a.d,f:a.f};});}

  GRUPOS.forEach(function(g){
    var og=document.createElement('optgroup');og.label=g;
    A.forEach(function(a){if(a.g===g)og.appendChild(new Option(a.n,a.id));});
    el.ap.appendChild(og);
  });
  FR_ORDEN.forEach(function(k){el.fr.add(new Option(FR[k].n,k));});
  POT.forEach(function(p){el.kw.add(new Option(kwf(p)+' kW',String(p)));});

  el.ap.addEventListener('change',function(){cargarForm(byId[el.ap.value]);});
  el.add.addEventListener('click',function(){
    var id=el.ap.value, a=byId[id];
    var it={id:id,w:Math.max(1,num(el.w,a.w)),h:Math.min(24,Math.max(0.05,num(el.h,a.h))),d:Math.min(7,Math.max(1,Math.round(num(el.d,a.d)))),f:el.fr.value};
    if(editIdx>=0){S.items[editIdx]=it;nuevoIdx=editIdx;msg('Cambios guardados.');salirEdicion();}
    else{S.items.push(it);nuevoIdx=S.items.length-1;msg(a.n+' añadido.');}
    render();
  });
  el.cancel.addEventListener('click',function(){salirEdicion();render();});
  el.lista.addEventListener('click',function(e){
    var b=e.target.closest('button'); if(!b) return;
    if(b.hasAttribute('data-rm')){var i=+b.getAttribute('data-rm');S.items.splice(i,1);if(editIdx===i)salirEdicion();else if(editIdx>i)editIdx--;render();}
    else if(b.hasAttribute('data-ed')){
      editIdx=+b.getAttribute('data-ed');var it=S.items[editIdx];
      el.ap.value=it.id;el.w.value=it.w;el.h.value=it.h;el.d.value=it.d;el.fr.value=it.f;
      el.add.textContent='Guardar cambios';el.cancel.hidden=false;render();el.ap.focus();
    }
  });
  function tarifa(t){S.t=t;sync();render();}
  el.tu.addEventListener('click',function(){tarifa('u');});
  el.th.addEventListener('click',function(){tarifa('h');});
  [['pu','pu'],['pp','pp'],['pl','pl'],['pv','pv']].forEach(function(p){el[p[0]].addEventListener('input',function(){S[p[1]]=Math.max(0,num(el[p[0]],0));render();});});
  el.kw.addEventListener('change',function(){S.kw=parseFloat(el.kw.value);render();});
  el.rl.addEventListener('change',function(){S.rl=el.rl.checked?1:0;render();});
  $('tlc-ej').addEventListener('click',function(){ejemplo();salirEdicion();render();msg('Ejemplo cargado: piso de 3 personas.');});
  $('tlc-vac').addEventListener('click',function(){S.items=[];salirEdicion();render();});

  function copiar(txt,ok,ko){
    if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(txt).then(ok,function(){copiarViejo(txt,ok,ko);});}
    else copiarViejo(txt,ok,ko);
  }
  function copiarViejo(txt,ok,ko){
    try{var ta=document.createElement('textarea');ta.value=txt;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();var r=document.execCommand('copy');document.body.removeChild(ta);r?ok():ko();}catch(e){ko();}
  }
  $('tlc-share').addEventListener('click',function(){
    var o={t:S.t,pu:S.pu,pp:S.pp,pl:S.pl,pv:S.pv,kw:S.kw,rl:S.rl,i:S.items.map(function(it){return [it.id,it.w,it.h,it.d,it.f];})};
    var url=location.href.split('#')[0]+'#calc='+encodeURIComponent(JSON.stringify(o));
    try{history.replaceState(null,'',url);}catch(e){}
    copiar(url,function(){msg('Enlace copiado: compártelo y verán tu cálculo.');},function(){msg('No se pudo copiar. Copia la dirección de la barra del navegador.');});
  });
  function desdeEnlace(){
    var m=location.hash.match(/#calc=(.+)$/); if(!m) return false;
    try{
      var o=JSON.parse(decodeURIComponent(m[1]));
      S.t=o.t==='h'?'h':'u';
      ['pu','pp','pl','pv'].forEach(function(k){if(isFinite(o[k]))S[k]=+o[k];});
      if(POT.indexOf(+o.kw)>=0)S.kw=+o.kw;
      S.rl=o.rl?1:0;
      S.items=(o.i||[]).filter(function(x){return byId[x[0]]&&FR[x[4]];}).map(function(x){return {id:x[0],w:+x[1]||1,h:Math.min(24,+x[2]||1),d:Math.min(7,Math.max(1,+x[3]||7)),f:x[4]};});
      return true;
    }catch(e){return false;}
  }

  document.querySelectorAll('.tlc [data-add]').forEach(function(b){
    b.addEventListener('click',function(){
      var a=byId[b.getAttribute('data-add')];
      salirEdicion();
      S.items.push({id:a.id,w:a.w,h:a.h,d:a.d,f:a.f});nuevoIdx=S.items.length-1;
      el.ap.value=a.id;cargarForm(a);render();msg(a.n+' añadido a tu casa.');
      app.scrollIntoView({behavior:'smooth',block:'start'});
    });
  });

  if(!desdeEnlace()) ejemplo();
  el.ap.value='ac'; cargarForm(byId.ac);
  sync(); render();
})();
