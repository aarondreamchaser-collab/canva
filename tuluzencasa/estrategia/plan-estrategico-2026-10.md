# Plan estratégico de tuluzencasa.com (octubre de 2026)

**Estado: propuesta. No se ha publicado ni cambiado nada en la web.** Espera el OK del titular antes de crear nada.

Fuentes consultadas el 7-10-2026. Al final de cada apartado se marca **[VERIFICAR]** lo que no he podido comprobar en una fuente primaria. Los datos propios (producción solar y población) están en `estrategia/pvgis_ccaa.json` y `estrategia/poblacion_ine_2021.json`, con el script que los genera.

---

## 0. Punto de partida

- **Contenido:** 36 entradas publicadas.
  - Repartidas entre consumo de aparatos (la mayoría), factura y tarifas, calefacción y aire, averías e instalación, ahorro, placas solares y coche eléctrico.
  - Una página piloto por comunidad (Aragón).
  - 8 páginas: portada, 2 calculadoras, legales, contacto y sobre nosotros.
- **Herramientas:** calculadoras v3 de consumo y potencia, publicadas el 7-10-2026.
- **Ventaja diferencial:** cifras calculadas con script y un precio de referencia único (0,165 €/kWh), fuentes oficiales enlazadas y herramientas propias. Es lo que hay que proteger: cada pieza nueva tiene que aportar un cálculo, un dato o una herramienta que no esté en otra web.
- **AdSense:** pendiente de aprobación. Hasta que aprueben, la prioridad es la calidad y la confianza, no monetizar.

---

## 1. Contenido y estructura

### 1.1 Arquitectura final propuesta

```
Portada
├── Calculadoras (sección de herramientas)
│   ├── Consumo eléctrico (v3)            ✔ existe
│   ├── Potencia contratada (v3)          ✔ existe
│   ├── Precio de la luz hoy por horas    ✚ nueva (apartado 3)
│   ├── Placas solares (PVGIS)            ✚ nueva
│   ├── Coste de cargar el coche          ✚ nueva
│   ├── Tu factura: ¿qué tarifa te conviene? ✚ nueva
│   └── ¿Tienes derecho al bono social?   ✚ nueva
├── Guías por temas (7 categorías + 1)
│   ├── Consumo de aparatos      → pilar: «Cuánto consume cada aparato» (tabla resumen enlazada)
│   ├── Factura y tarifas        → pilar: «Cómo leer la factura de la luz» ✔ (reforzar como pilar)
│   ├── Trámites ✚ nueva categoría → pilar: «Trámites de la luz: alta, titular, potencia y reclamaciones»
│   ├── Ahorrar luz              → pilar: «Cómo pagar menos luz: lo que de verdad ahorra»
│   ├── Calefacción y aire       → pilar: «Calefacción eléctrica más barata» ✔
│   ├── Averías e instalación    → pilar: «Se ha ido la luz» ✔ + «Boletín eléctrico» ✔
│   ├── Placas solares           → pilar: «Placas solares en casa» ✔ (ampliar con PVGIS)
│   └── Coche eléctrico          → pilar: «Cargar el coche eléctrico en casa» ✔
├── Luz por comunidades          → página índice (mapa/tabla) + 1 página por comunidad
├── Actualidad ✚                 → noticias de fuentes oficiales (1-2 por semana)
└── Sobre nosotros / Metodología / Contacto / Legales
```

**Menú (cabe en una fila, ya probado con 5-6 entradas):**
`Consumo de aparatos · Factura y tarifas · Trámites · Ahorro y placas ▾ · Más temas ▾ · Calculadoras ▾`

- «Ahorro y placas» agrupa Ahorrar luz, Placas solares y Coche eléctrico.
- «Más temas» agrupa Calefacción y aire, Averías e instalación, Luz por comunidades y Actualidad.
- Según CLAUDE.md, el menú solo incluye categorías con al menos una entrada publicada: Trámites y Actualidad entran cuando tengan contenido.

**Enlazado (reglas fijas):**
1. Cada artículo enlaza a su **pilar** y a la **calculadora** que le corresponde (ya se hace con la de consumo; añadir la de potencia, la de placas y la de coche donde toque).
2. Cada pilar enlaza a todos los artículos de su tema, con una frase de contexto, no una lista suelta.
3. Las páginas de comunidad enlazan a los pilares nacionales. Los artículos nacionales enlazan a la página índice de comunidades, nunca a 19 páginas a la vez.
4. Las noticias de Actualidad enlazan a la guía que explica el tema de fondo. Así la noticia caduca, pero la guía se actualiza.
5. Se mantiene la regla actual: como máximo 2 enlaces nuevos por artículo publicado y por tanda.

### 1.2 Próximos 30 artículos (tandas de 4, por prioridad)

**Criterios de orden:**
- Temporada: estamos en otoño, así que van primero calefacción y trámites de cambio de tarifa.
- Huecos frente a la competencia (1.3).
- Que el artículo dé apoyo a una herramienta nueva.
- Que haya datos oficiales para calcularlo.

No tengo acceso a volúmenes de búsqueda (Planificador de Google Ads o Search Console), así que el orden **no** se basa en volumen. **[VERIFICAR]** Conviene revisarlo cuando haya datos de Search Console.

| Tanda | # | Artículo propuesto | Categoría | Por qué ahora |
|---|---|---|---|---|
| 1 | 1 | Tarifa fija o indexada: cuál te conviene según tu consumo | Factura | Hueco claro; base del futuro comparador |
| 1 | 2 | Bono social térmico: qué es, cuánto se cobra y quién lo recibe | Ahorro / normativa | Temporada de invierno |
| 1 | 3 | Ver tu consumo por horas: el contador inteligente y Datadis | Trámites | Base de la herramienta de factura |
| 1 | 4 | Calefacción por suelo radiante eléctrico: cuánto consume | Climatización | Temporada; completa la serie de calefacción |
| 2 | 5 | Cambiar la potencia contratada: pasos, coste y plazos | Trámites | Apoya la calculadora de potencia |
| 2 | 6 | Alta de luz en una vivienda: pasos, derechos de acometida y plazos | Trámites | Hueco claro frente a la competencia |
| 2 | 7 | Cambio de titular de la luz: cómo hacerlo y qué cuesta | Trámites | Hueco claro |
| 2 | 8 | Compensación de excedentes y batería virtual | Placas | Muy buscado; apoya la calculadora de placas |
| 3 | 9 | Punto de recarga en casa y en garaje comunitario: normativa (ITC-BT-52, Ley de Propiedad Horizontal) | Coche / normativa | Apoya la calculadora de coche y la captación de instaladores |
| 3 | 10 | Deducciones del IRPF por eficiencia energética (prorrogadas hasta 2026 y 2027) | Ahorro / normativa | Dato oficial reciente (Real Decreto-ley 7/2026, art. 36; el RDL 16/2025 fue derogado al no convalidarse) |
| 3 | 11 | Cuánto producen las placas solares en cada comunidad (PVGIS) | Placas | Datos propios ya calculados (apartado 2) |
| 3 | 12 | Termo aerotérmico (bomba de calor para agua caliente): cuánto consume | Consumo | Continúa la serie de aerotermia |
| 4 | 13 | Reclamar a tu compañía de luz: pasos, plazos y arbitraje de consumo | Trámites | Hueco; para la confianza |
| 4 | 14 | Factura estimada o lectura errónea: qué hacer | Factura | Consulta frecuente en invierno |
| 4 | 15 | Corte de luz por impago: plazos y suministros esenciales | Normativa | Tema sensible: solo con BOE |
| 4 | 16 | Aire acondicionado portátil: cuánto consume y por qué gasta más | Consumo | Sirve en primavera; se prepara antes |
| 5 | 17 | Autoconsumo compartido en una comunidad de vecinos | Placas | Hueco; potencial de captación |
| 5 | 18 | Baterías para placas solares: cuándo compensan | Placas | Cálculo con PVGIS |
| 5 | 19 | Certificado energético de la vivienda: qué es y cuánto cuesta | Normativa | Enlaza con las deducciones del IRPF |
| 5 | 20 | Llamadas y visitas comerciales de luz: tus derechos | Trámites | Protege al lector; para la confianza |
| 6 | 21 | Potencia distinta de día y de noche (P1 y P2) | Factura | Clave para el coche eléctrico |
| 6 | 22 | Impuestos de la factura de la luz: impuesto eléctrico, IVA, IGIC e IPSI | Normativa | Base de las páginas de Canarias, Ceuta y Melilla |
| 6 | 23 | Qué potencia de cargador elegir: 3,7, 7,4 u 11 kW | Coche | Apoya la calculadora de coche |
| 6 | 24 | Revisión de la instalación eléctrica en viviendas antiguas: cuándo hace falta | Instalación | Encaja con el instalador local |
| 7 | 25 | Comunidades energéticas: qué son y cómo apuntarse | Placas / normativa | Hueco |
| 7 | 26 | Bonificaciones del IBI y el ICIO por poner placas solares | Placas | Datos municipales (cuidado con la actualización) |
| 7 | 27 | Bicicleta y patinete eléctricos: cuánto cuesta cargarlos | Coche | Fácil, buen enlace con la calculadora |
| 7 | 28 | Cuánto consume una vivienda media en España | Consumo | Pilar estadístico (datos oficiales) |
| 8 | 29 | Precio de la luz en 2026: cómo ha evolucionado, mes a mes | Actualidad / factura | Sale de los datos de REE del apartado 3 |
| 8 | 30 | Ayudas para placas solares y aerotermia: dónde mirar en cada comunidad | Placas / normativa | Solo con convocatorias verificadas |

Todos siguen CLAUDE.md:
- Precio 0,165 €/kWh y mes de 30,4 días.
- Cifras calculadas con script.
- Fuentes oficiales con enlace y fecha.
- Tabla, trucos y 3-5 preguntas frecuentes.
- **[VERIFICAR]** en cada dato que no esté en una fuente primaria.

### 1.3 Temas que faltan frente a las webs de referencia

Revisadas el 7-10-2026: [Selectra](https://selectra.es/energia), [Tarifaluzhora](https://tarifaluzhora.es/), Papernest, Kelisto y Rastreator (estas tres ya se revisaron en el rediseño).

| Tema que cubren ellas | ¿Lo tenemos? | Propuesta |
|---|---|---|
| Precio de la luz hoy y mañana, por horas | No | Herramienta con datos de REE (apartado 3) |
| Trámites: alta, cambio de titular, cambio de potencia | No | Categoría «Trámites» (tandas 1-2) |
| Comparador de tarifas | No | Herramienta «Tu factura» (apartado 5), sin hacernos comparador comercial |
| Fichas de compañías y teléfonos | No | **No recomendado:** contenido fino y fácil de quedar desfasado. Como mucho, distribuidoras en las páginas de comunidad |
| Ayudas y subvenciones | Parcial | Artículo 30 y bloque en cada comunidad, solo con convocatorias verificadas |
| Bono social (calculadora) | Artículo sí, herramienta no | Simulador (apartado 5) |
| Autoconsumo: excedentes, baterías, comunidades | Parcial | Tandas 2, 5 y 7 |
| Análisis de factura gratis o de pago | No | Servicio propio (apartado 4.4), después de AdSense |
| Alertas por email o Telegram del precio | No | Fase 3 (opcional) |

---

## 2. Comunidades autónomas sin contenido duplicado

### 2.1 Qué cambia de verdad en cada comunidad

| Dato | ¿Cambia? | Fuente | Cómo se usa |
|---|---|---|---|
| **Distribuidora** | Sí, por zonas | Web de cada distribuidora y [CNMC](https://www.cnmc.es/) | Quién atiende las averías, los contadores y los trámites de acometida. Ejemplos: e-distribución en partes de Andalucía, Aragón, Baleares, Canarias, Cataluña, Extremadura, Castilla y León, Galicia y Ceuta; i-DE en Madrid, C. Valenciana, Murcia, País Vasco, Navarra, La Rioja y otras; UFD sobre todo en Galicia; E-Redes en Asturias; Viesgo en Cantabria. **[VERIFICAR]** el reparto exacto por provincia con los mapas de cada distribuidora antes de publicar. |
| **Impuestos** | Solo Canarias, Ceuta y Melilla | AEAT y normas forales | **Canarias:** IGIC 0 % en el suministro de la vivienda con 10 kW o menos y 3 % en el resto (varias fuentes coinciden). **Ceuta y Melilla:** IPSI en lugar de IVA, con un tipo reducido para la electricidad (las fuentes secundarias dan el 1 %). **[VERIFICAR]** en las ordenanzas fiscales de cada ciudad y en la Ley del Impuesto Especial sobre la Electricidad si hay bonificación en Ceuta y Melilla. |
| **Zona climática (CTE)** | Sí, por **provincia y altitud** | [CTE DB-HE, anejo B, tabla B.1](https://www.codigotecnico.org/) (PDF oficial) | Ya hecho en Aragón: Zaragoza C3/D3/E1, Huesca C3/D3/D2/E1 y Teruel C3/C2/D2/E1 según la altitud. Cuidado: los resultados de búsqueda que dan una sola zona por capital no sirven; hay que leer la tabla oficial. |
| **Producción solar** | Sí | [PVGIS 5.3 (JRC)](https://re.jrc.ec.europa.eu/pvg_tools/) | Calculada (abajo): de 1.206 a 1.769 kWh por kWp al año. |
| **Ayudas autonómicas** | Sí, y caducan | Boletín oficial de cada comunidad y [IDAE](https://www.idae.es/) | Solo se citan convocatorias abiertas, con enlace al boletín y fecha. Las fuentes secundarias consultadas dan importes contradictorios: **no publicar ninguna cifra sin la convocatoria oficial.** |
| **Consumo y reclamaciones** | Sí | Dirección general de consumo y junta arbitral de cada comunidad | Ya hecho en Aragón (arbitraje). |
| **Industria (boletín y altas)** | Sí | Servicio de industria de cada comunidad y su sede electrónica | Cómo se tramita el certificado de instalación (CIE) y si se hace en línea. |
| **Clima y uso** | Sí | AEMET (grados-día) **[VERIFICAR]** si hay serie descargable | Calefacción frente a aire acondicionado: calcular el coste tipo con la calculadora. |

**Producción solar estimada por capital** (PVGIS 5.3, 1 kWp, pérdidas del 14 %, inclinación y orientación óptimas; consulta del 7-10-2026):

| Comunidad | Ciudad | kWh/kWp·año |
|---|---|---|
| Canarias | Santa Cruz de Tenerife | 1.769 |
| Andalucía | Sevilla | 1.672 |
| C. Valenciana | Valencia | 1.632 |
| Castilla-La Mancha | Toledo | 1.631 |
| Región de Murcia | Murcia | 1.630 |
| C. de Madrid | Madrid | 1.621 |
| Aragón | Zaragoza | 1.618 |
| Extremadura | Mérida | 1.615 |
| Canarias | Las Palmas de G. C. | 1.612 |
| Melilla | Melilla | 1.600 |
| Illes Balears | Palma | 1.598 |
| Ceuta | Ceuta | 1.594 |
| Cataluña | Barcelona | 1.572 |
| Castilla y León | Valladolid | 1.560 |
| La Rioja | Logroño | 1.429 |
| Navarra | Pamplona | 1.406 |
| Galicia | Santiago de Compostela | 1.295 |
| País Vasco | Vitoria-Gasteiz | 1.277 |
| Cantabria | Santander | 1.210 |
| Asturias | Oviedo | 1.206 |

A 0,165 €/kWh, 1 kWp en Sevilla produce unos 276 € de electricidad al año, y en Oviedo unos 199 €. Esa diferencia ya hace única cada página. La cifra exacta se calculará con el script en cada artículo.

### 2.2 Plantilla de página (secciones fijas, contenido único)

Es la estructura de la página de Aragón, ya publicada:

1. **Qué es igual en toda España y qué cambia aquí:** 2 párrafos, con lo que cambia en primer lugar.
2. **Quién te lleva la luz:** distribuidora o distribuidoras por zona, cómo avisar de una avería y enlace oficial.
3. **El clima y tu factura:** zonas del CTE por provincia y altitud, con la tabla de coste de calefacción tipo calculada.
4. **Agua caliente:** coste en cada capital, según la temperatura del agua de red. **[VERIFICAR]** la fuente por provincia, como en Aragón.
5. **Placas solares:** PVGIS por provincia, producción y ahorro tipo, y ayudas abiertas solo si hay convocatoria verificada.
6. **Impuestos:** solo en Canarias, Ceuta y Melilla; en el resto, una línea («IVA e impuesto eléctrico como en el resto de España»).
7. **Trámites:** industria (boletín), consumo y arbitraje, con enlaces oficiales y la fecha de consulta.
8. **Trucos para esta comunidad:** al menos 3 propios del clima, de la tarifa o del autoconsumo, nunca genéricos.
9. **Preguntas frecuentes:** 3-5 propias de la comunidad.

**Reglas contra las páginas puerta** ([política de Google sobre *doorway abuse* y *scaled content abuse*](https://developers.google.com/search/docs/essentials/spam-policies)):
- Mínimo **5 datos propios** por comunidad (distribuidora, zonas, PVGIS, coste de agua caliente o calefacción calculado, organismos). Sin ellos, la página no se publica.
- Nada de textos con «Aragón» cambiado por «Murcia». Cada introducción y cada truco se escriben de nuevo.
- **Máximo 4 comunidades por tanda.** Nunca las 19 a la vez.
- La página índice enlaza a cada comunidad con su dato más llamativo (por ejemplo, «Asturias: 1.206 kWh/kWp, la que menos produce»).

### 2.3 Orden propuesto (población del INE)

Orden por población (INE, cifras oficiales del padrón a 1-1-2021, tabla 2853; la última cifra puede variar algo, pero no el orden de las grandes **[VERIFICAR]**):

| Tanda | Comunidades |
|---|---|
| A | Andalucía (8,47 M), Cataluña (7,76 M), C. de Madrid (6,75 M), C. Valenciana (5,06 M) |
| B | Galicia (2,70 M), Castilla y León (2,38 M), País Vasco (2,21 M), Canarias (2,17 M; impuestos propios) |
| C | Castilla-La Mancha (2,05 M), Región de Murcia (1,52 M), Illes Balears (1,17 M), Extremadura (1,06 M) |
| D | Asturias (1,01 M), Navarra (0,66 M), Cantabria (0,58 M), La Rioja (0,32 M) |
| E | Ceuta y Melilla (una página cada una; IPSI) |

**Alternativa:** si Search Console da datos, ordenar por impresiones de «luz + comunidad». Andalucía es la más costosa: 8 provincias con zonas climáticas distintas.

### 2.4 Qué se puede mantener al día y cada cuánto

| Dato | Frecuencia | Cómo |
|---|---|---|
| Ayudas autonómicas | Mensual | Revisión manual de los boletines oficiales y el IDAE; anotar «revisado en [mes]» |
| Impuestos (IGIC, IPSI, IVA, impuesto eléctrico) | Trimestral y cuando lo publique el BOE | La alerta del BOE de Actualidad lo detecta |
| Distribuidora y organismos | Semestral | Comprobar enlaces (script de enlaces rotos ya hecho en la revisión) |
| PVGIS y zonas del CTE | Solo si cambia la versión de PVGIS o el CTE | Script `pvgis_ccaa.py` |
| Precio de referencia (0,165 €/kWh) | Cuando cambie | Como dice CLAUDE.md: cambiar «Cálculos con precios de [mes] de [año]» en todo |

---

## 3. Actualidad y datos en tiempo real

### 3.1 Página «Precio de la luz hoy por horas»

**Fuentes de datos (consultadas el 7-10-2026):**

| Opción | ¿Clave? | Qué da | Notas |
|---|---|---|---|
| **API de ESIOS** (`api.esios.ree.es`), indicador **1001** (PVPC 2.0TD) | **Sí, token personal gratuito**: se pide a `consultasios@ree.es` (documentado en [esios.ree.es/es/token](https://www.esios.ree.es/es/token) y en integraciones como [Home Assistant](https://home-assistant.io/integrations/pvpc_hourly_pricing)) | Precio PVPC de hoy y de mañana | Es la fuente oficial del PVPC. **[VERIFICAR]** las condiciones de uso y reutilización: la web de ESIOS es una aplicación y no he podido leer su aviso legal; preguntarlo al pedir el token. |
| **API REData** (`apidatos.ree.es`) | No consta que haga falta ([documentación](https://www.ree.es/es/apidatos)) | Precios de mercado y componentes, demanda y generación | Solo admite GET. No se publican límites ni licencia **[VERIFICAR]**. |
| Ambas | — | — | **Las dos me devolvieron un bloqueo antibots (Incapsula) desde este servidor.** Antes de construir nada hay que probar desde el alojamiento de EasyWP que responden. |

**Dato importante:** desde el 1-10-2025 el mercado diario fija un precio cada **15 minutos** (96 al día). Las facturas siguen usando la media de cada hora, porque los contadores registran por horas ([explicación divulgativa](https://autosolar.es/precio-luz/horario-precio-luz-que-debes-saber-del-mercado-cuarto-horario)). **[VERIFICAR]** con el token si el indicador 1001 sigue siendo horario.

**Diseño en WordPress sin plugins pesados (2 piezas):**
1. **Fragmento PHP en WPCode** («Precio luz hoy, datos»):
   - Registra una tarea programada (`wp_schedule_event`, dos veces al día, por ejemplo a las 20:45 y a las 08:00) que pide los datos a ESIOS con `wp_remote_get` y el token.
   - El token se guarda como constante en el propio fragmento: nunca en el contenido ni en el repo.
   - Guarda las 24 horas de hoy y de mañana en una opción de WordPress.
   - Expone un endpoint REST de solo lectura (`/wp-json/tl/v1/precio`) para el JavaScript.
   - **Ojo:** en EasyWP, WP-Cron solo se dispara con visitas, así que la tarea se lanza también cuando un visitante pide el endpoint y los datos tienen más de 6 horas.
2. **Fragmento JavaScript y contenido de la página:**
   - El contenido lleva el texto explicativo (para Google) y un contenedor.
   - El JavaScript pinta la tabla de 24 horas, la gráfica de colores por tramo, la hora más barata y la más cara, y el «mañana» cuando REE lo publica. Suele ser por la tarde-noche **[VERIFICAR]** la hora exacta con los datos.
   - Mismo estilo que la calculadora v3 (reutiliza sus componentes).
3. **Caché de EasyWP:** el HTML se cachea, así que los datos se piden por JavaScript al endpoint. **[VERIFICAR]** que EasyWP no cachee las respuestas del REST demasiado tiempo.

**Para no hacer «contenido escalado»:** una **única URL** permanente, y nunca una página por día. El histórico va en una tabla mensual, en el artículo 29.

### 3.2 Sección «Actualidad»

**Fuentes (solo oficiales):**
- BOE: [API de datos abiertos, sin clave, probada](https://www.boe.es/datosabiertos/api/boe/sumario/20261006); devuelve 252 disposiciones el 6-10-2026.
- CNMC (notas de prensa).
- MITECO (sala de prensa).
- IDAE (noticias).
- REE (notas e informes).

**Proceso semanal propuesto:**
1. **Lunes, vigilancia automática:**
   - Un script en el repo lee el sumario del BOE de la semana y las páginas de noticias de las otras cuatro fuentes.
   - Filtra por palabras clave (electricidad, PVPC, autoconsumo, bono social, peajes, IVA, impuesto eléctrico).
   - Descarta anuncios y licitaciones: en la prueba del 6-10-2026, casi todo lo que contenía «eléctric» eran licitaciones y anuncios de la sección V.
   - Me deja una lista corta.
2. **Selección:** propongo 1-2 temas, con el enlace oficial y por qué afectan a la factura de una casa. Tú eliges.
3. **Redacción:**
   - Borrador con el titular informativo, qué cambia, desde cuándo, a quién afecta y cuánto supone en euros (calculado con script si se puede).
   - Enlace a la fuente oficial con la fecha y a la guía de fondo.
   - Se sube **como borrador**.
4. **Revisión y publicación:** las haces tú.
5. **Para evitar contenido de poco valor:** cada noticia tiene que llevar al menos uno de estos tres:
   - una cifra propia calculada,
   - un «qué tienes que hacer»,
   - un cambio en una guía existente (y se actualiza la guía).

   Si no hay noticias así esa semana, no se publica nada.
6. **Prohibido:** reescribir noticias de medios o de redes sociales. La fuente siempre es el documento oficial.

---

## 4. Monetización además de AdSense

### 4.1 Afiliación de comercializadoras y comparadores

| Programa | Condiciones verificadas | ¿Webs nuevas? | ¿Empresa o autónomo? |
|---|---|---|---|
| **niba** (comercializadora, en Awin) | Hasta **45 € por alta confirmada**; validación en un máximo de 45 días; cookie de 30 días; prohibido pujar por su marca y el tráfico incentivado ([perfil en Awin](https://ui.awin.com/merchant-profile/118409)) | Admite comparadores, portales de ahorro y blogs | Ver Awin |
| **Awin** (red) | **Depósito de 5 £, devuelto con el primer pago** ([Awin](https://www.awin.com/gb/compliance-and-regulations/application-process-and-joining-fee)); verificación con tarjeta. **Autofacturación:** Awin emite las facturas y pide los datos fiscales y si estás registrado a efectos de IVA ([condiciones de agosto de 2025, cláusula 7](https://www.awin.com/docs.awin.com/Legal/Publisher+Terms/2025/ES_Awin-AG-Publisher-terms_August-2025.pdf)) | La aprobación queda a criterio de Awin y de cada anunciante | Admite personas físicas mayores de 18 años. En España, los ingresos son una actividad económica: **[VERIFICAR]** con una gestoría si hace falta el alta censal o de autónomo desde el primer euro |
| Holaluz, Octopus, Plenitude y otras | **No he encontrado programas de afiliación públicos.** Lo que hay son «planes amigo» para clientes ([resumen](https://www.patillero.es/plan-amigo-luz/)), que no son para webs y suelen prohibir el uso comercial | — | — |
| Comparadores (Selectra, Kelisto, Rastreator, Papernest) | **No he encontrado programas públicos para afiliados** | — | Habría que contactarlos directamente |

**Recomendación:** a lo sumo 1-2 comercializadoras, y solo dentro de una herramienta neutral (apartado 5, «Tu factura»), con el aviso visible. Si los resultados dependen de quién paga, la web pierde su mayor valor, que es la confianza.

### 4.2 Contactos de placas, aerotermia y puntos de recarga

- **SotySolar** tiene programa de partners ([web](https://sotysolar.es/partners)) y un plan de referidos (SumaSolar), pero **no publica importes ni condiciones para webs.** Hay que pedirlas.
- **No he encontrado plataformas con pago por contacto y condiciones públicas** para aerotermia ni puntos de recarga. Las plataformas tipo marketplace (de presupuestos) cobran a los profesionales, no pagan a las webs.
- **Recomendación:** pedir condiciones por escrito a 2-3 empresas. Para la zona de Calatayud y Zaragoza, la opción más limpia es el instalador local (4.5).

### 4.3 Amazon Afiliados

- **Comisiones del programa** ([tabla oficial](https://afiliados.amazon.es/help/node/topic/GRXPHT8U84RAYDXZ)):
  - **3 %:** categorías «resto», donde caen la mayoría de medidores de consumo y enchufes inteligentes **[VERIFICAR]** la categoría exacta de cada producto.
  - **2,5 %:** grandes electrodomésticos y electrónica móvil.
  - **5 %:** hogar y cocina.
- **Requisitos:**
  - **3 ventas en los primeros 180 días**, o cierran la cuenta (fuentes secundarias; figura en el acuerdo operativo **[VERIFICAR]** al darse de alta).
  - Web pública con contenido original.
- **Encaje:** medidor de consumo por enchufe (para «Consumo fantasma» y la calculadora), enchufes inteligentes con medición, termómetro e higrómetro (deshumidificador), regletas con interruptor y cargador portátil para el coche.
- **Riesgo:** la política de *thin affiliation* de Google penaliza copiar fichas del comercio sin contenido propio. Solo enlaces dentro de artículos que ya aportan (mediciones y cálculos) y **nunca páginas «los 10 mejores» sin haber probado los productos.**

### 4.4 Servicios de pago propios

| Servicio | Qué sería | Precio orientativo | Cobro | Trabajo |
|---|---|---|---|---|
| Revisión de la factura | La persona sube 1-2 facturas y recibe un PDF con errores, potencia recomendada, tarifa y ahorro calculado | 15-29 € | Pasarela (Stripe o PayPal) con enlace de pago | 30-45 min por caso |
| Informe de ahorro de la casa | Factura + cuestionario + CSV de consumo horario (Datadis) → informe de 8-10 páginas con aparatos, horarios, potencia, placas (PVGIS) y prioridades | 39-59 € | Igual | 1,5-2 h por caso |
| Guía descargable | PDF «Paga menos luz en 30 días», con plantillas | 7-12 € | Venta digital | Una vez y luego actualizar |

**Requisitos legales y fiscales en España.** Es información general, no asesoramiento: **conviene una gestoría antes de cobrar el primer euro.**
- **Alta en Hacienda** (declaración censal, modelo 036/037, con epígrafe de actividad) y **alta de autónomo (RETA)** si la actividad es habitual.
  - 2026: **tarifa plana de 80 €/mes** el primer año, y luego cuota por tramos de rendimientos, de unos 200 a 590 €/mes ([Infoautónomos](https://www.infoautonomos.com/seguridad-social/tarifa-plana-autonomos/); **[VERIFICAR]** en Import@ss).
- **Facturas e IVA:**
  - Factura con IVA del 21 % en servicios a particulares en España.
  - La guía en PDF podría tener otro tipo (libro electrónico) **[VERIFICAR]** con la gestoría.
  - **VeriFactu:** los programas de facturación tienen que estar adaptados antes del **1-7-2027** para autónomos (y del 1-1-2027 para sociedades), según el [Real Decreto-ley 15/2025, BOE de 3-12-2025](https://sede.agenciatributaria.gob.es/Sede/en_gb/todas-noticias/2025/diciembre/3/ampliacion-plazo-adaptacion-sistemas-informaticos-facturacion.html). Conviene usar desde el principio un programa que ya cumpla.
- **Protección de datos (RGPD y LOPDGDD):** las facturas llevan nombre, dirección y CUPS.
  - Hacen falta consentimiento y política de privacidad específicos, plazo de borrado (por ejemplo, 30 días tras entregar el informe), almacenamiento seguro y registro de actividades de tratamiento.
  - Nunca se piden los datos por el formulario general de contacto.
- **Consumidores:** condiciones de venta, precio final con IVA y derecho de desistimiento. En los contenidos digitales se pierde si el cliente acepta la entrega inmediata **[VERIFICAR]** el texto con la gestoría o un abogado.
- **Aviso legal (LSSI):** datos del titular, NIF y contacto. Ya hay aviso legal: hay que ampliarlo.

### 4.5 Instalador eléctrico local (Calatayud y Zaragoza)

- **Página «Instalación eléctrica en Calatayud y Zaragoza»** con:
  - el nombre del instalador y su número de empresa instaladora habilitada (comprobarlo en el registro de industria de Aragón),
  - qué hace (boletines, cuadros, puntos de recarga, placas),
  - zona y plazos.
- **Aviso visible arriba:** «Tu luz en casa no es una empresa instaladora. Esta página es una colaboración comercial con [empresa], que hace los trabajos y los factura. Podemos recibir una compensación por cada contacto.» Las comunicaciones comerciales tienen que ser identificables como tales (LSSI, artículo 20).
- **Formulario:**
  - Casilla de consentimiento para ceder los datos a esa empresa, con su nombre, la finalidad y el plazo.
  - Envío directo al instalador y sin guardar los datos en la web.
  - Contrato escrito con el instalador: importe por contacto o comisión, protección de datos y quién es el responsable.
- **Coherente con CLAUDE.md:** la web nunca dice que el autor es electricista. Los artículos siguen diciendo qué puede hacer el usuario y qué tiene que hacer un instalador autorizado; la página de servicios es lo único comercial.
- **Ingresos:** facturar al instalador implica el alta del 4.4.

---

## 5. Herramientas nuevas

| Herramienta | Utilidad | Dificultad | Monetización | Datos |
|---|---|---|---|---|
| **Precio de la luz hoy por horas** | Muy alta, uso diario | Media (token, tarea programada, caché) | AdSense (visitas repetidas) | ESIOS (apartado 3) |
| **Calculadora de placas solares** | Alta | Media: PVGIS no se puede llamar desde el navegador (no envía la cabecera CORS, comprobado), así que se precalcula por provincia o se pasa por un endpoint del servidor | Contactos de placas o instalador local | PVGIS + calculadora de consumo |
| **Coste de cargar el coche** | Alta | Baja (extensión de la calculadora de consumo) | Amazon (cargadores) e instalador (puntos de recarga) | Mismos precios y tarifas |
| **Tu factura: ¿qué tarifa te conviene?** (con el CSV de Datadis) | Muy alta y original: analiza tu consumo real hora a hora **en el navegador**, sin subir datos | Media-alta (cada distribuidora da un CSV distinto) | Servicio de revisión de pago y, con cuidado, afiliación | CSV del usuario + tarifas de referencia |
| **Simulador del bono social** | Alta en invierno | Media: requisitos de renta e IPREM **[VERIFICAR]** la normativa vigente cada año | Solo AdSense (tema sensible: nada de afiliación) | BOE |
| Comparador de ofertas comerciales | Media | Alta | Afiliación | **No hay API pública verificada** de la CNMC: se enlaza a su comparador oficial en lugar de copiarlo |

**Las que más enlaces atraen:**
- «Tu factura» con el CSV, porque nadie analiza el consumo real sin pedir datos.
- Placas por provincia con PVGIS.
- El precio de la luz hoy, si es más claro y rápido que los de la competencia.

---

## 6. Por dónde empezar

### Este mes (antes de que AdSense apruebe)
1. **No monetizar todavía:** sin afiliación ni servicios. AdSense revisa la calidad y la confianza.
2. Tandas 1 y 2 de artículos, y crear la categoría «Trámites» en cuanto tenga 2 entradas publicadas.
3. **Precio de la luz hoy:**
   - Tú pides hoy mismo el token a `consultasios@ree.es` y preguntas las condiciones de uso.
   - Yo pruebo desde EasyWP que REData y ESIOS responden.
   - Prototipo sin publicar.
4. Comunidades, tanda A (Andalucía, Cataluña, Madrid, C. Valenciana), con la plantilla y la regla de los 5 datos propios.
5. Página «Metodología» (cómo calculamos y qué fuentes usamos) enlazada en el pie: refuerza la confianza para AdSense.

### En 3 meses
1. Tandas 3 a 5 y comunidades B y C.
2. «Precio de la luz hoy» publicada, y «Actualidad» funcionando (1-2 noticias por semana, revisadas por ti).
3. Calculadoras de coche y de placas (PVGIS por provincia).
4. **Si AdSense ha aprobado:**
   - Amazon Afiliados en 5-8 artículos con producto real.
   - Solicitud a Awin para niba.
   - Aviso de afiliación en cada artículo con enlaces y en una página «Cómo nos financiamos».

### En 6 meses
1. Tandas 6 a 8 y todas las comunidades.
2. Herramienta «Tu factura» (CSV de Datadis).
3. **Decisión sobre ingresos propios:** con la gestoría, alta y servicio piloto de revisión de factura a precio de lanzamiento. Página del instalador local si hay acuerdo firmado.
4. Revisar con Search Console qué funciona y reordenar las tandas siguientes.

### Qué depende de que AdSense apruebe
- **Todo lo comercial:** afiliación, Amazon, servicios e instalador. Mejor después, para que la revisión vea una web informativa limpia.
- La colocación definitiva de anuncios en la página del precio de la luz y en las calculadoras, sin que tapen la herramienta.

### Qué puede perjudicar la revisión o la confianza (y cómo se evita)
| Riesgo | Cómo se evita |
|---|---|
| Páginas de comunidad casi iguales (páginas puerta) | 5 datos propios mínimos y 4 por tanda |
| Una página por día del precio de la luz (contenido escalado) | Una sola URL |
| Enlaces de afiliado sin avisar | Aviso visible y `rel="sponsored"` en todos |
| Recomendar la tarifa que paga comisión | Herramientas neutrales; la afiliación nunca ordena los resultados |
| Noticias copiadas de medios | Solo fuentes oficiales, con una cifra o un «qué hacer» propio |
| Ayudas caducadas o importes inventados | Solo convocatorias verificadas, con la fecha de revisión |
| Datos personales de facturas | Análisis en el navegador; si es servicio de pago, RGPD completo y borrado |

---

## 7. Lo que no he podido verificar
1. Las condiciones de uso y reutilización de los datos de ESIOS y REData: sus webs bloquean a los programas.
2. Si el indicador 1001 del PVPC sigue siendo horario tras el paso del mercado a 15 minutos.
3. La hora exacta a la que se publica el PVPC del día siguiente.
4. El IPSI de la electricidad en Ceuta y en Melilla, y si allí hay bonificación del impuesto eléctrico: solo hay fuentes secundarias.
5. El reparto exacto de distribuidoras por provincia: los datos son de fuentes secundarias.
6. Las ayudas autonómicas al autoconsumo vigentes: hay información contradictoria.
7. Los programas de afiliación de comercializadoras distintas de niba, y los de comparadores y plataformas de contactos.
8. Las cuotas de autónomo de 2026 y el tipo de IVA de una guía en PDF: hay que confirmarlos con la Seguridad Social y una gestoría.
9. Los volúmenes de búsqueda (no tengo acceso a herramientas de palabras clave).

## Fuentes principales (consultadas el 7-10-2026)
- [Google Search Central, políticas de spam](https://developers.google.com/search/docs/essentials/spam-policies)
- [REE, API REData](https://www.ree.es/es/apidatos) · [ESIOS, token](https://www.esios.ree.es/es/token) · [API de ESIOS](https://api.esios.ree.es/)
- [PVGIS 5.3, JRC](https://re.jrc.ec.europa.eu/api/v5_3/PVcalc) (llamadas en `estrategia/pvgis_ccaa.py`)
- [INE, tabla 2853](https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/2853)
- [BOE, API de datos abiertos](https://www.boe.es/datosabiertos/api/boe/sumario/20261006)
- [Amazon Afiliados, comisiones](https://afiliados.amazon.es/help/node/topic/GRXPHT8U84RAYDXZ)
- [Awin: perfil de niba](https://ui.awin.com/merchant-profile/118409) · [Awin: depósito de alta](https://www.awin.com/gb/compliance-and-regulations/application-process-and-joining-fee) · [Awin: condiciones de agosto de 2025](https://www.awin.com/docs.awin.com/Legal/Publisher+Terms/2025/ES_Awin-AG-Publisher-terms_August-2025.pdf)
- [AEAT, aplazamiento de VeriFactu (RDL 15/2025)](https://sede.agenciatributaria.gob.es/Sede/en_gb/todas-noticias/2025/diciembre/3/ampliacion-plazo-adaptacion-sistemas-informaticos-facturacion.html)
- [MIVAU, prórroga de las deducciones por eficiencia energética](https://www.mivau.gob.es/el-ministerio/sala-de-prensa/noticias/lun-23122024-1223) · [RDL 7/2026, art. 36 (BOE consolidado)](https://www.boe.es/buscar/act.php?id=BOE-A-2026-6544) · corrección del 7/10/2026: el RDL 16/2025 fue derogado (Resolución del Congreso de 27/1/2026, BOE-A-2026-2024) · [RDL 16/2025 (resumen del COAAT Madrid, ya no vigente)](https://oficinarehabilitacionaparejadores.es/-/publicado-el-real-decreto-ley-16/2025-de-23-de-diciembre-por-el-que-se-prorrogan-las-deducciones-fiscales-en-el-irpf-por-obras-de-mejora-energ%C3%A9tica-en-viviendas)
- [SotySolar, partners](https://sotysolar.es/partners) · [Selectra](https://selectra.es/energia) · [Tarifaluzhora](https://tarifaluzhora.es/)
- Secundarias (marcadas **[VERIFICAR]**): Infoautónomos (cuotas), Autosolar (mercado de 15 minutos), comparadorluz.com (IGIC) y otras citadas en el texto.
