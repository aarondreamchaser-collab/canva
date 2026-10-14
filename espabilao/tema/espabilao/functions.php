<?php
/**
 * Espabilao: funciones del tema.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

define( 'ESPABILAO_VERSION', '1.0.0' );
define( 'ESPABILAO_DIR', get_template_directory() );
define( 'ESPABILAO_URI', get_template_directory_uri() );

require ESPABILAO_DIR . '/inc/setup.php';
require ESPABILAO_DIR . '/inc/taxonomias.php';
require ESPABILAO_DIR . '/inc/campos.php';
require ESPABILAO_DIR . '/inc/activacion.php';
require ESPABILAO_DIR . '/inc/personalizar.php';
require ESPABILAO_DIR . '/inc/publicidad.php';
require ESPABILAO_DIR . '/inc/plantillas.php';
require ESPABILAO_DIR . '/inc/bloques.php';
require ESPABILAO_DIR . '/inc/glosario.php';
require ESPABILAO_DIR . '/inc/contenido.php';
