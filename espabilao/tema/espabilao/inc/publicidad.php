<?php
/**
 * Huecos de AdSense configurables desde Personalizar.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * ¿Se deben pintar marcadores en lugar de anuncios? (vista previa de Personalizar).
 */
function espabilao_huecos_visibles() {
	return is_customize_preview() || apply_filters( 'espabilao_mostrar_huecos', false );
}

/**
 * ¿Hay anuncios en esta vista?
 */
function espabilao_anuncios_permitidos() {
	if ( is_page() && ! espabilao_opcion( 'ads_paginas' ) ) {
		return false;
	}
	return ! is_404();
}

/**
 * Script de AdSense en la cabecera (solo si hay ID de editor).
 */
add_action( 'wp_head', function () {
	$cliente = espabilao_opcion( 'ads_cliente' );
	if ( ! $cliente || ! espabilao_opcion( 'ads_script' ) || ! espabilao_anuncios_permitidos() || is_customize_preview() ) {
		return;
	}
	printf(
		'<script async src="%s" crossorigin="anonymous"></script>' . "\n",
		esc_url( 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' . rawurlencode( $cliente ) )
	);
}, 5 );

/**
 * HTML de un hueco de anuncio.
 *
 * @param string $hueco parrafo|final|portada|archivo.
 * @return string
 */
function espabilao_anuncio( $hueco ) {
	if ( ! espabilao_anuncios_permitidos() ) {
		return '';
	}
	$cliente = espabilao_opcion( 'ads_cliente' );
	$slot    = espabilao_opcion( 'ads_slot_' . $hueco );
	$altura  = absint( espabilao_opcion( 'ads_altura' ) );
	$estilo  = $altura ? ' style="min-height:' . $altura . 'px"' : '';

	if ( espabilao_huecos_visibles() && ( ! $cliente || ! $slot || is_customize_preview() ) ) {
		return '<div class="anuncio anuncio--' . esc_attr( $hueco ) . ' anuncio--muestra"' . $estilo . '><span class="anuncio__etiqueta">Publicidad</span><span class="anuncio__muestra">Hueco «' . esc_html( $hueco ) . '»' . ( $slot ? '' : ' · sin ID de bloque' ) . '</span></div>';
	}
	if ( ! $cliente || ! $slot ) {
		return '';
	}
	return sprintf(
		'<div class="anuncio anuncio--%1$s"%4$s><span class="anuncio__etiqueta">Publicidad</span><ins class="adsbygoogle" style="display:block" data-ad-client="%2$s" data-ad-slot="%3$s" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>',
		esc_attr( $hueco ),
		esc_attr( $cliente ),
		esc_attr( $slot ),
		$estilo
	);
}

/**
 * Inserta un anuncio tras el párrafo N de primer nivel del contenido.
 * Cuenta solo párrafos que no están dentro de citas, listas, tablas ni bloques
 * del tema (cartas, pólizas, escalera…), para no romper su maquetación.
 *
 * @param string $html Contenido.
 * @param int    $n    Número de párrafo.
 * @param string $insertar HTML a insertar.
 * @return string
 */
function espabilao_insertar_tras_parrafo( $html, $n, $insertar ) {
	if ( ! $insertar || $n < 1 ) {
		return $html;
	}
	$profundidad = 0;
	$contador    = 0;
	$offset      = 0;
	$contenedores = 'div|blockquote|ul|ol|table|figure|section|aside|details|form';
	if ( ! preg_match_all( '#<(/?)(' . $contenedores . '|p)\b[^>]*>#i', $html, $m, PREG_SET_ORDER | PREG_OFFSET_CAPTURE ) ) {
		return $html;
	}
	foreach ( $m as $etiqueta ) {
		$cierre = '/' === $etiqueta[1][0];
		$nombre = strtolower( $etiqueta[2][0] );
		if ( 'p' === $nombre ) {
			if ( $cierre && 0 === $profundidad ) {
				$contador++;
				if ( $contador === $n ) {
					$offset = $etiqueta[0][1] + strlen( $etiqueta[0][0] );
					break;
				}
			}
			continue;
		}
		$profundidad += $cierre ? -1 : 1;
		$profundidad  = max( 0, $profundidad );
	}
	if ( ! $offset ) {
		return $html;
	}
	return substr( $html, 0, $offset ) . $insertar . substr( $html, $offset );
}

add_filter( 'the_content', function ( $html ) {
	if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() ) {
		return $html;
	}
	return espabilao_insertar_tras_parrafo( $html, absint( espabilao_opcion( 'ads_parrafo' ) ), espabilao_anuncio( 'parrafo' ) );
}, 30 );
