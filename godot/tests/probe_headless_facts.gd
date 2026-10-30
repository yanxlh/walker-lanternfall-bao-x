extends SceneTree
## Probe for CLAUDE.md "Headless facts": what a headless run on this machine reports about shaders and frames.
## Not a test suite. Pass `-- mutate` to compile hurt_tint.gdshader's source with one semicolon removed, in memory only.

const SHADER_PATH := "res://shaders/hurt_tint.gdshader"
const FRAMES := 288

var process_frames := 0
var physics_frames := 0
var post_draws := 0
var ticks_per_frame: Array[int] = []
var physics_at_last_frame := 0

func _initialize() -> void:
	print("engine ", Engine.get_version_info().string)
	print("rendering driver '", RenderingServer.get_current_rendering_driver_name(), "', method '",
		RenderingServer.get_current_rendering_method(), "', adapter '", RenderingServer.get_video_adapter_name(), "'")
	print("physics_ticks_per_second ", Engine.physics_ticks_per_second, ", max_fps ", Engine.max_fps)
	var shader: Shader = load(SHADER_PATH)
	if "mutate" in OS.get_cmdline_user_args():
		_probe_mutation(shader.code)
		quit()
		return
	_probe_shader(shader)
	physics_frame.connect(func(): physics_frames += 1)
	process_frame.connect(_on_process_frame)
	RenderingServer.frame_post_draw.connect(func(): post_draws += 1)

func _probe_shader(shader: Shader) -> void:
	for u in shader.get_shader_uniform_list():
		print("uniform ", u.name, " type ", u.type, " hint ", u.hint, " hint_string '", u.hint_string, "'")
	for name in ["hurt_amount", "hurt_color"]:
		print("RenderingServer default ", name, " = ", RenderingServer.shader_get_parameter_default(shader.get_rid(), name))
	var mat := ShaderMaterial.new()
	mat.shader = shader
	print("fresh material get_shader_parameter(hurt_amount) = ", mat.get_shader_parameter("hurt_amount"))
	mat.set_shader_parameter("hurt_amout", 0.5)
	print("undeclared hurt_amout set 0.5, read back = ", mat.get_shader_parameter("hurt_amout"))

func _probe_mutation(code: String) -> void:
	var cut := code.rfind(";")
	var broken := Shader.new()
	broken.code = code.substr(0, cut) + code.substr(cut + 1)
	print("mutated: removed the semicolon at offset ", cut, "; uniform list size ", broken.get_shader_uniform_list().size())

func _on_process_frame() -> void:
	process_frames += 1
	ticks_per_frame.append(physics_frames - physics_at_last_frame)
	physics_at_last_frame = physics_frames
	if process_frames == FRAMES:
		var counts := {}
		for n in ticks_per_frame:
			counts[n] = counts.get(n, 0) + 1
		print("after ", FRAMES, " process frames: ", physics_frames, " physics frames; ticks-per-frame histogram ", counts)
		print("frame_post_draw emitted ", post_draws, " times")
		quit()
