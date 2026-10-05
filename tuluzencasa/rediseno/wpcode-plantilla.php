<?php
/* Rediseño tuluzencasa: plantilla de artículo, portada y calculadoras.
   WPCode: fragmento PHP, «Plantilla tuluzencasa», ejecutar en todas partes.
   Pega desde la línea siguiente (sin «<?php»).
   Solo cambia lo que se muestra. No modifica el texto guardado de ningún artículo.
   Para deshacerlo, desactiva el fragmento. */

/* --- Ajustes --- */
define( 'TL_PAGINA_CALC_CONSUMO', 'calculadora-consumo-electrico' );
define( 'TL_PAGINA_CALC_POTENCIA', 'calculadora-potencia-contratada' );

/* 1. Rutas de navegación de Rank Math arriba del todo en las entradas (antes de la imagen destacada) */
add_action( 'generate_before_content', function () {
	if ( is_single() && function_exists( 'rank_math_the_breadcrumbs' ) ) {
		rank_math_the_breadcrumbs();
	}
}, 5 );

/* 2. Fecha de última actualización visible («Actualizado el …») */
add_filter( 'generate_post_date_show_updated_only', function ( $only ) {
	return is_single() ? true : $only;
} );
add_filter( 'generate_post_date_output', function ( $output, $time_string ) {
	if ( ! is_single() ) {
		return $output;
	}
	return '<span class="posted-on">Actualizado el ' . $time_string . '</span> ';
}, 10, 2 );

/* 3. Contenido de las entradas: índice, huecos de anuncios, autor y relacionados */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	$hueco = function ( $sitio ) {
		return '<div class="tl-hueco" data-hueco="' . $sitio . '"></div>';
	};

	// Índice: envuelve el «En este artículo:» que ya tienen los artículos.
	$content = preg_replace(
		'#<p class="wp-block-paragraph">En este artículo:</p>\s*(<ul class="wp-block-list">.*?</ul>)#s',
		'<nav class="tl-indice" aria-label="Índice"><p>En este artículo</p>$1</nav>',
		$content,
		1
	);

	// Hueco 1: tras la introducción (antes del índice o tras el 2.º párrafo).
	$pos = strpos( $content, '<nav class="tl-indice"' );
	if ( false === $pos ) {
		$pos = 0;
		for ( $i = 0; $i < 2 && false !== $pos; $i++ ) {
			$pos = strpos( $content, '</p>', $pos );
			if ( false !== $pos ) {
				$pos += 4;
			}
		}
	}
	if ( $pos ) {
		$content = substr( $content, 0, $pos ) . $hueco( 'intro' ) . substr( $content, $pos );
	}

	// Hueco 2: antes del H2 que queda en mitad del artículo.
	if ( preg_match_all( '#<h2[ >]#', $content, $m, PREG_OFFSET_CAPTURE ) && count( $m[0] ) >= 3 ) {
		$mitad   = $m[0][ intdiv( count( $m[0] ), 2 ) ][1];
		$content = substr( $content, 0, $mitad ) . $hueco( 'mitad' ) . substr( $content, $mitad );
	}

	// Hueco 3: al final.
	$content .= $hueco( 'final' );

	// Caja de autor.
	$autor_id = (int) get_post_field( 'post_author', get_the_ID() );
	$nombre   = get_the_author_meta( 'display_name', $autor_id );
	$bio      = get_the_author_meta( 'description', $autor_id );
	if ( '' === trim( $bio ) ) {
		$bio = 'Escribe Tu luz en casa desde Calatayud (Zaragoza). Calcula cada cifra con las mismas reglas y precios de referencia de toda la web y enlaza las fuentes oficiales.';
	}
	$content .= '<aside class="tl-autor" aria-label="Autor"><div class="tl-autor-av" aria-hidden="true">'
		. esc_html( mb_substr( $nombre, 0, 1 ) ) . '</div><div><p class="tl-autor-n">' . esc_html( $nombre )
		. '</p><p>' . esc_html( $bio ) . '</p><p><a href="' . esc_url( home_url( '/sobre-nosotros/' ) )
		. '">Cómo hacemos los cálculos</a></p></div></aside>';

	// 3 artículos relacionados de la misma categoría (si faltan, los más recientes).
	$id   = get_the_ID();
	$cats = wp_get_post_categories( $id );
	$rel  = get_posts( array(
		'category__in'        => $cats,
		'post__not_in'        => array( $id ),
		'posts_per_page'      => 3,
		'ignore_sticky_posts' => true,
		'no_found_rows'       => true,
	) );
	if ( count( $rel ) < 3 ) {
		$rel = array_merge( $rel, get_posts( array(
			'post__not_in'   => array_merge( array( $id ), wp_list_pluck( $rel, 'ID' ) ),
			'posts_per_page' => 3 - count( $rel ),
			'no_found_rows'  => true,
		) ) );
	}
	if ( $rel ) {
		$html = '';
		foreach ( $rel as $p ) {
			$img   = get_the_post_thumbnail( $p, 'medium_large', array( 'loading' => 'lazy', 'alt' => '' ) );
			$html .= '<li><a href="' . esc_url( get_permalink( $p ) ) . '">' . $img . '<span>'
				. esc_html( get_the_title( $p ) ) . '</span></a></li>';
		}
		$content .= '<section class="tl-rel"><h2>Artículos relacionados</h2><ul>' . $html . '</ul></section>';
	}
	return $content;
}, 20 );

/* 4. Sin «Entrada anterior / siguiente» (los relacionados la sustituyen) */
add_filter( 'generate_show_post_navigation', function ( $show ) {
	return is_single() ? false : $show;
} );

/* 5. Páginas de calculadora a ancho completo, sin barra lateral */
add_filter( 'generate_sidebar_layout', function ( $layout ) {
	if ( is_page( array( TL_PAGINA_CALC_CONSUMO ) ) ) {
		return 'no-sidebar';
	}
	return $layout;
} );

/* 6. Cuadrícula de categorías con icono y número de artículos: [tl_categorias] */
add_shortcode( 'tl_categorias', function () {
	$iconos = array(
		'consumo'         => '<path d="M9 2v6M15 2v6M6 8h12v3a6 6 0 0 1-12 0zM12 17v5"/>',
		'factura-luz'     => '<path d="M5 2h14v20l-3-2-2 2-2-2-2 2-2-2-3 2zM9 7h6M9 11h6M9 15h4"/>',
		'climatizacion'   => '<path d="M14 14.8V4a2 2 0 0 0-4 0v10.8a4 4 0 1 0 4 0zM12 9v7"/>',
		'ahorro'          => '<path d="M3 7l6 6 4-4 8 8M21 11v6h-6"/>',
		'placas-solares'  => '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
		'coche-electrico' => '<path d="M5 16h14v-4l-2-5H7l-2 5zM5 12h14"/><circle cx="8" cy="17" r="2"/><circle cx="16" cy="17" r="2"/>',
		'instalacion'     => '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
	);
	$orden = array_keys( $iconos );
	$cats  = get_terms( array( 'taxonomy' => 'category', 'hide_empty' => true ) );
	if ( is_wp_error( $cats ) ) {
		return '';
	}
	usort( $cats, function ( $a, $b ) use ( $orden ) {
		$ia = array_search( $a->slug, $orden, true );
		$ib = array_search( $b->slug, $orden, true );
		return ( false === $ia ? 99 : $ia ) - ( false === $ib ? 99 : $ib );
	} );
	$html = '<ul class="tl-cats">';
	foreach ( $cats as $c ) {
		if ( 'uncategorized' === $c->slug || 'sin-categoria' === $c->slug ) {
			continue;
		}
		$svg   = isset( $iconos[ $c->slug ] ) ? $iconos[ $c->slug ] : $iconos['consumo'];
		$html .= '<li><a href="' . esc_url( get_category_link( $c ) ) . '"><span class="tl-ico"><svg viewBox="0 0 24 24" aria-hidden="true">'
			. $svg . '</svg></span><span><strong>' . esc_html( $c->name ) . '</strong><small>'
			. sprintf( _n( '%d artículo', '%d artículos', $c->count ), $c->count ) . '</small></span></a></li>';
	}
	return $html . '</ul>';
} );
