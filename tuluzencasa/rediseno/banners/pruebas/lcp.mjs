import {chromium,abrir,disp} from './comun.mjs';
const b=await chromium.launch();
const init=()=>{window.__l=[];new PerformanceObserver(l=>{for(const e of l.getEntries()) window.__l.push([Math.round(e.startTime),e.element?e.element.nodeName+'.'+e.element.className:'?',e.size])}).observe({type:'largest-contentful-paint',buffered:true});};
for (const [dn,opt] of Object.entries(disp)) for (const v of ['base','fx']) {const r=[];for(let i=0;i<3;i++){
  const ctx=await b.newContext(opt); const p=await abrir(ctx,'home',v,{init}); await p.waitForTimeout(3000);
  r.push(JSON.stringify(await p.evaluate(()=>window.__l.at(-1)))); await ctx.close();}
  console.log(dn,v,r.join(' '));}
await b.close();
