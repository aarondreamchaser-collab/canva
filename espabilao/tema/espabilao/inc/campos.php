<?php
/**
 * Campos propios de cada artículo: respuesta rápida, veredicto,
 * fecha de revisión y fuentes. Y el cargo del autor.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Vías por las que se resolvió un caso.
 *
 * @return array<string, string>
 */
function espabilao_vias() {
	return array(
		'aseguradora' => 'La propia aseguradora',
		'sac'         => 'Servicio de Atención al Cliente',
		'dgsfp'       => 'Reclamación ante la DGSFP',
		'arbitraje'   => 'Arbitraje de consumo',
		'juzgado'     => 'Juzgado',
	);
}

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
		'_esp_reclamado' => 'string',
		'_esp_obtenido'  => 'string',
		'_esp_duracion'  => 'string',
		'_esp_via'       => 'string',
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
	$reclamado = get_post_meta( $post->ID, '_esp_reclamado', true );
	$obtenido  = get_post_meta( $post->ID, '_esp_obtenido', true );
	$duracion  = get_post_meta( $post->ID, '_esp_duracion', true );
	$via       = get_post_meta( $post->ID, '_esp_via', true );
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
		<fieldset style="border:1px solid #dcdcde;padding:10px 12px 0;margin:0 0 1.2em">
			<legend style="font-weight:600;padding:0 4px">Ficha del caso (opcional, solo casos)</legend>
			<p><label for="esp_reclamado">Importe reclamado (€)</label><input type="text" id="esp_reclamado" name="esp_reclamado" value="<?php echo esc_attr( $reclamado ); ?>" placeholder="2.300"></p>
			<p><label for="esp_obtenido">Importe obtenido (€)</label><input type="text" id="esp_obtenido" name="esp_obtenido" value="<?php echo esc_attr( $obtenido ); ?>" placeholder="2.300"></p>
			<p><label for="esp_duracion">Cuánto tardó</label><input type="text" id="esp_duracion" name="esp_duracion" value="<?php echo esc_attr( $duracion ); ?>" placeholder="3 semanas"></p>
			<p><label for="esp_via">Dónde se resolvió</label>
				<select id="esp_via" name="esp_via"><option value="">—</option>
					<?php foreach ( espabilao_vias() as $clave => $nombre ) : ?>
						<option value="<?php echo esc_attr( $clave ); ?>" <?php selected( $via, $clave ); ?>><?php echo esc_html( $nombre ); ?></option>
					<?php endforeach; ?>
				</select>
			</p>
		</fieldset>
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
	$reclamado = isset( $_POST['esp_reclamado'] ) ? sanitize_text_field( wp_unslash( $_POST['esp_reclamado'] ) ) : '';
	$obtenido  = isset( $_POST['esp_obtenido'] ) ? sanitize_text_field( wp_unslash( $_POST['esp_obtenido'] ) ) : '';
	$duracion  = isset( $_POST['esp_duracion'] ) ? sanitize_text_field( wp_unslash( $_POST['esp_duracion'] ) ) : '';
	$via       = isset( $_POST['esp_via'] ) ? sanitize_key( wp_unslash( $_POST['esp_via'] ) ) : '';
	if ( ! isset( espabilao_vias()[ $via ] ) ) {
		$via = '';
	}
	if ( $revision && ! preg_match( '/^\d{4}-\d{2}-\d{2}$/', $revision ) ) {
		$revision = '';
	}

	$valores = array(
		'_esp_respuesta' => $respuesta,
		'_esp_veredicto' => $veredicto,
		'_esp_revision'  => $revision,
		'_esp_fuentes'   => $fuentes,
		'_esp_reclamado' => $reclamado,
		'_esp_obtenido'  => $obtenido,
		'_esp_duracion'  => $duracion,
		'_esp_via'       => $via,
	);
	foreach ( $valores as $clave => $valor ) {
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
