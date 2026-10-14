<?php
/**
 * Herramientas gratuitas: calculadora de plazos, calculadora de infraseguro,
 * generador de cartas y detector de letra pequeña. Todo funciona en el
 * navegador del lector: no se envía ni se guarda ningún dato.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

/**
 * Catálogo de herramientas.
 *
 * @return array<string, array<string, string>>
 */
function espabilao_herramientas() {
	return array(
		'calculadora-de-plazos'      => array(
			'titulo'    => 'Calculadora de plazos',
			'corto'     => '¿Estoy a tiempo?',
			'texto'     => 'Pon la fecha de tu siniestro, de tu reclamación o del vencimiento y te decimos cada plazo legal, con aviso en tu calendario.',
			'icono'     => 'calendario',
			'shortcode' => 'calculadora_plazos',
		),
		'generador-de-cartas'        => array(
			'titulo'    => 'Generador de cartas',
			'corto'     => 'Carta lista en 2 minutos',
			'texto'     => 'Reclamación, oposición a la renovación, petición del rechazo por escrito o de intereses de demora. Rellenas, copias y envías.',
			'icono'     => 'carta',
			'shortcode' => 'generador_carta',
		),
		'detector-de-letra-pequena'  => array(
			'titulo'    => 'Detector de letra pequeña',
			'corto'     => 'Pega tu póliza',
			'texto'     => 'Pega una cláusula o tus condiciones y te marcamos exclusiones, límites, franquicias y trampas, explicadas en cristiano.',
			'icono'     => 'lupa-doc',
			'shortcode' => 'detector_letra_pequena',
		),
		'calculadora-de-infraseguro' => array(
			'titulo'    => 'Calculadora de infraseguro',
			'corto'     => '¿Cuánto te pagarían?',
			'texto'     => 'Si aseguraste tu casa por menos de lo que vale, te pagan en proporción. Calcula cuánto perderías en un siniestro.',
			'icono'     => 'calculadora',
			'shortcode' => 'calculadora_infraseguro',
		),
	);
}

/**
 * URL de una herramienta (su página) o cadena vacía.
 *
 * @param string $slug Slug de la herramienta.
 * @return string
 */
function espabilao_url_herramienta( $slug ) {
	$ids = (array) get_option( 'espabilao_paginas_herramientas', array() );
	if ( ! empty( $ids[ $slug ] ) && 'publish' === get_post_status( $ids[ $slug ] ) ) {
		return (string) get_permalink( $ids[ $slug ] );
	}
	return '';
}

/**
 * URL de la página «Herramientas».
 *
 * @return string
 */
function espabilao_url_herramientas() {
	$ids = (array) get_option( 'espabilao_paginas_herramientas', array() );
	return ( ! empty( $ids['_padre'] ) && 'publish' === get_post_status( $ids['_padre'] ) ) ? (string) get_permalink( $ids['_padre'] ) : '';
}

/**
 * ¿Estamos en la página de herramientas o en una de sus hijas?
 *
 * @return bool
 */
function espabilao_es_herramienta() {
	if ( ! is_page() ) {
		return false;
	}
	$ids = (array) get_option( 'espabilao_paginas_herramientas', array() );
	$id  = (int) get_queried_object_id();
	return in_array( $id, array_map( 'intval', $ids ), true );
}

add_filter( 'body_class', function ( $clases ) {
	if ( espabilao_es_herramienta() ) {
		$clases[] = 'es-herramienta';
	}
	return $clases;
} );

/**
 * Crea las páginas de herramientas si no existen (una sola vez).
 */
function espabilao_crear_paginas_herramientas() {
	$ids = (array) get_option( 'espabilao_paginas_herramientas', array() );

	if ( empty( $ids['_padre'] ) || ! get_post( $ids['_padre'] ) ) {
		$existente = get_page_by_path( 'herramientas' );
		$ids['_padre'] = $existente ? $existente->ID : wp_insert_post( array(
			'post_type'    => 'page',
			'post_status'  => 'publish',
			'post_title'   => 'Herramientas',
			'post_name'    => 'herramientas',
			'post_excerpt' => 'Calculadoras y generadores gratuitos para defenderte frente a tu aseguradora. Funcionan en tu navegador: no enviamos ni guardamos nada.',
			'post_content' => "<!-- wp:paragraph -->\n<p>Calculadoras y generadores gratuitos para defenderte frente a tu aseguradora. Funcionan en tu navegador: no enviamos ni guardamos nada de lo que escribas.</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:shortcode -->\n[herramientas]\n<!-- /wp:shortcode -->",
		) );
	}

	foreach ( espabilao_herramientas() as $slug => $h ) {
		if ( ! empty( $ids[ $slug ] ) && get_post( $ids[ $slug ] ) ) {
			continue;
		}
		$existente = get_page_by_path( 'herramientas/' . $slug );
		$ids[ $slug ] = $existente ? $existente->ID : wp_insert_post( array(
			'post_type'    => 'page',
			'post_status'  => 'publish',
			'post_title'   => $h['titulo'],
			'post_name'    => $slug,
			'post_parent'  => (int) $ids['_padre'],
			'post_excerpt' => $h['texto'],
			'post_content' => "<!-- wp:paragraph -->\n<p>" . esc_html( $h['texto'] ) . "</p>\n<!-- /wp:paragraph -->\n\n<!-- wp:shortcode -->\n[" . $h['shortcode'] . "]\n<!-- /wp:shortcode -->",
		) );
	}
	update_option( 'espabilao_paginas_herramientas', $ids, false );
}

/**
 * Carga el script de herramientas solo donde se usa.
 */
function espabilao_cargar_herramientas_js() {
	wp_enqueue_script( 'espabilao-herramientas', ESPABILAO_URI . '/assets/js/herramientas.js', array(), ESPABILAO_VERSION, array( 'strategy' => 'defer', 'in_footer' => true ) );
}

/**
 * Aviso común de privacidad.
 */
function espabilao_aviso_privacidad() {
	return '<p class="herramienta__privado">' . espabilao_icono( 'escudo', 16 ) . ' Todo ocurre en tu navegador: no enviamos ni guardamos nada de lo que escribas.</p>'
		. '<noscript><p class="herramienta__noscript">Esta herramienta necesita JavaScript activado.</p></noscript>';
}

/**
 * [herramientas] — rejilla de herramientas.
 */
add_shortcode( 'herramientas', function () {
	ob_start();
	echo '<ul class="herramientas-rejilla">';
	foreach ( espabilao_herramientas() as $slug => $h ) {
		$url = espabilao_url_herramienta( $slug );
		printf(
			'<li class="herramienta-tarjeta"><a href="%1$s"><span class="herramienta-tarjeta__icono">%2$s</span><span class="herramienta-tarjeta__corto">%3$s</span><span class="herramienta-tarjeta__titulo">%4$s</span><span class="herramienta-tarjeta__texto">%5$s</span><span class="herramienta-tarjeta__ir">Usar gratis %6$s</span></a></li>',
			esc_url( $url ? $url : '#' ),
			espabilao_icono( $h['icono'], 28 ), // phpcs:ignore
			esc_html( $h['corto'] ),
			esc_html( $h['titulo'] ),
			esc_html( $h['texto'] ),
			espabilao_icono( 'flecha', 16 ) // phpcs:ignore
		);
	}
	echo '</ul>';
	return ob_get_clean();
} );

/**
 * [calculadora_plazos]
 */
add_shortcode( 'calculadora_plazos', function () {
	espabilao_cargar_herramientas_js();
	$hoy = wp_date( 'Y-m-d' );
	ob_start();
	?>
	<div class="herramienta" data-herramienta="plazos" data-hoy="<?php echo esc_attr( $hoy ); ?>" data-boe-lcs="<?php echo esc_url( ESPABILAO_BOE_LCS ); ?>" data-boe-l44="<?php echo esc_url( ESPABILAO_BOE_L44 ); ?>">
		<div class="herramienta__pestanas" role="tablist" aria-label="¿Qué necesitas calcular?">
			<button type="button" role="tab" aria-selected="true" data-modo="siniestro"><?php echo espabilao_icono( 'alerta', 18 ); // phpcs:ignore ?> Tengo un siniestro</button>
			<button type="button" role="tab" aria-selected="false" data-modo="reclamacion"><?php echo espabilao_icono( 'carta', 18 ); // phpcs:ignore ?> Reclamé y no contestan</button>
			<button type="button" role="tab" aria-selected="false" data-modo="renovacion"><?php echo espabilao_icono( 'calendario', 18 ); // phpcs:ignore ?> No quiero renovar</button>
		</div>

		<div class="herramienta__panel" data-panel="siniestro">
			<div class="campos">
				<label class="campo"><span>¿Qué día ocurrió (o te enteraste)?</span><input type="date" data-campo="fecha_siniestro" value="<?php echo esc_attr( $hoy ); ?>"></label>
				<label class="campo"><span>¿Qué día avisaste a la aseguradora? <em>Opcional</em></span><input type="date" data-campo="fecha_aviso"></label>
				<label class="campo"><span>Tipo de seguro</span>
					<select data-campo="tipo">
						<option value="danos">De daños (hogar, coche, moto, mascotas, alquiler…)</option>
						<option value="personas">De personas (vida, salud, decesos, accidentes…)</option>
					</select>
				</label>
			</div>
		</div>
		<div class="herramienta__panel" data-panel="reclamacion" hidden>
			<div class="campos">
				<label class="campo"><span>¿Qué día presentaste la reclamación al Servicio de Atención al Cliente?</span><input type="date" data-campo="fecha_reclamacion" value="<?php echo esc_attr( $hoy ); ?>"></label>
			</div>
		</div>
		<div class="herramienta__panel" data-panel="renovacion" hidden>
			<div class="campos">
				<label class="campo"><span>¿Qué día vence tu póliza?</span><input type="date" data-campo="fecha_vencimiento"></label>
			</div>
		</div>

		<div class="herramienta__resultado" aria-live="polite">
			<ol class="linea-tiempo" data-salida></ol>
			<div class="herramienta__acciones" data-acciones hidden>
				<button type="button" class="boton boton--naranja" data-ics><?php echo espabilao_icono( 'calendario', 18 ); // phpcs:ignore ?> Añadir a mi calendario</button>
				<button type="button" class="boton boton--borde" data-imprimir><?php echo espabilao_icono( 'imprimir', 18 ); // phpcs:ignore ?> Imprimir</button>
			</div>
		</div>
		<p class="herramienta__nota">Cálculo orientativo según la Ley 50/1980, de Contrato de Seguro, y la Ley 44/2002. Los días se cuentan naturales desde el día siguiente y los meses de fecha a fecha (art. 5 del Código Civil). Si tu póliza da plazos más favorables, se aplican los de tu póliza.</p>
		<?php echo espabilao_aviso_privacidad(); // phpcs:ignore ?>
	</div>
	<?php
	return trim( ob_get_clean() );
} );

/**
 * [calculadora_infraseguro]
 */
add_shortcode( 'calculadora_infraseguro', function () {
	espabilao_cargar_herramientas_js();
	ob_start();
	?>
	<div class="herramienta" data-herramienta="infraseguro" data-boe-lcs="<?php echo esc_url( ESPABILAO_BOE_LCS ); ?>">
		<div class="campos campos--dos">
			<label class="campo"><span>Valor real de lo asegurado</span><span class="campo__euro"><input type="number" inputmode="decimal" min="0" step="100" data-campo="valor" placeholder="40000"><b>€</b></span><small>Lo que costaría reponer hoy tu contenido o reconstruir tu vivienda.</small></label>
			<label class="campo"><span>Suma asegurada en tu póliza</span><span class="campo__euro"><input type="number" inputmode="decimal" min="0" step="100" data-campo="suma" placeholder="25000"><b>€</b></span><small>Está en tus condiciones particulares.</small></label>
			<label class="campo"><span>Importe del daño</span><span class="campo__euro"><input type="number" inputmode="decimal" min="0" step="50" data-campo="dano" placeholder="6000"><b>€</b></span></label>
			<label class="campo"><span>Franquicia <em>Opcional</em></span><span class="campo__euro"><input type="number" inputmode="decimal" min="0" step="50" data-campo="franquicia" placeholder="0"><b>€</b></span></label>
		</div>
		<label class="casilla"><input type="checkbox" data-campo="primer_riesgo"> Mi póliza es «a primer riesgo» o excluye expresamente la regla proporcional</label>
		<div class="herramienta__resultado" aria-live="polite" data-salida></div>
		<p class="herramienta__nota">Aplica la regla proporcional del <a href="<?php echo esc_url( ESPABILAO_BOE_LCS . '#atreinta' ); ?>" target="_blank" rel="noopener">art. 30 de la Ley de Contrato de Seguro</a>. Cálculo orientativo: tu póliza puede tener límites por garantía o reglas distintas.</p>
		<?php echo espabilao_aviso_privacidad(); // phpcs:ignore ?>
	</div>
	<?php
	return trim( ob_get_clean() );
} );

/**
 * [generador_carta]
 */
add_shortcode( 'generador_carta', function () {
	espabilao_cargar_herramientas_js();
	$campos = array(
		'nombre'      => array( 'Tu nombre y apellidos', 'text', '' ),
		'dni'         => array( 'DNI / NIE', 'text', '' ),
		'direccion'   => array( 'Tu dirección', 'text', '' ),
		'email'       => array( 'Tu correo electrónico', 'email', '' ),
		'aseguradora' => array( 'Aseguradora', 'text', '' ),
		'poliza'      => array( 'N.º de póliza', 'text', '' ),
		'siniestro'   => array( 'N.º de siniestro', 'text', 'reclamacion rechazo intereses' ),
		'fecha_sin'   => array( 'Fecha del siniestro', 'date', 'reclamacion rechazo intereses' ),
		'vencimiento' => array( 'Fecha de vencimiento de la póliza', 'date', 'renovacion' ),
		'hechos'      => array( 'Qué pasó (breve)', 'textarea', 'reclamacion rechazo' ),
		'peticion'    => array( 'Qué pides exactamente', 'textarea', 'reclamacion' ),
		'importe'     => array( 'Importe que te deben (€)', 'number', 'intereses' ),
	);
	ob_start();
	?>
	<div class="herramienta herramienta--carta" data-herramienta="carta" data-lugar="">
		<div class="herramienta__rejilla">
			<div class="herramienta__formulario">
				<label class="campo"><span>¿Qué carta necesitas?</span>
					<select data-campo="modelo">
						<option value="reclamacion">Reclamación al Servicio de Atención al Cliente</option>
						<option value="rechazo">Pedir el rechazo por escrito y la documentación</option>
						<option value="renovacion">Oposición a la renovación (no renovar)</option>
						<option value="intereses">Reclamar intereses por pagar tarde</option>
					</select>
				</label>
				<div class="campos">
					<?php foreach ( $campos as $clave => $c ) : ?>
						<label class="campo" <?php echo $c[2] ? 'data-solo="' . esc_attr( $c[2] ) . '"' : ''; ?>><span><?php echo esc_html( $c[0] ); ?></span>
							<?php if ( 'textarea' === $c[1] ) : ?>
								<textarea rows="3" data-campo="<?php echo esc_attr( $clave ); ?>"></textarea>
							<?php else : ?>
								<input type="<?php echo esc_attr( $c[1] ); ?>" data-campo="<?php echo esc_attr( $clave ); ?>" autocomplete="off">
							<?php endif; ?>
						</label>
					<?php endforeach; ?>
				</div>
			</div>
			<div class="herramienta__vista">
				<div class="esp-carta esp-carta--generada">
					<div class="esp-carta__barra"><span class="etiqueta"><?php echo espabilao_icono( 'carta', 18 ); // phpcs:ignore ?> Vista previa</span>
						<span class="esp-carta__botones">
							<button type="button" class="boton-copiar" data-copiar-generada><?php echo espabilao_icono( 'copiar', 18 ); // phpcs:ignore ?><span class="boton-copiar__texto">Copiar</span></button>
							<button type="button" class="boton-icono boton-icono--peq" data-descargar aria-label="Descargar como texto"><?php echo espabilao_icono( 'descargar', 18 ); // phpcs:ignore ?></button>
							<button type="button" class="boton-icono boton-icono--peq" data-imprimir aria-label="Imprimir"><?php echo espabilao_icono( 'imprimir', 18 ); // phpcs:ignore ?></button>
						</span>
					</div>
					<p class="esp-carta__nota"><?php echo espabilao_icono( 'alerta', 16 ); // phpcs:ignore ?> Modelo orientativo, adáptalo a tu caso. Envíalo por un medio que deje constancia.</p>
					<pre class="carta-generada" data-salida tabindex="0" aria-label="Texto de la carta"></pre>
				</div>
			</div>
		</div>
		<?php echo espabilao_aviso_privacidad(); // phpcs:ignore ?>
	</div>
	<?php
	return trim( ob_get_clean() );
} );

/**
 * [detector_letra_pequena]
 */
add_shortcode( 'detector_letra_pequena', function () {
	espabilao_cargar_herramientas_js();
	$glosario = array();
	foreach ( espabilao_terminos_glosario() as $t ) {
		$glosario[] = array( 'f' => $t['formas'], 't' => $t['titulo'], 'd' => $t['def'], 'u' => $t['url'] );
	}
	ob_start();
	?>
	<div class="herramienta herramienta--detector" data-herramienta="detector">
		<script type="application/json" data-glosario><?php echo wp_json_encode( $glosario, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP ); ?></script>
		<label class="campo"><span>Pega aquí una cláusula o las condiciones de tu póliza</span>
			<textarea rows="8" data-campo="texto" placeholder="Ej.: «Quedan excluidos los daños producidos por filtraciones o humedades debidas al desgaste notorio… La franquicia será de 300 € por siniestro…»"></textarea>
		</label>
		<div class="herramienta__acciones">
			<button type="button" class="boton boton--naranja" data-analizar><?php echo espabilao_icono( 'lupa-doc', 18 ); // phpcs:ignore ?> Analizar letra pequeña</button>
			<button type="button" class="boton boton--borde" data-ejemplo>Probar con un ejemplo</button>
		</div>
		<div class="herramienta__resultado" aria-live="polite" data-salida></div>
		<p class="herramienta__nota">El detector busca expresiones que suelen recortar derechos. No sustituye a leer la póliza completa ni a un profesional.</p>
		<?php echo espabilao_aviso_privacidad(); // phpcs:ignore ?>
	</div>
	<?php
	return trim( ob_get_clean() );
} );
