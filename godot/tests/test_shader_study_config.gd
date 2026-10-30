extends "res://tests/harness.gd"

func run() -> void:
	suite = "shader_study_config"
	var study := (load("res://previews/shader_study/hit_sparks_gpu.tscn") as PackedScene).instantiate()
	var gpu := study.get_node("HitSparksGPU") as GPUParticles2D
	var cpu := (load("res://effects/defeat_sparks.tscn") as PackedScene).instantiate() as CPUParticles2D
	var mat := gpu.process_material as ShaderMaterial
	check("generated-shader-reference", mat.shader.resource_path == "res://shaders/particles_generated.gdshader")
	var ramp := mat.get_shader_parameter("color_ramp") as GradientTexture1D
	var scale_tex := mat.get_shader_parameter("scale_curve") as CurveTexture
	check("color-ramp-texture-assigned", ramp != null)
	check("scale-curve-texture-assigned", scale_tex != null)
	if ramp:
		check("gradient-point-count", ramp.gradient.get_point_count() == cpu.color_ramp.get_point_count())
		for i in cpu.color_ramp.get_point_count():
			check("gradient-offset-%d" % i, is_equal_approx(ramp.gradient.get_offset(i), cpu.color_ramp.get_offset(i)))
			check("gradient-color-%d" % i, ramp.gradient.get_color(i).is_equal_approx(cpu.color_ramp.get_color(i)))
	if scale_tex:
		check("curve-point-count", scale_tex.curve.get_point_count() == cpu.scale_amount_curve.get_point_count())
		for t in [0.0, 0.1, 0.2, 0.5, 0.8, 1.0]:
			check("scale-sample-%.1f" % t, is_equal_approx(scale_tex.curve.sample(t), cpu.scale_amount_curve.sample(t)))
	check("world-coordinates-match", gpu.local_coords == cpu.local_coords)
	check("amount-match", gpu.amount == cpu.amount)
	check("lifetime-match", is_equal_approx(gpu.lifetime, cpu.lifetime))
	check("study-never-used-in-game", not FileAccess.get_file_as_string("res://game/session.gd").contains("shader_study"))
	study.free()
	cpu.free()
	completed = true
