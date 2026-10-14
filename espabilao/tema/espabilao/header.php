<?php
/**
 * Cabecera con megamenú de tipos de seguro.
 *
 * @package Espabilao
 */

$esp_url_herr = espabilao_url_herramientas();
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
<div class="progreso" aria-hidden="true"><span></span></div>

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
				<ul class="menu">
					<li class="mega">
						<button type="button" class="mega__boton" aria-expanded="false" aria-controls="mega-seguros">Seguros <?php echo espabilao_icono( 'abajo', 16 ); // phpcs:ignore ?></button>
						<div class="mega__panel" id="mega-seguros">
							<div class="mega__rejilla">
								<ul class="mega__tipos">
									<?php foreach ( espabilao_categorias_ordenadas() as $esp_c ) : ?>
										<li><a href="<?php echo esc_url( get_term_link( $esp_c ) ); ?>">
											<span class="mega__icono"><?php echo espabilao_icono( $esp_c->slug, 24 ); // phpcs:ignore ?></span>
											<span><strong><?php echo esc_html( 'Seguro de ' . mb_strtolower( $esp_c->name ) ); ?></strong><small><?php echo esc_html( espabilao_lema_tipo( $esp_c->slug ) ); ?></small></span>
										</a></li>
									<?php endforeach; ?>
								</ul>
								<div class="mega__lateral">
									<p class="supra">Herramientas gratis</p>
									<ul class="mega__herr">
										<?php foreach ( espabilao_herramientas() as $esp_slug => $esp_h ) : ?>
											<?php $esp_u = espabilao_url_herramienta( $esp_slug ); ?>
											<?php if ( $esp_u ) : ?>
												<li><a href="<?php echo esc_url( $esp_u ); ?>"><?php echo espabilao_icono( $esp_h['icono'], 20 ); // phpcs:ignore ?> <?php echo esc_html( $esp_h['titulo'] ); ?></a></li>
											<?php endif; ?>
										<?php endforeach; ?>
									</ul>
									<p class="mega__nota"><?php echo espabilao_icono( 'escudo', 16 ); // phpcs:ignore ?> Sin formularios: todo funciona en tu navegador.</p>
								</div>
							</div>
						</div>
					</li>
					<?php echo espabilao_items_secciones(); // phpcs:ignore WordPress.Security.EscapeOutput ?>
					<?php if ( $esp_url_herr ) : ?>
						<li class="menu__destacado<?php echo espabilao_es_herramienta() ? ' current-menu-item' : ''; ?>"><a href="<?php echo esc_url( $esp_url_herr ); ?>"><?php echo espabilao_icono( 'chispa', 16 ); // phpcs:ignore ?> Herramientas</a></li>
					<?php endif; ?>
				</ul>
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
						<?php if ( $esp_url_herr ) : ?>
							<p class="supra">Herramientas gratis</p>
							<ul class="menu-movil__herr">
								<?php foreach ( espabilao_herramientas() as $esp_slug => $esp_h ) : ?>
									<?php $esp_u = espabilao_url_herramienta( $esp_slug ); ?>
									<?php if ( $esp_u ) : ?>
										<li><a href="<?php echo esc_url( $esp_u ); ?>"><?php echo espabilao_icono( $esp_h['icono'], 20 ); // phpcs:ignore ?> <?php echo esc_html( $esp_h['titulo'] ); ?></a></li>
									<?php endif; ?>
								<?php endforeach; ?>
							</ul>
						<?php endif; ?>
						<p class="supra">Tipos de seguro</p>
						<?php espabilao_tipos( 'lista' ); ?>
					</div>
				</details>
			</div>
		</div>
	</div>
</header>

<main id="contenido" class="principal">
