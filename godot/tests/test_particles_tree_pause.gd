extends "res://tests/harness.gd"
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")

func frames(count: int) -> void:
	for i in count:
		await physics_frame
		await process_frame

func key(code: int, down: bool) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = down
	Input.parse_input_event(event)

func run() -> void:
	suite = "particles_tree_pause"
	var game = Session.new()
	game.test_no_spawn = true
	root.add_child(game)
	await frames(2)
	key(KEY_ENTER, true)
	await frames(1)
	key(KEY_ENTER, false)
	key(KEY_D, true)
	await frames(5)
	check("playing-before-tree-pause", game.state.current == GS.PLAYING)
	check("moving-trail-before-tree-pause", game.particles.trail.emitting)
	var before: Vector2 = game.player.position
	var emitting_before: bool = game.particles.trail.emitting
	paused = true
	await frames(5)
	check("tree-pause-blocks-player-processing", not game.player.can_process())
	check("tree-pause-blocks-presentation-processing", not game.particles.can_process())
	check("tree-pause-blocks-trail-processing", not game.particles.trail.can_process())
	check("tree-pause-freezes-player-position", game.player.position.is_equal_approx(before))
	check("tree-pause-retains-emission-state", game.particles.trail.emitting == emitting_before)
	check("tree-pause-does-not-change-game-state", game.state.current == GS.PLAYING)
	paused = false
	await frames(5)
	check("tree-resume-restores-movement", not game.player.position.is_equal_approx(before))
	check("tree-resume-restores-trail-processing", game.particles.trail.can_process() and game.particles.trail.emitting)
	key(KEY_D, false)
	await frames(2)
	check("idle-after-tree-resume-stops-emission", not game.particles.trail.emitting)
	game.free()
	completed = true
