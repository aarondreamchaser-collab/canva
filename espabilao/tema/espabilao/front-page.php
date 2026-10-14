<?php
/**
 * Portada.
 *
 * @package Espabilao
 */

get_header();

$esp_casos_ids = array();
$esp_casos     = get_posts( array(
	'numberposts' => 4,
	'tax_query'   => array( array( 'taxonomy' => 'seccion', 'field' => 'slug', 'terms' => 'pago-o-no-pago' ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
) );
$esp_destacado = $esp_casos ? array_shift( $esp_casos ) : null;
foreach ( array_merge( $esp_destacado ? array( $esp_destacado ) : array(), $esp_casos ) as $esp_p ) {
	$esp_casos_ids[] = $esp_p->ID;
}
$esp_busquedas = array_filter( array_map( 'trim', explode( ',', (string) espabilao_opcion( 'busquedas' ) ) ) );
?>

<div class="envoltorio">

	<section class="portada-hero" aria-labelledby="portada-titulo">
		<div class="portada-hero__texto">
			<p class="etiqueta"><?php echo esc_html( espabilao_opcion( 'hero_etiqueta' ) ); ?></p>
			<h2 id="portada-titulo" class="portada-hero__titulo"><?php echo esc_html( espabilao_opcion( 'hero_titulo' ) ); ?> <em><?php echo esc_html( espabilao_opcion( 'hero_destacado' ) ); ?></em></h2>
			<p class="portada-hero__entradilla"><?php echo esc_html( espabilao_opcion( 'hero_texto' ) ); ?></p>
			<?php get_search_form(); ?>
			<?php if ( $esp_busquedas ) : ?>
				<p class="sugerencias"><span>Buscan mucho:</span>
					<?php foreach ( $esp_busquedas as $esp_b ) : ?>
						<a href="<?php echo esc_url( home_url( '/?s=' . rawurlencode( $esp_b ) ) ); ?>"><?php echo esc_html( $esp_b ); ?></a>
					<?php endforeach; ?>
				</p>
			<?php endif; ?>
		</div>

		<?php if ( $esp_destacado ) : ?>
			<article class="expediente">
				<p class="expediente__pestana">Caso n.º <?php echo esc_html( str_pad( (string) $esp_destacado->ID, 4, '0', STR_PAD_LEFT ) ); ?></p>
				<?php espabilao_antetitulo( $esp_destacado->ID ); ?>
				<h3 class="expediente__titulo"><a href="<?php echo esc_url( get_permalink( $esp_destacado ) ); ?>"><?php echo esc_html( get_the_title( $esp_destacado ) ); ?></a></h3>
				<p class="expediente__resumen"><?php echo esc_html( get_the_excerpt( $esp_destacado ) ); ?></p>
				<?php echo espabilao_sello( $esp_destacado->ID, 'sello--grande' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			</article>
		<?php endif; ?>
	</section>

	<section class="bloque" aria-labelledby="t-secciones">
		<header class="bloque__cabecera"><h2 class="bloque__titulo" id="t-secciones"><span class="etiqueta">01—04</span> Las secciones</h2></header>
		<ul class="secciones">
			<?php
			$esp_n = 0;
			foreach ( espabilao_secciones() as $esp_slug => $esp_s ) :
				$esp_n++;
				$esp_t = get_term_by( 'slug', $esp_slug, 'seccion' );
				if ( ! $esp_t ) {
					continue;
				}
				?>
				<li class="seccion">
					<a href="<?php echo esc_url( get_term_link( $esp_t ) ); ?>">
						<span class="seccion__n" aria-hidden="true"><?php echo esc_html( sprintf( '%02d', $esp_n ) ); ?></span>
						<span class="seccion__nombre"><?php echo esc_html( $esp_t->name ); ?></span>
						<span class="seccion__texto"><?php echo esc_html( $esp_t->description ? $esp_t->description : $esp_s['descripcion'] ); ?></span>
					</a>
				</li>
			<?php endforeach; ?>
		</ul>
	</section>

	<?php if ( $esp_casos ) : ?>
		<section class="bloque" aria-labelledby="t-casos">
			<?php
			$esp_term_casos = get_term_by( 'slug', 'pago-o-no-pago', 'seccion' );
			echo '<header class="bloque__cabecera"><h2 class="bloque__titulo" id="t-casos"><span class="etiqueta">Archivo</span> Últimos casos</h2>';
			if ( $esp_term_casos ) {
				echo '<a class="bloque__mas" href="' . esc_url( get_term_link( $esp_term_casos ) ) . '">Todos los casos <span aria-hidden="true">→</span></a>';
			}
			echo '</header>';
			?>
			<div class="casos">
				<?php
				foreach ( $esp_casos as $esp_p ) {
					espabilao_tarjeta_caso( $esp_p );
				}
				?>
			</div>
		</section>
	<?php endif; ?>

	<?php echo espabilao_anuncio( 'portada' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>

	<section class="bloque" aria-labelledby="t-tipos">
		<header class="bloque__cabecera"><h2 class="bloque__titulo" id="t-tipos"><span class="etiqueta">Índice</span> Tipos de seguro</h2></header>
		<?php espabilao_tipos(); ?>
	</section>

	<section class="bloque" aria-labelledby="t-ultimos">
		<header class="bloque__cabecera"><h2 class="bloque__titulo" id="t-ultimos"><span class="etiqueta">Recién revisado</span> Últimos artículos</h2></header>
		<div class="con-lateral">
			<div class="lista">
				<?php
				$esp_ultimos = get_posts( array( 'numberposts' => 6, 'post__not_in' => $esp_casos_ids ) );
				foreach ( $esp_ultimos as $esp_p ) {
					espabilao_fila( $esp_p );
				}
				if ( ! $esp_ultimos ) {
					echo '<p>Todavía no hay artículos publicados.</p>';
				}
				?>
			</div>
			<div class="lateral">
				<div class="caja-regla">
					<p class="etiqueta">Nuestra regla</p>
					<p class="caja-regla__titulo">No vendemos seguros.</p>
					<p>Información general con fuentes oficiales: BOE, Ley de Contrato de Seguro y Dirección General de Seguros. Sin comisiones ni formularios.</p>
				</div>
				<div class="caja-regla caja-regla--glosario">
					<p class="etiqueta">Glosario</p>
					<p class="caja-regla__titulo">¿Franquicia, carencia, infraseguro?</p>
					<p>Las palabras con las que te la cuelan, traducidas.</p>
					<a class="enlace-flecha" href="<?php echo esc_url( (string) get_post_type_archive_link( 'glosario' ) ); ?>">Abrir el glosario <span aria-hidden="true">→</span></a>
				</div>
			</div>
		</div>
	</section>

</div>

<?php
get_footer();
