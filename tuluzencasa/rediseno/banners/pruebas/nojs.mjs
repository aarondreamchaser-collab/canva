import {chromium,abrir,disp} from './comun.mjs';
const b=await chromium.launch();
for (const k of ['home','art','art2']){
  const ctx=await b.newContext({...disp.escritorio,javaScriptEnabled:false}); const p=await abrir(ctx,k); await p.waitForTimeout(1500);
  console.log(k,JSON.stringify(await p.evaluate(()=>{const o=s=>[...document.querySelectorAll(s)].map(e=>getComputedStyle(e).opacity).filter(x=>x!=='1').length;
    return {h1:document.querySelector('h1')&&getComputedStyle(document.querySelector('h1')).opacity,noOpacos:o('h1,h2,h3,p,li,table,figure,.tl-dato,section'),
      linea:[...document.querySelectorAll('.entry-content>h2')].map(h=>getComputedStyle(h,'::after').transform).slice(0,2),txt:document.body.innerText.length}})));
  await ctx.close();
}
await b.close();
