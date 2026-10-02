// Valida bloques de Gutenberg igual que el editor: parse() marca isValid=false si el HTML guardado
// no coincide con lo que generaría el bloque a partir de sus atributos.
require('global-jsdom/register');
window.matchMedia = window.matchMedia || (() => ({ matches: false, addListener() {}, removeListener() {} }));
const fs = require('fs');
const origWarn = console.warn, origErr = console.error, origInfo = console.info;
console.warn = console.error = console.info = () => {};
const { registerCoreBlocks } = require('@wordpress/block-library');
const { parse } = require('@wordpress/blocks');
registerCoreBlocks();
console.warn = origWarn; console.error = origErr; console.info = origInfo;
let fallos = 0;
for (const f of process.argv.slice(2)) {
  const html = f.endsWith('.json') ? JSON.parse(fs.readFileSync(f, 'utf8')).raw : fs.readFileSync(f, 'utf8');
  const silence = [console.warn, console.error, console.info, console.log];
  console.warn = console.error = console.info = () => {};
  const blocks = parse(html);
  [console.warn, console.error, console.info] = silence;
  const malos = [], tipos = {};
  const walk = (bs) => bs.forEach(b => { if (b.name) { tipos[b.name] = (tipos[b.name] || 0) + 1; if (!b.isValid) malos.push(b); } walk(b.innerBlocks || []); });
  walk(blocks);
  fallos += malos.length;
  console.log(`${f.split('/').pop()}: ${Object.values(tipos).reduce((a, b) => a + b, 0)} bloques, no válidos: ${malos.length}`, JSON.stringify(tipos));
  malos.forEach(b => console.log('   NO VÁLIDO', b.name, (b.originalContent || '').slice(0, 160)));
}
process.exit(fallos ? 1 : 0);
