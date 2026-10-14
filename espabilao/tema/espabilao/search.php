<?php
/**
 * Resultados de búsqueda.
 *
 * @package Espabilao
 */

get_header();
global $wp_query;
?>

<div class="envoltorio">
	<header class="archivo__cabecera">
		<p class="etiqueta">Búsqueda</p>
		<h1 class="archivo__titulo">
			<?php if ( get_search_query() ) : ?>
				«<?php echo esc_html( get_search_query() ); ?>»
			<?php else : ?>
				¿Qué te preocupa de tu seguro?
			<?php endif; ?>
		</h1>
		<?php if ( get_search_query() ) : ?>
			<p class="archivo__desc"><?php echo esc_html( sprintf( _n( '%d resultado', '%d resultados', (int) $wp_query->found_posts, 'espabilao' ), (int) $wp_query->found_posts ) ); ?></p>
		<?php endif; ?>
		<?php get_search_form(); ?>
	</header>

	<?php if ( have_posts() && get_search_query() ) : ?>
		<div class="lista lista--ancha">
			<?php
			$esp_i = 0;
			while ( have_posts() ) :
				the_post();
				if ( 'glosario' === get_post_type() ) :
					?>
					<article class="fila fila--glosario">
						<div class="fila__texto">
							<p class="antetitulo">Glosario</p>
							<h2 class="fila__titulo"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
							<p class="fila__resumen"><?php echo esc_html( wp_trim_words( get_the_excerpt(), 30 ) ); ?></p>
						</div>
					</article>
					<?php
				else :
					espabilao_fila( get_post(), 'h2' );
				endif;
				if ( 3 === ++$esp_i ) {
					echo espabilao_anuncio( 'archivo' ); // phpcs:ignore WordPress.Security.EscapeOutput
				}
			endwhile;
			espabilao_paginacion();
			?>
		</div>
	<?php elseif ( get_search_query() ) : ?>
		<div class="vacio">
			<p class="vacio__titulo">No hemos encontrado nada con esas palabras.</p>
			<p>Prueba con algo más corto («gotera», «franquicia», «baja») o entra por tipo de seguro:</p>
			<?php espabilao_tipos(); ?>
		</div>
	<?php else : ?>
		<?php espabilao_tipos(); ?>
	<?php endif; ?>
</div>

<?php
get_footer();
