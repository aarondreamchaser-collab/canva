<?php
/**
 * Página estática.
 *
 * @package Espabilao
 */

get_header();

while ( have_posts() ) :
	the_post();
	?>
	<article <?php post_class( 'articulo articulo--pagina' ); ?>>
		<div class="envoltorio <?php echo espabilao_es_herramienta() ? 'envoltorio--medio' : 'envoltorio--texto'; ?>">
			<?php if ( espabilao_es_herramienta() ) : ?>
				<?php espabilao_migas(); ?>
			<?php endif; ?>
			<header class="articulo__cabecera articulo__cabecera--simple">
				<?php if ( espabilao_es_herramienta() ) : ?>
					<p class="antetitulo"><span class="pildora pildora--seccion"><?php echo espabilao_icono( 'chispa', 14 ); // phpcs:ignore ?> Herramienta gratuita</span></p>
				<?php endif; ?>
				<?php the_title( '<h1 class="articulo__titulo">', '</h1>' ); ?>
			</header>
			<?php if ( has_post_thumbnail() ) : ?>
				<figure class="articulo__imagen"><?php the_post_thumbnail( 'large' ); ?></figure>
			<?php endif; ?>
			<div class="contenido">
				<?php
				the_content();
				wp_link_pages();
				?>
			</div>
		</div>
	</article>
	<?php
endwhile;

get_footer();
