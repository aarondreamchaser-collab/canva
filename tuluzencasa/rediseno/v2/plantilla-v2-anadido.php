
/* ===================== Rediseño 2 (7-10-2026) =====================
   Va al final de «Plantilla tuluzencasa». Solo cambia lo que se muestra. */

/* 7. Cabecera del artículo: subtítulo (el extracto), tiempo de lectura y sello de fuentes */
add_action( 'generate_after_entry_title', function () {
	if ( ! is_singular( 'post' ) ) {
		return;
	}
	$extracto = get_post_field( 'post_excerpt', get_the_ID() );
	if ( '' !== trim( $extracto ) ) {
		echo '<p class="tl-art-sub">' . esc_html( $extracto ) . '</p>';
	}
}, 5 );
add_action( 'generate_after_entry_title', function () {
	if ( ! is_singular( 'post' ) ) {
		return;
	}
	$palabras = count( preg_split( '/\s+/u', trim( wp_strip_all_tags( get_post_field( 'post_content', get_the_ID() ) ) ) ) );
	$min      = max( 1, (int) ceil( $palabras / 220 ) );
	echo '<div class="tl-art-extra"><span class="tl-lectura">' . $min . ' min de lectura</span>'
		. '<span class="tl-sello">Cifras calculadas con fuentes oficiales</span></div>';
}, 15 );

/* 8. Índice lateral «En esta página» con los H2 del artículo (escritorio y tablet) */
add_action( 'generate_before_right_sidebar_content', function () {
	if ( ! is_singular( 'post' ) ) {
		return;
	}
	$html = get_post_field( 'post_content', get_the_ID() );
	if ( ! preg_match_all( '#<h2[^>]*\sid="([^"]+)"[^>]*>(.*?)</h2>#s', $html, $m, PREG_SET_ORDER ) || count( $m ) < 2 ) {
		return;
	}
	$li = '';
	foreach ( $m as $h ) {
		$li .= '<li><a href="#' . esc_attr( $h[1] ) . '">' . esc_html( wp_strip_all_tags( $h[2] ) ) . '</a></li>';
	}
	echo '<aside class="widget inner-padding tl-toc" aria-label="En esta página"><p class="tl-toc-t">En esta página</p><ol>' . $li . '</ol></aside>';
} );

/* 9. Categorías, búsqueda y blog a ancho completo (cuadrícula de tarjetas) y nº de artículos en la cabecera */
add_filter( 'generate_sidebar_layout', function ( $layout ) {
	if ( is_archive() || is_search() || is_home() ) {
		return 'no-sidebar';
	}
	return $layout;
}, 20 );
add_action( 'generate_after_archive_description', function () {
	if ( is_category() ) {
		$n = (int) get_queried_object()->count;
		echo '<span class="tl-cat-num">' . sprintf( _n( '%d guía', '%d guías', $n ), $n ) . '</span>';
	}
} );

/* 10. Pie nuevo: marca, temas, calculadoras y guías, y la web */
add_action( 'generate_before_footer', function () {
	$cats = get_terms( array( 'taxonomy' => 'category', 'hide_empty' => true, 'orderby' => 'count', 'order' => 'DESC' ) );
	$temas = '';
	if ( ! is_wp_error( $cats ) ) {
		foreach ( $cats as $c ) {
			if ( in_array( $c->slug, array( 'uncategorized', 'sin-categoria' ), true ) ) {
				continue;
			}
			$temas .= '<li><a href="' . esc_url( get_category_link( $c ) ) . '">' . esc_html( $c->name ) . '</a></li>';
		}
	}
	$u = function ( $ruta ) {
		return esc_url( home_url( $ruta ) );
	};
	echo '<footer class="tl-pie" aria-label="Pie de página"><div class="tl-pie-in">'
		. '<div><a class="tl-pie-marca" href="' . $u( '/' ) . '">Tu luz en casa</a>'
		. '<p>Guías y calculadoras para entender lo que gastas en luz y pagar menos. Cifras calculadas con el mismo precio de referencia en toda la web y fuentes oficiales enlazadas.</p></div>'
		. '<div><h2>Temas</h2><ul>' . $temas . '</ul></div>'
		. '<div><h2>Calculadoras y guías</h2><ul>'
		. '<li><a href="' . $u( '/calculadora-consumo-electrico/' ) . '">Calculadora de consumo eléctrico</a></li>'
		. '<li><a href="' . $u( '/calculadora-potencia-contratada/' ) . '">Calculadora de potencia contratada</a></li>'
		. '<li><a href="' . $u( '/como-leer-factura-luz/' ) . '">Cómo leer la factura de la luz</a></li>'
		. '<li><a href="' . $u( '/que-potencia-contratar/' ) . '">Qué potencia contratar</a></li>'
		. '<li><a href="' . $u( '/bono-social-electrico/' ) . '">Bono social eléctrico</a></li></ul></div>'
		. '<div><h2>La web</h2><ul>'
		. '<li><a href="' . $u( '/sobre-nosotros/' ) . '">Sobre nosotros</a></li>'
		. '<li><a href="' . $u( '/contacto/' ) . '">Contacto</a></li>'
		. '<li><a href="' . $u( '/aviso-legal/' ) . '">Aviso legal</a></li>'
		. '<li><a href="' . $u( '/politica-de-privacidad/' ) . '">Política de privacidad</a></li>'
		. '<li><a href="' . $u( '/politica-de-cookies/' ) . '">Política de cookies</a></li></ul></div>'
		. '</div><div class="tl-pie-base"><span>© ' . esc_html( wp_date( 'Y' ) ) . ' Tu luz en casa</span>'
		. '<span>Precio de referencia: 0,165 €/kWh con impuestos. Cambia por el de tu factura.</span></div></footer>';
} );
