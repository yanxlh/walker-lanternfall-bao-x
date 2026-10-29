extends SceneTree
## Windowed play-check captures for the particle effects (Assignment 6, step 2). Each scene is a fresh Session with
## seeded enemies, gems or a starting position; hits, movement, pause, cards and restart come from real physics and
## parsed keyboard input. Writes PNGs and states.json to --out. The game never loads this script.
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")

var game
var out_dir := ""
var scene_name := ""
var records := []
var hit_frames := []
var trail_log := []

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var at := args.find("--out")
	out_dir = args[at + 1] if at >= 0 and at + 1 < args.size() else ProjectSettings.globalize_path("res://../captures/play-checks/latest")
	DirAccess.make_dir_recursive_absolute(out_dir)
	AudioServer.set_bus_mute(0, true)
	call_deferred("_main")

func key(code: int, pressed: bool = true) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)

func frames(count: int) -> void:
	for n in count:
		await physics_frame
		await process_frame
		if is_instance_valid(game):
			trail_log.append([scene_name, Engine.get_physics_frames(), game.particles.trail.emitting, game.player.position.x, game.player.position.y])

func tap(code: int) -> void:
	key(code)
	await frames(1)
	key(code, false)
	await frames(1)

func shot(label: String, note: String = "") -> void:
	await RenderingServer.frame_post_draw
	var file := "%s-%s.png" % [scene_name, label]
	root.get_texture().get_image().save_png(out_dir.path_join(file))
	var p = game.particles
	records.append({
		"file": file, "scene": scene_name, "label": label, "note": note,
		"state": GS.NAMES[game.state.current],
		"trail_emitting": p.trail.emitting, "trail_speed_scale": p.trail.speed_scale,
		"particles_visible": p.is_visible_in_tree(),
		"hit_bursts": p.hit_bursts.size(), "level_bursts": p.level_bursts.size(),
		"hits_seen": p.hits_seen, "hits_spawned": p.hits_spawned,
		"player": [snappedf(game.player.position.x, 0.01), snappedf(game.player.position.y, 0.01)],
		"camera_zoom": snappedf(game.camera.zoom.x, 0.001),
		"physics_frame": Engine.get_physics_frames(),
	})
	print("shot ", file)

func new_session(label: String, setup: Callable = Callable()) -> void:
	for code in [KEY_D, KEY_A, KEY_W, KEY_S]:
		key(code, false)
	if is_instance_valid(game):
		game.free()
		await frames(1)
	scene_name = label
	hit_frames.clear()
	game = Session.new()
	game.test_no_spawn = true
	root.add_child(game)
	game.weapon_hit.connect(func(_at): hit_frames.append(Engine.get_physics_frames()))
	if setup.is_valid():
		game.run_started.connect(setup, CONNECT_ONE_SHOT)
	await frames(2)
	await tap(KEY_ENTER)

func pinned(kind: String, at: Vector2, hp: float = 9999.0):
	var e = game.spawn_enemy(kind, at)
	e.hp = hp
	e.speed = 0.0
	return e

func wait_hit(limit: int = 180) -> bool:
	var before := hit_frames.size()
	for n in limit:
		await frames(1)
		if hit_frames.size() > before:
			return true
	return false

func nearest_prop(kind: String) -> Vector2:
	var best := Vector2.INF
	for p in game.ground.props:
		if p["kind"] == kind and (best == Vector2.INF or p["pos"].length() < best.length()):
			best = p["pos"]
	return best

func open_spot(candidates: Array) -> Vector2:
	for c in candidates:
		if not game.ground.blocks(c, Tuning.PLAYER_RADIUS + 1.0):
			return c
	return candidates[0]

func _main() -> void:
	await scene_upgrade()
	await scene_hit_dark()
	await scene_hit_bright("hit-bright-cart", "cart", Vector2(0, 0))
	await scene_hit_bright("hit-bright-post", "post", Vector2(2, -10))
	await scene_trail_dark()
	await scene_trail_bright()
	await scene_blocked()
	await scene_restart_while_moving()
	await scene_pause_hidden()
	await scene_card_screen()
	await scene_death_and_restart()
	await scene_win()
	for code in [KEY_D, KEY_A, KEY_W, KEY_S]:
		key(code, false)
	var f := FileAccess.open(out_dir.path_join("states.json"), FileAccess.WRITE)
	f.store_string(JSON.stringify({"shots": records, "trail_per_frame": trail_log}, "  "))
	f.close()
	print("saved ", records.size(), " shots to ", out_dir)
	game.free()
	quit()

## Upgrade celebration at the card-screen portrait, from a real gem pickup.
func scene_upgrade() -> void:
	await new_session("upgrade")
	await frames(10)
	game.drop_gem(game.player.position, game.prog.xp_needed())
	var waited := 0
	while game.state.current != GS.LEVELUP and waited < 10:
		await frames(1)
		waited += 1
	await shot("f%02d" % waited, "frames after the gem drop; LEVELUP began")
	var elapsed := waited
	for target in [6, 12, 24, 40]:
		await frames(target - elapsed)
		elapsed = target
		await shot("f%02d" % target, "frames after the gem drop")
	await tap(KEY_1)
	await shot("after-card", "card 1 chosen")

## Weapon hits on plain floor inside the spawn plaza.
func scene_hit_dark() -> void:
	await new_session("hit-dark", func():
		game.prog.beam_pierce = 3
		pinned("wraith", Vector2(60, 0))
		pinned("moth", Vector2(48, 0), 2.0))
	await burst_sequence("plain floor")

## Weapon hits where the burst spreads over a bright prop; `offset` places the enemy on its brightest pixels.
func scene_hit_bright(label: String, kind: String, offset: Vector2) -> void:
	await new_session(label, func():
		var prop := nearest_prop(kind)
		var target := prop + offset
		game.player.position = open_spot([target + Vector2(-60, 0), target + Vector2(60, 0), target + Vector2(0, 60), target + Vector2(0, -60)])
		game.prog.beam_pierce = 3
		pinned("wraith", target))
	await burst_sequence(kind)

func burst_sequence(where: String) -> void:
	if not await wait_hit():
		await shot("no-hit", "no weapon hit within 180 frames: " + where)
		return
	await shot("hit+00", "first frame after the first hit, " + where)
	await frames(3)
	await shot("hit+03", where)
	await frames(5)
	await shot("hit+08", where)
	await frames(8)
	await shot("hit+16", where)
	await frames(14)
	await shot("hit+30", where)

## Trail across the plaza past pinned enemies and loose gems.
func scene_trail_dark() -> void:
	await new_session("trail-dark", func():
		game.prog.beam_pierce = 1
		pinned("wraith", Vector2(70, -30))
		pinned("moth", Vector2(110, 30))
		game.drop_gem(Vector2(95, -40), 1)
		game.drop_gem(Vector2(130, 42), 1))
	key(KEY_D)
	for at in [10, 25, 45, 70]:
		await frames(at - trail_t)
		trail_t = at
		await shot("move%02d" % at, "holding D")
	trail_t = 0
	key(KEY_D, false)
	for at in [1, 6, 12, 22]:
		await frames(at - trail_t)
		trail_t = at
		await shot("stop+%02d" % at, "released D")
	trail_t = 0

var trail_t := 0 # frames since the current hold or release began

## Trail through a lantern post's light pool, the brightest floor area in the level.
func scene_trail_bright() -> void:
	await new_session("trail-bright", func():
		var post := nearest_prop("post")
		game.player.position = open_spot([post + Vector2(-70, 34), post + Vector2(-70, 40)]))
	key(KEY_D)
	for at in [30, 45, 60, 75]:
		await frames(at - trail_t)
		trail_t = at
		await shot("move%02d" % at, "holding D through the light pool")
	trail_t = 0
	key(KEY_D, false)
	await frames(6)
	await shot("stop+06", "released D")

## Pushing straight into a stall: input held, no displacement, so no trail.
func scene_blocked() -> void:
	await new_session("blocked", func():
		var stall := nearest_prop("stall")
		game.player.position = Vector2(stall.x - 19.0 - Tuning.PLAYER_RADIUS - 0.5, stall.y))
	await frames(10)
	var start: Vector2 = game.player.position
	await shot("idle", "touching the stall's left edge")
	key(KEY_D)
	await frames(30)
	await shot("push30", "holding D into the stall for 30 frames; moved %.3f px" % game.player.position.distance_to(start))
	key(KEY_D, false)
	key(KEY_W)
	await frames(20)
	await shot("slide-up20", "holding W along the stall edge: real movement")
	key(KEY_W, false)

## Restart (R) while still holding D: the courier jumps to the plaza centre without a connecting line.
func scene_restart_while_moving() -> void:
	await new_session("restart")
	key(KEY_D)
	await frames(60)
	await shot("before-r", "holding D for 60 frames")
	await tap(KEY_R)
	await shot("r+01", "restart pressed, D still held")
	await frames(3)
	await shot("r+04", "D still held")
	await frames(10)
	await shot("r+14", "D still held")
	key(KEY_D, false)

## Pause during live hits and trail, then the hidden-presentation toggle.
func scene_pause_hidden() -> void:
	await new_session("pause", func():
		game.prog.beam_pierce = 3
		pinned("wraith", Vector2(70, 0)))
	key(KEY_D)
	await wait_hit()
	await frames(3)
	await shot("live", "moving with a live hit burst")
	await tap(KEY_P)
	await shot("paused+01", "P pressed")
	await frames(30)
	await shot("paused+31", "still paused; image should match paused+01")
	await tap(KEY_P)
	await frames(6)
	await shot("resumed+06", "P pressed again, D held")
	game.particles.hide()
	await frames(8)
	await shot("hidden+08", "presentation hidden while moving")
	game.particles.show()
	await frames(8)
	await shot("shown+08", "presentation shown again")
	key(KEY_D, false)

## Card screen arriving while a hit burst and trail are live.
func scene_card_screen() -> void:
	await new_session("card", func():
		game.prog.beam_pierce = 3
		pinned("wraith", Vector2(70, 0)))
	key(KEY_D)
	await wait_hit()
	await frames(2)
	game.drop_gem(game.player.position, game.prog.xp_needed())
	await frames(2)
	await shot("levelup+02", "card screen over a live hit and trail")
	await frames(30)
	await shot("levelup+32", "card screen held")
	key(KEY_D, false)
	await tap(KEY_2)
	await frames(4)
	await shot("chosen+04", "card 2 chosen")

## Death with live effects, then R from the LOST screen.
func scene_death_and_restart() -> void:
	await new_session("death", func():
		game.prog.beam_pierce = 3
		pinned("wraith", Vector2(70, 0)))
	key(KEY_D)
	await wait_hit()
	await frames(2)
	await shot("live", "moving with a live hit burst")
	game.player.hp = 1
	game.player.iframes = 0
	pinned("wraith", game.player.position + Vector2(4, 0))
	var waited := 0
	while game.state.current != GS.LOST and waited < 30:
		await frames(1)
		waited += 1
	await shot("lost+00", "first frame in LOST")
	key(KEY_D, false)
	await frames(30)
	await shot("lost+30", "LOST screen held")
	await tap(KEY_R)
	await frames(4)
	await shot("restart+04", "R pressed from LOST")

## Victory with live effects.
func scene_win() -> void:
	await new_session("win", func():
		game.prog.beam_pierce = 3
		pinned("wraith", Vector2(70, 0)))
	key(KEY_D)
	await wait_hit()
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 3
	var waited := 0
	while game.state.current != GS.WON and waited < 30:
		await frames(1)
		waited += 1
	await shot("won+00", "first frame in WON")
	key(KEY_D, false)
	await frames(30)
	await shot("won+30", "WON screen held")
