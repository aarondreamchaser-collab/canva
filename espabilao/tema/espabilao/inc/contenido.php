<?php
/**
 * Utilidades sobre el contenido del artículo: índice y tiempo de lectura.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Añade id a los H2 del contenido y devuelve [html, índice].
 *
 * @param string $html Contenido ya filtrado.
 * @return array{0:string, 1:array<int, array{0:string, 1:string}>}
 */
function espabilao_indice( $html ) {
	$indice = array();
	$usados = array();
	$html   = preg_replace_callback( '#<h2\b([^>]*)>(.*?)</h2>#is', function ( $m ) use ( &$indice, &$usados ) {
		$texto = trim( wp_strip_all_tags( $m[2] ) );
		if ( '' === $texto ) {
			return $m[0];
		}
		// Los títulos de bloques del tema (escalera, plazos) no entran en el índice.
		if ( preg_match( '/class="[^"]*(escalera__titulo|plazos__titulo)/', $m[1] ) ) {
			return $m[0];
		}
		if ( preg_match( '/\bid="([^"]+)"/', $m[1], $id ) ) {
			$ancla = $id[1];
			$atrib = $m[1];
		} else {
			$base  = sanitize_title( $texto );
			$ancla = $base ? $base : 'apartado';
			$n     = 2;
			while ( isset( $usados[ $ancla ] ) ) {
				$ancla = $base . '-' . $n++;
			}
			$atrib = $m[1] . ' id="' . esc_attr( $ancla ) . '"';
		}
		$usados[ $ancla ] = true;
		$indice[]         = array( $ancla, $texto );
		return '<h2' . $atrib . '>' . $m[2] . '</h2>';
	}, $html );
	return array( $html, $indice );
}

/**
 * Minutos de lectura (200 palabras por minuto).
 *
 * @param int $post_id Entrada.
 * @return int
 */
function espabilao_minutos_lectura( $post_id ) {
	$texto    = trim( wp_strip_all_tags( strip_shortcodes( get_post_field( 'post_content', $post_id ) ) ) );
	$palabras = '' === $texto ? 0 : count( preg_split( '/\s+/u', $texto ) );
	return max( 1, (int) round( $palabras / 200 ) );
}

/**
 * ¿Debe añadirse la escalera de reclamación al final de este artículo?
 *
 * @param int $post_id Entrada.
 * @return bool
 */
function espabilao_necesita_escalera( $post_id ) {
	if ( ! espabilao_opcion( 'escalera_auto' ) ) {
		return false;
	}
	if ( has_shortcode( get_post_field( 'post_content', $post_id ), 'escalera_reclamacion' ) ) {
		return false;
	}
	return has_term( array( 'pago-o-no-pago', 'que-hacer-si' ), 'seccion', $post_id );
}
