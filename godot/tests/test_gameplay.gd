extends "res://tests/harness.gd"
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")
var game

func fresh(seed_value: int = 1, no_spawn: bool = true) -> void:
	if is_instance_valid(game):
		game.free()
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = no_spawn
	root.add_child(game)
	game.start_run(seed_value)

func run() -> void:
	suite = "gameplay"
	await fresh()
	check("run-starts-playing", game.state.current == GS.PLAYING and game.tick_count == 0 and game.player.hp == Tuning.PLAYER_MAX_HP)
	var poses: Array = game.player.POSES
	var sheet_ok: bool = game.player.sheet == null or game.player.sheet.get_width() == 32 * poses.size()
	var origin: Vector2 = game.player.SPRITE_ORIGIN
	var torso_ok := true
	var torso := {}
	if game.player.sheet:
		var img: Image = game.player.sheet.get_image()
		var navy := Color("#2E3A59")
		for pose in ["idle", "walk_contact", "walk_passing", "cast", "levelup", "sunflare", "victory"]:
			var i: int = poses.find(pose)
			var sum := Vector2.ZERO
			var n := 0
			for y in 32:
				for x in 32:
					var c := img.get_pixel(i * 32 + x, y)
					if c.a > 0.5 and c.is_equal_approx(navy):
						sum += Vector2(x, y)
						n += 1
			var centre := sum / maxi(n, 1)
			torso[pose] = [snappedf(centre.x, 0.1), snappedf(centre.y, 0.1)]
			torso_ok = torso_ok and n > 0 and absf(centre.x - origin.x) <= 1.5 and absf(centre.y - origin.y) <= 1.5
	check("hurtbox-centred-on-torso", game.player.sheet == null or torso_ok, {"sprite_origin": [origin.x, origin.y], "coat_centres": torso})
	check("pose-table-matches-sheet", poses.size() == 10 and not ("turn_side" in poses) and not ("turn_back" in poses) and sheet_ok, {"poses": poses})
	game.test_axis = Vector2.RIGHT
	game.step_ticks(60)
	check("move-speed", absf(game.player.position.x - 90.0) < 0.5, {"x": game.player.position.x})
	check("walk-pose", game.player.pose in ["walk_contact", "walk_passing", "cast"], {"pose": game.player.pose})
	await fresh()
	game.test_axis = Vector2(1, 1)
	game.step_ticks(60)
	check("diagonal-normalized", absf(game.player.position.length() - 90.0) < 0.5, {"dist": game.player.position.length()})
	game.test_axis = Vector2(-1, 0)
	game.step_ticks(1)
	check("facing-left", game.player.facing == -1)
	game.test_axis = Vector2(0.08, 1)
	game.step_ticks(5)
	check("facing-deadzone", game.player.facing == -1)
	game.test_axis = Vector2.ZERO
	game.step_ticks(20)
	check("idle-pose", game.player.pose in ["idle", "cast"], {"pose": game.player.pose})
	game.test_axis = Vector2.LEFT
	game.step_ticks(1200)
	check("arena-clamp", game.player.position.x >= Tuning.ARENA.position.x, {"x": game.player.position.x})

	await fresh()
	game.spawn_enemy("moth", Vector2(80, 0))
	var kills := [0]
	game.enemy_killed.connect(func(_p): kills[0] += 1)
	game.step_ticks(2)
	check("cast-pose-on-fire", game.player.pose == "cast", {"pose": game.player.pose})
	game.step_ticks(38)
	check("beam-kills-moth", kills[0] == 1 and game.gems.size() == 1 and game.enemies.is_empty(), {"kills": kills[0], "gems": game.gems.size()})
	var picked := [0]
	game.gem_collected.connect(func(_v): picked[0] += 1)
	game.test_axis = Vector2.RIGHT
	game.step_ticks(60)
	check("gem-flies-and-collects", picked[0] == 1 and game.prog.xp == 1 and game.gems.is_empty(), {"xp": game.prog.xp})

	await fresh()
	var above = game.spawn_enemy("moth", Vector2(0, -90))
	var decoy = game.spawn_enemy("moth", Vector2(300, 0))
	game.test_axis = Vector2.ZERO
	game.step_ticks(20)
	check("beam-aims-nearest", above.dead and not decoy.dead, {"nearest_dead": above.dead, "far_dead": decoy.dead})

	await fresh()
	game.prog.add_xp(3)
	game.tick()
	check("levelup-opens", game.state.current == GS.LEVELUP and game.offered.size() == 3 and game.player.pose == "levelup", {"offered": game.offered})
	var frozen: int = game.tick_count
	game.step_ticks(30)
	check("levelup-freezes-sim", game.tick_count == frozen)
	check("choose-card", game.choose_card(0) and game.state.current == GS.PLAYING and game.prog.pending_levelups == 0)
	check("choose-card-rejected-when-playing", not game.choose_card(0))

	await fresh()
	game.prog.add_xp(3 + 5 + 7)
	var opens := 0
	for i in 10:
		game.tick()
		if game.state.current == GS.LEVELUP:
			opens += 1
			game.choose_card(0)
	check("levelup-queue", opens == 3 and game.prog.pending_levelups == 0, {"opens": opens})

	await fresh()
	game.toggle_pause()
	game.prog.add_xp(3)
	game.step_ticks(10)
	check("levelup-while-paused", game.state.current == GS.PAUSED)
	game.toggle_pause()
	game.tick()
	check("levelup-after-unpause", game.state.current == GS.LEVELUP)

	await fresh()
	var hurts: Array = []
	game.player_hurt.connect(func(_hp): hurts.append(game.tick_count))
	var w = game.spawn_enemy("wraith", Vector2.ZERO)
	w.hp = 9999
	for i in 150:
		w.position = game.player.position
		game.tick()
	var spaced := true
	for i in range(1, hurts.size()):
		spaced = spaced and hurts[i] - hurts[i - 1] >= Tuning.IFRAME_TICKS
	check("hurt-iframes", hurts.size() == 4 and spaced, {"hurt_ticks": hurts})
	check("hurt-knockback-and-hp", game.player.hp == Tuning.PLAYER_MAX_HP - 8)

	await fresh()
	game.player.hp = 1
	var w2 = game.spawn_enemy("wraith", game.player.position)
	w2.hp = 9999
	game.tick()
	check("death-lost", game.state.current == GS.LOST and game.player.pose == "defeat")
	var t_end: int = game.tick_count
	game.step_ticks(10)
	check("lost-freezes-sim", game.tick_count == t_end)

	await fresh()
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.tick()
	check("won-at-3min", game.state.current == GS.WON and game.player.pose == "victory")

	await fresh()
	var terminal := [0]
	game.state.changed.connect(func(_f, t):
		if t == GS.WON or t == GS.LOST:
			terminal[0] += 1)
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.player.hp = 1
	var w3 = game.spawn_enemy("wraith", game.player.position)
	w3.hp = 9999
	game.tick()
	check("death-and-timer-same-tick", terminal[0] == 1 and game.state.current == GS.LOST)

	await fresh()
	var evo := [0]
	game.evolved.connect(func(): evo[0] += 1)
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(3)
	game.tick()
	check("sunflare-offered", game.offered[0] == "sunflare", {"offered": game.offered})
	game.choose_card(0)
	var ring = game.spawn_enemy("moth", Vector2(200, 0))
	game.step_ticks(Tuning.SUNFLARE_FIRST_DELAY + 1)
	check("sunflare-evolves-once", evo[0] == 1 and game.orbit_positions().is_empty() and game.shots.is_empty() and game.player.empowered)
	check("sunflare-burst-kills", game.enemies.is_empty() and game.banner_ticks > 0)

	await fresh(5, false)
	game.player.hp = 1
	game.step_ticks(20000)
	var lost_first: bool = game.state.is_terminal()
	game.start_run(5)
	check("restart-resets", lost_first and game.state.current == GS.PLAYING and game.tick_count == 0 and game.enemies.is_empty() and game.gems.is_empty() and game.player.hp == Tuning.PLAYER_MAX_HP and game.prog.level == 1)

	Art.disabled = true
	await fresh(9, false)
	game.test_axis = Vector2(1, 0.3)
	for i in 600:
		if game.state.current == GS.LEVELUP:
			game.choose_card(0)
		game.tick()
	check("missing-art-no-crash", game.tick_count > 0 and game.player.sheet == null)
	Art.disabled = false

	await fresh(3, false)
	var chosen: Array = []
	for t in Tuning.RUN_SECONDS * Tuning.TICK_HZ + 10:
		if game.state.is_terminal():
			break
		if game.state.current == GS.LEVELUP:
			chosen.append(game.offered[0])
			game.choose_card(0)
		var a := float(t) / 90.0
		game.test_axis = Vector2(cos(a), sin(a))
		game.tick()
	check("long-run-smoke", game.state.is_terminal(), {"state": GS.NAMES[game.state.current], "seconds": game.tick_count / 60, "kills": game.kills, "level": game.prog.level, "cards": chosen})
	await fresh()
	check("hud-shows-timer-hp-level", _has(game.hud.lines(), "0:00") and _has(game.hud.lines(), "HP 10/10") and _has(game.hud.lines(), "Lv 1"), {"lines": game.hud.lines()})
	game.prog.add_xp(3)
	game.tick()
	check("hud-shows-cards", _has(game.hud.lines(), "[1]") and _has(game.hud.lines(), "[3]"), {"lines": game.hud.lines()})
	game.choose_card(0)
	game.toggle_pause()
	check("hud-shows-paused", _has(game.hud.lines(), "PAUSED"))
	game.toggle_pause()
	game.player.hp = 1
	var wx = game.spawn_enemy("wraith", game.player.position)
	wx.hp = 9999
	game.tick()
	check("hud-shows-lost-and-retry", _has(game.hud.lines(), "The lamp went out") and _has(game.hud.lines(), "R / Y to retry"))
	game.audio.toggle_bus("Music")
	check("hud-shows-mute-state", _has(game.hud.lines(), "MUSIC off"))
	game.audio.toggle_bus("Music")
	await fresh()
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(3)
	game.tick()
	game.choose_card(0)
	game.player.hp = 1
	var wb = game.spawn_enemy("wraith", game.player.position)
	wb.hp = 9999
	game.step_ticks(40)
	check("end-panel-hides-banner-and-ring", game.state.current == GS.LOST and not _has(game.hud.lines(), "SUNFLARE LIGHTHOUSE") and not game.fx.ring_visible(), {"lines": game.hud.lines()})
	# storyboard camera moves (visual only; the simulation never reads the camera)
	await fresh()
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(3)
	game.tick()
	game.choose_card(game.offered.find("sunflare"))
	game.step_ticks(game.camera.SUNFLARE_OUT_TICKS)
	var zoomed_out: float = game.camera.zoom.x
	game.step_ticks(game.camera.SUNFLARE_BACK_TICKS + 5)
	check("camera-sunflare-zoom-out", zoomed_out < 0.8 and is_equal_approx(game.camera.zoom.x, 1.0), {"at_peak": zoomed_out, "after": game.camera.zoom.x})

	await fresh()
	var wt = game.spawn_enemy("wraith", game.player.position)
	wt.hp = 9999
	game.tick()
	var tilt: float = game.camera.rotation
	game.enemies.erase(wt)
	wt.queue_free()
	game.step_ticks(Tuning.HURT_POSE_TICKS + 2)
	check("camera-hurt-tilt", absf(tilt) > 0.02 and is_zero_approx(game.camera.rotation), {"tilt": tilt, "after": game.camera.rotation})

	# the title push-in and the fog lifting run on real time, because the simulation is stopped then
	game.free()
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = true
	root.add_child(game)
	var z0: float = game.camera.zoom.x
	await create_timer(0.6).timeout
	check("camera-menu-push-in", game.state.current == GS.MENU and z0 < game.camera.zoom.x and game.camera.zoom.x <= 1.0, {"start": z0, "after": game.camera.zoom.x})
	game.start_run(1)
	check("camera-reset-on-start", is_equal_approx(game.camera.zoom.x, 1.0) and is_zero_approx(game.camera.rotation))
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.tick()
	await create_timer(0.6).timeout
	check("fog-lifts-on-win", game.state.current == GS.WON and game.camera.fog_lift() > 0.1 and game.camera.zoom.x < 1.0, {"lift": game.camera.fog_lift(), "zoom": game.camera.zoom.x})
	completed = true

func _has(lines: PackedStringArray, needle: String) -> bool:
	for l in lines:
		if needle in l:
			return true
	return false
