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
		var original = boton.getAttribute( 'data-texto' ) || boton.textContent;
		boton.setAttribute( 'data-texto', original );
		boton.textContent = ok ? '¡Copiada!' : 'Selecciona y copia';
		boton.classList.toggle( 'is-copiado', ok );
		window.setTimeout( function () {
			boton.textContent = original;
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

	// Región viva para lectores de pantalla en los botones de copiar.
	Array.prototype.forEach.call( document.querySelectorAll( '[data-copiar]' ), function ( b ) {
		b.setAttribute( 'aria-live', 'polite' );
	} );
}() );
