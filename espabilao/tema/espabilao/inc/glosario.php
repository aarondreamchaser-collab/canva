<?php
/**
 * Glosario emergente: marca la primera aparición de cada término del
 * glosario en el artículo y muestra su definición al pulsarlo.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

add_action( 'add_meta_boxes', function () {
	add_meta_box( 'espabilao-variantes', 'Variantes del término', function ( $post ) {
		wp_nonce_field( 'espabilao_variantes', 'espabilao_variantes_nonce' );
		printf(
			'<p><input type="text" class="widefat" name="esp_variantes" value="%s" placeholder="plurales, sinónimos…"></p><p class="description">Separadas por comas. El título del término se detecta siempre (también en plural). La definición es el contenido; si rellenas el extracto, se usa el extracto como definición corta.</p>',
			esc_attr( get_post_meta( $post->ID, '_esp_variantes', true ) )
		);
	}, 'glosario', 'side' );
} );

add_action( 'save_post_glosario', function ( $post_id ) {
	delete_transient( 'espabilao_glosario' );
	if ( ! isset( $_POST['espabilao_variantes_nonce'] ) || ! wp_verify_nonce( sanitize_key( $_POST['espabilao_variantes_nonce'] ), 'espabilao_variantes' ) ) {
		return;
	}
	if ( current_user_can( 'edit_post', $post_id ) && isset( $_POST['esp_variantes'] ) ) {
		update_post_meta( $post_id, '_esp_variantes', sanitize_text_field( wp_unslash( $_POST['esp_variantes'] ) ) );
	}
} );
add_action( 'deleted_post', function () {
	delete_transient( 'espabilao_glosario' );
} );

/**
 * Términos del glosario con sus formas a buscar (en caché).
 *
 * @return array<int, array{id:int, titulo:string, def:string, url:string, formas:string[]}>
 */
function espabilao_terminos_glosario() {
	$cache = get_transient( 'espabilao_glosario' );
	if ( is_array( $cache ) ) {
		return $cache;
	}
	$terminos = array();
	$posts    = get_posts( array( 'post_type' => 'glosario', 'post_status' => 'publish', 'numberposts' => 300, 'orderby' => 'title', 'order' => 'ASC' ) );
	foreach ( $posts as $p ) {
		$def = has_excerpt( $p ) ? $p->post_excerpt : wp_strip_all_tags( strip_shortcodes( $p->post_content ) );
		$def = wp_trim_words( $def, 45, '…' );
		$formas = array( $p->post_title );
		foreach ( explode( ',', (string) get_post_meta( $p->ID, '_esp_variantes', true ) ) as $v ) {
			$v = trim( $v );
			if ( '' !== $v ) {
				$formas[] = $v;
			}
		}
		// Las formas más largas primero, para que «periodo de carencia» gane a «carencia».
		usort( $formas, function ( $a, $b ) {
			return mb_strlen( $b ) - mb_strlen( $a );
		} );
		$terminos[] = array(
			'id'     => $p->ID,
			'titulo' => $p->post_title,
			'def'    => $def,
			'url'    => get_permalink( $p ),
			'formas' => $formas,
		);
	}
	set_transient( 'espabilao_glosario', $terminos, DAY_IN_SECONDS );
	return $terminos;
}

/**
 * Marca términos del glosario en un HTML.
 *
 * @param string $html HTML del contenido.
 * @param int    $max  Máximo de términos marcados.
 * @return string
 */
function espabilao_marcar_glosario( $html, $max = 12 ) {
	$terminos = espabilao_terminos_glosario();
	if ( ! $terminos ) {
		return $html;
	}

	$partes   = preg_split( '/(<[^>]+>)/', $html, -1, PREG_SPLIT_DELIM_CAPTURE );
	$saltar   = 0; // Profundidad dentro de etiquetas donde no se marca.
	$prohibidas = '/^<(\/?)(a|h[1-6]|button|code|pre|script|style|figcaption|label|select|textarea|kbd|abbr|dfn)\b/i';
	$usados   = array();
	$marcados = 0;
	$total    = count( $partes );

	for ( $i = 0; $i < $total; $i++ ) {
		$trozo = $partes[ $i ];
		if ( '' === $trozo ) {
			continue;
		}
		if ( '<' === $trozo[0] ) {
			if ( preg_match( $prohibidas, $trozo, $m ) && '/>' !== substr( $trozo, -2 ) ) {
				$saltar += ( '/' === $m[1] ) ? -1 : 1;
				$saltar  = max( 0, $saltar );
			}
			continue;
		}
		if ( $saltar > 0 || $marcados >= $max || '' === trim( $trozo ) ) {
			continue;
		}
		foreach ( $terminos as $t ) {
			if ( isset( $usados[ $t['id'] ] ) || $marcados >= $max ) {
				continue;
			}
			$alternativas = implode( '|', array_map( function ( $f ) {
				return preg_quote( $f, '/' );
			}, $t['formas'] ) );
			$patron = '/(?<![\p{L}\p{N}])(' . $alternativas . ')((?:e?s)?)(?![\p{L}\p{N}])/iu';
			if ( ! preg_match( $patron, $trozo, $m, PREG_OFFSET_CAPTURE ) ) {
				continue;
			}
			$encontrado = $m[0][0];
			$pos        = $m[0][1];
			$id         = 'glosa-' . $t['id'] . '-' . wp_unique_id();
			$marca      = sprintf(
				'<span class="glosa"><button type="button" class="glosa__termino" aria-expanded="false" aria-controls="%1$s">%2$s</button><span class="glosa__def" id="%1$s" role="tooltip" hidden><strong>%3$s.</strong> %4$s <a href="%5$s">Ver en el glosario</a></span></span>',
				esc_attr( $id ),
				$encontrado,
				esc_html( $t['titulo'] ),
				esc_html( $t['def'] ),
				esc_url( $t['url'] )
			);
			// Lo que viene después del término se vuelve a procesar como trozo nuevo.
			$antes   = substr( $trozo, 0, $pos );
			$despues = substr( $trozo, $pos + strlen( $encontrado ) );
			array_splice( $partes, $i, 1, array( $antes, $marca, $despues ) );
			$total += 2;
			$usados[ $t['id'] ] = true;
			$marcados++;
			// Volver a revisar $antes con el resto de términos; la marca se salta
			// sola (empieza por «<») y después se procesa $despues.
			$i--;
			break;
		}
	}
	return implode( '', $partes );
}

add_filter( 'the_content', function ( $html ) {
	if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() || ! espabilao_opcion( 'glosario_auto' ) ) {
		return $html;
	}
	return espabilao_marcar_glosario( $html );
}, 25 );
