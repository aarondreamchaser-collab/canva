import {chromium,abrir,disp} from './comun.mjs';
const b=await chromium.launch();
for (const [dn,opt] of Object.entries(disp)){
  const ctx=await b.newContext(opt); const p=await abrir(ctx,'home');
  const r=await p.evaluate(()=>{const l=document.querySelector('.site-header .site-logo'),i=l.querySelector('img'),s=document.querySelector('.tlb-luz');const R=e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(n=>+n.toFixed(1))};return {logo:R(l),img:R(i),luz:s&&R(s),clave:!!document.querySelector('.tlb-clave'),errs:0}});
  console.log(dn,JSON.stringify(r),p.errs.join('|'));
  // zoom on logo with overlay forced visible
  await p.evaluate(()=>{const s=document.querySelector('.tlb-luz');s.classList.remove('ini');s.style.opacity=1});
  const c=r.img; await p.screenshot({path:`/tmp/claude-0/-home-user-canva/557847bc-71e6-5871-a563-54935582d0d3/scratchpad/logo-${dn}.png`,clip:{x:c[0]-4,y:c[1]-4,width:c[2]+8,height:c[3]+8}});
  await ctx.close();
}
await b.close();
