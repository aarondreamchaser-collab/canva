# PLAN.md — Monetización y próximos pasos de tuluzencasa.com

Léelo junto con CLAUDE.md. CLAUDE.md manda en estilo, precios, seguridad y reglas técnicas. Este archivo explica hacia dónde va el proyecto y qué falta.

## 1. Estado actual (octubre de 2026)
- WordPress en EasyWP, tema GeneratePress, Rank Math, WPCode (carga `calculadora.js` en el pie).
- Home con calculadora de factura por aparatos (página Inicio, portada estática).
- Páginas legales publicadas: Aviso legal, Política de privacidad y Política de cookies.
- 6 artículos publicados: aire acondicionado, radiador de aceite, freidora de aire, termo eléctrico, nevera y diferencial.
- Titular: particular (Aaron), sin empresa. Contacto: contacto@tuluzencasa.com.

## 2. Modelo de ingresos
La web gana dinero por tres vías, en este orden de puesta en marcha:

### 2.1 Google AdSense (base)
- **Todavía no está solicitado.** Se pedirá con 25–30 artículos publicados, Sobre nosotros y Contacto, y varias páginas ya indexadas.
- **No añadas ningún código de AdSense ni archivo ads.txt** hasta que el titular te pase su ID de editor (`ca-pub-…`).
- Cuando llegue el momento: el código irá por WPCode en la cabecera, ads.txt en la raíz y el mensaje de consentimiento de Google (Privacidad y mensajes) activado.
- Posiciones previstas: bajo la respuesta directa y la primera tabla, tras el segundo H2, uno cada 400–600 palabras y anclado en móvil. Nunca pegado a la calculadora ni a botones.

### 2.2 Afiliación (segunda fuente)
- **Amazon Afiliados España**: productos que ayudan a medir o reducir el consumo y que encajan con cada artículo.
  - Enchufes inteligentes con medidor de consumo (todos los artículos de consumo).
  - Programadores horarios para termo y electrodomésticos.
  - Regletas con interruptor (consumo en espera).
  - Freidoras de aire, radiadores de aceite, deshumidificadores, mantas eléctricas y bombillas LED en sus artículos.
- **Comparadores o comercializadoras de luz** con programa de afiliación (para los artículos de factura y tarifas). Investiga qué programas existen en España y resúmelos para que el titular decida; no te des de alta en nada.
- Reglas obligatorias:
  - No pongas enlaces de afiliado reales hasta que el titular te dé su ID de afiliado. Usa el marcador `[AFILIADO: producto]` donde iría el enlace.
  - Enlaces de afiliado con `rel="sponsored nofollow"`.
  - En cada artículo con enlaces de afiliado, añade al principio una nota breve: «Algunos enlaces de esta página son de afiliado: si compras a través de ellos, ganamos una pequeña comisión sin coste para ti.»
  - No inventes precios, especificaciones ni pruebas. Nunca escribas «lo hemos probado» si no es verdad. Las guías de compra se basan en criterios (potencia, consumo, programador, etc.) y en datos que el titular confirme.

### 2.3 Leads (más adelante)
- Formulario de presupuesto para instalaciones (boletín, renovación, placas solares, cargadores) conectado a n8n por webhook.
- **No lo actives** hasta que haya un instalador colaborador real que reciba los contactos.

## 3. Tareas pendientes, por prioridad

### Prioridad 1 — Páginas que exige AdSense (esta semana)
1. **Sobre nosotros** (`/sobre-nosotros/`): quién está detrás (Aaron, desde Calatayud, Zaragoza), por qué existe la web, cómo se calculan las cifras (enlace a la home) y cómo se revisan los artículos. Deja marcado con `[CONFIRMAR: …]` cualquier dato personal o profesional que el titular deba confirmar. **No afirmes que el autor es electricista ni que los artículos los revisa un profesional.**
2. **Contacto** (`/contacto/`): email contacto@tuluzencasa.com, plazo orientativo de respuesta y aviso de que no se dan diagnósticos de averías a distancia. Sin formulario por ahora.
3. Añadir ambas al menú **Legal** del pie de página.

### Prioridad 2 — Contenido antes de noviembre (2–3 semanas)
Artículos en borrador, mismas reglas que los anteriores (CLAUDE.md):

| Slug | Categoría | Tipo |
| --- | --- | --- |
| como-leer-la-factura-de-la-luz | factura-luz | Pilar |
| que-potencia-contratar | factura-luz | Pilar |
| pvpc-o-mercado-libre | factura-luz | Comercial (afiliación de tarifas) |
| trucos-para-ahorrar-luz | ahorro | Pilar |
| consumo-de-electrodomesticos | consumo | Pilar (tabla de todos los aparatos de la calculadora) |
| calefaccion-electrica-mas-barata | climatizacion | Pilar |
| bomba-de-calor-o-radiadores-electricos | climatizacion | Comparativa |
| radiador-de-aceite-convector-o-calefactor | climatizacion | Comparativa |
| cuanto-consume-una-estufa-electrica | climatizacion | Consumo |
| cuanto-consumen-los-emisores-termicos | climatizacion | Consumo |
| cuanto-consume-una-manta-electrica | climatizacion | Consumo |
| cuanto-consume-un-deshumidificador | climatizacion | Consumo |
| placas-solares-precio-amortizacion | placas-solares | Pilar |
| enchufe-inteligente-medidor-consumo | ahorro | Guía de compra (afiliación) |

Después de crearlos, añade enlaces desde los 6 artículos publicados hacia los nuevos que sean pertinentes (máximo 2 por artículo) y desde cada pilar hacia los artículos de su categoría.

### Prioridad 3 — Preparar la monetización (cuando haya 25–30 artículos)
1. Lista de los huecos de afiliado `[AFILIADO: …]` que hay en todos los artículos, para que el titular dé de alta los productos.
2. Propuesta de colocación de anuncios con WPCode o hooks de GeneratePress, lista para activar en cuanto llegue el ID de AdSense.
3. Comprobación final antes de pedir AdSense: páginas legales completas, Sobre nosotros, Contacto, sin enlaces rotos, sin `[VERIFICAR]` ni `[CONFIRMAR]`, y todas las entradas con imagen destacada.

## 4. Lo que hace siempre el titular, no tú
- Revisar y publicar cada artículo.
- Darse de alta en AdSense, Amazon Afiliados y cualquier otro programa.
- Poner sus fotos propias y las imágenes destacadas.
- Activar HackGuardian y el Firewall de EasyWP al terminar cada sesión.
