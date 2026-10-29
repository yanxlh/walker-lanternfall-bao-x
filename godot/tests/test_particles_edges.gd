extends "res://tests/harness.gd"
## Edge cases for the particle policy: blocked input, a position discontinuity, and terminal states.
## Fixtures may place the courier, seed enemies or set the clock; events come from physics and parsed keys.
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
var game
var hits := 0

func key(code: int, pressed: bool = true) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)

func frames(count: int) -> void:
	for i in count:
		await physics_frame
		await process_frame

func tap(code: int) -> void:
	key(code)
	await frames(1)
	key(code, false)
	await frames(1)

func fresh(setup: Callable) -> void:
	if is_instance_valid(game):
		game.free()
	hits = 0
	game = Session.new()
	game.test_no_spawn = true
	root.add_child(game)
	game.weapon_hit.connect(func(_at): hits += 1)
	game.run_started.connect(setup, CONNECT_ONE_SHOT)
	await frames(2)
	await tap(KEY_ENTER)

func pinned(at: Vector2) -> void:
	var e = game.spawn_enemy("wraith", at)
	e.hp = 9999.0
	e.speed = 0.0

func nearest_stall() -> Vector2:
	var best := Vector2.INF
	for p in game.ground.props:
		if p["kind"] == "stall" and (best == Vector2.INF or p["pos"].length() < best.length()):
			best = p["pos"]
	return best

func run() -> void:
	suite = "particles_edges"
	# 1. Pushing straight into a stall: input is held but the courier cannot move.
	await fresh(func():
		var stall := nearest_stall()
		game.player.position = Vector2(stall.x - 19.0 - Tuning.PLAYER_RADIUS, stall.y))
	await frames(4)
	var start: Vector2 = game.player.position
	key(KEY_D)
	var emitted := 0
	var moved := 0.0
	for i in 30:
		await frames(1)
		moved = maxf(moved, game.player.position.distance_to(start))
		emitted += 1 if game.particles.trail.emitting else 0
	key(KEY_D, false)
	check("blocked-input-held-no-displacement", moved < 0.01, {"moved": moved})
	check("blocked-push-never-emits", emitted == 0, {"emitting_frames": emitted})
	key(KEY_W)
	await frames(4)
	check("slide-along-blocker-emits", game.particles.trail.emitting)
	key(KEY_W, false)
	await frames(2)
	# 2. A position discontinuity while moving is treated as a teleport for one frame.
	# Walk left, away from the stall that still blocks rightward movement.
	key(KEY_A)
	await frames(10)
	check("moving-before-jump-emits", game.particles.trail.emitting)
	game.player.position += Vector2(0, -120)
	await frames(1)
	check("jump-frame-no-emission", not game.particles.trail.emitting)
	check("jump-trail-follows-feet", game.particles.trail.global_position.is_equal_approx(game.player.global_position + Vector2(0, 7)))
	await frames(1)
	check("after-jump-real-movement-resumes", game.particles.trail.emitting)
	key(KEY_A, false)
	# 3. Restart while D is held: history resets to the new run's origin.
	key(KEY_D)
	await frames(40)
	await tap(KEY_R)
	check("restart-history-at-new-origin", game.particles.previous_position.distance_to(game.player.global_position) <= game.player.speed / Tuning.TICK_HZ + 0.01, {"previous": str(game.particles.previous_position), "player": str(game.player.global_position)})
	check("restart-player-near-origin", game.player.position.length() < 6.0, {"player": str(game.player.position)})
	key(KEY_D, false)
	# 4. Death with live hit bursts and trail.
	await fresh(func():
		game.prog.beam_pierce = 3
		pinned(Vector2(70, 0)))
	key(KEY_D)
	var waited := 0
	while hits == 0 and waited < 120:
		await frames(1)
		waited += 1
	await frames(2)
	check("lost-fixture-has-live-effects", game.particles.hit_bursts.size() >= 1 and game.particles.trail.emitting)
	game.player.hp = 1
	game.player.iframes = 0
	pinned(game.player.position + Vector2(4, 0))
	waited = 0
	while game.state.current != GS.LOST and waited < 30:
		await frames(1)
		waited += 1
	check("real-contact-reaches-lost", game.state.current == GS.LOST)
	check("lost-clears-hit-bursts", game.particles.hit_bursts.is_empty())
	check("lost-stops-freezes-trail", not game.particles.trail.emitting and game.particles.trail.speed_scale == 0.0)
	key(KEY_D, false)
	await tap(KEY_R)
	check("restart-from-lost-clean", game.state.current == GS.PLAYING and game.particles.hit_bursts.is_empty() and game.particles.hits_spawned == 0)
	# 5. Victory with live effects.
	await fresh(func():
		game.prog.beam_pierce = 3
		pinned(Vector2(70, 0)))
	key(KEY_D)
	waited = 0
	while hits == 0 and waited < 120:
		await frames(1)
		waited += 1
	check("won-fixture-has-live-hit", game.particles.hit_bursts.size() >= 1)
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 3
	waited = 0
	while game.state.current != GS.WON and waited < 30:
		await frames(1)
		waited += 1
	check("clock-reaches-won", game.state.current == GS.WON)
	check("won-clears-hit-bursts", game.particles.hit_bursts.is_empty() and game.particles.level_bursts.is_empty())
	check("won-stops-freezes-trail", not game.particles.trail.emitting and game.particles.trail.speed_scale == 0.0)
	key(KEY_D, false)
	game.free()
	completed = true
