<?php
/**
 * Iconos SVG en línea (sin peticiones extra). Trazo: currentColor.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Devuelve un icono SVG.
 *
 * @param string $nombre Nombre del icono (o slug de tipo de seguro).
 * @param int    $tam    Tamaño en px.
 * @return string
 */
function espabilao_icono( $nombre, $tam = 24 ) {
	$i = array(
		'hogar'     => '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 9.8V20h13V9.8"/><path d="M10 20v-5.5h4V20"/>',
		'coche'     => '<path d="M4 14.5 5.8 9.6A2 2 0 0 1 7.7 8.3h8.6a2 2 0 0 1 1.9 1.3l1.8 4.9"/><rect x="3" y="14.5" width="18" height="3.8" rx="1.2"/><circle cx="7.5" cy="18.6" r="1.6"/><circle cx="16.5" cy="18.6" r="1.6"/>',
		'moto'      => '<circle cx="5.5" cy="16.5" r="3"/><circle cx="18.5" cy="16.5" r="3"/><path d="M5.5 16.5 9.2 10h5l4.3 6.5"/><path d="M14.2 10 12.8 7H10.5"/><path d="M9.2 10l3 6.5h1.6"/>',
		'salud'     => '<rect x="4" y="4" width="16" height="16" rx="4.5"/><path d="M12 8.3v7.4M8.3 12h7.4"/>',
		'vida'      => '<path d="M12 20s-7.5-4.6-7.5-10.2A4.1 4.1 0 0 1 12 7.4a4.1 4.1 0 0 1 7.5 2.4C19.5 15.4 12 20 12 20z"/>',
		'decesos'   => '<rect x="8.5" y="10.5" width="7" height="9.5" rx="1.2"/><path d="M12 3.8c1.7 1.9 1.7 3.6 0 5-1.7-1.4-1.7-3.1 0-5z"/><path d="M6 20h12"/>',
		'mascotas'  => '<circle cx="8.3" cy="7.6" r="1.7"/><circle cx="15.7" cy="7.6" r="1.7"/><circle cx="5" cy="12.2" r="1.5"/><circle cx="19" cy="12.2" r="1.5"/><path d="M12 11.6c-2.9 0-5 3.4-5 5.4 0 1.5 1.1 2.3 2.4 2.3 1 0 1.6-.6 2.6-.6s1.6.6 2.6.6c1.3 0 2.4-.8 2.4-2.3 0-2-2.1-5.4-5-5.4z"/>',
		'viaje'     => '<rect x="4" y="8" width="16" height="12" rx="2.2"/><path d="M9 8V5.6c0-.6.4-1 1-1h4c.6 0 1 .4 1 1V8"/><path d="M8 8v12M16 8v12"/>',
		'alquiler'  => '<circle cx="8" cy="15.5" r="4"/><path d="M10.9 12.6 19 4.5M15.8 7.7l2.3 2.3M13.6 9.9l1.8 1.8"/>',
		'autonomos' => '<rect x="3.5" y="7.5" width="17" height="12" rx="2.2"/><path d="M9 7.5V5.4c0-.5.4-.9.9-.9h4.2c.5 0 .9.4.9.9v2.1"/><path d="M3.5 12.8h17"/><path d="M11 12.8v1.7h2v-1.7"/>',
		'buscar'    => '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/>',
		'si'        => '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
		'no'        => '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>',
		'medias'    => '<circle cx="12" cy="12" r="7.5"/><path d="M12 4.5v15" /><path d="M12 4.5a7.5 7.5 0 0 1 0 15z" fill="currentColor"/>',
		'escudo'    => '<path d="M12 3.5 19 6v5.6c0 4.3-2.9 7.6-7 8.9-4.1-1.3-7-4.6-7-8.9V6z"/><path d="m8.8 12 2.2 2.2 4.3-4.4"/>',
		'libro'     => '<path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H11v16H5.5A1.5 1.5 0 0 1 4 18.5z"/><path d="M20 5.5A1.5 1.5 0 0 0 18.5 4H13v16h5.5a1.5 1.5 0 0 0 1.5-1.5z"/>',
		'reloj'     => '<circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3 2"/>',
		'flecha'    => '<path d="M5 12h14M13 6l6 6-6 6"/>',
		'menu'      => '<path d="M4 7h16M4 12h16M4 17h16"/>',
		'doc'       => '<path d="M7 3.5h7l4 4V20a.5.5 0 0 1-.5.5h-10A.5.5 0 0 1 7 20z" transform="translate(-1 0)"/><path d="M13 3.5v4h4" transform="translate(-1 0)"/><path d="M9 12h6M9 15.5h6"/>',
		'alerta'    => '<path d="M12 4 21 19.5H3z"/><path d="M12 10v4.2M12 17h.01"/>',
		'copiar'    => '<rect x="8.5" y="8.5" width="11" height="11" rx="2"/><path d="M15.5 8.5V6a1.5 1.5 0 0 0-1.5-1.5H6A1.5 1.5 0 0 0 4.5 6v8A1.5 1.5 0 0 0 6 15.5h2.5"/>',
		'escalera'  => '<path d="M4 19.5h5v-5h5v-5h6"/><path d="M17 6.5 20 9.5 17 12.5" />',
		'lupa-doc'  => '<path d="M6 3.5h7l4 4V11"/><path d="M13 3.5v4h4"/><path d="M6 3.5v16h5"/><circle cx="16" cy="16" r="3.2"/><path d="m18.4 18.4 2.3 2.3"/>',
		'bombilla'  => '<path d="M9 17.5h6M9.8 20.5h4.4"/><path d="M12 3.5a5.5 5.5 0 0 0-3.3 9.9c.7.5 1.1 1.3 1.1 2.1v.5h4.4v-.5c0-.8.4-1.6 1.1-2.1A5.5 5.5 0 0 0 12 3.5z"/>',
		'carta'     => '<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/>',
	);
	$tam = absint( $tam );
	if ( ! isset( $i[ $nombre ] ) ) {
		$nombre = 'doc';
	}
	return '<svg class="icono icono--' . esc_attr( $nombre ) . '" width="' . $tam . '" height="' . $tam . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . $i[ $nombre ] . '</svg>';
}

/**
 * Icono de cada sección de la marca.
 *
 * @param string $slug Slug de la sección.
 * @return string
 */
function espabilao_icono_seccion( $slug ) {
	$mapa = array(
		'pago-o-no-pago'      => 'escudo',
		'polizas-al-desnudo'  => 'lupa-doc',
		'que-hacer-si'        => 'escalera',
		'trucos-de-espabilao' => 'bombilla',
	);
	return espabilao_icono( isset( $mapa[ $slug ] ) ? $mapa[ $slug ] : 'doc', 28 );
}
