import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs'); const b=await chromium.launch(); const cache=new Map(); const out={};
const URLS={home:'https://tuluzencasa.com/',art:'https://tuluzencasa.com/cuanto-consume-lavadora/',art2:'https://tuluzencasa.com/que-potencia-contratar/'};
const RM=process.argv.includes('--rm');
async function abrir(ctx,file,url){
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  if(RM) await p.emulateMedia({reducedMotion:'reduce'});
  const html=fs.readFileSync(file,'utf8');
  await p.addInitScript(()=>{window.__cls=0;window.__s=[];window.__lt=[];
    new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput){window.__cls+=e.value;window.__s.push(e.sources.map(s=>s.node?s.node.nodeName+'.'+(s.node.className||''):'?').join(','))}}).observe({type:'layout-shift',buffered:true});
    new PerformanceObserver(l=>{for(const e of l.getEntries()) window.__lt.push(Math.round(e.duration))}).observe({type:'longtask',buffered:true});});
  await p.route('**/*', async route=>{const rq=route.request(); const u=rq.url();
    if(rq.resourceType()==='document'&&u.startsWith(url)) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:html});
    if(/googlesyndication|doubleclick|adtrafficquality|google-analytics|googletagmanager/.test(u)) return route.abort();
    try{let c=cache.get(u); if(!c){const r=await fetch(u); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} await route.fulfill(c);}catch(e){await route.abort();}});
  const t0=Date.now(); await p.goto(url,{waitUntil:'networkidle',timeout:120000});
  return [p,errs];
}
const disp={escritorio:{viewport:{width:1280,height:800}},tablet:{viewport:{width:820,height:1180},isMobile:true,hasTouch:true,deviceScaleFactor:2},movil:{viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2}};
for (const [dn,opt] of Object.entries(disp)){
  const ctx=await b.newContext(opt);
  for (const k of Object.keys(URLS)) for (const v of ['base','fx']){
    const [p,errs]=await abrir(ctx,`${k}_${v}.html`,URLS[k]);
    const nav=await p.evaluate(()=>{const n=performance.getEntriesByType('navigation')[0];const fcp=performance.getEntriesByName('first-contentful-paint')[0];return {dcl:Math.round(n.domContentLoadedEventEnd),load:Math.round(n.loadEventEnd),fcp:fcp?Math.round(fcp.startTime):null}});
    const info=await p.evaluate(()=>({ms:(()=>{const a=performance.getEntriesByName('tlb-ini')[0],b=performance.getEntriesByName('tlb-fin')[0];return a&&b?+(b.startTime-a.startTime).toFixed(1):null})(),
      barra:!!document.querySelector('.tlb-barra'),cinta:!!document.querySelector('.tlb-cinta'),franja:!!document.querySelector('.tlb-franja'),tarjeta:(()=>{const t=document.querySelector('.tlb-tarjeta');if(!t)return null;const prev=t.previousElementSibling,next=t.nextElementSibling;return (t.querySelector('.tlb-bt')||{}).textContent+' | antes:'+(prev&&(prev.className||prev.tagName))+' | después:'+(next&&next.textContent.slice(0,40))})(),
      faq:document.querySelectorAll('.tlb-faq-b').length,ocultos:document.querySelectorAll('.tlb-oculto').length}));
    const altura=await p.evaluate(()=>document.body.scrollHeight);
    const fijoVisto=[];
    for(let y=0;y<altura;y+=500){ await p.evaluate(y=>scrollTo(0,y),y); await p.waitForTimeout(110); fijoVisto.push(await p.evaluate(()=>document.documentElement.classList.contains('tlb-fijo-on')?1:0)); }
    await p.waitForTimeout(800);
    const fin=await p.evaluate(()=>({cls:+window.__cls.toFixed(4),src:window.__s.slice(0,4),lt:window.__lt,ocultosFin:document.querySelectorAll('.tlb-oculto').length,guias:(document.querySelector('[data-tlb="guias"]')||{}).textContent,act:(document.querySelector('.tlb-act')||{}).textContent,anim:document.getAnimations().length}));
    out[`${k}/${dn}/${v}`]={...nav,...info,...fin,fijo:fijoVisto.join(''),errs:errs.join('|')};
    await p.close();
  }
  await ctx.close();
}
await b.close();
for (const [k,v] of Object.entries(out)) console.log(k.padEnd(20),JSON.stringify(v));
