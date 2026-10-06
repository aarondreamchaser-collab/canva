import {chromium,abrir,disp,URLS} from './comun.mjs';
const b=await chromium.launch(); const RM=process.argv.includes('--rm'); const out=[];
const init=()=>{window.__cls=0;window.__s=[];window.__lt=[];window.__lcp=0;
  new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput){window.__cls+=e.value;window.__s.push(e.sources.map(s=>s.node?s.node.nodeName+'.'+(s.node.className||''):'?').join(','))}}).observe({type:'layout-shift',buffered:true});
  new PerformanceObserver(l=>{for(const e of l.getEntries()) window.__lt.push(Math.round(e.duration))}).observe({type:'longtask',buffered:true});
  new PerformanceObserver(l=>{for(const e of l.getEntries()) window.__lcp=Math.round(e.startTime)}).observe({type:'largest-contentful-paint',buffered:true});};
for (const [dn,opt] of Object.entries(disp)){
  const ctx=await b.newContext(opt);
  for (const k of Object.keys(URLS)) for (const v of ['base','fx']){
    const p=await abrir(ctx,k,v,{rm:RM,init});
    const nav=await p.evaluate(()=>{const n=performance.getEntriesByType('navigation')[0];const f=performance.getEntriesByName('first-contentful-paint')[0];
      const a=performance.getEntriesByName('tlb-ini')[0],z=performance.getEntriesByName('tlb-fin')[0];
      return {fcp:f?Math.round(f.startTime):null,dcl:Math.round(n.domContentLoadedEventEnd),ms:a&&z?+(z.startTime-a.startTime).toFixed(1):null,
        luz:!!document.querySelector('.tlb-luz'),clave:!!document.querySelector('.tlb-clave'),ocultos:document.querySelectorAll('.tlb-oculto').length}});
    const alt=await p.evaluate(()=>document.body.scrollHeight);
    for(let y=0;y<alt;y+=500){await p.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y);await p.waitForTimeout(90);}
    await p.waitForTimeout(1200);
    const fin=await p.evaluate(()=>({lcp:window.__lcp,cls:+window.__cls.toFixed(4),src:window.__s.slice(0,3),lt:window.__lt,ocultosFin:document.querySelectorAll('.tlb-oculto').length,
      anims:document.getAnimations().filter(a=>a.playState==='running').map(a=>a.animationName||'t').join(',')}));
    out.push([`${k}/${dn}/${v}`,{...nav,...fin,errs:p.errs.filter(e=>!/Unexpected token '<'/.test(e)).join('|')}]);
    await p.close();
  }
  await ctx.close();
}
await b.close();
for (const [k,v] of out) console.log(k.padEnd(22),JSON.stringify(v));
