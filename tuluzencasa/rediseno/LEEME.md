# Rediseño de tuluzencasa (estilo web de nicho con AdSense)

Estado: **solo vista previa.** No se ha aplicado nada en WordPress.

## Archivos

| Archivo | Qué es |
|---|---|
| `wpcode-diseno.css` | Fragmento CSS de WPCode («Diseño tuluzencasa»), en todo el sitio. Incluye las mejoras de móvil de `mejoras-movil/`. |
| `wpcode-plantilla.php` | Fragmento PHP de WPCode («Plantilla tuluzencasa»). Añade la ruta de navegación, la fecha de actualización, la respuesta rápida, el índice, los huecos de anuncios, la caja de autor y los artículos relacionados, y el shortcode `[tl_categorias]`. No modifica el texto guardado de los artículos. |
| `portada.html` | Contenido nuevo de la página 23 (Inicio), en bloques de WordPress. Se genera con `generar.py`. |
| `pagina-calculadora-consumo.html` | Página nueva «Calculadora de consumo eléctrico» (`/calculadora-consumo-electrico/`), con la calculadora de la portada actual tal cual. |
| `vista-previa/*.jpg` | Capturas de la vista previa local en escritorio (1280 px), tablet (820 px) y móvil (390 px). |
| `copia-seguridad/` | Copia del estado actual: contenido de la página 23, menús 21 y 22, widgets y barras laterales, y los dos JS de las calculadoras. |
| `herramientas/` | Scripts de la vista previa: `construir.py` y `capturas.mjs`. |

## Orden para aplicar (cuando haya OK)

| # | Quién | Cambio |
|---|---|---|
| 1 | Claude | Copia de seguridad recién hecha justo antes de aplicar (se compara con `copia-seguridad/`). |
| 2 | Titular | WPCode: crear el CSS «Diseño tuluzencasa» (todo el sitio, cabecera). Desactivar «CSS artículos móvil» si existe. |
| 3 | Titular | WPCode: crear el PHP «Plantilla tuluzencasa» (ejecutar en todas partes). |
| 4 | Titular | Personalizador › Diseño › Navegación principal: Búsqueda en la navegación = Activar; Punto de corte del menú móvil = 1024 px. |
| 5 | Titular | Rank Math › Ajustes generales › Rutas de navegación: activar. Separador `›`. Mostrar Inicio. |
| 6 | Claude | Crear la página «Calculadora de consumo eléctrico» en **borrador**. La publica el titular. |
| 7 | Titular | WPCode: «Calculadora Home» → lógica condicional «solo en la página calculadora-consumo-electrico». «Calculadora potencia» → solo en `calculadora-potencia-contratada`. |
| 8 | Claude | Menú 21: quitar Inicio. Mover Averías e instalación dentro de «Ahorro y energía». Añadir «Calculadoras ▾» con las 2 páginas. |
| 9 | Claude | Widget «Calculadoras» (block-3): enlace a la página nueva. |
| 10 | Claude | Página 23: contenido de `portada.html`, y título/descripción de Rank Math nuevos para la portada. La página de la calculadora recibe los actuales. |

## Deshacer

- CSS y PHP: desactivar los dos fragmentos de WPCode.
- Personalizador y Rank Math: volver a poner los valores anteriores (búsqueda desactivada, corte en 768 px, rutas desactivadas).
- Página 23, menú y widgets: Claude restaura desde `copia-seguridad/`.
- Página nueva: pasarla a borrador.
