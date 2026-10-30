shader_type spatial;

uniform sampler2D color_tex : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D normal_tex : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D roughness_tex : filter_linear_mipmap, repeat_enable;

group_uniforms Surface;
uniform vec4 tint : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float uv_scale : hint_range(0.25, 4.0) = 1.0;

group_uniforms Response;
uniform float roughness_min : hint_range(0.0, 1.0) = 0.2;
uniform float roughness_max : hint_range(0.0, 1.0) = 0.8;
uniform float normal_strength : hint_range(0.0, 2.0) = 1.0;
group_uniforms;

void fragment() {
	vec2 uv = UV * uv_scale;
	ALBEDO = texture(color_tex, uv).rgb * tint.rgb;
	ROUGHNESS = mix(roughness_min, roughness_max, texture(roughness_tex, uv).r);
	NORMAL_MAP = texture(normal_tex, uv).rgb;
	NORMAL_MAP_DEPTH = normal_strength;
	METALLIC = 0.0;
}
