<?php
/**
 * Página no encontrada (con humor).
 *
 * @package Espabilao
 */

get_header();
?>

<div class="envoltorio">
	<section class="error404__caja">
		<div class="error404__expediente">
			<p class="expediente__pestana">Siniestro n.º 404</p>
			<p class="etiqueta">Resolución del expediente</p>
			<h1 class="error404__titulo">Lo sentimos: esta página no está cubierta.</h1>
			<p class="error404__texto">Hemos revisado las condiciones generales, las particulares y hasta la letra pequeña de la letra pequeña. La página que buscas no existe, se mudó sin avisar o alguien escribió mal la dirección.</p>
			<p class="error404__clausula"><span class="etiqueta">Cláusula aplicable</span> Art. 404 de nuestras condiciones: «Quedan excluidos los enlaces rotos, las direcciones mal tecleadas y las páginas que cambiaron de domicilio sin comunicarlo en el plazo de 7 días».</p>
			<span class="sello sello--no-pago sello--grande error404__sello">No cubierto</span>
		</div>
		<div class="error404__salidas">
			<p class="etiqueta">Pero tranquilo, aquí no hay franquicia</p>
			<p>Para esto no hace falta reclamar por escrito. Busca lo que necesitas:</p>
			<?php get_search_form(); ?>
			<p class="etiqueta error404__o">O entra por una sección</p>
			<?php espabilao_menu_defecto(); ?>
		</div>
	</section>
</div>

<?php
get_footer();
