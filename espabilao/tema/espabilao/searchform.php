<?php
/**
 * Buscador.
 *
 * @package Espabilao
 */
$esp_id = wp_unique_id( 'buscar-' );
?>
<form role="search" method="get" class="buscador" action="<?php echo esc_url( home_url( '/' ) ); ?>">
	<label class="screen-reader-text" for="<?php echo esc_attr( $esp_id ); ?>">Buscar en Espabilao</label>
	<input type="search" id="<?php echo esc_attr( $esp_id ); ?>" class="buscador__campo" name="s" value="<?php echo esc_attr( get_search_query() ); ?>" placeholder="<?php echo esc_attr( espabilao_opcion( 'buscador_texto' ) ); ?>" autocomplete="off">
	<button type="submit" class="buscador__boton">Buscar</button>
</form>
