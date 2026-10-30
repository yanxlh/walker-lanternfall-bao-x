shader_type spatial;
render_mode unshaded;

// Assign the same PNG to both samplers in the ShaderMaterial.
uniform sampler2D color_sample : source_color, filter_nearest;
uniform sampler2D raw_sample : filter_nearest;
uniform bool use_color = true;

void fragment() {
	if (use_color) {
		ALBEDO = texture(color_sample, UV).rgb;
	} else {
		ALBEDO = texture(raw_sample, UV).rgb;
	}
}
