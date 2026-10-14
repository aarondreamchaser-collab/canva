<?php
/**
 * Archivo del glosario: todos los términos en orden alfabético.
 *
 * @package Espabilao
 */

get_header();
?>

<div class="envoltorio envoltorio--texto">
	<header class="archivo__cabecera">
		<p class="supra">Glosario</p>
		<h1 class="archivo__titulo">Las palabras con las que te la cuelan</h1>
		<p class="archivo__desc">Los términos de las pólizas, traducidos. En los artículos, pulsa sobre una palabra subrayada para ver su definición.</p>
	</header>

	<?php if ( have_posts() ) : ?>
		<div class="glosario">
		<?php
		$esp_letra = '';
		while ( have_posts() ) :
			the_post();
			$esp_inicial = mb_strtoupper( mb_substr( remove_accents( get_the_title() ), 0, 1 ) );
			if ( $esp_inicial !== $esp_letra ) {
				if ( '' !== $esp_letra ) {
					echo '</dl>';
				}
				$esp_letra = $esp_inicial;
				echo '<h2 class="glosario__letra">' . esc_html( $esp_letra ) . '</h2><dl>';
			}
			?>
			<div class="glosario__item" id="<?php echo esc_attr( get_post_field( 'post_name' ) ); ?>">
				<dt><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></dt>
				<dd><?php echo esc_html( has_excerpt() ? get_the_excerpt() : wp_strip_all_tags( get_the_content() ) ); ?></dd>
			</div>
			<?php
		endwhile;
		echo '</dl>';
		?>
		</div>
	<?php else : ?>
		<p>El glosario está vacío por ahora.</p>
	<?php endif; ?>
</div>

<?php
get_footer();
