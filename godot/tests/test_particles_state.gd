extends "res://tests/harness.gd"
## Seeded scene fixtures; events come only from normal physics and parsed keyboard input.
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
var game
var hit_events: Array[Vector2] = []
var first
var second
var tough
var fixture_pending := true

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

func run() -> void:
	suite = "particles_state"
	game = Session.new()
	game.test_no_spawn = true
	root.add_child(game)
	game.weapon_hit.connect(func(at): hit_events.append(at))
	game.run_started.connect(func():
		if fixture_pending:
			fixture_pending = false
			# Seed the world before its first physics tick; leave damage and trigger functions alone.
			game.prog.beam_pierce = 3
			first = game.spawn_enemy("moth", Vector2(70, 0))
			second = game.spawn_enemy("moth", Vector2(85, 0))
			tough = game.spawn_enemy("wraith", Vector2(105, 0)))
	await frames(2)
	check("menu-no-bursts", game.particles.hit_bursts.is_empty() and game.particles.level_bursts.is_empty())
	check("menu-no-trail", not game.particles.trail.emitting)
	await tap(KEY_ENTER)
	check("real-start-input", game.state.current == GS.PLAYING and not game.test_mode)
	check("idle-no-trail", not game.particles.trail.emitting)
	# The real automatic beam drives the hits in the seeded world.
	await frames(18)
	check("real-beam-hits", hit_events.size() >= 3, {"events": hit_events.size()})
	check("rapid-hits-overlap", game.particles.hit_bursts.size() >= 2, {"live": game.particles.hit_bursts.size()})
	check("lethal-hit-survives-enemy-free", not is_instance_valid(first) and not is_instance_valid(second) and game.particles.hit_bursts.size() >= 2)
	check("nonlethal-hit-also-bursts", is_instance_valid(tough) and tough.hp < 8 and tough.hp > 0)
	var correct_positions: bool = game.particles.hit_bursts.size() == hit_events.size()
	for i in mini(game.particles.hit_bursts.size(), hit_events.size()):
		correct_positions = correct_positions and game.particles.hit_bursts[i].global_position.is_equal_approx(game.to_global(hit_events[i]))
	check("hit-event-position", correct_positions)
	check("one-instance-per-accepted-hit", game.particles.hits_spawned == hit_events.size())
	await tap(KEY_P)
	check("pause-freezes-hit", game.state.current == GS.PAUSED and game.particles.hit_bursts[0].speed_scale == 0.0)
	check("pause-stops-freezes-trail", not game.particles.trail.emitting and game.particles.trail.speed_scale == 0.0)
	await tap(KEY_P)
	key(KEY_D)
	await frames(3)
	check("real-movement-starts-trail", game.particles.trail.emitting)
	check("trail-follows-feet", game.particles.trail.global_position.is_equal_approx(game.player.global_position + Vector2(0, 7)))
	check("trail-world-coordinates", not game.particles.trail.local_coords)
	game.particles.hide()
	await frames(2)
	check("hidden-stops-emission-keeps-simulation", not game.particles.trail.emitting and game.particles.trail.speed_scale == 1.0)
	game.particles.show()
	await frames(2)
	check("visible-moving-resumes-trail", game.particles.trail.emitting)
	key(KEY_D, false)
	await frames(2)
	check("idle-stops-trail", not game.particles.trail.emitting)
	# Place a real pickup at the courier. Pickup processing awards XP and emits the real level signal.
	game.drop_gem(game.player.position, game.prog.xp_needed())
	await frames(2)
	check("real-pickup-causes-levelup", game.state.current == GS.LEVELUP)
	check("upgrade-burst-at-ui-portrait", game.particles.level_bursts.size() == 1 and game.particles.level_bursts[0].position.is_equal_approx(Vector2(56, 325)))
	check("upgrade-overlay-above-hud", game.particles.level_overlay.layer > game.hud.layer)
	var upgrade_particle = game.particles.level_bursts[0]
	check("upgrade-screen-position-matches-portrait", upgrade_particle.get_global_transform_with_canvas().origin.is_equal_approx(game.hud.transform * Vector2(56, 325)))
	var before_camera_change: Vector2 = upgrade_particle.get_global_transform_with_canvas().origin
	game.camera.position += Vector2(40, 20)
	await frames(1)
	check("upgrade-position-independent-of-camera", upgrade_particle.get_global_transform_with_canvas().origin.is_equal_approx(before_camera_change))
	check("upgrade-celebration-continues-on-card-screen", game.particles.level_bursts.size() == 1 and game.particles.level_bursts[0].speed_scale == 1.0)
	check("upgrade-stops-freezes-trail", not game.particles.trail.emitting and game.particles.trail.speed_scale == 0.0)
	await tap(KEY_1)
	check("real-card-input-resumes-game", game.state.current == GS.PLAYING)
	await tap(KEY_R)
	check("restart-clears-bursts", game.particles.hit_bursts.is_empty() and game.particles.level_bursts.is_empty())
	check("restart-resets-counters", game.particles.hits_spawned == 0 and game.particles.levels_spawned == 0)
	check("restart-no-phantom-trail", not game.particles.trail.emitting)
	game.free()
	# Stress fixture: forty ordinary enemies intersect a high-pierce beam in real physics.
	game = Session.new()
	game.test_no_spawn = true
	root.add_child(game)
	game.run_started.connect(func():
		game.prog.beam_pierce = 40
		for i in 40:
			game.spawn_enemy("wraith", Vector2(70 + i * 0.2, 0)))
	await tap(KEY_ENTER)
	await frames(18)
	check("hit-cap-sees-all-events", game.particles.hits_seen == 40, {"seen": game.particles.hits_seen})
	check("hit-cap-limits-instances", game.particles.hits_spawned == 32 and game.particles.hit_bursts.size() == 32)
	check("hit-cap-allocation", game.particles.hit_bursts.size() * 16 == 512)
	# A real pickup can award several levels in a single game tick.
	game.drop_gem(game.player.position, 51)
	await frames(2)
	check("level-cap-sees-all-events", game.particles.levels_seen == 6, {"seen": game.particles.levels_seen})
	check("level-cap-limits-instances", game.particles.levels_spawned == 4 and game.particles.level_bursts.size() == 4)
	game.free()
	completed = true
