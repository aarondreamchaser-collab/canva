import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs'); const b=await chromium.launch(); const cache=new Map();
async function abrir(ctx,file,url){ const p=await ctx.newPage(); const html=fs.readFileSync(file,'utf8');
 await p.route('**/*', async route=>{const rq=route.request(); const u=rq.url();
  if(rq.resourceType()==='document'&&u.startsWith(url)) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:html});
  if(/googlesyndication|doubleclick|adtrafficquality/.test(u)) return route.abort();
  try{let c=cache.get(u); if(!c){const r=await fetch(u); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} await route.fulfill(c);}catch(e){await route.abort();}});
 await p.goto(url,{waitUntil:'networkidle'}); return p; }
// 1) reducir movimiento en escritorio
let ctx=await b.newContext({viewport:{width:1280,height:800},reducedMotion:'reduce'});
let p=await abrir(ctx,'art_fx.html','https://tuluzencasa.com/cuanto-consume-termo-electrico/');
await p.mouse.move(400,300); await p.mouse.move(500,350); await p.waitForTimeout(1600);
await p.evaluate(()=>scrollTo(0,1500)); await p.waitForTimeout(500);
console.log('reducir movimiento:',JSON.stringify(await p.evaluate(()=>({cursor:getComputedStyle(document.body).cursor, lienzo:!!document.getElementById('tl-chispas'), barra:!!document.getElementById('tl-progreso'), cuentan:document.querySelectorAll('td.tl-cuenta').length, animando:document.querySelectorAll('td.tl-anim').length}))));
await ctx.close();
// 2) cursores sobre elementos interactivos (escritorio con ratón)
ctx=await b.newContext({viewport:{width:1280,height:800}});
p=await abrir(ctx,'calc_fx.html','https://tuluzencasa.com/calculadora-consumo-electrico/');
console.log('cursores calculadora:',JSON.stringify(await p.evaluate(()=>{const c=s=>{const e=document.querySelector(s);return e?getComputedStyle(e).cursor.slice(0,24):'(no hay)'};
 return {cuerpo:c('body'),enlace:c('a'),boton:c('#tlc-app button'),inputNumero:c('#tlc-app input[type=number]'),inputTexto:c('#tlc-app input:not([type])')||c('#tlc-app input[type=text]'),select:c('#tlc-app select'),checkbox:c('#tlc-app input[type=checkbox]'),hamburguesa:c('.menu-toggle')}})));
await ctx.close(); await b.close();
