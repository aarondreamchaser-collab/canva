/**
 * Espabilao: glosario emergente y botón «Copiar carta». Sin dependencias.
 */
( function () {
	'use strict';

	/* Glosario --------------------------------------------------------- */
	var abierto = null;

	function cerrar( devolverFoco ) {
		if ( ! abierto ) {
			return;
		}
		var def = document.getElementById( abierto.getAttribute( 'aria-controls' ) );
		abierto.setAttribute( 'aria-expanded', 'false' );
		if ( def ) {
			def.hidden = true;
			def.style.left = '';
		}
		if ( devolverFoco ) {
			abierto.focus();
		}
		abierto = null;
	}

	function abrir( boton ) {
		cerrar( false );
		var def = document.getElementById( boton.getAttribute( 'aria-controls' ) );
		if ( ! def ) {
			return;
		}
		def.hidden = false;
		boton.setAttribute( 'aria-expanded', 'true' );
		abierto = boton;
		// En escritorio, que no se salga por la derecha.
		if ( window.matchMedia( '(min-width: 600px)' ).matches ) {
			var r = def.getBoundingClientRect();
			var sobra = r.right - ( document.documentElement.clientWidth - 12 );
			if ( sobra > 0 ) {
				def.style.left = ( -sobra ) + 'px';
			}
		}
	}

	document.addEventListener( 'click', function ( e ) {
		var boton = e.target.closest ? e.target.closest( '.glosa__termino' ) : null;
		if ( boton ) {
			e.preventDefault();
			if ( boton === abierto ) {
				cerrar( false );
			} else {
				abrir( boton );
			}
			return;
		}
		if ( abierto && ! e.target.closest( '.glosa__def' ) ) {
			cerrar( false );
		}
	} );

	document.addEventListener( 'keydown', function ( e ) {
		if ( 'Escape' === e.key && abierto ) {
			cerrar( true );
		}
	} );

	/* Copiar carta ----------------------------------------------------- */
	function textoDeCarta( carta ) {
		var partes = [];
		Array.prototype.forEach.call( carta.querySelectorAll( 'p, li, pre' ), function ( el ) {
			if ( el.closest( '.esp-carta__barra, .esp-carta__nota' ) || el.parentElement.closest( 'li' ) ) {
				return;
			}
			var t = ( el.innerText || el.textContent || '' ).trim();
			if ( t ) {
				partes.push( 'LI' === el.tagName ? '- ' + t : t );
			}
		} );
		return partes.join( '\n\n' );
	}

	function copiarAntiguo( texto ) {
		var area = document.createElement( 'textarea' );
		area.value = texto;
		area.setAttribute( 'readonly', '' );
		area.style.position = 'fixed';
		area.style.opacity = '0';
		document.body.appendChild( area );
		area.select();
		var ok = false;
		try {
			ok = document.execCommand( 'copy' );
		} catch ( err ) {
			ok = false;
		}
		document.body.removeChild( area );
		return ok;
	}

	function avisar( boton, ok ) {
		var etiqueta = boton.querySelector( '.boton-copiar__texto' ) || boton;
		var original = boton.getAttribute( 'data-texto' ) || etiqueta.textContent;
		boton.setAttribute( 'data-texto', original );
		etiqueta.textContent = ok ? '¡Copiada!' : 'Selecciona y copia';
		boton.classList.toggle( 'is-copiado', ok );
		window.setTimeout( function () {
			etiqueta.textContent = original;
			boton.classList.remove( 'is-copiado' );
		}, 2200 );
	}

	document.addEventListener( 'click', function ( e ) {
		var boton = e.target.closest ? e.target.closest( '[data-copiar]' ) : null;
		if ( ! boton ) {
			return;
		}
		var carta = boton.closest( '.esp-carta' );
		if ( ! carta ) {
			return;
		}
		var texto = textoDeCarta( carta );
		if ( navigator.clipboard && window.isSecureContext ) {
			navigator.clipboard.writeText( texto ).then( function () {
				avisar( boton, true );
			}, function () {
				avisar( boton, copiarAntiguo( texto ) );
			} );
		} else {
			avisar( boton, copiarAntiguo( texto ) );
		}
	} );

	/* Desplegables de la cabecera (buscar y menú) ----------------------- */
	var desplegables = document.querySelectorAll( '.desplegable' );
	Array.prototype.forEach.call( desplegables, function ( d ) {
		d.addEventListener( 'toggle', function () {
			if ( ! d.open ) {
				return;
			}
			Array.prototype.forEach.call( desplegables, function ( otro ) {
				if ( otro !== d ) {
					otro.open = false;
				}
			} );
			var campo = d.querySelector( 'input[type=search]' );
			if ( campo ) {
				campo.focus();
			}
		} );
	} );
	document.addEventListener( 'click', function ( e ) {
		Array.prototype.forEach.call( desplegables, function ( d ) {
			if ( d.open && ! d.contains( e.target ) ) {
				d.open = false;
			}
		} );
	} );
	document.addEventListener( 'keydown', function ( e ) {
		if ( 'Escape' !== e.key ) {
			return;
		}
		Array.prototype.forEach.call( desplegables, function ( d ) {
			if ( d.open ) {
				d.open = false;
				d.querySelector( 'summary' ).focus();
			}
		} );
	} );

	/* Megamenú «Seguros» ------------------------------------------- */
	var mega = document.querySelector( '.mega__boton' );
	if ( mega ) {
		var li = mega.parentNode;
		mega.addEventListener( 'click', function ( e ) {
			e.stopPropagation();
			var abierto = 'true' === mega.getAttribute( 'aria-expanded' );
			mega.setAttribute( 'aria-expanded', abierto ? 'false' : 'true' );
			li.classList.toggle( 'is-abierto', ! abierto );
		} );
		document.addEventListener( 'click', function ( e ) {
			if ( ! li.contains( e.target ) ) {
				mega.setAttribute( 'aria-expanded', 'false' );
				li.classList.remove( 'is-abierto' );
			}
		} );
		document.addEventListener( 'keydown', function ( e ) {
			if ( 'Escape' === e.key && li.classList.contains( 'is-abierto' ) ) {
				mega.setAttribute( 'aria-expanded', 'false' );
				li.classList.remove( 'is-abierto' );
				mega.focus();
			}
		} );
	}

	/* Barra de progreso de lectura (solo artículos) ----------------- */
	var barra = document.querySelector( '.progreso span' );
	var cuerpo = document.querySelector( '.single .contenido' );
	if ( barra && cuerpo ) {
		document.documentElement.classList.add( 'con-progreso' );
		var pendiente = false;
		var medir = function () {
			pendiente = false;
			var r = cuerpo.getBoundingClientRect();
			var total = r.height - window.innerHeight * 0.6;
			var hecho = Math.min( 1, Math.max( 0, -r.top / ( total > 0 ? total : 1 ) ) );
			barra.style.transform = 'scaleX(' + hecho + ')';
		};
		window.addEventListener( 'scroll', function () {
			if ( ! pendiente ) {
				pendiente = true;
				window.requestAnimationFrame( medir );
			}
		}, { passive: true } );
		medir();
	}

	/* Escuchar el artículo (síntesis de voz del navegador) ------------ */
	var escuchar = document.querySelector( '[data-escuchar]' );
	if ( escuchar && 'speechSynthesis' in window && cuerpo ) {
		escuchar.hidden = false;
		var hablando = false;
		var etiqueta = escuchar.querySelector( 'span' );
		var parar = function () {
			window.speechSynthesis.cancel();
			hablando = false;
			etiqueta.textContent = 'Escuchar';
			escuchar.classList.remove( 'is-activo' );
		};
		escuchar.addEventListener( 'click', function () {
			if ( hablando ) {
				parar();
				return;
			}
			var clon = cuerpo.cloneNode( true );
			Array.prototype.forEach.call( clon.querySelectorAll( '.anuncio, .glosa__def, .esp-carta__barra, script, style' ), function ( n ) {
				n.remove();
			} );
			var titulo = document.querySelector( '.articulo__titulo' );
			var texto = ( titulo ? titulo.textContent + '. ' : '' ) + clon.textContent.replace( /\s+/g, ' ' );
			// Trozos cortos: algunos navegadores cortan las locuciones largas.
			var trozos = texto.match( /[^.!?]+[.!?]+|[^.!?]+$/g ) || [ texto ];
			var voces = window.speechSynthesis.getVoices().filter( function ( v ) {
				return /^es(-|_)ES/i.test( v.lang );
			} );
			trozos.forEach( function ( t, i ) {
				var u = new window.SpeechSynthesisUtterance( t.trim() );
				u.lang = 'es-ES';
				if ( voces[ 0 ] ) {
					u.voice = voces[ 0 ];
				}
				if ( i === trozos.length - 1 ) {
					u.onend = parar;
				}
				window.speechSynthesis.speak( u );
			} );
			hablando = true;
			etiqueta.textContent = 'Parar';
			escuchar.classList.add( 'is-activo' );
		} );
		window.addEventListener( 'pagehide', parar );
	}

	/* Compartir e imprimir ------------------------------------------- */
	var compartir = document.querySelector( '[data-compartir]' );
	if ( compartir ) {
		compartir.addEventListener( 'click', function () {
			var url = compartir.getAttribute( 'data-url' );
			var titulo = compartir.getAttribute( 'data-titulo' );
			var et = compartir.querySelector( 'span' );
			if ( navigator.share ) {
				navigator.share( { title: titulo, url: url } ).catch( function () {} );
				return;
			}
			var hecho = function () {
				et.textContent = '¡Enlace copiado!';
				setTimeout( function () {
					et.textContent = 'Compartir';
				}, 2000 );
			};
			if ( navigator.clipboard && window.isSecureContext ) {
				navigator.clipboard.writeText( url ).then( hecho, function () {} );
			} else {
				window.prompt( 'Copia el enlace:', url );
			}
		} );
	}
	var imprimir = document.querySelector( '[data-imprimir-articulo]' );
	if ( imprimir ) {
		imprimir.addEventListener( 'click', function () {
			window.print();
		} );
	}

	// Región viva para lectores de pantalla en los botones de copiar.
	Array.prototype.forEach.call( document.querySelectorAll( '[data-copiar]' ), function ( b ) {
		b.setAttribute( 'aria-live', 'polite' );
	} );
}() );
