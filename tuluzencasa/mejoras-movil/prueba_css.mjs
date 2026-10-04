import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const PORT=process.env.PORT; const b=await chromium.launch(); const res={};
for (const w of [390,360,1280]) {
 const ctx=await b.newContext({viewport:{width:w,height:844},deviceScaleFactor:w<500?2:1,isMobile:w<500,hasTouch:w<500});
 for (const f of ['t_home_fix.html','t_art_fix.html','t_cat_fix.html','t_102_v2.html']) {
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route('https://**/*', async route=>{const req=route.request();
    try{const r=await fetch(req.url(),{method:req.method(),headers:{...req.headers()},redirect:'manual'});
    const hd={};r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v;});
    await route.fulfill({status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())});}catch(e){await route.abort();}});
  await p.goto(`http://localhost:${PORT}/${f}`,{waitUntil:'networkidle',timeout:90000});
  res[f+'@'+w]=await p.evaluate(()=>{const h1=document.querySelector('h1');const r=h1.getBoundingClientRect();const fp=document.querySelector('.entry-content p, .tlc-intro, .entry-summary p, main p');
   return {ov:document.documentElement.scrollWidth-innerWidth,h1L:Math.round(r.left),h1R:Math.round(innerWidth-r.right),h1fs:getComputedStyle(h1).fontSize,firstP:fp?Math.round(fp.getBoundingClientRect().top+scrollY):null,
   tables:[...document.querySelectorAll('.entry-content table')].map(t=>t.scrollWidth+'/'+t.parentElement.clientWidth+' '+getComputedStyle(t).fontSize),
   tlpH2:document.querySelector('.tlp-casa-h h2')?getComputedStyle(document.querySelector('.tlp-casa-h h2')).fontSize:null}});
  res[f+'@'+w].errs=errs.length;
  if(w===390){ await p.screenshot({path:'css_'+f.replace('.html','')+'_390.png'});
    if(f==='t_art_fix.html'){const t=await p.$$('.entry-content figure.wp-block-table'); await t[1].scrollIntoViewIfNeeded(); await p.screenshot({path:'css_tabla_390.png'});} }
  await p.close();
 }
 await ctx.close();
}
await b.close(); for (const [k,v] of Object.entries(res)) console.log(k,JSON.stringify(v));
