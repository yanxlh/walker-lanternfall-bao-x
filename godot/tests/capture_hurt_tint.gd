extends SceneTree
## Windowed controlled-value captures for the hurt tint (Assignment 5, Use It). Loads the real main scene with no
## enemy spawns (disclosed fixture), starts the run with a parsed Enter key and waits for the idle courier (facing
## right, unempowered, iframes 0, white modulate). Then the simulation is frozen with Session.test_mode (no ticks, so
## pose and blink cannot change between values) and F9 captures hurt_amount 0.0, 0.5, 1.0 and 2.0 with the
## assignment's pattern: stop the driver, set the parameter, await frame_post_draw, save the viewport image.
## `-- --auto` injects F9 itself and labels the captures scripted-input. Writes PNGs, captures.json and CAPTURES.md
## to --out (default captures/hurt-tint/<stamp>). The game never loads this script.
const GS = preload("res://game/game_state.gd")
const DriverScript = preload("res://effects/hurt_tint_presentation.gd")
const VALUES := [0.0, 0.5, 1.0, 2.0]
## Named texels of the idle frame (CHANGE-BRIEF.md, controlled inputs), frame-local, with their stored colours.
const TEXELS := {
	"lamp": {"texel": Vector2i(20, 16), "stored": [242, 184, 75]},
	"coat": {"texel": Vector2i(16, 24), "stored": [46, 58, 89]},
}

var game
var driver
var out_dir := ""
var revision := "unknown"
var scripted := false
var busy := false
var done := false

## Receives F9 from the real window (or from parsed input under --auto).
class KeyCatcher extends Node:
	signal capture_requested
	func _input(event: InputEvent) -> void:
		if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F9:
			capture_requested.emit()

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	scripted = "--auto" in args or "auto" in args
	var at := args.find("--rev")
	if at >= 0 and at + 1 < args.size():
		revision = args[at + 1]
	at = args.find("--out")
	var stamp := Time.get_datetime_string_from_system().replace(":", "").replace("-", "").replace("T", "-")
	out_dir = args[at + 1] if at >= 0 and at + 1 < args.size() else ProjectSettings.globalize_path("res://../captures/hurt-tint/" + stamp)
	DirAccess.make_dir_recursive_absolute(out_dir)
	AudioServer.set_bus_mute(0, true)
	call_deferred("_main")

func key(code: int, pressed: bool = true) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)

func frames(count: int) -> void:
	for n in count:
		await process_frame

func _main() -> void:
	game = load("res://game/main.tscn").instantiate()
	game.test_no_spawn = true
	root.add_child(game)
	for c in game.get_children():
		if c.get_script() == DriverScript:
			driver = c
	await frames(3)
	key(KEY_ENTER)
	await frames(1)
	key(KEY_ENTER, false)
	var p = game.player
	for n in 600:
		await physics_frame
		if game.state.current == GS.PLAYING and p.pose == "idle" and p.cast_ticks == 0 and p.iframes == 0 and p.facing == 1 and not p.empowered:
			break
	game.test_mode = true
	await frames(2)
	var catcher := KeyCatcher.new()
	root.add_child(catcher)
	catcher.capture_requested.connect(_on_capture)
	print("ready: courier idle, simulation frozen; press F9 in the window to capture" + (" (scripted F9 follows)" if scripted else ""))
	if scripted:
		key(KEY_F9)
		await frames(1)
		key(KEY_F9, false)

func _on_capture() -> void:
	if busy or done:
		return
	busy = true
	var mat: ShaderMaterial = game.player.material
	var records := []
	for v in VALUES:
		# The assignment's capture pattern; without set_process(false) the driver overwrites the value before the draw.
		driver.set_process(false)
		mat.set_shader_parameter("hurt_amount", v)
		await RenderingServer.frame_post_draw
		var img := root.get_texture().get_image()
		var file := "hurt-amount-%.1f.png" % v
		img.save_png(out_dir.path_join(file))
		var read_back = mat.get_shader_parameter("hurt_amount")
		driver.set_process(true)
		records.append(_record(v, read_back, file, img))
		print("captured ", file, " read back ", read_back)
	_write(records)
	done = true
	busy = false
	quit()

## Maps a frame texel's centre to a pixel of the captured image and samples it.
func _record(v: float, read_back, file: String, img: Image) -> Dictionary:
	var p = game.player
	var to_canvas: Transform2D = p.get_global_transform_with_canvas()
	var visible := root.get_visible_rect()
	var scale := Vector2(img.get_width(), img.get_height()) / visible.size
	var samples := {}
	for name in TEXELS:
		var t: Vector2i = TEXELS[name].texel
		var local := Vector2(t.x - p.SPRITE_ORIGIN.x + 0.5, t.y - p.SPRITE_ORIGIN.y + 0.5)
		var px := Vector2i(((to_canvas * local - visible.position) * scale).floor())
		var c := img.get_pixelv(px)
		samples[name] = {"texel": [t.x, t.y], "pixel": [px.x, px.y], "rgb": [c.r8, c.g8, c.b8], "stored": TEXELS[name].stored}
	return {
		"file": file, "hurt_amount_set": v, "hurt_amount_read_back": read_back, "samples": samples,
		"pose": p.pose, "modulate": [p.modulate.r, p.modulate.g, p.modulate.b, p.modulate.a],
		"image_size": [img.get_width(), img.get_height()], "visible_rect": [visible.size.x, visible.size.y],
		"scale": [scale.x, scale.y], "player_canvas_origin": [to_canvas.origin.x, to_canvas.origin.y],
	}

func _write(records: Array) -> void:
	var self_check := true
	for name in TEXELS:
		self_check = self_check and records[0].samples[name].rgb == TEXELS[name].stored
	var meta := {
		"engine": Engine.get_version_info().string,
		"renderer": RenderingServer.get_current_rendering_method(),
		"driver": RenderingServer.get_current_rendering_driver_name(),
		"adapter": RenderingServer.get_video_adapter_name(),
		"revision": revision,
		"input": "scripted-input" if scripted else "human F9",
		"utc": Time.get_datetime_string_from_system(true),
		"fixtures": "test_no_spawn = true; simulation frozen with test_mode = true while capturing",
		"self_check_0_equals_stored": self_check,
	}
	var f := FileAccess.open(out_dir.path_join("captures.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"meta": meta, "captures": records}, "  "))
	f.close()
	var md := ["# Hurt tint controlled-value captures", "",
		"- Engine %s, renderer %s (%s, %s), revision `%s`" % [meta.engine, meta.renderer, meta.driver, meta.adapter, revision],
		"- Input: %s. Fixtures: %s." % [meta.input, meta.fixtures],
		"- Capture: viewport image after `frame_post_draw`, driver stopped, %dx%d px." % records[0].image_size,
		"- Self-check (hurt_amount 0.0 reproduces the stored texel colours): %s" % ("PASS" if self_check else "FAIL"), "",
		"| File | Set | Read back | Lamp (20,16) pixel | Lamp RGB | Coat (16,24) pixel | Coat RGB |", "|---|---|---|---|---|---|---|"]
	for r in records:
		var l: Dictionary = r.samples.lamp
		var c: Dictionary = r.samples.coat
		md.append("| `%s` | %.1f | %s | %s | %s | %s | %s |" % [r.file, r.hurt_amount_set, str(r.hurt_amount_read_back), str(l.pixel), str(l.rgb), str(c.pixel), str(c.rgb)])
	md.append("")
	md.append("Measured values only; the comparison with the hand-computed table and any verdict belong to Bao.")
	f = FileAccess.open(out_dir.path_join("CAPTURES.md"), FileAccess.WRITE)
	f.store_string("\n".join(md) + "\n")
	f.close()
	print("wrote ", out_dir, " self-check ", "PASS" if self_check else "FAIL")
