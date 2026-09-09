# Proveedor de producción (fulfillment) — decisión

**Fecha:** 2026-09-09
**Estado:** CERRADA — proveedor principal: **Printify**.

## Pregunta que originó esta decisión

¿Usar CJ Dropshipping como proveedor de impresión/envío de las camisetas?

## Investigación

- CJ Dropshipping tiene un servicio POD real (DTG, subida de diseño propio),
  no es solo dropshipping de producto ajeno.
- Su sincronización automática de pedidos cubre Shopify, WooCommerce y
  TikTok Shop — **no tiene integración nativa con Etsy**.
- Reseñas 2026 lo describen como inconsistente en tiempos de envío y calidad
  de producto frente a lo anunciado.
- Etsy exige declarar el "production partner" (proveedor de fabricación)
  sea cual sea el proveedor elegido — esto no es un factor diferencial.

## Decisión

**No usar CJ Dropshipping como proveedor principal de las camisetas.**

Motivos:
1. Sin integración Etsy → fulfillment manual, lo que a partir de cierto
   volumen genera retrasos/errores que penalizan el ranking del shop en
   Etsy (tiempo de envío, order defect rate).
2. Nuestra marca depende de la calidad de prenda (heavyweight, oversized,
   tacto garment-dyed/descolorido — ver `brand-guidelines.md`). CJ es un
   generalista de sourcing con POD añadido; un especialista de apparel da
   más consistencia en ese tipo de blank concreto.

**Proveedor principal:** Printify.

**Uso posible de CJ Dropshipping:** proveedor secundario, más adelante,
para accesorios de marca no textiles (chapas, stickers, tazas) donde la
consistencia de prenda no aplica y el precio es más competitivo.

## Printify — configuración de la marca

### Por qué Printify encaja con nuestra dirección artística

Printify tiene en catálogo exactamente los blanks que pide
`brand-guidelines.md` (heavyweight, garment-dyed, oversized), cubiertos
por su "Quality Promise":

### Blank estándar de la colección: Comfort Colors® 1717

**Decisión cerrada:** Comfort Colors® 1717 es el blank por defecto de TODA
la colección, salvo excepción justificada por diseño concreto.

Motivo: es exactamente el tejido garment-dyed heavyweight que pide
`brand-guidelines.md`, con 63 colores reales (no solo camiseta blanca +
tintado digital), y es el blank que el propio mercado (ver `research.md`)
ya asocia con calidad vintage — jugamos con ventaja de reconocimiento.
Además, ya estaba en la lista de favoritos de la cuenta Printify del
proyecto, lo que confirma la elección de forma independiente.

**Datos reales de la cuenta Printify (confirmados en catálogo, no
estimados):**

- Precio base: USD 12,65 (USD 10,93 con Printify Premium)
- 7 tamaños, 63 colores
- **10 proveedores de impresión** disponibles — margen para comparar
  tiempos de producción entre proveedores sin cambiar de blank si alguno
  da problemas de plazo o calidad.

**Otras opciones descartadas de la lista de favoritos** (Bella+Canvas
3001, Next Level 6210/3600, Gildan 2000/64000/5000, Jerzees 29M, A4
Sprint): todas son tejidos ligeros/suaves "modernos", deportivos, o
algodón grueso sin teñido en prenda — ninguna da el tacto garment-dyed
descolorido que es nuestro diferenciador de marca, y Gildan 5000 en
particular es el blank más genérico de todo el mercado POD (cero
diferenciación).

**Corte oversized sin cambiar de blank:** el 1717 tiene un corte
relajado/clásico, no un boxy fit exagerado. Para lograr el efecto
oversized que pide el brief sin perder el tacto garment-dyed, se indica en
el listing pedir una talla por encima de la habitual ("oversized fit —
pide tu talla habitual para un ajuste relajado, una talla menos para
ajustado").

**Mapa color de marca → color real de Comfort Colors 1717:**

| Color de marca (`brand-guidelines.md`) | Color Comfort Colors 1717 |
|---|---|
| Crema/hueso | Ivory |
| Mostaza / naranja óxido | Sandstone |
| Verde bosque desvanecido | Moss |
| Azul marino descolorido | Blue Jean |
| Negro desvanecido | Pepper |
| Rojo ladrillo | Brick |

**Excepción admitida:** "Build Your Brand" Heavy Oversize Tee (hombro
caído, corte boxy real) para algún diseño puntual que necesite ese corte
específico y donde la gama de color más limitada no sea un problema — se
evalúa caso a caso, no es el estándar.

**Comfort Colors® 6030 (pocket tee):** misma calidad que el 1717, versión
con bolsillo; opción de variante si algún diseño usa el bolsillo como
elemento gráfico.

### Integración con Etsy

**Tienda ya creada:** [pichydesigns.etsy.com](https://pichydesigns.etsy.com)
("PichyDesigns"). Pendiente en el panel de Etsy: logotipo y banner de
tienda (checklist "Personaliza tu tienda", 1/5 completado — solo el
nombre está hecho).

1. En Printify → "Manage my stores" → "Add new store" → Etsy → autorizar
   OAuth (~3 min).
2. **Declarar a Printify como "production partner" en Etsy Shop
   Manager** — obligatorio por política de Etsy, no opcional.
3. Por cada diseño: elegir blank → subir artwork FINAL de Canva →
   posicionar según medidas de `canva/instrucciones.md` del diseño →
   publicar → sincroniza como listing en Etsy.
4. Pedidos de Etsy fluyen automáticamente a Printify → Printify los
   enruta al print provider correspondiente → el tracking vuelve a Etsy
   y marca el pedido como enviado.

### Branding propio en Printify (etiqueta y packaging)

**Sí es posible personalizar, con límites reales:**

- **Etiqueta interior impresa (neck label):** sustituye la etiqueta de
  composición por una con logo propio, impresa (no cosida). Desde $0.55
  ($0.37 con Printify Premium, -33%). Solo camisetas/sudaderas.
- **Inserto de packaging:** tarjeta física dentro de la bolsa del pedido
  con logo/mensaje de marca. Desde $0.25 ($0.15 con Premium). Es la pieza
  de marca con más impacto real (el cliente la ve al abrir el paquete).
- **No existe** personalización de la etiqueta de tela cosida — solo la
  alternativa impresa.
- Solo una opción de etiqueta a la vez (interior O exterior).
- **Restricción clave para nuestra marca:** la etiqueta **exterior** no se
  puede combinar con estampado de espalda — y todos nuestros diseños
  llevan gráfico grande en la espalda. Usar siempre **etiqueta interior**,
  nunca exterior.
- Composición, talla, país de origen y cuidado son obligatorios por ley y
  los fija Printify — no se pueden sustituir.

**Recomendación:** etiqueta interior con logo (barata, no interfiere con
el back print) + inserto de packaging para el mensaje de marca real.
Activar Printify Premium en cuanto haya ventas regulares — el ahorro en
ambos conceptos se amortiza rápido.

### Pendiente antes de publicar el primer diseño

- Elegir el print provider concreto dentro de Printify para Comfort
  Colors (Printify enruta automáticamente al más barato que cumpla, pero
  conviene revisar reseñas de tiempos de producción del provider
  asignado antes de confirmar precio final de venta).
- Confirmar tallas y colores de blank disponibles para pedir una muestra
  física antes del lanzamiento (control de calidad real, no solo mockup).
