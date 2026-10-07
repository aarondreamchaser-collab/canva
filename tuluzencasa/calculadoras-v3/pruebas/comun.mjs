import { createRequire } from 'module';
const require = createRequire(import.meta.url);
export const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
export const fs=require('fs');
const cache=new Map();
export function ruta(url,file){return async route=>{const rq=route.request(),u=rq.url();
  if(rq.resourceType()==='document'&&u.split('?')[0].split('#')[0]===url) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:fs.readFileSync(file,'utf8')});
  if(/googlesyndication|doubleclick|adtrafficquality|google-analytics|googletagmanager|fundingchoices/.test(u)) return route.abort();
  try{let c=cache.get(u);if(!c){await new Promise(r=>setTimeout(r,120));const r=await fetch(u,{headers:{'User-Agent':'Mozilla/5.0 tl-audit'}});const hd={};r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;});c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())};if(r.status===200)cache.set(u,c);}await route.fulfill(c);}catch(e){await route.abort();}}}
