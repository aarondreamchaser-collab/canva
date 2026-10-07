import {chromium,fs,ruta} from './comun.mjs';
const P={con:['https://tuluzencasa.com/calculadora-consumo-electrico/','con3.html','#tl3-consumo'],pot:['https://tuluzencasa.com/calculadora-potencia-contratada/','pot3.html','#tl3-potencia']};
const b=await chromium.launch();
for (const k of Object.keys(P)){ const ctx=await b.newContext({viewport:{width:1280,height:900}}); const p=await ctx.newPage(); await p.route('**/*',ruta(P[k][0],P[k][1]));
  await p.goto(P[k][0],{waitUntil:'networkidle',timeout:90000}); const out=[];
  for (const w of [1400,1280,1100,1025,1024,900,769,768,700,601,600,480,390,360]){await p.setViewportSize({width:w,height:900});await p.waitForTimeout(400);
    out.push(w+':'+await p.evaluate(s=>Math.round(document.querySelector(s).getBoundingClientRect().height),P[k][2]));}
  console.log(k,out.join(' ')); await ctx.close();}
await b.close();
