extends SceneTree
## Windowed controlled-value captures for the hurt tint (Assignment 5, Use It). Loads the real main scene with no
## enemy spawns (disclosed fixture), starts the run with a parsed Enter key and waits for the idle courier (facing
## right, unempowered, iframes 0, white modulate). Then the simulation is frozen with Session.test_mode (no ticks, so
## pose and blink cannot change between values) and F9 captures hurt_amount 0.0, 0.5, 1.0 and 2.0 with the
## assignment's pattern: stop the driver, set the parameter, await frame_post_draw, save the viewport image.
## `-- --auto` injects F9 itself and labels the captures scripted-input. `--red` captures the red blink phase instead:
## one seeded wraith (disclosed fixture) hits the courier through real contact and take_hit(); the real simulation
## runs until the courier is idle in a red phase, the wraith is freed and the simulation frozen, then 0.0, 0.5 and 1.0
## are captured. Writes PNGs, captures.json and CAPTURES.md to --out (default captures/hurt-tint/<stamp>[-red]).
## `--hold <seconds>` (white phase): after the captures, keeps the driver stopped at hurt_amount 0.5, moves the window to
## (80, 80), captures that frame in-engine again and writes hold.json with the window rect and screen scale, then holds
## the frame for the given seconds so an OS screenshot of the same frame can be taken from outside.
## The game never loads this script.
const GS = preload("res://game/game_state.gd")
const DriverScript = preload("res://effects/hurt_tint_presentation.gd")
const VALUES := [0.0, 0.5, 1.0, 2.0]
const RED_VALUES := [0.0, 0.5, 1.0]
const RED := Color(1, 0.45, 0.45)
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
var red := false
var fixture_note := "test_no_spawn = true; simulation frozen with test_mode = true while capturing"
var busy := false
var done := false
var hold := 0.0

## Receives F9 from the real window (or from parsed input under --auto).
class KeyCatcher extends Node:
	signal capture_requested
	func _input(event: InputEvent) -> void:
		if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F9:
			capture_requested.emit()

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	scripted = "--auto" in args or "auto" in args
	red = "--red" in args
	var at := args.find("--rev")
	if at >= 0 and at + 1 < args.size():
		revision = args[at + 1]
	at = args.find("--hold")
	if at >= 0 and at + 1 < args.size():
		hold = float(args[at + 1])
	at = args.find("--out")
	var stamp := Time.get_datetime_string_from_system().replace(":", "").replace("-", "").replace("T", "-") + ("-red" if red else "")
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
	if red:
		if not await _reach_red_phase():
			print("no idle red-phase frame reached; nothing captured")
			quit(1)
			return
	else:
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

## Red phase: one seeded wraith (fixture: position and hp only) reaches the courier by real movement and the hit lands
## through take_hit(). The real simulation runs until the courier is idle in a red blink phase; at that physics_frame,
## before the next tick, the simulation is frozen and the wraith freed, so the drawn courier keeps that pose and modulate.
func _reach_red_phase() -> bool:
	var p = game.player
	var e = game.spawn_enemy("wraith", p.position + Vector2(40, 0))
	e.hp = 1000.0
	fixture_note = "test_no_spawn = true; one wraith spawned 40 px right of the courier with hp 1000 so the beam cannot kill it; after its real hit it is freed and the simulation frozen with test_mode = true while capturing"
	for n in 1800:
		await physics_frame
		if game.state.current != GS.PLAYING:
			return false
		if p.iframes > 0 and p.iframes <= 36 and (p.iframes / 4) % 2 == 0 and p.pose == "idle" and p.walk_ticks == 0 \
				and p.override_pose == "" and p.cast_ticks == 0 and p.modulate.is_equal_approx(RED):
			game.test_mode = true
			game.enemies.erase(e)
			e.queue_free()
			return true
	return false

func _on_capture() -> void:
	if busy or done:
		return
	busy = true
	var mat: ShaderMaterial = game.player.material
	var records := []
	for v in (RED_VALUES if red else VALUES):
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
	if hold > 0.0 and not red:
		await _hold_frame(mat)
	done = true
	busy = false
	quit()

## Holds one frame at hurt_amount 0.5 at a known window position for an OS screenshot of the same frame.
func _hold_frame(mat: ShaderMaterial) -> void:
	driver.set_process(false)
	mat.set_shader_parameter("hurt_amount", 0.5)
	DisplayServer.window_set_position(Vector2i(80, 80))
	DisplayServer.window_move_to_foreground()
	await frames(10)
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	var file := "hold-hurt-amount-0.5.png"
	img.save_png(out_dir.path_join(file))
	var rec := _record(0.5, mat.get_shader_parameter("hurt_amount"), file, img)
	var screen := DisplayServer.window_get_current_screen()
	var pos := DisplayServer.window_get_position()
	var size := DisplayServer.window_get_size()
	var info := {
		"window_position_px": [pos.x, pos.y], "window_size_px": [size.x, size.y],
		"window_position_with_decorations_px": [DisplayServer.window_get_position_with_decorations().x, DisplayServer.window_get_position_with_decorations().y],
		"screen": screen, "screen_scale": DisplayServer.screen_get_scale(screen), "screen_max_scale": DisplayServer.screen_get_max_scale(),
		"screen_position_px": [DisplayServer.screen_get_position(screen).x, DisplayServer.screen_get_position(screen).y],
		"screen_size_px": [DisplayServer.screen_get_size(screen).x, DisplayServer.screen_get_size(screen).y],
		"image_size": [img.get_width(), img.get_height()], "hold_seconds": hold, "record": rec,
	}
	var f := FileAccess.open(out_dir.path_join("hold.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify(info, "  "))
	f.close()
	print("HOLD READY ", JSON.stringify(info))
	await create_timer(hold).timeout
	driver.set_process(true)

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
		"pose": p.pose, "modulate": [p.modulate.r, p.modulate.g, p.modulate.b, p.modulate.a], "iframes": p.iframes,
		"camera_rotation": game.camera.rotation, "canvas_rotation": to_canvas.get_rotation(),
		"image_size": [img.get_width(), img.get_height()], "visible_rect": [visible.size.x, visible.size.y],
		"scale": [scale.x, scale.y], "player_canvas_origin": [to_canvas.origin.x, to_canvas.origin.y],
		"player_position": [p.position.x, p.position.y],
	}

## The colour hurt_amount 0.0 should reproduce: the stored texel, times the red modulate in red phase, rounded.
func _expected_zero(stored: Array) -> Array:
	if not red:
		return stored
	return [roundi(stored[0] * RED.r), roundi(stored[1] * RED.g), roundi(stored[2] * RED.b)]

func _write(records: Array) -> void:
	var self_check := true
	for name in TEXELS:
		self_check = self_check and records[0].samples[name].rgb == _expected_zero(TEXELS[name].stored)
	var meta := {
		"engine": Engine.get_version_info().string,
		"renderer": RenderingServer.get_current_rendering_method(),
		"driver": RenderingServer.get_current_rendering_driver_name(),
		"adapter": RenderingServer.get_video_adapter_name(),
		"revision": revision,
		"input": "scripted-input" if scripted else "human F9",
		"utc": Time.get_datetime_string_from_system(true),
		"fixtures": fixture_note,
		"phase": "red" if red else "white",
	}
	if red:
		meta["zero_sampled_vs_stored_times_red"] = {}
		for name in TEXELS:
			meta["zero_sampled_vs_stored_times_red"][name] = {"sampled": records[0].samples[name].rgb, "product": _expected_zero(TEXELS[name].stored)}
		meta["zero_matches_product"] = self_check
	else:
		meta["self_check_0_equals_stored"] = self_check
	var f := FileAccess.open(out_dir.path_join("captures.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"meta": meta, "captures": records}, "  "))
	f.close()
	var md := ["# Hurt tint controlled-value captures", "",
		"- Engine %s, renderer %s (%s, %s), revision `%s`" % [meta.engine, meta.renderer, meta.driver, meta.adapter, revision],
		"- Input: %s. Fixtures: %s." % [meta.input, meta.fixtures],
		"- Capture: viewport image after `frame_post_draw`, driver stopped, %dx%d px." % records[0].image_size]
	if red:
		md.append("- Red phase, hurt_amount 0.0 sampled vs stored x (1, 0.45, 0.45) rounded: lamp %s vs %s, coat %s vs %s" % [
			str(records[0].samples.lamp.rgb), str(_expected_zero(TEXELS.lamp.stored)),
			str(records[0].samples.coat.rgb), str(_expected_zero(TEXELS.coat.stored))])
	else:
		md.append("- Self-check (hurt_amount 0.0 reproduces the stored texel colours): %s" % ("PASS" if self_check else "FAIL"))
	md.append_array(["", "| File | Set | Read back | iframes | Modulate | Camera rot | Lamp (20,16) pixel | Lamp RGB | Coat (16,24) pixel | Coat RGB |",
		"|---|---|---|---|---|---|---|---|---|---|"])
	for r in records:
		var l: Dictionary = r.samples.lamp
		var c: Dictionary = r.samples.coat
		md.append("| `%s` | %.1f | %s | %d | %s | %s | %s | %s | %s | %s |" % [r.file, r.hurt_amount_set, str(r.hurt_amount_read_back), r.iframes,
			str(r.modulate.slice(0, 3)), str(r.camera_rotation), str(l.pixel), str(l.rgb), str(c.pixel), str(c.rgb)])
	md.append("")
	md.append("Measured values only; the comparison with the hand-computed table and any verdict belong to Bao.")
	f = FileAccess.open(out_dir.path_join("CAPTURES.md"), FileAccess.WRITE)
	f.store_string("\n".join(md) + "\n")
	f.close()
	print("wrote ", out_dir, (" red-phase 0.0 matches product: " if red else " self-check ") + ("yes" if red and self_check else ("no" if red else ("PASS" if self_check else "FAIL"))))
