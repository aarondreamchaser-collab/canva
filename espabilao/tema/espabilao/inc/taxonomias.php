<?php
/**
 * Taxonomía propia «Sección» y tipo de contenido «Glosario».
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Secciones de la marca. El orden importa: es el que se muestra en portada.
 *
 * @return array<string, array{nombre:string, descripcion:string, corto:string}>
 */
function espabilao_secciones() {
	return array(
		'pago-o-no-pago'      => array(
			'nombre'      => '¿Pagó o no pagó?',
			'corto'       => '¿Pagó o no pagó?',
			'descripcion' => 'Casos reales de siniestros con veredicto: pagó, no pagó o a medias.',
		),
		'polizas-al-desnudo'  => array(
			'nombre'      => 'Pólizas al desnudo',
			'corto'       => 'Pólizas al desnudo',
			'descripcion' => 'Las condiciones de cada aseguradora, explicadas sin letra pequeña.',
		),
		'que-hacer-si'        => array(
			'nombre'      => 'Qué hacer si…',
			'corto'       => 'Qué hacer si…',
			'descripcion' => 'Guías paso a paso, con plazos y plantillas de cartas.',
		),
		'trucos-de-espabilao' => array(
			'nombre'      => 'Trucos de espabilao',
			'corto'       => 'Trucos',
			'descripcion' => 'Consejos rápidos que ahorran disgustos (y dinero).',
		),
	);
}

/**
 * Tipos de seguro: categorías normales de WordPress.
 *
 * @return array<string, string>
 */
function espabilao_tipos_seguro() {
	return array(
		'hogar'     => 'Hogar',
		'coche'     => 'Coche',
		'moto'      => 'Moto',
		'salud'     => 'Salud',
		'vida'      => 'Vida',
		'decesos'   => 'Decesos',
		'mascotas'  => 'Mascotas',
		'viaje'     => 'Viaje',
		'alquiler'  => 'Alquiler',
		'autonomos' => 'Autónomos',
	);
}

function espabilao_registrar_tipos() {
	register_taxonomy( 'seccion', array( 'post' ), array(
		'labels'            => array(
			'name'          => 'Secciones',
			'singular_name' => 'Sección',
			'menu_name'     => 'Secciones',
			'all_items'     => 'Todas las secciones',
			'edit_item'     => 'Editar sección',
			'add_new_item'  => 'Añadir sección',
			'search_items'  => 'Buscar secciones',
			'not_found'     => 'No hay secciones',
		),
		'hierarchical'      => true,
		'public'            => true,
		'show_in_rest'      => true,
		'show_admin_column' => true,
		'rewrite'           => array( 'slug' => 'seccion', 'with_front' => false ),
	) );

	register_post_type( 'glosario', array(
		'labels'        => array(
			'name'          => 'Glosario',
			'singular_name' => 'Término',
			'add_new'       => 'Añadir término',
			'add_new_item'  => 'Añadir término al glosario',
			'edit_item'     => 'Editar término',
			'all_items'     => 'Todos los términos',
			'menu_name'     => 'Glosario',
			'search_items'  => 'Buscar términos',
			'not_found'     => 'No hay términos',
		),
		'public'        => true,
		'has_archive'   => 'glosario',
		'rewrite'       => array( 'slug' => 'glosario', 'with_front' => false ),
		'menu_icon'     => 'dashicons-book-alt',
		'menu_position' => 21,
		'supports'      => array( 'title', 'editor', 'excerpt' ),
		'show_in_rest'  => true,
	) );
}
add_action( 'init', 'espabilao_registrar_tipos' );

/**
 * Glosario ordenado alfabéticamente y completo en su archivo.
 */
add_action( 'pre_get_posts', function ( $q ) {
	if ( is_admin() || ! $q->is_main_query() ) {
		return;
	}
	if ( $q->is_post_type_archive( 'glosario' ) ) {
		$q->set( 'orderby', 'title' );
		$q->set( 'order', 'ASC' );
		$q->set( 'posts_per_page', 200 );
	}
	// Filtro por veredicto en el archivo de la sección de casos: ?veredicto=pago.
	if ( $q->is_tax( 'seccion' ) && ! empty( $_GET['veredicto'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
		$v = sanitize_key( wp_unslash( $_GET['veredicto'] ) ); // phpcs:ignore WordPress.Security.NonceVerification
		if ( isset( espabilao_veredictos()[ $v ] ) ) {
			$q->set( 'meta_key', '_esp_veredicto' );
			$q->set( 'meta_value', $v );
		}
	}
} );
