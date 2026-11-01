extends Node3D
## Film fixture (agent-made for the Assignment 5 film; isolated copy of the game only, never the repository).
## Two 2 x 2 m planes side by side under one directional light and one orthographic camera:
##   left  — the editor-converted material exactly as saved in res://a5/scratch/standard_conversion.tscn
##           (standard_generated.gdshader, the three cobblestone maps, albedo white, roughness 1, normal_scale 1);
##   right — a new ShaderMaterial on Bao's res://shaders/cobblestone_surface.gdshader with the same three maps and
##           neutral values (tint white, uv_scale 1, roughness 0..1, normal_strength 1), set in memory, never saved.
## Nothing here is gameplay. It renders one picture per camera pose and quits:
##   godot --path . res://shader_pair_fixture.tscn -- <out_dir> [pair | control-generated | control-bao]
## The two controls put the same material on both planes, to show the setup itself treats left and right alike.
## Poses: "straight" (camera looking straight down: the view-space NORMAL of both planes is (0, 0, 1)) and
## "tilted" (the camera pitched 50 degrees off vertical, so abs(NORMAL.z) = cos 50).

const TEX := "res://assets/textures/cobblestone_floor_08/cobblestone_floor_08_%s_1k.png"
const POSES := {"straight": 0.0, "tilted": 50.0}

var out_dir := ""
var camera: Camera3D
var left: MeshInstance3D
var right: MeshInstance3D
var report := {}

func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	out_dir = args[0] if args.size() > 0 else OS.get_user_data_dir()
	var mode: String = args[1] if args.size() > 1 else "pair"
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.055, 0.063, 0.125)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.25, 0.25, 0.25)
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-35.0, -90.0, 0.0)     # low light from +X, so the normal map's relief shows
	sun.light_energy = 1.4
	add_child(sun)
	var scratch: Node = load("res://a5/scratch/standard_conversion.tscn").instantiate()
	var generated: Material = scratch.get_node("Surface").material_override
	var bao := ShaderMaterial.new()
	bao.shader = load("res://shaders/cobblestone_surface.gdshader")
	bao.set_shader_parameter("color_tex", load(TEX % "diff"))
	bao.set_shader_parameter("normal_tex", load(TEX % "nor_gl"))
	bao.set_shader_parameter("roughness_tex", load(TEX % "rough"))
	bao.set_shader_parameter("tint", Color(1, 1, 1, 1))
	bao.set_shader_parameter("uv_scale", 1.0)
	bao.set_shader_parameter("roughness_min", 0.0)
	bao.set_shader_parameter("roughness_max", 1.0)
	bao.set_shader_parameter("normal_strength", 1.0)
	left = _plane(Vector3(-1.1, 0, 0), bao if mode == "control-bao" else generated)
	right = _plane(Vector3(1.1, 0, 0), generated if mode == "control-generated" else bao)
	scratch.free()
	camera = Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 2.5
	add_child(camera)
	camera.current = true
	report = {"engine": Engine.get_version_info().string, "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(), "generated_material": "res://a5/scratch/standard_conversion.tscn :: Surface",
		"bao_material": {"shader": "res://shaders/cobblestone_surface.gdshader", "tint": [1, 1, 1, 1], "uv_scale": 1.0,
			"roughness_min": 0.0, "roughness_max": 1.0, "normal_strength": 1.0},
		"light": {"rotation_degrees": [-35.0, -90.0, 0.0], "energy": 1.4}, "ambient": [0.25, 0.25, 0.25],
		"note": "film fixture, agent-made; parameters set in memory, nothing saved", "mode": mode, "poses": {}}
	for pose in POSES:
		var pitch: float = POSES[pose]
		# Orbit about the X axis so both planes stay at the same depth: left and right stay mirror-placed.
		camera.position = Vector3(0, 5.0 * cos(deg_to_rad(pitch)), 5.0 * sin(deg_to_rad(pitch)))
		camera.rotation_degrees = Vector3(-90.0 + pitch, 0, 0)
		for i in 8:
			await RenderingServer.frame_post_draw
		var img := get_viewport().get_texture().get_image()
		var path := "%s/%s-%s.png" % [out_dir, "shader-pair" if mode == "pair" else mode, pose]
		img.save_png(path)
		report.poses[pose] = {"pitch_deg": pitch, "file": path.get_file(), "size": [img.get_width(), img.get_height()],
			"left_center_px": _px(left.global_position), "right_center_px": _px(right.global_position),
			"abs_normal_z": absf(cos(deg_to_rad(pitch)))}
	var f := FileAccess.open("%s/%s.json" % [out_dir, "shader-pair" if mode == "pair" else mode], FileAccess.WRITE)
	f.store_string(JSON.stringify(report, "  "))
	f.close()
	print("SHADER_PAIR ", JSON.stringify(report))
	get_tree().quit()

func _plane(at: Vector3, m: Material) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.mesh = PlaneMesh.new()          # 2 x 2 m, the same default PlaneMesh as the scratch scene's Surface
	mi.material_override = m
	mi.position = at
	add_child(mi)
	return mi

func _px(p: Vector3) -> Array:
	var v: Vector2 = camera.unproject_position(p)
	var s: Vector2 = Vector2(get_viewport().get_texture().get_size()) / get_viewport().get_visible_rect().size
	return [snappedf(v.x * s.x, 0.1), snappedf(v.y * s.y, 0.1)]
