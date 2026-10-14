<?php
/**
 * Campos propios de cada artículo: respuesta rápida, veredicto,
 * fecha de revisión y fuentes. Y el cargo del autor.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Veredictos posibles.
 *
 * @return array<string, string>
 */
function espabilao_veredictos() {
	return array(
		'pago'     => 'Pagó',
		'no-pago'  => 'No pagó',
		'a-medias' => 'A medias',
	);
}

add_action( 'init', function () {
	$campos = array(
		'_esp_respuesta' => 'string',
		'_esp_veredicto' => 'string',
		'_esp_revision'  => 'string',
		'_esp_fuentes'   => 'string',
	);
	foreach ( $campos as $clave => $tipo ) {
		register_post_meta( 'post', $clave, array(
			'type'          => $tipo,
			'single'        => true,
			'show_in_rest'  => true,
			'auth_callback' => function () {
				return current_user_can( 'edit_posts' );
			},
		) );
	}
} );

add_action( 'add_meta_boxes', function () {
	add_meta_box( 'espabilao-ficha', 'Ficha Espabilao', 'espabilao_caja_ficha', 'post', 'normal', 'high' );
} );

/**
 * Caja de campos en el editor.
 *
 * @param WP_Post $post Entrada.
 */
function espabilao_caja_ficha( $post ) {
	wp_nonce_field( 'espabilao_ficha', 'espabilao_ficha_nonce' );
	$respuesta = get_post_meta( $post->ID, '_esp_respuesta', true );
	$veredicto = get_post_meta( $post->ID, '_esp_veredicto', true );
	$revision  = get_post_meta( $post->ID, '_esp_revision', true );
	$fuentes   = get_post_meta( $post->ID, '_esp_fuentes', true );
	?>
	<style>
		.esp-ficha p{margin:0 0 1.2em}.esp-ficha label{display:block;font-weight:600;margin-bottom:4px}
		.esp-ficha textarea,.esp-ficha input[type=date],.esp-ficha select{width:100%;max-width:100%}
		.esp-ficha .description{color:#646970;font-size:12px;margin-top:4px}
	</style>
	<div class="esp-ficha">
		<p>
			<label for="esp_respuesta">Respuesta rápida</label>
			<textarea id="esp_respuesta" name="esp_respuesta" rows="3"><?php echo esc_textarea( $respuesta ); ?></textarea>
			<span class="description">Dos o tres frases que respondan a la pregunta del titular. Aparece arriba del artículo, en un recuadro.</span>
		</p>
		<p>
			<label for="esp_veredicto">Veredicto (para casos de «¿Pagó o no pagó?»)</label>
			<select id="esp_veredicto" name="esp_veredicto">
				<option value="">— Sin veredicto —</option>
				<?php foreach ( espabilao_veredictos() as $clave => $nombre ) : ?>
					<option value="<?php echo esc_attr( $clave ); ?>" <?php selected( $veredicto, $clave ); ?>><?php echo esc_html( $nombre ); ?></option>
				<?php endforeach; ?>
			</select>
		</p>
		<p>
			<label for="esp_revision">Fecha de revisión</label>
			<input type="date" id="esp_revision" name="esp_revision" value="<?php echo esc_attr( $revision ); ?>">
			<span class="description">Último día en que comprobaste que la información sigue vigente. Si la dejas vacía se usa la fecha de última modificación.</span>
		</p>
		<p>
			<label for="esp_fuentes">Fuentes</label>
			<textarea id="esp_fuentes" name="esp_fuentes" rows="5" placeholder="Ley 50/1980 de Contrato de Seguro, art. 16 | https://www.boe.es/buscar/act.php?id=BOE-A-1980-22501#adieciseis"><?php echo esc_textarea( $fuentes ); ?></textarea>
			<span class="description">Una fuente por línea, con el formato <code>Nombre de la fuente | https://enlace</code>. El enlace es opcional.</span>
		</p>
	</div>
	<?php
}

add_action( 'save_post_post', function ( $post_id ) {
	if ( ! isset( $_POST['espabilao_ficha_nonce'] ) || ! wp_verify_nonce( sanitize_key( $_POST['espabilao_ficha_nonce'] ), 'espabilao_ficha' ) ) {
		return;
	}
	if ( ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) || ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	$respuesta = isset( $_POST['esp_respuesta'] ) ? sanitize_textarea_field( wp_unslash( $_POST['esp_respuesta'] ) ) : '';
	$veredicto = isset( $_POST['esp_veredicto'] ) ? sanitize_key( wp_unslash( $_POST['esp_veredicto'] ) ) : '';
	$revision  = isset( $_POST['esp_revision'] ) ? sanitize_text_field( wp_unslash( $_POST['esp_revision'] ) ) : '';
	$fuentes   = isset( $_POST['esp_fuentes'] ) ? sanitize_textarea_field( wp_unslash( $_POST['esp_fuentes'] ) ) : '';

	if ( ! isset( espabilao_veredictos()[ $veredicto ] ) ) {
		$veredicto = '';
	}
	if ( $revision && ! preg_match( '/^\d{4}-\d{2}-\d{2}$/', $revision ) ) {
		$revision = '';
	}

	foreach ( array( '_esp_respuesta' => $respuesta, '_esp_veredicto' => $veredicto, '_esp_revision' => $revision, '_esp_fuentes' => $fuentes ) as $clave => $valor ) {
		if ( '' === $valor ) {
			delete_post_meta( $post_id, $clave );
		} else {
			update_post_meta( $post_id, $clave, $valor );
		}
	}
} );

/**
 * Fuentes de un artículo como lista de [texto, url].
 *
 * @param int $post_id Entrada.
 * @return array<int, array{0:string, 1:string}>
 */
function espabilao_fuentes( $post_id ) {
	$lineas = preg_split( '/\R/', (string) get_post_meta( $post_id, '_esp_fuentes', true ) );
	$salida = array();
	foreach ( $lineas as $linea ) {
		$linea = trim( $linea );
		if ( '' === $linea ) {
			continue;
		}
		$partes = array_map( 'trim', explode( '|', $linea, 2 ) );
		$url    = isset( $partes[1] ) ? esc_url_raw( $partes[1] ) : '';
		if ( ! $url && preg_match( '#^https?://\S+$#', $partes[0] ) ) {
			$url = esc_url_raw( $partes[0] );
		}
		$salida[] = array( $partes[0], $url );
	}
	return $salida;
}

/**
 * Fecha de revisión (Y-m-d) del artículo.
 *
 * @param int $post_id Entrada.
 * @return string Marca de tiempo UNIX.
 */
function espabilao_fecha_revision( $post_id ) {
	$revision = get_post_meta( $post_id, '_esp_revision', true );
	if ( $revision ) {
		return (string) strtotime( $revision . ' 12:00:00' );
	}
	return (string) get_post_modified_time( 'U', false, $post_id );
}

/**
 * Cargo o especialidad del autor (perfil de usuario).
 */
function espabilao_campo_cargo( $user ) {
	?>
	<h2>Espabilao</h2>
	<table class="form-table" role="presentation">
		<tr>
			<th><label for="esp_cargo">Cargo o especialidad</label></th>
			<td>
				<input type="text" name="esp_cargo" id="esp_cargo" class="regular-text" value="<?php echo esc_attr( get_user_meta( $user->ID, 'esp_cargo', true ) ); ?>">
				<p class="description">Se muestra junto a tu nombre en los artículos. Ej.: «Periodista especializado en seguros». La biografía se toma del campo «Información biográfica».</p>
			</td>
		</tr>
	</table>
	<?php
}
add_action( 'show_user_profile', 'espabilao_campo_cargo' );
add_action( 'edit_user_profile', 'espabilao_campo_cargo' );

function espabilao_guardar_cargo( $user_id ) {
	if ( ! current_user_can( 'edit_user', $user_id ) || ! isset( $_POST['esp_cargo'] ) ) {
		return;
	}
	check_admin_referer( 'update-user_' . $user_id );
	update_user_meta( $user_id, 'esp_cargo', sanitize_text_field( wp_unslash( $_POST['esp_cargo'] ) ) );
}
add_action( 'personal_options_update', 'espabilao_guardar_cargo' );
add_action( 'edit_user_profile_update', 'espabilao_guardar_cargo' );
