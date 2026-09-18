# GAREEYSTUDIO — Mockups de producto con recreación fiel

Segunda línea de trabajo del repositorio, independiente de PichyDesigns.
Marca: **GAREEYSTUDIO · ZGZ.2026**. Productos personalizados con foto
(peanas de metacrilato y similares) cuyos mockups se recrean a partir de
referencias de proveedor, sustituyendo a las personas y aplicando la
identidad visual de la marca.

## Principio de trabajo

**REFERENCE FIRST. MODIFICATION SECOND. CREATIVITY ONLY WHEN EXPLICITLY
REQUESTED.** La referencia visual es la fuente de verdad. Se cambia
únicamente lo que el usuario pide; todo lo demás queda bloqueado.

Cada proyecto se entrega con la estructura A–F: análisis de referencia,
modificación solicitada, elementos bloqueados, prompt final para
Higgsfield, restricciones negativas y ajustes recomendados.

## Documentos

- `estilo-mockups.md` — guía de estilo APROBADA (tipografía, acentos
  dorados, checklist). Leer antes de producir cualquier mockup.
- `mockups/<nn>-<nombre>/` — un proyecto por mockup:
  - `reference-original.*` — referencia del proveedor / imagen de partida
  - `reference-tipografia.*` — referencia tipográfica si la hay
  - `prompt-higgsfield.txt` — prompt exacto usado en Higgsfield
  - `artwork/` — salidas de Higgsfield numeradas (`v01`, `v02`...)
  - `final/` — versión aprobada por el usuario (`FINAL-...`)

## Herramientas

- **Higgsfield** vía MCP `WEBS`: subida de referencias con
  `media_upload` + `media_confirm`, generación con `generate_image`
  (modelo `gpt_image_2_5`, `quality: high`, `resolution: 2k`).
- **ChatGPT / Canva**: acabado gráfico manual cuando haga falta.

## Proyectos

| # | Proyecto | Estado |
|---|---|---|
| 01 | Peana de metacrilato · pareja de boda | FINAL aprobado 2026-09-18 |
| 02 | Infografía "impreso por las dos caras" | 2 variantes generadas, pendiente de elección |
| 03 | Tallas del producto M(15cm) / S(10cm) | v01 generada |
| 04 | Antes y después del recorte de fondo | v01 generada |
| 05 | Ambientación lifestyle, sin texto | v01 generada |
| 06 | Escala talla S sobre fieltro verde | v01 generada |
| 07 | Escala talla M sobre fieltro verde | v01 generada |
| 08 | Vídeo del listing, fondo crema, sin audio | FINAL v05 |

## Continuidad entre mockups

Todos los mockups de una misma ficha de producto llevan **la misma pareja
protagonista**. Para conseguirlo se pasa el archivo `final/FINAL-...` del
proyecto 01 como segunda referencia (`image_references`) en cada generación
posterior, junto a la referencia de composición del mockup nuevo.
