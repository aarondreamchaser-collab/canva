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

- **Comfort Colors® 1717** — heavyweight, garment-dyed, algodón ring-spun
  100% pre-encogido. Es nuestro blank base para el corte "clásico
  vintage" (front+back estándar).
- **Comfort Colors® 6030 (pocket tee)** — misma calidad, versión con
  bolsillo; opción de variante para diseños con logo de pecho pequeño.
- **"Build Your Brand" Heavy Oversize Tee** — para los diseños que pidan
  el corte boxy/oversized más marcado (ver `concept.md` de cada diseño,
  campo "Tipo de camiseta").

Colores de blank a priorizar según nuestra paleta: arena/sand, musgo,
negro descolorido ("faded black" / "pepper"), azul denim, crema — nunca
blanco puro ni tonos saturados.

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
