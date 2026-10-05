import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const b=await chromium.launch(); const cache=new Map();
const urls={portada:'https://tuluzencasa.com/',articulo:'https://tuluzencasa.com/tramos-horarios-luz/',consumo:'https://tuluzencasa.com/calculadora-consumo-electrico/',potencia:'https://tuluzencasa.com/calculadora-potencia-contratada/'};
const res={};
for (const [w,hgt,nombre] of [[1280,900,'escritorio'],[820,1180,'tablet'],[390,844,'movil']]){
 const mob=w<500; const ctx=await b.newContext({viewport:{width:w,height:hgt},deviceScaleFactor:mob?2:1,isMobile:mob,hasTouch:w<=1024});
 for (const [k,u] of Object.entries(urls)){
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  let bytes=0,reqs=0;
  await p.route('**/*', async route=>{const rq=route.request(); const uu=rq.url();
   try{let c=cache.get(uu); if(!c||rq.resourceType()==='document'){const r=await fetch(uu,{headers:{'user-agent':'Mozilla/5.0 tlc-check'}}); const hd={}; r.headers.forEach((v,kk)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(kk))hd[kk]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(uu,c);} bytes+=c.body.length; reqs++; await route.fulfill(c);}catch(e){await route.abort();}});
  await p.goto(u,{waitUntil:'networkidle',timeout:120000});
  const m=await p.evaluate(()=>{const t=document.querySelector('#mobile-menu-control-wrapper .menu-toggle');const lis=[...document.querySelectorAll('#menu-principal > li')].filter(l=>l.offsetParent);
   const q=s=>document.querySelector(s);
   return {ov:document.documentElement.scrollWidth-innerWidth, header:Math.round(q('#masthead').getBoundingClientRect().height), hamburguesa:getComputedStyle(t).display!=='none', filasMenu:[...new Set(lis.map(l=>Math.round(l.getBoundingClientRect().top)))].length,
     calcConsumo: q('.tlc-lcd-big')? q('.tlc-lcd-big').textContent.trim().replace(/\s+/g,' ') : null,
     calcPotencia: q('#tlp-app')? (q('#tlp-app').innerText.match(/\d+,\d+\s*kW/)||[''])[0] : null,
     migas: !!q('.rank-math-breadcrumb'), relacionados: document.querySelectorAll('.tl-rel li').length}});
  // interacción: calculadora de consumo, cargar ejemplo
  if(k==='consumo'){ const btn=await p.$('text=Cargar ejemplo'); if(btn){await btn.click(); await p.waitForTimeout(400); m.trasEjemplo=await p.evaluate(()=>document.querySelector('.tlc-lcd-big').textContent.trim().replace(/\s+/g,' '));} }
  if(k==='potencia'){ const cb=await p.$$('#tlp-app input[type=checkbox]'); if(cb.length>2){ await cb[2].check({force:true}).catch(()=>{}); await p.waitForTimeout(300); m.trasMarcar=await p.evaluate(()=>(document.querySelector('#tlp-app').innerText.match(/\d+,\d+\s*kW/g)||[]).slice(0,3)); } }
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){scrollTo(0,y);await new Promise(r=>setTimeout(r,50));}scrollTo(0,0)}); await p.waitForTimeout(700);
  await p.screenshot({path:`final/${k}_${nombre}.png`,fullPage:true});
  await p.screenshot({path:`final/${k}_${nombre}_arriba.png`});
  if(k==='articulo' && w<=820){ await p.click('#mobile-menu-control-wrapper .menu-toggle').catch(()=>{}); await p.waitForTimeout(300); await p.screenshot({path:`final/menu_${nombre}.png`}); }
  if(k==='articulo' && w===1280){ await p.hover('#menu-item-183'); await p.waitForTimeout(400); await p.screenshot({path:`final/menu_escritorio.png`,clip:{x:0,y:0,width:1280,height:300}}); }
  res[`${k}@${nombre}`]={...m,errs,kb:Math.round(bytes/1024),reqs}; await p.close();
 }
 await ctx.close();
}
await b.close(); for(const [k,v] of Object.entries(res)) console.log(k,JSON.stringify(v));
