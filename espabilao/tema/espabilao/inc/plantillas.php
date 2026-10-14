<?php
/**
 * Piezas reutilizables de las plantillas.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Logotipo: el personalizado o el tipográfico.
 *
 * @param string $etiqueta Elemento contenedor.
 */
function espabilao_logo( $etiqueta = 'p' ) {
	if ( has_custom_logo() ) {
		the_custom_logo();
		return;
	}
	printf(
		'<%1$s class="logo"><a href="%2$s" rel="home">%3$s<span class="logo__punto" aria-hidden="true">.</span></a></%1$s>',
		tag_escape( $etiqueta ),
		esc_url( home_url( '/' ) ),
		esc_html( get_bloginfo( 'name' ) ? get_bloginfo( 'name' ) : 'Espabilao' )
	);
}

/**
 * Sello de veredicto.
 *
 * @param int    $post_id Entrada.
 * @param string $extra   Clase extra (p. ej. «sello--grande»).
 * @return string
 */
function espabilao_sello( $post_id, $extra = '' ) {
	$v = get_post_meta( $post_id, '_esp_veredicto', true );
	$todos = espabilao_veredictos();
	if ( ! isset( $todos[ $v ] ) ) {
		return '';
	}
	return sprintf(
		'<span class="sello sello--%1$s %2$s"><span class="screen-reader-text">Veredicto: </span>%3$s</span>',
		esc_attr( $v ),
		esc_attr( $extra ),
		esc_html( $todos[ $v ] )
	);
}

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
 * Primera categoría (tipo de seguro) de una entrada, sin «Sin categoría».
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
 * Antetítulo: «Sección · Tipo de seguro».
 *
 * @param int  $post_id Entrada.
 * @param bool $enlaces Con enlaces.
 */
function espabilao_antetitulo( $post_id, $enlaces = false ) {
	$piezas = array();
	foreach ( array( espabilao_seccion_de( $post_id ), espabilao_tipo_de( $post_id ) ) as $t ) {
		if ( ! $t ) {
			continue;
		}
		$piezas[] = $enlaces
			? '<a href="' . esc_url( get_term_link( $t ) ) . '">' . esc_html( $t->name ) . '</a>'
			: esc_html( $t->name );
	}
	if ( $piezas ) {
		echo '<p class="antetitulo">' . implode( ' <span aria-hidden="true">·</span> ', $piezas ) . '</p>'; // phpcs:ignore WordPress.Security.EscapeOutput
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
		'<span class="revisado">Revisado el <time datetime="%1$s">%2$s</time></span>',
		esc_attr( wp_date( 'Y-m-d', $ts ) ),
		esc_html( wp_date( $formato, $ts ) )
	);
}

/**
 * Imagen destacada o, si no hay, una portadilla tipográfica.
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
	$letra = $t ? mb_substr( $t->name, 0, 1 ) : '§';
	echo '<span class="imagen imagen--vacia" aria-hidden="true"><span>' . esc_html( $letra ) . '</span></span>';
}

/**
 * Tarjeta de caso (con sello).
 *
 * @param WP_Post $post Entrada.
 */
function espabilao_tarjeta_caso( $post ) {
	?>
	<article class="caso">
		<?php espabilao_antetitulo( $post->ID ); ?>
		<h3 class="caso__titulo"><a href="<?php echo esc_url( get_permalink( $post ) ); ?>"><?php echo esc_html( get_the_title( $post ) ); ?></a></h3>
		<p class="caso__resumen"><?php echo esc_html( get_the_excerpt( $post ) ); ?></p>
		<?php echo espabilao_sello( $post->ID ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
	</article>
	<?php
}

/**
 * Fila de artículo para listados.
 *
 * @param WP_Post $post    Entrada.
 * @param string  $nivel   Nivel de título (h2|h3).
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
			<p class="fila__meta"><?php espabilao_revisado( $post->ID ); ?><?php echo espabilao_sello( $post->ID, 'sello--mini' ); // phpcs:ignore ?></p>
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
 */
function espabilao_menu_defecto() {
	echo '<ul class="menu">';
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
 * Lista de tipos de seguro con su número de artículos.
 */
function espabilao_tipos() {
	$cats = get_categories( array( 'hide_empty' => false, 'exclude' => array( (int) get_option( 'default_category' ) ) ) );
	$orden = array_keys( espabilao_tipos_seguro() );
	usort( $cats, function ( $a, $b ) use ( $orden ) {
		$ia = array_search( $a->slug, $orden, true );
		$ib = array_search( $b->slug, $orden, true );
		$ia = false === $ia ? 99 : $ia;
		$ib = false === $ib ? 99 : $ib;
		return $ia <=> $ib ?: strcmp( $a->name, $b->name );
	} );
	if ( ! $cats ) {
		return;
	}
	echo '<ul class="tipos">';
	foreach ( $cats as $c ) {
		printf(
			'<li><a href="%s"><span class="tipos__nombre">%s</span><span class="tipos__n">%d<span class="screen-reader-text"> %s</span></span></a></li>',
			esc_url( get_term_link( $c ) ),
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
 * Cabecera de sección en portada.
 */
function espabilao_titulo_bloque( $etiqueta, $titulo, $enlace = '', $texto_enlace = 'Ver todo' ) {
	echo '<header class="bloque__cabecera"><h2 class="bloque__titulo"><span class="etiqueta">' . esc_html( $etiqueta ) . '</span> ' . esc_html( $titulo ) . '</h2>';
	if ( $enlace ) {
		echo '<a class="bloque__mas" href="' . esc_url( $enlace ) . '">' . esc_html( $texto_enlace ) . ' <span aria-hidden="true">→</span></a>';
	}
	echo '</header>';
}
