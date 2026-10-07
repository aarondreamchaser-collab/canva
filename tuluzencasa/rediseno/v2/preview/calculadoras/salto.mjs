import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs'); const U='https://tuluzencasa.com/calculadora-consumo-electrico/';
const b=await chromium.launch(); const cache=new Map();
for (const w of [1280,390]){
  const mob=w<500; const ctx=await b.newContext({viewport:{width:w,height:mob?844:900},isMobile:mob,hasTouch:mob}); const p=await ctx.newPage();
  await p.route('**/*',async route=>{const rq=route.request(),u=rq.url();
    if(rq.resourceType()==='document'&&u.split('?')[0]===U) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:fs.readFileSync('con-final.html','utf8')});
    if(/googlesyndication|doubleclick|adtrafficquality|google-analytics|googletagmanager/.test(u)) return route.abort();
    try{let c=cache.get(u);if(!c){const r=await fetch(u);const hd={};r.headers.forEach((vv,kk)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(kk))hd[kk]=vv;});c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())};cache.set(u,c);}await route.fulfill(c);}catch(e){await route.abort();}});
  await p.goto(U,{waitUntil:'networkidle',timeout:90000});
  const q=p.locator('.tlc-q').first(); await q.scrollIntoViewIfNeeded(); await q.click(); await p.waitForTimeout(1500);
  const r=await p.evaluate(()=>{const a=document.getElementById('tlc-app').getBoundingClientRect().top;const hd=document.querySelector('.site-header').getBoundingClientRect();return {app:Math.round(a),cabecera:Math.round(hd.bottom),pos:getComputedStyle(document.querySelector('.site-header')).position}});
  await p.screenshot({path:`salto-${w}.jpg`,type:'jpeg',quality:55});
  console.log(w,JSON.stringify(r)); await ctx.close();
}
await b.close();
