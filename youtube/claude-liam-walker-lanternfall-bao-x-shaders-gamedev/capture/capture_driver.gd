extends Node
## Film capture driver (Assignment 5 shader film) — used only in an isolated copy of the game at the film's source
## revision. Adapted from the Assignment 6 film's driver: it plays Lanternfall through the game's real input map
## (Input.action_press / InputEventAction), so the session reads the same actions a player's keys produce. Scripted
## input, labelled on screen. The one shortcut: the run starts with game.start_run(seed) instead of a random-seeded
## Enter press, so a take can be reproduced exactly. Disclosed in CAPTURE.md and FACTCHECK.md.
##
##   godot --always-on-top --path . res://capture_main.tscn --write-movie out.avi --fixed-fps 30 -- hurt <seed>
##   godot --headless --path . res://capture_main.tscn --fixed-fps 30 -- hurt <seed>          (dry run)
##
## The "hurt" take walks the courier into the nearest monster until a hit is accepted, then lets go of every key
## for the whole protection window (until player.iframes is back to 0), so the yellow tint can be watched fading,
## then walks away from the nearest monster for 1 s. On the second accepted hit it presses
## pause halfway through the window and resumes 1.5 s later. Diagnostics are read-only: every accepted hit
## (player.damaged), and, per movie frame, the courier's viewport position, the hurt_amount stored on his material,
## player.iframes, whether the red blink is on, the run state, hp and whether a monster is touching him.

const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")

const TITLE_FRAMES := 120          # 2 s of title screen before the run starts (physics frames, 60/s)
const HITS_WANTED := 3
const FLEE_TICKS := 60           # after each window: walk away from the nearest monster for 1 s
const PAUSE_ON_HIT := 2            # the second accepted hit ...
const PAUSE_AT_IFRAMES := 24       # ... gets a pause when half of its window is left ...
const PAUSE_FOR_FRAMES := 90       # ... held for 1.5 s
const END_HOLD_FRAMES := 60
const MAX_RUN_TICKS := 90 * 60
const CARD_HOLD_FRAMES := 120
const CARD_PRIORITY := ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius",
	"pass_damage", "pass_haste", "pass_magnet", "pass_speed", "pass_hp", "heal", "sunflare"]

var game
var take := "hurt"
var run_seed := 1
var f := 0
var started_at := -1
var finish_at := -1
var phase := "seek"
var phase_tick := 0
var hits := 0
var paused_at := -1
var resume_sent := false
var card_seen_at := -1
var card_pressed_f := -1000
var log_lines: Array = []
var label: Label
var stale: Array = []
var last_stale := -1
var track: Array = []

func _ready() -> void:
	process_physics_priority = -100   # act before the session reads the input this frame
	process_priority = 100000         # record after the tint driver has written this frame's value
	process_mode = Node.PROCESS_MODE_ALWAYS
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		take = args[0]
	if args.size() > 1:
		run_seed = int(args[1])
	game = Session.new()
	game.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(game)
	game.player.damaged.connect(func(hp: int):
		hits += 1
		_log("hit", {"n": hits, "hp": hp, "iframes": game.player.iframes, "amount_before_refresh": _amount()}))
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

func _amount() -> float:
	var m = game.player.material
	return float(m.get_shader_parameter("hurt_amount")) if m else -1.0

func _contact() -> int:
	var p: Vector2 = game.player.position
	for e in game.enemies:
		if is_instance_valid(e) and not e.dead and e.position.distance_to(p) < e.radius + Tuning.PLAYER_RADIUS:
			return 1
	return 0

## One row per engine iteration, after every other _process() (the tint driver runs at priority 200), so a row
## holds exactly what this iteration draws and Movie Maker writes: row i = movie frame i.
func _process(_d: float) -> void:
	if DisplayServer.get_name() != "headless" and not DisplayServer.window_can_draw():
		return
	if OS.get_environment("LF_LOG_TRACK") != "1":
		return
	var t: Transform2D = get_viewport().get_canvas_transform()
	var pl = game.player
	var p: Vector2 = t * pl.position
	track.append([snappedf(p.x, 0.1), snappedf(p.y, 0.1), snappedf(t.get_scale().x, 0.001),
		snappedf(_amount(), 0.0001), pl.iframes, 1 if pl.modulate.g < 0.5 else 0, game.state.current,
		pl.hp, _contact(), game.tick_count])

func _physics_process(_d: float) -> void:
	if _hold_for_window():
		return
	f += 1
	if f == 1:
		_log("first_frame", {"process_frame": Engine.get_process_frames()})
	if f == TITLE_FRAMES:
		game.start_run(run_seed)
		started_at = f
		_log("start_run", {"seed": run_seed})
	if started_at < 0:
		return
	if finish_at > 0:
		_release_moves()
		if f >= finish_at:
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
		_log("ended", {"state": GS.NAMES[st], "tick": game.tick_count, "hits": hits})
		finish_at = f + END_HOLD_FRAMES
		return
	if st == GS.PAUSED:
		_release_moves()
		if f >= paused_at + PAUSE_FOR_FRAMES and not resume_sent:
			resume_sent = true
			_action("pause")
		return
	if game.tick_count >= MAX_RUN_TICKS:
		_log("timeout", {"hits": hits})
		finish_at = f + END_HOLD_FRAMES
		return
	_hurt_take()

func _hurt_take() -> void:
	var t: int = game.tick_count
	match phase:
		"seek":
			if game.player.iframes > 0:          # a hit was accepted this tick or the last
				_set_phase("hold", t)
				_release_moves()
				return
			var target = _nearest_enemy()
			_steer((target - game.player.position).normalized() if target != null else Vector2(cos(t / 90.0), sin(t / 90.0)))
		"hold":
			_release_moves()
			if hits == PAUSE_ON_HIT and paused_at < 0 and game.player.iframes == PAUSE_AT_IFRAMES:
				paused_at = f
				_action("pause")
				return
			if game.player.iframes == 0:
				_set_phase("flee", t)
		"flee":
			var near = _nearest_enemy()
			if near != null:
				var away: Vector2 = game.player.position - near
				_steer(away.normalized() if away.length() > 0.01 else Vector2.LEFT)
			if t >= phase_tick + FLEE_TICKS:
				if hits >= HITS_WANTED:
					_log("done", {"hits": hits, "tick": t})
					finish_at = f + END_HOLD_FRAMES
				else:
					_set_phase("seek", t)

func _set_phase(p: String, t: int) -> void:
	phase = p
	phase_tick = t
	_log("phase", {"name": p})

func _nearest_enemy():
	var best = null
	var best_d := INF
	for e in game.enemies:
		if is_instance_valid(e) and not e.dead:
			var d: float = e.position.distance_squared_to(game.player.position)
			if d < best_d:
				best_d = d
				best = e.position
	return best

## Movie Maker writes one frame per engine iteration, but macOS skips drawing while the window is occluded and the
## writer then repeats the last picture. While the window cannot draw, the whole tree is paused and the iteration
## is logged as stale. The game's own code and state are untouched by this.
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

func _log(what: String, data: Dictionary) -> void:
	var line := {"frame": f, "pf": Engine.get_process_frames(), "tick": game.tick_count if game.prog else 0, "event": what}
	line.merge(data)
	log_lines.append(line)
	print(JSON.stringify(line))

func _finish() -> void:
	_log("movie_frames", {"process_frame": Engine.get_process_frames(), "stale": stale})
	if not track.is_empty():
		_log("track", {"note": "entry i = movie frame i (recorded in _process after the tint driver): courier viewport [x, y], zoom, hurt_amount on his material, iframes, red blink on, state, hp, monster contact, tick", "frames": track})
	var path := OS.get_environment("LF_CAPTURE_LOG")
	if path != "":
		var fh := FileAccess.open(path, FileAccess.WRITE)
		for l in log_lines:
			fh.store_line(JSON.stringify(l))
		fh.close()
	get_tree().quit()
