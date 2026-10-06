import {chromium,abrir,disp} from './comun.mjs';
const b=await chromium.launch();
const init=()=>{window.__l=[];new PerformanceObserver(l=>{for(const e of l.getEntries()) window.__l.push([Math.round(e.startTime),e.element?e.element.nodeName+'.'+e.element.className.slice(0,40):'?',e.size])}).observe({type:'largest-contentful-paint',buffered:true});};
for(let i=0;i<2;i++){const ctx=await b.newContext(disp.tablet); const p=await abrir(ctx,'home','fx',{init});
const antes=await p.evaluate(()=>JSON.stringify(window.__l));
const alt=await p.evaluate(()=>document.body.scrollHeight);
for(let y=0;y<alt;y+=500){await p.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y);await p.waitForTimeout(90);}
await p.waitForTimeout(1000);
console.log('antes de bajar',antes,'\n después',JSON.stringify(await p.evaluate(()=>window.__l.slice(-2)))); await ctx.close();}
// con desplazamiento real (rueda del ratón): el LCP se cierra
const ctx=await b.newContext({viewport:{width:820,height:1180}}); const p=await abrir(ctx,'home','fx',{init});
await p.mouse.move(400,600); for(let i=0;i<20;i++){await p.mouse.wheel(0,500);await p.waitForTimeout(90)}
await p.waitForTimeout(1000); console.log('rueda',JSON.stringify(await p.evaluate(()=>window.__l.slice(-1))));
await b.close();
