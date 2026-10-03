# Arreglos de la auditoría del 2 de octubre de 2026 (preparados, sin aplicar)

| # | Arreglo | Cómo | Estado |
|---|---|---|---|
| 1.1 | Redirección de www | Ya funciona: `https://www.tuluzencasa.com/*` responde 301 a la versión sin www (comprobado el 3 de octubre). `wpcode-redireccion-www.php` queda de reserva; **no hace falta activarlo**. | Resuelto fuera de WordPress |
| 1.2 | Categorías vacías en la portada | `portada-categorias-proximamente.diff`: Factura y tarifas, Ahorrar luz, Placas solares y Coche eléctrico pasan a «Próximamente», sin enlace. Cuando una tenga su primer artículo publicado, se vuelve a poner el enlace. | Pendiente de confirmación |
| 2.1 | Schema de los artículos | Rank Math → Títulos y metas → Entradas → «Tipo de schema»: **Artículo** (BlogPosting). Afecta a todas las entradas; las páginas no cambian. No requiere código. | Pendiente (ajuste del plugin) |
| 2.2 | Título y descripción de la portada | Rank Math de la página Inicio (ID 23): título «Calculadora de consumo de luz por aparato - Tu luz en casa» y descripción «Calcula cuánto te cuesta la luz aparato por aparato con la tarifa 2.0TD: punta, llano y valle, potencia e impuestos. Gratis y sin registro.» | Pendiente de confirmación |
| 2.5 | Dos H1 en la portada | Mejor sin código: editar Inicio → GeneratePress → «Desactivar elementos» → «Título del contenido». Alternativa: `wpcode-ocultar-titulo-portada.php` (PHP, solo en el frontend). | Pendiente de confirmación |

Los fragmentos PHP pasan `php -l` sin errores.
