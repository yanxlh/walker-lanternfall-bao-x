extends Node
## Film take driver for the Assignment 7 film. Used only in an isolated copy of the game at the film's source revision
## (`git archive 5f09b7f godot`), never in the repository. It plays Lanternfall through the real input map: every
## key is an event parsed with Input.parse_input_event and flushed before the session's physics step, so the session
## reads it on that tick. Disclosed fixtures, also printed on screen: no enemy spawns; seed 1; XP added for one
## level-up and the card offer set so the Courier's Dash card is first; for each interrupted dash a wraith (hp 9999)
## is placed on the courier for one step. The script is the same in the window and in the headless dry run.
##
##   godot --path . res://film_main.tscn --write-movie <out>/take-dash.avi --fixed-fps 30 -- <out>/take-dash-log.jsonl
##   godot --headless --path . res://film_main.tscn --fixed-fps 30 -- <out>/take-dash-dryrun.jsonl
##
## Timeline, in physics steps (60 per second): right held from 0; level-up at 40, card screen until 220, card "1";
## dash at 320 (no interrupt); left from 420; dash at 470 with a hit on startup frame 2; dash at 560 with a hit on
## active frame 8; right from 650; dash at 670 with a hit on recovery frame 16; end at 840.
## One log row per rendered frame: movie frame N is row N.

const GS = preload("res://game/game_state.gd")
const MAIN := "res://game/main.tscn"
const END_STEP := 840
const LABEL := "Real engine capture · scripted input · fixtures: no spawns, the dash card set first in the offer, a wraith placed for each hit"

var game
var step := 0
var frame := -1
var wraith
var log_path := ""
var log_file: FileAccess
var events: Array = []

class Hook extends Node:
	var on_step: Callable
	func _physics_process(_d: float) -> void:
		on_step.call()

func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	log_path = args[0] if args.size() > 0 else ProjectSettings.globalize_path("res://take-dash-log.jsonl")
	log_file = FileAccess.open(log_path, FileAccess.WRITE)
	AudioServer.set_bus_mute(0, true)
	game = load(MAIN).instantiate()
	game.test_no_spawn = true
	add_child(game)
	game.start_run(1)
	var layer := CanvasLayer.new()
	layer.layer = 100
	var label := Label.new()
	label.text = LABEL
	label.position = Vector2(8, 344)
	label.add_theme_font_size_override("font_size", 8)
	label.add_theme_color_override("font_color", Color(1, 0.95, 0.8, 0.9))
	layer.add_child(label)
	add_child(layer)
	var hook := Hook.new()
	hook.process_physics_priority = -100
	hook.on_step = _drive
	add_child(hook)
	game.player.dash_phase_changed.connect(func(from: String, to: String): events.append("phase %s>%s" % [from, to]))
	game.player.damaged.connect(func(hp: int): events.append("hit hp=%d" % hp))
	process_priority = 100000

func _action(name: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = name
	ev.pressed = pressed
	ev.strength = 1.0 if pressed else 0.0
	Input.parse_input_event(ev)

func _key(code: Key) -> void:
	for pressed in [true, false]:
		var ev := InputEventKey.new()
		ev.physical_keycode = code
		ev.keycode = code
		ev.pressed = pressed
		Input.parse_input_event(ev)

func _place_wraith() -> void:
	wraith = game.spawn_enemy("wraith", game.player.position)
	wraith.hp = 9999
	events.append("wraith placed")

func _remove_wraith() -> void:
	if is_instance_valid(wraith):
		game.enemies.erase(wraith)
		wraith.free()
	events.append("wraith removed")

func _drive() -> void:
	match step:
		0:
			_action("move_right", true)
		40:
			game.prog.add_xp(game.prog.xp_needed())
			events.append("xp added for one level-up")
		41:
			game.offered = Array(["dash", "heal", "heal"], TYPE_STRING, "", null)
			events.append("offer set: dash, heal, heal")
		220:
			_key(KEY_1)
			events.append("card key 1")
		320, 470, 560, 670:
			_key(KEY_SHIFT)
			events.append("dash key")
		420:
			_action("move_right", false)
			_action("move_left", true)
		472, 568, 686:
			_place_wraith()
		473, 569, 687:
			_remove_wraith()
		650:
			_action("move_left", false)
			_action("move_right", true)
		END_STEP:
			_action("move_right", false)
	Input.flush_buffered_events()
	step += 1
	if step > END_STEP + 30 and log_file:
		log_file.close()
		log_file = null
		get_tree().quit()

func _process(_d: float) -> void:
	if log_file == null:
		return
	frame += 1
	var p = game.player
	var body = p.get_node("CourierVisual/Body")
	var screen: Vector2 = p.get_global_transform_with_canvas().origin
	log_file.store_line(JSON.stringify({"frame": frame, "step": step, "tick": game.tick_count, "state": GS.NAMES[game.state.current],
		"pose": p.pose, "cell": body.frame if body.is_visible_in_tree() else -1, "phase": p.dash_phase, "dash_ticks": p.dash_ticks,
		"cooldown": p.dash_cooldown, "unlocked": p.dash_unlocked, "x": snappedf(p.position.x, 0.01), "y": snappedf(p.position.y, 0.01),
		"sx": snappedf(screen.x, 0.1), "sy": snappedf(screen.y, 0.1), "iframes": p.iframes, "hp": p.hp, "events": events}))
	log_file.flush()
	events = []
