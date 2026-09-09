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
`brand-guidelines.md`, con 61 colores reales (no solo camiseta blanca +
tintado digital), precio base ~$12.41 ($10.72 con Printify Premium), y es
el blank que el propio mercado (ver `research.md`) ya asocia con calidad
vintage — jugamos con ventaja de reconocimiento.

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

### Pendiente antes de publicar el primer diseño

- Elegir el print provider concreto dentro de Printify para Comfort
  Colors (Printify enruta automáticamente al más barato que cumpla, pero
  conviene revisar reseñas de tiempos de producción del provider
  asignado antes de confirmar precio final de venta).
- Confirmar tallas y colores de blank disponibles para pedir una muestra
  física antes del lanzamiento (control de calidad real, no solo mockup).
