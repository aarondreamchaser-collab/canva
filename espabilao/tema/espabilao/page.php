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
		<div class="envoltorio envoltorio--texto">
			<header class="articulo__cabecera">
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
