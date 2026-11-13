extends "res://tests/harness.gd"
## Assignment 7 dash edges (CHANGE-BRIEF.md "The dash rules"), at every phase boundary. Presses go through
## Input.parse_input_event and session._unhandled_input; ticks go through session.tick(). Hits are real contact:
## a wraith (hp 9999) is placed on the courier before the target tick and removed after it.
## Disclosed fixtures: no enemy spawns; the dash card is put in the offer (offers are random) and picked with a
## parsed "1" key. The last part drops test_mode and runs the real physics loop, so its tick counts must match at
## 30, 60 and 144 fps. New properties are read with get() so the suite fails on assertions, not on a script error,
## before the dash exists.
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")

const STARTUP := 6
const ACTIVE := 10
const RECOVERY := 12
const COOLDOWN := 60
const SPEED := 330.0
const DISTANCE := 55.0
const TRANSITIONS := {"": ["startup"], "startup": ["active", ""], "active": ["recovery"], "recovery": [""]}

var game
var seen_transitions := {}

func fresh(seed_value: int = 1) -> void:
	if is_instance_valid(game):
		game.free()
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = true
	root.add_child(game)
	game.start_run(seed_value)
	if game.player.has_signal("dash_phase_changed"):
		game.player.dash_phase_changed.connect(func(from: String, to: String): seen_transitions["%s>%s" % [from, to]] = true)
	await process_frame

func key(code: Key) -> void:
	var down := InputEventKey.new()
	down.physical_keycode = code
	down.keycode = code
	down.pressed = true
	Input.parse_input_event(down)
	var up: InputEventKey = down.duplicate()
	up.pressed = false
	Input.parse_input_event(up)
	await process_frame
	await process_frame

## Unlocks the dash through a level-up and the card key.
func unlock() -> void:
	game.prog.add_xp(game.prog.xp_needed())
	game.tick()
	game.offered = Array(["dash", "heal", "heal"], TYPE_STRING, "", null)
	await key(KEY_1)

func phase() -> String:
	return str(game.player.get("dash_phase"))

func ticks(n: int, axis: Vector2 = Vector2.ZERO) -> Array:
	game.test_axis = axis
	var out := []
	for i in n:
		game.tick()
		out.append(phase())
	return out

func rep(v, n: int) -> Array:
	var out := []
	out.resize(n)
	out.fill(v)
	return out

func counts(phases: Array) -> Dictionary:
	var c := {"startup": 0, "active": 0, "recovery": 0, "": 0}
	for p in phases:
		c[p] = c.get(p, 0) + 1
	return c

## A wraith on the courier now, so the next tick's contact check hits; returns it for removal.
func wraith_on_courier() -> Node2D:
	var w = game.spawn_enemy("wraith", game.player.position)
	w.hp = 9999
	return w

func remove(w) -> void:
	game.enemies.erase(w)
	w.free()

func cell() -> int:
	var body = game.player.get_node_or_null("CourierVisual/Body")
	return body.frame if body and body.is_visible_in_tree() else -1

func rig_shown() -> bool:
	var rig = game.player.get_node_or_null("CourierVisual/Rig")
	return rig != null and rig.is_visible_in_tree()

class Recorder extends Node:
	var game
	var samples := {}
	func _physics_process(_d: float) -> void:
		samples[game.tick_count] = [str(game.player.get("dash_phase")), game.player.position.x]

## The render rate this run is pinned to: the median process delta is 1 / N under --fixed-fps N.
func measured_fps() -> int:
	var deltas := []
	for i in 9:
		await process_frame
		deltas.append(root.get_process_delta_time())
	deltas.sort()
	return roundi(1.0 / deltas[4])

func run() -> void:
	var rate: int = await measured_fps()
	suite = "dash_edges_%dfps" % rate
	var fps := Engine.physics_ticks_per_second

	# Locked: a press does nothing; the card is offered and unlocks it.
	await fresh()
	await key(KEY_SHIFT)
	var locked := ticks(3, Vector2.RIGHT)
	check("locked-press-dropped", locked == ["", "", ""] and game.player.get("dash_unlocked") != true, {"phases": locked})
	check("card-offered-while-locked", "dash" in game.prog.eligible_cards(), {"eligible": game.prog.eligible_cards()})
	check("card-has-text", game.prog.CARD_TEXT.has("dash"), {})
	await unlock()
	check("card-unlocks", game.state.current == GS.PLAYING and game.player.get("dash_unlocked") == true and not ("dash" in game.prog.eligible_cards()), {"state": GS.NAMES[game.state.current], "eligible": game.prog.eligible_cards()})

	# One whole dash with right held: phases, movement, visual.
	ticks(5)
	var x0: float = game.player.position.x
	await key(KEY_SHIFT)
	check("press-is-a-request-until-the-tick", game.player.get("dash_requested") == true and phase() == "", {"phase": phase()})
	game.test_axis = Vector2.RIGHT
	var phases := []
	var xs := []
	var shown := []
	for i in 29:
		game.tick()
		phases.append(phase())
		xs.append(game.player.position.x - x0)
		shown.append([cell(), rig_shown(), game.player.pose])
	check("phase-lengths", phases.slice(0, 28) == rep("startup", STARTUP) + rep("active", ACTIVE) + rep("recovery", RECOVERY) and phases[28] == "", {"counts": counts(phases)})
	check("startup-holds-still", xs.slice(0, STARTUP).all(func(x): return is_zero_approx(x)), {"x": xs.slice(0, STARTUP)})
	var steps_ok := true
	for i in range(STARTUP, STARTUP + ACTIVE):
		steps_ok = steps_ok and is_equal_approx(xs[i] - (xs[i - 1] if i > 0 else 0.0), SPEED / Tuning.TICK_HZ)
	check("active-moves-5.5-per-tick", steps_ok, {"x": xs.slice(STARTUP - 1, STARTUP + ACTIVE)})
	check("active-distance-55", is_equal_approx(xs[STARTUP + ACTIVE - 1], DISTANCE), {"x_after_active": xs[STARTUP + ACTIVE - 1]})
	check("recovery-holds-still", xs.slice(STARTUP + ACTIVE, 28).all(func(x): return is_equal_approx(x, DISTANCE)), {"x": xs.slice(STARTUP + ACTIVE, 28)})
	check("walks-again-after", xs[28] > DISTANCE, {"x": xs[28]})
	check("rig-shown-during-dash", shown.slice(0, 28).all(func(s): return s[0] == -1 and s[1] and s[2] == "dash"), {"first": shown[0], "last": shown[27]})
	check("sprite-back-after-dash", shown[28][0] in [2, 3, 4] and not shown[28][1], {"after": shown[28]})
	check("cooldown-starts-when-dash-ends", game.player.get("dash_cooldown") == COOLDOWN, {"cooldown": game.player.get("dash_cooldown")})

	# Cooldown boundary: the press after 59 cooldown ticks is dropped, the press after 60 starts a dash.
	ticks(COOLDOWN - 1)
	await key(KEY_SHIFT)
	var early := ticks(1)
	check("press-on-last-cooldown-tick-dropped", early == [""] and game.player.get("dash_requested") == false, {"phase": early, "cooldown": game.player.get("dash_cooldown")})
	await key(KEY_SHIFT)
	var ready := ticks(1)
	check("press-after-cooldown-starts", ready == ["startup"], {"phase": ready})

	# A press during a dash is dropped, not queued.
	ticks(STARTUP + 2)
	await key(KEY_SHIFT)
	var rest := ticks(28 - (STARTUP + 3) + COOLDOWN + 5)
	check("press-during-dash-dropped", not ("startup" in rest) and game.player.get("dash_requested") == false, {"after_press": counts(rest)})

	# Direction: locked at the start; no input means the facing direction; a diagonal is normalised.
	await fresh()
	await unlock()
	ticks(1, Vector2.LEFT)
	var start: Vector2 = game.player.position
	await key(KEY_SHIFT)
	ticks(STARTUP, Vector2.ZERO)
	ticks(ACTIVE, Vector2.RIGHT)
	check("no-input-dashes-along-facing", is_equal_approx(game.player.position.x - start.x, -DISTANCE) and game.player.facing == -1,
		{"dx": game.player.position.x - start.x, "facing": game.player.facing})
	ticks(RECOVERY + COOLDOWN + 1)
	start = game.player.position
	game.test_axis = Vector2(1, 1)
	await key(KEY_SHIFT)
	ticks(STARTUP + ACTIVE, Vector2(1, 1))
	check("diagonal-normalised", is_equal_approx((game.player.position - start).length(), DISTANCE), {"d": (game.player.position - start).length()})

	# Hits at the phase boundaries. Startup: cancelled, no cooldown. Active: continues. Recovery: cancelled, cooldown.
	for case in [["last-startup", STARTUP], ["first-active", STARTUP + 1], ["last-active", STARTUP + ACTIVE], ["first-recovery", STARTUP + ACTIVE + 1]]:
		await fresh()
		await unlock()
		var hp0: int = game.player.hp
		await key(KEY_SHIFT)
		var before := ticks(case[1] - 1)
		var w := wraith_on_courier()
		# The phase changes inside the hit tick: the tick's own phase step, then the hit's cancel, if any.
		var during := []
		var rec := func(from: String, to: String): during.append("%s>%s" % [from, to])
		game.player.dash_phase_changed.connect(rec)
		var at := ticks(1)
		game.player.dash_phase_changed.disconnect(rec)
		remove(w)
		var after := ticks(2)
		var obs := {"changes_in_hit_tick": during, "phase_after_hit_tick": at[0], "after": after, "hp": game.player.hp, "iframes": game.player.iframes, "cooldown": game.player.get("dash_cooldown")}
		var damaged: bool = game.player.hp < hp0
		match case[0]:
			"last-startup":
				check("hit-last-startup-tick-cancels-no-cooldown", during == ["startup>"] and before.size() == 5 and before.all(func(x): return x == "startup") and after == ["", ""] and damaged and game.player.get("dash_cooldown") == 0, obs)
				check("hurt-pose-after-startup-cancel", game.player.pose == "hurt" and cell() == 5, {"pose": game.player.pose})
				await key(KEY_SHIFT)
				check("dash-again-after-startup-cancel", ticks(1) == ["startup"], {})
			"first-active":
				check("hit-first-active-tick-continues", during == ["startup>active"] and after == ["active", "active"] and damaged and game.player.iframes > 0, obs)
				check("not-invincible-during-active", damaged, {"hp": game.player.hp, "was": hp0})
			"last-active":
				check("hit-last-active-tick-continues", during == [] and at == ["active"] and after == ["recovery", "recovery"] and damaged, obs)
				check("dash-pose-kept-after-active-hit", game.player.pose == "dash" and rig_shown(), {"pose": game.player.pose})
			"first-recovery":
				check("hit-first-recovery-tick-cancels-with-cooldown", during == ["active>recovery", "recovery>"] and after == ["", ""] and damaged and game.player.get("dash_cooldown") == COOLDOWN - 2, obs)

	# Level-up in each phase: the dash freezes with the run and resumes on the same tick.
	for frame in [2, STARTUP + 3, STARTUP + ACTIVE + 4]:
		await fresh()
		await unlock()
		await key(KEY_SHIFT)
		var first := ticks(frame - 1)
		game.prog.add_xp(game.prog.xp_needed())
		first.append_array(ticks(1))
		var frozen_at = game.player.get("dash_ticks")
		var in_levelup: bool = game.state.current == GS.LEVELUP
		var frozen_view := [cell(), rig_shown()]
		ticks(10)
		var still_frozen: bool = game.player.get("dash_ticks") == frozen_at
		game.offered = Array(["heal", "heal", "heal"], TYPE_STRING, "", null)
		await key(KEY_1)
		var resumed_view := [cell(), rig_shown()]
		var second := ticks(30 - frame)
		var all := first + second
		check("levelup-freezes-dash-at-frame-%d" % frame, in_levelup and still_frozen and frozen_view == [6, false] and resumed_view == [-1, true],
			{"dash_ticks": frozen_at, "levelup_view": frozen_view, "resumed_view": resumed_view})
		check("levelup-keeps-phase-lengths-at-frame-%d" % frame, counts(all.slice(0, 28)) == {"startup": STARTUP, "active": ACTIVE, "recovery": RECOVERY, "": 0}, {"counts": counts(all.slice(0, 28))})

	# Death during the dash shows defeat; restart clears everything.
	await fresh()
	await unlock()
	await key(KEY_SHIFT)
	ticks(STARTUP + 2)
	game.player.hp = 1
	var killer := wraith_on_courier()
	ticks(1)
	check("death-during-dash-shows-defeat", game.state.current == GS.LOST and cell() == 8 and not rig_shown(), {"state": GS.NAMES[game.state.current], "cell": cell()})
	remove(killer)
	await fresh()
	await unlock()
	await key(KEY_SHIFT)
	ticks(STARTUP + 2, Vector2.RIGHT)
	await key(KEY_R)
	check("restart-clears-dash", phase() == "" and game.player.get("dash_unlocked") != true and game.player.get("dash_cooldown") == 0
		and game.player.get("dash_requested") == false and cell() == 1 and not rig_shown(), {"phase": phase(), "cell": cell()})

	# Walls: the arena clamp and the market blocker hold during the dash.
	await fresh()
	await unlock()
	var edge: float = Tuning.ARENA.end.x - 16
	game.player.position = Vector2(edge - 20, 0)
	await key(KEY_SHIFT)
	ticks(STARTUP + ACTIVE, Vector2.RIGHT)
	check("arena-clamp-holds", game.player.position.x <= edge + 0.001, {"x": game.player.position.x, "edge": edge})
	var box: Rect2 = game.ground.solids[0]
	game.player.position = Vector2(box.position.x - Tuning.PLAYER_RADIUS - 20, box.get_center().y)
	ticks(RECOVERY + COOLDOWN + 1)
	game.player.position = Vector2(box.position.x - Tuning.PLAYER_RADIUS - 20, box.get_center().y)
	await key(KEY_SHIFT)
	ticks(STARTUP + ACTIVE, Vector2.RIGHT)
	check("blocker-holds", game.player.position.x <= box.position.x - Tuning.PLAYER_RADIUS + 0.001 and not game.ground.blocks(game.player.position, Tuning.PLAYER_RADIUS - 0.01),
		{"x": game.player.position.x, "box_left": box.position.x})

	# Weapons keep firing; the dash pose outranks the cast pose.
	await fresh()
	await unlock()
	while game.beam_timer != 4:
		ticks(1)
	var shots_before: int = game.shots.size()
	await key(KEY_SHIFT)
	ticks(STARTUP)
	check("beam-fires-during-dash", game.shots.size() > shots_before and game.player.cast_ticks > 0 and game.player.pose == "dash", {"shots": [shots_before, game.shots.size()], "cast_ticks": game.player.cast_ticks, "pose": game.player.pose})

	# The input trap: Input.action_press never reaches _unhandled_input, so it cannot request a dash.
	await fresh()
	await unlock()
	Input.action_press("dash")
	await process_frame
	await process_frame
	var pressed_by_action := ticks(2)
	Input.action_release("dash")
	check("action-press-does-not-reach-unhandled-input", pressed_by_action == ["", ""], {"phases": pressed_by_action})

	# Every phase change seen above is in the brief's table.
	var illegal := []
	for t in seen_transitions:
		var pair: PackedStringArray = t.split(">")
		if not TRANSITIONS.get(pair[0], []).has(pair[1]):
			illegal.append(t)
	check("only-legal-transitions", not seen_transitions.is_empty() and illegal.is_empty(), {"seen": seen_transitions.keys(), "illegal": illegal})

	# The real loop at this frame rate: held movement and a dash key; a recorder that runs after the session in
	# every physics step logs the tick count, the phase and x.
	await fresh()
	await unlock()
	var recorder := Recorder.new()
	recorder.game = game
	recorder.process_physics_priority = 100
	root.add_child(recorder)
	game.test_mode = false
	var hold := InputEventAction.new()
	hold.action = "move_right"
	hold.pressed = true
	hold.strength = 1.0
	Input.parse_input_event(hold)
	await process_frame
	await key(KEY_SHIFT)
	var guard := 0
	while guard < 600 and recorder.samples.size() < 60:
		await physics_frame
		guard += 1
	var release: InputEventAction = hold.duplicate()
	release.pressed = false
	release.strength = 0.0
	Input.parse_input_event(release)
	game.test_mode = true
	recorder.queue_free()
	var ordered: Array = recorder.samples.keys()
	ordered.sort()
	var loop_phases := ordered.map(func(t): return recorder.samples[t][0])
	var c := counts(loop_phases)
	var first_active: int = loop_phases.find("active")
	var first_recovery: int = loop_phases.find("recovery")
	var dx := 0.0
	if first_active > 0 and first_recovery > 0:
		dx = recorder.samples[ordered[first_recovery]][1] - recorder.samples[ordered[first_active - 1]][1]
	var gaps := 0
	for i in range(1, ordered.size()):
		gaps += 1 if ordered[i] != ordered[i - 1] + 1 else 0
	check("real-loop-phase-ticks-at-%dfps" % rate,
		gaps == 0 and c["startup"] == STARTUP and c["active"] == ACTIVE and c["recovery"] == RECOVERY and is_equal_approx(dx, DISTANCE),
		{"physics_ticks_per_second": fps, "counts": c, "active_distance": dx, "ticks_logged": ordered.size(), "missing_ticks": gaps, "physics_frames_awaited": guard})
	completed = true
