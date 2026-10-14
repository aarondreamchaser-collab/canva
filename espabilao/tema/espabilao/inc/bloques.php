<?php
/**
 * Bloques propios de Espabilao: escalera de reclamación, plazos que te
 * protegen, plantilla de carta y «dónde dice eso en tu póliza».
 *
 * Escalera y plazos son shortcodes (contenido común que se actualiza desde
 * el tema). Carta y póliza son patrones de bloques editables en Gutenberg.
 * Todos aparecen en el insertador de bloques, pestaña Patrones > Espabilao.
 *
 * @package Espabilao
 */

defined( 'ABSPATH' ) || exit;

const ESPABILAO_BOE_LCS = 'https://www.boe.es/buscar/act.php?id=BOE-A-1980-22501';
const ESPABILAO_BOE_LEC = 'https://www.boe.es/buscar/act.php?id=BOE-A-2000-323';
const ESPABILAO_BOE_L44 = 'https://www.boe.es/buscar/act.php?id=BOE-A-2002-22807';
const ESPABILAO_BOE_LO1 = 'https://www.boe.es/buscar/act.php?id=BOE-A-2025-76';

/**
 * Plazos de la Ley 50/1980, de Contrato de Seguro, con su ancla en el BOE.
 *
 * @return array<string, array<string, string>>
 */
function espabilao_plazos() {
	return array(
		'16' => array(
			'cifra'  => '7 días',
			'titulo' => 'Para avisar del siniestro',
			'texto'  => 'Tienes 7 días desde que lo conoces para comunicarlo a la aseguradora, salvo que tu póliza dé más plazo. Si te retrasas no pierdes el seguro, pero pueden reclamarte los daños que cause el retraso.',
			'quien'  => 'Tú',
			'ancla'  => 'adieciseis',
		),
		'38' => array(
			'cifra'  => '5 días',
			'titulo' => 'Para enviar la lista de daños',
			'texto'  => 'En seguros de daños (hogar, comercio…), desde el aviso tienes 5 días para mandar por escrito la relación de objetos dañados o salvados y tu estimación. Si no hay acuerdo, cada parte puede nombrar su perito.',
			'quien'  => 'Tú',
			'ancla'  => 'atreintayocho',
		),
		'18' => array(
			'cifra'  => '40 días',
			'titulo' => 'Para que te adelanten el mínimo',
			'texto'  => 'En 40 días desde que reciben tu declaración, la aseguradora debe pagarte al menos el importe mínimo que reconozca deber, aunque siga peritando.',
			'quien'  => 'Aseguradora',
			'ancla'  => 'adieciocho',
		),
		'20' => array(
			'cifra'  => '3 meses',
			'titulo' => 'A partir de aquí, paga intereses',
			'texto'  => 'Si no ha pagado en 3 meses desde el siniestro (o no adelantó el mínimo en 40 días), entra en mora y debe intereses: el interés legal más un 50 %, y al menos un 20 % anual a partir de los dos años.',
			'quien'  => 'Aseguradora',
			'ancla'  => 'aveinte',
		),
		'22' => array(
			'cifra'  => '1 mes',
			'titulo' => 'Para no renovar',
			'texto'  => 'Puedes oponerte a la renovación avisando por escrito al menos 1 mes antes del vencimiento. La aseguradora necesita 2 meses, y también debe avisarte con 2 meses de antelación de cualquier cambio en el contrato.',
			'quien'  => 'Tú',
			'ancla'  => 'aveintidos',
		),
		'15' => array(
			'cifra'  => '1 mes',
			'titulo' => 'De margen si se te pasa un recibo',
			'texto'  => 'Si no pagas un recibo que no sea el primero, la cobertura se suspende un mes después del vencimiento. Si la aseguradora no lo reclama en 6 meses, el contrato se extingue. Al pagar, la cobertura vuelve a las 24 horas.',
			'quien'  => 'Tú',
			'ancla'  => 'aquince',
		),
		'10' => array(
			'cifra'  => '1 mes',
			'titulo' => 'Para rescindir por datos mal declarados',
			'texto'  => 'Si la aseguradora descubre que contestaste mal el cuestionario, tiene 1 mes desde que lo sabe para rescindir. Ojo: solo responde por lo que te preguntaron en el cuestionario.',
			'quien'  => 'Aseguradora',
			'ancla'  => 'adiez',
		),
	);
}

/**
 * [plazos articulos="16,38,18,20,22" titulo="Plazos que te protegen"]
 */
function espabilao_sc_plazos( $atts ) {
	$atts  = shortcode_atts( array( 'articulos' => '16,38,18,20,22', 'titulo' => 'Plazos que te protegen' ), $atts, 'plazos' );
	$todos = espabilao_plazos();
	$lista = array_filter( array_map( 'trim', explode( ',', $atts['articulos'] ) ), function ( $a ) use ( $todos ) {
		return isset( $todos[ $a ] );
	} );
	if ( ! $lista ) {
		return '';
	}
	$id = wp_unique_id( 'plazos-' );
	ob_start();
	?>
	<section class="plazos" aria-labelledby="<?php echo esc_attr( $id ); ?>">
		<header class="plazos__cabecera">
			<span class="etiqueta"><?php echo espabilao_icono( 'reloj', 18 ); // phpcs:ignore ?> Ley 50/1980, de Contrato de Seguro</span>
			<h2 id="<?php echo esc_attr( $id ); ?>" class="plazos__titulo"><?php echo esc_html( $atts['titulo'] ); ?></h2>
		</header>
		<ol class="plazos__lista">
			<?php foreach ( $lista as $art ) : $p = $todos[ $art ]; ?>
				<li class="plazo">
					<span class="plazo__cifra"><?php echo esc_html( $p['cifra'] ); ?></span>
					<div class="plazo__cuerpo">
						<h3 class="plazo__titulo"><?php echo esc_html( $p['titulo'] ); ?> <span class="plazo__quien"><?php echo esc_html( $p['quien'] ); ?></span></h3>
						<p><?php echo esc_html( $p['texto'] ); ?></p>
						<a class="plazo__boe" href="<?php echo esc_url( ESPABILAO_BOE_LCS . '#' . $p['ancla'] ); ?>" target="_blank" rel="noopener">Art. <?php echo esc_html( $art ); ?> de la Ley de Contrato de Seguro <span class="screen-reader-text">(se abre en el BOE)</span><span aria-hidden="true"> · BOE ↗</span></a>
					</div>
				</li>
			<?php endforeach; ?>
		</ol>
		<p class="plazos__nota">Si tu póliza te da un plazo más favorable, se aplica el de tu póliza.</p>
	</section>
	<?php
	return trim( ob_get_clean() );
}
add_shortcode( 'plazos', 'espabilao_sc_plazos' );

/**
 * [escalera_reclamacion]
 */
function espabilao_sc_escalera() {
	$id    = wp_unique_id( 'escalera-' );
	$dgsfp = espabilao_opcion( 'dgsfp_url' );
	$pasos = array(
		array(
			'titulo'  => 'Pide el «no» por escrito',
			'texto'   => 'Exige que el rechazo te llegue por escrito y diga en qué cláusula se basa. Sin eso no hay nada que discutir. Guarda fotos, facturas, correos y apunta fechas.',
			'plazo'   => 'Antes de nada',
			'enlaces' => array(),
		),
		array(
			'titulo'  => 'Reclama al Servicio de Atención al Cliente',
			'texto'   => 'Reclamación formal al Servicio de Atención al Cliente o al Defensor del Cliente de tu aseguradora, por un medio que deje constancia (registro en su web, correo con acuse o burofax). Deben acusar recibo y contestarte por escrito y de forma motivada. Indica póliza, siniestro, qué pides y por qué.',
			'plazo'   => 'Tienen 1 mes para responderte',
			'enlaces' => array(
				array( ESPABILAO_BOE_L44 . '#a29', 'Art. 29 bis de la Ley 44/2002 · BOE' ),
			),
		),
		array(
			'titulo'  => 'Acude a la DGSFP',
			'texto'   => 'Si ha pasado un mes sin respuesta, no admiten tu reclamación o te la desestiman, preséntala ante el Servicio de Reclamaciones de la Dirección General de Seguros. Es gratis y se puede hacer online. Su informe no obliga a la aseguradora, pero pesa.',
			'plazo'   => 'Requisito: haber reclamado antes en el peldaño 2',
			'enlaces' => array(
				array( $dgsfp, 'Cómo reclamar en la DGSFP' ),
				array( ESPABILAO_BOE_L44 . '#a30', 'Art. 30 de la Ley 44/2002 · BOE' ),
			),
		),
		array(
			'titulo'  => 'Juzgado (o arbitraje de consumo)',
			'texto'   => 'Hasta 2.000 € puedes reclamar en un juicio verbal sin abogado ni procurador. Si la aseguradora está adherida al arbitraje de consumo, también puedes ir por ahí. Antes de demandar, la ley exige haber intentado un medio de acuerdo (negociación, mediación, conciliación…): guarda por escrito todo lo que hayas reclamado.',
			'plazo'   => 'Si te dan la razón, reclama también los intereses de demora (art. 20 de la Ley de Contrato de Seguro)',
			'enlaces' => array(
				array( ESPABILAO_BOE_LEC . '#a23', 'Arts. 23 y 31 de la Ley de Enjuiciamiento Civil · BOE' ),
				array( ESPABILAO_BOE_LO1 . '#a5', 'Art. 5 de la Ley Orgánica 1/2025 · BOE' ),
			),
		),
	);
	ob_start();
	?>
	<section class="escalera" aria-labelledby="<?php echo esc_attr( $id ); ?>">
		<header class="escalera__cabecera">
			<span class="etiqueta"><?php echo espabilao_icono( 'escalera', 18 ); // phpcs:ignore ?> Si no te pagan</span>
			<h2 id="<?php echo esc_attr( $id ); ?>" class="escalera__titulo">Escalera de reclamación</h2>
			<p class="escalera__intro">Sube peldaño a peldaño y no te saltes ninguno: cada uno es requisito del siguiente.</p>
		</header>
		<ol class="escalera__pasos">
			<?php foreach ( $pasos as $i => $paso ) : ?>
				<li class="peldano">
					<span class="peldano__n" aria-hidden="true"><?php echo esc_html( $i + 1 ); ?></span>
					<div class="peldano__cuerpo">
						<h3 class="peldano__titulo"><?php echo esc_html( $paso['titulo'] ); ?></h3>
						<p><?php echo esc_html( $paso['texto'] ); ?></p>
						<p class="peldano__plazo"><?php echo esc_html( $paso['plazo'] ); ?></p>
						<?php foreach ( $paso['enlaces'] as $enlace ) : ?>
							<?php if ( ! empty( $enlace[0] ) ) : ?>
								<a class="peldano__enlace" href="<?php echo esc_url( $enlace[0] ); ?>" target="_blank" rel="noopener"><?php echo esc_html( $enlace[1] ); ?> <span aria-hidden="true">↗</span><span class="screen-reader-text">(fuente oficial, se abre en otra pestaña)</span></a>
							<?php endif; ?>
						<?php endforeach; ?>
					</div>
				</li>
			<?php endforeach; ?>
		</ol>
	</section>
	<?php
	return trim( ob_get_clean() );
}
add_shortcode( 'escalera_reclamacion', 'espabilao_sc_escalera' );

/**
 * Cabecera de los bloques «carta» y «póliza» (se añade al pintar el grupo).
 */
add_filter( 'render_block', function ( $html, $block ) {
	if ( 'core/group' !== $block['blockName'] || empty( $block['attrs']['className'] ) ) {
		return $html;
	}
	$clases = ' ' . $block['attrs']['className'] . ' ';

	if ( false !== strpos( $clases, ' esp-carta ' ) ) {
		$barra = '<div class="esp-carta__barra"><span class="etiqueta">' . espabilao_icono( 'carta', 18 ) . ' Plantilla de carta</span><button type="button" class="boton-copiar" data-copiar>' . espabilao_icono( 'copiar', 18 ) . '<span class="boton-copiar__texto">Copiar carta</span></button></div>'
			. '<p class="esp-carta__nota" role="note">' . espabilao_icono( 'alerta', 16 ) . ' Modelo orientativo, adáptalo a tu caso. Sustituye todo lo que va entre [corchetes].</p>';
		return preg_replace( '/^(\s*<div\b[^>]*>)/', '$1' . $barra, $html, 1 );
	}
	if ( false !== strpos( $clases, ' esp-poliza ' ) ) {
		$cabecera = '<div class="esp-poliza__cabecera"><span class="etiqueta">' . espabilao_icono( 'lupa-doc', 18 ) . ' Dónde dice eso en tu póliza</span></div>';
		return preg_replace( '/^(\s*<div\b[^>]*>)/', '$1' . $cabecera, $html, 1 );
	}
	return $html;
}, 10, 2 );

/**
 * Patrones de bloques.
 */
add_action( 'init', function () {
	if ( ! function_exists( 'register_block_pattern' ) ) {
		return;
	}
	register_block_pattern_category( 'espabilao', array( 'label' => 'Espabilao' ) );

	register_block_pattern( 'espabilao/escalera', array(
		'title'       => 'Escalera de reclamación',
		'description' => 'Los cuatro peldaños para reclamar a una aseguradora, con enlace a la DGSFP.',
		'categories'  => array( 'espabilao' ),
		'keywords'    => array( 'reclamar', 'dgsfp', 'escalera' ),
		'content'     => "<!-- wp:shortcode -->\n[escalera_reclamacion]\n<!-- /wp:shortcode -->",
	) );

	register_block_pattern( 'espabilao/plazos', array(
		'title'       => 'Plazos que te protegen',
		'description' => 'Plazos de la Ley de Contrato de Seguro con enlace a cada artículo en el BOE. Artículos disponibles: 10, 15, 16, 18, 20, 22 y 38.',
		'categories'  => array( 'espabilao' ),
		'keywords'    => array( 'plazos', 'boe', 'ley' ),
		'content'     => "<!-- wp:shortcode -->\n[plazos articulos=\"16,38,18,20,22\"]\n<!-- /wp:shortcode -->",
	) );

	register_block_pattern( 'espabilao/carta', array(
		'title'       => 'Plantilla de carta',
		'description' => 'Carta con botón «Copiar». Edita el texto; lo que va entre corchetes es lo que el lector debe cambiar.',
		'categories'  => array( 'espabilao' ),
		'keywords'    => array( 'carta', 'plantilla', 'modelo', 'reclamación' ),
		'content'     => '<!-- wp:group {"className":"esp-carta","layout":{"type":"default"}} -->
<div class="wp-block-group esp-carta"><!-- wp:heading {"level":3,"className":"esp-carta__titulo"} -->
<h3 class="wp-block-heading esp-carta__titulo">Reclamación al Servicio de Atención al Cliente</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>[Tu nombre y apellidos]<br>[DNI]<br>[Dirección]<br>[Correo electrónico]</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>A la atención del Servicio de Atención al Cliente de [nombre de la aseguradora]</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>[Lugar], a [fecha]</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Asunto: Reclamación por el siniestro n.º [número], póliza n.º [número]</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>El [fecha del siniestro] comuniqué a la compañía [breve descripción de lo ocurrido]. El [fecha] recibí la respuesta de que [lo que os contestaron], sin indicar en qué cláusula de la póliza se basa esa decisión.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Considero que el siniestro está cubierto por [garantía o apartado de las condiciones], por lo que SOLICITO [lo que pides: el pago de X €, la reparación, la revisión del peritaje…].</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Adjunto [fotos, facturas, informe pericial…]. Quedo a la espera de su respuesta por escrito en el plazo legalmente previsto.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Atentamente,<br>[Firma]</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->',
	) );

	register_block_pattern( 'espabilao/poliza', array(
		'title'       => 'Dónde dice eso en tu póliza',
		'description' => 'Cita literal de la cláusula, con documento, apartado y página, y su explicación.',
		'categories'  => array( 'espabilao' ),
		'keywords'    => array( 'póliza', 'cláusula', 'condiciones' ),
		'content'     => '<!-- wp:group {"className":"esp-poliza","layout":{"type":"default"}} -->
<div class="wp-block-group esp-poliza"><!-- wp:paragraph {"className":"esp-poliza__ref"} -->
<p class="esp-poliza__ref"><strong>Aseguradora:</strong> [Compañía] · [Producto]<br><strong>Documento:</strong> Condiciones generales, edición [mes/año]<br><strong>Apartado:</strong> [4.2 Exclusiones] · página [12]</p>
<!-- /wp:paragraph -->

<!-- wp:quote {"className":"esp-poliza__cita"} -->
<blockquote class="wp-block-quote esp-poliza__cita"><!-- wp:paragraph -->
<p>[Copia aquí el texto literal de la cláusula, sin cambiar ni una coma.]</p>
<!-- /wp:paragraph --></blockquote>
<!-- /wp:quote -->

<!-- wp:paragraph {"className":"esp-poliza__cristiano"} -->
<p class="esp-poliza__cristiano"><strong>En cristiano:</strong> [Qué significa para el lector, en una o dos frases.]</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->',
	) );

	register_block_pattern( 'espabilao/caso', array(
		'title'       => 'Estructura de un caso (¿Pagó o no pagó?)',
		'description' => 'Esqueleto para un caso real: qué pasó, qué dice la póliza, qué alegó la compañía y cómo acabó.',
		'categories'  => array( 'espabilao' ),
		'content'     => '<!-- wp:heading -->
<h2 class="wp-block-heading">Qué pasó</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>[Hechos, con fechas.]</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Qué dice la póliza</h2>
<!-- /wp:heading -->

<!-- wp:pattern {"slug":"espabilao/poliza"} /-->

<!-- wp:heading -->
<h2 class="wp-block-heading">Qué alegó la aseguradora</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>[Motivo del rechazo, literal si es posible.]</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Cómo acabó</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>[Resultado y por qué. Recuerda elegir el veredicto en la «Ficha Espabilao».]</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Qué puedes aprender</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list"><li>[Lección 1]</li><li>[Lección 2]</li></ul>
<!-- /wp:list -->',
	) );
} );
