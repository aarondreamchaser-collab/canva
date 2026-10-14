<?php
/**
 * Página no encontrada (con humor).
 *
 * @package Espabilao
 */

get_header();
?>

<div class="envoltorio">
	<section class="e404">
		<div class="e404__poliza">
			<p class="e404__numero" aria-hidden="true">404</p>
			<?php echo espabilao_veredicto_html( 'no-pago', 'veredicto--grande', 'No cubierto' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			<h1 class="e404__titulo">Lo sentimos: esta página no está cubierta por tu póliza.</h1>
			<p class="e404__texto">Hemos revisado las condiciones generales, las particulares y hasta la letra pequeña de la letra pequeña. La página que buscas no existe, se mudó sin avisar o alguien escribió mal la dirección.</p>
			<div class="e404__clausula">
				<p class="supra">Cláusula aplicable</p>
				<p>Art. 404: «Quedan excluidos los enlaces rotos, las direcciones mal tecleadas y las páginas que cambiaron de domicilio sin comunicarlo en el plazo de 7 días».</p>
			</div>
		</div>
		<div class="e404__salidas">
			<p class="supra supra--naranja">Buena noticia: aquí no hay franquicia</p>
			<p class="e404__subtitulo">Para esto no hace falta reclamar por escrito.</p>
			<?php get_search_form(); ?>
			<p class="supra e404__o">O entra por un tipo de seguro</p>
			<?php espabilao_tipos( 'lista' ); ?>
		</div>
	</section>
</div>

<?php
get_footer();
