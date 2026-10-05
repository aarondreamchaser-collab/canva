# Efectos tuluzencasa

Fragmento único de WPCode: `efectos-tuluzencasa.html` (7766 bytes; 3511 bytes con gzip). Sin librerías ni peticiones externas.

## Cómo instalarlo
1. WPCode › Añadir fragmento › **Añade tu código personalizado** › tipo **Fragmento HTML** (no «JavaScript»: el HTML admite a la vez el `<style>` y el `<script>`).
2. Título: «Efectos tuluzencasa». Pega el archivo entero.
3. Inserción: **Automática** · Ubicación: **Pie de todo el sitio** (Site Wide Footer).
4. Activar y guardar. Para quitarlo todo, desactívalo.

## Qué hace
| Efecto | Dónde | Cuándo no aparece |
|---|---|---|
| Cursor de rayo + estela de chispas | Todo el sitio | Móvil y tablet (`pointer: coarse`), «reducir movimiento». Mano en enlaces/botones/desplegables/casillas; cursor de texto en campos. El lienzo se crea con el primer movimiento del ratón y el bucle se para cuando no hay chispas. |
| Barra de lectura amarilla | Solo entradas (`.single-post`) | — (no se anima: solo marca el avance) |
| Números de tablas que cuentan | Solo entradas, celdas que son solo una cifra (+ unidad) | «reducir movimiento». Una sola vez por celda. El texto real no cambia: la cifra que cuenta se pinta encima, así que no hay saltos de diseño y Google y los lectores de pantalla leen siempre el valor final. |
| Caja «Dato clave» | Contenido con la clase `tl-dato` | — |

Marcado de la caja en los artículos (bloques):
```
<!-- wp:group {"className":"tl-dato","layout":{"type":"default"}} -->
<div class="wp-block-group tl-dato"><!-- wp:paragraph {"className":"tl-dato-t"} -->
<p class="tl-dato-t">Dato clave</p>
<!-- /wp:paragraph -->
<!-- wp:paragraph -->
<p>…</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->
```

## Pruebas (5-10-2026, HTML real de la web, sin anuncios cargados)
Artículo del termo, portada y calculadora de consumo; escritorio 1280 px (ratón), tablet 820 px y móvil 390 px (táctil):
- Tiempo del script durante la carga: 0,4–0,8 ms (lo de las entradas espera a `requestIdleCallback`).
- CLS: 0 en todos los casos (antes de cambiar a la técnica de superposición, la tabla daba 0,017–0,05).
- Tareas largas añadidas: ninguna. Bucles de animación en reposo: 0.
- Con «reducir movimiento»: sin chispas ni conteo, cursor normal.
- Lighthouse no se pudo ejecutar contra la web publicada desde este entorno (Chromium no acepta el certificado del proxy y no se desactiva TLS).

Capturas en `capturas/`. El rayo de la captura 1 es una ilustración: las capturas de pantalla no muestran el cursor real.
