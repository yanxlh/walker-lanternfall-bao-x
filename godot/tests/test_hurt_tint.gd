extends "res://tests/harness.gd"
## Hurt tint: the shader contract from its source and uniform list, then the driver through the real game loop.
## Seeded fixtures only place enemies, a gem, hp = 1 and a late tick_count; hits come from real contact and
## state changes from parsed keyboard input. The test never calls the driver or writes hurt_amount, except
## on a second session's material to show the two materials are independent.
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
const HurtTint = preload("res://shaders/hurt_tint.gdshader")
const DriverScript = preload("res://effects/hurt_tint_presentation.gd")
const SAMPLER_PRIORITY := 100000

## Records one row per rendered frame after every other _process() has run.
class Sampler extends Node:
	const Tuning = preload("res://features/tuning.gd")
	var game
	var driver
	var rows: Array = []
	var frames := 0
	var game_time := 0.0

	func _process(delta: float) -> void:
		frames += 1
		game_time += delta
		if not is_instance_valid(game):
			return
		var p = game.player
		var contact := false
		for e in game.enemies:
			if is_instance_valid(e) and not e.dead and e.position.distance_to(p.position) < e.radius + Tuning.PLAYER_RADIUS:
				contact = true
		rows.append({
			"frame": frames, "t": game_time, "us": Time.get_ticks_usec(), "delta": delta,
			"amount": p.material.get_shader_parameter("hurt_amount") if p.material else null,
			"iframes": p.iframes, "state": game.state.current, "tick": game.tick_count, "hp": p.hp,
			"mod": p.modulate, "contact": contact, "tree_paused": get_tree().paused,
			"driver_active": driver.can_process() if is_instance_valid(driver) else false,
		})

var game
var sampler: Sampler
var driver
var hits: Array = []
var runs := 0
var fixture := Callable()
var restart_reads: Array = []

func key(code: int, pressed: bool = true) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)

func frames(count: int) -> void:
	for i in count:
		await process_frame

func tap(code: int) -> void:
	key(code)
	await frames(1)
	key(code, false)
	await frames(1)

func wait_until(cond: Callable, limit: int) -> bool:
	for i in limit:
		if cond.call():
			return true
		await process_frame
	return cond.call()

func wraith(at: Vector2):
	var e = game.spawn_enemy("wraith", at)
	e.hp = 1000.0
	return e

func amount() -> Variant:
	return game.player.material.get_shader_parameter("hurt_amount")

func expected_iframes(tick: int, hit_tick: int) -> int:
	return maxi(0, Tuning.IFRAME_TICKS - (tick - hit_tick))

## Every live-state row at or after hit_tick (and before until_tick) must show iframes counting down one per
## tick from 48 and hurt_amount == iframes / 48. Returns the mismatches.
func curve_mismatches(from_row: int, to_row: int, hit_tick: int, until_tick: int = 1 << 30) -> Array:
	var bad := []
	for i in range(from_row, to_row):
		var r: Dictionary = sampler.rows[i]
		if r.tick < hit_tick or r.tick >= until_tick or not (r.state in [GS.PLAYING, GS.PAUSED, GS.LEVELUP]):
			continue
		var want := expected_iframes(r.tick, hit_tick)
		if r.iframes != want or r.amount == null or not is_equal_approx(r.amount, clampf(float(want) / 48.0, 0.0, 1.0)):
			bad.append([r.tick, r.iframes, r.amount, want])
	return bad

func first_row_at_tick(from_row: int, tick: int) -> int:
	for i in range(from_row, sampler.rows.size()):
		if sampler.rows[i].tick >= tick:
			return i
	return -1

func held(from_row: int, to_row: int, before: Dictionary) -> Dictionary:
	var n := 0
	var same := true
	for i in range(from_row, to_row):
		var r: Dictionary = sampler.rows[i]
		n += 1
		same = same and r.tick == before.tick and r.iframes == before.iframes and is_equal_approx(r.amount, before.amount) and r.mod == before.mod
	return {"rows": n, "same": same and n > 0}

func snapshot() -> Dictionary:
	return {"tick": game.tick_count, "iframes": game.player.iframes, "amount": amount(), "mod": game.player.modulate}

func all_nodes(n: Node, out: Array) -> void:
	out.append(n)
	for c in n.get_children():
		all_nodes(c, out)

func run() -> void:
	suite = "hurt_tint"
	_shader_contract()
	game = Session.new()
	game.test_no_spawn = true
	root.add_child(game)
	for c in game.get_children():
		if c.get_script() == DriverScript:
			driver = c
	sampler = Sampler.new()
	sampler.game = game
	sampler.driver = driver
	sampler.process_priority = SAMPLER_PRIORITY
	sampler.process_mode = Node.PROCESS_MODE_ALWAYS
	root.add_child(sampler)
	game.player.damaged.connect(func(hp): hits.append({"tick": game.tick_count, "hp": hp, "run": runs}))
	game.run_started.connect(func():
		runs += 1
		restart_reads.append(amount())
		if fixture.is_valid():
			fixture.call())
	await frames(3)
	var period := 0.0
	var mat = game.player.material
	check("player-has-own-tint-material", mat is ShaderMaterial and mat.shader == HurtTint and driver != null)
	var nodes := []
	all_nodes(root, nodes)
	var top := -1000000000
	for n in nodes:
		if n != sampler:
			top = maxi(top, n.process_priority)
	check("sampler-runs-last", top < SAMPLER_PRIORITY and driver.process_priority < SAMPLER_PRIORITY, {"highest_other": top, "driver": driver.process_priority, "sampler": SAMPLER_PRIORITY})
	var menu_rows: Array = sampler.rows.filter(func(r): return r.state == GS.MENU)
	check("menu-zero", game.state.current == GS.MENU and typeof(amount()) == TYPE_FLOAT and amount() == 0.0 and menu_rows.all(func(r): return r.amount == 0.0), {"amount": amount(), "rows": menu_rows.size()})

	# Run A: one real contact, the wraith keeps touching during protection, then the courier walks away (W).
	fixture = func(): wraith(Vector2(20, 0))
	var mark := sampler.rows.size()
	await tap(KEY_ENTER)
	check("real-start-input", game.state.current == GS.PLAYING and not game.test_mode)
	await wait_until(func(): return hits.size() >= 1, 120)
	var h_a: int = hits[0].tick
	await wait_until(func(): return game.player.iframes <= 24, 240)
	key(KEY_W)
	await wait_until(func(): return game.tick_count >= h_a + 70, 600)
	key(KEY_W, false)
	var end_a := sampler.rows.size()
	var first := first_row_at_tick(mark, h_a)
	var r0: Dictionary = sampler.rows[first]
	# The frame period is read from the window's own frames; early menu frames can report a different delta.
	period = 0.0
	for i in range(first, end_a):
		period = maxf(period, sampler.rows[i].delta)
	var peak_want := float(expected_iframes(r0.tick, h_a)) / 48.0
	check("hit-starts-window", hits.size() == 1 and is_equal_approx(r0.amount, peak_want) and (period > 1.0 / 45.0 or r0.amount == 1.0),
		{"hit_tick": h_a, "first_row_tick": r0.tick, "first_amount": r0.amount, "period": period})
	var mism := curve_mismatches(mark, end_a, h_a)
	check("curve-follows-ticks", mism.is_empty(), {"mismatches": mism.slice(0, 5)})
	var zero_i := -1
	for i in range(first, end_a):
		if sampler.rows[i].amount == 0.0:
			zero_i = i
			break
	var zr: Dictionary = sampler.rows[zero_i] if zero_i > 0 else {}
	var dur: float = zr.t - r0.t if zero_i > 0 else -1.0
	check("zero-after-48-ticks", zero_i > 0 and zr.tick >= h_a + 48 and sampler.rows[zero_i - 1].tick < h_a + 48 and sampler.rows[zero_i - 1].amount > 0.0 and absf(dur - 0.8) <= period + 1e-6,
		{"zero_tick": zr.get("tick"), "ticks_after_hit": zr.get("tick", 0) - h_a, "frames": zr.get("frame", 0) - r0.frame, "game_seconds": dur, "allowed": period})
	var ignored := 0
	var non_increasing := true
	var hp_same := true
	for i in range(first, end_a):
		var r: Dictionary = sampler.rows[i]
		if r.contact and r.iframes > 0 and r.iframes < 48:
			ignored += 1
		if i > first:
			non_increasing = non_increasing and r.amount <= sampler.rows[i - 1].amount
		hp_same = hp_same and r.hp == hits[0].hp
	check("ignored-hit-no-retrigger", ignored > 0 and hits.size() == 1 and non_increasing and hp_same, {"contact_rows_in_window": ignored, "accepted_hits": hits.size(), "hp": game.player.hp})

	# Run B: PAUSED through the real P key mid-window, then restart with R mid-window.
	fixture = func(): wraith(Vector2(20, 0))
	var n_hits := hits.size()
	await tap(KEY_R)
	await wait_until(func(): return hits.size() > n_hits, 120)
	var h_b: int = hits[-1].tick
	mark = sampler.rows.size()
	await wait_until(func(): return game.player.iframes <= 30, 240)
	await tap(KEY_P)
	var before := snapshot()
	var p0 := sampler.rows.size()
	await frames(30)
	var hold := held(p0, sampler.rows.size(), before)
	check("paused-holds", game.state.current == GS.PAUSED and before.amount > 0.0 and hold.same, {"before": {"tick": before.tick, "iframes": before.iframes, "amount": before.amount}, "rows": hold.rows})
	await tap(KEY_P)
	await frames(6)
	mism = curve_mismatches(mark, sampler.rows.size(), h_b)
	check("paused-resumes", game.state.current == GS.PLAYING and game.player.iframes < before.iframes and mism.is_empty(), {"iframes_now": game.player.iframes, "mismatches": mism.slice(0, 5)})
	var pre_restart := snapshot()
	fixture = func(): wraith(Vector2(60, 0))
	restart_reads.clear()
	mark = sampler.rows.size()
	await tap(KEY_R)
	var new_run := -1
	for i in range(mark, sampler.rows.size()):
		if sampler.rows[i].tick < pre_restart.tick:
			new_run = i
			break
	var nr: Dictionary = sampler.rows[new_run] if new_run >= 0 else {}
	check("restart-writes-zero", pre_restart.amount > 0.0 and restart_reads == [0.0] and nr.get("amount") == 0.0 and nr.get("iframes") == 0,
		{"before": pre_restart.amount, "at_run_started": restart_reads, "first_frame": {"tick": nr.get("tick"), "amount": nr.get("amount")}})

	# Run C: LEVELUP through a real pickup mid-window, real 1 resumes; the wraith stays on the courier.
	n_hits = hits.size()
	await wait_until(func(): return hits.size() > n_hits, 600)
	var h_c: int = hits[-1].tick
	mark = sampler.rows.size()
	await wait_until(func(): return game.player.iframes <= 30, 240)
	game.drop_gem(game.player.position, game.prog.xp_needed())
	await wait_until(func(): return game.state.current == GS.LEVELUP, 20)
	before = snapshot()
	p0 = sampler.rows.size()
	await frames(30)
	hold = held(p0, sampler.rows.size(), before)
	check("levelup-holds", game.state.current == GS.LEVELUP and before.amount > 0.0 and hold.same, {"before": {"tick": before.tick, "iframes": before.iframes, "amount": before.amount}, "rows": hold.rows})
	await tap(KEY_1)
	await frames(6)
	n_hits = hits.size()
	mism = curve_mismatches(mark, sampler.rows.size(), h_c)
	check("levelup-resumes", game.state.current == GS.PLAYING and game.player.iframes < before.iframes and mism.is_empty(), {"iframes_now": game.player.iframes, "mismatches": mism.slice(0, 5)})
	# The next accepted hit can only come once protection has ended, and it starts a fresh 48-tick window.
	await wait_until(func(): return hits.size() > n_hits, 600)
	var h_d: int = hits[-1].tick
	mism = curve_mismatches(mark, sampler.rows.size(), h_c, h_d)
	check("next-hit-after-end-new-window", h_d - h_c >= 48 and mism.is_empty() and curve_mismatches(first_row_at_tick(mark, h_d), sampler.rows.size(), h_d).is_empty(),
		{"previous_hit": h_c, "next_hit": h_d, "gap_ticks": h_d - h_c})

	# Tree pause mid-window: the driver pauses with the tree and the value holds. The test pauses after this
	# frame's physics tick and before its _process, so the held value is the one the driver wrote last frame.
	mark = first_row_at_tick(mark, h_d)
	await wait_until(func(): return game.player.iframes <= 30, 240)
	var last_written = sampler.rows[-1].amount
	var p_pause := sampler.rows.size()
	paused = true
	before = snapshot()
	p0 = sampler.rows.size()
	await frames(30)
	hold = held(p0, sampler.rows.size(), before)
	var driver_stopped: bool = sampler.rows.slice(p0).all(func(r): return r.tree_paused and not r.driver_active)
	var p_end := sampler.rows.size()
	paused = false
	await frames(6)
	mism = curve_mismatches(mark, p_pause, h_d) + curve_mismatches(p_end, sampler.rows.size(), h_d)
	check("tree-pause-holds", before.amount > 0.0 and is_equal_approx(before.amount, last_written) and hold.same and driver_stopped,
		{"held_amount": before.amount, "iframes": before.iframes, "tick": before.tick, "lag_ticks": roundi(before.amount * 48.0) - before.iframes, "rows": hold.rows, "driver_stopped": driver_stopped})
	check("tree-pause-resumes", game.player.iframes < before.iframes and mism.is_empty(), {"iframes_now": game.player.iframes, "mismatches": mism.slice(0, 5)})

	# Engine.time_scale = 0.5: one full window measured from accepted hit to the next accepted hit.
	Engine.time_scale = 0.5
	mark = sampler.rows.size()
	n_hits = hits.size()
	await wait_until(func(): return hits.size() > n_hits, 2000)
	var h_e: int = hits[-1].tick
	await wait_until(func(): return hits.size() > n_hits + 1, 2000)
	await frames(1)
	Engine.time_scale = 1.0
	var h_f: int = hits[-1].tick
	var re := first_row_at_tick(mark, h_e)
	var rf := first_row_at_tick(re, h_f)
	var ts := {}
	if re >= 0 and rf >= 0:
		var a: Dictionary = sampler.rows[re]
		var b: Dictionary = sampler.rows[rf]
		ts = {"ticks": h_f - h_e, "frames": b.frame - a.frame, "scaled_game_seconds": b.t - a.t,
			"unscaled_frame_seconds": (b.frame - a.frame) * period, "real_seconds": (b.us - a.us) / 1e6}
	check("time-scale-window-ticks", re >= 0 and rf >= 0 and h_f - h_e == 48 and curve_mismatches(re, rf, h_e, h_f).is_empty(), ts)

	# Run D: a real lethal contact leaves iframes == 48 in LOST; the tint is forced to zero.
	fixture = func():
		game.player.hp = 1
		wraith(Vector2(20, 0))
	mark = sampler.rows.size()
	await tap(KEY_R)
	await wait_until(func(): return game.state.current == GS.LOST, 120)
	await frames(10)
	var lost_rows: Array = sampler.rows.slice(mark).filter(func(r): return r.state == GS.LOST)
	check("lethal-lost-zero", game.state.current == GS.LOST and game.player.iframes == 48 and amount() == 0.0 and lost_rows.size() > 0 and lost_rows.all(func(r): return r.amount == 0.0),
		{"state": GS.NAMES[game.state.current], "iframes": game.player.iframes, "amount": amount(), "lost_rows": lost_rows.size()})

	# Run E: a contact a few ticks before the end of the run; WON arrives mid-window.
	fixture = func():
		game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 10
		wraith(Vector2(20, 0))
	n_hits = hits.size()
	mark = sampler.rows.size()
	await tap(KEY_R)
	await wait_until(func(): return game.state.current == GS.WON, 120)
	await frames(10)
	var won_rows: Array = sampler.rows.slice(mark).filter(func(r): return r.state == GS.WON)
	check("won-zero", game.state.current == GS.WON and hits.size() > n_hits and game.player.iframes > 0 and amount() == 0.0 and won_rows.size() > 0 and won_rows.all(func(r): return r.amount == 0.0),
		{"state": GS.NAMES[game.state.current], "iframes": game.player.iframes, "amount": amount(), "won_rows": won_rows.size()})

	var spaced := true
	for i in range(1, hits.size()):
		if hits[i].run == hits[i - 1].run:
			spaced = spaced and hits[i].tick - hits[i - 1].tick >= 48
	check("accepted-hits-spaced-48", spaced, {"hits": hits.map(func(h): return [h.run, h.tick])})

	# A second session gets its own material; the Shader resource is shared.
	var other = Session.new()
	other.test_no_spawn = true
	root.add_child(other)
	await frames(1)
	var m1 = game.player.material
	var m2 = other.player.material
	var m1_before = m1.get_shader_parameter("hurt_amount")
	check("distinct-materials", m1 is ShaderMaterial and m2 is ShaderMaterial and m1 != m2 and m1.shader == m2.shader, {"m1": m1.get_instance_id(), "m2": m2.get_instance_id()})
	m2.set_shader_parameter("hurt_amount", 0.75)
	check("materials-independent", m2.get_shader_parameter("hurt_amount") == 0.75 and m1.get_shader_parameter("hurt_amount") == m1_before, {"m1": m1.get_shader_parameter("hurt_amount"), "m2": m2.get_shader_parameter("hurt_amount")})
	other.free()
	game.free()
	sampler.free()
	completed = true

func _shader_contract() -> void:
	var uniforms: Array = HurtTint.get_shader_uniform_list()
	var by_name := {}
	for u in uniforms:
		by_name[u.name] = u
	var names := by_name.keys()
	names.sort()
	var range_ok := false
	if by_name.has("hurt_amount"):
		var parts: PackedStringArray = str(by_name.hurt_amount.hint_string).split(",")
		range_ok = by_name.hurt_amount.hint == PROPERTY_HINT_RANGE and parts.size() >= 2 and float(parts[0]) == 0.0 and float(parts[1]) == 1.0
	check("shader-parses", uniforms.size() > 0, {"uniforms": uniforms.size()})
	check("uniform-names-types", names == ["hurt_amount", "hurt_color"] and by_name.hurt_amount.type == TYPE_FLOAT and by_name.hurt_color.type == TYPE_COLOR and range_ok,
		{"uniforms": uniforms.map(func(u): return [u.name, u.type, u.hint, u.hint_string])})
	check("no-sampler-uniforms", uniforms.all(func(u): return u.type != TYPE_OBJECT))
	var code: String = HurtTint.code
	var patterns := {
		"type": "shader_type\\s+canvas_item\\s*;",
		"mode": "render_mode\\s+unshaded\\s*;",
		"amount_default": "uniform\\s+float\\s+hurt_amount\\s*:\\s*hint_range\\(\\s*0\\.0\\s*,\\s*1\\.0\\s*\\)\\s*=\\s*0\\.0\\s*;",
		"color_default": "uniform\\s+vec4\\s+hurt_color\\s*:\\s*source_color\\s*=\\s*vec4\\(\\s*1\\.0\\s*,\\s*1\\.0\\s*,\\s*0\\.0\\s*,\\s*1\\.0\\s*\\)\\s*;",
	}
	var found := {}
	for k in patterns:
		var rx := RegEx.new()
		rx.compile(patterns[k])
		found[k] = rx.search(code) != null
	found["mix_line"] = code.contains("COLOR.rgb = mix(COLOR.rgb, hurt_color.rgb, hurt_amount);")
	check("defaults-from-source", found.values().all(func(v): return v), found)
	check("no-time-no-resample", not code.contains("TIME") and not code.contains("texture("))
	var rx := RegEx.new()
	rx.compile("set_shader_parameter\\(\"(\\w+)\"")
	var written := rx.search_all(FileAccess.get_file_as_string("res://effects/hurt_tint_presentation.gd")).map(func(m): return m.get_string(1))
	check("driver-uses-declared-names", written.size() > 0 and written.all(func(n): return by_name.has(n)), {"written": written})
