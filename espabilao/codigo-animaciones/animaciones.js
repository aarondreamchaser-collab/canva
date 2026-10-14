/* ESPABILAO · Animaciones (JavaScript). Pegar en WPCode como fragmento JavaScript, ubicación: pie de página */
/**
 * Espabilao · capa de movimiento.
 * Sin librerías. Se apaga sola con «reducir movimiento» y nunca oculta
 * contenido si el JavaScript falla: las clases se añaden desde aquí.
 */
( function () {
	'use strict';

	var html = document.documentElement;
	var reducir = window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
	var punteroFino = window.matchMedia( '(hover: hover) and (pointer: fine)' ).matches;

	// Evita que se ejecute dos veces (por ejemplo, si el tema ya trae las animaciones).
	if ( window.espabilaoMovimientoActivo || document.querySelector( 'script[src*="movimiento.js"]' ) ) {
		return;
	}
	window.espabilaoMovimientoActivo = true;

	if ( reducir ) {
		html.classList.remove( 'movimiento' );
		return;
	}
	html.classList.add( 'movimiento' );

	function todos( sel, ctx ) {
		return Array.prototype.slice.call( ( ctx || document ).querySelectorAll( sel ) );
	}

	/* 1. Aparición al desplazarse, escalonada por grupos ------------- */
	var GRUPOS = [
		'.bloque__cabecera', '.garantias > li', '.herramientas-rejilla > li', '.tipos--rejilla > li',
		'.secciones > li', '.tarjetas > .tarjeta', '.marcador', '.lista > .fila', '.lateral > .caja',
		'.banda-reclamar__texto', '.mini-escalera > li', '.faq__item', '.nube > li', '.hub__datos > .dato',
		'.hub__saltos > a', '.plazos__lista > .plazo', '.escalera__pasos > .peldano', '.esp-carta', '.esp-poliza',
		'.autor', '.fuentes', '.ficha-caso__dato', '.e404__salidas', '.pie__mapa > nav', '.archivo__cabecera',
		'.relacionados .bloque__cabecera'
	];
	var alto = window.innerHeight;
	var revelables = [];
	todos( GRUPOS.join( ',' ) ).forEach( function ( el ) {
		// Lo que ya se ve al cargar no se anima (no retrasa la primera pintura).
		if ( el.getBoundingClientRect().top < alto * 0.92 ) {
			return;
		}
		var hermanos = el.parentNode ? Array.prototype.indexOf.call( el.parentNode.children, el ) : 0;
		el.style.setProperty( '--retraso', ( Math.max( 0, hermanos ) % 6 ) * 70 + 'ms' );
		el.classList.add( 'revelar' );
		revelables.push( el );
	} );

	/* 2. Sellos de veredicto que «golpean» al aparecer --------------- */
	var sellos = todos( '.veredicto--grande, .veredicto--flotante, .ficha-caso .veredicto' );
	sellos.forEach( function ( s ) {
		s.classList.add( 'sello-espera' );
	} );

	/* 3. Iconos que se dibujan solos ---------------------------------- */
	var iconos = todos( '.tipos--rejilla .tipos__icono svg, .herramienta-tarjeta__icono svg, .seccion__icono svg, .hub__icono svg, .garantias svg' );
	iconos.forEach( function ( svg ) {
		todos( 'path, circle, rect, line, polyline', svg ).forEach( function ( forma ) {
			forma.setAttribute( 'pathLength', '1' );
		} );
		svg.classList.add( 'dibujar' );
	} );

	/* 4. Contadores que suben ----------------------------------------- */
	var contadores = todos( '.dato strong, .seccion__n, .tipos__n' ).filter( function ( el ) {
		return /\d/.test( el.textContent ) && el.getBoundingClientRect().top > alto;
	} );
	// Reservar el ancho final antes de contar (fuera de pantalla) para que nada se mueva.
	contadores.forEach( function ( el ) {
		if ( 'inline' === window.getComputedStyle( el ).display ) {
			el.style.display = 'inline-block';
		}
		el.style.minWidth = el.getBoundingClientRect().width + 'px';
	} );
	function contar( el ) {
		var nodo = null;
		// Solo el primer nodo de texto con número (respeta iconos y textos ocultos).
		var paseo = document.createTreeWalker( el, NodeFilter.SHOW_TEXT );
		while ( paseo.nextNode() ) {
			if ( /\d/.test( paseo.currentNode.nodeValue ) ) {
				nodo = paseo.currentNode;
				break;
			}
		}
		if ( ! nodo ) {
			return;
		}
		var original = nodo.nodeValue;
		var m = original.match( /\d+/ );
		var fin = parseInt( m[ 0 ], 10 );
		if ( ! fin ) {
			return;
		}
		var inicio = null;
		var paso = function ( t ) {
			if ( null === inicio ) {
				inicio = t;
			}
			var p = Math.min( 1, ( t - inicio ) / 900 );
			var suave = 1 - Math.pow( 1 - p, 3 );
			nodo.nodeValue = original.replace( m[ 0 ], String( Math.round( fin * suave ) ) );
			if ( p < 1 ) {
				window.requestAnimationFrame( paso );
			} else {
				nodo.nodeValue = original;
			}
		};
		window.requestAnimationFrame( paso );
	}

	/* Observador común ------------------------------------------------- */
	var objetivos = revelables.concat( sellos, iconos, contadores, todos( '.marcador, .dato--ancho' ) );
	if ( 'IntersectionObserver' in window ) {
		var obs = new IntersectionObserver( function ( entradas ) {
			entradas.forEach( function ( e ) {
				if ( ! e.isIntersecting ) {
					return;
				}
				var el = e.target;
				el.classList.add( 'es-visible' );
				if ( contadores.indexOf( el ) > -1 ) {
					contar( el );
				}
				obs.unobserve( el );
			} );
		}, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 } );
		objetivos.forEach( function ( el ) {
			obs.observe( el );
		} );
	} else {
		objetivos.forEach( function ( el ) {
			el.classList.add( 'es-visible' );
		} );
	}

	/* 5. Cabecera inteligente: se esconde al bajar y vuelve al subir --- */
	var cabecera = document.querySelector( '.cabecera' );
	if ( cabecera ) {
		var ultimo = window.scrollY;
		var pendiente = false;
		var revisar = function () {
			pendiente = false;
			var y = window.scrollY;
			var abierto = document.querySelector( '.desplegable[open], .mega.is-abierto' );
			cabecera.classList.toggle( 'is-scroll', y > 8 );
			if ( ! abierto && y > 420 && y > ultimo + 6 ) {
				cabecera.classList.add( 'is-oculta' );
			} else if ( y < ultimo - 6 || y < 420 ) {
				cabecera.classList.remove( 'is-oculta' );
			}
			ultimo = y;
		};
		window.addEventListener( 'scroll', function () {
			if ( ! pendiente ) {
				pendiente = true;
				window.requestAnimationFrame( revisar );
			}
		}, { passive: true } );
		cabecera.addEventListener( 'focusin', function () {
			cabecera.classList.remove( 'is-oculta' );
		} );
	}

	/* 6. Foco de luz que sigue al ratón en las tarjetas ----------------- */
	if ( punteroFino ) {
		todos( '.herramienta-tarjeta a, .tipos--rejilla a, .seccion a, .tarjeta, .caja--crema' ).forEach( function ( el ) {
			el.classList.add( 'con-foco' );
			el.addEventListener( 'pointermove', function ( e ) {
				var r = el.getBoundingClientRect();
				el.style.setProperty( '--mx', ( e.clientX - r.left ) + 'px' );
				el.style.setProperty( '--my', ( e.clientY - r.top ) + 'px' );
			} );
		} );

		/* 7. Efecto 3D en el caso destacado y la tarjeta de 404 --------- */
		todos( '.caso-destacado, .e404__poliza' ).forEach( function ( el ) {
			el.classList.add( 'con-3d' );
			el.addEventListener( 'pointermove', function ( e ) {
				var r = el.getBoundingClientRect();
				var x = ( e.clientX - r.left ) / r.width - 0.5;
				var y = ( e.clientY - r.top ) / r.height - 0.5;
				el.style.setProperty( '--rx', ( -y * 7 ).toFixed( 2 ) + 'deg' );
				el.style.setProperty( '--ry', ( x * 9 ).toFixed( 2 ) + 'deg' );
			} );
			el.addEventListener( 'pointerleave', function () {
				el.style.setProperty( '--rx', '0deg' );
				el.style.setProperty( '--ry', '0deg' );
			} );
		} );

		/* 8. Botones magnéticos ------------------------------------------ */
		todos( '.boton--naranja, .buscador__boton' ).forEach( function ( b ) {
			b.classList.add( 'magnetico' );
			b.addEventListener( 'pointermove', function ( e ) {
				var r = b.getBoundingClientRect();
				b.style.setProperty( '--tx', ( ( e.clientX - r.left - r.width / 2 ) * 0.18 ).toFixed( 1 ) + 'px' );
				b.style.setProperty( '--ty', ( ( e.clientY - r.top - r.height / 2 ) * 0.25 ).toFixed( 1 ) + 'px' );
			} );
			b.addEventListener( 'pointerleave', function () {
				b.style.setProperty( '--tx', '0px' );
				b.style.setProperty( '--ty', '0px' );
			} );
		} );
	}

	/* 9. Buscador de portada que escribe preguntas solo ----------------- */
	var campo = document.querySelector( '.hero__buscador .buscador__campo' );
	// Edita aquí las preguntas que se escriben solas en el buscador de la portada.
	var preguntas = window.espabilaoPreguntas || [
		'¿Me cubre una gotera del vecino?',
		'¿Me pagan la luna rota del coche?',
		'¿Qué es la franquicia?',
		'¿Cómo no renuevo mi seguro?',
		'¿Cubre la baja médica?'
	];
	if ( campo && preguntas.length ) {
		var original = campo.getAttribute( 'placeholder' );
		var i = 0;
		var letra = 0;
		var borrando = false;
		var parado = false;
		var temporizador = null;
		var escribir = function () {
			if ( parado ) {
				return;
			}
			var frase = preguntas[ i % preguntas.length ];
			if ( ! borrando ) {
				letra++;
				campo.setAttribute( 'placeholder', frase.slice( 0, letra ) );
				if ( letra >= frase.length ) {
					borrando = true;
					temporizador = setTimeout( escribir, 1800 );
					return;
				}
				temporizador = setTimeout( escribir, 45 + Math.random() * 45 );
			} else {
				letra--;
				campo.setAttribute( 'placeholder', frase.slice( 0, letra ) );
				if ( letra <= 0 ) {
					borrando = false;
					i++;
					temporizador = setTimeout( escribir, 350 );
					return;
				}
				temporizador = setTimeout( escribir, 22 );
			}
		};
		var parar = function () {
			parado = true;
			clearTimeout( temporizador );
			campo.setAttribute( 'placeholder', original );
		};
		campo.addEventListener( 'focus', parar );
		campo.addEventListener( 'input', parar );
		// La primera pregunta empieza cuando la página ya está pintada.
		temporizador = setTimeout( escribir, 1400 );
		document.addEventListener( 'visibilitychange', function () {
			if ( document.hidden ) {
				clearTimeout( temporizador );
			} else if ( ! parado ) {
				temporizador = setTimeout( escribir, 600 );
			}
		} );
	}

	/* 10. Botón «volver arriba» con anillo de progreso --------------------- */
	var arriba = document.createElement( 'button' );
	arriba.type = 'button';
	arriba.className = 'volver-arriba';
	arriba.setAttribute( 'aria-label', 'Volver arriba' );
	arriba.innerHTML = '<svg viewBox="0 0 44 44" width="44" height="44" aria-hidden="true"><circle class="volver-arriba__pista" cx="22" cy="22" r="19"/><circle class="volver-arriba__anillo" cx="22" cy="22" r="19" pathLength="1"/><path d="M22 28V16M16.5 21.5 22 16l5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
	document.body.appendChild( arriba );
	var anillo = arriba.querySelector( '.volver-arriba__anillo' );
	var medir = function () {
		var max = document.documentElement.scrollHeight - window.innerHeight;
		var p = max > 0 ? window.scrollY / max : 0;
		anillo.style.strokeDashoffset = String( 1 - p );
		arriba.classList.toggle( 'is-visible', window.scrollY > window.innerHeight * 1.2 );
	};
	window.addEventListener( 'scroll', function () {
		window.requestAnimationFrame( medir );
	}, { passive: true } );
	arriba.addEventListener( 'click', function () {
		window.scrollTo( { top: 0, behavior: 'smooth' } );
	} );
	medir();
}() );
