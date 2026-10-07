import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs');
const URL='https://tuluzencasa.com/calculadora-consumo-electrico/';
const [,, dir, variantes, widths] = process.argv;
const b=await chromium.launch(); const cache=new Map();
for (const v of variantes.split(',')) for (const w of widths.split(',').map(Number)){
  const mob=w<500; const ctx=await b.newContext({viewport:{width:w,height:mob?844:900},isMobile:mob,hasTouch:mob});
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push('console:'+m.text().slice(0,150)+' @'+(m.location().url||'').slice(0,90))});p.on('requestfailed',q=>errs.push('fail:'+q.url().slice(0,90)));
  await p.route('**/*',async route=>{const rq=route.request(),u=rq.url();
    if(rq.resourceType()==='document'&&u.split('?')[0]===URL) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:fs.readFileSync(`${dir}/con-${v}.html`,'utf8')});
    if(/googlesyndication|doubleclick|adtrafficquality|google-analytics|googletagmanager/.test(u)) return route.abort();
    try{let c=cache.get(u);if(!c){const r=await fetch(u);const hd={};r.headers.forEach((vv,kk)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(kk))hd[kk]=vv;});c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())};cache.set(u,c);}await route.fulfill(c);}catch(e){await route.abort();}});
  await p.goto(URL,{waitUntil:'networkidle',timeout:90000}); await p.waitForTimeout(600);
  const r={};
  const est=()=>p.evaluate(()=>({ap:document.querySelectorAll('#tlc-ap option').length,kw:document.querySelectorAll('#tlc-kw option').length,lista:document.querySelectorAll('#tlc-lista>li').length,fac:document.getElementById('tlc-fac').textContent,kwh:document.getElementById('tlc-kwh').textContent,tips:document.getElementById('tlc-tips').children.length}));
  r.ini=await est();
  try{
    await p.click('#tlc-vac'); r.vaciar=await est();
    await p.selectOption('#tlc-ap','lav').catch(async()=>{await p.selectOption('#tlc-ap',{index:3})});
    await p.click('#tlc-add'); r.anadir=await est();
    await p.click('#tlc-ej'); r.ejemplo=await est();
    await p.selectOption('#tlc-kw',{index:0}); r.potencia=await est();
    await p.click('#tlc-t-h'); r.horas=await est();
    const q=p.locator('.tlc-q').first(); await q.scrollIntoViewIfNeeded(); await q.click(); r.rapido=await est();
  }catch(e){r.fallo=e.message.split('\n')[0]}
  await p.screenshot({path:`${dir}/con-${v}-${w}.jpg`,type:'jpeg',quality:60,fullPage:false});
  console.log(v,w,JSON.stringify(r),'ERR:',errs.join(' | ')||'-');
  await ctx.close();
}
await b.close();
