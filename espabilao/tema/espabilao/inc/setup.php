<?php
/**
 * Configuración básica, recursos y limpieza de la cabecera.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

add_action( 'after_setup_theme', function () {
	load_theme_textdomain( 'espabilao', ESPABILAO_DIR . '/languages' );

	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'automatic-feed-links' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'align-wide' );
	add_theme_support( 'editor-styles' );
	add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script', 'navigation-widgets' ) );
	add_theme_support( 'custom-logo', array( 'height' => 80, 'width' => 320, 'flex-height' => true, 'flex-width' => true ) );
	remove_theme_support( 'core-block-patterns' );

	add_editor_style( 'assets/css/editor.css' );

	add_image_size( 'espabilao-tarjeta', 640, 400, true );
	add_image_size( 'espabilao-mini', 240, 240, true );

	register_nav_menus( array(
		'principal' => __( 'Menú principal', 'espabilao' ),
		'pie'       => __( 'Menú del pie', 'espabilao' ),
	) );

	// Paleta del editor: la misma que el tema.
	add_theme_support( 'editor-color-palette', array(
		array( 'name' => 'Tinta', 'slug' => 'tinta', 'color' => '#1a1a1f' ),
		array( 'name' => 'Naranja Espabilao', 'slug' => 'naranja', 'color' => '#ff6a2b' ),
		array( 'name' => 'Crema', 'slug' => 'crema', 'color' => '#fff3ea' ),
		array( 'name' => 'Gris claro', 'slug' => 'gris-claro', 'color' => '#f5f3f0' ),
		array( 'name' => 'Blanco', 'slug' => 'blanco', 'color' => '#ffffff' ),
	) );
	add_theme_support( 'disable-custom-colors' );
} );

add_action( 'after_setup_theme', function () {
	$GLOBALS['content_width'] = 720;
}, 0 );

/**
 * Hojas de estilo y script (sin jQuery).
 */
add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'espabilao', ESPABILAO_URI . '/assets/css/espabilao.css', array(), ESPABILAO_VERSION );
	wp_enqueue_script( 'espabilao', ESPABILAO_URI . '/assets/js/espabilao.js', array(), ESPABILAO_VERSION, array( 'strategy' => 'defer', 'in_footer' => true ) );

	// Estilos de bloques solo cuando se usan.
	wp_dequeue_style( 'classic-theme-styles' );
} );
add_filter( 'should_load_separate_core_block_assets', '__return_true' );

/**
 * Precarga de las dos fuentes que se ven en la primera pantalla.
 */
add_action( 'wp_head', function () {
	foreach ( array( 'BricolageGrotesque-600_800.woff2', 'Figtree-400_700.woff2' ) as $fuente ) {
		printf( '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n", esc_url( ESPABILAO_URI . '/assets/fonts/' . $fuente ) );
	}
	echo '<meta name="theme-color" content="#ffffff">' . "\n";
}, 1 );

/**
 * Limpieza: emojis, embeds y enlaces innecesarios en la cabecera.
 */
add_action( 'init', function () {
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
	remove_action( 'admin_print_styles', 'print_emoji_styles' );
	remove_filter( 'the_content_feed', 'wp_staticize_emoji' );
	remove_filter( 'comment_text_rss', 'wp_staticize_emoji' );
	remove_filter( 'wp_mail', 'wp_staticize_emoji_for_email' );
	add_filter( 'emoji_svg_url', '__return_false' );
	remove_action( 'wp_head', 'wp_generator' );
	remove_action( 'wp_head', 'wlwmanifest_link' );
	remove_action( 'wp_head', 'rsd_link' );
	remove_action( 'wp_head', 'wp_shortlink_wp_head' );
	remove_action( 'wp_head', 'wp_oembed_add_host_js' );
} );

/**
 * El tema no genera schema ni JSON-LD: de eso se encarga Rank Math.
 * Los comentarios no se muestran en el tema (web sin formularios de usuario).
 */
add_filter( 'comments_open', '__return_false', 20 );
add_filter( 'pings_open', '__return_false', 20 );

/**
 * Extracto más corto y sin corchetes.
 */
add_filter( 'excerpt_length', function () {
	return 26;
} );
add_filter( 'excerpt_more', function () {
	return '…';
} );

/**
 * Clase para saber si hay JavaScript.
 */
add_action( 'wp_head', function () {
	echo "<script>document.documentElement.className=document.documentElement.className.replace('no-js','js');</script>\n";
}, 0 );
