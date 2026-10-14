<?php
/**
 * Al activar el tema: crea secciones, tipos de seguro (categorías)
 * y los términos básicos del glosario. Nunca borra ni sobrescribe nada.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Términos iniciales del glosario: título, variantes y definición.
 *
 * @return array<int, array{0:string, 1:string, 2:string}>
 */
function espabilao_glosario_inicial() {
	return array(
		array( 'Franquicia', '', 'Parte del daño que pagas tú en cada siniestro. Si la franquicia es de 300 € y la reparación cuesta 1.000 €, la aseguradora paga 700 €.' ),
		array( 'Carencia', 'periodo de carencia, periodos de carencia', 'Tiempo desde que contratas durante el que una cobertura todavía no funciona. Es habitual en salud (partos, operaciones) y en algunos seguros de mascotas.' ),
		array( 'Infraseguro', 'infraasegurado, infraasegurada', 'Cuando declaras un valor inferior al real (por ejemplo, del contenido de tu casa). La aseguradora puede pagarte solo en proporción: es la «regla proporcional» del artículo 30 de la Ley de Contrato de Seguro.' ),
		array( 'Sobreseguro', '', 'Cuando la suma asegurada supera claramente el valor real de lo asegurado. Pagas más prima, pero en un siniestro solo te indemnizan el daño real (art. 31 de la Ley de Contrato de Seguro).' ),
		array( 'Regla proporcional', '', 'Fórmula que reduce la indemnización cuando hay infraseguro: te pagan el mismo porcentaje del daño que el porcentaje del valor real que tenías asegurado.' ),
		array( 'Preexistencia', 'preexistencias, enfermedad preexistente, enfermedades preexistentes', 'Enfermedad o lesión que ya tenías antes de contratar. Muchas pólizas de salud y vida las excluyen si no las declaraste en el cuestionario.' ),
		array( 'Siniestro', '', 'El hecho que activa el seguro: un accidente, una avería cubierta, un robo, una enfermedad… Debes comunicarlo en un máximo de 7 días desde que lo conoces, salvo que la póliza dé más plazo.' ),
		array( 'Prima', '', 'Lo que pagas por el seguro, normalmente cada año o cada mes.' ),
		array( 'Tomador', 'tomador del seguro', 'La persona que contrata y paga el seguro. No siempre coincide con el asegurado ni con el beneficiario.' ),
		array( 'Beneficiario', 'beneficiarios', 'Quien cobra la indemnización. En un seguro de vida, la persona designada para recibir el capital.' ),
		array( 'Perito', 'peritos, peritaje, contraperitaje', 'Profesional que valora los daños. Si no estás de acuerdo con el de la aseguradora, puedes nombrar uno propio (art. 38 de la Ley de Contrato de Seguro).' ),
		array( 'Cláusula limitativa', 'cláusulas limitativas', 'Condición que recorta tus derechos como asegurado. Por ley debe estar destacada en la póliza y firmada expresamente por ti (art. 3 de la Ley de Contrato de Seguro).' ),
		array( 'Condiciones generales', '', 'El reglamento común de un producto de seguro, igual para todos los clientes. Aquí suelen estar las exclusiones.' ),
		array( 'Condiciones particulares', '', 'La parte de la póliza con tus datos: qué se asegura, por cuánto, franquicias, fechas y prima.' ),
		array( 'Valor de reposición', 'valor a nuevo', 'Indemnización por lo que cuesta comprar hoy un bien nuevo equivalente, sin descontar el desgaste.' ),
		array( 'Valor venal', '', 'Lo que valía tu vehículo justo antes del siniestro en el mercado de segunda mano. Suele ser lo que te pagan en caso de siniestro total.' ),
		array( 'Suma asegurada', 'capital asegurado', 'Límite máximo que la aseguradora pagará por una cobertura.' ),
		array( 'Exclusión', 'exclusiones', 'Situación que la póliza deja fuera expresamente: si ocurre, no hay cobertura.' ),
	);
}

/**
 * Crea un término si no existe.
 */
function espabilao_crear_termino( $nombre, $slug, $taxonomia, $descripcion = '' ) {
	if ( term_exists( $slug, $taxonomia ) ) {
		return;
	}
	wp_insert_term( $nombre, $taxonomia, array( 'slug' => $slug, 'description' => $descripcion ) );
}

function espabilao_al_activar() {
	espabilao_registrar_tipos();

	foreach ( espabilao_secciones() as $slug => $s ) {
		espabilao_crear_termino( $s['nombre'], $slug, 'seccion', $s['descripcion'] );
	}
	foreach ( espabilao_tipos_seguro() as $slug => $nombre ) {
		espabilao_crear_termino( $nombre, $slug, 'category', 'Todo sobre el seguro de ' . mb_strtolower( $nombre ) . ': coberturas, casos y reclamaciones.' );
	}

	if ( ! get_option( 'espabilao_glosario_creado' ) ) {
		foreach ( espabilao_glosario_inicial() as $t ) {
			if ( get_page_by_path( sanitize_title( $t[0] ), OBJECT, 'glosario' ) ) {
				continue;
			}
			$id = wp_insert_post( array(
				'post_type'    => 'glosario',
				'post_status'  => 'publish',
				'post_title'   => $t[0],
				'post_content' => '<!-- wp:paragraph --><p>' . esc_html( $t[2] ) . '</p><!-- /wp:paragraph -->',
			) );
			if ( $id && ! is_wp_error( $id ) && $t[1] ) {
				update_post_meta( $id, '_esp_variantes', $t[1] );
			}
		}
		update_option( 'espabilao_glosario_creado', 1, false );
	}

	if ( function_exists( 'espabilao_crear_paginas_herramientas' ) ) {
		espabilao_crear_paginas_herramientas();
	}

	update_option( 'espabilao_version_datos', 3, false );
	flush_rewrite_rules();
}
add_action( 'after_switch_theme', 'espabilao_al_activar' );

/**
 * Al actualizar el tema (sin cambiar de tema) también se crean las piezas nuevas.
 */
add_action( 'init', function () {
	if ( (int) get_option( 'espabilao_version_datos', 0 ) < 3 ) {
		espabilao_al_activar();
	}
}, 30 );
