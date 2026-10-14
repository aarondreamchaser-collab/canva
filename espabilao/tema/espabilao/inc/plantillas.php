<?php
/**
 * Piezas reutilizables de las plantillas.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Logotipo: el personalizado o el de la marca (icono «¡!» + nombre).
 *
 * @param string $etiqueta Elemento contenedor.
 * @param string $clase    Clase extra.
 */
function espabilao_logo( $etiqueta = 'p', $clase = '' ) {
	if ( has_custom_logo() ) {
		echo '<' . tag_escape( $etiqueta ) . ' class="logo ' . esc_attr( $clase ) . '">';
		the_custom_logo();
		echo '</' . tag_escape( $etiqueta ) . '>';
		return;
	}
	$nombre = get_bloginfo( 'name' ) ? get_bloginfo( 'name' ) : 'Espabilao';
	printf(
		'<%1$s class="logo %4$s"><a href="%2$s" rel="home"><span class="logo__icono" aria-hidden="true">¡!</span><span class="logo__nombre">%3$s</span></a></%1$s>',
		tag_escape( $etiqueta ),
		esc_url( home_url( '/' ) ),
		esc_html( mb_strtolower( $nombre ) ),
		esc_attr( $clase )
	);
}

/**
 * Etiqueta de veredicto («semáforo»).
 *
 * @param int    $post_id Entrada.
 * @param string $extra   Clase extra (veredicto--grande, veredicto--mini).
 * @return string
 */
function espabilao_sello( $post_id, $extra = '' ) {
	$v     = get_post_meta( $post_id, '_esp_veredicto', true );
	$todos = espabilao_veredictos();
	if ( ! isset( $todos[ $v ] ) ) {
		return '';
	}
	return espabilao_veredicto_html( $v, $extra );
}

/**
 * HTML de un veredicto concreto.
 *
 * @param string $v     pago|no-pago|a-medias.
 * @param string $extra Clase extra.
 * @param string $texto Texto alternativo.
 * @return string
 */
function espabilao_veredicto_html( $v, $extra = '', $texto = '' ) {
	$todos  = espabilao_veredictos();
	$iconos = array( 'pago' => 'si', 'no-pago' => 'no', 'a-medias' => 'medias' );
	return sprintf(
		'<span class="veredicto veredicto--%1$s %2$s"><span class="veredicto__icono">%3$s</span><span class="screen-reader-text">Veredicto: </span>%4$s</span>',
		esc_attr( $v ),
		esc_attr( $extra ),
		espabilao_icono( $iconos[ $v ], 16 ),
		esc_html( $texto ? $texto : $todos[ $v ] )
	);
}

/**
 * Recuento de casos por veredicto (en caché 12 h).
 *
 * @return array<string, int>
 */
function espabilao_marcador() {
	$cache = get_transient( 'espabilao_marcador' );
	if ( is_array( $cache ) ) {
		return $cache;
	}
	$salida = array();
	foreach ( array_keys( espabilao_veredictos() ) as $v ) {
		$q = new WP_Query( array(
			'post_type'      => 'post',
			'post_status'    => 'publish',
			'posts_per_page' => 1,
			'fields'         => 'ids',
			'no_found_rows'  => false,
			'meta_key'       => '_esp_veredicto', // phpcs:ignore WordPress.DB.SlowDBQuery
			'meta_value'     => $v, // phpcs:ignore WordPress.DB.SlowDBQuery
		) );
		$salida[ $v ] = (int) $q->found_posts;
	}
	set_transient( 'espabilao_marcador', $salida, 12 * HOUR_IN_SECONDS );
	return $salida;
}
add_action( 'save_post_post', function () {
	delete_transient( 'espabilao_marcador' );
}, 20 );

/**
 * Primera sección de una entrada.
 *
 * @param int $post_id Entrada.
 * @return WP_Term|null
 */
function espabilao_seccion_de( $post_id ) {
	$t = get_the_terms( $post_id, 'seccion' );
	return ( $t && ! is_wp_error( $t ) ) ? $t[0] : null;
}

/**
 * Primera categoría (tipo de seguro), sin la categoría por defecto.
 *
 * @param int $post_id Entrada.
 * @return WP_Term|null
 */
function espabilao_tipo_de( $post_id ) {
	foreach ( get_the_category( $post_id ) as $c ) {
		if ( (int) get_option( 'default_category' ) !== (int) $c->term_id ) {
			return $c;
		}
	}
	return null;
}

/**
 * Píldoras de sección y tipo de seguro.
 *
 * @param int  $post_id Entrada.
 * @param bool $enlaces Con enlaces.
 */
function espabilao_antetitulo( $post_id, $enlaces = false ) {
	$piezas = array();
	$s      = espabilao_seccion_de( $post_id );
	$t      = espabilao_tipo_de( $post_id );
	if ( $s ) {
		$piezas[] = $enlaces
			? '<a class="pildora pildora--seccion" href="' . esc_url( get_term_link( $s ) ) . '">' . esc_html( $s->name ) . '</a>'
			: '<span class="pildora pildora--seccion">' . esc_html( $s->name ) . '</span>';
	}
	if ( $t ) {
		$piezas[] = $enlaces
			? '<a class="pildora" href="' . esc_url( get_term_link( $t ) ) . '">' . espabilao_icono( $t->slug, 14 ) . esc_html( $t->name ) . '</a>'
			: '<span class="pildora">' . espabilao_icono( $t->slug, 14 ) . esc_html( $t->name ) . '</span>';
	}
	if ( $piezas ) {
		echo '<p class="antetitulo">' . implode( '', $piezas ) . '</p>'; // phpcs:ignore WordPress.Security.EscapeOutput
	}
}

/**
 * «Revisado el 10 oct 2026».
 *
 * @param int    $post_id Entrada.
 * @param string $formato Formato de fecha.
 */
function espabilao_revisado( $post_id, $formato = 'j M Y' ) {
	$ts = (int) espabilao_fecha_revision( $post_id );
	printf(
		'<span class="revisado">%3$s Revisado el <time datetime="%1$s">%2$s</time></span>',
		esc_attr( wp_date( 'Y-m-d', $ts ) ),
		esc_html( mb_strtolower( wp_date( $formato, $ts ) ) ),
		espabilao_icono( 'reloj', 14 ) // phpcs:ignore WordPress.Security.EscapeOutput
	);
}

/**
 * Imagen destacada o portadilla con el icono del tipo de seguro.
 *
 * @param int    $post_id Entrada.
 * @param string $tamano  Tamaño de imagen.
 */
function espabilao_imagen( $post_id, $tamano = 'espabilao-tarjeta' ) {
	if ( has_post_thumbnail( $post_id ) ) {
		echo get_the_post_thumbnail( $post_id, $tamano, array( 'class' => 'imagen', 'loading' => 'lazy', 'alt' => '' ) );
		return;
	}
	$t     = espabilao_tipo_de( $post_id );
	$s     = espabilao_seccion_de( $post_id );
	$tinte = $s ? $s->slug : 'general';
	echo '<span class="imagen imagen--vacia imagen--' . esc_attr( $tinte ) . '" aria-hidden="true">' . espabilao_icono( $t ? $t->slug : 'doc', 44 ) . '</span>'; // phpcs:ignore WordPress.Security.EscapeOutput
}

/**
 * Tarjeta de artículo o caso.
 *
 * @param WP_Post $post   Entrada.
 * @param string  $nivel  h2|h3.
 */
function espabilao_tarjeta( $post, $nivel = 'h3' ) {
	$nivel = in_array( $nivel, array( 'h2', 'h3' ), true ) ? $nivel : 'h3';
	$url   = get_permalink( $post );
	?>
	<article class="tarjeta">
		<a class="tarjeta__imagen" href="<?php echo esc_url( $url ); ?>" tabindex="-1" aria-hidden="true">
			<?php espabilao_imagen( $post->ID ); ?>
			<?php echo espabilao_sello( $post->ID, 'veredicto--flotante' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
		</a>
		<div class="tarjeta__cuerpo">
			<?php espabilao_antetitulo( $post->ID ); ?>
			<<?php echo $nivel; // phpcs:ignore ?> class="tarjeta__titulo"><a href="<?php echo esc_url( $url ); ?>"><?php echo esc_html( get_the_title( $post ) ); ?></a></<?php echo $nivel; // phpcs:ignore ?>>
			<p class="tarjeta__resumen"><?php echo esc_html( get_the_excerpt( $post ) ); ?></p>
			<p class="tarjeta__meta"><?php espabilao_revisado( $post->ID ); ?></p>
		</div>
	</article>
	<?php
}

/**
 * Compatibilidad con plantillas antiguas.
 *
 * @param WP_Post $post Entrada.
 */
function espabilao_tarjeta_caso( $post ) {
	espabilao_tarjeta( $post );
}

/**
 * Fila compacta para listados.
 *
 * @param WP_Post $post  Entrada.
 * @param string  $nivel h2|h3.
 */
function espabilao_fila( $post, $nivel = 'h3' ) {
	$nivel = in_array( $nivel, array( 'h2', 'h3' ), true ) ? $nivel : 'h3';
	?>
	<article class="fila">
		<a class="fila__imagen" href="<?php echo esc_url( get_permalink( $post ) ); ?>" tabindex="-1" aria-hidden="true"><?php espabilao_imagen( $post->ID, 'espabilao-mini' ); ?></a>
		<div class="fila__texto">
			<?php espabilao_antetitulo( $post->ID ); ?>
			<<?php echo $nivel; // phpcs:ignore ?> class="fila__titulo"><a href="<?php echo esc_url( get_permalink( $post ) ); ?>"><?php echo esc_html( get_the_title( $post ) ); ?></a></<?php echo $nivel; // phpcs:ignore ?>>
			<p class="fila__resumen"><?php echo esc_html( get_the_excerpt( $post ) ); ?></p>
			<p class="fila__meta"><?php espabilao_revisado( $post->ID ); ?><?php echo espabilao_sello( $post->ID, 'veredicto--mini' ); // phpcs:ignore ?></p>
		</div>
	</article>
	<?php
}

/**
 * Migas de pan: las de Rank Math si están activas; si no, unas sencillas.
 * (Sin marcado de datos estructurados: eso lo pone Rank Math.)
 */
function espabilao_migas() {
	if ( function_exists( 'rank_math_the_breadcrumbs' ) ) {
		$opciones = get_option( 'rank-math-options-general' );
		if ( is_array( $opciones ) && ! empty( $opciones['breadcrumbs'] ) && 'off' !== $opciones['breadcrumbs'] ) {
			echo '<nav class="migas" aria-label="Migas de pan">';
			rank_math_the_breadcrumbs();
			echo '</nav>';
			return;
		}
	}
	$items = array( '<a href="' . esc_url( home_url( '/' ) ) . '">Inicio</a>' );
	if ( is_singular( 'post' ) ) {
		$s = espabilao_seccion_de( get_the_ID() );
		if ( $s ) {
			$items[] = '<a href="' . esc_url( get_term_link( $s ) ) . '">' . esc_html( $s->name ) . '</a>';
		}
	} elseif ( is_singular( 'glosario' ) ) {
		$items[] = '<a href="' . esc_url( get_post_type_archive_link( 'glosario' ) ) . '">Glosario</a>';
	}
	echo '<nav class="migas" aria-label="Migas de pan"><ol><li>' . implode( '</li><li>', $items ) . '</li></ol></nav>'; // phpcs:ignore WordPress.Security.EscapeOutput
}

/**
 * Menú por defecto si no se ha creado uno: las cuatro secciones + glosario.
 *
 * @param array $args Argumentos de wp_nav_menu (se usa menu_class).
 */
function espabilao_menu_defecto( $args = array() ) {
	$clase = is_array( $args ) && ! empty( $args['menu_class'] ) ? $args['menu_class'] : 'menu';
	echo '<ul class="' . esc_attr( $clase ) . '">';
	foreach ( espabilao_secciones() as $slug => $s ) {
		$t = get_term_by( 'slug', $slug, 'seccion' );
		if ( $t ) {
			printf( '<li><a href="%s">%s</a></li>', esc_url( get_term_link( $t ) ), esc_html( $s['corto'] ) );
		}
	}
	printf( '<li><a href="%s">Glosario</a></li>', esc_url( (string) get_post_type_archive_link( 'glosario' ) ) );
	echo '</ul>';
}

/**
 * Tipos de seguro (categorías) en el orden de la marca.
 *
 * @return WP_Term[]
 */
function espabilao_categorias_ordenadas() {
	$cats  = get_categories( array( 'hide_empty' => false, 'exclude' => array( (int) get_option( 'default_category' ) ) ) );
	$orden = array_keys( espabilao_tipos_seguro() );
	usort( $cats, function ( $a, $b ) use ( $orden ) {
		$ia = array_search( $a->slug, $orden, true );
		$ib = array_search( $b->slug, $orden, true );
		$ia = false === $ia ? 99 : $ia;
		$ib = false === $ib ? 99 : $ib;
		return $ia <=> $ib ?: strcmp( $a->name, $b->name );
	} );
	return $cats;
}

/**
 * Rejilla de tipos de seguro con icono y número de artículos.
 *
 * @param string $variante «rejilla» o «lista».
 */
function espabilao_tipos( $variante = 'rejilla' ) {
	$cats = espabilao_categorias_ordenadas();
	if ( ! $cats ) {
		return;
	}
	echo '<ul class="tipos tipos--' . esc_attr( $variante ) . '">';
	foreach ( $cats as $c ) {
		printf(
			'<li><a href="%1$s"><span class="tipos__icono">%2$s</span><span class="tipos__nombre">%3$s</span><span class="tipos__n">%4$d<span class="screen-reader-text"> %5$s</span></span></a></li>',
			esc_url( get_term_link( $c ) ),
			espabilao_icono( $c->slug, 28 ), // phpcs:ignore WordPress.Security.EscapeOutput
			esc_html( $c->name ),
			(int) $c->count,
			esc_html( _n( 'artículo', 'artículos', $c->count, 'espabilao' ) )
		);
	}
	echo '</ul>';
}

/**
 * Paginación de listados.
 */
function espabilao_paginacion() {
	the_posts_pagination( array(
		'mid_size'           => 1,
		'prev_text'          => '← Anteriores',
		'next_text'          => 'Siguientes →',
		'screen_reader_text' => 'Más páginas',
	) );
}

/**
 * Cabecera de bloque en portada.
 *
 * @param string $id           Id del título.
 * @param string $antetitulo   Texto pequeño.
 * @param string $titulo       Título.
 * @param string $enlace       URL «ver todo».
 * @param string $texto_enlace Texto del enlace.
 */
function espabilao_titulo_bloque( $id, $antetitulo, $titulo, $enlace = '', $texto_enlace = 'Ver todo' ) {
	echo '<header class="bloque__cabecera"><div><p class="supra">' . esc_html( $antetitulo ) . '</p><h2 class="bloque__titulo" id="' . esc_attr( $id ) . '">' . esc_html( $titulo ) . '</h2></div>';
	if ( $enlace ) {
		echo '<a class="enlace-mas" href="' . esc_url( $enlace ) . '">' . esc_html( $texto_enlace ) . ' ' . espabilao_icono( 'flecha', 18 ) . '</a>'; // phpcs:ignore WordPress.Security.EscapeOutput
	}
	echo '</header>';
}

/**
 * Un término del glosario al azar (cambia cada día).
 *
 * @return WP_Post|null
 */
function espabilao_palabra_del_dia() {
	$ids = get_posts( array( 'post_type' => 'glosario', 'numberposts' => 200, 'fields' => 'ids', 'orderby' => 'title', 'order' => 'ASC' ) );
	if ( ! $ids ) {
		return null;
	}
	return get_post( $ids[ (int) wp_date( 'z' ) % count( $ids ) ] );
}
