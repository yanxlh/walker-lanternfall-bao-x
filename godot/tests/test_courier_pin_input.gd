extends "res://tests/harness.gd"
## Assignment 7 pin through real input and the real game loop. The real main scene runs with test_mode off; a Driver
## node that runs before the session in every physics step parses input events (Input.parse_input_event, then
## Input.flush_buffered_events, so the session reads them in the same step), and a Recorder that runs after the
## session logs what the courier shows. Scripted run: Enter starts, right held 40 steps, release, left held 20 steps,
## one wraith hit, R restarts, right again. Disclosed fixtures: no enemy spawns; the wraith (hp 9999) is placed on
## the courier for one step and then removed. Pins: the run states in order, the cell, mirroring and pose each step,
## the walk speed, and the hit (hp, i-frames, knockback) that the dash is later read against.
## The expected values were recorded with `-- --record` on 9ccf078, before any A7 change (see TEST-REPORT).
const GS = preload("res://game/game_state.gd")
const MAIN := "res://game/main.tscn"

const EXPECTED := {
	"after-restart-cells": [[1, 1], [4, 7], [3, 8], [2, 4], [1, 20]],
	"after-restart-start": [0.0, 10, 1],
	"cells": [[2, 1], [4, 7], [3, 7], [2, 8], [3, 8], [2, 8], [3, 1], [1, 1], [4, 7], [1, 2], [2, 7], [3, 8], [2, 5], [1, 11], [5, 11], [1, 29], [4, 7], [1, 22]],
	"flips": [[1, 50], [-1, 100]],
	"hit-step": [10, 8, 48, 30.0, 32.67],
	"iframes-run-out": [102],
	"poses": [["walk_contact", 1], ["cast", 7], ["walk_passing", 7], ["walk_contact", 8], ["walk_passing", 8], ["walk_contact", 8], ["walk_passing", 1], ["idle", 1], ["cast", 7], ["idle", 2], ["walk_contact", 7], ["walk_passing", 8], ["walk_contact", 5], ["idle", 11], ["hurt", 11], ["idle", 29], ["cast", 7], ["idle", 22]],
	"run-states-in-order": ["menu>playing", "playing>playing"],
	"ticks-are-consecutive": [true, true],
	"walk-speed-x-after-40-steps": [60.0, 0.0],
	"x-after-left-walk": [30.0],
}

var game
var record := false
var observed := {}
var steps := 0
var rows: Array = []
var states: Array = []
var wraith

class Driver extends Node:
	var on_step: Callable
	func _physics_process(_d: float) -> void:
		on_step.call()

class Recorder extends Node:
	var on_step: Callable
	func _physics_process(_d: float) -> void:
		on_step.call()

func shown_cell() -> int:
	var p = game.player
	var body = p.get_node_or_null("CourierVisual/Body")
	if body:
		return body.frame if body.is_visible_in_tree() and body.texture != null else -1
	return p.POSES.find(p.pose) if p.sheet != null else -1

func shown_flip() -> int:
	var visual = game.player.get_node_or_null("CourierVisual")
	if visual:
		return 1 if visual.scale.x > 0 else -1
	return game.player.facing

func rle(values: Array) -> Array:
	var out := []
	for v in values:
		if not out.is_empty() and typeof(out[-1][0]) == typeof(v) and out[-1][0] == v:
			out[-1][1] += 1
		else:
			out.append([v, 1])
	return out

func send_action(action: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	ev.strength = 1.0 if pressed else 0.0
	Input.parse_input_event(ev)

func send_key(code: Key) -> void:
	for pressed in [true, false]:
		var ev := InputEventKey.new()
		ev.physical_keycode = code
		ev.keycode = code
		ev.pressed = pressed
		Input.parse_input_event(ev)

## Runs before the session in each physics step. Step 0 is the step whose tick is the run's first.
func _drive() -> void:
	if game.state.current == GS.MENU:
		# Starts the run in this step, before the session's first tick.
		send_key(KEY_ENTER)
		Input.flush_buffered_events()
	match steps:
		0:
			send_action("move_right", true)
		40:
			send_action("move_right", false)
		50:
			send_action("move_left", true)
		70:
			send_action("move_left", false)
		80:
			wraith = game.spawn_enemy("wraith", game.player.position)
			wraith.hp = 9999
		81:
			game.enemies.erase(wraith)
			wraith.free()
		150:
			send_key(KEY_R)
		151:
			send_action("move_right", true)
		170:
			send_action("move_right", false)
	Input.flush_buffered_events()

func _record() -> void:
	if game.state.current == GS.MENU:
		return
	var p = game.player
	rows.append({"tick": game.tick_count, "cell": shown_cell(), "flip": shown_flip(), "pose": p.pose,
		"x": snappedf(p.position.x, 0.01), "y": snappedf(p.position.y, 0.01), "iframes": p.iframes, "hp": p.hp})
	steps += 1

func pin(id: String, got: Array) -> void:
	observed[id] = got
	if record:
		return
	var want = EXPECTED.get(id)
	check(id, want != null and JSON.stringify(got) == JSON.stringify(want), {"observed": got, "expected": want})

func run() -> void:
	suite = "courier_pin_input"
	record = "--record" in OS.get_cmdline_user_args()
	game = load(MAIN).instantiate()
	game.test_no_spawn = true
	root.add_child(game)
	game.state.changed.connect(func(from: int, to: int): states.append("%s>%s" % [GS.NAMES[from], GS.NAMES[to]]))
	var driver := Driver.new()
	driver.on_step = _drive
	driver.process_physics_priority = -100
	root.add_child(driver)
	var recorder := Recorder.new()
	recorder.on_step = _record
	recorder.process_physics_priority = 100
	root.add_child(recorder)
	var guard := 0
	while steps < 190 and guard < 2000:
		await physics_frame
		guard += 1
	driver.queue_free()
	recorder.queue_free()
	send_action("move_right", false)
	send_action("move_left", false)
	Input.flush_buffered_events()
	var first: Array = rows.slice(0, 150)
	var second: Array = rows.slice(150, 190)
	pin("run-states-in-order", states)
	pin("ticks-are-consecutive", [first.map(func(r): return r["tick"]) == range(1, 151), second.map(func(r): return r["tick"]) == range(1, 41)])
	pin("cells", rle(first.map(func(r): return r["cell"])))
	pin("flips", rle(first.map(func(r): return r["flip"])))
	pin("poses", rle(first.map(func(r): return r["pose"])))
	pin("walk-speed-x-after-40-steps", [first[39]["x"], first[39]["y"]])
	pin("x-after-left-walk", [first[69]["x"]])
	# The wraith is placed in step 80, so the hit lands in that step's tick (tick 81, row 80); knockback moves x after.
	pin("hit-step", [first[79]["hp"], first[80]["hp"], first[80]["iframes"], first[80]["x"], first[81]["x"]])
	pin("iframes-run-out", [first.map(func(r): return r["iframes"]).count(0)])
	pin("after-restart-cells", rle(second.map(func(r): return r["cell"])))
	pin("after-restart-start", [second[0]["x"], second[0]["hp"], second[0]["flip"]])
	if record:
		print("RECORD ", JSON.stringify(observed))
	completed = true
