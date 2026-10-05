import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const b=await chromium.launch(); const cache=new Map(); const fs=require('fs');
const local=fs.readFileSync(process.argv[2],'utf8'); const tag=process.argv[3];
for (const w of [1440,1280,1200,1100,1025,1024,820,768,390,360]){
 const mob=w<500; const ctx=await b.newContext({viewport:{width:w,height:700},deviceScaleFactor:mob?2:1,isMobile:mob,hasTouch:w<=1024}); const p=await ctx.newPage();
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.route('**/*', async route=>{const rq=route.request(); const u=rq.url();
  if(rq.resourceType()==='document') return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:local});
  try{let c=cache.get(u); if(!c){const r=await fetch(u); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} await route.fulfill(c);}catch(e){await route.abort();}});
 await p.goto('https://tuluzencasa.com/tramos-horarios-luz/',{waitUntil:'networkidle'});
 const r=await p.evaluate(()=>{const q=s=>document.querySelector(s);const bx=e=>{if(!e||!e.offsetParent)return null;const b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top),Math.round(b.width),Math.round(b.height)]};
   const lis=[...document.querySelectorAll('#menu-principal > li, #site-navigation .menu-bar-item')].filter(l=>l.offsetParent);
   return {header:Math.round(q('#masthead').getBoundingClientRect().height), logo:bx(q('.header-image')), titulo:bx(q('.main-title')), filas:[...new Set(lis.map(l=>Math.round(l.getBoundingClientRect().top)))].length, hamb:bx(q('#mobile-menu-control-wrapper .menu-toggle')), lupa:bx(q('#mobile-menu-control-wrapper .menu-bar-item')), ov:document.documentElement.scrollWidth-innerWidth}});
 console.log(w,JSON.stringify(r),errs.length?errs:'');
 await p.screenshot({path:`logo/${tag}_${w}.png`,clip:{x:0,y:0,width:w,height:120}});
 if(w===820||w===390){await p.click('#mobile-menu-control-wrapper .menu-toggle'); await p.waitForTimeout(300); await p.screenshot({path:`logo/${tag}_${w}_menu.png`,clip:{x:0,y:0,width:w,height:520}});}
 await ctx.close();}
await b.close();
