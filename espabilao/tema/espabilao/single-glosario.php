<?php
/**
 * Término del glosario.
 *
 * @package Espabilao
 */

get_header();

while ( have_posts() ) :
	the_post();
	?>
	<article <?php post_class( 'articulo articulo--glosario' ); ?>>
		<div class="envoltorio envoltorio--texto">
			<?php espabilao_migas(); ?>
			<header class="articulo__cabecera">
				<p class="antetitulo">Glosario</p>
				<?php the_title( '<h1 class="articulo__titulo">', '</h1>' ); ?>
			</header>
			<div class="contenido"><?php the_content(); ?></div>
			<p><a class="enlace-flecha" href="<?php echo esc_url( (string) get_post_type_archive_link( 'glosario' ) ); ?>"><span aria-hidden="true">←</span> Todo el glosario</a></p>
		</div>
	</article>
	<?php
endwhile;

get_footer();
