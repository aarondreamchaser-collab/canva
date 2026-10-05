import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs'); const b=await chromium.launch(); const cache=new Map();
const URL='https://tuluzencasa.com/cuanto-consume-termo-electrico/';
async function abrir(ctx,file){ const p=await ctx.newPage(); const html=fs.readFileSync(file,'utf8');
 await p.route('**/*', async route=>{const rq=route.request(); const u=rq.url();
  if(rq.resourceType()==='document'&&u.startsWith(URL)) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:html});
  if(/googlesyndication|doubleclick|adtrafficquality/.test(u)) return route.abort();
  try{let c=cache.get(u); if(!c){const r=await fetch(u); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} await route.fulfill(c);}catch(e){await route.abort();}});
 await p.goto(URL,{waitUntil:'networkidle'}); await p.waitForTimeout(600); return p; }
const CUR="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath d='M13.5 1.5 3.5 13.5h6.5l-1.5 9 10-12.5h-6.5z' fill='%23F2C230' stroke='%2318222E' stroke-width='1.6' stroke-linejoin='round'/%3E%3C/svg%3E";
for (const [n,opt] of [['escritorio',{viewport:{width:1280,height:800}}],['tablet',{viewport:{width:820,height:1180},isMobile:true,hasTouch:true,deviceScaleFactor:1}],['movil',{viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2}]]){
 const ctx=await b.newContext(opt); const p=await abrir(ctx, n==='escritorio'?'art_fx.html':'art_fx.html');
 // ir a la primera tabla
 const y=await p.evaluate(()=>{const t=document.querySelector('.entry-content figure.wp-block-table');return t.getBoundingClientRect().top+scrollY-140});
 await p.evaluate(y=>scrollTo(0,y),y);
 if(n==='escritorio'){
   let x=0,yy=0; for(let i=0;i<16;i++){ x=560+i*18; yy=420+Math.sin(i/2.5)*40; await p.mouse.move(x,yy); await p.waitForTimeout(12);} 
   await p.waitForTimeout(120);
   await p.evaluate(([x,y,c])=>{const i=document.createElement('img');i.src=c;i.style.cssText=`position:fixed;left:${x-12}px;top:${y-2}px;width:24px;height:24px;z-index:2147483647;pointer-events:none`;document.body.appendChild(i)},[x,yy,CUR]);
 } else { await p.waitForTimeout(260); }
 await p.screenshot({path:`cap/${n}_animando.png`});
 await p.waitForTimeout(1200);
 await p.evaluate(()=>document.querySelectorAll('img[src^="data:image/svg"]').forEach(i=>i.remove()));
 await p.screenshot({path:`cap/${n}_final.png`});
 const caja=await p.$('.tl-dato'); await caja.scrollIntoViewIfNeeded(); await p.waitForTimeout(300); await caja.screenshot({path:`cap/${n}_dato.png`});
 await p.evaluate(()=>scrollTo(0,document.body.scrollHeight*0.55)); await p.waitForTimeout(400);
 await p.screenshot({path:`cap/${n}_barra.png`,clip:{x:0,y:0,width:opt.viewport.width,height:120}});
 await ctx.close();
}
await b.close();
