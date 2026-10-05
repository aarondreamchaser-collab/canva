import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs'); const b=await chromium.launch(); const cache=new Map();
const url='https://tuluzencasa.com/cuanto-consume-termo-electrico/'; const html=fs.readFileSync(process.argv[2],'utf8');
const ctx=await b.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2}); const p=await ctx.newPage();
await p.addInitScript(()=>{window.__s=[];new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput) window.__s.push({v:+e.value.toFixed(4),t:Math.round(e.startTime),src:e.sources.map(s=>{const n=s.node;return n?(n.nodeName+'.'+(n.className||'')+' '+(n.textContent||'').trim().slice(0,30)):'?'})})}).observe({type:'layout-shift',buffered:true});});
await p.route('**/*', async route=>{const rq=route.request(); const u=rq.url();
 if(rq.resourceType()==='document'&&u.startsWith(url)) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:html});
 if(/googlesyndication|doubleclick|adtrafficquality/.test(u)) return route.abort();
 try{let c=cache.get(u); if(!c){const r=await fetch(u); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} await route.fulfill(c);}catch(e){await route.abort();}});
await p.goto(url,{waitUntil:'networkidle'});
const h=await p.evaluate(()=>document.body.scrollHeight);
for(let y=0;y<h;y+=600){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(150);}
await p.waitForTimeout(900);
console.log(JSON.stringify(await p.evaluate(()=>window.__s),null,0));
await b.close();
