<?php
/**
 * Archivo: tipo de seguro (categoría), sección, etiqueta, autor y fechas.
 *
 * @package Espabilao
 */

get_header();

$esp_obj       = get_queried_object();
$esp_es_seccion = is_tax( 'seccion' );
$esp_n_seccion = '';
if ( $esp_es_seccion ) {
	$esp_pos = array_search( $esp_obj->slug, array_keys( espabilao_secciones() ), true );
	$esp_n_seccion = false === $esp_pos ? '' : sprintf( '%02d', $esp_pos + 1 );
}
if ( is_category() ) {
	$esp_etiqueta = 'Tipo de seguro';
	$esp_titulo   = 'Seguro de ' . mb_strtolower( single_cat_title( '', false ) );
} elseif ( $esp_es_seccion ) {
	$esp_etiqueta = $esp_n_seccion ? 'Sección ' . $esp_n_seccion : 'Sección';
	$esp_titulo   = single_term_title( '', false );
} elseif ( is_author() ) {
	$esp_etiqueta = 'Autor';
	$esp_titulo   = get_the_author_meta( 'display_name', (int) get_query_var( 'author' ) );
} else {
	$esp_etiqueta = 'Archivo';
	$esp_titulo   = wp_strip_all_tags( get_the_archive_title() );
}
$esp_desc = is_author() ? get_the_author_meta( 'description', (int) get_query_var( 'author' ) ) : wp_strip_all_tags( get_the_archive_description() );
?>

<div class="envoltorio">
	<?php espabilao_migas(); ?>

	<header class="archivo__cabecera<?php echo $esp_es_seccion ? ' archivo__cabecera--seccion' : ''; ?>">
		<?php if ( $esp_es_seccion ) : ?>
			<span class="archivo__icono"><?php echo espabilao_icono_seccion( $esp_obj->slug ); // phpcs:ignore ?></span>
		<?php elseif ( is_category() ) : ?>
			<span class="archivo__icono"><?php echo espabilao_icono( $esp_obj->slug, 28 ); // phpcs:ignore ?></span>
		<?php endif; ?>
		<p class="supra"><?php echo esc_html( $esp_etiqueta ); ?></p>
		<h1 class="archivo__titulo"><?php echo esc_html( $esp_titulo ); ?></h1>
		<?php if ( $esp_desc ) : ?>
			<p class="archivo__desc"><?php echo esc_html( $esp_desc ); ?></p>
		<?php endif; ?>

		<?php if ( $esp_es_seccion && 'pago-o-no-pago' === $esp_obj->slug ) : ?>
			<?php
			$esp_actual = isset( $_GET['veredicto'] ) ? sanitize_key( wp_unslash( $_GET['veredicto'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
			$esp_base   = get_term_link( $esp_obj );
			?>
			<nav class="filtro" aria-label="Filtrar por veredicto">
				<a href="<?php echo esc_url( $esp_base ); ?>" <?php echo '' === $esp_actual ? 'aria-current="page"' : ''; ?>>Todos</a>
				<?php foreach ( espabilao_veredictos() as $esp_k => $esp_v ) : ?>
					<a class="filtro--<?php echo esc_attr( $esp_k ); ?>" href="<?php echo esc_url( add_query_arg( 'veredicto', $esp_k, $esp_base ) ); ?>" <?php echo $esp_actual === $esp_k ? 'aria-current="page"' : ''; ?>><?php echo espabilao_veredicto_html( $esp_k, 'veredicto--mini' ); // phpcs:ignore ?></a>
				<?php endforeach; ?>
			</nav>
		<?php endif; ?>
	</header>

	<?php if ( have_posts() ) : ?>
		<div class="con-lateral">
			<div class="lista">
				<?php
				$esp_i = 0;
				while ( have_posts() ) :
					the_post();
					espabilao_fila( get_post(), 'h2' );
					if ( 3 === ++$esp_i ) {
						echo espabilao_anuncio( 'archivo' ); // phpcs:ignore WordPress.Security.EscapeOutput
					}
				endwhile;
				?>
				<?php espabilao_paginacion(); ?>
			</div>
			<div class="lateral">
				<div class="caja caja--borde">
					<p class="supra">Tipos de seguro</p>
					<?php espabilao_tipos( 'lista' ); ?>
				</div>
			</div>
		</div>
	<?php else : ?>
		<div class="vacio">
			<p class="vacio__titulo">Aquí todavía no hay expedientes.</p>
			<p>Prueba con el buscador o vuelve en unos días.</p>
			<?php get_search_form(); ?>
		</div>
	<?php endif; ?>
</div>

<?php
get_footer();
