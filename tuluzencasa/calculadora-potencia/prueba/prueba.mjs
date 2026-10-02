// Prueba de la calculadora de potencia: node prueba.mjs  (genera capturas en esta carpeta)
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
import path from 'path';
const url = 'file://' + path.resolve('prueba.html');
const IMP = 1.21 * 1.0511, anual = kw => kw * 0.09 * 365 * IMP;
const f2 = n => n.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
let fallos = 0;
const ok = (c, m) => { console.log((c ? 'OK   ' : 'FALLO') + ' ' + m); if (!c) fallos++; };

const browser = await chromium.launch();
for (const vp of [{ n: 'escritorio', w: 1280, h: 900 }, { n: 'movil', w: 390, h: 844 }, { n: 'movil-pequeno', w: 360, h: 740 }]) {
  const page = await browser.newPage({ viewport: { width: vp.w, height: vp.h }, deviceScaleFactor: vp.w < 500 ? 2 : 1 });
  const errores = [];
  page.on('pageerror', e => errores.push(e.message));
  await page.goto(url, { waitUntil: 'networkidle' });
  console.log(`\n== ${vp.n} (${vp.w}px)`);
  const t = async id => (await page.textContent('#' + id)).trim();
  const tip = async () => (await page.textContent('#tlp-tip')).replace(/\s+/g, ' ');
  const marca = async (id, on = true) => { const c = page.locator(`#tlp-lista input[value="${id}"]`); on ? await c.check() : await c.uncheck(); };

  // Estado inicial: nevera 150 + tele 100 + LED 90 = 340 W -> 0,374 kW -> 2,3 kW; tiene 4,6 kW
  ok((await t('tlp-sum')) === '0,34 kW', 'inicial suma 0,34 kW');
  ok((await t('tlp-rec')).startsWith('2,3'), 'inicial recomienda 2,3 kW');
  ok((await tip()).includes(f2(anual(4.6) - anual(2.3)) + ' € al año'), `inicial ahorro ${f2(anual(4.6) - anual(2.3))} €`);

  // Piso eléctrico: + inducción, horno, termo = 5,84 kW -> 6,42 -> 6,9 (sube desde 4,6)
  for (const id of ['ind', 'hor', 'ter']) await marca(id);
  ok((await t('tlp-sum')) === '5,84 kW' && (await t('tlp-mar')) === '6,42 kW', 'cocina eléctrica 5,84 / 6,42 kW');
  ok((await t('tlp-rec')).startsWith('6,9'), 'recomienda 6,9 kW');
  ok((await tip()).includes('Puede saltar el limitador') && (await t('tlp-dif')) === '+' + f2(anual(6.9) - anual(4.6)) + ' €', 'aviso de limitador y sobrecoste');

  // Termo de madrugada y 6,9 contratados -> 4,34 -> 5,75; ahorra un escalón
  await marca('ter', false);
  await page.selectOption('#tlp-kw', '6.9');
  ok((await t('tlp-rec')).startsWith('5,75'), 'sin termo recomienda 5,75 kW');
  ok((await tip()).includes(f2(anual(6.9) - anual(5.75)) + ' € al año'), `ahorro de un escalón ${f2(anual(6.9) - anual(5.75))} €`);

  // Cantidad: 2 radiadores
  await marca('rad');
  await page.selectOption('select[data-q="rad"]', '2');
  ok((await t('tlp-sum')) === '8,34 kW', 'dos radiadores suman 4 kW');
  ok((await t('tlp-rec')).startsWith('9,2'), '8,34 kW x 1,10 = 9,17 kW -> 9,2 kW');
  await marca('her');
  ok((await t('tlp-rec')).startsWith('+9,2') && (await tip()).includes('Más de 9,2 kW'), 'con el hervidor (10,34 kW) avisa de que supera 9,2 kW');

  // Otro aparato y Vaciar
  await page.click('#tlp-reset');
  ok((await t('tlp-rec')) === '–' && (await tip()).includes('Empieza aquí'), 'vaciar deja la calculadora en blanco');
  await page.fill('#tlp-otro', '3000');
  await page.selectOption('#tlp-kw', '3.45');
  ok((await t('tlp-rec')).startsWith('3,45') && (await tip()).includes('Tu potencia es la recomendada'), 'otro aparato 3.000 W -> 3,3 kW -> 3,45 kW bien ajustada');

  // Estado bonito para la captura
  await page.fill('#tlp-otro', '');
  await page.click('#tlp-reset');
  for (const id of ['nev', 'tv', 'led', 'ind', 'hor', 'lav']) await marca(id);
  await page.selectOption('#tlp-kw', '6.9');

  const barraVisible = await page.isVisible('#tlp-barra');
  ok(vp.w < 900 ? barraVisible : !barraVisible, `barra resumen ${vp.w < 900 ? 'visible' : 'oculta'}`);
  if (vp.w < 900) {
    ok((await t('tlp-b-rec')) === (await t('tlp-rec')).replace('kW', ' kW'), 'la barra muestra la misma potencia que la pantalla');
    await page.locator('#tlp-lista input[value="sev"]').scrollIntoViewIfNeeded();
    await page.screenshot({ path: `captura-${vp.n}-barra.png` });
  }
  const scroll = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  ok(scroll <= 0, `sin scroll horizontal (sobran ${scroll}px)`);
  const anchoApp = await page.evaluate(() => Math.round(document.getElementById('tlp-app').getBoundingClientRect().width));
  console.log(`     ancho de la calculadora: ${anchoApp}px`);
  ok(errores.length === 0, 'sin errores de JavaScript ' + errores.join(' | '));
  await page.locator('.tlp').screenshot({ path: `captura-${vp.n}.png` });
  await page.close();
}
await browser.close();
console.log(fallos ? `\n${fallos} fallos` : '\nTodo correcto');
process.exit(fallos ? 1 : 0);
