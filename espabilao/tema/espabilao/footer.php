<?php
/**
 * Pie.
 *
 * @package Espabilao
 */
?>
</main>

<footer class="pie" role="contentinfo">
	<div class="envoltorio">
		<div class="pie__rejilla">
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
			</div>
			<nav class="pie__menu" aria-label="Menú del pie">
				<p class="supra">Espabilao</p>
				<?php
				wp_nav_menu( array(
					'theme_location' => 'pie',
					'container'      => false,
					'menu_class'     => 'menu',
					'depth'          => 1,
					'fallback_cb'    => 'espabilao_menu_defecto',
				) );
				?>
			</nav>
		</div>
		<p class="pie__legal">© <?php echo esc_html( wp_date( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?> · Información general, no asesoramiento personalizado.</p>
	</div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
