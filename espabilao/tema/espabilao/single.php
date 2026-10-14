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
	$esp_autor     = (int) get_the_author_meta( 'ID' );
	$esp_respuesta = get_post_meta( $esp_id, '_esp_respuesta', true );
	$esp_fuentes   = espabilao_fuentes( $esp_id );

	ob_start();
	the_content();
	$esp_html = ob_get_clean();

	$esp_indice = array();
	if ( espabilao_opcion( 'mostrar_indice' ) ) {
		list( $esp_html, $esp_indice ) = espabilao_indice( $esp_html );
	}
	$esp_hay_indice = count( $esp_indice ) >= 3;

	ob_start();
	if ( $esp_hay_indice ) :
		?>
		<ol>
			<?php foreach ( $esp_indice as $esp_item ) : ?>
				<li><a href="#<?php echo esc_attr( $esp_item[0] ); ?>"><?php echo esc_html( $esp_item[1] ); ?></a></li>
			<?php endforeach; ?>
		</ol>
		<?php
	endif;
	$esp_lista_indice = ob_get_clean();
	?>

	<article <?php post_class( 'articulo' ); ?>>
		<header class="articulo__cabecera">
			<div class="envoltorio envoltorio--medio">
				<?php espabilao_migas(); ?>
				<?php espabilao_antetitulo( $esp_id, true ); ?>
				<?php the_title( '<h1 class="articulo__titulo">', '</h1>' ); ?>
				<?php if ( has_excerpt() ) : ?>
					<p class="articulo__entradilla"><?php echo esc_html( get_the_excerpt() ); ?></p>
				<?php endif; ?>
				<div class="articulo__meta">
					<span class="articulo__autor">
						<?php echo get_avatar( $esp_autor, 40, '', '', array( 'loading' => 'lazy' ) ); ?>
						<span>Por <a href="<?php echo esc_url( get_author_posts_url( $esp_autor ) ); ?>"><?php the_author(); ?></a></span>
					</span>
					<?php espabilao_revisado( $esp_id, 'j \d\e F \d\e Y' ); ?>
					<span class="revisado"><?php echo espabilao_icono( 'libro', 14 ); // phpcs:ignore ?> <?php echo esc_html( espabilao_minutos_lectura( $esp_id ) ); ?> min de lectura</span>
				</div>
				<?php if ( get_post_meta( $esp_id, '_esp_veredicto', true ) ) : ?>
					<div class="articulo__veredicto">
						<span class="articulo__veredicto-texto">Veredicto</span>
						<?php echo espabilao_sello( $esp_id, 'veredicto--grande' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
					</div>
				<?php endif; ?>
			</div>
		</header>

		<div class="envoltorio envoltorio--medio articulo__rejilla">
			<div class="articulo__principal">
				<?php if ( has_post_thumbnail() ) : ?>
					<figure class="articulo__imagen"><?php the_post_thumbnail( 'large', array( 'loading' => 'eager', 'fetchpriority' => 'high' ) ); ?></figure>
				<?php endif; ?>

				<?php if ( $esp_respuesta ) : ?>
					<aside class="respuesta" aria-label="Respuesta rápida">
						<p class="respuesta__titulo"><?php echo espabilao_icono( 'bombilla', 20 ); // phpcs:ignore ?> Respuesta rápida</p>
						<div class="respuesta__texto"><?php echo wp_kses_post( wpautop( esc_html( $esp_respuesta ) ) ); ?></div>
					</aside>
				<?php endif; ?>

				<?php if ( $esp_hay_indice ) : ?>
					<nav class="indice indice--movil" aria-label="Índice del artículo">
						<details>
							<summary>En este artículo <span class="indice__n" aria-hidden="true">· <?php echo esc_html( count( $esp_indice ) ); ?> apartados</span></summary>
							<?php echo $esp_lista_indice; // phpcs:ignore WordPress.Security.EscapeOutput ?>
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
						<h2 id="t-fuentes" class="fuentes__titulo"><?php echo espabilao_icono( 'libro', 20 ); // phpcs:ignore ?> Fuentes</h2>
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
					<?php echo espabilao_icono( 'alerta', 22 ); // phpcs:ignore ?>
					<p><strong>Aviso.</strong> <?php echo esc_html( espabilao_opcion( 'aviso_articulo' ) ); ?></p>
				</aside>

				<?php echo espabilao_anuncio( 'final' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>

				<?php get_template_part( 'template-parts/autor' ); ?>
			</div>

			<div class="articulo__lateral">
				<?php if ( $esp_hay_indice ) : ?>
					<nav class="indice indice--lateral" aria-label="Índice del artículo (lateral)">
						<p class="supra">En este artículo</p>
						<?php echo $esp_lista_indice; // phpcs:ignore WordPress.Security.EscapeOutput ?>
					</nav>
				<?php endif; ?>
				<?php $esp_guias = get_term_by( 'slug', 'que-hacer-si', 'seccion' ); ?>
				<div class="caja caja--oscura">
					<p class="caja__titulo">¿Te han dicho que no?</p>
					<p>Pide el rechazo por escrito y reclama: tienen 1 mes para responderte.</p>
					<?php if ( $esp_guias ) : ?>
						<a class="enlace-mas" href="<?php echo esc_url( get_term_link( $esp_guias ) ); ?>">Cómo reclamar <?php echo espabilao_icono( 'flecha', 16 ); // phpcs:ignore ?></a>
					<?php endif; ?>
				</div>
			</div>
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
				<?php espabilao_titulo_bloque( 't-rel', 'Sigue leyendo', $esp_tipo ? 'Más sobre seguros de ' . mb_strtolower( $esp_tipo->name ) : 'Más artículos' ); ?>
				<div class="tarjetas">
					<?php
					foreach ( $esp_rel as $esp_p ) {
						espabilao_tarjeta( $esp_p );
					}
					?>
				</div>
			</div>
		</section>
	<?php endif; ?>

	<?php
endwhile;

get_footer();
