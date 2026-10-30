shader_type canvas_item;
render_mode unshaded;

uniform float hurt_amount : hint_range(0.0, 1.0) = 0.0;
uniform vec4 hurt_color : source_color = vec4(1.0, 1.0, 0.0, 1.0);

void fragment() {
	COLOR.rgb = mix(COLOR.rgb, hurt_color.rgb, hurt_amount);
}
