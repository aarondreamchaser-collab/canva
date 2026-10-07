import {chromium,fs,ruta} from './comun.mjs';
const P={con:['https://tuluzencasa.com/calculadora-consumo-electrico/','con3.html','#tl3-consumo'],pot:['https://tuluzencasa.com/calculadora-potencia-contratada/','pot3.html','#tl3-potencia']};
const b=await chromium.launch();
for (const k of Object.keys(P)) for (const w of [1280,390]){
  const mob=w<500; const ctx=await b.newContext({viewport:{width:w,height:mob?844:900},isMobile:mob,hasTouch:mob});
  const p=await ctx.newPage();
  await p.addInitScript(()=>{window.__cls=0;window.__src=[];new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput){window.__cls+=e.value;window.__src.push(e.sources?.map(s=>s.node?.className||s.node?.nodeName).join(','))}}).observe({type:'layout-shift',buffered:true});});
  await p.route('**/*',ruta(P[k][0],P[k][1]));
  await p.goto(P[k][0],{waitUntil:'networkidle',timeout:90000}); await p.waitForTimeout(1500);
  const r=await p.evaluate(s=>({cls:+window.__cls.toFixed(4),src:window.__src.slice(0,4),alto:Math.round(document.querySelector(s).getBoundingClientRect().height),top:Math.round(document.querySelector(s).getBoundingClientRect().top+scrollY)}),P[k][2]);
  console.log(k,w,JSON.stringify(r));
  await ctx.close();
}
await b.close();
