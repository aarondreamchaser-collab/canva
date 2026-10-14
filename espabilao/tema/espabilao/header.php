<?php
/**
 * Cabecera.
 *
 * @package Espabilao
 */
?><!doctype html>
<html <?php language_attributes(); ?> class="no-js">
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="saltar" href="#contenido">Saltar al contenido</a>

<header class="cabecera-sitio" role="banner">
<div class="barra">
	<div class="envoltorio barra__dentro">
		<span class="barra__fecha"><?php echo esc_html( wp_date( 'l, j \d\e F \d\e Y' ) ); ?></span>
		<?php if ( espabilao_opcion( 'barra_superior' ) ) : ?>
			<span class="barra__aviso"><?php echo esc_html( espabilao_opcion( 'barra_superior' ) ); ?></span>
		<?php endif; ?>
	</div>
</div>

<div class="cabecera">
	<div class="envoltorio">
		<?php espabilao_logo( is_front_page() ? 'h1' : 'p' ); ?>
		<?php if ( get_bloginfo( 'description' ) ) : ?>
			<p class="lema"><?php bloginfo( 'description' ); ?></p>
		<?php endif; ?>
	</div>
</div>
</header>

<nav class="menu-principal" aria-label="Menú principal">
	<div class="envoltorio menu-principal__dentro">
		<?php
		wp_nav_menu( array(
			'theme_location' => 'principal',
			'container'      => false,
			'menu_class'     => 'menu',
			'depth'          => 2,
			'fallback_cb'    => 'espabilao_menu_defecto',
		) );
		?>
		<a class="menu-principal__buscar" href="<?php echo esc_url( home_url( '/?s=' ) ); ?>" aria-label="Buscar en Espabilao">
			<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
		</a>
	</div>
</nav>

<main id="contenido" class="principal">
