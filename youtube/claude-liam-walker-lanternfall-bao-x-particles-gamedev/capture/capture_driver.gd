extends Node
## Film capture driver (Assignment 6 particle film) — used only in an isolated copy of the game at the film's
## source revision. Adapted from the Assignment 2 film's driver: it plays Lanternfall through the game's real input
## map (Input.action_press / InputEventAction), so the session reads the same actions a player's keys produce.
## Scripted input, labelled on screen. The one shortcut: the run starts with game.start_run(seed) instead of a
## random-seeded Enter press, so a take can be reproduced exactly. Disclosed in CAPTURE.md and FACTCHECK.md.
##
##   godot --path . res://capture_main.tscn --write-movie out.avi --fixed-fps 30 -- <take> <seed> [stop_after_s]
##   godot --headless --path . res://capture_main.tscn --fixed-fps 30 -- <take> <seed> [stop_after_s]   (dry run)
##
## Particle diagnostics are read-only: every weapon_hit and leveled_up signal, and, per movie frame, the live hit
## bursts, celebrations and whether the trail is emitting, with the courier's viewport position.

const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")

const TITLE_FRAMES := 120          # 2 s of title screen before the run starts (physics frames, 60/s)
const PAUSE_AT_S := 30.0           # main take: pause 30 s into the run ...
const PAUSE_FOR_FRAMES := 150      # ... for 2.5 s
const END_HOLD_FRAMES := 120
const CARD_HOLD_FRAMES := 120      # each card screen stays up 2 s before the scripted pick, so it can be read
const CARD_PRIORITY := ["sunflare", "beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius",
	"pass_damage", "pass_haste", "pass_magnet", "pass_speed", "pass_hp", "heal"]

var game
var take := "main"
var run_seed := 1
var f := 0
var started_at := -1
var ended_at := -1
var paused_at := -1
var card_seen_at := -1
var card_pressed_f := -1000
var log_lines: Array = []
var label: Label
var stop_after_s := -1.0
var stale: Array = []
var last_stale := -1
var track: Array = []

func _ready() -> void:
	process_physics_priority = -100   # act before the session reads the input this frame
	process_mode = Node.PROCESS_MODE_ALWAYS
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		take = args[0]
	if args.size() > 1:
		run_seed = int(args[1])
	if args.size() > 2:
		stop_after_s = float(args[2])
	game = Session.new()
	game.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(game)
	game.weapon_hit.connect(func(at: Vector2):
		var v: Vector2 = get_viewport().get_canvas_transform() * at
		_log("hit", {"view": [snappedf(v.x, 0.1), snappedf(v.y, 0.1)], "live": game.particles.hit_bursts.size()}))
	game.leveled_up.connect(func(l: int): _log("levelup", {"level": l}))
	var layer := CanvasLayer.new()
	layer.layer = 50
	add_child(layer)
	label = Label.new()
	label.text = "Real engine capture · scripted input"
	label.add_theme_font_size_override("font_size", 9)
	label.modulate = Color(1, 1, 1, 0.55)
	label.position = Vector2(8, 340)
	layer.add_child(label)

func _physics_process(_d: float) -> void:
	if _hold_for_window():
		return
	f += 1
	if f % 2 == 1 and f > 1 and OS.get_environment("LF_LOG_TRACK") == "1":
		# first physics step of an iteration: state as the previous movie frame was drawn
		var t: Transform2D = get_viewport().get_canvas_transform()
		var p: Vector2 = t * game.player.position
		var pp = game.particles
		track.append([snappedf(p.x, 0.1), snappedf(p.y, 0.1), snappedf(t.get_scale().x, 0.001),
			pp.hit_bursts.size(), pp.level_bursts.size(), 1 if pp.trail.emitting else 0, game.state.current])
	if f == 1:
		_log("first_frame", {"process_frame": Engine.get_process_frames()})
	if f == TITLE_FRAMES:
		game.start_run(run_seed)
		started_at = f
		_log("start_run", {"seed": run_seed})
	if started_at < 0:
		return
	if stop_after_s > 0.0 and game.tick_count >= int(stop_after_s * 60):
		_finish()
		return
	var st: int = game.state.current
	if st == GS.LEVELUP:
		_release_moves()
		if f - card_pressed_f < 4:
			return
		if card_seen_at < 0:
			card_seen_at = f
		elif f >= card_seen_at + CARD_HOLD_FRAMES:
			_choose_card()
			card_pressed_f = f
			card_seen_at = -1
		return
	card_seen_at = -1
	if st == GS.WON or st == GS.LOST:
		_release_moves()
		if ended_at < 0:
			ended_at = f
			_log("ended", {"state": GS.NAMES[st], "run_s": game.tick_count / 60.0, "level": game.prog.level, "kills": game.kills})
		if f >= ended_at + END_HOLD_FRAMES:
			_finish()
		return
	match take:
		"main":
			if paused_at < 0 and game.tick_count >= int(PAUSE_AT_S * 60):
				paused_at = f
				_release_moves()
				_action("pause")
				return
			if st == GS.PAUSED:
				if f >= paused_at + PAUSE_FOR_FRAMES:
					_action("pause")
				return
			_steer(_smart_axis())
		"props":
			_props_take()

## Movie Maker writes one frame per engine iteration, but macOS skips drawing while the window is occluded and the
## writer then repeats the last picture. While the window cannot draw, the whole tree is paused and the iteration
## is logged as stale; the edit drops those frames. The game's own code and state are untouched by this.
func _hold_for_window() -> bool:
	if DisplayServer.get_name() == "headless":
		return false
	if not DisplayServer.window_can_draw():
		var it := Engine.get_process_frames()
		if it != last_stale:
			last_stale = it
			stale.append(it)
		if not get_tree().paused:
			get_tree().paused = true
			if game.audio:
				game.audio.process_mode = Node.PROCESS_MODE_PAUSABLE
		return true
	if get_tree().paused:
		if game.audio:
			game.audio.process_mode = Node.PROCESS_MODE_ALWAYS
		get_tree().paused = false
	return false

## Walk to the nearest stall, push straight into its side (input held, no displacement), then push diagonally
## so the courier slides along it, then walk away.
func _props_take() -> void:
	var t: int = game.tick_count
	var stall: Vector2 = _nearest("stall")
	var box: Rect2 = game.ground._solid_box("stall", stall)
	var target := Vector2(box.position.x - 40, box.get_center().y)
	if t < 360:
		var to: Vector2 = target - game.player.position
		_steer(to.normalized() if to.length() > 6 else Vector2.ZERO)
		if t == 359:
			_log("phase", {"name": "push_right"})
	elif t < 540:
		_steer(Vector2.RIGHT)
		if t == 539:
			_log("phase", {"name": "slide_down_right"})
	elif t < 660:
		_steer(Vector2(1, 1).normalized())
		if t == 659:
			_log("phase", {"name": "stand"})
	elif t < 720:
		_steer(Vector2.ZERO)
	else:
		_finish()

func _smart_axis() -> Vector2:
	var p: Vector2 = game.player.position
	var push := Vector2.ZERO
	for e in game.enemies:
		var d: Vector2 = p - e.position
		if d.length() < 90.0:
			push += d.normalized() * (90.0 - d.length())
	if push.length() > 1.0:
		return push.normalized()
	if not game.gems.is_empty():
		var best: Vector2 = game.gems[0].position
		for g in game.gems:
			if g.position.distance_to(p) < best.distance_to(p):
				best = g.position
		return (best - p).normalized()
	var a := float(game.tick_count) / 90.0
	return Vector2(cos(a), sin(a))

func _choose_card() -> void:
	for want in CARD_PRIORITY:
		var i: int = game.offered.find(want)
		if i >= 0:
			_action("card_%d" % (i + 1))
			_log("card", {"picked": want, "offered": game.offered})
			return

func _steer(axis: Vector2) -> void:
	_set_action("move_right", maxf(axis.x, 0.0))
	_set_action("move_left", maxf(-axis.x, 0.0))
	_set_action("move_down", maxf(axis.y, 0.0))
	_set_action("move_up", maxf(-axis.y, 0.0))

func _set_action(a: String, strength: float) -> void:
	if strength > 0.0:
		Input.action_press(a, strength)
	else:
		Input.action_release(a)

func _release_moves() -> void:
	_steer(Vector2.ZERO)

func _action(a: String) -> void:
	var ev := InputEventAction.new()
	ev.action = a
	ev.pressed = true
	Input.parse_input_event(ev)
	var up := InputEventAction.new()
	up.action = a
	up.pressed = false
	Input.parse_input_event(up)
	_log("action", {"action": a})

func _nearest(kind: String) -> Vector2:
	var best := Vector2.INF
	for p in game.ground.props:
		if p["kind"] == kind and p["pos"].length() < best.length():
			best = p["pos"]
	return best

func _log(what: String, data: Dictionary) -> void:
	var line := {"frame": f, "pf": Engine.get_process_frames(), "tick": game.tick_count if game.prog else 0, "event": what}
	line.merge(data)
	log_lines.append(line)
	print(JSON.stringify(line))

func _finish() -> void:
	_log("movie_frames", {"process_frame": Engine.get_process_frames(), "stale": stale})
	if not track.is_empty():
		_log("track", {"note": "entry i = movie frame i: courier viewport [x, y], zoom, live hit bursts, live celebrations, trail emitting, state", "frames": track})
	var path := OS.get_environment("LF_CAPTURE_LOG")
	if path != "":
		var fh := FileAccess.open(path, FileAccess.WRITE)
		for l in log_lines:
			fh.store_line(JSON.stringify(l))
		fh.close()
	get_tree().quit()
