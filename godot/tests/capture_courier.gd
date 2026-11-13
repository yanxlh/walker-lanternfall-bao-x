extends SceneTree
## Assignment 7 windowed replay for Movie Maker. Loads the real main scene, then drives a scripted timeline through
## Input.parse_input_event (movement, the dash, card keys) and writes one log line per rendered frame, so movie
## frame N lines up with log line N. Run it with a renderer, never --headless:
##   Godot --path godot --resolution 1280x720 --fixed-fps 60 --debug-collisions \
##     --write-movie <dir>/movie/frame.png --script res://tests/capture_courier.gd -- --scenario <name> --out <dir>
## Disclosed fixtures, applied after the scene loads: no enemy spawns; the run starts with seed 1 (start_run(1));
## the particle presentation is hidden for --scenario pin, whose crops are compared pixel for pixel before and
## after a change; the courier's collision circle is shown (F3 state) so --debug-collisions has something to show.
## Scenarios: pin (walk, stop, walk left, one wraith hit, level-up), walk (walk cycle), dash (unlock and dashes).
## The game never loads this script.
const GS = preload("res://game/game_state.gd")
const MAIN := "res://game/main.tscn"

var game
var out_dir := ""
var scenario := "pin"
var frame := -1
var lines: PackedStringArray = []
var timeline := {}
var end_frame := 0
var wraith

class Ticker extends Node:
	signal ticked
	func _process(_d: float) -> void:
		ticked.emit()

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var at := args.find("--scenario")
	if at >= 0 and at + 1 < args.size():
		scenario = args[at + 1]
	at = args.find("--out")
	out_dir = args[at + 1] if at >= 0 and at + 1 < args.size() else ProjectSettings.globalize_path("res://../captures/assignment-7/" + scenario)
	DirAccess.make_dir_recursive_absolute(out_dir)
	AudioServer.set_bus_mute(0, true)
	call_deferred("_main")

func _main() -> void:
	game = load(MAIN).instantiate()
	root.add_child(game)
	game.test_no_spawn = true
	game.start_run(1)
	game.player.show_collision = true
	if scenario == "pin":
		game.particles.visible = false
		for n in game.particles.find_children("*", "CanvasItem", true, false):
			n.visible = false
	_build_timeline()
	var t := Ticker.new()
	t.process_priority = 1000
	root.add_child(t)
	t.ticked.connect(_on_frame)

func _hold(action: String, from: int, to: int) -> void:
	_at(from, ["press", action])
	_at(to, ["release", action])

func _at(f: int, step: Array) -> void:
	if not timeline.has(f):
		timeline[f] = []
	timeline[f].append(step)

func _build_timeline() -> void:
	match scenario:
		"pin":
			_hold("move_right", 2, 42)
			_hold("move_left", 52, 72)
			_at(120, ["wraith"])
			_at(121, ["unwraith"])
			_at(185, ["xp", 3])
			_at(193, ["tap", "card_1"])
			_hold("move_right", 195, 206)
			end_frame = 215
		"walk":
			_hold("move_right", 2, 66)
			end_frame = 75
		"dash":
			_at(2, ["unlock"])
			_hold("move_right", 4, 200)
			_at(20, ["tap", "dash"])
			_at(60, ["tap", "dash"])
			_at(130, ["tap", "dash"])
			end_frame = 210

func _send(action: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	ev.strength = 1.0 if pressed else 0.0
	Input.parse_input_event(ev)

func _on_frame() -> void:
	frame += 1
	for step in timeline.get(frame, []):
		match step[0]:
			"press":
				_send(step[1], true)
			"release":
				_send(step[1], false)
			"tap":
				_send(step[1], true)
				_send(step[1], false)
			"wraith":
				wraith = game.spawn_enemy("wraith", game.player.position)
				wraith.hp = 9999
			"unwraith":
				game.enemies.erase(wraith)
				wraith.queue_free()
			"xp":
				game.prog.add_xp(step[1])
			"unlock":
				game.prog.apply("dash")
				if "dash_unlocked" in game.player:
					game.player.dash_unlocked = true
	_log()
	if frame >= end_frame:
		var f := FileAccess.open(out_dir + "/frames.log", FileAccess.WRITE)
		f.store_string("\n".join(lines) + "\n")
		f.close()
		print("wrote %d log lines to %s" % [lines.size(), out_dir])
		quit()

func _log() -> void:
	var p = game.player
	var body = p.get_node_or_null("CourierVisual/Body")
	var cell: int = (body.frame if body.is_visible_in_tree() else -1) if body else p.POSES.find(p.pose)
	var screen: Vector2 = p.get_global_transform_with_canvas().origin
	var phase: String = str(p.get("dash_phase")) if "dash_phase" in p else "-"
	lines.append("frame=%d tick=%d state=%s pose=%s cell=%d phase=%s x=%.2f y=%.2f sx=%.1f sy=%.1f iframes=%d hp=%d facing=%d" % [
		frame, game.tick_count, GS.NAMES[game.state.current], p.pose, cell, phase, p.position.x, p.position.y,
		screen.x, screen.y, p.iframes, p.hp, p.facing])
