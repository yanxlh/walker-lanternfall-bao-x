extends "res://tests/harness.gd"
## Assignment 7 structure test of the courier's state machine against CHANGE-BRIEF.md ("State machine and
## authority", "The dash rules", "Two clocks"): the priority order, the clip each state plays, the dash phase
## table against both Tuning and the dash clip's boundary keys, one authority over the AnimationPlayer, and,
## tick by tick, that the cell on screen is the cell the pose names. New members are read with get() so the
## suite fails on assertions before the dash exists.
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")

const PRIORITY := ["override", "dash", "hurt", "cast", "walk", "idle"]
const STATE_CLIP := {"dash": "dash", "hurt": "hurt", "cast": "cast", "walk": "walk", "idle": "idle"}
const OVERRIDES := ["levelup", "sunflare", "defeat", "victory"]
const TRANSITIONS := {"": ["startup"], "startup": ["active", ""], "active": ["recovery"], "recovery": [""]}
const PHASE_TICKS := {"DASH_STARTUP_TICKS": 6, "DASH_ACTIVE_TICKS": 10, "DASH_RECOVERY_TICKS": 12, "DASH_COOLDOWN_TICKS": 60}
const FPS := 60.0

var game

func fresh() -> void:
	if is_instance_valid(game):
		game.free()
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = true
	root.add_child(game)
	game.start_run(1)

func run() -> void:
	suite = "courier_states"
	await fresh()
	var p = game.player
	var anim: AnimationPlayer = p.get_node("CourierVisual/AnimationPlayer")
	var consts: Dictionary = p.get_script().get_script_constant_map()
	var tuning_consts: Dictionary = (load("res://features/tuning.gd") as Script).get_script_constant_map()

	check("priority-order", consts.get("STATES") == PRIORITY, {"STATES": consts.get("STATES")})
	var missing := []
	for s in STATE_CLIP:
		if not anim.has_animation(STATE_CLIP[s]):
			missing.append(STATE_CLIP[s])
	for o in OVERRIDES:
		if not anim.has_animation(o):
			missing.append(o)
	for pose in p.POSES:
		if not pose.begins_with("walk_") and not anim.has_animation(pose):
			missing.append(pose)
	check("every-state-has-its-clip", missing.is_empty(), {"missing": missing})
	check("dash-transition-table", consts.get("DASH_TRANSITIONS") == TRANSITIONS, {"DASH_TRANSITIONS": consts.get("DASH_TRANSITIONS")})

	# The phase table lives in Tuning, and the dash clip's boundary keys sit on the same ticks.
	var tuning := {}
	for k in PHASE_TICKS:
		tuning[k] = tuning_consts.get(k)
	check("tuning-phase-table", tuning == PHASE_TICKS and tuning_consts.get("DASH_SPEED") == 330.0, {"tuning": tuning, "speed": tuning_consts.get("DASH_SPEED")})
	var dash := anim.get_animation("dash")
	var boundaries := [0, PHASE_TICKS["DASH_STARTUP_TICKS"], PHASE_TICKS["DASH_STARTUP_TICKS"] + PHASE_TICKS["DASH_ACTIVE_TICKS"],
		PHASE_TICKS["DASH_STARTUP_TICKS"] + PHASE_TICKS["DASH_ACTIVE_TICKS"] + PHASE_TICKS["DASH_RECOVERY_TICKS"]]
	var on_boundaries := true
	for t in dash.get_track_count():
		if dash.value_track_get_update_mode(t) != Animation.UPDATE_CONTINUOUS:
			continue
		for b in boundaries:
			var k := dash.track_find_key(t, b / FPS, Animation.FIND_MODE_APPROX)
			on_boundaries = on_boundaries and k >= 0 and absf(dash.track_get_key_time(t, k) - b / FPS) < 1e-6
	check("clip-boundaries-match-tuning", on_boundaries and absf(dash.length - boundaries[-1] / FPS) < 1e-6, {"boundary_ticks": boundaries, "length_ticks": dash.length * FPS})

	# The clock: manual mode in the running game, and no other animation driver anywhere in the courier.
	check("runtime-callback-mode-manual", anim.callback_mode_process == AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL and anim.autoplay == "", {"mode": anim.callback_mode_process})
	var other := []
	for n in p.find_children("*", "", true, false):
		if (n is AnimationPlayer and n != anim) or n is AnimationTree or n is AnimatedSprite2D:
			other.append(str(p.get_path_to(n)))
	check("one-animation-driver", other.is_empty() and p.find_children("CourierVisual", "", false, false).size() == 1, {"others": other})

	# One authority in source: only player.gd plays or seeks the courier's clips or sets the Body frame.
	var offenders := []
	var re := RegEx.create_from_string("(courier_visual|CourierVisual|\\banim\\.(play|seek|advance)|Body\\.frame|\\.frame\\s*=)")
	for dir in ["res://features", "res://game", "res://ui", "res://effects", "res://audio"]:
		for file in _scripts(dir):
			if file in ["res://features/player/player.gd", "res://features/player/build_courier_visual.gd"]:
				continue
			if re.search(FileAccess.get_file_as_string(file)):
				offenders.append(file)
	check("one-authority-in-source", offenders.is_empty(), {"offenders": offenders})

	# Tick by tick through walking, cast, a hit and a level-up: the state's clip is the clip playing, and the cell
	# on screen is the cell the pose names.
	var mismatches := []
	var states_seen := {}
	var run_ticks := func(n: int, axis: Vector2) -> void:
		game.test_axis = axis
		for i in n:
			game.tick()
			var state: String = p.call("current_state")
			states_seen[state] = true
			# The visual is set inside step(), from the pose chosen there; the weapons and the hit come later in
			# the same tick (the one-tick lag the pin records), so the clip follows the pose, not the state now.
			var want_clip: String = "walk" if p.pose.begins_with("walk_") else p.pose
			var body: Sprite2D = p.get_node("CourierVisual/Body")
			if anim.current_animation != want_clip:
				mismatches.append({"tick": game.tick_count, "state": state, "pose": p.pose, "clip": anim.current_animation})
			if state != "dash" and body.frame != p.POSES.find(p.pose):
				mismatches.append({"tick": game.tick_count, "pose": p.pose, "frame": body.frame})
	run_ticks.call(50, Vector2.RIGHT)
	var w = game.spawn_enemy("wraith", p.position)
	w.hp = 9999
	run_ticks.call(1, Vector2.ZERO)
	game.enemies.erase(w)
	w.free()
	run_ticks.call(20, Vector2.ZERO)
	game.prog.add_xp(game.prog.xp_needed())
	run_ticks.call(1, Vector2.RIGHT)
	game.choose_card(game.offered.find("heal") if "heal" in game.offered else 1)
	run_ticks.call(10, Vector2.RIGHT)
	check("clip-and-cell-follow-the-state", mismatches.is_empty() and states_seen.has("walk") and states_seen.has("cast") and states_seen.has("hurt") and states_seen.has("idle"),
		{"mismatches": mismatches.slice(0, 5), "states_seen": states_seen.keys()})
	completed = true

func _scripts(dir: String) -> Array:
	var out := []
	var d := DirAccess.open(dir)
	if d == null:
		return out
	for f in d.get_files():
		if f.ends_with(".gd"):
			out.append(dir + "/" + f)
	for sub in d.get_directories():
		out.append_array(_scripts(dir + "/" + sub))
	return out
