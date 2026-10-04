/* Calculadora de potencia contratada de tuluzencasa.com (v2).
   Pegar como snippet JavaScript en WPCode, sin etiquetas <script>, en el pie de todo el sitio.
   Se activa solo si existe #tlp-app. Funciona con el marcado antiguo y con el nuevo: los campos
   nuevos (potencia exacta, precio, avisos, copiar) solo se usan si están en la página. */
(function(){
  var app=document.getElementById('tlp-app'); if(!app) return;
  var IMP=1.21*1.0511, PRECIO_DEF=0.09, MES=30.4, MARGEN=1.1, DEF_KW=4.6, MAX_OTRO=20000;
  var POT=[2.3,3.45,4.6,5.75,6.9,8.05,9.2], MAX_KW=POT[POT.length-1];
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
  /* tocado: el visitante ya ha cambiado la lista; hasta entonces no se dan importes. */
  var S={kw:DEF_KW,exacta:false,precio:PRECIO_DEF,sel:{},otro:0,tocado:false};
  A.forEach(function(a){if(a.on)S.sel[a.id]=1;});

  function $(id){return document.getElementById(id);}
  function nf(n,min,max){return n.toLocaleString('es-ES',{minimumFractionDigits:min,maximumFractionDigits:max});}
  function miles(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,'.');}
  function eur(n){return nf(n,2,2);}
  function kwf(n){return nf(n,0,2);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function anual(kw){return kw*S.precio*365*IMP;}
  function mensual(kw){return kw*S.precio*MES*IMP;}
  function igual(a,b){return Math.abs(a-b)<1e-6;}
  function normalizar(s){return String(s).replace(/\s+/g,' ').trim().toLowerCase();}
  /* Lee un número escrito en español: «1.200», «1200», «4,4», «4.4». Devuelve NaN si no es un número. */
  function leerNumero(txt,unidad){
    var s=String(txt).trim().replace(/\s+/g,'');
    if(unidad) s=s.replace(new RegExp(unidad+'$','i'),'');
    if(/^\d{1,3}(\.\d{3})+(,\d+)?$/.test(s)) s=s.replace(/\./g,'');
    s=s.replace(',','.');
    return /^\d*\.?\d+$/.test(s)?Number(s):NaN;
  }
  function mensaje(id,texto,error,campo){
    var m=$(id); if(m){m.textContent=texto||'';m.classList.toggle('is-error',!!error);}
    if(campo){ if(error) campo.setAttribute('aria-invalid','true'); else campo.removeAttribute('aria-invalid'); }
  }

  /* Título de la diferencia: por id en el marcado nuevo; si no, se localiza por su texto. */
  var etiquetas=[], etiqueta=$('tlp-dif-label');
  if(etiqueta && app.contains(etiqueta)){
    etiquetas.push(etiqueta);
  } else {
    var walker=document.createTreeWalker(app,4), nodo;
    while((nodo=walker.nextNode())){
      if(nodo.parentElement && !nodo.parentElement.closest('script, style') &&
         normalizar(nodo.nodeValue)==='diferencia al año') etiquetas.push(nodo);
    }
  }
  function ponerEtiqueta(texto){
    etiquetas.forEach(function(el){
      if(el.nodeType===3) el.nodeValue=texto;
      else el.textContent=texto;
    });
  }

  /* Marca de exceso, limitada a esta calculadora. */
  if(!$('tlp-estilo-exceso')){
    var estilo=document.createElement('style');
    estilo.id='tlp-estilo-exceso';
    estilo.textContent=
      '#tlp-app #tlp-barra.is-exceso{outline:2px solid #c2410c;outline-offset:3px;}'+
      '#tlp-app #tlp-esc li.is-exceso{background:#fff7ed;color:#9a3412;outline:2px solid #c2410c;outline-offset:-2px;}'+
      '#tlp-app #tlp-esc li.is-exceso span{color:#9a3412;font-weight:700;}';
    document.head.appendChild(estilo);
  }

  /* Lista de aparatos. */
  var html='';
  GRUPOS.forEach(function(g){
    html+='<fieldset class="tlp-g"><legend>'+esc(g)+'</legend><div class="tlp-ops">';
    A.filter(function(a){return a.g===g;}).forEach(function(a){
      html+='<div class="tlp-op" data-id="'+a.id+'"><label class="tlp-op-l"><input type="checkbox" value="'+a.id+'"'+(S.sel[a.id]?' checked':'')+'>'+
        '<span class="tlp-op-t"><span class="tlp-op-n">'+esc(a.n)+'</span><span class="tlp-op-w">'+miles(a.w)+' W</span></span></label>'+
        '<label class="tlp-op-q"><span class="tlp-sr">Cuántos '+esc(a.n)+'</span><select aria-label="Cuántos: '+esc(a.n)+'" data-q="'+a.id+'"'+(S.sel[a.id]?'':' disabled')+'>'+
        '<option value="1">×1</option><option value="2">×2</option><option value="3">×3</option><option value="4">×4</option></select></label></div>';
    });
    html+='</div></fieldset>';
  });
  $('tlp-lista').innerHTML=html;
  var selKw=$('tlp-kw'), inKw=$('tlp-kw-ex'), inPrecio=$('tlp-precio'), inOtro=$('tlp-otro');
  function opcionesKw(){
    var h=POT.map(function(k){return '<option value="'+k+'"'+(!S.exacta&&igual(k,S.kw)?' selected':'')+'>'+kwf(k)+' kW</option>';}).join('');
    if(S.exacta) h+='<option value="exacta" selected>'+kwf(S.kw)+' kW (la que has escrito)</option>';
    selKw.innerHTML=h;
  }
  opcionesKw();
  $('tlp-esc').innerHTML=POT.map(function(k){return '<li data-kw="'+k+'"><span>'+kwf(k)+'</span></li>';}).join('');

  function suma(){
    var w=0;
    A.forEach(function(a){if(S.sel[a.id])w+=a.w*S.sel[a.id];});
    return w+S.otro;
  }
  function seleccion(){
    var l=[];
    A.forEach(function(a){if(S.sel[a.id])l.push(a.n+' ('+miles(a.w)+' W)'+(S.sel[a.id]>1?' ×'+S.sel[a.id]:''));});
    if(S.otro>0) l.push('Otro aparato ('+miles(S.otro)+' W)');
    return l;
  }

  var R={};  /* último resultado, para copiarlo */
  function pintar(){
    var w=suma(), kw=w/1000, need=kw*MARGEN, rec=null, i;
    if(w>0){
      for(i=0;i<POT.length;i++){if(POT[i]>=need-1e-9){rec=POT[i];break;}}
    }
    var exceso=w>0 && rec===null;
    var n=0; A.forEach(function(a){if(S.sel[a.id])n+=S.sel[a.id];}); if(S.otro>0)n++;
    $('tlp-sum').textContent=kwf(kw)+' kW';
    $('tlp-mar').textContent=kwf(need)+' kW';
    $('tlp-cur').textContent=kwf(S.kw)+' kW';
    $('tlp-n').textContent=n===1?'1 aparato':n+' aparatos';
    Array.prototype.forEach.call(app.querySelectorAll('[data-tlp="precio"]'),function(el){el.textContent=nf(S.precio,2,4);});
    var dif=$('tlp-dif'), tip=$('tlp-tip'), bR=$('tlp-b-rec'), bD=$('tlp-b-dif'), barra=$('tlp-barra');
    R={w:w,kw:kw,need:need,rec:rec,exceso:exceso,estado:'vacio'};

    Array.prototype.forEach.call($('tlp-esc').children,function(li){
      var k=parseFloat(li.getAttribute('data-kw')), marca=exceso && k===MAX_KW;
      li.classList.toggle('is-rec',rec!==null && igual(k,rec));
      li.classList.toggle('is-cur',igual(k,S.kw));
      li.classList.toggle('is-exceso',marca);
      var span=li.querySelector('span');
      if(span) span.textContent=(marca?'>':'')+kwf(k);
      if(marca) li.setAttribute('title','La potencia necesaria con margen supera '+kwf(MAX_KW)+' kW');
      else li.removeAttribute('title');
    });

    if(!w){
      ponerEtiqueta('Comparación anual');
      $('tlp-rec').innerHTML='–';
      dif.textContent='–'; bR.textContent='–'; bD.textContent='Marca aparatos'; barra.className='tlp-barra';
      tip.className='tlp-tip';
      tip.innerHTML='<p class="tlp-tip-k">Empieza aquí</p><h3>Marca lo que puede estar encendido a la vez</h3><p>Piensa en el peor momento normal del día, por ejemplo la hora de la cena. No marques todo lo que tienes en casa.</p>';
      return;
    }

    if(exceso){
      R.estado='exceso';
      ponerEtiqueta('Comparación anual');
      $('tlp-rec').innerHTML='&gt;'+kwf(MAX_KW)+'<small>kW</small>';
      dif.textContent='–';
      bR.textContent='Más de '+kwf(MAX_KW)+' kW';
      bD.textContent='Fuera de la escala';
      barra.className='tlp-barra is-aviso is-exceso';
      tip.className='tlp-tip tlp-tip--aviso';
      tip.innerHTML='<p class="tlp-tip-k">Aviso</p><h3>Necesitas más de '+kwf(MAX_KW)+' kW con margen</h3><p>Los aparatos seleccionados suman '+kwf(kw)+' kW. Con el margen del 10 %, la potencia necesaria es '+kwf(need)+' kW y supera el máximo de esta tabla.</p>'+
        (S.kw>=need-1e-9?'<p>Tus '+kwf(S.kw)+' kW cubren lo que has marcado.</p>':
         kw>S.kw+1e-9?'<p>Además, lo marcado supera los '+kwf(S.kw)+' kW que tienes: si coincide, saltará el limitador.</p>':'')+
        '<p>Revisa si realmente pueden coincidir todos. Si es así, consulta a tu comercializadora o a un instalador autorizado.</p>';
      return;
    }

    $('tlp-rec').innerHTML=kwf(rec)+'<small>kW</small>';
    bR.textContent=kwf(rec)+' kW';

    if(!S.tocado){
      /* Solo cuentan los aparatos que vienen marcados: no se anuncia ahorro todavía. */
      R.estado='inicial';
      ponerEtiqueta('Comparación anual');
      dif.textContent='–'; bD.textContent='Marca tus aparatos'; barra.className='tlp-barra';
      tip.className='tlp-tip';
      tip.innerHTML='<p class="tlp-tip-k">Empieza aquí</p><h3>Añade lo que enciendes a la vez</h3><p>Ahora solo cuentan la nevera, la televisión y las luces, que suelen estar siempre encendidas. Marca lo que pueda coincidir con ellos en tu peor momento del día y verás la diferencia estimada con tu potencia.</p>';
      return;
    }

    var anio=anual(S.kw)-anual(rec), mes=mensual(S.kw)-mensual(rec);
    R.anio=anio; R.mes=mes;

    if(Math.abs(anio)<0.005){
      R.estado='igual';
      ponerEtiqueta('Sin diferencia anual');
      dif.textContent='0,00 €';
      bD.textContent='Bien ajustada';
      barra.className='tlp-barra is-ok';
      tip.className='tlp-tip tlp-tip--ok';
      tip.innerHTML='<p class="tlp-tip-k">Bien ajustada</p><h3>Tu potencia es la recomendada</h3><p>Con '+kwf(S.kw)+' kW cubres '+kwf(kw)+' kW a la vez con el margen del 10 %. Si quitas algún aparato de la lista, mira si podrías bajar un escalón.</p>';

    } else if(anio>0){
      R.estado='ahorro';
      ponerEtiqueta('Pagas de más al año');
      dif.textContent='≈ '+eur(anio)+' €';
      bD.textContent='Ahorrarías ≈ '+eur(anio)+' €/año';
      barra.className='tlp-barra is-ok';
      tip.className='tlp-tip tlp-tip--ahorro';
      tip.innerHTML='<p class="tlp-tip-k">Ahorro estimado</p><h3>Te sobra potencia</h3><p>Pasando de '+kwf(S.kw)+' a '+kwf(rec)+' kW pagarías menos por el término de potencia, con impuesto eléctrico e IVA:</p><span class="tlp-tip-s">≈ '+eur(anio)+' € al año</span><p class="tlp-tip-m">≈ '+eur(mes)+' € al mes, con un precio de '+nf(S.precio,2,4)+' € por kW y día. Los posibles costes del cambio de potencia no están incluidos.</p>';

    } else if(kw>S.kw+1e-9){
      R.estado='supera';
      ponerEtiqueta('Coste adicional al año');
      dif.textContent='≈ '+eur(-anio)+' €';
      bD.textContent='Superas tu potencia · +'+eur(-anio)+' €/año';
      barra.className='tlp-barra is-aviso';
      tip.className='tlp-tip tlp-tip--aviso';
      tip.innerHTML='<p class="tlp-tip-k">Aviso</p><h3>Los aparatos superan tu potencia contratada</h3><p>Lo que has marcado suma '+kwf(kw)+' kW y tienes '+kwf(S.kw)+' kW: si coinciden, saltará el limitador. Evita que coincidan o sube a '+kwf(rec)+' kW para cubrirlos con el margen del 10 %. El coste adicional estimado por el término de potencia sería:</p><span class="tlp-tip-s">≈ '+eur(-anio)+' € al año</span><p class="tlp-tip-m">≈ '+eur(-mes)+' € al mes, con un precio de '+nf(S.precio,2,4)+' € por kW y día. Los posibles costes del cambio de potencia no están incluidos.</p>';

    } else {
      R.estado='margen';
      ponerEtiqueta('Coste adicional al año');
      dif.textContent='≈ '+eur(-anio)+' €';
      bD.textContent='Poco margen · +'+eur(-anio)+' €/año';
      barra.className='tlp-barra is-aviso';
      tip.className='tlp-tip tlp-tip--margen';
      tip.innerHTML='<p class="tlp-tip-k">Atención</p><h3>Tienes potencia suficiente, pero poco margen</h3><p>Lo que has marcado suma '+kwf(kw)+' kW y tienes '+kwf(S.kw)+' kW: cabe, pero sin el margen del 10 % ('+kwf(need)+' kW). Un arranque o un aparato que no has contado puede hacer saltar el limitador. Si te pasa a menudo, sube a '+kwf(rec)+' kW. El coste adicional estimado sería:</p><span class="tlp-tip-s">≈ '+eur(-anio)+' € al año</span><p class="tlp-tip-m">≈ '+eur(-mes)+' € al mes, con un precio de '+nf(S.precio,2,4)+' € por kW y día. Los posibles costes del cambio de potencia no están incluidos.</p>';
    }
  }

  function tocar(){S.tocado=true;}

  $('tlp-lista').addEventListener('change',function(e){
    var t=e.target, id;
    if(t.type==='checkbox'){
      id=t.value;
      var q=app.querySelector('select[data-q="'+id+'"]');
      if(t.checked){S.sel[id]=parseInt(q.value,10)||1;q.disabled=false;}
      else{delete S.sel[id];q.disabled=true;}
      t.closest('.tlp-op').classList.toggle('is-on',t.checked);
    } else if(t.hasAttribute('data-q')){
      id=t.getAttribute('data-q'); if(S.sel[id])S.sel[id]=parseInt(t.value,10)||1;
    }
    tocar(); pintar();
  });

  selKw.addEventListener('change',function(){
    if(this.value==='exacta') return;
    S.kw=parseFloat(this.value); S.exacta=false;
    if(inKw){inKw.value=''; mensaje('tlp-kw-msg','',false,inKw);}
    opcionesKw(); pintar();
  });

  if(inKw) inKw.addEventListener('input',function(){
    var txt=this.value.trim();
    if(!txt){
      if(S.exacta){S.exacta=false; S.kw=DEF_KW;}
      mensaje('tlp-kw-msg','',false,inKw); opcionesKw(); pintar(); return;
    }
    var v=leerNumero(txt,'kw');
    if(isNaN(v) || v<1 || v>15){
      mensaje('tlp-kw-msg','Escribe la potencia en kW, entre 1 y 15, por ejemplo 4,4. Mientras tanto se usa '+kwf(S.kw)+' kW.',true,inKw);
      return;
    }
    S.kw=v; S.exacta=!POT.some(function(k){return igual(k,v);});
    mensaje('tlp-kw-msg',S.exacta?'Usamos '+kwf(v)+' kW, la potencia que has escrito.':'',false,inKw);
    opcionesKw(); pintar();
  });

  if(inPrecio) inPrecio.addEventListener('input',function(){
    var txt=this.value.trim(), v=leerNumero(txt);
    if(!txt){
      S.precio=PRECIO_DEF; mensaje('tlp-precio-msg','Sin precio: se usa '+nf(PRECIO_DEF,2,4)+' € por kW y día.',false,inPrecio); pintar(); return;
    }
    if(isNaN(v) || v<0.01 || v>1){
      mensaje('tlp-precio-msg','Escribe el precio en € por kW y día, entre 0,01 y 1, por ejemplo 0,09. Mientras tanto se usa '+nf(S.precio,2,4)+' €.',true,inPrecio);
      return;
    }
    S.precio=v; mensaje('tlp-precio-msg','',false,inPrecio); pintar();
  });

  inOtro.addEventListener('input',function(){
    var txt=this.value.trim(), v=leerNumero(txt,'w');
    tocar();
    if(!txt){S.otro=0; mensaje('tlp-otro-msg','',false,inOtro); pintar(); return;}
    if(isNaN(v)){
      S.otro=0; mensaje('tlp-otro-msg','Escribe solo la potencia en vatios, por ejemplo 1200. No se ha sumado.',true,inOtro);
    } else if(v<=0){
      S.otro=0; mensaje('tlp-otro-msg','La potencia tiene que ser mayor que 0 W. No se ha sumado.',true,inOtro);
    } else if(v>MAX_OTRO){
      S.otro=0; mensaje('tlp-otro-msg','El máximo es '+miles(MAX_OTRO)+' W ('+kwf(MAX_OTRO/1000)+' kW). No se ha sumado: revisa la cifra.',true,inOtro);
    } else {
      S.otro=v; mensaje('tlp-otro-msg','Se suman '+miles(v)+' W.',false,inOtro);
    }
    pintar();
  });

  $('tlp-reset').addEventListener('click',function(){
    S.sel={}; S.otro=0; S.tocado=true; inOtro.value=''; mensaje('tlp-otro-msg','',false,inOtro);
    Array.prototype.forEach.call(app.querySelectorAll('#tlp-lista input[type=checkbox]'),function(c){
      c.checked=false;
      c.closest('.tlp-op').classList.remove('is-on');
    });
    Array.prototype.forEach.call(app.querySelectorAll('#tlp-lista select'),function(s){
      s.value='1';
      s.disabled=true;
    });
    mensaje('tlp-copiar-msg','');
    pintar();
  });

  /* En móvil, tocar la barra fija lleva al resultado. */
  $('tlp-barra').addEventListener('click',function(){
    var t=$('tlp-res')||$('tlp-tip'); if(t && t.scrollIntoView) t.scrollIntoView({behavior:'smooth',block:'start'});
  });

  function textoResultado(){
    var l=['Calculadora de potencia contratada (tuluzencasa.com)'];
    l.push('Aparatos a la vez: '+seleccion().join(', '));
    l.push('Suman '+kwf(R.kw)+' kW; con el margen del 10 %, '+kwf(R.need)+' kW.');
    if(R.exceso) l.push('Potencia necesaria: más de '+kwf(MAX_KW)+' kW (fuera de la escala). Tienes '+kwf(S.kw)+' kW.');
    else l.push('Potencia recomendada: '+kwf(R.rec)+' kW. Tienes '+kwf(S.kw)+' kW.');
    var t={igual:'Tu potencia es la recomendada.',
      ahorro:'Pagas de más: ahorrarías ≈ '+eur(R.anio||0)+' € al año (≈ '+eur(R.mes||0)+' € al mes).',
      supera:'Los aparatos superan tu potencia contratada. Subir a la recomendada costaría ≈ '+eur(-(R.anio||0))+' € más al año.',
      margen:'Tienes potencia suficiente, pero poco margen. Subir a la recomendada costaría ≈ '+eur(-(R.anio||0))+' € más al año.',
      exceso:'Revisa si de verdad coinciden todos los aparatos.',
      inicial:'Solo cuentan los aparatos marcados por defecto.'}[R.estado];
    if(t) l.push(t);
    l.push('Estimación con '+nf(S.precio,2,4)+' € por kW y día sin impuestos, impuesto eléctrico 5,11 % e IVA 21 %. Solo término de potencia.');
    l.push(location.href.split('#')[0]);
    return l.join('\n');
  }
  var btnCopiar=$('tlp-copiar');
  if(btnCopiar) btnCopiar.addEventListener('click',function(){
    if(!R.w){mensaje('tlp-copiar-msg','Marca algún aparato antes de copiar el resultado.',true); return;}
    var texto=textoResultado();
    function bien(){mensaje('tlp-copiar-msg','Resultado copiado.',false);}
    function aMano(){
      var ta=document.createElement('textarea'); ta.value=texto; ta.setAttribute('readonly','');
      ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select();
      var ok=false; try{ok=document.execCommand('copy');}catch(e){}
      document.body.removeChild(ta);
      if(ok) bien(); else mensaje('tlp-copiar-msg','No se ha podido copiar. Prueba de nuevo o haz una captura.',true);
    }
    if(navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(texto).then(bien,aMano);
    else aMano();
  });

  Array.prototype.forEach.call(app.querySelectorAll('#tlp-lista input[type=checkbox]:checked'),function(c){
    c.closest('.tlp-op').classList.add('is-on');
  });
  pintar();
})();
