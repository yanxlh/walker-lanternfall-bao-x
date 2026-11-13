extends Node2D
## Assignment 7 fixture for the frame strips (CHANGE-BRIEF "The frame strip"). The real game session on the real market
## ground, followed by the real camera. Disclosed fixtures: no enemy spawns; seed 1; the dash unlocked; the courier
## starts at START; right is held from the first tick; for `--clip dash` the dash key is parsed on TRIGGER_TICK.
## Input goes through Input.parse_input_event and is flushed before the session's step, so it lands on that tick.
## One log line per rendered frame (frame N of a Movie Maker capture is line N) goes to <out>/frames.log.
## Bao runs it (scripts/capture-strip.command); windowed only, a headless run draws nothing. The game never loads it.
##   Godot --path godot res://previews/courier_preview.tscn --write-movie <out>/frame.png --fixed-fps 30 \
##     --quit-after 90 -- --clip dash|walk --out <out>
const GS = preload("res://game/game_state.gd")
const MAIN := "res://game/main.tscn"
const TRIGGER_TICK := 10
## Plaza edge, walking right into the first market stalls: a representative stretch of the level.
const START := Vector2(60, 0)

var game
var clip := "dash"
var out_dir := ""
var log_file: FileAccess
var frame := -1

class Driver extends Node:
	var on_step: Callable
	func _physics_process(_d: float) -> void:
		on_step.call()

func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	var at := args.find("--clip")
	if at >= 0 and at + 1 < args.size():
		clip = args[at + 1]
	at = args.find("--out")
	out_dir = args[at + 1] if at >= 0 and at + 1 < args.size() else ProjectSettings.globalize_path("res://../captures/%s/preview" % clip)
	DirAccess.make_dir_recursive_absolute(out_dir)
	log_file = FileAccess.open(out_dir + "/frames.log", FileAccess.WRITE)
	AudioServer.set_bus_mute(0, true)
	game = load(MAIN).instantiate()
	game.test_no_spawn = true
	add_child(game)
	game.start_run(1)
	game.prog.apply("dash")
	game.player.dash_unlocked = true
	game.player.position = START
	var driver := Driver.new()
	driver.process_physics_priority = -100
	driver.on_step = _drive
	add_child(driver)
	process_priority = 1000

func _drive() -> void:
	if game.tick_count == 0:
		_send("move_right", true)
	if clip == "dash" and game.tick_count == TRIGGER_TICK:
		var down := InputEventKey.new()
		down.physical_keycode = KEY_SHIFT
		down.keycode = KEY_SHIFT
		down.pressed = true
		Input.parse_input_event(down)
		var up: InputEventKey = down.duplicate()
		up.pressed = false
		Input.parse_input_event(up)
	Input.flush_buffered_events()

func _send(action: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	ev.strength = 1.0 if pressed else 0.0
	Input.parse_input_event(ev)

func _process(_d: float) -> void:
	frame += 1
	var p = game.player
	var body = p.get_node("CourierVisual/Body")
	var screen: Vector2 = p.get_global_transform_with_canvas().origin
	log_file.store_line("frame=%d tick=%d state=%s pose=%s cell=%d phase=%s dash_ticks=%d x=%.2f y=%.2f sx=%.1f sy=%.1f iframes=%d hp=%d facing=%d" % [
		frame, game.tick_count, GS.NAMES[game.state.current], p.pose, body.frame if body.is_visible_in_tree() else -1,
		p.dash_phase, p.dash_ticks, p.position.x, p.position.y, screen.x, screen.y, p.iframes, p.hp, p.facing])
	log_file.flush()
