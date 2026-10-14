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
	<?php if ( espabilao_opcion( 'barra_superior' ) ) : ?>
		<div class="confianza">
			<div class="envoltorio confianza__dentro">
				<?php echo espabilao_icono( 'escudo', 16 ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
				<span><?php echo esc_html( espabilao_opcion( 'barra_superior' ) ); ?></span>
			</div>
		</div>
	<?php endif; ?>

	<div class="cabecera">
		<div class="envoltorio cabecera__dentro">
			<?php espabilao_logo( is_front_page() ? 'h1' : 'p' ); ?>

			<nav class="menu-principal" aria-label="Menú principal">
				<?php
				wp_nav_menu( array(
					'theme_location' => 'principal',
					'container'      => false,
					'menu_class'     => 'menu',
					'depth'          => 2,
					'fallback_cb'    => 'espabilao_menu_defecto',
				) );
				?>
			</nav>

			<div class="cabecera__acciones">
				<details class="desplegable desplegable--buscar">
					<summary class="boton-icono" aria-label="Buscar"><?php echo espabilao_icono( 'buscar', 22 ); // phpcs:ignore ?></summary>
					<div class="desplegable__panel">
						<?php get_search_form(); ?>
					</div>
				</details>
				<details class="desplegable desplegable--menu">
					<summary class="boton-icono" aria-label="Abrir menú"><?php echo espabilao_icono( 'menu', 22 ); // phpcs:ignore ?></summary>
					<div class="desplegable__panel menu-movil">
						<p class="supra">Secciones</p>
						<?php espabilao_menu_defecto( array( 'menu_class' => 'menu-movil__lista' ) ); ?>
						<p class="supra">Tipos de seguro</p>
						<?php espabilao_tipos( 'lista' ); ?>
					</div>
				</details>
			</div>
		</div>
	</div>
</header>

<main id="contenido" class="principal">
