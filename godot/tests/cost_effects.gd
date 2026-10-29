extends SceneTree
## Cost measurement for the particle effects; not a pass/fail test. Each condition runs with the presentation
## attached ("on") and freed before the run starts ("off") on the same fixture, interleaved over several trials.
## `frame_ms` is wall time between consecutive frames. Headless with --fixed-fps runs unthrottled (no vsync, dummy
## renderer), so it is the CPU cost of one whole frame. Performance.TIME_PROCESS read 0 under this script main loop.
## Windowed runs are vsync-limited, so their frame_ms is not a cost; they add the viewport's measured render time
## (CPU and GPU) from RenderingServer, the source the editor's Visual Profiler reads.
## Usage: Godot [--headless] --path godot --fixed-fps 60 --script res://tests/cost_effects.gd -- --out <file> [--rev <sha>] [--trials N]
const Session = preload("res://game/session.gd")
const Tuning = preload("res://features/tuning.gd")
var TRIALS := 5
const FRAMES := 300
const WARMUP := 30
const CELEBRATION_FRAMES := 38

var game
var bare: Node2D
var headless := false
var out_path := ""
var rev := "unknown"

func _initialize() -> void:
	headless = DisplayServer.get_name() == "headless"
	var args := OS.get_cmdline_user_args()
	var at := args.find("--out")
	out_path = args[at + 1] if at >= 0 and at + 1 < args.size() else ProjectSettings.globalize_path("res://../evidence/assignment-6/cost/cost_effects.json")
	at = args.find("--trials")
	if at >= 0 and at + 1 < args.size():
		TRIALS = int(args[at + 1])
	at = args.find("--rev")
	if at >= 0 and at + 1 < args.size():
		rev = args[at + 1]
	AudioServer.set_bus_mute(0, true)
	call_deferred("_main")

func key(code: int, pressed: bool = true) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)

func frame() -> void:
	await physics_frame
	await process_frame

func start(cond: String, effects: bool) -> void:
	key(KEY_D, false)
	if is_instance_valid(game):
		game.free()
	if is_instance_valid(bare):
		bare.free()
	await frame()
	if cond == "empty":
		bare = Node2D.new()
		root.add_child(bare)
		return
	game = Session.new()
	game.test_no_spawn = true
	root.add_child(game)
	if not effects:
		game.particles.free()
	game.run_started.connect(_fixture.bind(cond), CONNECT_ONE_SHOT)
	await frame()
	key(KEY_ENTER)
	await frame()
	key(KEY_ENTER, false)
	await frame()
	if cond == "move":
		key(KEY_D)
	elif cond == "celebration":
		# One real pickup worth six levels: the celebration cap (4) is reached on the card screen.
		game.drop_gem(game.player.position, 51)

func _fixture(cond: String) -> void:
	if cond == "acap":
		# The stress fixture from test_particles_state.gd: one beam volley hits 40 enemies, 32 bursts accepted.
		game.prog.beam_pierce = 40
		for i in 40:
			var e = game.spawn_enemy("wraith", Vector2(70 + i * 0.2, 0))
			e.hp = 999999.0
			e.speed = 0.0
	elif cond == "move":
		game.player.position = Vector2(-400, 0)

func sample(effects: bool, frame_ms: float) -> Dictionary:
	var s := {"frame_ms": frame_ms}
	if not headless:
		var rid := root.get_viewport_rid()
		s["render_cpu_ms"] = RenderingServer.viewport_get_measured_render_time_cpu(rid)
		s["render_gpu_ms"] = RenderingServer.viewport_get_measured_render_time_gpu(rid)
	s["hit_bursts"] = game.particles.hit_bursts.size() if effects and is_instance_valid(game) else 0
	s["level_bursts"] = game.particles.level_bursts.size() if effects and is_instance_valid(game) else 0
	s["trail"] = game.particles.trail.emitting if effects and is_instance_valid(game) else false
	return s

func measure(cond: String, effects: bool, count: int) -> Array:
	await start(cond, effects)
	for i in (2 if cond == "celebration" else WARMUP):
		await frame()
	var rows := []
	var last := Time.get_ticks_usec()
	for i in count:
		await frame()
		var now := Time.get_ticks_usec()
		rows.append(sample(effects, (now - last) / 1000.0))
		last = now
	return rows

func stats(values: Array) -> Dictionary:
	if values.is_empty():
		return {"n": 0}
	var sorted := values.duplicate()
	sorted.sort()
	var total := 0.0
	for v in values:
		total += v
	var mean := total / values.size()
	var sq := 0.0
	for v in values:
		sq += (v - mean) * (v - mean)
	return {"n": values.size(), "mean": mean, "sd": sqrt(sq / maxi(1, values.size() - 1)),
		"median": sorted[sorted.size() / 2], "p95": sorted[mini(sorted.size() - 1, int(sorted.size() * 0.95))]}

func column(rows: Array, field: String, filter: Callable = Callable()) -> Array:
	var out := []
	for r in rows:
		if r.has(field) and (not filter.is_valid() or filter.call(r)):
			out.append(r[field])
	return out

func _main() -> void:
	if not headless:
		RenderingServer.viewport_set_measure_render_time(root.get_viewport_rid(), true)
	var conditions := [
		["empty", false, FRAMES, TRIALS], ["idle", false, FRAMES, TRIALS], ["idle", true, FRAMES, TRIALS],
		["acap", false, FRAMES, TRIALS], ["acap", true, FRAMES, TRIALS],
		["move", false, FRAMES, TRIALS], ["move", true, FRAMES, TRIALS],
		["celebration", false, CELEBRATION_FRAMES, TRIALS * 2], ["celebration", true, CELEBRATION_FRAMES, TRIALS * 2],
	]
	var report := {}
	for c in conditions:
		report["%s-%s" % [c[0], "on" if c[1] else "off"]] = {"trials": []}
	for trial in TRIALS * 2:
		for c in conditions:
			if trial >= c[3]:
				continue
			var rows: Array = await measure(c[0], c[1], c[2])
			var t := {"frame_ms": stats(column(rows, "frame_ms"))}
			if not headless:
				t["render_cpu_ms"] = stats(column(rows, "render_cpu_ms"))
				t["render_gpu_ms"] = stats(column(rows, "render_gpu_ms"))
			if c[0] == "acap" and c[1]:
				t["frame_ms_at_cap"] = stats(column(rows, "frame_ms", func(r): return r["hit_bursts"] == 32))
				if not headless:
					t["render_gpu_ms_at_cap"] = stats(column(rows, "render_gpu_ms", func(r): return r["hit_bursts"] == 32))
					t["render_cpu_ms_at_cap"] = stats(column(rows, "render_cpu_ms", func(r): return r["hit_bursts"] == 32))
			t["max_hit_bursts"] = column(rows, "hit_bursts").max()
			t["max_level_bursts"] = column(rows, "level_bursts").max()
			t["trail_frames"] = column(rows, "trail", func(r): return r["trail"]).size()
			report["%s-%s" % [c[0], "on" if c[1] else "off"]]["trials"].append(t)
			print("%s-%s trial %d frame mean %.4f ms" % [c[0], "on" if c[1] else "off", trial, t["frame_ms"]["mean"]])
	key(KEY_D, false)
	var meta := {
		"engine": Engine.get_version_info().string,
		"renderer": RenderingServer.get_current_rendering_method(),
		"rendering_driver": RenderingServer.get_current_rendering_driver_name(),
		"project_renderer": ProjectSettings.get_setting("rendering/renderer/rendering_method"),
		"display": DisplayServer.get_name(),
		"adapter": RenderingServer.get_video_adapter_name(),
		"adapter_vendor": RenderingServer.get_video_adapter_vendor(),
		"cpu": OS.get_processor_name(),
		"os": OS.get_name() + " " + OS.get_version(),
		"source_revision": rev,
		"fixed_fps": Engine.physics_ticks_per_second,
		"utc": Time.get_datetime_string_from_system(true),
		"trials": TRIALS, "frames": FRAMES, "warmup": WARMUP,
	}
	DirAccess.make_dir_recursive_absolute(out_path.get_base_dir())
	var f := FileAccess.open(out_path, FileAccess.WRITE)
	f.store_string(JSON.stringify({"meta": meta, "conditions": report}, "  "))
	f.close()
	print("saved ", out_path)
	if is_instance_valid(game):
		game.free()
	quit()
