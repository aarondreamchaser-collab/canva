import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:820,height:640},isMobile:true,hasTouch:true});
const p=await ctx.newPage(); await p.route(/googlesyndication|doubleclick/,r=>r.abort());
await p.route('**/*', async route=>{try{const r=await fetch(route.request().url());const hd={};r.headers.forEach((v,k)=>{if(!['content-encoding','content-length','transfer-encoding'].includes(k))hd[k]=v});await route.fulfill({status:r.status,headers:hd,body:Buffer.from(await r.arrayBuffer())})}catch(e){await route.abort()}});
await p.goto('https://tuluzencasa.com/',{waitUntil:'networkidle'}); await p.screenshot({path:'/tmp/claude-0/-home-user-canva/557847bc-71e6-5871-a563-54935582d0d3/scratchpad/base_tablet.png'}); await b.close();
