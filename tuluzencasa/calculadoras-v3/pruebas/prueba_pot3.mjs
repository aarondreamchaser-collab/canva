import {chromium,fs,ruta} from './comun.mjs';
const URL='https://tuluzencasa.com/calculadora-potencia-contratada/';
const b=await chromium.launch();
for (const w of [1280,390]){
  const mob=w<500; const ctx=await b.newContext({viewport:{width:w,height:mob?844:900},isMobile:mob,hasTouch:mob});
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error'&&!/Failed to load/.test(m.text()))errs.push(m.text())});
  await p.route('**/*',ruta(URL,'pot3.html'));
  await p.goto(URL,{waitUntil:'networkidle',timeout:90000}); await p.waitForTimeout(800);
  const est=()=>p.evaluate(()=>{const g=k=>document.querySelector('#tl3-potencia [data-v="'+k+'"]')?.textContent;return {kw:g('kw'),n:g('n'),rec:g('rec'),dif:g('dif'),estado:g('estado'),saltado:document.querySelector('#tl3-potencia').classList.contains('is-saltado'),on:document.querySelectorAll('.tl3p-br[aria-pressed="true"]').length}});
  const r={ini:await est()};
  try{
    await p.locator('.tl3p-br[data-id="hor"]').click(); await p.locator('.tl3p-br[data-id="ter"]').click(); await p.waitForTimeout(300); r.marcar=await est();
    await p.locator('[data-x="hor"]').click(); await p.waitForTimeout(200); r.x2=await est();
    await p.selectOption('#tl3-potencia [data-kw]','3.45'); await p.waitForTimeout(300); r.kw345=await est();
    await p.locator('[data-sit="2"]').click(); await p.waitForTimeout(300); r.verano=await est();
    await p.fill('[data-otro]','1200'); await p.waitForTimeout(300); r.otro=await est();
    await p.locator('[data-acc="reset"]').click(); await p.waitForTimeout(200); r.reset=await est();
    await p.locator('[data-sit="0"]').click(); await p.locator('[data-acc="demo"]').click(); await p.waitForTimeout(9000); r.demo=await est(); r.msg=await p.locator('.tl3p-msg').textContent();
    r.desb=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  }catch(e){r.fallo=e.message.split('\n')[0]}
  await p.locator('#tl3-potencia').screenshot({path:`pot3-${w}.jpg`,type:'jpeg',quality:70});
  console.log(w,JSON.stringify(r)); console.log('ERRORES:',errs.join(' | ')||'ninguno');
  await ctx.close();
}
await b.close();
