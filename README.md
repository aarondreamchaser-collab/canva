# PichyDesigns — Sistema de Dirección Creativa

Tienda Etsy: [pichydesigns.etsy.com](https://pichydesigns.etsy.com)

Este repositorio es el centro de producción de la tienda de camisetas en Etsy.
Aquí vive el proceso completo: **IDEA → CONCEPTO → DIRECCIÓN ARTÍSTICA → PROMPT →
GENERACIÓN → SELECCIÓN → EDICIÓN → ARCHIVO FINAL → MOCKUP → LISTING DE ETSY**.

## Herramientas del flujo

- **Generación de imágenes:** Higgsfield Pro
- **Edición, composición, mockups y acabado:** Canva Business
- **Coordinación, dirección creativa y producción:** este asistente

## Reglas fijas del sistema

1. **Sin texto arriesgado en IA.** No se piden textos dentro de las imágenes generadas
   cuando exista riesgo de que salgan deformados o poco profesionales. El texto final
   se añade en Canva. Los prompts de Higgsfield que lo requieran llevarán la etiqueta
   `NO TEXT / NO LETTERING`.
2. **Sin inventar generaciones.** Si no hay acceso real a la herramienta de generación,
   se dice explícitamente en vez de simular un resultado.
3. **Originalidad ante todo.** Nada de logos, marcas, personajes protegidos, equipos
   deportivos, merchandising oficial ni composiciones que repliquen una obra concreta.
   Se avisa de cualquier riesgo de propiedad intelectual y se propone alternativa.
4. **Calidad > cantidad, diferenciación > tendencia copiada, marca > diseños sueltos,
   ventas > imágenes bonitas.**
5. **Simplicidad primero.** No se añaden automatizaciones, APIs o herramientas extra
   hasta que aporten valor real y probado.

## Estructura del repositorio

```
/etsy-tshirt-brand
  /brand
    brand-guidelines.md         ← posicionamiento, estética, paleta, reglas de marca
  /collections
    /<nombre-coleccion>
      research.md                ← Fase 1: investigación de mercado de la colección
      concepts.md                ← Fase 3: conceptos ranqueados de la colección
      /01-<nombre-diseno>
        concept.md                ← ficha del concepto individual (Fase 1-3)
        prompt-higgsfield.txt      ← prompt final para Higgsfield (Fase 4)
        artwork/                   ← salidas brutas de Higgsfield (v01, v02, ...)
        canva/                     ← proyectos/exports intermedios de Canva
        mockups/                   ← mockups de presentación
        final/                     ← PNG final listo para producción (FINAL)
        listing/                   ← listing.md con título, descripción, tags, precio
      /02-<nombre-diseno>
        ...
  /_TEMPLATE                   ← plantilla base para cada diseño nuevo (copiar, no editar)
COLLECTIONS.md                  ← índice general de colecciones y estado de cada diseño
```

### Convención de versiones

Nunca se sobrescribe un archivo. Se numera: `v01`, `v02`, `v03`... y la versión
aprobada se marca como `FINAL`.

## Comandos de trabajo

| Dices...            | Qué hago |
|---------------------|----------|
| `CREAR DISEÑO`      | Inicio el proceso completo (Fases 1-10) para una idea nueva |
| `CREAR COLECCIÓN`   | Propongo una colección coherente de 4-6 diseños |
| `MEJORAR DISEÑO`    | Analizo el concepto actual y propongo mejoras |
| `PROMPT HIGGSFIELD` | Entrego solo el prompt profesional para generar el artwork |
| `CANVA`             | Doy las instrucciones de edición y preparación final |
| `LISTING`           | Genero el listing completo para Etsy |
| `ANALIZA`           | Evalúo el diseño desde el punto de vista comercial y artístico |

## Estado

Posicionamiento de marca confirmado: **Vintage Weird Animal Streetwear**
(ver `/etsy-tshirt-brand/brand/brand-guidelines.md`). Primera colección en
fase de conceptos: **Fall Animal Club**
(ver `/etsy-tshirt-brand/collections/fall-animal-club/`). Aún no se ha
generado artwork de producción. Ver `COLLECTIONS.md` para el estado
detallado por diseño.
