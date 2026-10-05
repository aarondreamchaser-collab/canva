# Rediseño de tuluzencasa (estilo web de nicho con AdSense)

Estado: **aplicado y comprobado en la web publicada (5-10-2026)**. Capturas en `capturas-publicadas/`. Copia previa en `copia-seguridad/2026-10-05-antes-de-aplicar/`. Pendiente: limitar el JS de las dos calculadoras a su página (WPCode, lo hace el titular).

Nota: la portada (23) lleva un bloque HTML con `<style id="tl-portada-arreglo">` que anula el relleno de `.wp-block-group__inner-container` de GeneratePress. La misma regla está ya en `wpcode-diseno.css`; cuando se pegue en el fragmento 157, se puede quitar de la portada.

Cambios pedidos sobre la propuesta: sin caja de «Respuesta rápida»; menú con «Más temas ▾» (Ahorrar luz, Placas solares, Coche eléctrico, Averías e instalación) y «Calculadoras ▾», sin «Inicio»; el texto «calculadora de la portada» pasa a «nuestra calculadora de consumo» con enlace a la página nueva (lista exacta en `cambio-calculadora-portada.md`).

## Archivos

| Archivo | Qué es |
|---|---|
| `wpcode-diseno.css` | Fragmento CSS de WPCode («Diseño tuluzencasa»), en todo el sitio. Incluye las mejoras de móvil de `mejoras-movil/`. |
| `wpcode-plantilla.php` | Fragmento PHP de WPCode («Plantilla tuluzencasa»). Añade la ruta de navegación, la fecha de actualización, el índice, los huecos de anuncios, la caja de autor y los artículos relacionados, y el shortcode `[tl_categorias]`. No modifica el texto guardado de los artículos. |
| `portada.html` | Contenido nuevo de la página 23 (Inicio), en bloques de WordPress. Se genera con `generar.py`. |
| `pagina-calculadora-consumo.html` | Página nueva «Calculadora de consumo eléctrico» (`/calculadora-consumo-electrico/`), con la calculadora de la portada actual tal cual. |
| `vista-previa/*.jpg` | Capturas de la vista previa local en escritorio (1280 px), tablet (820 px) y móvil (390 px). |
| `copia-seguridad/` | Copia del estado actual: contenido de la página 23, menús 21 y 22, widgets y barras laterales, y los dos JS de las calculadoras. |
| `herramientas/` | Scripts de la vista previa: `construir.py` y `capturas.mjs`. |

## Orden para aplicar

| # | Quién | Cambio | Estado |
|---|---|---|---|
| 1 | Claude | Página 156 «Calculadora de consumo eléctrico» en borrador, con el título y la descripción de Rank Math que ahora tiene la portada | Hecho |
| 2 | Titular | WPCode: crear el CSS «Diseño tuluzencasa» (todo el sitio, cabecera). Desactivar «CSS artículos móvil» si existe | Hecho (fragmento 157, con el bloque de tablet) |
| 3 | Titular | WPCode: crear el PHP «Plantilla tuluzencasa» (ejecutar en todas partes) | Hecho |
| 4 | Titular | Personalizador › Diseño › Navegación principal: Búsqueda en la navegación = Activar. El menú hamburguesa hasta 1024 px lo hace el CSS (GeneratePress gratuito no tiene esa opción) | Hecho |
| 5 | Titular | Rank Math › Ajustes generales › Rutas de navegación: activar, separador `›`, mostrar Inicio | Hecho |
| 6 | Titular | Revisar la vista previa de la página 156 y publicarla | Hecho |
| 7 | Titular | WPCode: lógica condicional para que «Calculadora Home» cargue solo en `calculadora-consumo-electrico` y «Calculadora potencia» solo en `calculadora-potencia-contratada` (regla «URL de la página» › «Contiene») | Pendiente |
| 8 | Claude | Menú 21: quitar Inicio; el 151 pasa a «Más temas» y recibe Averías e instalación; nuevo «Calculadoras ▾» con las 2 páginas | Hecho |
| 9 | Claude | Widget «Calculadoras» (block-3): enlace a la página nueva | Hecho |
| 10 | Claude | Página 23: contenido de `portada.html` y título/descripción nuevos de Rank Math | Hecho |
| 11 | Claude | 20 entradas, Sobre nosotros y página 102: «calculadora de la portada» → «nuestra calculadora de consumo» (`cambio-calculadora-portada.md`; aprobado) | Hecho |

## Deshacer

- CSS y PHP: desactivar los dos fragmentos de WPCode.
- Personalizador y Rank Math: volver a poner los valores anteriores (búsqueda desactivada, punto de despliegue vacío, rutas desactivadas).
- Página 23, menú y widgets: Claude restaura desde `copia-seguridad/`.
- Página nueva: pasarla a borrador.
- Textos de las entradas: Claude los restaura desde la copia de cada entrada que guarda antes de aplicar.
