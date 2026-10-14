<?php
/**
 * Portada.
 *
 * @package Espabilao
 */

get_header();

$esp_term_casos = get_term_by( 'slug', 'pago-o-no-pago', 'seccion' );
$esp_term_guias = get_term_by( 'slug', 'que-hacer-si', 'seccion' );
$esp_casos      = get_posts( array(
	'numberposts' => 4,
	'tax_query'   => array( array( 'taxonomy' => 'seccion', 'field' => 'slug', 'terms' => 'pago-o-no-pago' ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
) );
$esp_destacado  = $esp_casos ? array_shift( $esp_casos ) : null;
$esp_excluir    = wp_list_pluck( array_merge( $esp_destacado ? array( $esp_destacado ) : array(), $esp_casos ), 'ID' );
$esp_busquedas  = array_filter( array_map( 'trim', explode( ',', (string) espabilao_opcion( 'busquedas' ) ) ) );
$esp_marcador   = espabilao_marcador();
$esp_total      = array_sum( $esp_marcador );
$esp_tintes     = array( 'pago-o-no-pago' => 'naranja', 'polizas-al-desnudo' => 'lila', 'que-hacer-si' => 'menta', 'trucos-de-espabilao' => 'amarillo' );
?>

<section class="hero" aria-labelledby="hero-titulo">
	<div class="envoltorio hero__dentro">
		<div class="hero__texto">
			<p class="supra supra--naranja"><?php echo esc_html( espabilao_opcion( 'hero_etiqueta' ) ); ?></p>
			<h2 id="hero-titulo" class="hero__titulo"><?php echo esc_html( espabilao_opcion( 'hero_titulo' ) ); ?> <mark><?php echo esc_html( espabilao_opcion( 'hero_destacado' ) ); ?></mark></h2>
			<p class="hero__entradilla"><?php echo esc_html( espabilao_opcion( 'hero_texto' ) ); ?></p>
			<div class="hero__buscador"><?php get_search_form(); ?></div>
			<?php if ( $esp_busquedas ) : ?>
				<p class="sugerencias"><span>Lo más buscado:</span>
					<?php foreach ( $esp_busquedas as $esp_b ) : ?>
						<a href="<?php echo esc_url( home_url( '/?s=' . rawurlencode( $esp_b ) ) ); ?>"><?php echo esc_html( $esp_b ); ?></a>
					<?php endforeach; ?>
				</p>
			<?php endif; ?>
		</div>

		<?php if ( $esp_destacado ) : ?>
			<article class="caso-destacado">
				<p class="caso-destacado__supra">Caso de la semana</p>
				<?php echo espabilao_sello( $esp_destacado->ID, 'veredicto--grande' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
				<h3 class="caso-destacado__titulo"><a href="<?php echo esc_url( get_permalink( $esp_destacado ) ); ?>"><?php echo esc_html( get_the_title( $esp_destacado ) ); ?></a></h3>
				<p class="caso-destacado__resumen"><?php echo esc_html( get_the_excerpt( $esp_destacado ) ); ?></p>
				<a class="enlace-mas" href="<?php echo esc_url( get_permalink( $esp_destacado ) ); ?>">Ver cómo acabó <?php echo espabilao_icono( 'flecha', 18 ); // phpcs:ignore ?></a>
			</article>
		<?php endif; ?>
	</div>

	<div class="envoltorio">
		<ul class="garantias">
			<li><?php echo espabilao_icono( 'escudo', 26 ); // phpcs:ignore ?><span><strong>No vendemos seguros</strong> Ni comisiones, ni formularios, ni llamadas.</span></li>
			<li><?php echo espabilao_icono( 'libro', 26 ); // phpcs:ignore ?><span><strong>Con fuentes oficiales</strong> BOE, Ley de Contrato de Seguro y DGSFP.</span></li>
			<li><?php echo espabilao_icono( 'reloj', 26 ); // phpcs:ignore ?><span><strong>Revisado y fechado</strong> Cada artículo dice cuándo se comprobó.</span></li>
		</ul>
	</div>
</section>

<div class="envoltorio">

	<section class="bloque" aria-labelledby="t-tipos">
		<?php espabilao_titulo_bloque( 't-tipos', 'Empieza por aquí', '¿Qué seguro te preocupa?' ); ?>
		<?php espabilao_tipos(); ?>
	</section>

	<section class="bloque" aria-labelledby="t-secciones">
		<?php espabilao_titulo_bloque( 't-secciones', 'Cuatro formas de espabilar', 'Nuestras secciones' ); ?>
		<ul class="secciones">
			<?php
			foreach ( espabilao_secciones() as $esp_slug => $esp_s ) :
				$esp_t = get_term_by( 'slug', $esp_slug, 'seccion' );
				if ( ! $esp_t ) {
					continue;
				}
				?>
				<li class="seccion seccion--<?php echo esc_attr( $esp_tintes[ $esp_slug ] ); ?>">
					<a href="<?php echo esc_url( get_term_link( $esp_t ) ); ?>">
						<span class="seccion__icono"><?php echo espabilao_icono_seccion( $esp_slug ); // phpcs:ignore ?></span>
						<span class="seccion__nombre"><?php echo esc_html( $esp_t->name ); ?></span>
						<span class="seccion__texto"><?php echo esc_html( $esp_t->description ? $esp_t->description : $esp_s['descripcion'] ); ?></span>
						<span class="seccion__n"><?php echo esc_html( sprintf( _n( '%d artículo', '%d artículos', $esp_t->count, 'espabilao' ), $esp_t->count ) ); ?> <?php echo espabilao_icono( 'flecha', 16 ); // phpcs:ignore ?></span>
					</a>
				</li>
			<?php endforeach; ?>
		</ul>
	</section>

	<?php if ( $esp_casos || $esp_total ) : ?>
		<section class="bloque" aria-labelledby="t-casos">
			<?php espabilao_titulo_bloque( 't-casos', 'Casos reales', '¿Pagó o no pagó?', $esp_term_casos ? get_term_link( $esp_term_casos ) : '', 'Todos los casos' ); ?>
			<?php if ( $esp_total ) : ?>
				<div class="marcador" role="group" aria-label="Marcador de veredictos">
					<p class="marcador__titulo">Marcador de <?php echo esc_html( $esp_total ); ?> casos analizados</p>
					<div class="marcador__barra" aria-hidden="true">
						<?php foreach ( $esp_marcador as $esp_v => $esp_n ) : ?>
							<?php if ( $esp_n ) : ?>
								<span class="marcador__tramo marcador__tramo--<?php echo esc_attr( $esp_v ); ?>" style="flex-grow:<?php echo (int) $esp_n; ?>"></span>
							<?php endif; ?>
						<?php endforeach; ?>
					</div>
					<ul class="marcador__leyenda">
						<?php foreach ( $esp_marcador as $esp_v => $esp_n ) : ?>
							<li>
								<?php if ( $esp_term_casos ) : ?>
									<a href="<?php echo esc_url( add_query_arg( 'veredicto', $esp_v, get_term_link( $esp_term_casos ) ) ); ?>"><?php echo espabilao_veredicto_html( $esp_v, 'veredicto--mini' ); // phpcs:ignore ?> <strong><?php echo esc_html( $esp_n ); ?></strong></a>
								<?php endif; ?>
							</li>
						<?php endforeach; ?>
					</ul>
				</div>
			<?php endif; ?>
			<div class="tarjetas">
				<?php
				foreach ( $esp_casos as $esp_p ) {
					espabilao_tarjeta( $esp_p );
				}
				?>
			</div>
		</section>
	<?php endif; ?>

	<?php echo espabilao_anuncio( 'portada' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
</div>

<section class="banda-reclamar" aria-labelledby="t-reclamar">
	<div class="envoltorio banda-reclamar__dentro">
		<div class="banda-reclamar__texto">
			<p class="supra supra--naranja">Lo que las aseguradoras no te cuentan</p>
			<h2 id="t-reclamar" class="banda-reclamar__titulo">¿Te han dicho que no? Así se reclama.</h2>
			<p>Los comparadores te ayudan a contratar. Nosotros te ayudamos cuando llega el siniestro: plazos legales, cartas para copiar y a quién acudir si no te hacen caso.</p>
			<?php if ( $esp_term_guias ) : ?>
				<a class="boton boton--naranja" href="<?php echo esc_url( get_term_link( $esp_term_guias ) ); ?>">Ver las guías «Qué hacer si…» <?php echo espabilao_icono( 'flecha', 18 ); // phpcs:ignore ?></a>
			<?php endif; ?>
		</div>
		<ol class="mini-escalera">
			<li><span>1</span> Pide el «no» por escrito</li>
			<li><span>2</span> Reclama a su Servicio de Atención al Cliente <em>1 mes para responder</em></li>
			<li><span>3</span> Acude gratis a la DGSFP</li>
			<li><span>4</span> Juzgado: hasta 2.000 € sin abogado</li>
		</ol>
	</div>
</section>

<div class="envoltorio">
	<section class="bloque" aria-labelledby="t-ultimos">
		<?php espabilao_titulo_bloque( 't-ultimos', 'Recién revisado', 'Últimos artículos' ); ?>
		<div class="con-lateral">
			<div class="tarjetas tarjetas--dos">
				<?php
				$esp_ultimos = get_posts( array( 'numberposts' => 6, 'post__not_in' => $esp_excluir ) );
				foreach ( $esp_ultimos as $esp_p ) {
					espabilao_tarjeta( $esp_p );
				}
				if ( ! $esp_ultimos ) {
					echo '<p>Todavía no hay artículos publicados.</p>';
				}
				?>
			</div>
			<div class="lateral">
				<?php $esp_palabra = espabilao_palabra_del_dia(); ?>
				<?php if ( $esp_palabra ) : ?>
					<div class="caja caja--crema">
						<p class="supra">Palabra del día</p>
						<p class="caja__titulo"><?php echo esc_html( get_the_title( $esp_palabra ) ); ?></p>
						<p><?php echo esc_html( wp_trim_words( has_excerpt( $esp_palabra ) ? $esp_palabra->post_excerpt : wp_strip_all_tags( $esp_palabra->post_content ), 34 ) ); ?></p>
						<a class="enlace-mas" href="<?php echo esc_url( (string) get_post_type_archive_link( 'glosario' ) ); ?>">Todo el glosario <?php echo espabilao_icono( 'flecha', 16 ); // phpcs:ignore ?></a>
					</div>
				<?php endif; ?>
				<div class="caja caja--borde">
					<p class="supra">Nuestra regla</p>
					<p class="caja__titulo">Si una web de seguros te pide el teléfono, te quiere vender algo.</p>
					<p>Aquí no hay formularios: solo información con fuentes para que decidas tú.</p>
				</div>
			</div>
		</div>
	</section>
</div>

<?php
get_footer();
