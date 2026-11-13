extends "res://tests/harness.gd"
## Assignment 7 pin, written before the courier's visual changes. It records what the courier shows tick by tick
## through the real simulation (session.tick), with no spawns: the sheet cell, the mirroring, the pose name and the
## tint path. It must pass on the unchanged code and, unchanged, after the move to a Sprite2D and an AnimationPlayer.
## `shown_cell()` is the only adapter: it reads the cell _draw() picks today, or the Body sprite's frame afterwards.
## Run with `-- --record` to print the observed sequences as run-length pairs instead of checking them.
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

## [cell, ticks] run-length pairs, observed on 9ccf078 with `-- --record` (13 November 2026).
const EXPECTED := {
	"deadzone-cells": [[2, 3], [3, 8], [4, 1]],
	"deadzone-flips": [[-1, 12]],
	"defeat-cells": [[8, 3]],
	"defeat-state": [true],
	"evolve-cells": [[7, 60], [1, 11]],
	"hurt-cells": [[4, 1], [5, 11], [1, 24], [4, 7], [1, 17]],
	"hurt-iframes-at-hit": [48, 8],
	"levelup-cells": [[6, 6], [4, 3], [2, 7], [3, 1]],
	"levelup-state": [true],
	"no-art-cells": [[-1, 30]],
	"restart-cell-flip": [1, 1],
	"restart-cells": [[1, 1], [4, 1]],
	"start-cell-flip-pose": [1, 1, "idle"],
	"stop-cells": [[1, 1], [4, 7], [1, 2]],
	"victory-cells": [[9, 3]],
	"walk-after-hurt-cells": [[2, 7], [3, 8], [2, 1], [4, 4]],
	"walk-left-cells": [[2, 7], [3, 8], [2, 5]],
	"walk-left-flips": [[-1, 20]],
	"walk-right-cells": [[2, 1], [4, 7], [3, 7], [2, 8], [3, 8], [2, 8], [3, 1]],
	"walk-right-flips": [[1, 40]],
	"walk-right-poses": [["walk_contact", 1], ["cast", 7], ["walk_passing", 7], ["walk_contact", 8], ["walk_passing", 8], ["walk_contact", 8], ["walk_passing", 1]],
}

var game
var record := false
var observed := {}

func fresh(seed_value: int = 1) -> void:
	if is_instance_valid(game):
		game.free()
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = true
	root.add_child(game)
	game.start_run(seed_value)

## The sheet cell the courier shows: -1 when nothing from the sheet is drawn (no sheet, or the sprite hidden).
func shown_cell() -> int:
	var p = game.player
	var body = p.get_node_or_null("CourierVisual/Body")
	if body:
		return body.frame if body.is_visible_in_tree() and body.texture != null else -1
	return p.POSES.find(p.pose) if p.sheet != null else -1

## +1 drawn as on the sheet, -1 mirrored.
func shown_flip() -> int:
	var p = game.player
	var visual = p.get_node_or_null("CourierVisual")
	if visual:
		return 1 if visual.scale.x > 0 else -1
	return p.facing

func rle(values: Array) -> Array:
	var out := []
	for v in values:
		if not out.is_empty() and typeof(out[-1][0]) == typeof(v) and out[-1][0] == v:
			out[-1][1] += 1
		else:
			out.append([v, 1])
	return out

## Steps n ticks with the given axis and returns [cells, flips, poses] after each tick.
func steps(n: int, axis: Vector2) -> Array:
	game.test_axis = axis
	var cells := []
	var flips := []
	var poses := []
	for i in n:
		game.tick()
		cells.append(shown_cell())
		flips.append(shown_flip())
		poses.append(game.player.pose)
	return [cells, flips, poses]

func pin(id: String, values: Array) -> void:
	pin_raw(id, rle(values))

## Compares the values as they are, without run-length pairs.
func pin_raw(id: String, got: Array) -> void:
	observed[id] = got
	if record:
		return
	var want = EXPECTED.get(id)
	check(id, want != null and JSON.stringify(got) == JSON.stringify(want), {"observed": got, "expected": want})

func run() -> void:
	suite = "courier_pin"
	record = "--record" in OS.get_cmdline_user_args()

	await fresh()
	pin_raw("start-cell-flip-pose", [shown_cell(), shown_flip(), game.player.pose])
	var walk := steps(40, Vector2.RIGHT)
	pin("walk-right-cells", walk[0])
	pin("walk-right-flips", walk[1])
	pin("walk-right-poses", walk[2])
	var stop := steps(10, Vector2.ZERO)
	pin("stop-cells", stop[0])
	var left := steps(20, Vector2.LEFT)
	pin("walk-left-cells", left[0])
	pin("walk-left-flips", left[1])
	var diag := steps(12, Vector2(0.08, 1))
	pin("deadzone-cells", diag[0])
	pin("deadzone-flips", diag[1])

	# One accepted hit through real contact, then the wraith is removed so it cannot hit again.
	await fresh()
	steps(45, Vector2.ZERO)
	var w = game.spawn_enemy("wraith", game.player.position)
	w.hp = 9999
	var hit := steps(1, Vector2.ZERO)
	pin_raw("hurt-iframes-at-hit", [game.player.iframes, game.player.hp])
	game.enemies.erase(w)
	w.free()
	var after_hit := steps(59, Vector2.ZERO)
	pin("hurt-cells", hit[0] + after_hit[0])
	var walk_hurt_fresh := steps(20, Vector2.RIGHT)
	pin("walk-after-hurt-cells", walk_hurt_fresh[0])

	# Level-up: the override shows while the simulation is frozen and clears when a card is chosen.
	await fresh()
	steps(45, Vector2.RIGHT)
	game.prog.add_xp(3)
	var lv := steps(1, Vector2.RIGHT)
	var frozen := steps(5, Vector2.RIGHT)
	var lv_cells: Array = lv[0] + frozen[0]
	pin_raw("levelup-state", [game.state.current == GS.LEVELUP])
	game.choose_card(0)
	lv_cells.append(shown_cell())
	lv_cells.append_array(steps(10, Vector2.RIGHT)[0])
	pin("levelup-cells", lv_cells)

	# Evolution: the sunflare override for EVOLVE_POSE_TICKS, then the empowered courier.
	await fresh()
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(game.prog.xp_needed())
	game.tick()
	game.choose_card(game.offered.find("sunflare"))
	var evo_cells := [shown_cell()]
	evo_cells.append_array(steps(70, Vector2.ZERO)[0])
	pin("evolve-cells", evo_cells)

	# Defeat through real contact.
	await fresh()
	game.player.hp = 1
	var w2 = game.spawn_enemy("wraith", game.player.position)
	w2.hp = 9999
	var dead := steps(3, Vector2.ZERO)
	pin("defeat-cells", dead[0])
	pin_raw("defeat-state", [game.state.current == GS.LOST])

	# Victory at the end of the run.
	await fresh()
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	var won := steps(3, Vector2.ZERO)
	pin("victory-cells", won[0])

	# Restart in the middle of a walk, facing left.
	await fresh()
	steps(13, Vector2.LEFT)
	game.start_run(1)
	pin_raw("restart-cell-flip", [shown_cell(), shown_flip()])
	pin("restart-cells", steps(2, Vector2.ZERO)[0])

	# Without the sheet nothing is drawn from it; the pose names are the same as with it.
	Art.disabled = true
	await fresh()
	var bare := steps(30, Vector2.RIGHT)
	Art.disabled = false
	await fresh()
	var full := steps(30, Vector2.RIGHT)
	pin("no-art-cells", bare[0])
	check("no-art-same-poses", bare[2] == full[2], {"without": rle(bare[2]), "with": rle(full[2])})

	# The hurt tint reaches whatever draws the courier: the courier itself, or children that use its material.
	await fresh()
	var p = game.player
	var drawers := []
	var all_use_parent := true
	for n in p.find_children("*", "CanvasItem", true, false):
		if n is Sprite2D or n is Polygon2D:
			drawers.append(str(p.get_path_to(n)))
			var at: Node = n
			while at != p:
				all_use_parent = all_use_parent and (at as CanvasItem).use_parent_material and (at as CanvasItem).material == null
				at = at.get_parent()
	check("tint-reaches-every-courier-drawer", p.material is ShaderMaterial and all_use_parent, {"material": str(p.material), "child_drawers": drawers})

	if record:
		print("RECORD ", JSON.stringify(observed))
	completed = true
