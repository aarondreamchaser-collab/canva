/* Calculadora de potencia contratada de tuluzencasa.com.
   Pegar como snippet JavaScript en WPCode, sin etiquetas <script>.
   Se activa solo si existe #tlp-app. */
(function(){
  var app=document.getElementById('tlp-app'); if(!app) return;
  var IMP=1.21*1.0511, POT_DIA=0.09, MES=30.4, MARGEN=1.1, DEF_KW=4.6;
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
  var S={kw:DEF_KW,sel:{},otro:0};
  A.forEach(function(a){if(a.on)S.sel[a.id]=1;});

  function $(id){return document.getElementById(id);}
  function nf(n,min,max){return n.toLocaleString('es-ES',{minimumFractionDigits:min,maximumFractionDigits:max});}
  function miles(n){return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,'.');}
  function eur(n){return nf(n,2,2);}
  function kwf(n){return nf(n,0,2);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function anual(kw){return kw*POT_DIA*365*IMP;}
  function normalizar(s){return String(s).replace(/\s+/g,' ').trim().toLowerCase();}

  /* Localiza el título existente, aunque no tenga id. */
  var etiquetas=[], etiqueta=$('tlp-dif-label');
  if(etiqueta && app.contains(etiqueta)){
    etiquetas.push(etiqueta);
  } else {
    var walker=document.createTreeWalker(app,4), nodo;
    while((nodo=walker.nextNode())){
      if(nodo.parentElement && !nodo.parentElement.closest('script, style') &&
         normalizar(nodo.nodeValue)==='diferencia al año') etiquetas.push(nodo);
    }
    /* Admite títulos repartidos entre varios spans. */
    if(!etiquetas.length){
      Array.prototype.forEach.call(app.querySelectorAll('*'),function(el){
        if(el.closest('script, style') || normalizar(el.textContent)!=='diferencia al año') return;
        var hijoCoincide=Array.prototype.some.call(el.children,function(hijo){
          return normalizar(hijo.textContent)==='diferencia al año';
        });
        if(!hijoCoincide) etiquetas.push(el);
      });
    }
  }
  function ponerEtiqueta(texto){
    etiquetas.forEach(function(el){
      if(el.nodeType===3) el.nodeValue=texto;
      else el.textContent=texto;
    });
  }

  /* Marca de exceso visible, limitada a esta calculadora. */
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
  $('tlp-kw').innerHTML=POT.map(function(k){return '<option value="'+k+'"'+(k===DEF_KW?' selected':'')+'>'+kwf(k)+' kW</option>';}).join('');
  $('tlp-esc').innerHTML=POT.map(function(k){return '<li data-kw="'+k+'"><span>'+kwf(k)+'</span></li>';}).join('');

  function suma(){
    var w=0;
    A.forEach(function(a){if(S.sel[a.id])w+=a.w*S.sel[a.id];});
    return w+S.otro;
  }

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
    var dif=$('tlp-dif'), tip=$('tlp-tip'), bR=$('tlp-b-rec'), bD=$('tlp-b-dif'), barra=$('tlp-barra');

    Array.prototype.forEach.call($('tlp-esc').children,function(li){
      var k=parseFloat(li.getAttribute('data-kw')), marca=exceso && k===MAX_KW;
      li.classList.toggle('is-rec',k===rec);
      li.classList.toggle('is-cur',k===S.kw);
      li.classList.toggle('is-exceso',marca);
      var span=li.querySelector('span');
      if(span) span.textContent=(marca?'>':'')+kwf(k);
      if(marca){
        li.setAttribute('title','La potencia necesaria con margen supera '+kwf(MAX_KW)+' kW');
      } else {
        li.removeAttribute('title');
      }
    });

    if(!w){
      ponerEtiqueta('Comparación anual');
      $('tlp-rec').innerHTML='–';
      dif.textContent='–'; bR.textContent='–'; bD.textContent='Marca aparatos'; barra.className='tlp-barra';
      tip.className='tlp-tip';
      tip.innerHTML='<p class="tlp-tip-k">Empieza aquí</p><h3>Marca lo que puede estar encendido a la vez</h3><p>Piensa en el peor momento normal del día, por ejemplo la hora de la cena.</p>';
      return;
    }

    if(exceso){
      ponerEtiqueta('Comparación anual');
      $('tlp-rec').innerHTML='&gt;'+kwf(MAX_KW)+'<small>kW</small>';
      dif.textContent='–';
      bR.textContent='Más de '+kwf(MAX_KW)+' kW';
      bD.textContent='Fuera de la escala';
      barra.className='tlp-barra is-aviso is-exceso';
      tip.className='tlp-tip tlp-tip--aviso';
      tip.innerHTML='<p class="tlp-tip-k">Aviso</p><h3>Necesitas más de '+kwf(MAX_KW)+' kW con margen</h3><p>Los aparatos seleccionados suman '+kwf(kw)+' kW. Con el margen del 10 %, la potencia necesaria es '+kwf(need)+' kW y supera el máximo de esta tabla.</p><p>Revisa si realmente pueden coincidir todos. Si es así, consulta a tu comercializadora o a un instalador autorizado.</p>';
      return;
    }

    $('tlp-rec').innerHTML=kwf(rec)+'<small>kW</small>';
    bR.textContent=kwf(rec)+' kW';
    var anio=anual(S.kw)-anual(rec), mes=(S.kw-rec)*POT_DIA*MES*IMP;

    if(Math.abs(anio)<0.005){
      ponerEtiqueta('Sin diferencia anual');
      dif.textContent='0,00 €';
      bD.textContent='Bien ajustada';
      barra.className='tlp-barra is-ok';
      tip.className='tlp-tip tlp-tip--ok';
      tip.innerHTML='<p class="tlp-tip-k">Bien ajustada</p><h3>Tu potencia es la recomendada</h3><p>Con '+kwf(S.kw)+' kW cubres '+kwf(kw)+' kW a la vez con el margen del 10 %. Si quitas algún aparato de la lista, mira si podrías bajar un escalón.</p>';

    } else if(anio>0){
      ponerEtiqueta('Pagas de más al año');
      dif.textContent=eur(anio)+' €';
      bD.textContent='Ahorrarías '+eur(anio)+' €/año';
      barra.className='tlp-barra is-ok';
      tip.className='tlp-tip tlp-tip--ahorro';
      tip.innerHTML='<p class="tlp-tip-k">Ahorro</p><h3>Te sobra potencia</h3><p>Pasando de '+kwf(S.kw)+' a '+kwf(rec)+' kW pagarías menos por el término de potencia, con impuesto eléctrico e IVA:</p><span class="tlp-tip-s">'+eur(anio)+' € al año</span><p class="tlp-tip-m">'+eur(mes)+' € al mes. Los posibles costes del cambio de potencia no están incluidos.</p>';

    } else {
      ponerEtiqueta('Coste adicional al año');
      dif.textContent=eur(-anio)+' €';
      bD.textContent='Pagarías '+eur(-anio)+' €/año más';
      barra.className='tlp-barra is-aviso';
      tip.className='tlp-tip tlp-tip--aviso';
      tip.innerHTML='<p class="tlp-tip-k">Aviso</p><h3>Puede saltar el limitador</h3><p>Lo que has marcado suma '+kwf(kw)+' kW y tienes '+kwf(S.kw)+' kW. Evita que coincidan o sube a '+kwf(rec)+' kW para cubrir el margen del 10 %. El coste adicional por el término de potencia sería:</p><span class="tlp-tip-s">'+eur(-anio)+' € al año</span><p class="tlp-tip-m">'+eur(-mes)+' € al mes. Los posibles costes del cambio de potencia no están incluidos.</p>';
    }
  }

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
    pintar();
  });

  $('tlp-kw').addEventListener('change',function(){
    S.kw=parseFloat(this.value);
    pintar();
  });

  $('tlp-otro').addEventListener('input',function(){
    var v=parseFloat(String(this.value).replace(',','.'));
    S.otro=isFinite(v)&&v>0?Math.min(v,20000):0;
    pintar();
  });

  $('tlp-reset').addEventListener('click',function(){
    S.sel={}; S.otro=0; $('tlp-otro').value='';
    Array.prototype.forEach.call(app.querySelectorAll('#tlp-lista input[type=checkbox]'),function(c){
      c.checked=false;
      c.closest('.tlp-op').classList.remove('is-on');
    });
    Array.prototype.forEach.call(app.querySelectorAll('#tlp-lista select'),function(s){
      s.value='1';
      s.disabled=true;
    });
    pintar();
  });

  Array.prototype.forEach.call(app.querySelectorAll('#tlp-lista input[type=checkbox]:checked'),function(c){
    c.closest('.tlp-op').classList.add('is-on');
  });
  pintar();
})();