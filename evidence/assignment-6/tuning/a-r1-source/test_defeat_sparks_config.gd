extends "res://tests/harness.gd"
## Expected values are transcribed from CHANGE-BRIEF.md, not from the scene.

func run() -> void:
	suite = "defeat_sparks_config"
	var scene := load("res://effects/defeat_sparks.tscn") as PackedScene
	check("effect-scene-loads", scene != null)
	if scene == null:
		completed = true
		return
	var node := scene.instantiate()
	check("cpu-2d-node", node is CPUParticles2D)
	var burst := node as CPUParticles2D
	var expected := {
		"amount": 16, "one_shot": true, "emitting": false,
		"explosiveness": 1.0, "lifetime": 0.45, "emission_shape": 0,
		"direction": Vector2(1, 0), "spread": 180.0,
		"initial_velocity_min": 25.0, "initial_velocity_max": 55.0,
		"gravity": Vector2(0, 12), "damping_min": 20.0, "damping_max": 30.0,
		"scale_amount_min": 0.7, "scale_amount_max": 1.8,
		"local_coords": false, "preprocess": 0.0, "use_fixed_seed": false,
	}
	for property in expected:
		var actual = burst.get(property)
		var wanted = expected[property]
		var matches: bool = is_equal_approx(float(actual), float(wanted)) if wanted is float else actual == wanted
		check("setting-" + property, matches, {"actual": str(actual), "expected": str(wanted)})
	check("texture-path", burst.texture != null and burst.texture.resource_path == "res://assets/particles/spark.png")
	if burst.texture:
		var image := burst.texture.get_image()
		check("texture-size", image.get_size() == Vector2i(3, 3))
		var exact := true
		for y in 3:
			for x in 3:
				var wanted := Color(1, 1, 1, 1 if x == 1 or y == 1 else 0)
				exact = exact and image.get_pixel(x, y).is_equal_approx(wanted)
		check("texture-binary-alpha-cross", exact)
	check("nearest-texture-filter", burst.texture_filter == CanvasItem.TEXTURE_FILTER_NEAREST)
	var material := burst.material as CanvasItemMaterial
	check("draw-material-type", material != null)
	check("additive-blend", material != null and material.blend_mode == CanvasItemMaterial.BLEND_MODE_ADD)
	var curve := burst.scale_amount_curve
	check("scale-curve-present", curve != null)
	if curve:
		var points := [Vector2(0, 1), Vector2(0.2, 0.85), Vector2(1, 0)]
		check("scale-curve-count", curve.point_count == points.size())
		for i in mini(curve.point_count, points.size()):
			check("scale-curve-point-%d" % i, curve.get_point_position(i).is_equal_approx(points[i]))
	var gradient := burst.color_ramp
	check("colour-ramp-present", gradient != null)
	if gradient:
		var offsets := [0.0, 0.35, 1.0]
		var colours := [Color(1, 0.95, 0.65, 1), Color(1, 0.6, 0.2, 0.85), Color(0.65, 0.2, 0.05, 0)]
		check("colour-ramp-count", gradient.get_point_count() == 3)
		for i in mini(gradient.get_point_count(), 3):
			check("colour-ramp-offset-%d" % i, is_equal_approx(gradient.get_offset(i), offsets[i]))
			check("colour-ramp-rgba-%d" % i, gradient.get_color(i).is_equal_approx(colours[i]))
	burst.free()
	completed = true
