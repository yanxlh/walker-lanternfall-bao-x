extends SceneTree
## Windowed captures for the A5 materials and the hint experiment (Assignment 5, Use It). Not a suite; the game never
## loads this script. Every parameter change is made in memory on the loaded resources and restored; nothing is saved.
## Capture pattern from the assignment: await RenderingServer.frame_post_draw, then save the viewport image.
## Modes (user args after `--`), one per run:
##   --hint                  hint_experiment.tscn; samples the centre of each band of both quads
##   --pair                  material_room.tscn from the fixed pose below; one capture
##   --sweep                 same pose; each non-texture uniform of the Floor material at low / material value / high
##   --one-material          same pose; Floor uv_scale 2.0 -> 4.0, stand-in rectangle compared pixel by pixel
##   --ambient               same pose; ambient_light_source as loaded (3, Sky) and switched to 2 (Color)
##   --compare-shader LABEL  same pose; one capture into a folder named after LABEL (before/after a shader edit)
## Also `--rev SHA` and `--out DIR`. No input reaches the window: every capture is labelled scripted.
## Writes PNGs, captures.json and CAPTURES.md to captures/a5-materials/<stamp>-<mode>/.

const ROOM := "res://a5/material_room.tscn"
const HINT_SCENE := "res://a5/hint_experiment/hint_experiment.tscn"
## Fixed camera pose for every material-room mode: the stand-in on the left, open floor in front of it.
const POSE_POSITION := Vector3(-0.6, 1.9, 5.2)
const POSE_TARGET := Vector3(-2.8, 0.35, 1.3)
## World points whose projections centre the measuring rectangles.
const FLOOR_POINT := Vector3(-1.4, 0.0, 2.9)
const FLOOR_HALF_PX := 28
const STANDIN_CENTRE := Vector3(-3.5, 0.6, 1.5)
const STANDIN_RADIUS := 0.25
const SETTLE_FRAMES := 12

var mode := ""
var label := ""
var out_dir := ""
var revision := "unknown"
var scene: Node
var camera: Camera3D
var records := []
var rects := {}

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	for m in ["--hint", "--pair", "--sweep", "--one-material", "--ambient", "--compare-shader"]:
		if m in args:
			mode = m.substr(2)
	if mode == "":
		print("pass one of --hint --pair --sweep --one-material --ambient --compare-shader LABEL; got ", args)
		quit(2)
		return
	var at := args.find("--compare-shader")
	if mode == "compare-shader":
		label = args[at + 1] if at + 1 < args.size() and not args[at + 1].begins_with("--") else "unlabelled"
	at = args.find("--rev")
	if at >= 0 and at + 1 < args.size():
		revision = args[at + 1]
	var stamp := Time.get_datetime_string_from_system().replace(":", "").replace("-", "").replace("T", "-")
	var folder := "%s-%s%s" % [stamp, mode, ("-" + label) if label != "" else ""]
	at = args.find("--out")
	out_dir = args[at + 1] if at >= 0 and at + 1 < args.size() else ProjectSettings.globalize_path("res://../captures/a5-materials/" + folder)
	DirAccess.make_dir_recursive_absolute(out_dir)
	AudioServer.set_bus_mute(0, true)
	call_deferred("_main")

func frames(count: int) -> void:
	for n in count:
		await process_frame

func _main() -> void:
	if mode == "hint":
		await _run_hint()
	else:
		await _run_room()
	_write()
	quit()

# --- capture helpers ----------------------------------------------------------------------------

## The assignment's pattern: wait for the frame to be drawn, then read the viewport.
func _capture(file: String) -> Image:
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	img.save_png(out_dir.path_join(file))
	print("captured ", file)
	return img

## Viewport position of a world point, in pixels of the captured image (canvas_items stretch: visible rect -> image).
func _to_px(world: Vector3, img_size: Vector2) -> Vector2i:
	var visible := root.get_visible_rect()
	var scale := img_size / visible.size
	return Vector2i(((camera.unproject_position(world) - visible.position) * scale).round())

func _mean(img: Image, r: Rect2i) -> Array:
	var sum := Vector3.ZERO
	for y in range(r.position.y, r.end.y):
		for x in range(r.position.x, r.end.x):
			var c := img.get_pixel(x, y)
			sum += Vector3(c.r8, c.g8, c.b8)
	var n := float(r.size.x * r.size.y)
	return [snappedf(sum.x / n, 0.01), snappedf(sum.y / n, 0.01), snappedf(sum.z / n, 0.01)]

func _max_diff(a: Image, b: Image, r: Rect2i) -> int:
	var worst := 0
	for y in range(r.position.y, r.end.y):
		for x in range(r.position.x, r.end.x):
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			worst = maxi(worst, maxi(absi(ca.r8 - cb.r8), maxi(absi(ca.g8 - cb.g8), absi(ca.b8 - cb.b8))))
	return worst

func _rect_json(r: Rect2i) -> Array:
	return [r.position.x, r.position.y, r.size.x, r.size.y]

# --- hint experiment ----------------------------------------------------------------------------

func _run_hint() -> void:
	scene = load(HINT_SCENE).instantiate()
	root.add_child(scene)
	camera = scene.get_node("Camera3D")
	await frames(SETTLE_FRAMES)
	var img := await _capture("hint-experiment.png")
	var size := Vector2(img.get_width(), img.get_height())
	var quads := {}
	for qname in ["QuadWithSourceColor", "QuadWithoutHint"]:
		var quad: MeshInstance3D = scene.get_node(qname)
		var mat: ShaderMaterial = quad.material_override
		var bands := []
		# A 3 x 1 quad holds one texel per metre; band centres sit at local x = -1, 0, +1 (left to right on screen).
		for i in 3:
			var world := quad.global_transform * Vector3(float(i) - 1.0, 0.0, 0.0)
			var px := _to_px(world, size)
			var c := img.get_pixelv(px)
			var edge_px := absi(_to_px(quad.global_transform * Vector3(float(i) - 0.5, 0.0, 0.0), size).x - px.x)
			bands.append({"band": ["left", "middle", "right"][i], "pixel": [px.x, px.y], "rgb": [c.r8, c.g8, c.b8],
				"px_to_band_edge": edge_px})
		quads[qname] = {"material": mat.resource_path, "use_color": mat.get_shader_parameter("use_color"), "bands": bands}
	var env: Environment = (scene.get_node("WorldEnvironment") as WorldEnvironment).environment
	records.append({"file": "hint-experiment.png", "image_size": [img.get_width(), img.get_height()], "quads": quads,
		"environment": {"tonemap_mode": env.tonemap_mode, "tonemap_exposure": env.tonemap_exposure, "glow": env.glow_enabled,
			"fog": env.fog_enabled, "adjustment": env.adjustment_enabled}})

# --- material room ------------------------------------------------------------------------------

func _run_room() -> void:
	scene = load(ROOM).instantiate()
	root.add_child(scene)
	await frames(2)
	camera = scene.get_node("Camera3D")
	camera.global_position = POSE_POSITION
	camera.look_at(POSE_TARGET)
	await frames(SETTLE_FRAMES)
	var floor_mat: ShaderMaterial = scene.get_node("Floor/Mesh").material_override
	match mode:
		"pair":
			await _room_capture("pair.png", {})
		"compare-shader":
			await _room_capture("compare-shader-%s.png" % label, {})
		"sweep":
			await _sweep(floor_mat)
		"one-material":
			var base := await _room_capture("one-material-baseline.png", {"floor uv_scale": floor_mat.get_shader_parameter("uv_scale")})
			var before = floor_mat.get_shader_parameter("uv_scale")
			floor_mat.set_shader_parameter("uv_scale", 4.0)
			var changed := await _room_capture("one-material-floor-uv_scale-4.0.png", {"floor uv_scale": 4.0})
			floor_mat.set_shader_parameter("uv_scale", before)
			records[-1]["standin_max_channel_diff_vs_baseline"] = _max_diff(base, changed, rects.standin)
			records[-1]["floor_max_channel_diff_vs_baseline"] = _max_diff(base, changed, rects.floor)
		"ambient":
			var env: Environment = (scene.get_node("WorldEnvironment") as WorldEnvironment).environment
			var loaded := env.ambient_light_source
			var energy := env.ambient_light_energy
			await _room_capture("ambient-source-%d-as-loaded.png" % loaded, {"ambient_light_source": loaded, "sky": env.sky != null, "ambient_light_energy": energy})
			env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
			await _room_capture("ambient-source-%d-color.png" % Environment.AMBIENT_SOURCE_COLOR, {"ambient_light_source": env.ambient_light_source, "ambient_light_energy": energy})
			# Positive controls: does an in-memory change to the environment reach the renderer at all?
			env.ambient_light_source = Environment.AMBIENT_SOURCE_DISABLED
			await _room_capture("ambient-source-%d-disabled.png" % Environment.AMBIENT_SOURCE_DISABLED, {"ambient_light_source": env.ambient_light_source, "ambient_light_energy": energy})
			env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
			env.ambient_light_energy = 0.0
			await _room_capture("ambient-source-%d-color-energy-0.0.png" % Environment.AMBIENT_SOURCE_COLOR, {"ambient_light_source": env.ambient_light_source, "ambient_light_energy": 0.0})
			# Colour/energy changes alone, with the source as loaded.
			env.ambient_light_source = loaded
			for e in [0.0, 2.0]:
				env.ambient_light_energy = e
				await _room_capture("ambient-source-%d-as-loaded-energy-%.1f.png" % [loaded, e], {"ambient_light_source": loaded, "ambient_light_energy": e})
			env.ambient_light_energy = energy
			env.ambient_light_source = loaded

func _room_capture(file: String, setting: Dictionary) -> Image:
	var img := await _capture(file)
	var size := Vector2(img.get_width(), img.get_height())
	if rects.is_empty():
		var fc := _to_px(FLOOR_POINT, size)
		var sc := _to_px(STANDIN_CENTRE, size)
		var edge := _to_px(STANDIN_CENTRE + camera.global_transform.basis.x * STANDIN_RADIUS, size)
		var half := maxi(2, int(absf(edge.x - sc.x) * 0.35))
		rects.floor = Rect2i(fc - Vector2i(FLOOR_HALF_PX, FLOOR_HALF_PX), Vector2i(FLOOR_HALF_PX * 2, FLOOR_HALF_PX * 2))
		rects.standin = Rect2i(sc - Vector2i(half, half * 2), Vector2i(half * 2, half * 4))
	var rec := {"file": file, "setting": setting, "floor_mean_rgb": _mean(img, rects.floor), "standin_mean_rgb": _mean(img, rects.standin)}
	records.append(rec)
	return img

func _sweep(mat: ShaderMaterial) -> void:
	var values := {
		"uv_scale": [0.25, mat.get_shader_parameter("uv_scale"), 4.0],
		"roughness_min": [0.0, mat.get_shader_parameter("roughness_min"), 1.0],
		"roughness_max": [0.0, mat.get_shader_parameter("roughness_max"), 1.0],
		"normal_strength": [0.0, mat.get_shader_parameter("normal_strength"), 2.0],
		"tint": [mat.get_shader_parameter("tint"), Color.WHITE, Color.BLACK],
	}
	for u in values:
		var original = mat.get_shader_parameter(u)
		for v in values[u]:
			mat.set_shader_parameter(u, v)
			var tag := ("%.2f" % v) if typeof(v) == TYPE_FLOAT else "%s" % [_color_tag(v)]
			await _room_capture("sweep-%s-%s.png" % [u, tag], {u: str(v), "is_material_value": v == original})
		mat.set_shader_parameter(u, original)

func _color_tag(c: Color) -> String:
	return "%.2f_%.2f_%.2f" % [c.r, c.g, c.b]

# --- output -------------------------------------------------------------------------------------

func _write() -> void:
	var meta := {
		"engine": Engine.get_version_info().string,
		"renderer": RenderingServer.get_current_rendering_method(),
		"driver": RenderingServer.get_current_rendering_driver_name(),
		"adapter": RenderingServer.get_video_adapter_name(),
		"revision": revision, "mode": mode, "label": label,
		"input": "scripted (no human input; parameters set in memory, never saved)",
		"utc": Time.get_datetime_string_from_system(true),
		"window": [root.size.x, root.size.y], "visible_rect": [root.get_visible_rect().size.x, root.get_visible_rect().size.y],
	}
	if mode != "hint":
		meta["pose"] = {"camera_position": [POSE_POSITION.x, POSE_POSITION.y, POSE_POSITION.z],
			"look_at": [POSE_TARGET.x, POSE_TARGET.y, POSE_TARGET.z], "fov": camera.fov,
			"floor_rect_px": _rect_json(rects.floor), "floor_rect_world_centre": [FLOOR_POINT.x, FLOOR_POINT.y, FLOOR_POINT.z],
			"standin_rect_px": _rect_json(rects.standin), "standin_rect_world_centre": [STANDIN_CENTRE.x, STANDIN_CENTRE.y, STANDIN_CENTRE.z]}
	var f := FileAccess.open(out_dir.path_join("captures.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"meta": meta, "captures": records}, "  "))
	f.close()
	var md := ["# A5 %s captures" % mode, "",
		"- Engine %s, renderer %s (%s, %s), revision `%s`" % [meta.engine, meta.renderer, meta.driver, meta.adapter, revision],
		"- Input: %s." % meta.input,
		"- Capture: viewport image after `frame_post_draw`, window %dx%d, visible rect %dx%d." % [root.size.x, root.size.y,
			root.get_visible_rect().size.x, root.get_visible_rect().size.y]]
	if mode == "hint":
		md.append_array(["", "| Quad | use_color | Left band | Middle band | Right band |", "|---|---|---|---|---|"])
		for q in records[0].quads:
			var b: Array = records[0].quads[q].bands
			md.append("| %s | %s | %s at %s | %s at %s | %s at %s |" % [q, str(records[0].quads[q].use_color),
				str(b[0].rgb), str(b[0].pixel), str(b[1].rgb), str(b[1].pixel), str(b[2].rgb), str(b[2].pixel)])
	else:
		md.append("- Pose: camera at %s looking at %s; floor rectangle %s px around %s; stand-in rectangle %s px around %s." % [
			str(meta.pose.camera_position), str(meta.pose.look_at), str(meta.pose.floor_rect_px), str(meta.pose.floor_rect_world_centre),
			str(meta.pose.standin_rect_px), str(meta.pose.standin_rect_world_centre)])
		md.append_array(["", "| File | Setting | Floor mean RGB | Stand-in mean RGB |", "|---|---|---|---|"])
		for r in records:
			md.append("| `%s` | %s | %s | %s |" % [r.file, str(r.setting), str(r.floor_mean_rgb), str(r.standin_mean_rgb)])
		if mode == "one-material":
			md.append("")
			md.append("Max per-channel difference vs baseline: stand-in rectangle %d, floor rectangle %d." % [
				records[-1].standin_max_channel_diff_vs_baseline, records[-1].floor_max_channel_diff_vs_baseline])
	md.append("")
	md.append("Measured values only; comparisons with the brief's predictions and any verdict belong to Bao.")
	f = FileAccess.open(out_dir.path_join("CAPTURES.md"), FileAccess.WRITE)
	f.store_string("\n".join(md) + "\n")
	f.close()
	print("wrote ", out_dir)
