<?php
/**
 * Portada de cada tipo de seguro (categoría): resumen, casos por veredicto,
 * contenidos agrupados por sección, herramientas útiles y listado completo.
 *
 * @package Espabilao
 */

get_header();

$esp_cat    = get_queried_object();
$esp_nombre = 'Seguro de ' . mb_strtolower( $esp_cat->name );
$esp_paged  = max( 1, (int) get_query_var( 'paged' ) );
$esp_desc   = wp_strip_all_tags( term_description( $esp_cat ) );
$esp_grupos = array();

if ( 1 === $esp_paged ) {
	foreach ( espabilao_secciones() as $esp_slug => $esp_s ) {
		$esp_t = get_term_by( 'slug', $esp_slug, 'seccion' );
		if ( ! $esp_t ) {
			continue;
		}
		$esp_q = new WP_Query( array(
			'posts_per_page'      => 3,
			'cat'                 => $esp_cat->term_id,
			'ignore_sticky_posts' => true,
			'tax_query'           => array( array( 'taxonomy' => 'seccion', 'field' => 'term_id', 'terms' => $esp_t->term_id ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
		) );
		if ( $esp_q->have_posts() ) {
			$esp_grupos[ $esp_slug ] = array( 'termino' => $esp_t, 'posts' => $esp_q->posts, 'total' => (int) $esp_q->found_posts );
		}
	}
}

$esp_veredictos = array();
foreach ( array_keys( espabilao_veredictos() ) as $esp_v ) {
	$esp_q = new WP_Query( array( 'posts_per_page' => 1, 'fields' => 'ids', 'cat' => $esp_cat->term_id, 'meta_key' => '_esp_veredicto', 'meta_value' => $esp_v ) ); // phpcs:ignore WordPress.DB.SlowDBQuery
	$esp_veredictos[ $esp_v ] = (int) $esp_q->found_posts;
}
$esp_casos = array_sum( $esp_veredictos );
$esp_herr  = array( 'calculadora-de-plazos', 'generador-de-cartas', 'detector-de-letra-pequena' );
if ( in_array( $esp_cat->slug, array( 'hogar', 'alquiler', 'autonomos' ), true ) ) {
	$esp_herr[] = 'calculadora-de-infraseguro';
}
?>

<section class="hub">
	<div class="envoltorio">
		<?php espabilao_migas(); ?>
		<div class="hub__dentro">
			<div class="hub__texto">
				<span class="hub__icono"><?php echo espabilao_icono( $esp_cat->slug, 40 ); // phpcs:ignore ?></span>
				<p class="supra supra--naranja">Tipo de seguro</p>
				<h1 class="hub__titulo"><?php echo esc_html( $esp_nombre ); ?></h1>
				<p class="hub__lema"><?php echo esc_html( espabilao_lema_tipo( $esp_cat->slug ) ); ?></p>
				<?php if ( $esp_desc ) : ?>
					<p class="hub__desc"><?php echo esc_html( $esp_desc ); ?></p>
				<?php endif; ?>
			</div>
			<div class="hub__datos">
				<div class="dato"><strong><?php echo esc_html( (int) $esp_cat->count ); ?></strong><span>artículos</span></div>
				<div class="dato"><strong><?php echo esc_html( $esp_casos ); ?></strong><span>casos con veredicto</span></div>
				<?php if ( $esp_casos ) : ?>
					<div class="dato dato--ancho">
						<div class="marcador__barra" aria-hidden="true">
							<?php foreach ( $esp_veredictos as $esp_v => $esp_n ) : ?>
								<?php if ( $esp_n ) : ?><span class="marcador__tramo marcador__tramo--<?php echo esc_attr( $esp_v ); ?>" style="flex-grow:<?php echo (int) $esp_n; ?>"></span><?php endif; ?>
							<?php endforeach; ?>
						</div>
						<ul class="marcador__leyenda">
							<?php foreach ( $esp_veredictos as $esp_v => $esp_n ) : ?>
								<li><?php echo espabilao_veredicto_html( $esp_v, 'veredicto--mini' ); // phpcs:ignore ?> <strong><?php echo esc_html( $esp_n ); ?></strong></li>
							<?php endforeach; ?>
						</ul>
					</div>
				<?php endif; ?>
			</div>
		</div>
		<?php if ( $esp_grupos ) : ?>
			<nav class="hub__saltos" aria-label="Ir a">
				<?php foreach ( $esp_grupos as $esp_slug => $esp_g ) : ?>
					<a href="#g-<?php echo esc_attr( $esp_slug ); ?>"><?php echo espabilao_icono_seccion( $esp_slug ); // phpcs:ignore ?> <?php echo esc_html( $esp_g['termino']->name ); ?> <span><?php echo esc_html( $esp_g['total'] ); ?></span></a>
				<?php endforeach; ?>
				<a href="#todos"><?php echo espabilao_icono( 'menu', 20 ); // phpcs:ignore ?> Todo</a>
			</nav>
		<?php endif; ?>
	</div>
</section>

<div class="envoltorio">
	<?php foreach ( $esp_grupos as $esp_slug => $esp_g ) : ?>
		<section class="bloque grupo" id="g-<?php echo esc_attr( $esp_slug ); ?>" aria-labelledby="t-g-<?php echo esc_attr( $esp_slug ); ?>">
			<?php
			espabilao_titulo_bloque(
				't-g-' . $esp_slug,
				$esp_nombre,
				$esp_g['termino']->name,
				$esp_g['total'] > 3 ? add_query_arg( 'cat', $esp_cat->term_id, get_term_link( $esp_g['termino'] ) ) : '',
				'Ver los ' . $esp_g['total']
			);
			?>
			<div class="tarjetas">
				<?php
				foreach ( $esp_g['posts'] as $esp_p ) {
					espabilao_tarjeta( $esp_p );
				}
				?>
			</div>
		</section>
	<?php endforeach; ?>

	<?php if ( 1 === $esp_paged && espabilao_url_herramientas() ) : ?>
		<section class="bloque" aria-labelledby="t-herr-cat">
			<?php espabilao_titulo_bloque( 't-herr-cat', 'Para tu ' . mb_strtolower( $esp_nombre ), 'Herramientas útiles' ); ?>
			<ul class="herramientas-rejilla herramientas-rejilla--compacta">
				<?php foreach ( $esp_herr as $esp_slug ) : ?>
					<?php $esp_h = espabilao_herramientas()[ $esp_slug ]; $esp_u = espabilao_url_herramienta( $esp_slug ); ?>
					<?php if ( $esp_u ) : ?>
						<li class="herramienta-tarjeta"><a href="<?php echo esc_url( $esp_u ); ?>"><span class="herramienta-tarjeta__icono"><?php echo espabilao_icono( $esp_h['icono'], 26 ); // phpcs:ignore ?></span><span class="herramienta-tarjeta__titulo"><?php echo esc_html( $esp_h['titulo'] ); ?></span><span class="herramienta-tarjeta__texto"><?php echo esc_html( $esp_h['corto'] ); ?></span></a></li>
					<?php endif; ?>
				<?php endforeach; ?>
			</ul>
		</section>
	<?php endif; ?>

	<section class="bloque" id="todos" aria-labelledby="t-todos">
		<?php espabilao_titulo_bloque( 't-todos', $esp_nombre, 'Todos los artículos' ); ?>
		<?php if ( have_posts() ) : ?>
			<div class="con-lateral">
				<div class="lista">
					<?php
					$esp_i = 0;
					while ( have_posts() ) :
						the_post();
						espabilao_fila( get_post(), 'h3' );
						if ( 3 === ++$esp_i ) {
							echo espabilao_anuncio( 'archivo' ); // phpcs:ignore WordPress.Security.EscapeOutput
						}
					endwhile;
					espabilao_paginacion();
					?>
				</div>
				<div class="lateral">
					<div class="caja caja--borde">
						<p class="supra">Otros seguros</p>
						<?php espabilao_tipos( 'lista' ); ?>
					</div>
				</div>
			</div>
		<?php else : ?>
			<div class="vacio">
				<p class="vacio__titulo">Todavía no hay artículos sobre este seguro.</p>
				<p>Mientras tanto, usa el buscador o las herramientas.</p>
				<?php get_search_form(); ?>
			</div>
		<?php endif; ?>
	</section>
</div>

<?php
get_footer();
