import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const PORT=process.env.PORT;
const IMP=1.21*1.0511, an=(kw,p=0.09)=>kw*p*365*IMP, me=(kw,p=0.09)=>kw*p*30.4*IMP;
const f2=n=>n.toLocaleString('es-ES',{minimumFractionDigits:2,maximumFractionDigits:2});
let fallos=0; const ok=(c,m)=>{console.log((c?'OK   ':'FALLO')+' '+m); if(!c) fallos++;};
const b=await chromium.launch();
async function abrir(ctx,file){
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('https://**/*', async route=>{const req=route.request();
    try{const r=await fetch(req.url(),{method:req.method(),headers:{...req.headers()},redirect:'manual'});
    const hd={};r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;});
    await route.fulfill({status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())});}catch(e){await route.abort();}});
  await p.goto(`http://localhost:${PORT}/${file}`,{waitUntil:'networkidle',timeout:90000});
  return {p,errs};
}
const T=async(p,id)=>(await p.textContent('#'+id)).replace(/\s+/g,' ').trim();
const marca=async(p,id,on=true)=>{const c=p.locator(`#tlp-lista input[value="${id}"]`); on?await c.check():await c.uncheck();};

for (const vp of [{n:'escritorio',w:1280,h:900},{n:'movil',w:390,h:844},{n:'movil-360',w:360,h:740}]) {
  console.log(`\n== v2 ${vp.n}`);
  const ctx=await b.newContext({viewport:{width:vp.w,height:vp.h},deviceScaleFactor:vp.w<500?2:1,isMobile:vp.w<500,hasTouch:vp.w<500});
  await ctx.grantPermissions(['clipboard-read','clipboard-write'],{origin:`http://localhost:${PORT}`});
  const {p,errs}=await abrir(ctx,'t_102_v2.html');
  // 1 inicial neutro
  ok(await T(p,'tlp-sum')==='0,34 kW' && (await T(p,'tlp-rec')).startsWith('2,3'),'inicial: 0,34 kW, recomienda 2,3');
  ok(await T(p,'tlp-dif')==='–' && await T(p,'tlp-b-dif')==='Marca tus aparatos' && !(await T(p,'tlp-tip')).includes('€'),'inicial: sin importes hasta que marcas algo');
  // 2 ahorro
  await marca(p,'mic');
  ok(await T(p,'tlp-dif-label')==='Pagas de más al año' && await T(p,'tlp-dif')==='≈ '+f2(an(4.6)-an(2.3))+' €','ahorro: «Pagas de más al año» ≈ '+f2(an(4.6)-an(2.3))+' €');
  ok(await T(p,'tlp-b-dif')==='Ahorrarías ≈ '+f2(an(4.6)-an(2.3))+' €/año' && (await T(p,'tlp-tip')).includes('Ahorro estimado'),'ahorro: barra «Ahorrarías» y tip «Ahorro estimado»');
  // 5 igualdad: 0,34+1(mic)+1,8(ind)+1(caf)=4,14 -> 4,554 -> 4,6
  await marca(p,'ind'); await marca(p,'caf');
  ok((await T(p,'tlp-rec')).startsWith('4,6') && await T(p,'tlp-dif')==='0,00 €' && await T(p,'tlp-dif-label')==='Sin diferencia anual','igualdad: 4,14 kW → 4,6 recomendada = la tuya, 0,00 €');
  // 4 margen: quitar caf/mic, añadir horno: 0,34+1,8+2,2=4,34 -> 4,774 -> 5,75
  await marca(p,'caf',false); await marca(p,'mic',false); await marca(p,'hor');
  const tipM=await T(p,'tlp-tip');
  ok(await T(p,'tlp-sum')==='4,34 kW' && tipM.includes('Tienes potencia suficiente, pero poco margen') && (await p.getAttribute('#tlp-tip','class')).includes('tlp-tip--margen'),'poco margen: 4,34 kW con 4,6 contratados');
  ok(await T(p,'tlp-dif-label')==='Coste adicional al año' && await T(p,'tlp-dif')==='≈ '+f2(an(5.75)-an(4.6))+' €' && (await T(p,'tlp-b-dif')).startsWith('Poco margen'),'poco margen: coste adicional ≈ '+f2(an(5.75)-an(4.6))+' €');
  // 3 supera: + termo 1,5 -> 5,84 > 4,6 -> 6,424 -> 6,9
  await marca(p,'ter');
  const tipS=await T(p,'tlp-tip');
  ok(tipS.includes('Los aparatos superan tu potencia contratada') && await T(p,'tlp-dif')==='≈ '+f2(an(6.9)-an(4.6))+' €' && (await T(p,'tlp-b-dif')).startsWith('Superas tu potencia'),'supera: 5,84 kW con 4,6 → coste adicional ≈ '+f2(an(6.9)-an(4.6))+' €');
  // 6 exceso: + coche 7,4 -> 13,24
  await marca(p,'car');
  const exc=await p.evaluate(()=>{const li=[...document.querySelectorAll('#tlp-esc li')].pop();return {cls:li.className,txt:li.textContent,bar:document.querySelector('#tlp-barra').className}});
  ok((await T(p,'tlp-rec')).startsWith('>9,2') && exc.cls.includes('is-exceso') && exc.txt==='>9,2' && exc.bar.includes('is-exceso') && await T(p,'tlp-b-dif')==='Fuera de la escala','exceso: >9,2 kW marcado en la escala y la barra');
  ok((await T(p,'tlp-tip')).includes('supera los 4,6 kW que tienes'),'exceso: avisa también de que supera la contratada');
  // 7 regreso al rango
  await marca(p,'car',false);
  const back=await p.evaluate(()=>{const li=[...document.querySelectorAll('#tlp-esc li')].pop();return {cls:li.className,txt:li.textContent,bar:document.querySelector('#tlp-barra').className}});
  ok((await T(p,'tlp-rec')).startsWith('6,9') && !back.cls.includes('is-exceso') && back.txt==='9,2' && !back.bar.includes('is-exceso'),'regreso al rango: vuelve a 6,9 y se quita la marca');
  // 8 potencia exacta
  await p.fill('#tlp-kw-ex','6,5');
  ok(await T(p,'tlp-cur')==='6,5 kW' && await p.$eval('#tlp-kw',s=>s.value)==='exacta','potencia exacta 6,5 kW: «Tienes 6,5 kW» y el selector lo muestra');
  ok(await T(p,'tlp-dif')==='≈ '+f2(an(6.9)-an(6.5))+' €' && (await T(p,'tlp-tip')).includes('poco margen'),'exacta 6,5 kW con 5,84 marcados (cabe, sin margen): coste ≈ '+f2(an(6.9)-an(6.5))+' €');
  await p.fill('#tlp-kw-ex','abc');
  ok((await T(p,'tlp-kw-msg')).includes('Escribe la potencia en kW') && await T(p,'tlp-cur')==='6,5 kW' && await p.inputValue('#tlp-kw-ex')==='abc','exacta no válida: aviso, se mantiene 6,5 y no se borra lo escrito');
  await p.selectOption('#tlp-kw','4.6');
  ok(await T(p,'tlp-cur')==='4,6 kW' && await p.inputValue('#tlp-kw-ex')==='' && await T(p,'tlp-kw-msg')==='','elegir en el selector vacía la exacta');
  // 9 precio
  await p.fill('#tlp-precio','0,1');
  ok(await T(p,'tlp-dif')==='≈ '+f2(an(6.9,0.1)-an(4.6,0.1))+' €' && (await p.textContent('[data-tlp="precio"]'))==='0,10','precio 0,10: coste ≈ '+f2(an(6.9,0.1)-an(4.6,0.1))+' € y la hipótesis se actualiza');
  await p.fill('#tlp-precio','5');
  ok((await T(p,'tlp-precio-msg')).includes('entre 0,01 y 1') && await T(p,'tlp-dif')==='≈ '+f2(an(6.9,0.1)-an(4.6,0.1))+' €','precio no válido: aviso y se mantiene el último válido');
  await p.fill('#tlp-precio','0,09');
  // 10 otro
  const s0=await T(p,'tlp-sum');
  await p.fill('#tlp-otro','25000');
  ok(await T(p,'tlp-sum')===s0 && (await T(p,'tlp-otro-msg')).includes('El máximo es 20.000 W') && await p.inputValue('#tlp-otro')==='25000' && await p.getAttribute('#tlp-otro','aria-invalid')==='true','otro 25000: aviso, no se suma y no se cambia lo escrito');
  await p.fill('#tlp-otro','abc');
  ok(await T(p,'tlp-sum')===s0 && (await T(p,'tlp-otro-msg')).includes('No se ha sumado'),'otro «abc»: aviso y no se suma');
  await p.fill('#tlp-otro','1.200');
  ok(await T(p,'tlp-sum')==='7,04 kW' && (await T(p,'tlp-otro-msg'))==='Se suman 1.200 W.','otro «1.200» se lee como 1.200 W (antes 1,2 W)');
  // 12 copiar
  await p.click('#tlp-copiar');
  await p.waitForTimeout(300);
  const clip=await p.evaluate(()=>navigator.clipboard.readText()).catch(()=>'');
  ok((await T(p,'tlp-copiar-msg'))==='Resultado copiado.' && clip.includes('Potencia recomendada: 8,05 kW') && clip.includes('Otro aparato (1.200 W)') && clip.includes('0,09 €'),'copiar resultado al portapapeles');
  // 13 barra (móvil)
  if(vp.w<500){
    await p.evaluate(()=>window.scrollTo(0,document.querySelector('#tlp-lista').offsetTop+300));
    const vis=await p.isVisible('#tlp-barra');
    await p.click('#tlp-barra'); await p.waitForTimeout(900);
    const top=await p.evaluate(()=>document.querySelector('#tlp-res').getBoundingClientRect().top);
    ok(vis && top<200 && top>-50,'móvil: tocar la barra lleva al resultado');
    await p.evaluate(()=>window.scrollTo(0,0));
    await p.screenshot({path:`v2_${vp.w}_panel.png`});
  }
  // 11 reinicio
  await p.click('#tlp-reset');
  ok(await T(p,'tlp-sum')==='0 kW' && await T(p,'tlp-rec')==='–' && await T(p,'tlp-dif')==='–' && (await T(p,'tlp-tip')).includes('Empieza aquí') && await p.inputValue('#tlp-otro')==='' && await T(p,'tlp-otro-msg')==='' && (await p.$$('#tlp-lista input:checked')).length===0,'reinicio: todo a cero y aviso de empezar');
  await p.click('#tlp-copiar');
  ok((await T(p,'tlp-copiar-msg')).includes('Marca algún aparato'),'copiar sin aparatos: avisa');
  const ov=await p.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
  ok(ov<=0,'sin scroll horizontal');
  ok(errs.length===0,'sin errores de JavaScript '+errs.join(' | '));
  await p.screenshot({path:`v2_${vp.w}_full.png`,fullPage:true});
  await ctx.close();
}
// compatibilidad: marcado actual + JS nuevo
console.log('\n== marcado actual + JS nuevo (390)');
{
  const ctx=await b.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  const {p,errs}=await abrir(ctx,'t_102_marcado_viejo_js_nuevo.html');
  ok(await T(p,'tlp-dif')==='–','inicial sin importes');
  await marca(p,'mic');
  ok((await p.textContent('.tlp-lcd')).includes('Pagas de más al año') && await T(p,'tlp-dif')==='≈ '+f2(an(4.6)-an(2.3))+' €','ahorro con la etiqueta localizada por texto');
  await p.fill('#tlp-otro','25000');
  ok(await T(p,'tlp-sum')==='1,34 kW','otro 25000 no se suma');
  await marca(p,'car'); ok((await T(p,'tlp-rec')).startsWith('>9,2'),'exceso');
  await marca(p,'car',false); ok((await T(p,'tlp-rec')).startsWith('2,3'),'regreso al rango');
  await p.click('#tlp-reset'); ok(await T(p,'tlp-sum')==='0 kW','reinicio');
  ok(errs.length===0,'sin errores de JavaScript '+errs.join(' | '));
  await ctx.close();
}
await b.close();
console.log(`\n${fallos?fallos+' FALLOS':'Todo correcto'}`);
process.exit(fallos?1:0);
