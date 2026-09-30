# Prompt para Claude Code (pégalo tal cual)

Lee CLAUDE.md antes de empezar y sigue sus reglas en todo momento. Trabaja por fases y enséñame un resumen al terminar cada una.

## Fase 1 — Comprobar el acceso
1. Comprueba que existen las variables de entorno WP_USER y WP_APP_PASSWORD (sin mostrar su valor).
2. Haz `GET /wp-json/wp/v2/users/me` para confirmar que la autenticación funciona.
3. Lista las categorías y guarda sus IDs.
Si algo falla, para y dime qué ha pasado.

## Fase 2 — Subir la home
1. Lee el archivo `home-para-wordpress.html` de esta carpeta.
2. Busca si ya existe una página con slug `inicio`. Si existe, pregúntame antes de modificarla.
3. Si no existe, crea una página publicada con título "Inicio", slug `inicio` y como contenido el HTML completo envuelto en un bloque HTML personalizado:
   `<!-- wp:html -->` + contenido del archivo + `<!-- /wp:html -->`
4. Descarga la página creada con `?context=edit` y comprueba que el `<script>` y el `<style>` se han guardado sin cambios. Si WordPress los ha eliminado, para y avísame.
5. Explícame que vas a configurar la página de inicio estática y, cuando te lo confirme, actualiza `/wp-json/wp/v2/settings` con `show_on_front: "page"` y `page_on_front: <ID de Inicio>`.
6. Descarga https://tuluzencasa.com y confirma que la home muestra la calculadora (busca el texto "Factura estimada").

## Fase 3 — Crear 6 artículos en borrador
Crea estos artículos con `status: "draft"`, su categoría y exactamente este slug:

| Slug | Título | Categoría | Palabra clave principal |
| --- | --- | --- | --- |
| cuanto-consume-aire-acondicionado | Cuánto consume un aire acondicionado por hora (y cuánto cuesta en tu factura) | consumo | cuánto consume un aire acondicionado |
| cuanto-consume-radiador-de-aceite | Cuánto consume un radiador de aceite: coste por hora, día y mes | climatizacion | cuánto consume un radiador de aceite |
| cuanto-consume-freidora-de-aire | Cuánto consume una freidora de aire frente a un horno eléctrico | consumo | cuánto consume una freidora de aire |
| cuanto-consume-termo-electrico | Cuánto consume un termo eléctrico y cómo programarlo para ahorrar | consumo | cuánto consume un termo eléctrico |
| cuanto-consume-una-nevera | Cuánto consume una nevera al mes según su etiqueta energética | consumo | cuánto consume una nevera |
| por-que-salta-el-diferencial | Por qué salta el diferencial: causas y cómo encontrar el aparato culpable | instalacion | por qué salta el diferencial |

Para cada artículo:
1. Calcula con un script todas las cifras siguiendo los criterios de precios y factores de CLAUDE.md, y guarda los cálculos en `calculos/<slug>.md` para que pueda revisarlos.
2. Redacta el artículo siguiendo el estilo de CLAUDE.md.
3. Añade un extracto de máximo 155 caracteres que responda a la pregunta con una cifra: servirá de metadescripción.
4. Intenta guardar en Rank Math la palabra clave principal y la metadescripción (campos `rank_math_focus_keyword` y `rank_math_description`). Si la API no lo permite, no insistas: apúntalo en el resumen final para que lo haga a mano.
5. Guarda también una copia local en `articulos/<slug>.html`.

Enlazado interno obligatorio entre estos 6 artículos:
- Aire acondicionado ↔ radiador de aceite ↔ termo (consumo de climatización y agua caliente).
- Freidora de aire ↔ nevera ↔ termo (cocina y consumo continuo).
- El artículo del diferencial enlaza al del aire acondicionado y al del radiador (aparatos que suelen hacerlo saltar), y todos enlazan a la home.
Usa URLs con el formato `https://tuluzencasa.com/<slug>/`.

## Fase 4 — Resumen final
Dame una tabla con: título, enlace de edición en WordPress (`/wp-admin/post.php?post=<ID>&action=edit`), número de palabras, si se guardó la palabra clave de Rank Math y cualquier dato marcado como `[VERIFICAR]`.
No publiques nada: yo revisaré y publicaré cada artículo.
