=== Espabilao ===
Contributors: espabilao
Requires at least: 6.3
Tested up to: 7.1
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Tema propio de Espabilao (espabilao.com): información independiente sobre seguros en España.

== Descripción ==

Dirección de diseño «Expediente»: papel, tinta y sellos de veredicto. Sin jQuery ni constructores, móvil primero y en español. No genera schema ni JSON-LD (lo hace Rank Math) y no incluye aviso de cookies (usa «Privacidad y mensajes» de AdSense).

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

= Glosario =
Menú Glosario en el escritorio. La primera aparición de cada término en un artículo se marca y muestra la definición al pulsarla. Archivo en /glosario/.

= Publicidad =
Apariencia > Personalizar > Espabilao > Publicidad: ID de editor (ca-pub-…) y los ID de bloque para: tras el párrafo N, final del artículo, portada y listados.

= Nota =
La sección, el glosario y los bloques viven en el tema: si algún día cambias de tema, el contenido sigue en la base de datos, pero dejará de mostrarse hasta volver a activar este tema o pasarlo a un plugin.

== Licencias ==
Código: GPLv2 o posterior.
Fuentes: Fraunces, Source Serif 4 e IBM Plex Mono, SIL Open Font License 1.1 (assets/fonts/OFL-*.txt).

== Registro de cambios ==
= 1.0.0 =
* Primera versión.
