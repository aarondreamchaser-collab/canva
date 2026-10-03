// Redirige www.tuluzencasa.com a tuluzencasa.com con un 301, conservando la ruta y los parámetros.
// WPCode: tipo «Fragmento de PHP», inserción automática, ubicación «Ejecutar en todas partes».
add_action( 'init', function () {
	if ( ( defined( 'WP_CLI' ) && WP_CLI ) || wp_doing_cron() ) {
		return;
	}
	$host = isset( $_SERVER['HTTP_HOST'] ) ? strtolower( wp_unslash( $_SERVER['HTTP_HOST'] ) ) : '';
	if ( 'www.tuluzencasa.com' !== $host ) {
		return;
	}
	$ruta = isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '/';
	wp_safe_redirect( 'https://tuluzencasa.com' . $ruta, 301 );
	exit;
}, 1 );
