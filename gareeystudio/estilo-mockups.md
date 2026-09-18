# GAREEYSTUDIO — Guía de estilo para mockups de producto

**Marca:** GAREEYSTUDIO · ZGZ.2026
**Producto de referencia:** peana de metacrilato con foto personalizada (custom photo standee).
**Estado:** estilo APROBADO por el usuario el 2026-09-18 sobre el mockup
`mockups/01-acrylic-standee-boda/final/FINAL-v01-edit-chatgpt.png`.

Esta guía recoge los cambios que el usuario aplicó a mano (en ChatGPT) sobre la
salida de Higgsfield. **Son el estándar a reproducir en todos los mockups
futuros de la marca**, salvo que el usuario indique lo contrario.

---

## 1. Tipografía

| Elemento | Regla aprobada |
|---|---|
| Familia | Serif clásica de alto contraste, estilo Times New Roman / Didot (misma familia que el logotipo GAREEYSTUDIO en `reference-tipografia.png`). |
| Caja | **TODO EN MAYÚSCULAS**, en todos los textos del mockup (titular, etiquetas, llamadas). |
| Peso | Bold / semibold. Legible a tamaño de miniatura de listing. |
| Tracking | Normal-ligeramente amplio. No tan expandido como el logotipo. |
| Color | **Negro puro** (#000000). Nunca marrón ni gris. |
| Texto sobre placa dorada | Negro sobre oro. |

Textos habituales del producto (se conservan tal cual, solo cambia el estilo):
`CUSTOM PHOTO` · `AFTER CUTTING OUT THE IMAGE` · `YOUR PHOTO`

## 2. Acentos dorados (identidad visual de la marca)

Todo elemento gráfico de apoyo se hace en **oro metálico** con degradado
(luces cálidas claras y sombras ámbar), sin brillos exagerados:

- **Placa del titular:** rectángulo con esquinas redondeadas, relleno oro
  metálico con bisel sutil, texto negro centrado en dos líneas
  (`CUSTOM / PHOTO`). Sustituye a cualquier pincelada, splash o globo de color.
- **Flechas:** trazo sólido, curvo, con punta triangular, en oro metálico.
  Sin línea discontinua, sin bucles decorativos, sin contorno blanco.
  Dos flechas: una desde el inset "YOUR PHOTO" hacia el producto y otra
  desde la placa del titular hacia el producto.
- **Marco del inset "YOUR PHOTO":** borde fino de oro metálico con esquinas
  redondeadas, sin sombra visible, sobre la foto de origen del cliente.

Paleta orientativa del oro: base `#D4AF37`, luces `#F3DC8C`, sombras `#A67C1B`.

## 3. Lo que NO cambia respecto a la referencia original del producto

- Composición 1:1 (cuadrado), producto centrado, inset abajo-izquierda,
  titular arriba-derecha, etiqueta explicativa a la izquierda a media altura.
- Fondo de estudio blanco cálido con peanas desenfocadas de otras parejas.
- Peana de metacrilato con borde transparente visible y base circular.
- Fotografía realista, iluminación suave frontal-superior.
- Las personas del inset y las del producto son **la misma pareja**.

## 4. Cómo se produce (flujo aprobado)

1. **Higgsfield (WEBS)** — recreación fiel de la referencia con las personas
   sustituidas y tipografía serif. Modelo `gpt_image_2_5`, calidad `high`,
   resolución `2k`, ratio `1:1`, 2 variantes, 3 créditos por variante.
   Prompt base en `mockups/01-acrylic-standee-boda/prompt-higgsfield.txt`.
2. **Acabado gráfico** (placa dorada, flechas doradas, marco dorado, texto
   negro) — el usuario lo hace en ChatGPT o Canva. En futuras generaciones
   estos acentos se piden ya en el prompt de Higgsfield para ahorrar el paso
   manual, y se comprueba el resultado contra esta guía.
3. **Aprobación** — el usuario valida; la versión validada se guarda en
   `final/` con prefijo `FINAL-`.

## 5. Checklist de control antes de entregar un mockup

- [ ] Todos los textos en MAYÚSCULAS, serif bold, negro.
- [ ] Titular dentro de placa rectangular dorada con esquinas redondeadas.
- [ ] Flechas sólidas doradas, curvas, sin discontinuas ni contornos.
- [ ] Marco dorado fino en el inset de la foto del cliente.
- [ ] Nada marrón, ocre, ni pinceladas de color.
- [ ] Composición, fondo, producto y personas conforme a la referencia.
- [ ] Sin logos, marcas ni textos añadidos que el usuario no haya pedido
      (`GAREEYSTUDIO` y `ZGZ.2026` solo si se solicitan expresamente).
