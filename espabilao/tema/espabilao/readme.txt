=== Espabilao ===
Contributors: espabilao
Requires at least: 6.3
Tested up to: 7.1
Requires PHP: 7.4
Stable tag: 3.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Tema propio de Espabilao (espabilao.com): información independiente sobre seguros en España.

== Descripción ==

Diseño «Alerta naranja»: blanco, tinta y naranja, iconos por tipo de seguro, semáforo de veredictos y marcador de casos. Sin jQuery ni constructores, móvil primero y en español. No genera schema ni JSON-LD (lo hace Rank Math) y no incluye aviso de cookies (usa «Privacidad y mensajes» de AdSense).

= Al activarlo =
Crea, si no existen, las secciones (¿Pagó o no pagó?, Pólizas al desnudo, Qué hacer si…, Trucos de espabilao), las categorías de tipo de seguro (hogar, coche, moto, salud, vida, decesos, mascotas, viaje, alquiler, autónomos) y 18 términos básicos del glosario. No borra ni cambia nada existente.

= Ficha de cada artículo =
En el editor, caja «Ficha Espabilao»: respuesta rápida, veredicto (Pagó / No pagó / A medias), fecha de revisión y fuentes (una por línea: «Nombre | https://enlace»). El cargo del autor se edita en Usuarios > Perfil; la biografía en «Información biográfica».

= Bloques propios =
En el insertador de bloques > Patrones > Espabilao:
* Escalera de reclamación (también con el shortcode [escalera_reclamacion]). Se añade sola al final de los artículos de «¿Pagó o no pagó?» y «Qué hacer si…» si no la has puesto tú (se puede desactivar).
* Plazos que te protegen: [plazos articulos="16,38,18,20,22"]. Artículos disponibles: 10, 15, 16, 18, 20, 22 y 38 de la Ley de Contrato de Seguro, cada uno enlazado al BOE.
* Plantilla de carta, con botón «Copiar carta» y la nota «Modelo orientativo, adáptalo a tu caso».
* Dónde dice eso en tu póliza.
* Estructura de un caso.

= Herramientas (nuevo en 3.0) =
Al activar o actualizar el tema se crea la página «Herramientas» con cuatro páginas hijas (no se duplican si ya existen):
* Calculadora de plazos [calculadora_plazos]: siniestro, reclamación o renovación; exporta los plazos a tu calendario (.ics).
* Generador de cartas [generador_carta]: reclamación, petición del rechazo por escrito, oposición a la renovación e intereses de demora.
* Detector de letra pequeña [detector_letra_pequena]: marca exclusiones, límites, franquicias y términos del glosario.
* Calculadora de infraseguro [calculadora_infraseguro]: regla proporcional del art. 30 LCS.
Todo funciona en el navegador del lector: no se envía ni se guarda ningún dato. Puedes usar los shortcodes en cualquier entrada.

= Ficha del caso (nuevo en 3.0) =
En la «Ficha Espabilao»: importe reclamado, importe obtenido, cuánto tardó y dónde se resolvió. Se muestra arriba del caso.

= Glosario =
Menú Glosario en el escritorio. La primera aparición de cada término en un artículo se marca y muestra la definición al pulsarla. Archivo en /glosario/.

= Publicidad =
Apariencia > Personalizar > Espabilao > Publicidad: ID de editor (ca-pub-…) y los ID de bloque para: tras el párrafo N, final del artículo, portada y listados.

= Nota =
La sección, el glosario y los bloques viven en el tema: si algún día cambias de tema, el contenido sigue en la base de datos, pero dejará de mostrarse hasta volver a activar este tema o pasarlo a un plugin.

== Licencias ==
Código: GPLv2 o posterior.
Fuentes: Bricolage Grotesque y Figtree, SIL Open Font License 1.1 (assets/fonts/OFL-*.txt).

== Registro de cambios ==
= 3.0.0 =
* Megamenú «Seguros» con los diez tipos y acceso a las herramientas.
* Portada de cada tipo de seguro: datos, marcador de veredictos, contenidos por sección, herramientas útiles y listado completo.
* Cuatro herramientas gratuitas que funcionan en el navegador.
* Ficha del caso, barra de progreso de lectura, botón «Escuchar», compartir e imprimir.
* Portada reorganizada: herramientas, preguntas frecuentes y glosario.
* Pie con mapa del sitio.

= 2.0.0 =
* Rediseño completo «Alerta naranja»: cabecera con menú móvil y buscador desplegable, iconos por tipo de seguro, marcador de veredictos, banda «Así se reclama», índice lateral fijo en los artículos y palabra del día del glosario.
* Escalera de reclamación actualizada a la Ley 10/2025 (1 mes para responder; arts. 29 bis y 30 de la Ley 44/2002).

= 1.0.0 =
* Primera versión.
