import {chromium,abrir,disp,fs} from './comun.mjs';
const b=await chromium.launch(); const T='/tmp/claude-0/-home-user-canva/557847bc-71e6-5871-a563-54935582d0d3/scratchpad/frames/';
fs.rmSync(T,{recursive:true,force:true}); fs.mkdirSync(T,{recursive:true});
const solo=process.argv[2];
const RATE=0.2;
async function grabar(p,nombre,clip,msReal,accion,{rate=RATE,cada=40}={}){
  if(solo&&solo!==nombre)return;
  const cdp=await p.context().newCDPSession(p); await cdp.send('Animation.enable'); await cdp.send('Animation.setPlaybackRate',{playbackRate:rate});
  const dir=T+nombre+'/'; fs.mkdirSync(dir,{recursive:true}); const meta=[];
  const t0=Date.now(); if(accion) await accion();
  let i=0; while((Date.now()-t0)*rate<msReal){ const t=(Date.now()-t0)*rate; await p.screenshot({path:`${dir}${String(i).padStart(3,'0')}.png`,clip}); meta.push(Math.round(t)); i++; if(rate===1) await p.waitForTimeout(cada); }
  fs.writeFileSync(dir+'meta.json',JSON.stringify(meta)); await cdp.send('Animation.setPlaybackRate',{playbackRate:1});
  console.log(nombre,i,'fotogramas');
}
const R=async(p,s)=>p.evaluate(s=>{const r=document.querySelector(s).getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}},s);
const pad=(c,m,W)=>({x:Math.max(0,c.x-m),y:Math.max(0,c.y-m),width:Math.min(W,c.width+2*m),height:c.height+2*m});

let ctx=await b.newContext({viewport:{width:1280,height:800},deviceScaleFactor:1.5}); let p=await abrir(ctx,'home'); await p.waitForTimeout(3500);
// 1. logo al cargar (se repite el encendido)
let c=pad(await R(p,'.site-logo'),14,1280);
await grabar(p,'1-logo-al-cargar',c,1600,()=>p.evaluate(()=>{const s=document.querySelector('.tlb-luz');s.classList.remove('ini');void s.offsetWidth;s.classList.add('ini')}));
await grabar(p,'2-logo-raton',c,1800,()=>p.mouse.move(c.x+30,c.y+30));
await p.mouse.move(700,700);
// 3. título de la portada
c={x:0,y:(await R(p,'.tl-hero h1')).y-20,width:1280,height:(await R(p,'.tl-hero h1')).height+40};
await grabar(p,'3-titulo-portada',c,2600,()=>p.evaluate(()=>{const h=document.querySelector('.tl-hero h1'),k=document.querySelector('.tlb-clave');h.style.animation='none';k.className='';void h.offsetWidth;h.style.animation='';k.className='tlb-clave'}));
// 4. botones: ratón, destello, flecha y clic
let bb=await R(p,'.tl-botones'); c=pad(bb,24,1280);
const b1=await p.evaluate(()=>[...document.querySelectorAll('.tl-botones a')].map(a=>{const r=a.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}));
await grabar(p,'4-botones-raton-y-clic',c,3400,async()=>{(async()=>{await p.mouse.move(b1[0][0],b1[0][1],{steps:3});await new Promise(r=>setTimeout(r,1300/RATE*0.0+5500));await p.mouse.move(b1[1][0],b1[1][1],{steps:3});await new Promise(r=>setTimeout(r,4000));await p.mouse.down();await new Promise(r=>setTimeout(r,1200));await p.mouse.up();})()});
await p.mouse.move(700,780);
await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(500);
await grabar(p,'5-botones-latido',c,4600,null,{rate:1,cada:60});
// 6. menú: subrayado y desplegable
const m=await p.evaluate(()=>{const a=document.querySelector('#menu-item-151>a').getBoundingClientRect();const n=document.querySelector('#site-navigation .inside-navigation').getBoundingClientRect();return {ax:a.x+a.width/2,ay:a.y+a.height/2,x:n.x,y:n.y,w:n.width}});
const m2=await p.evaluate(()=>{const a=document.querySelector('#menu-item-38>a').getBoundingClientRect();return [a.x+a.width/2,a.y+a.height/2]});
c={x:Math.max(0,m.x-10),y:Math.max(0,m.y-6),width:Math.min(1280-Math.max(0,m.x-10),m.w+20),height:260};console.log(JSON.stringify(m));
await grabar(p,'6-menu',c,2400,async()=>{(async()=>{await p.mouse.move(m2[0],m2[1]);await new Promise(r=>setTimeout(r,4500));await p.mouse.move(m.ax,m.ay);})()});
await ctx.close();

// artículo
ctx=await b.newContext({viewport:{width:1280,height:800},deviceScaleFactor:1.5}); p=await abrir(ctx,'art'); await p.waitForTimeout(1500);
// 7. H2 con línea al llegar
const yh=await p.evaluate(()=>{const h=[...document.querySelectorAll('.entry-content>h2.tlb-oculto')][1];h.id=h.id||'x';window.__h=h;return h.getBoundingClientRect().top+scrollY});
await p.evaluate(y=>scrollTo({top:y-500,behavior:'instant'}),yh); await p.waitForTimeout(300);
c={x:0,y:200,width:1280,height:420};
await grabar(p,'7-h2-y-linea',c,1800,()=>p.evaluate(y=>scrollTo({top:y-300,behavior:'instant'}),yh));
// 8. caja Dato clave / tabla aparecen
const yd=await p.evaluate(()=>{const d=document.querySelector('.entry-content>.tl-dato.tlb-oculto,.entry-content>.wp-block-table.tlb-oculto');return d.getBoundingClientRect().top+scrollY});
await p.evaluate(y=>scrollTo({top:y-900,behavior:'instant'}),yd); await p.waitForTimeout(300);
c={x:0,y:150,width:1280,height:500};
await grabar(p,'8-caja-y-tabla-aparecen',c,1800,()=>p.evaluate(y=>scrollTo({top:y-350,behavior:'instant'}),yd));
// 9. enlace del texto
const ln=await p.evaluate(()=>{const a=[...document.querySelectorAll('.entry-content p a:not([class])')].find(a=>a.offsetWidth>80&&!a.closest('.tl-autor'));a.scrollIntoView({block:'center',behavior:'instant'});const r=a.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}});
await p.waitForTimeout(700);
c={x:Math.max(0,ln.x-200),y:ln.y-50,width:Math.min(760,1280-Math.max(0,ln.x-200)),height:ln.h+100};
await grabar(p,'9-enlace',c,900,()=>p.mouse.move(ln.x+ln.w/2,ln.y+ln.h/2,{steps:2}));
await p.mouse.move(5,790);
// 10. tarjeta de calculadora: botón
const tj=await p.evaluate(()=>{const t=document.querySelector('.tlb-tarjeta');t.scrollIntoView({block:'center',behavior:'instant'});t.classList.add('tlb-visto');t.classList.remove('tlb-oculto');const r=t.getBoundingClientRect(),bt=t.querySelector('.tlb-bt').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,bx:bt.x+bt.width/2,by:bt.y+bt.height/2}});
await p.waitForTimeout(900);
c={x:tj.x-12,y:tj.y-12,width:tj.w+24,height:tj.h+24};
await grabar(p,'10-tarjeta-boton',c,1300,()=>p.mouse.move(tj.bx,tj.by,{steps:2}));
await ctx.close();

// móvil: portada (título y menú)
ctx=await b.newContext({...disp.movil,deviceScaleFactor:1.5}); p=await abrir(ctx,'home'); await p.waitForTimeout(3000);
await grabar(p,'11-movil-titulo',{x:0,y:0,width:390,height:700},2600,()=>p.evaluate(()=>{const h=document.querySelector('.tl-hero h1'),k=document.querySelector('.tlb-clave'),s=document.querySelector('.tlb-luz');h.style.animation='none';k.className='';s.classList.remove('ini');void h.offsetWidth;h.style.animation='';k.className='tlb-clave';s.classList.add('ini')}));
await grabar(p,'12-movil-menu',{x:0,y:0,width:390,height:700},900,()=>p.tap('.mobile-menu-control-wrapper .menu-toggle'));
await ctx.close();
await b.close();
