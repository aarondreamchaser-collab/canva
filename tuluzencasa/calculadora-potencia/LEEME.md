# Calculadora de potencia contratada (Fase 4)

Estado: **solo en el repositorio**. No hay nada subido a WordPress ni activado en WPCode.

| Archivo | Qué es |
|---|---|
| `pagina.html` | Contenido de la página `/calculadora-potencia-contratada/` en formato de bloques: un bloque «HTML personalizado» con el CSS y el marcado de la calculadora, y debajo unas 800 palabras de texto. |
| `calculadora-potencia.js` | JavaScript del fragmento nuevo de WPCode. Sale sin hacer nada si la página no tiene `#tlp-app`. |
| `prueba/montar.py` | Monta `prueba/prueba.html` con el HTML real de una página de la web (tema GeneratePress) y la calculadora dentro. |
| `prueba/prueba.mjs` | Prueba con Playwright en 1280, 390 y 360 px: cálculos, avisos, barra móvil, scroll horizontal y errores de JS. Genera capturas. |

Constantes, iguales que en la calculadora de la portada: término de potencia 0,09 €/kW·día, impuesto eléctrico 1,0511, IVA 1,21, 30,4 días por mes, margen del 10 % y potencias 2,3 · 3,45 · 4,6 · 5,75 · 6,9 · 8,05 · 9,2 kW.

Las clases usan el prefijo `tlp-` para no chocar con las de la portada (`tlc-`).

## Plan del fragmento de WPCode (pendiente de tu confirmación)

1. **Crear el fragmento.** WPCode → Añadir fragmento → «Añade tu código personalizado» → tipo **JavaScript Snippet**.
   - Nombre: `Calculadora de potencia contratada`.
   - Código: el contenido de `calculadora-potencia.js`, sin etiquetas `<script>`, porque WPCode las añade.
2. **Inserción.** Automática, en **Pie de página de todo el sitio** (*Site Wide Footer*), como el fragmento de la portada.
   - El código comprueba `#tlp-app` en la primera línea: en cualquier otra página no hace nada.
   - Si tu versión de WPCode permite lógica condicional, se puede limitar además a la página `calculadora-potencia-contratada`. Así ni siquiera se carga en el resto de páginas, aunque no es imprescindible.
3. **Guardar el fragmento desactivado.** Primero crear la página en borrador con `pagina.html`. Después activar el fragmento y comprobar la vista previa en escritorio y móvil.
4. **Marcha atrás.** Basta con desactivar el fragmento. La página sigue mostrando el marcado, pero sin cálculos.

## Pendiente

- **Palabra clave.** TAREAS.md pide «qué potencia contratar» para esta página, pero es la misma que la del artículo `que-potencia-contratar`, y las dos compiten en Google. Propuesta: usar «calculadora de potencia contratada» en la página y dejar «qué potencia contratar» para el artículo. Se enlazan entre sí.
- **Enlaces.** El artículo `que-potencia-contratar` ya enlaza a esta página. Los dos enlaces funcionarán cuando ambas estén publicadas.
