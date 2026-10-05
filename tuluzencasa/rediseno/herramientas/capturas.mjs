import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const PORT=process.env.PORT; const b=await chromium.launch(); const res={};
const cache=new Map();
async function abrir(ctx,url){
  const p=await ctx.newPage(); const st={bytes:0,req:0,imgs:0,errs:[]}; p.on('pageerror',e=>st.errs.push(e.message));
  await p.route('**/*', async route=>{const rq=route.request(); const u=rq.url();
    if(u.startsWith('http://localhost')){ const r=await route.fetch(); const body=await r.body(); st.bytes+=body.length; st.req++; return route.fulfill({response:r,body}); }
    try{ let c=cache.get(u); if(!c){ const r=await fetch(u,{headers:{'user-agent':'Mozilla/5.0 tlc-preview'}}); const hd={}; r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;}); c={status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())}; cache.set(u,c);} 
      st.bytes+=c.body.length; st.req++; if(rq.resourceType()==='image') st.imgs++; await route.fulfill(c);}catch(e){await route.abort();}});
  await p.goto(url,{waitUntil:'networkidle',timeout:120000}); return [p,st];
}
const pages=[['home','p_home.html'],['calc','p_calc.html'],['art','p_art.html'],['artold','p_art_old.html']];
for (const [w,hgt] of [[1280,900],[1025,800],[820,1000],[390,844]]) {
  const mob=w<500; const ctx=await b.newContext({viewport:{width:w,height:hgt},deviceScaleFactor:mob?2:1,isMobile:mob,hasTouch:mob});
  for (const [n,f] of pages) {
    const [p,st]=await abrir(ctx,`http://localhost:${PORT}/${f}`);
    const m=await p.evaluate(()=>{const lis=[...document.querySelectorAll('#menu-principal > li')].filter(l=>l.offsetParent);
      const t=document.querySelector('.main-title'); const hd=document.querySelector('#masthead');
      return {ov:document.documentElement.scrollWidth-innerWidth, headerH:Math.round(hd.getBoundingClientRect().height),
        logoLines:Math.round(t.getBoundingClientRect().height/parseFloat(getComputedStyle(t).lineHeight)),
        menuTops:[...new Set(lis.map(l=>Math.round(l.getBoundingClientRect().top)))], toggle:getComputedStyle(document.querySelector('#mobile-menu-control-wrapper .menu-toggle')).display};});
    res[`${n}@${w}`]={...m,bytes:st.bytes,req:st.req,errs:st.errs};
    await p.screenshot({path:`capturas/${n}_${w}_top.png`});
    if(['home','art'].includes(n)&&[1280,820,390].includes(w)) {await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){scrollTo(0,y);await new Promise(r=>setTimeout(r,60));}scrollTo(0,0)}); await p.waitForTimeout(800); await p.screenshot({path:`capturas/${n}_${w}_full.png`,fullPage:true});}
    if(n==='art'&&w===1280){ await p.hover('#menu-item-151'); await p.waitForTimeout(400); await p.screenshot({path:'capturas/menu_desplegable_1280.png',clip:{x:0,y:0,width:1280,height:380}});
      await p.click('#site-navigation .search-item a'); await p.waitForTimeout(300); await p.screenshot({path:'capturas/buscador_1280.png',clip:{x:0,y:0,width:1280,height:200}}); }
    if(n==='art'&&w===390){ await p.click('#mobile-menu-control-wrapper .menu-toggle'); await p.waitForTimeout(400); await p.screenshot({path:'capturas/menu_movil_390.png'}); }
    if(n==='calc'&&w===390){ {await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){scrollTo(0,y);await new Promise(r=>setTimeout(r,60));}scrollTo(0,0)}); await p.waitForTimeout(800); await p.screenshot({path:`capturas/calc_390_full.png`,fullPage:true});} }
    await p.close();
  }
  await ctx.close();
}
// Peso de la web publicada (actual), mismas condiciones
const ctx=await b.newContext({viewport:{width:1280,height:900}});
for (const [n,u] of [['live_home','https://tuluzencasa.com/'],['live_art','https://tuluzencasa.com/tramos-horarios-luz/']]) { cache.clear(); const [p,st]=await abrir(ctx,u); res[n]={bytes:st.bytes,req:st.req,errs:st.errs}; await p.close(); }
cache.clear(); for (const [n,f] of [['home','p_home.html'],['art','p_art.html']]) { const [p,st]=await abrir(ctx,`http://localhost:${PORT}/${f}`); res['nuevo_'+n]={bytes:st.bytes,req:st.req}; await p.close(); }
await b.close(); for (const [k,v] of Object.entries(res)) console.log(k,JSON.stringify(v));
