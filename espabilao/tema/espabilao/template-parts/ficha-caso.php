<?php
/**
 * Ficha del caso: veredicto, importes, duración y vía de resolución.
 *
 * @package Espabilao
 */

$esp_id        = get_the_ID();
$esp_veredicto = get_post_meta( $esp_id, '_esp_veredicto', true );
$esp_reclamado = get_post_meta( $esp_id, '_esp_reclamado', true );
$esp_obtenido  = get_post_meta( $esp_id, '_esp_obtenido', true );
$esp_duracion  = get_post_meta( $esp_id, '_esp_duracion', true );
$esp_via       = get_post_meta( $esp_id, '_esp_via', true );
$esp_vias      = espabilao_vias();

if ( ! $esp_veredicto && ! $esp_reclamado && ! $esp_obtenido && ! $esp_duracion && ! $esp_via ) {
	return;
}
?>
<dl class="ficha-caso">
	<?php if ( $esp_veredicto ) : ?>
		<div class="ficha-caso__dato ficha-caso__dato--veredicto"><dt>Veredicto</dt><dd><?php echo espabilao_sello( $esp_id, 'veredicto--grande' ); // phpcs:ignore WordPress.Security.EscapeOutput ?></dd></div>
	<?php endif; ?>
	<?php if ( $esp_reclamado ) : ?>
		<div class="ficha-caso__dato"><dt>Reclamado</dt><dd><?php echo esc_html( $esp_reclamado ); ?> €</dd></div>
	<?php endif; ?>
	<?php if ( $esp_obtenido ) : ?>
		<div class="ficha-caso__dato"><dt>Obtenido</dt><dd><?php echo esc_html( $esp_obtenido ); ?> €</dd></div>
	<?php endif; ?>
	<?php if ( $esp_duracion ) : ?>
		<div class="ficha-caso__dato"><dt>Tardó</dt><dd><?php echo esc_html( $esp_duracion ); ?></dd></div>
	<?php endif; ?>
	<?php if ( $esp_via && isset( $esp_vias[ $esp_via ] ) ) : ?>
		<div class="ficha-caso__dato"><dt>Se resolvió en</dt><dd><?php echo esc_html( $esp_vias[ $esp_via ] ); ?></dd></div>
	<?php endif; ?>
</dl>
