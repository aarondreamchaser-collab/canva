# Arreglos de la auditoría del 2 de octubre de 2026 (estado al 4 de octubre)

| # | Arreglo | Cómo | Estado |
|---|---|---|---|
| 1.1 | Redirección de www | Ya funciona: `https://www.tuluzencasa.com/*` responde 301 a la versión sin www (comprobado el 3 de octubre). `wpcode-redireccion-www.php` queda de reserva; **no hace falta activarlo**. | Resuelto fuera de WordPress |
| 1.2 | Categorías vacías en la portada | Aplicado en la página 23 (sin enlace y con «Próximamente»): Factura y tarifas, Ahorrar luz, Placas solares y Coche eléctrico. `portada-categorias-proximamente.diff` queda como referencia. Cuando una tenga su primer artículo publicado, se vuelve a poner el enlace. | Hecho (4 oct) |
| 2.1 | Schema de los artículos | El ajuste global no se aplica a las entradas creadas por la API, y los campos `rank_math_rich_snippet` + `rank_math_snippet_article_type` solos dejan `"@type":""`. Se guarda un schema BlogPosting por entrada con `/rankmath/v1/updateSchemas` (`SCHEMA` en `scripts/subir2.py`, que ya lo hace al subir). Aplicado a 16–21, 92–98 y 104–106; JSON-LD BlogPosting comprobado en el HTML público de 16–21. | Hecho (4 oct) |
| 2.2 | Título y descripción de la portada | Rank Math de la página Inicio (ID 23): título «Calculadora de consumo de luz por aparato - Tu luz en casa» y descripción «Calcula cuánto te cuesta la luz aparato por aparato con la tarifa 2.0TD: punta, llano y valle, potencia e impuestos. Gratis y sin registro.» Comprobado en el HTML público. | Hecho (4 oct) |
| 2.5 | Dos H1 en la portada | GeneratePress gratuito no tiene «Desactivar elementos» (es Premium): fragmento PHP `wpcode-ocultar-titulo-portada.php`, que crea el titular en WPCode. | Pendiente (titular) |

Los fragmentos PHP pasan `php -l` sin errores.
