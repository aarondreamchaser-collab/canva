<?php
/**
 * Opciones en Apariencia > Personalizar.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Valores por defecto de todas las opciones.
 *
 * @return array<string, mixed>
 */
function espabilao_opciones_defecto() {
	return array(
		// Portada.
		'hero_etiqueta'   => 'Información independiente sobre seguros',
		'hero_titulo'     => 'Que no te la cuelen',
		'hero_destacado'  => 'con tu seguro.',
		'hero_texto'      => 'Casos reales con veredicto, pólizas explicadas sin letra pequeña y cartas listas para reclamar. Todo con fuentes oficiales y sin venderte nada.',
		'buscador_texto'  => 'Busca tu duda: gotera, franquicia, baja…',
		'busquedas'       => 'gotera del vecino, luna rota, baja médica, perro mordió',
		// Avisos.
		'barra_superior'  => 'Independientes: no vendemos seguros, no pedimos datos y no cobramos comisiones.',
		'aviso_articulo'  => 'Información general. Espabilao no vende seguros ni es mediador de seguros: no cobramos comisiones ni pedimos datos. Lo que cubre tu seguro depende de tu póliza concreta; revisa siempre tus condiciones generales y particulares.',
		'texto_pie'       => 'Información general sobre seguros en España. Espabilao no vende seguros ni es mediador. Consulta siempre tu póliza.',
		// Artículo.
		'mostrar_indice'  => true,
		'glosario_auto'   => true,
		'escalera_auto'   => true,
		'dgsfp_url'       => 'https://dgsfp.mineco.gob.es/es/Consumidor/Reclamaciones/Paginas/InformacionProcedimiento.aspx',
		// Publicidad.
		'ads_cliente'     => '',
		'ads_script'      => true,
		'ads_parrafo'     => 2,
		'ads_slot_parrafo' => '',
		'ads_slot_final'  => '',
		'ads_slot_portada' => '',
		'ads_slot_archivo' => '',
		'ads_paginas'     => false,
		'ads_altura'      => 280,
	);
}

/**
 * Lee una opción del tema con su valor por defecto.
 *
 * @param string $clave Opción.
 * @return mixed
 */
function espabilao_opcion( $clave ) {
	$defecto = espabilao_opciones_defecto();
	return get_theme_mod( 'esp_' . $clave, isset( $defecto[ $clave ] ) ? $defecto[ $clave ] : '' );
}

function espabilao_limpiar_bool( $v ) {
	return (bool) $v;
}

function espabilao_limpiar_cliente( $v ) {
	$v = trim( (string) $v );
	if ( preg_match( '/^(ca-)?pub-\d{10,20}$/', $v ) ) {
		return 0 === strpos( $v, 'ca-' ) ? $v : 'ca-' . $v;
	}
	return '';
}

function espabilao_limpiar_slot( $v ) {
	return preg_replace( '/\D/', '', (string) $v );
}

add_action( 'customize_register', function ( WP_Customize_Manager $c ) {
	$d = espabilao_opciones_defecto();

	$c->add_panel( 'espabilao', array(
		'title'    => 'Espabilao',
		'priority' => 30,
	) );

	$ajuste = function ( $clave, $tipo, $seccion, $etiqueta, $descripcion = '', $limpiar = 'sanitize_text_field', $extra = array() ) use ( $c, $d ) {
		$c->add_setting( 'esp_' . $clave, array(
			'default'           => $d[ $clave ],
			'sanitize_callback' => $limpiar,
			'transport'         => 'refresh',
		) );
		$c->add_control( 'esp_' . $clave, array_merge( array(
			'type'        => $tipo,
			'section'     => $seccion,
			'label'       => $etiqueta,
			'description' => $descripcion,
		), $extra ) );
	};

	// Publicidad.
	$c->add_section( 'esp_publicidad', array(
		'panel'       => 'espabilao',
		'title'       => 'Publicidad (AdSense)',
		'description' => 'Pega aquí tu ID de editor y los ID de bloque de anuncio de AdSense. Si un hueco no tiene ID, no se muestra. El aviso de cookies lo gestiona «Privacidad y mensajes» de AdSense.',
	) );
	$ajuste( 'ads_cliente', 'text', 'esp_publicidad', 'ID de editor', 'Formato: ca-pub- seguido de 16 cifras (lo encontrarás en AdSense > Cuenta)', 'espabilao_limpiar_cliente', array( 'input_attrs' => array( 'placeholder' => 'ca-pub-…' ) ) );
	$ajuste( 'ads_script', 'checkbox', 'esp_publicidad', 'Cargar el script de AdSense desde el tema', 'Desactívalo si ya lo carga otro plugin (por ejemplo, Site Kit) para no duplicarlo.', 'espabilao_limpiar_bool' );
	$ajuste( 'ads_slot_parrafo', 'text', 'esp_publicidad', 'Bloque dentro del artículo', 'ID del bloque (data-ad-slot) que se inserta tras el párrafo indicado abajo.', 'espabilao_limpiar_slot' );
	$ajuste( 'ads_parrafo', 'number', 'esp_publicidad', 'Insertar tras el párrafo n.º', '', 'absint', array( 'input_attrs' => array( 'min' => 1, 'max' => 10 ) ) );
	$ajuste( 'ads_slot_final', 'text', 'esp_publicidad', 'Bloque al final del artículo', '', 'espabilao_limpiar_slot' );
	$ajuste( 'ads_slot_portada', 'text', 'esp_publicidad', 'Bloque en la portada', 'Entre «Últimos casos» y «Tipos de seguro».', 'espabilao_limpiar_slot' );
	$ajuste( 'ads_slot_archivo', 'text', 'esp_publicidad', 'Bloque en categorías, secciones y búsqueda', 'Se muestra tras los primeros resultados.', 'espabilao_limpiar_slot' );
	$ajuste( 'ads_paginas', 'checkbox', 'esp_publicidad', 'Mostrar también en páginas estáticas', 'Por defecto los anuncios solo aparecen en artículos.', 'espabilao_limpiar_bool' );
	$ajuste( 'ads_altura', 'number', 'esp_publicidad', 'Altura reservada (px)', 'Reserva espacio para que el texto no salte al cargar el anuncio. Recomendado: 280.', 'absint', array( 'input_attrs' => array( 'min' => 0, 'max' => 600, 'step' => 10 ) ) );

	// Portada.
	$c->add_section( 'esp_portada', array( 'panel' => 'espabilao', 'title' => 'Portada' ) );
	$ajuste( 'hero_etiqueta', 'text', 'esp_portada', 'Etiqueta superior' );
	$ajuste( 'hero_titulo', 'text', 'esp_portada', 'Titular' );
	$ajuste( 'hero_destacado', 'text', 'esp_portada', 'Final del titular (resaltado)' );
	$ajuste( 'hero_texto', 'textarea', 'esp_portada', 'Entradilla', '', 'sanitize_textarea_field' );
	$ajuste( 'buscador_texto', 'text', 'esp_portada', 'Texto de ejemplo del buscador' );
	$ajuste( 'busquedas', 'text', 'esp_portada', 'Búsquedas sugeridas', 'Separadas por comas.' );

	// Avisos.
	$c->add_section( 'esp_avisos', array( 'panel' => 'espabilao', 'title' => 'Avisos y textos' ) );
	$ajuste( 'barra_superior', 'text', 'esp_avisos', 'Barra superior' );
	$ajuste( 'aviso_articulo', 'textarea', 'esp_avisos', 'Aviso al final de cada artículo', '', 'sanitize_textarea_field' );
	$ajuste( 'texto_pie', 'textarea', 'esp_avisos', 'Texto del pie', '', 'sanitize_textarea_field' );

	// Artículo.
	$c->add_section( 'esp_articulo', array( 'panel' => 'espabilao', 'title' => 'Artículos' ) );
	$ajuste( 'mostrar_indice', 'checkbox', 'esp_articulo', 'Índice automático', 'Se muestra cuando el artículo tiene 3 o más subtítulos (H2).', 'espabilao_limpiar_bool' );
	$ajuste( 'glosario_auto', 'checkbox', 'esp_articulo', 'Glosario emergente automático', 'Marca la primera aparición de cada término del glosario y muestra su definición al pulsar.', 'espabilao_limpiar_bool' );
	$ajuste( 'escalera_auto', 'checkbox', 'esp_articulo', 'Escalera de reclamación automática', 'Al final de los artículos de «¿Pagó o no pagó?» y «Qué hacer si…», salvo que ya la hayas insertado tú.', 'espabilao_limpiar_bool' );
	$ajuste( 'dgsfp_url', 'url', 'esp_articulo', 'Enlace a Reclamaciones de la DGSFP', 'Por si cambia la dirección oficial.', 'esc_url_raw' );
} );
