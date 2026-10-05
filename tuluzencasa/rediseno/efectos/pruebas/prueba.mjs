import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs'); const b=await chromium.launch(); const cache=new Map(); const out={};
const URLS={art:'https://tuluzencasa.com/cuanto-consume-termo-electrico/',home:'https://tuluzencasa.com/',calc:'https://tuluzencasa.com/calculadora-consumo-electrico/'};
async function abrir(ctx,file,url){
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  const html=fs.readFileSync(file,'utf8');
  await p.addInitScript(()=>{window.__cls=0;window.__lt=[];window.__raf=0;const r=window.requestAnimationFrame;window.requestAnimationFrame=f=>{window.__raf++;return r(f)};
    new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput) window.__cls+=e.value}).observe({type:'layout-shift',buffered:true});
    new PerformanceObserver(l=>{for(const e of l.getEntries()) window.__lt.push(Math.round(e.duration))}).observe({type:'longtask',buffered:true});});
  await p.route('**/*', async route=>{const rq=route.request(); const u=rq.url();
    if(rq.resourceType()==='document'&&u.startsWith(url)) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:html});
    if(/googlesyndication|doubleclick|adtrafficquality|google-analytics|googletagmanager/.test(u)) return route.abort(); // sin anuncios en la prueba
    try{let c=cache.get(u); if(!c){const r=await fetch(u); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} await route.fulfill(c);}catch(e){await route.abort();}});
  await p.goto(url,{waitUntil:'networkidle',timeout:120000}); return [p,errs];
}
const disp={escritorio:{viewport:{width:1280,height:800}},tablet:{viewport:{width:820,height:1180},isMobile:true,hasTouch:true,deviceScaleFactor:2},movil:{viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2}};
for (const [dn,opt] of Object.entries(disp)){
  const ctx=await b.newContext(opt);
  for (const k of ['art','home','calc']) for (const v of ['base','fx']){
    const [p,errs]=await abrir(ctx,`${k}_${v}.html`,URLS[k]);
    const info=await p.evaluate(()=>({fine:matchMedia('(pointer: fine)').matches, canvasAlCargar:!!document.getElementById("tl-chispas"), barra:!!document.getElementById('tl-progreso'), cuentan:document.querySelectorAll('td.tl-cuenta').length,
      ms:(()=>{const a=performance.getEntriesByName('fx-ini')[0],b=performance.getEntriesByName('fx-fin')[0];return a&&b?+(b.startTime-a.startTime).toFixed(1):null})(), cursor:getComputedStyle(document.body).cursor.slice(0,30)}));
    // recorrido: mover el ratón (solo escritorio) y bajar por la página
    if(dn==='escritorio'){ for(let i=0;i<30;i++){ await p.mouse.move(300+i*20,300+Math.sin(i/3)*80); await p.waitForTimeout(16);} }
    const altura=await p.evaluate(()=>document.body.scrollHeight);
    for(let y=0;y<altura;y+=600){ await p.evaluate(y=>scrollTo(0,y),y); await p.waitForTimeout(120); }
    await p.waitForTimeout(900);
    const conLienzo=await p.evaluate(()=>!!document.getElementById('tl-chispas')); const r0=await p.evaluate(()=>window.__raf); await p.waitForTimeout(1000); const r1=await p.evaluate(()=>window.__raf);
    const fin=await p.evaluate(()=>({cls:+window.__cls.toFixed(4), lt:window.__lt, finales:[...document.querySelectorAll('td.tl-cuenta')].every(td=>!td.classList.contains('tl-anim')&&!td.hasAttribute('data-n')), visibles:[...document.querySelectorAll('td.tl-cuenta')].slice(0,3).map(t=>t.textContent)}));
    out[`${k}/${dn}/${v}`]={...info,...fin,lienzoTrasMover:conLienzo,rafReposo1s:r1-r0,errs:errs.length};
    await p.close();
  }
  await ctx.close();
}
await b.close();
for (const [k,v] of Object.entries(out)) console.log(k.padEnd(22),JSON.stringify(v));
