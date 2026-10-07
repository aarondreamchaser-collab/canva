<?php
// Simula lo mínimo de WordPress para ejecutar la plantilla y capturar lo que imprime cada gancho.
$CTX = json_decode( file_get_contents( $argv[1] ), true );
$GLOBALS['H'] = array();
function add_action( $h, $f, $p = 10, $n = 1 ) { $GLOBALS['H'][ $h ][ $p ][] = $f; }
function add_filter( $h, $f, $p = 10, $n = 1 ) { add_action( $h, $f, $p, $n ); }
function add_shortcode( $t, $f ) { $GLOBALS['SC'][ $t ] = $f; }
function correr( $h, $args = array() ) { ob_start(); $r = null; if ( isset( $GLOBALS['H'][ $h ] ) ) { ksort( $GLOBALS['H'][ $h ] ); foreach ( $GLOBALS['H'][ $h ] as $fs ) foreach ( $fs as $f ) { $r = call_user_func_array( $f, $args ); if ( $args ) $args[0] = $r; } } return array( ob_get_clean(), $r ); }
function c( $k ) { global $CTX; return $CTX[ $k ] ?? null; }
function is_single() { return c( 'tipo' ) === 'post'; }
function is_singular( $t = '' ) { return c( 'tipo' ) === 'post'; }
function is_archive() { return c( 'tipo' ) === 'cat'; }
function is_category() { return c( 'tipo' ) === 'cat'; }
function is_search() { return false; }
function is_home() { return false; }
function is_page( $s = '' ) { return c( 'tipo' ) === 'page' && c( 'slug' ) === $s; }
function in_the_loop() { return true; }
function is_main_query() { return true; }
function get_the_ID() { return c( 'id' ); }
function get_post_field( $f, $id ) { return array( 'post_content' => c( 'contenido' ), 'post_excerpt' => c( 'extracto' ), 'post_author' => 1 )[ $f ]; }
function wp_strip_all_tags( $s ) { return trim( strip_tags( preg_replace( '@<(script|style)[^>]*?>.*?</\\1>@si', '', $s ) ) ); }
function esc_html( $s ) { return htmlspecialchars( $s, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( $s, ENT_QUOTES ); }
function esc_url( $s ) { return $s; }
function home_url( $p = '' ) { return 'https://tuluzencasa.com' . $p; }
function get_terms( $a ) { $o = array(); foreach ( c( 'cats' ) as $x ) { $o[] = (object) $x; } usort( $o, function ( $a, $b ) { return $b->count - $a->count; } ); return $o; }
function is_wp_error( $x ) { return false; }
function get_category_link( $c ) { return 'https://tuluzencasa.com/' . $c->slug . '/'; }
function wp_date( $f ) { return '2026'; }
function _n( $s, $p, $n ) { return $n == 1 ? $s : $p; }
function get_queried_object() { return (object) c( 'cat' ); }
function function_exists_rm() {}
function get_the_author_meta( $f, $id ) { return $f === 'display_name' ? 'Aaron' : ''; }
function wp_get_post_categories( $id ) { return array(); }
function get_posts( $a ) { return array(); }
function wp_list_pluck( $a, $k ) { return array(); }
require $argv[2];
$out = array();
foreach ( array( 'generate_after_entry_title', 'generate_before_right_sidebar_content', 'generate_before_footer', 'generate_after_archive_description' ) as $h ) { $out[ $h ] = correr( $h )[0]; }
$out['sidebar'] = correr( 'generate_sidebar_layout', array( 'right-sidebar' ) )[1];
echo json_encode( $out );
