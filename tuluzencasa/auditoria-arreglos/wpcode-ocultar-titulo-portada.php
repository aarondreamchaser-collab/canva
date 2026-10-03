// Quita el título de la página (H1 «Inicio») solo en la portada. Usa el filtro de GeneratePress.
// Alternativa sin código: editar la página Inicio → panel de GeneratePress → «Desactivar elementos» → «Título del contenido».
// WPCode: tipo «Fragmento de PHP», inserción automática, ubicación «Solo en el frontend».
add_filter( 'generate_show_title', function ( $mostrar ) {
	return is_front_page() ? false : $mostrar;
} );
