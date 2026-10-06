import { createRequire } from 'module';
const require = createRequire(import.meta.url);
export const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
export const fs=require('fs');
export const URLS={home:'https://tuluzencasa.com/',art:'https://tuluzencasa.com/cuanto-consume-lavadora/',art2:'https://tuluzencasa.com/que-potencia-contratar/',calc:'https://tuluzencasa.com/calculadora-consumo-electrico/',pot:'https://tuluzencasa.com/calculadora-potencia-contratada/'};
export const disp={escritorio:{viewport:{width:1280,height:800}},tablet:{viewport:{width:820,height:1180},isMobile:true,hasTouch:true,deviceScaleFactor:2},movil:{viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2}};
const cache=new Map();
export async function abrir(ctx,k,v='fx',{rm=false,init=null,wait='networkidle'}={}){
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); const url=URLS[k];
  if(rm) await p.emulateMedia({reducedMotion:'reduce'});
  if(init) await p.addInitScript(init);
  const html=fs.readFileSync(new URL(`./${k}_${v}.html`,import.meta.url),'utf8');
  await p.route('**/*', async route=>{const rq=route.request(); const u=rq.url();
    if(rq.resourceType()==='document'&&u.startsWith(url)) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:html});
    if(/googlesyndication|doubleclick|adtrafficquality|google-analytics|googletagmanager/.test(u)) return route.abort();
    try{let c=cache.get(u); if(!c){const r=await fetch(u); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} await route.fulfill(c);}catch(e){await route.abort();}});
  await p.goto(url,{waitUntil:wait,timeout:120000});
  p.errs=errs; return p;
}
