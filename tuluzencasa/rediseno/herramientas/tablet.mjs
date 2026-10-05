import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const b=await chromium.launch(); const cache=new Map();
for (const w of [390,768,769,820,900,1024,1025,1280]){
 const mob=w<500; const ctx=await b.newContext({viewport:{width:w,height:900},isMobile:mob,hasTouch:w<=1024,deviceScaleFactor:1}); const p=await ctx.newPage();
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.route('**/*', async route=>{const u=route.request().url(); if(u.startsWith('http://localhost')) return route.continue();
  try{let c=cache.get(u); if(!c){const r=await fetch(u); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} await route.fulfill(c);}catch(e){await route.abort();}});
 await p.goto('http://localhost:8765/t_live_new.html',{waitUntil:'networkidle'});
 const est=()=>p.evaluate(()=>{const t=document.querySelector('#mobile-menu-control-wrapper .menu-toggle');const lis=[...document.querySelectorAll('#menu-principal > li')].filter(l=>l.offsetParent);
   const r=e=>{const x=document.querySelector(e);if(!x||!x.offsetParent)return null;const b=x.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)]};
   return {toggle:getComputedStyle(t).display, header:Math.round(document.querySelector('#masthead').getBoundingClientRect().height), filas:[...new Set(lis.map(l=>Math.round(l.getBoundingClientRect().top)))].length, items:lis.length, logo:r('.main-title'), lupaMovil:r('#mobile-menu-control-wrapper .menu-bar-item'), hamb:r('#mobile-menu-control-wrapper .menu-toggle'), ov:document.documentElement.scrollWidth-innerWidth}});
 const r={antes:await est()};
 if(w<=1024){
   await p.screenshot({path:`capturas/tab_${w}_cerrado.png`,clip:{x:0,y:0,width:w,height:160}});
   await p.click('#mobile-menu-control-wrapper .menu-toggle'); await p.waitForTimeout(300);
   r.abierto=await est();
   await p.click('#menu-item-151 > a .dropdown-menu-toggle'); await p.waitForTimeout(300);
   r.submenu=await p.evaluate(()=>{const s=document.querySelector('#menu-item-151 .sub-menu');const b=s.getBoundingClientRect();return {visible:getComputedStyle(s).visibility, alto:Math.round(b.height), hijos:[...s.querySelectorAll('a')].map(a=>a.offsetParent?a.textContent:null)}});
   await p.screenshot({path:`capturas/tab_${w}_abierto.png`,fullPage:false});
   await p.click('#mobile-menu-control-wrapper .menu-toggle'); await p.waitForTimeout(200);
   await p.click('#mobile-menu-control-wrapper .menu-bar-item a'); await p.waitForTimeout(400);
   r.buscador=await p.evaluate(()=>{const m=document.getElementById('gp-search');return m?m.classList.contains('gp-modal--open')||getComputedStyle(m).display!=='none':null});
 } else { await p.screenshot({path:`capturas/tab_${w}_cerrado.png`,clip:{x:0,y:0,width:w,height:160}}); }
 r.errs=errs; console.log(w,JSON.stringify(r)); await ctx.close();
}
await b.close();
