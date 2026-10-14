<?php
/**
 * Artículo.
 *
 * @package Espabilao
 */

get_header();

while ( have_posts() ) :
	the_post();
	$esp_id        = get_the_ID();
	$esp_respuesta = get_post_meta( $esp_id, '_esp_respuesta', true );
	$esp_fuentes   = espabilao_fuentes( $esp_id );

	ob_start();
	the_content();
	$esp_html = ob_get_clean();

	$esp_indice = array();
	if ( espabilao_opcion( 'mostrar_indice' ) ) {
		list( $esp_html, $esp_indice ) = espabilao_indice( $esp_html );
	}
	?>

	<article <?php post_class( 'articulo' ); ?>>
		<div class="envoltorio envoltorio--texto">
			<?php espabilao_migas(); ?>

			<header class="articulo__cabecera">
				<?php espabilao_antetitulo( $esp_id, true ); ?>
				<?php the_title( '<h1 class="articulo__titulo">', '</h1>' ); ?>
				<?php if ( has_excerpt() ) : ?>
					<p class="articulo__entradilla"><?php echo esc_html( get_the_excerpt() ); ?></p>
				<?php endif; ?>
				<div class="articulo__meta">
					<span class="articulo__autor">Por <a href="<?php echo esc_url( get_author_posts_url( (int) get_the_author_meta( 'ID' ) ) ); ?>"><?php the_author(); ?></a></span>
					<?php espabilao_revisado( $esp_id, 'j \d\e F \d\e Y' ); ?>
					<span><?php echo esc_html( espabilao_minutos_lectura( $esp_id ) ); ?> min de lectura</span>
				</div>
				<?php echo espabilao_sello( $esp_id, 'sello--grande articulo__sello' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			</header>

			<?php if ( has_post_thumbnail() ) : ?>
				<figure class="articulo__imagen"><?php the_post_thumbnail( 'large', array( 'loading' => 'eager', 'fetchpriority' => 'high' ) ); ?></figure>
			<?php endif; ?>

			<?php if ( $esp_respuesta ) : ?>
				<aside class="respuesta" aria-label="Respuesta rápida">
					<p class="etiqueta">Respuesta rápida</p>
					<div class="respuesta__texto"><?php echo wp_kses_post( wpautop( esc_html( $esp_respuesta ) ) ); ?></div>
				</aside>
			<?php endif; ?>

			<?php if ( count( $esp_indice ) >= 3 ) : ?>
				<nav class="indice" aria-label="Índice del artículo">
					<details open>
						<summary class="etiqueta">En este artículo</summary>
						<ol>
							<?php foreach ( $esp_indice as $esp_item ) : ?>
								<li><a href="#<?php echo esc_attr( $esp_item[0] ); ?>"><?php echo esc_html( $esp_item[1] ); ?></a></li>
							<?php endforeach; ?>
						</ol>
					</details>
				</nav>
			<?php endif; ?>

			<div class="contenido">
				<?php echo $esp_html; // phpcs:ignore WordPress.Security.EscapeOutput ?>
				<?php
				if ( espabilao_necesita_escalera( $esp_id ) ) {
					echo espabilao_sc_escalera(); // phpcs:ignore WordPress.Security.EscapeOutput
				}
				?>
			</div>

			<?php the_tags( '<ul class="etiquetas" aria-label="Etiquetas"><li>', '</li><li>', '</li></ul>' ); ?>

			<?php if ( $esp_fuentes ) : ?>
				<section class="fuentes" aria-labelledby="t-fuentes">
					<h2 id="t-fuentes" class="fuentes__titulo">Fuentes</h2>
					<ol>
						<?php foreach ( $esp_fuentes as $esp_f ) : ?>
							<li>
								<?php if ( $esp_f[1] ) : ?>
									<a href="<?php echo esc_url( $esp_f[1] ); ?>" target="_blank" rel="noopener"><?php echo esc_html( $esp_f[0] ); ?></a>
								<?php else : ?>
									<?php echo esc_html( $esp_f[0] ); ?>
								<?php endif; ?>
							</li>
						<?php endforeach; ?>
					</ol>
				</section>
			<?php endif; ?>

			<aside class="aviso" role="note">
				<p class="etiqueta">Aviso</p>
				<p><?php echo esc_html( espabilao_opcion( 'aviso_articulo' ) ); ?></p>
			</aside>

			<?php echo espabilao_anuncio( 'final' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>

			<?php get_template_part( 'template-parts/autor' ); ?>
		</div>
	</article>

	<?php
	$esp_tipo = espabilao_tipo_de( $esp_id );
	$esp_rel  = get_posts( array(
		'numberposts'  => 3,
		'post__not_in' => array( $esp_id ),
		'cat'          => $esp_tipo ? $esp_tipo->term_id : 0,
	) );
	if ( $esp_rel ) :
		?>
		<section class="relacionados" aria-labelledby="t-rel">
			<div class="envoltorio">
				<header class="bloque__cabecera"><h2 class="bloque__titulo" id="t-rel"><span class="etiqueta">Sigue leyendo</span> <?php echo $esp_tipo ? esc_html( 'Más sobre seguros de ' . mb_strtolower( $esp_tipo->name ) ) : 'Más artículos'; ?></h2></header>
				<div class="casos">
					<?php
					foreach ( $esp_rel as $esp_p ) {
						espabilao_tarjeta_caso( $esp_p );
					}
					?>
				</div>
			</div>
		</section>
	<?php endif; ?>

	<?php
endwhile;

get_footer();
