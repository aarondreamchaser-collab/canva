# CLAUDE.md — tuluzencasa.com

## Qué es este proyecto
Web de contenido en español (España) sobre consumo eléctrico doméstico, factura de la luz, ahorro e instalación eléctrica. Se monetiza con AdSense, afiliación y, más adelante, leads. WordPress en EasyWP (Namecheap), tema GeneratePress, Rank Math SEO. Sin acceso SSH: todo se hace por la API REST de WordPress.

## Acceso
- Web: https://tuluzencasa.com
- API: https://tuluzencasa.com/wp-json/wp/v2/
- Credenciales en variables de entorno: `WP_USER` y `WP_APP_PASSWORD` (contraseña de aplicación). Autenticación HTTP Basic.
- Nunca muestres, registres ni guardes la contraseña en archivos, commits ni salidas de consola.

## Reglas de seguridad
- Los artículos se crean SIEMPRE con `status: "draft"`. Nunca publiques un artículo.
- No borres ni modifiques entradas, páginas, categorías, usuarios, plugins ni ajustes existentes salvo que la tarea lo pida explícitamente.
- Antes de cualquier cambio de ajustes del sitio, explica qué vas a cambiar y espera confirmación.
- El menú Principal solo debe incluir categorías con al menos una entrada publicada. Cuando el titular publique artículos de una categoría nueva, propón añadirla al menú y hazlo cuando lo confirme.
- Si una petición devuelve 403 o un bloqueo, para y avisa: probablemente el firewall o HackGuardian de EasyWP está activo.
- No metas `<script>` dentro del contenido de páginas o entradas: WordPress convierte algunos `&&` en `&#038;&#038;` y rompe el JavaScript. El JS de la calculadora de consumo vive en WPCode (fragmento «Calculadora Home», JavaScript, pie, solo en la página `calculadora-consumo-electrico`) y su copia está en `calculadora.js`. La calculadora está en la página «Calculadora de consumo eléctrico» (ID 156, `https://tuluzencasa.com/calculadora-consumo-electrico/`), cuyo contenido es `rediseno/pagina-calculadora-consumo.html`; la portada (ID 23) ya no la lleva. Si cambias la calculadora, actualiza `calculadora.js` y pega el contenido en ese fragmento.
- Diseño del sitio: fragmentos de WPCode «Diseño tuluzencasa» (CSS) y «Plantilla tuluzencasa» (PHP), con copia en `rediseno/`. La plantilla añade a cada entrada la ruta de navegación, la fecha de actualización, los huecos de anuncios, la caja de autor y los relacionados: no los escribas en el contenido.

## Categorías (slug → nombre)
consumo → Consumo de aparatos · factura-luz → Factura y tarifas · ahorro → Ahorrar luz · instalacion → Averías e instalación · climatizacion → Calefacción y aire · placas-solares → Placas solares · coche-electrico → Coche eléctrico.
Consulta sus IDs con `GET /wp-json/wp/v2/categories?per_page=100` antes de usarlas.

## Criterios de los precios (deben coincidir con la calculadora de consumo)
- Precio de la energía: 0,13 €/kWh sin impuestos. Impuestos: impuesto eléctrico 5,11 % e IVA 21 % → factor 1,272 → **0,165 €/kWh con impuestos**. Indica siempre este precio en el artículo y que el lector puede cambiarlo por el de su factura.
- Tarifa por horas (2.0TD) orientativa: punta 0,19 · llano 0,12 · valle 0,08 €/kWh sin impuestos. Punta 10–14 h y 18–22 h; llano 8–10, 14–18 y 22–24 h; valle 0–8 h y fines de semana.
- Factores de uso real: aire acondicionado 0,6 · radiador de aceite 0,6 · estufa 0,85 · nevera y congelador 0,2 (sobre 150 W nominales) · termo 0,7 · horno 0,6 · inducción 0,7 · vitrocerámica 0,75 · lavavajillas 0,55 · secadora 0,8 · freidora de aire 0,7 · emisor térmico 0,6 · manta eléctrica 0,5 · deshumidificador 0,8 · resto 1.
- Aire acondicionado de 3.000 frigorías = 1.000 W de potencia eléctrica (EER 3,5). Usa este valor en artículos y en la calculadora de consumo.
- Horno eléctrico de referencia: 2.200 W con factor 0,6 (45 min por uso, precalentado incluido), igual que en la calculadora de consumo.
- Mes = 30,4 días y año = 12 meses (364,8 días), igual que la calculadora de consumo. Temporadas en meses: verano 3 meses, invierno 4 meses. Lo que se cuenta por usos (p. ej., 12 usos al mes) no depende de los días.
- Calcula todas las cifras con un script (no de memoria) y redondea a 2 decimales en euros.
- Justo debajo de la primera tabla de cada artículo va el párrafo «Cálculos con precios de octubre de 2026». Cada vez que cambien los precios de referencia, actualiza el mes y el año en esa línea en todos los artículos (y la calculadora si corresponde).

## Estilo de los artículos
- Español de España, tuteo, frases claras, sin relleno ni frases de IA ("en el mundo actual", "es importante destacar", "en conclusión").
- Respuesta directa en las dos primeras frases, con una cifra concreta.
- Tabla con coste por hora, por día y por mes (y por año si aporta) para varias potencias o situaciones.
- 1.200–1.800 palabras, H2 descriptivos, un apartado de trucos de ahorro concretos y 3–5 preguntas frecuentes al final.
- Sin datos inventados: nada de estudios, porcentajes o marcas que no puedas justificar. Si un dato necesita verificación, márcalo como `[VERIFICAR: …]`.
- No afirmes que el autor es electricista ni que el contenido está revisado por un profesional.
- En temas de instalación eléctrica: indica claramente qué puede comprobar el usuario sin riesgo y qué debe hacer un instalador autorizado (REBT, RD 842/2002). Nunca des instrucciones para manipular el cuadro con tensión.
- 3 enlaces internos por artículo (a otros artículos del plan o a la home `https://tuluzencasa.com/`), con anchor descriptivo.
- Al final de cada artículo: «Calcula tu caso exacto con nuestra calculadora de consumo», con el enlace en «nuestra calculadora de consumo» a `https://tuluzencasa.com/calculadora-consumo-electrico/`. Si se menciona la calculadora en el texto, llámala «nuestra calculadora de consumo» (nunca «la calculadora de la portada»).
- Contenido en formato de bloques de Gutenberg (HTML con comentarios `<!-- wp:paragraph -->`, `<!-- wp:heading -->`, `<!-- wp:table -->`, `<!-- wp:list -->`).
