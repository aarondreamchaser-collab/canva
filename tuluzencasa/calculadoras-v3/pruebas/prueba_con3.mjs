import {chromium,fs,ruta} from './comun.mjs';
const URL='https://tuluzencasa.com/calculadora-consumo-electrico/';
const b=await chromium.launch();
for (const w of (process.argv[2]||'1280,390').split(',').map(Number)){
  const mob=w<500; const ctx=await b.newContext({viewport:{width:w,height:mob?844:900},isMobile:mob,hasTouch:mob,deviceScaleFactor:1});
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error'&&!/Failed to load/.test(m.text()))errs.push(m.text())});
  await p.route('**/*',ruta(URL,'con3.html'));
  await p.goto(URL,{waitUntil:'networkidle',timeout:90000}); await p.waitForTimeout(800);
  const hud=()=>p.evaluate(()=>{const g=k=>document.querySelector('[data-v="'+k+'"]')?.textContent;return {fac:g('fac'),ano:g('ano'),kwh:g('kwh'),pico:g('pico'),on:document.querySelectorAll('.tl3-ap.is-on').length,ia:document.querySelectorAll('.tl3-t').length}});
  const r={ini:await hud()};
  const app=p.locator('#tl3-consumo'); await app.scrollIntoViewIfNeeded();
  await p.screenshot({path:`con3-${w}-ini.jpg`,fullPage:true,type:'jpeg',quality:65});
  try{
    // encender aire acondicionado
    await p.locator('.tl3-ap[data-id="ac"] [data-sw]').click(); await p.waitForTimeout(600); r.aire=await hud();
    // abrir ajustes del aire, cambiar horas y hora de inicio
    await p.locator('.tl3-ap[data-id="ac"] [data-ed]').click(); await p.waitForTimeout(300);
    await p.locator('.tl3-ap[data-id="ac"] [data-f="h"]').fill('4'); await p.waitForTimeout(700); r.horas=await hud();
    await p.locator('.tl3-ap[data-id="ac"] [data-f="s"]').evaluate(e=>{e.value='20';e.dispatchEvent(new Event('input',{bubbles:true}))}); await p.waitForTimeout(600); r.inicio=await hud();
    // tarifa por horas
    await p.locator('[data-tab="ta"]').click(); await p.locator('[data-t="h"]').click(); await p.waitForTimeout(600); r.horasTarifa=await hud();
    // optimizar
    const opt=p.locator('[data-acc="optimizar"]'); r.hayOpt=await opt.count();
    if(r.hayOpt){await opt.click(); await p.waitForTimeout(700); r.optimizado=await hud(); r.msg=await p.locator('.tl3-msg').textContent();}
    // escenario A y cambio
    await p.locator('[data-acc="A"]').click(); await p.locator('[data-tab="ap"]').click(); await p.locator('.tl3-ap[data-id="ac"] [data-sw]').click(); await p.waitForTimeout(600);
    r.esc=await p.locator('[data-esc]').textContent();
    // habitación
    await p.locator('[data-sala="cocina"]').click({force:true}); await p.waitForTimeout(400); r.cocina=await p.locator('.tl3-ap').count();
    // factura
    await p.locator('[data-tab="fa"]').click(); await p.locator('[data-fa="kwh"]').fill('300'); await p.locator('[data-fa="dias"]').fill('30'); await p.waitForTimeout(300);
    r.factura=(await p.locator('[data-fa-res]').textContent()).slice(0,120);
    // perfil coche
    await p.locator('.tl3-perf button',{hasText:'coche'}).click(); await p.waitForTimeout(600); r.coche=await hud();
    // hover gráfica
    const g=p.locator('[data-graf] svg'); await g.scrollIntoViewIfNeeded(); const bb=await g.boundingBox(); await p.mouse.move(bb.x+bb.width*0.9,bb.y+bb.height/2); r.lectura=await p.locator('[data-lec]').textContent();
    r.desb=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  }catch(e){r.fallo=e.message.split('\n')[0]}
  await app.screenshot({path:`con3-${w}-app.jpg`,type:'jpeg',quality:70});
  console.log(w,JSON.stringify(r,null,0)); console.log('ERRORES:',errs.join(' | ')||'ninguno');
  await ctx.close();
}
await b.close();
