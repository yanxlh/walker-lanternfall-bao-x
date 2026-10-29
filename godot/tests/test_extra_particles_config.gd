extends "res://tests/harness.gd"

func inspect_effect(path: String, expected: Dictionary, points: Array, offsets: Array, colours: Array) -> void:
	var effect := (load(path) as PackedScene).instantiate() as CPUParticles2D
	var prefix := path.get_file().get_basename() + "/"
	check(prefix + "cpu-2d", effect != null)
	if effect == null:
		return
	for property in expected:
		var actual = effect.get(property)
		var wanted = expected[property]
		var matches: bool = is_equal_approx(float(actual), float(wanted)) if wanted is float else actual == wanted
		check(prefix + property, matches, {"actual": str(actual), "expected": str(wanted)})
	check(prefix + "texture", effect.texture != null and effect.texture.resource_path == "res://assets/particles/spark.png")
	check(prefix + "nearest", effect.texture_filter == CanvasItem.TEXTURE_FILTER_NEAREST)
	var material := effect.material as CanvasItemMaterial
	check(prefix + "additive-material", material != null and material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD)
	var curve := effect.scale_amount_curve
	check(prefix + "curve-present", curve != null)
	if curve:
		check(prefix + "curve-count", curve.point_count == points.size())
		for i in mini(curve.point_count, points.size()):
			check(prefix + "curve-point-%d" % i, curve.get_point_position(i).is_equal_approx(points[i]))
			check(prefix + "curve-tangents-%d" % i, is_zero_approx(curve.get_point_left_tangent(i)) and is_zero_approx(curve.get_point_right_tangent(i)))
	var ramp := effect.color_ramp
	check(prefix + "ramp-present", ramp != null)
	if ramp:
		check(prefix + "ramp-count", ramp.get_point_count() == offsets.size())
		for i in mini(ramp.get_point_count(), offsets.size()):
			check(prefix + "ramp-offset-%d" % i, is_equal_approx(ramp.get_offset(i), offsets[i]))
			check(prefix + "ramp-colour-%d" % i, ramp.get_color(i).is_equal_approx(colours[i]))
	effect.free()

func run() -> void:
	suite = "extra_particles_config"
	inspect_effect("res://effects/lantern_trail.tscn", {
		"amount": 24, "one_shot": false, "emitting": false,
		"lifetime": 0.35, "explosiveness": 0.0, "preprocess": 0.0,
		"emission_shape": 1, "emission_sphere_radius": 3.0,
		"direction": Vector2(0, -1), "spread": 25.0,
		"initial_velocity_min": 2.0, "initial_velocity_max": 6.0,
		"gravity": Vector2(0, -4), "damping_min": 1.0, "damping_max": 3.0,
		"scale_amount_min": 0.35, "scale_amount_max": 0.7,
		"local_coords": false, "use_fixed_seed": false,
	}, [Vector2(0, 0.7), Vector2(0.2, 1), Vector2(1, 0)],
	[0.0, 0.5, 1.0], [Color(1, 0.7, 0.25, 0.95), Color(0.8, 0.35, 0.08, 0.7), Color(0.3, 0.1, 0.02, 0)])
	inspect_effect("res://effects/level_up_sparks.tscn", {
		"amount": 32, "one_shot": true, "emitting": false,
		"lifetime": 0.7, "explosiveness": 1.0, "preprocess": 0.0,
		"emission_shape": 1, "emission_sphere_radius": 12.0,
		"direction": Vector2(0, -1), "spread": 180.0,
		"initial_velocity_min": 35.0, "initial_velocity_max": 65.0,
		"gravity": Vector2(0, 8), "damping_min": 15.0, "damping_max": 25.0,
		"scale_amount_min": 0.8, "scale_amount_max": 1.5,
		"local_coords": false, "use_fixed_seed": false,
	}, [Vector2(0, 1), Vector2(0.25, 0.9), Vector2(1, 0)],
	[0.0, 0.4, 1.0], [Color(1, 1, 0.8, 1), Color(1, 0.75, 0.2, 0.8), Color(1, 0.4, 0.05, 0)])
	var overlay := (load("res://effects/level_up_overlay.tscn") as PackedScene).instantiate() as CanvasLayer
	check("level-up-overlay-layer-11", overlay != null and overlay.layer == 11)
	overlay.free()
	completed = true
