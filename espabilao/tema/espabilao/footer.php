<?php
/**
 * Pie: mapa del sitio, escalera rápida y sellos de confianza.
 *
 * @package Espabilao
 */
?>
</main>

<footer class="pie" role="contentinfo">
	<div class="envoltorio">
		<div class="pie__superior">
			<div class="pie__marca">
				<?php espabilao_logo( 'p', 'logo--claro' ); ?>
				<p class="pie__texto"><?php echo esc_html( espabilao_opcion( 'texto_pie' ) ); ?></p>
				<ul class="pie__sellos">
					<li><?php echo espabilao_icono( 'escudo', 18 ); // phpcs:ignore ?> No vendemos seguros</li>
					<li><?php echo espabilao_icono( 'no', 18 ); // phpcs:ignore ?> Sin formularios ni llamadas</li>
					<li><?php echo espabilao_icono( 'libro', 18 ); // phpcs:ignore ?> Fuentes oficiales: BOE y DGSFP</li>
				</ul>
			</div>
			<div class="pie__reclamar">
				<p class="supra">¿Te han rechazado un siniestro?</p>
				<ol class="pie__pasos">
					<li>Pide el «no» por escrito.</li>
					<li>Reclama a su Servicio de Atención al Cliente.</li>
					<li>Si en 1 mes no te responden, <a href="<?php echo esc_url( espabilao_opcion( 'dgsfp_url' ) ); ?>" target="_blank" rel="noopener">acude a la DGSFP</a>.</li>
				</ol>
				<?php $esp_u = espabilao_url_herramienta( 'calculadora-de-plazos' ); ?>
				<?php if ( $esp_u ) : ?>
					<a class="boton boton--naranja boton--peq" href="<?php echo esc_url( $esp_u ); ?>"><?php echo espabilao_icono( 'calendario', 18 ); // phpcs:ignore ?> Calcula tus plazos</a>
				<?php endif; ?>
			</div>
		</div>

		<div class="pie__mapa">
			<nav aria-label="Tipos de seguro">
				<p class="supra">Seguros</p>
				<ul>
					<?php foreach ( espabilao_categorias_ordenadas() as $esp_c ) : ?>
						<li><a href="<?php echo esc_url( get_term_link( $esp_c ) ); ?>"><?php echo esc_html( 'Seguro de ' . mb_strtolower( $esp_c->name ) ); ?></a></li>
					<?php endforeach; ?>
				</ul>
			</nav>
			<nav aria-label="Secciones">
				<p class="supra">Secciones</p>
				<?php espabilao_menu_defecto( array( 'menu_class' => '' ) ); ?>
			</nav>
			<nav aria-label="Herramientas">
				<p class="supra">Herramientas</p>
				<ul>
					<?php foreach ( espabilao_herramientas() as $esp_slug => $esp_h ) : ?>
						<?php $esp_u = espabilao_url_herramienta( $esp_slug ); ?>
						<?php if ( $esp_u ) : ?>
							<li><a href="<?php echo esc_url( $esp_u ); ?>"><?php echo esc_html( $esp_h['titulo'] ); ?></a></li>
						<?php endif; ?>
					<?php endforeach; ?>
				</ul>
			</nav>
			<nav aria-label="Espabilao">
				<p class="supra">Espabilao</p>
				<?php
				if ( has_nav_menu( 'pie' ) ) {
					wp_nav_menu( array(
						'theme_location' => 'pie',
						'container'      => false,
						'menu_class'     => '',
						'depth'          => 1,
					) );
				} else {
					echo '<ul>';
					wp_list_pages( array( 'title_li' => '', 'depth' => 1, 'exclude' => implode( ',', array_map( 'intval', (array) get_option( 'espabilao_paginas_herramientas', array() ) ) ) ) );
					echo '</ul>';
				}
				?>
			</nav>
		</div>

		<p class="pie__legal">© <?php echo esc_html( wp_date( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?> · Información general, no asesoramiento personalizado.</p>
	</div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
