/**
 * Espabilao · herramientas (plazos, infraseguro, cartas, detector).
 * Todo se calcula en el navegador: no se envía ni se guarda nada.
 */
( function () {
	'use strict';

	var MESES = [ 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre' ];
	var DIAS = [ 'domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado' ];

	function $( sel, ctx ) {
		return ( ctx || document ).querySelector( sel );
	}
	function $$( sel, ctx ) {
		return Array.prototype.slice.call( ( ctx || document ).querySelectorAll( sel ) );
	}
	function esc( t ) {
		return String( t ).replace( /[&<>"']/g, function ( c ) {
			return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ c ];
		} );
	}
	function campo( raiz, nombre ) {
		var el = $( '[data-campo="' + nombre + '"]', raiz );
		if ( ! el ) {
			return '';
		}
		return 'checkbox' === el.type ? el.checked : el.value.trim();
	}

	/* Fechas (art. 5 del Código Civil) ------------------------------- */
	function leerFecha( v ) {
		if ( ! /^\d{4}-\d{2}-\d{2}$/.test( v ) ) {
			return null;
		}
		var p = v.split( '-' );
		return new Date( +p[ 0 ], +p[ 1 ] - 1, +p[ 2 ] );
	}
	function sumarDias( f, n ) {
		var d = new Date( f.getTime() );
		d.setDate( d.getDate() + n );
		return d;
	}
	// Meses de fecha a fecha; si no existe el día, el último del mes.
	function sumarMeses( f, n ) {
		var y = f.getFullYear();
		var m = f.getMonth() + n;
		var destino = new Date( y, m, 1 );
		var ultimo = new Date( destino.getFullYear(), destino.getMonth() + 1, 0 ).getDate();
		destino.setDate( Math.min( f.getDate(), ultimo ) );
		return destino;
	}
	function fechaLarga( f ) {
		return DIAS[ f.getDay() ] + ', ' + f.getDate() + ' de ' + MESES[ f.getMonth() ] + ' de ' + f.getFullYear();
	}
	function iso( f ) {
		return f.getFullYear() + '-' + ( '0' + ( f.getMonth() + 1 ) ).slice( -2 ) + '-' + ( '0' + f.getDate() ).slice( -2 );
	}
	function estado( f, hoy ) {
		var dias = Math.round( ( f - hoy ) / 86400000 );
		if ( dias < 0 ) {
			return { clase: 'pasado', texto: 'Pasó hace ' + ( -dias ) + ( -1 === dias ? ' día' : ' días' ) };
		}
		if ( 0 === dias ) {
			return { clase: 'hoy', texto: 'Es hoy' };
		}
		return { clase: dias <= 7 ? 'pronto' : 'futuro', texto: 'Faltan ' + dias + ( 1 === dias ? ' día' : ' días' ) };
	}

	/* Calculadora de plazos ------------------------------------------ */
	function iniciarPlazos( raiz ) {
		var lcs = raiz.getAttribute( 'data-boe-lcs' );
		var l44 = raiz.getAttribute( 'data-boe-l44' );
		var hoy = leerFecha( raiz.getAttribute( 'data-hoy' ) ) || new Date();
		var modo = 'siniestro';
		var eventos = [];

		function calcular() {
			var filas = [];
			if ( 'siniestro' === modo ) {
				var s = leerFecha( campo( raiz, 'fecha_siniestro' ) );
				if ( s ) {
					var aviso = leerFecha( campo( raiz, 'fecha_aviso' ) ) || s;
					var tipo = campo( raiz, 'tipo' );
					filas.push( { f: sumarDias( s, 7 ), t: 'Último día para avisar a tu aseguradora', d: 'Tienes 7 días desde que conoces el siniestro, salvo que tu póliza dé más.', a: 'Art. 16 LCS', u: lcs + '#adieciseis' } );
					if ( 'danos' === tipo ) {
						filas.push( { f: sumarDias( aviso, 5 ), t: 'Enviar por escrito la lista de daños', d: 'Relación de objetos dañados o salvados y tu estimación, 5 días después del aviso.', a: 'Art. 38 LCS', u: lcs + '#atreintayocho' } );
					}
					filas.push( { f: sumarDias( aviso, 40 ), t: 'Deben haberte pagado el importe mínimo', d: 'En 40 días desde tu declaración, aunque sigan peritando.', a: 'Art. 18 LCS', u: lcs + '#adieciocho' } );
					filas.push( { f: sumarMeses( s, 3 ), t: 'Si no han pagado, te deben intereses', d: 'A los 3 meses del siniestro la aseguradora entra en mora: interés legal + 50 %.', a: 'Art. 20 LCS', u: lcs + '#aveinte' } );
					filas.push( { f: sumarMeses( s, 'personas' === tipo ? 60 : 24 ), t: 'Fecha orientativa de prescripción', d: 'Para reclamar en los tribunales: ' + ( 'personas' === tipo ? '5 años en seguros de personas' : '2 años en seguros de daños' ) + '. Reclamar por escrito antes puede interrumpirla.', a: 'Art. 23 LCS', u: lcs + '#aveintitres' } );
				}
			} else if ( 'reclamacion' === modo ) {
				var r = leerFecha( campo( raiz, 'fecha_reclamacion' ) );
				if ( r ) {
					var mes = sumarMeses( r, 1 );
					filas.push( { f: mes, t: 'Límite para que te respondan', d: 'El Servicio de Atención al Cliente tiene 1 mes para resolver tu reclamación.', a: 'Art. 29 bis Ley 44/2002', u: l44 + '#a29' } );
					filas.push( { f: sumarDias( mes, 1 ), t: 'Desde aquí puedes ir a la DGSFP', d: 'Si no han contestado o te dicen que no, presenta tu reclamación gratis ante la Dirección General de Seguros.', a: 'Art. 30 Ley 44/2002', u: l44 + '#a30' } );
				}
			} else {
				var v = leerFecha( campo( raiz, 'fecha_vencimiento' ) );
				if ( v ) {
					filas.push( { f: sumarMeses( v, -2 ), t: 'La aseguradora debía avisarte de cambios', d: 'Cualquier modificación (también de precio) debe comunicártela al menos 2 meses antes del vencimiento.', a: 'Art. 22.3 LCS', u: lcs + '#aveintidos' } );
					filas.push( { f: sumarMeses( v, -1 ), t: 'Último día para enviar tu oposición', d: 'Avisa por escrito al menos 1 mes antes del vencimiento para no renovar.', a: 'Art. 22.2 LCS', u: lcs + '#aveintidos' } );
					filas.push( { f: v, t: 'Vencimiento de tu póliza', d: 'Si te opusiste a tiempo, el contrato termina este día.', a: 'Art. 22 LCS', u: lcs + '#aveintidos' } );
				}
			}
			filas.sort( function ( a, b ) {
				return a.f - b.f;
			} );
			pintar( filas );
		}

		function pintar( filas ) {
			var salida = $( '[data-salida]', raiz );
			var acciones = $( '[data-acciones]', raiz );
			eventos = filas;
			if ( ! filas.length ) {
				salida.innerHTML = '<li class="linea-tiempo__vacio">Elige una fecha para ver tus plazos.</li>';
				acciones.hidden = true;
				return;
			}
			salida.innerHTML = filas.map( function ( x ) {
				var e = estado( x.f, hoy );
				return '<li class="hito hito--' + e.clase + '"><div class="hito__fecha"><strong>' + esc( fechaLarga( x.f ) ) + '</strong><span class="hito__estado">' + esc( e.texto ) + '</span></div>' +
					'<div class="hito__texto"><p class="hito__titulo">' + esc( x.t ) + '</p><p>' + esc( x.d ) + '</p><a href="' + esc( x.u ) + '" target="_blank" rel="noopener">' + esc( x.a ) + ' · BOE ↗</a></div></li>';
			} ).join( '' );
			acciones.hidden = false;
		}

		function ics() {
			var ahora = new Date().toISOString().replace( /[-:]/g, '' ).split( '.' )[ 0 ] + 'Z';
			var lineas = [ 'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Espabilao//Plazos//ES', 'CALSCALE:GREGORIAN' ];
			eventos.forEach( function ( x, i ) {
				var fin = sumarDias( x.f, 1 );
				lineas.push( 'BEGIN:VEVENT', 'UID:espabilao-' + iso( x.f ) + '-' + i + '@espabilao', 'DTSTAMP:' + ahora,
					'DTSTART;VALUE=DATE:' + iso( x.f ).replace( /-/g, '' ), 'DTEND;VALUE=DATE:' + iso( fin ).replace( /-/g, '' ),
					'SUMMARY:' + ( 'Seguro: ' + x.t ).replace( /[,;]/g, ' ' ), 'DESCRIPTION:' + ( x.d + ' (' + x.a + ')' ).replace( /[,;]/g, ' ' ),
					'BEGIN:VALARM', 'TRIGGER:-P1D', 'ACTION:DISPLAY', 'DESCRIPTION:Plazo de tu seguro mañana', 'END:VALARM', 'END:VEVENT' );
			} );
			lineas.push( 'END:VCALENDAR' );
			descargar( lineas.join( '\r\n' ), 'plazos-seguro.ics', 'text/calendar' );
		}

		$$( '[role=tab]', raiz ).forEach( function ( b ) {
			b.addEventListener( 'click', function () {
				modo = b.getAttribute( 'data-modo' );
				$$( '[role=tab]', raiz ).forEach( function ( o ) {
					o.setAttribute( 'aria-selected', o === b ? 'true' : 'false' );
				} );
				$$( '[data-panel]', raiz ).forEach( function ( p ) {
					p.hidden = p.getAttribute( 'data-panel' ) !== modo;
				} );
				calcular();
			} );
		} );
		raiz.addEventListener( 'input', calcular );
		raiz.addEventListener( 'change', calcular );
		$( '[data-ics]', raiz ).addEventListener( 'click', ics );
		$( '[data-imprimir]', raiz ).addEventListener( 'click', function () {
			window.print();
		} );
		calcular();
	}

	/* Calculadora de infraseguro ------------------------------------- */
	function euros( n ) {
		return n.toLocaleString( 'es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 } );
	}
	function iniciarInfraseguro( raiz ) {
		function calcular() {
			var valor = parseFloat( campo( raiz, 'valor' ) ) || 0;
			var suma = parseFloat( campo( raiz, 'suma' ) ) || 0;
			var dano = parseFloat( campo( raiz, 'dano' ) ) || 0;
			var franquicia = parseFloat( campo( raiz, 'franquicia' ) ) || 0;
			var primer = campo( raiz, 'primer_riesgo' );
			var salida = $( '[data-salida]', raiz );
			if ( ! valor || ! suma || ! dano ) {
				salida.innerHTML = '<p class="resultado__vacio">Rellena el valor real, la suma asegurada y el importe del daño.</p>';
				return;
			}
			var proporcion = Math.min( 1, suma / valor );
			var sinRegla = Math.max( 0, Math.min( dano, suma ) - franquicia );
			var conRegla = primer ? sinRegla : Math.max( 0, Math.min( dano * proporcion, suma ) - franquicia );
			var pierdes = Math.max( 0, dano - conRegla );
			var infra = suma < valor && ! primer;
			var pct = Math.round( proporcion * 100 );
			salida.innerHTML =
				'<div class="resultado__cifras">' +
				'<div class="cifra"><span>Tienes asegurado</span><strong>' + pct + ' %</strong><small>del valor real</small></div>' +
				'<div class="cifra cifra--destacada"><span>Te pagarían aprox.</span><strong>' + euros( conRegla ) + '</strong><small>de un daño de ' + euros( dano ) + '</small></div>' +
				'<div class="cifra ' + ( pierdes > 0 ? 'cifra--mal' : '' ) + '"><span>Pagarías tú</span><strong>' + euros( pierdes ) + '</strong><small>' + ( franquicia ? 'incluida la franquicia' : 'sin franquicia' ) + '</small></div></div>' +
				'<div class="barra-proporcion" aria-hidden="true"><span style="width:' + Math.round( ( conRegla / dano ) * 100 ) + '%"></span></div>' +
				'<p class="resultado__veredicto resultado__veredicto--' + ( infra ? 'mal' : 'bien' ) + '">' +
				( infra
					? '<strong>Estás infraasegurado.</strong> Como solo cubres el ' + pct + ' % del valor, te pagan ese mismo porcentaje del daño. Para evitarlo, revisa la suma asegurada con tu aseguradora o busca una póliza a primer riesgo o con cláusula de no aplicación de la regla proporcional.'
					: '<strong>Sin regla proporcional.</strong> ' + ( primer ? 'Con una póliza a primer riesgo te pagan el daño hasta el capital contratado.' : 'Tu suma asegurada cubre el valor real.' ) ) +
				'</p>';
		}
		raiz.addEventListener( 'input', calcular );
		raiz.addEventListener( 'change', calcular );
		calcular();
	}

	/* Generador de cartas -------------------------------------------- */
	function v( raiz, nombre, porDefecto ) {
		var x = campo( raiz, nombre );
		return x ? x : '[' + porDefecto + ']';
	}
	function fechaCampo( raiz, nombre, porDefecto ) {
		var f = leerFecha( campo( raiz, nombre ) );
		return f ? f.getDate() + ' de ' + MESES[ f.getMonth() ] + ' de ' + f.getFullYear() : '[' + porDefecto + ']';
	}
	function cabecera( raiz, destinatario ) {
		var hoy = new Date();
		return v( raiz, 'nombre', 'Tu nombre y apellidos' ) + '\nDNI: ' + v( raiz, 'dni', 'DNI' ) + '\n' + v( raiz, 'direccion', 'Tu dirección' ) + '\n' + v( raiz, 'email', 'Tu correo' ) +
			'\n\n' + destinatario + ' de ' + v( raiz, 'aseguradora', 'nombre de la aseguradora' ) +
			'\n\n[Lugar], a ' + hoy.getDate() + ' de ' + MESES[ hoy.getMonth() ] + ' de ' + hoy.getFullYear() + '\n\n';
	}
	var MODELOS = {
		reclamacion: function ( r ) {
			return cabecera( r, 'A la atención del Servicio de Atención al Cliente' ) +
				'Asunto: Reclamación. Póliza n.º ' + v( r, 'poliza', 'n.º de póliza' ) + ', siniestro n.º ' + v( r, 'siniestro', 'n.º de siniestro' ) + '\n\n' +
				'El ' + fechaCampo( r, 'fecha_sin', 'fecha del siniestro' ) + ' se produjo el siguiente siniestro, que comuniqué en plazo: ' + v( r, 'hechos', 'describe brevemente lo ocurrido' ) + '\n\n' +
				'No estoy de acuerdo con la respuesta recibida, por lo que, al amparo de la normativa de atención a la clientela de las entidades aseguradoras, presento esta reclamación y SOLICITO: ' + v( r, 'peticion', 'lo que pides: pago de X €, reparación, revisión del peritaje…' ) + '\n\n' +
				'Les ruego que acusen recibo de esta reclamación y la resuelvan por escrito y de forma motivada en el plazo máximo de un mes. Transcurrido ese plazo sin respuesta satisfactoria, acudiré al Servicio de Reclamaciones de la Dirección General de Seguros y Fondos de Pensiones.\n\n' +
				'Adjunto: [fotos, facturas, informes, comunicaciones previas].\n\nAtentamente,\n\n' + v( r, 'nombre', 'Firma' );
		},
		rechazo: function ( r ) {
			return cabecera( r, 'A la atención del Departamento de Siniestros' ) +
				'Asunto: Solicitud de respuesta escrita y documentación. Póliza n.º ' + v( r, 'poliza', 'n.º de póliza' ) + ', siniestro n.º ' + v( r, 'siniestro', 'n.º de siniestro' ) + '\n\n' +
				'En relación con el siniestro del ' + fechaCampo( r, 'fecha_sin', 'fecha del siniestro' ) + ' (' + v( r, 'hechos', 'breve descripción' ) + '), se me ha comunicado verbalmente que no será atendido.\n\n' +
				'SOLICITO que me remitan por escrito:\n1. La decisión sobre el siniestro y sus motivos, indicando la cláusula de la póliza en la que se basa.\n2. Copia del informe pericial.\n3. Copia de las condiciones generales, particulares y especiales vigentes en la fecha del siniestro.\n\n' +
				'Quedo a la espera de su respuesta.\n\nAtentamente,\n\n' + v( r, 'nombre', 'Firma' );
		},
		renovacion: function ( r ) {
			return cabecera( r, 'A la atención de' ) +
				'Asunto: Oposición a la prórroga de la póliza n.º ' + v( r, 'poliza', 'n.º de póliza' ) + '\n\n' +
				'Por medio de la presente les comunico, conforme al artículo 22 de la Ley 50/1980, de Contrato de Seguro, mi voluntad de NO prorrogar la póliza indicada, cuyo periodo en curso vence el ' + fechaCampo( r, 'vencimiento', 'fecha de vencimiento' ) + '.\n\n' +
				'Les ruego que no emitan ni carguen ningún recibo posterior a esa fecha y que me confirmen por escrito la recepción de esta comunicación.\n\nAtentamente,\n\n' + v( r, 'nombre', 'Firma' );
		},
		intereses: function ( r ) {
			return cabecera( r, 'A la atención del Servicio de Atención al Cliente' ) +
				'Asunto: Reclamación de intereses de demora. Póliza n.º ' + v( r, 'poliza', 'n.º de póliza' ) + ', siniestro n.º ' + v( r, 'siniestro', 'n.º de siniestro' ) + '\n\n' +
				'El siniestro se produjo el ' + fechaCampo( r, 'fecha_sin', 'fecha del siniestro' ) + ' y la indemnización de ' + v( r, 'importe', 'importe' ) + ' € no fue satisfecha en el plazo de tres meses.\n\n' +
				'Conforme al artículo 20 de la Ley 50/1980, de Contrato de Seguro, SOLICITO el abono de los intereses de demora correspondientes desde la fecha del siniestro hasta la fecha de pago.\n\n' +
				'Les ruego que acusen recibo y resuelvan por escrito en el plazo máximo de un mes.\n\nAtentamente,\n\n' + v( r, 'nombre', 'Firma' );
		}
	};
	function iniciarCarta( raiz ) {
		function actualizar() {
			var modelo = campo( raiz, 'modelo' ) || 'reclamacion';
			$$( '[data-solo]', raiz ).forEach( function ( l ) {
				l.hidden = -1 === l.getAttribute( 'data-solo' ).split( ' ' ).indexOf( modelo );
			} );
			$( '[data-salida]', raiz ).textContent = MODELOS[ modelo ]( raiz );
		}
		raiz.addEventListener( 'input', actualizar );
		raiz.addEventListener( 'change', actualizar );
		$( '[data-copiar-generada]', raiz ).addEventListener( 'click', function () {
			var b = this;
			copiar( $( '[data-salida]', raiz ).textContent, function ( ok ) {
				var et = $( '.boton-copiar__texto', b );
				et.textContent = ok ? '¡Copiada!' : 'Selecciona y copia';
				b.classList.toggle( 'is-copiado', ok );
				setTimeout( function () {
					et.textContent = 'Copiar';
					b.classList.remove( 'is-copiado' );
				}, 2200 );
			} );
		} );
		$( '[data-descargar]', raiz ).addEventListener( 'click', function () {
			descargar( $( '[data-salida]', raiz ).textContent, 'carta-' + ( campo( raiz, 'modelo' ) || 'espabilao' ) + '.txt', 'text/plain' );
		} );
		$( '[data-imprimir]', raiz ).addEventListener( 'click', function () {
			window.print();
		} );
		actualizar();
	}

	/* Detector de letra pequeña -------------------------------------- */
	var ALERTAS = [
		{ r: /(?:quedan?|quedarán|estarán?|serán?) excluid[oa]s?|exclusi(?:ón|ones)|no (?:queda|quedan|estará|estarán|serán?) cubiert[oa]s?|no se cubre[n]?/gi, n: 'Exclusión', g: 'alta', d: 'Situaciones que la póliza deja fuera. Comprueba si tu caso encaja aquí.' },
		{ r: /\b(?:salvo|excepto|a excepción de|con excepción de|siempre que|siempre y cuando)\b/gi, n: 'Condición o excepción', g: 'media', d: 'Lo que viene después limita la cobertura: léelo despacio.' },
		{ r: /franquicias?/gi, n: 'Franquicia', g: 'alta', d: 'La parte del daño que pagas tú en cada siniestro.' },
		{ r: /(?:periodos? de )?carencias?/gi, n: 'Carencia', g: 'alta', d: 'Tiempo desde la contratación en el que esa cobertura todavía no funciona.' },
		{ r: /l[ií]mite[s]?(?: máximo)?|limitad[oa]s?|hasta un máximo de|con un máximo de|sublímite/gi, n: 'Límite de indemnización', g: 'media', d: 'Tope de lo que te pagan, aunque el daño sea mayor.' },
		{ r: /a primer riesgo/gi, n: 'Primer riesgo', g: 'info', d: 'Te pagan hasta ese capital sin aplicar la regla proporcional. Comprueba que el capital es suficiente.' },
		{ r: /regla proporcional|infraseguro/gi, n: 'Regla proporcional', g: 'alta', d: 'Si aseguraste por menos de lo que vale, te pagan en proporción (art. 30 LCS).' },
		{ r: /valor venal/gi, n: 'Valor venal', g: 'media', d: 'Te pagan lo que valía en el mercado de segunda mano, no lo que cuesta uno nuevo.' },
		{ r: /valor real|depreciaci(?:ón|ones)|uso y antig[üu]edad|desgaste/gi, n: 'Desgaste o depreciación', g: 'media', d: 'Pueden descontar la antigüedad del bien, o negar el siniestro por desgaste.' },
		{ r: /preexistent[ea]s?|preexistencias?|anteriores? a la (?:fecha de )?(?:contrataci[oó]n|efecto)/gi, n: 'Preexistencias', g: 'alta', d: 'Lo que ya tenías antes de contratar suele quedar fuera si no lo declaraste.' },
		{ r: /\bdolo\b|culpa grave|mala fe|negligencia/gi, n: 'Pérdida de cobertura por conducta', g: 'media', d: 'Si se demuestra dolo o culpa grave, pueden negarse a pagar.' },
		{ r: /deber[áa] (?:comunicar|declarar|notificar|aportar)|est[áa] obligad[oa] a|obligaci[oó]n de (?:comunicar|declarar)/gi, n: 'Obligación tuya', g: 'media', d: 'Algo que tienes que hacer tú. Si no lo haces, pueden reducir o negar el pago.' },
		{ r: /pr[óo]rroga|renovaci[oó]n (?:t[áa]cita|autom[áa]tica)|se renovar[áa]/gi, n: 'Renovación automática', g: 'info', d: 'Se renueva sola. Para no renovar, avisa por escrito al menos 1 mes antes (art. 22 LCS).' },
		{ r: /revalorizaci[oó]n|actualizaci[oó]n autom[áa]tica|\bIPC\b/gi, n: 'Subida automática', g: 'info', d: 'El capital o la prima pueden subir cada año sin que lo pidas.' },
		{ r: /copagos?/gi, n: 'Copago', g: 'media', d: 'Pagas una cantidad cada vez que usas un servicio.' },
		{ r: /cuadro m[ée]dico|centros? concertados?|red de (?:proveedores|talleres|profesionales)/gi, n: 'Red concertada', g: 'info', d: 'Solo cubren al 100 % si usas sus profesionales o talleres.' },
		{ r: /cl[áa]usulas? limitativas?/gi, n: 'Cláusula limitativa', g: 'alta', d: 'Recorta tus derechos: debe estar destacada y firmada por ti (art. 3 LCS).' },
		{ r: /\d+(?:[.,]\d+)?\s?(?:€|euros)/gi, n: 'Importe', g: 'info', d: 'Cifra concreta: compárala con lo que necesitarías de verdad.' },
		{ r: /\d+\s?(?:d[ií]as|meses|años|horas)/gi, n: 'Plazo', g: 'info', d: 'Un plazo que debes vigilar. Anótalo o usa la calculadora de plazos.' }
	];
	var EJEMPLO = 'Quedan excluidos los daños producidos por filtraciones o humedades debidas al desgaste notorio de las conducciones. En la garantía de daños por agua se aplicará una franquicia de 300 euros por siniestro. Las joyas quedan cubiertas a primer riesgo con un límite máximo de 1.500 €, salvo que se encuentren en caja fuerte. El asegurado deberá comunicar el siniestro en un plazo de 7 días. La póliza se renovará automáticamente por periodos anuales y el capital se actualizará conforme al IPC.';

	function iniciarDetector( raiz ) {
		var glosario = [];
		try {
			glosario = JSON.parse( $( '[data-glosario]', raiz ).textContent || '[]' );
		} catch ( e ) {
			glosario = [];
		}
		function analizar() {
			var texto = campo( raiz, 'texto' );
			var salida = $( '[data-salida]', raiz );
			if ( ! texto ) {
				salida.innerHTML = '<p class="resultado__vacio">Pega un texto para analizarlo.</p>';
				return;
			}
			var marcas = [];
			ALERTAS.forEach( function ( a, i ) {
				a.r.lastIndex = 0;
				var m;
				while ( ( m = a.r.exec( texto ) ) ) {
					marcas.push( { ini: m.index, fin: m.index + m[ 0 ].length, tipo: i, g: a.g } );
					if ( ! m[ 0 ].length ) {
						a.r.lastIndex++;
					}
				}
			} );
			glosario.forEach( function ( t, i ) {
				t.f.forEach( function ( forma ) {
					var re = new RegExp( '(^|[^\\p{L}\\p{N}])(' + forma.replace( /[.*+?^${}()|[\]\\]/g, '\\$&' ) + ')(?:e?s)?(?![\\p{L}\\p{N}])', 'giu' );
					var m;
					while ( ( m = re.exec( texto ) ) ) {
						var ini = m.index + m[ 1 ].length;
						marcas.push( { ini: ini, fin: ini + m[ 2 ].length, glosa: i, g: 'glosa' } );
					}
				} );
			} );
			// Quitar solapes: gana la marca que empieza antes y, a igualdad, la más larga.
			marcas.sort( function ( a, b ) {
				return a.ini - b.ini || ( b.fin - b.ini ) - ( a.fin - a.ini );
			} );
			var limpias = [];
			var hasta = -1;
			marcas.forEach( function ( m ) {
				if ( m.ini >= hasta ) {
					limpias.push( m );
					hasta = m.fin;
				}
			} );
			var html = '';
			var pos = 0;
			var cuenta = {};
			limpias.forEach( function ( m ) {
				html += esc( texto.slice( pos, m.ini ) );
				var trozo = esc( texto.slice( m.ini, m.fin ) );
				if ( undefined !== m.glosa ) {
					var g = glosario[ m.glosa ];
					html += '<mark class="marca marca--glosa" title="' + esc( g.t + ': ' + g.d ) + '">' + trozo + '</mark>';
					cuenta[ 'g' + m.glosa ] = { n: g.t, d: g.d, g: 'glosa', u: g.u, c: ( cuenta[ 'g' + m.glosa ] ? cuenta[ 'g' + m.glosa ].c : 0 ) + 1 };
				} else {
					var a = ALERTAS[ m.tipo ];
					html += '<mark class="marca marca--' + a.g + '" title="' + esc( a.n + ': ' + a.d ) + '">' + trozo + '</mark>';
					cuenta[ 'a' + m.tipo ] = { n: a.n, d: a.d, g: a.g, c: ( cuenta[ 'a' + m.tipo ] ? cuenta[ 'a' + m.tipo ].c : 0 ) + 1 };
				}
				pos = m.fin;
			} );
			html += esc( texto.slice( pos ) );
			var lista = Object.keys( cuenta ).map( function ( k ) {
				return cuenta[ k ];
			} );
			var orden = { alta: 0, media: 1, glosa: 2, info: 3 };
			lista.sort( function ( a, b ) {
				return orden[ a.g ] - orden[ b.g ];
			} );
			var altas = lista.filter( function ( x ) {
				return 'alta' === x.g;
			} ).length;
			salida.innerHTML =
				'<div class="detector__resumen"><strong>' + lista.length + ' puntos a revisar</strong>' + ( altas ? ' · <span class="detector__alerta">' + altas + ' importantes</span>' : '' ) + '</div>' +
				'<div class="detector__texto">' + html.replace( /\n/g, '<br>' ) + '</div>' +
				'<ul class="detector__lista">' + lista.map( function ( x ) {
					return '<li class="detector__item detector__item--' + x.g + '"><span class="detector__nombre">' + esc( x.n ) + ( x.c > 1 ? ' ×' + x.c : '' ) + '</span><span>' + esc( x.d ) + ( x.u ? ' <a href="' + esc( x.u ) + '">Glosario</a>' : '' ) + '</span></li>';
				} ).join( '' ) + '</ul>' +
				'<p class="detector__leyenda"><span class="marca marca--alta">importante</span> <span class="marca marca--media">a vigilar</span> <span class="marca marca--glosa">término del glosario</span> <span class="marca marca--info">dato</span></p>';
		}
		$( '[data-analizar]', raiz ).addEventListener( 'click', analizar );
		$( '[data-ejemplo]', raiz ).addEventListener( 'click', function () {
			$( '[data-campo="texto"]', raiz ).value = EJEMPLO;
			analizar();
		} );
	}

	/* Utilidades ------------------------------------------------------ */
	function descargar( contenido, nombre, tipo ) {
		var blob = new Blob( [ contenido ], { type: tipo + ';charset=utf-8' } );
		var a = document.createElement( 'a' );
		a.href = URL.createObjectURL( blob );
		a.download = nombre;
		document.body.appendChild( a );
		a.click();
		setTimeout( function () {
			URL.revokeObjectURL( a.href );
			a.remove();
		}, 500 );
	}
	function copiar( texto, cb ) {
		if ( navigator.clipboard && window.isSecureContext ) {
			navigator.clipboard.writeText( texto ).then( function () {
				cb( true );
			}, function () {
				cb( false );
			} );
			return;
		}
		var t = document.createElement( 'textarea' );
		t.value = texto;
		document.body.appendChild( t );
		t.select();
		var ok = false;
		try {
			ok = document.execCommand( 'copy' );
		} catch ( e ) {
			ok = false;
		}
		t.remove();
		cb( ok );
	}

	var iniciar = { plazos: iniciarPlazos, infraseguro: iniciarInfraseguro, carta: iniciarCarta, detector: iniciarDetector };
	$$( '[data-herramienta]' ).forEach( function ( raiz ) {
		var f = iniciar[ raiz.getAttribute( 'data-herramienta' ) ];
		if ( f ) {
			f( raiz );
		}
	} );
}() );
