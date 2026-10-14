<?php
/**
 * Caja de autor.
 *
 * @package Espabilao
 */

$esp_autor = (int) get_the_author_meta( 'ID' );
$esp_bio   = get_the_author_meta( 'description', $esp_autor );
$esp_cargo = get_user_meta( $esp_autor, 'esp_cargo', true );
?>
<section class="autor" aria-label="Sobre el autor">
	<div class="autor__foto"><?php echo get_avatar( $esp_autor, 96, '', '', array( 'loading' => 'lazy' ) ); ?></div>
	<div class="autor__texto">
		<p class="supra">Escrito y revisado por</p>
		<p class="autor__nombre"><a href="<?php echo esc_url( get_author_posts_url( $esp_autor ) ); ?>"><?php echo esc_html( get_the_author_meta( 'display_name', $esp_autor ) ); ?></a></p>
		<?php if ( $esp_cargo ) : ?>
			<p class="autor__cargo"><?php echo esc_html( $esp_cargo ); ?></p>
		<?php endif; ?>
		<?php if ( $esp_bio ) : ?>
			<p class="autor__bio"><?php echo esc_html( $esp_bio ); ?></p>
		<?php endif; ?>
	</div>
</section>
