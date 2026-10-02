# TAREAS.md — Hoja de ruta de Claude Code para tuluzencasa.com

Lee antes CLAUDE.md (reglas) y PLAN.md (monetización). Este archivo dice **qué hacer y en qué orden**. Trabaja siempre por fases: termina una, dame el resumen y espera mi confirmación antes de empezar la siguiente.

## Reglas comunes a todas las tareas
- Trabaja siempre sobre la versión actual de WordPress (`?context=edit`), nunca sobrescribas con copias locales.
- No publiques nada: todo en borrador. Yo reviso y publico.
- Antes de cambiar ajustes, plugins, menús o código del sitio, explícame el plan y espera confirmación.
- Si una tarea necesita un dato que no tienes (ID de afiliado, de AdSense, datos personales), deja `[CONFIRMAR: …]` y sigue.
- Al terminar cada fase: tabla resumen, enlaces de edición y lista de `[CONFIRMAR]`. Sube las copias al repositorio.

---

## Fase 1 — Páginas que faltan (prioridad máxima)
1. **Sobre nosotros** (`/sobre-nosotros/`): quién está detrás (Aaron, desde Calatayud, Zaragoza), por qué existe la web, cómo se calculan las cifras (enlace a la portada) y cómo se revisan los artículos. Sin afirmar que el autor es electricista ni que un profesional revisa los textos.
2. **Contacto** (`/contacto/`): contacto@tuluzencasa.com, plazo orientativo de respuesta y aviso de que no se diagnostican averías a distancia. Sin formulario.
3. Añade ambas al menú **Legal** del pie (te pediré confirmación antes).

**Hecho cuando:** las dos páginas están en borrador, sin schema Article y con los `[CONFIRMAR]` listados.

## Fase 2 — Contenido de octubre (antes de noviembre)
Crea en tandas de 3–4 artículos los de la tabla de la Prioridad 2 de PLAN.md, empezando por:
1. `como-leer-la-factura-de-la-luz`
2. `que-potencia-contratar`
3. `pvpc-o-mercado-libre`
4. `calefaccion-electrica-mas-barata` y el resto de climatización.

Para cada artículo: cálculos con script en `calculos/`, palabra clave en el título, la primera frase y un H2, metadescripción y extracto iguales, un enlace externo oficial, índice con anclas, 3 enlaces internos y cero `[VERIFICAR]` sin resolver (si queda alguno, enséñamelo con tu propuesta).

**Hecho cuando:** cada tanda está en borrador y me das la tabla con palabra clave, palabras, enlaces y pendientes.

## Fase 3 — Enlazado interno
Cada vez que publique una tanda:
1. Revisa todos los artículos publicados y propón enlaces hacia los nuevos (máximo 2 por artículo y solo donde encajen de forma natural).
2. Enséñame la lista (artículo origen → frase → artículo destino) y aplica solo los que confirme.
3. Si una categoría nueva ya tiene entradas publicadas, propón añadirla al menú Principal.

## Fase 4 — Calculadora de potencia contratada
Página nueva `/calculadora-potencia-contratada/` (borrador) con:
- El usuario marca los aparatos que pueden funcionar a la vez y la calculadora suma su potencia, aplica un margen y recomienda la potencia normalizada (2,3 · 3,45 · 4,6 · 5,75 · 6,9 · 8,05 · 9,2 kW).
- Muestra cuánto ahorra o cuánto le cuesta cambiar de potencia al año, con el mismo precio de potencia y los mismos impuestos que la calculadora de la portada.
- Mismo diseño que la portada. El HTML va en la página y el JavaScript en un fragmento nuevo de WPCode que solo actúe si encuentra su contenedor.
- Texto explicativo de unas 800 palabras debajo, con su palabra clave («qué potencia contratar»), y enlace desde el artículo `que-potencia-contratar`.

**Hecho cuando:** funciona en la vista previa en escritorio y móvil, y me pasas el plan del fragmento de WPCode antes de activarlo.

## Fase 5 — Mini calculadoras en los artículos
Para aire acondicionado, radiador de aceite, termo y freidora, añade una calculadora pequeña dentro del artículo (debajo de la primera tabla):
- Campos: potencia, horas al día y precio del kWh, con los valores del artículo por defecto.
- Resultado: coste por hora, día, mes (30,4 días) y año, con impuestos.
- Un único fragmento de WPCode para todas, que detecte los contenedores `data-tlc-mini`.
- Enlace «Calcula toda tu casa» hacia la portada.

## Fase 6 — Preguntas frecuentes con datos estructurados
En los artículos que ya tienen preguntas frecuentes, conviértelas al bloque FAQ de Rank Math (o añade el schema FAQPage) sin cambiar el texto. Comprueba que el resultado es válido.

## Fase 7 — Auditoría mensual
Una vez al mes, revisa toda la web y dame un informe con:
- Enlaces internos y externos rotos.
- Títulos SEO o metadescripciones duplicados o de más de 60 / 155 caracteres.
- Entradas sin imagen destacada, sin texto alternativo o sin enlaces internos.
- Artículos con más de 6 meses sin actualizar.
- Resultado de PageSpeed (móvil y escritorio) de la portada y de los 3 artículos con más tráfico, con mejoras concretas.
No corrijas nada sin mi confirmación.

## Fase 8 — Actualización de precios
Crea un script que, a partir de un único archivo de configuración (`config/precios.json`: precio del kWh, tramos 2.0TD, precio de potencia, impuestos y días por mes):
1. Actualice las constantes de `calculadora.js`.
2. Recalcule las cifras de todos los artículos y me enseñe los cambios (antes → después) antes de aplicarlos.
3. Actualice la fecha «Precios revisados en…» de la portada.

## Fase 9 — Monetización (cuando tenga las cuentas)
- **Afiliación:** lista de todos los huecos `[AFILIADO: …]` con el producto sugerido y el artículo. Cuando te pase mi ID, sustituye los marcadores con `rel="sponsored nofollow"` y la nota de afiliación al principio.
- **AdSense:** cuando te pase mi ID `ca-pub-…`, prepara el fragmento de WPCode para la cabecera, el archivo ads.txt y la propuesta de posiciones de anuncios de PLAN.md. No lo actives sin mi confirmación.
- **Comprobación previa a AdSense:** confirma que se cumple la lista de la Prioridad 3 de PLAN.md.

## Fase 10 — Contenido para redes
Por cada artículo publicado, genera en `redes/<slug>.md`:
- 2 guiones de vídeo corto (30–45 s) para TikTok, Reels o Shorts: gancho en la primera frase, una cifra concreta y llamada a la calculadora.
- 3 textos para pines de Pinterest (título, descripción y texto para la imagen).
No publiques nada en redes.

---

## Orden recomendado
Fase 1 → Fase 2 (primera tanda) → Fase 3 → Fase 4 → Fase 2 (resto) → Fase 5 → Fase 6 → Fase 10. Las fases 7, 8 y 9 se ejecutan cuando toque (mensual, cuando cambien los precios y cuando tenga las cuentas).
