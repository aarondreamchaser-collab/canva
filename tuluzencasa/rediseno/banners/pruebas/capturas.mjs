import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs'); const b=await chromium.launch(); const cache=new Map(); const C='../capturas/';
const URLS={home:'https://tuluzencasa.com/',art:'https://tuluzencasa.com/cuanto-consume-lavadora/',art2:'https://tuluzencasa.com/que-potencia-contratar/'};
async function abrir(ctx,k){const p=await ctx.newPage();const url=URLS[k];const html=fs.readFileSync(`${k}_fx.html`,'utf8');
  await p.route('**/*', async route=>{const rq=route.request(); const u=rq.url();
    if(rq.resourceType()==='document'&&u.startsWith(url)) return route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:html});
    if(/googlesyndication|doubleclick|adtrafficquality|google-analytics|googletagmanager/.test(u)) return route.abort();
    try{let c=cache.get(u); if(!c){const r=await fetch(u); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} await route.fulfill(c);}catch(e){await route.abort();}});
  await p.goto(url,{waitUntil:'networkidle',timeout:120000});return p;}
const disp={escritorio:{viewport:{width:1280,height:800}},tablet:{viewport:{width:820,height:1180},isMobile:true,hasTouch:true,deviceScaleFactor:1},movil:{viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2}};
for (const [dn,opt] of Object.entries(disp)){
  const ctx=await b.newContext(opt);
  // portada arriba: barra, cinta y franja (bajamos lo justo para ver la franja y que se vea la cinta)
  let p=await abrir(ctx,'home');
  await p.evaluate(()=>{const f=document.querySelector('.tlb-franja');f.classList.remove('tlb-oculto');f.classList.add('tlb-visto')});
  await p.waitForTimeout(1500);
  const fy=await p.evaluate(()=>document.querySelector('.tlb-franja').getBoundingClientRect().bottom+scrollY);
  await p.screenshot({path:`${C}1-portada-${dn}.png`,clip:{x:0,y:0,width:opt.viewport.width,height:Math.min(fy+30,dn==='movil'?1500:1300)},fullPage:true});
  if(dn==='escritorio'){
    await p.waitForTimeout(4500); await p.screenshot({path:`${C}2-barra-mensaje-2.png`,clip:{x:0,y:0,width:1280,height:80}});
    const c=await p.evaluate(()=>{const e=document.querySelector('.tl-calc');e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();return {x:r.x,y:r.y}});
    await p.waitForTimeout(900); await p.mouse.move(c.x+60,c.y+60); await p.waitForTimeout(500);
    await p.screenshot({path:`${C}3-tarjetas-al-pasar-el-raton.png`});
  }
  await p.close();
  // artículo: tarjeta de calculadora
  for (const k of ['art','art2']){
    p=await abrir(ctx,k);
    await p.evaluate(()=>{const t=document.querySelector('.tlb-tarjeta');t.scrollIntoView({block:'center'})}); await p.waitForTimeout(1200);
    await p.screenshot({path:`${C}4-tarjeta-${k}-${dn}.png`});
    if(k==='art'){
      // botón fijo + volver arriba
      const h=await p.evaluate(()=>document.body.scrollHeight);
      for(let y=0;y<h;y+=200){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(80);
        if(await p.evaluate(()=>document.documentElement.classList.contains('tlb-fijo-on')))break;}
      await p.waitForTimeout(900); await p.screenshot({path:`${C}5-boton-fijo-${dn}.png`});
      // preguntas frecuentes: abrir la 2.ª
      await p.evaluate(()=>document.getElementById('preguntas-frecuentes').scrollIntoView({block:'start'})); await p.waitForTimeout(900);
      await p.evaluate(()=>scrollBy(0,-20)); await p.click('#tlb-faq-1 ~ h3 .tlb-faq-b'); await p.waitForTimeout(700);
      await p.screenshot({path:`${C}6-preguntas-${dn}.png`});
    }
    await p.close();
  }
  await ctx.close();
}
await b.close();
