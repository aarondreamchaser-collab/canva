/* Usuarios fuera de la API pública.
   WPCode: fragmento PHP nuevo, «Usuarios API privada», ejecutar en todas partes.
   Este archivo se pega entero: ya va sin la etiqueta de apertura de PHP.
   Quien no ha iniciado sesión deja de ver /wp-json/wp/v2/users (el listado y cada usuario).
   Con sesión iniciada o con contraseña de aplicación todo sigue igual: el editor de bloques
   y los scripts de la web usan la API autenticada.
   Para deshacerlo, desactiva el fragmento. */

add_filter( 'rest_endpoints', function ( $endpoints ) {
	if ( is_user_logged_in() ) {
		return $endpoints;
	}
	foreach ( array_keys( $endpoints ) as $ruta ) {
		if ( 0 === strpos( $ruta, '/wp/v2/users' ) ) {
			unset( $endpoints[ $ruta ] );
		}
	}
	return $endpoints;
} );
