extends "res://tests/harness.gd"
## Assignment 7 read-back of the courier's clips against CHANGE-BRIEF.md. It loads the saved scene and library
## (never the builder) and checks: every track resolves; key frames, times and values; loop modes; discrete frame
## tracks keying only cells that exist; the walk seam; the dash's phase-boundary keys and spacing; the rig's
## regions, pivots and rest pose against the sheet; the clock mode; and that no Godot 3 name slipped in.
## The expected values below are copied from the brief, not imported from the builder.
const SCENE := "res://features/player/courier_visual.tscn"
const LIBRARY := "res://animations/courier_clips.tres"
const SHEET := "res://assets/art/pc_sheet.png"
const FPS := 60.0
const ORIGIN := Vector2(16, 23)

const SPRITE_CLIPS := {
	"turn_front": {"frames": [[0, 0]], "length": 1, "loop": Animation.LOOP_NONE},
	"idle": {"frames": [[1, 0]], "length": 1, "loop": Animation.LOOP_NONE},
	"walk": {"frames": [[2, 0], [3, 8]], "length": 16, "loop": Animation.LOOP_LINEAR},
	"cast": {"frames": [[4, 0]], "length": 1, "loop": Animation.LOOP_NONE},
	"hurt": {"frames": [[5, 0]], "length": 1, "loop": Animation.LOOP_NONE},
	"levelup": {"frames": [[6, 0]], "length": 1, "loop": Animation.LOOP_NONE},
	"sunflare": {"frames": [[7, 0]], "length": 1, "loop": Animation.LOOP_NONE},
	"defeat": {"frames": [[8, 0]], "length": 1, "loop": Animation.LOOP_NONE},
	"victory": {"frames": [[9, 0]], "length": 1, "loop": Animation.LOOP_NONE},
}
const PHASES := {"startup": [0, 4], "active": [4, 14], "recovery": [14, 20]}
const TRANSITIONS := {"startup": 2.0, "active": 1.0, "recovery": 0.5}
const DASH_KEYS := {
	"Rig:position": [[0, Vector2(0, 0)], [3, Vector2(0, 1)], [4, Vector2(0, -1)], [14, Vector2(0, 0)], [16, Vector2(0, 1)], [20, Vector2(0, 0)]],
	"Rig/Hips:rotation": [[0, 0.0], [3, -0.15], [4, 0.35], [14, 0.30], [16, -0.08], [20, 0.0]],
	"Rig/Hips/Chest/Neck:rotation": [[0, 0.0], [3, 0.10], [4, -0.30], [10, -0.20], [14, -0.25], [16, 0.15], [18, -0.05], [20, 0.0]],
}
const RIG_CELL := 2
const PART_REGIONS := {"Head": Rect2(17, 8, 8, 12), "Arm": Rect2(12, 13, 5, 7), "Coat": Rect2(11, 20, 14, 8), "Legs": Rect2(11, 28, 14, 4)}
const PIVOTS := {"Rig/Hips": Vector2(16, 27), "Rig/Hips/Chest": Vector2(16, 20), "Rig/Hips/Chest/Neck": Vector2(18, 19)}

## Every track in every clip resolves to a real node, and to a real property, bone or blend shape where the track
## names one (the assignment's check, unchanged apart from the indentation).
static func track_problems(player: AnimationPlayer) -> Array[String]:
	var problems: Array[String] = []
	var root := player.get_node(player.root_node)
	for clip_name in player.get_animation_list():
		var clip := player.get_animation(clip_name)
		for t in clip.get_track_count():
			var path := clip.track_get_path(t)
			var node := root.get_node_or_null(NodePath(path.get_concatenated_names()))
			if node == null:
				problems.append("%s track %d: no node at %s" % [clip_name, t, path])
				continue
			if path.get_subname_count() == 0:
				continue
			var sub := path.get_subname(0)
			match clip.track_get_type(t):
				Animation.TYPE_POSITION_3D, Animation.TYPE_ROTATION_3D, Animation.TYPE_SCALE_3D:
					var skeleton := node as Skeleton3D
					if skeleton == null or skeleton.find_bone(sub) == -1:
						problems.append("%s track %d: no bone %s on %s" % [clip_name, t, sub, node.name])
				Animation.TYPE_BLEND_SHAPE:
					var mesh := node as MeshInstance3D
					if mesh == null or mesh.find_blend_shape_by_name(sub) == -1:
						problems.append("%s track %d: no blend shape %s on %s" % [clip_name, t, sub, node.name])
				_:
					if not (sub in node):
						problems.append("%s track %d: %s has no property %s" % [clip_name, t, node.name, sub])
	return problems

## Key times are stored as 32-bit floats: a key is "at frame f" when it is within 1e-6 s of f / 60. That is far
## tighter than the assignment's half-frame tolerance (0.5 / 60 s), and still above the float32 error (about 7e-9 s).
func at_frame(time: float, f: int) -> bool:
	return absf(time - f / FPS) < 1e-6

func key_frames(clip: Animation, t: int) -> Array:
	var out := []
	for k in clip.track_get_key_count(t):
		out.append(roundi(clip.track_get_key_time(t, k) * FPS))
	return out

func phase_of(f: int) -> String:
	for p in PHASES:
		if f >= PHASES[p][0] and f < PHASES[p][1]:
			return p
	return "recovery"

func run() -> void:
	suite = "courier_clips"
	var packed: PackedScene = load(SCENE)
	check("scene-loads", packed != null, {"scene": SCENE})
	var visual: Node2D = packed.instantiate()
	root.add_child(visual)
	var player: AnimationPlayer = visual.get_node("AnimationPlayer")
	var body: Sprite2D = visual.get_node("Body")
	var library := player.get_animation_library("")
	check("library-is-the-committed-tres", library != null and library.resource_path == LIBRARY, {"path": library.resource_path if library else ""})

	var problems := track_problems(player)
	check("every-track-resolves", problems.is_empty(), {"problems": problems})
	var names := Array(player.get_animation_list())
	names.sort()
	var want := SPRITE_CLIPS.keys() + ["dash"]
	want.sort()
	check("clip-names", names == want, {"clips": names})

	# The clock: nothing advances the player but the courier's own tick.
	check("callback-mode-manual", player.callback_mode_process == AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL, {"callback_mode_process": player.callback_mode_process})
	check("no-autoplay", player.autoplay == "" and is_equal_approx(player.speed_scale, 1.0), {"autoplay": player.autoplay, "speed_scale": player.speed_scale})

	# The sheet and its slicing.
	var sheet: Texture2D = body.texture
	var cells: int = body.hframes * body.vframes
	check("body-slices-the-sheet", sheet != null and sheet.resource_path == SHEET and body.hframes == 10 and body.vframes == 1
		and sheet.get_width() / body.hframes == 32 and sheet.get_height() / body.vframes == 32,
		{"texture": sheet.resource_path if sheet else "", "size": [sheet.get_width(), sheet.get_height()] if sheet else [], "hframes": body.hframes, "vframes": body.vframes})
	check("body-registration", not body.centered and body.offset == -ORIGIN and body.position == Vector2.ZERO, {"centered": body.centered, "offset": [body.offset.x, body.offset.y]})

	# Sprite clips: frames, times, loop, discrete updates, frames inside the sheet, both visibility keys.
	for clip_name in SPRITE_CLIPS:
		var spec: Dictionary = SPRITE_CLIPS[clip_name]
		var clip := player.get_animation(clip_name)
		var t := clip.find_track(NodePath("Body:frame"), Animation.TYPE_VALUE)
		var got := []
		var inside := true
		var times_ok := true
		for k in clip.track_get_key_count(t):
			var value: int = clip.track_get_key_value(t, k)
			got.append([value, roundi(clip.track_get_key_time(t, k) * FPS)])
			inside = inside and value >= 0 and value < cells
			times_ok = times_ok and at_frame(clip.track_get_key_time(t, k), got[-1][1])
		check(clip_name + "-frame-keys", t >= 0 and got == spec["frames"] and times_ok, {"keys": got, "brief": spec["frames"]})
		check(clip_name + "-frames-inside-sheet", inside, {"cells": cells, "keys": got})
		check(clip_name + "-discrete", t >= 0 and clip.value_track_get_update_mode(t) == Animation.UPDATE_DISCRETE, {"update_mode": clip.value_track_get_update_mode(t)})
		check(clip_name + "-length-and-loop", at_frame(clip.length, spec["length"]) and clip.loop_mode == spec["loop"], {"length_frames": clip.length * FPS, "loop_mode": clip.loop_mode})
		# step is one frame period at the brief's 60 per second (the default is 1/30), so editor snapping agrees.
		check(clip_name + "-step", is_equal_approx(clip.step, 1.0 / FPS), {"step": clip.step})
		_check_visibility(clip_name, clip, true)

	# The walk seam, frame-track rule: no duplicate across the wrap; last key to length equals the key interval.
	var walk := player.get_animation("walk")
	var wt := walk.find_track(NodePath("Body:frame"), Animation.TYPE_VALUE)
	var n := walk.track_get_key_count(wt)
	var interval := walk.track_get_key_time(wt, 1) - walk.track_get_key_time(wt, 0)
	var tail := walk.length - walk.track_get_key_time(wt, n - 1)
	check("walk-seam", walk.track_get_key_value(wt, 0) != walk.track_get_key_value(wt, n - 1) and absf(tail - interval) < 1e-6,
		{"first": walk.track_get_key_value(wt, 0), "last": walk.track_get_key_value(wt, n - 1), "interval_frames": interval * FPS, "tail_frames": tail * FPS})

	# Played back through the player in manual mode: the cell at every tick of two cycles.
	player.play("walk")
	var shown := []
	for tick in 32:
		player.seek((tick % 16) / FPS, true)
		shown.append(body.frame)
	var expect := []
	for tick in 32:
		expect.append(2 if (tick % 16) < 8 else 3)
	check("walk-played-back-cells", shown == expect, {"shown": shown})

	# The dash: length, loop, keys at every phase boundary, values, spacing per phase.
	var dash := player.get_animation("dash")
	check("dash-length-and-loop", at_frame(dash.length, 20) and dash.loop_mode == Animation.LOOP_NONE, {"length_frames": dash.length * FPS, "loop_mode": dash.loop_mode})
	check("dash-step", is_equal_approx(dash.step, 1.0 / FPS), {"step": dash.step})
	_check_visibility("dash", dash, false)
	for path in DASH_KEYS:
		var t := dash.find_track(NodePath(path), Animation.TYPE_VALUE)
		var frames := key_frames(dash, t) if t >= 0 else []
		var values_ok: bool = t >= 0 and frames.size() == DASH_KEYS[path].size()
		var transitions_ok: bool = values_ok
		var times_ok: bool = values_ok
		if values_ok:
			for k in frames.size():
				var brief_key: Array = DASH_KEYS[path][k]
				var v = dash.track_get_key_value(t, k)
				values_ok = values_ok and frames[k] == brief_key[0] and (v.is_equal_approx(brief_key[1]) if v is Vector2 else is_equal_approx(v, brief_key[1]))
				times_ok = times_ok and at_frame(dash.track_get_key_time(t, k), brief_key[0])
				transitions_ok = transitions_ok and is_equal_approx(dash.track_get_key_transition(t, k), TRANSITIONS[phase_of(frames[k])])
		var boundaries := true
		for f in [0, 4, 14, 20]:
			boundaries = boundaries and f in frames
		check("dash-keys " + path, values_ok and times_ok, {"frames": frames})
		check("dash-phase-boundaries " + path, boundaries, {"frames": frames, "boundaries": [0, 4, 14, 20]})
		check("dash-spacing " + path, transitions_ok and dash.value_track_get_update_mode(t) == Animation.UPDATE_CONTINUOUS, {"transitions": Array(range(dash.track_get_key_count(t)).map(func(k): return dash.track_get_key_transition(t, k)))})

	# The rig against the sheet: regions, no overlap, every opaque pixel of the cell covered once.
	var img: Image = sheet.get_image()
	var uncovered := 0
	var doubled := 0
	for y in 32:
		for x in 32:
			if img.get_pixel(RIG_CELL * 32 + x, y).a <= 0.5:
				continue
			var hits := 0
			for part in PART_REGIONS:
				if PART_REGIONS[part].has_point(Vector2(x, y) + Vector2(0.5, 0.5)):
					hits += 1
			uncovered += 1 if hits == 0 else 0
			doubled += 1 if hits > 1 else 0
	check("rig-regions-cover-the-cell", uncovered == 0 and doubled == 0, {"uncovered_pixels": uncovered, "doubled_pixels": doubled})
	var regions_ok := true
	var rest_ok := true
	var rest := {}
	player.play("dash")
	player.seek(0.0, true)
	for part in PART_REGIONS:
		var s: Sprite2D = visual.find_child(part, true, false)
		var region: Rect2 = PART_REGIONS[part]
		regions_ok = regions_ok and s != null and s.region_enabled and s.texture == sheet and not s.centered and s.region_rect == Rect2(region.position + Vector2(RIG_CELL * 32, 0), region.size)
		# At dash time 0 every rotation is 0, so each part's top-left lands where it sits in the cell.
		var at: Vector2 = (visual.get_global_transform().affine_inverse() * s.get_global_transform()).origin
		rest[part] = [at.x, at.y]
		rest_ok = rest_ok and at.is_equal_approx(region.position - ORIGIN)
	check("rig-part-regions", regions_ok)
	check("rig-rest-pose-matches-cell", rest_ok, {"rest": rest})
	var pivots := {}
	var pivots_ok := true
	for path in PIVOTS:
		var pivot: Node2D = visual.get_node(path)
		var at: Vector2 = (visual.get_global_transform().affine_inverse() * pivot.get_global_transform()).origin
		pivots[path] = [at.x, at.y]
		pivots_ok = pivots_ok and at.is_equal_approx(PIVOTS[path] - ORIGIN)
	check("rig-pivots", pivots_ok, {"pivots": pivots})

	# Played back: the pose at each phase boundary.
	var hips: Node2D = visual.get_node("Rig/Hips")
	var neck: Node2D = visual.get_node("Rig/Hips/Chest/Neck")
	var rig: Node2D = visual.get_node("Rig")
	var sampled := {}
	var sample_ok := true
	for f in [0, 4, 14, 20]:
		player.seek(f / FPS, true)
		sampled[f] = [snappedf(hips.rotation, 0.0001), snappedf(neck.rotation, 0.0001), rig.position.y, rig.visible, body.visible]
		var hk = DASH_KEYS["Rig/Hips:rotation"].filter(func(k): return k[0] == f)[0][1]
		sample_ok = sample_ok and is_equal_approx(hips.rotation, hk) and rig.visible and not body.visible
	check("dash-played-back-at-boundaries", sample_ok, {"sampled": sampled})

	# The tint path: every canvas item of the visual uses the courier's material.
	var own := []
	for c in visual.find_children("*", "CanvasItem", true, false) + [visual]:
		if not c.use_parent_material or c.material != null:
			own.append(str(visual.get_path_to(c)))
	check("every-part-uses-parent-material", own.is_empty(), {"not_using_parent": own})

	# Godot 3 names load without complaint and do nothing.
	var godot3 := []
	for path in [SCENE, LIBRARY]:
		var text := FileAccess.get_file_as_string(path)
		for pattern in ["(?m)^loop = ", "playback_speed", "(?m)^playing = ", "(?m)^frames = ", "AnimatedSprite\"", "playback_process_mode"]:
			var re := RegEx.create_from_string(pattern)
			if re.search(text):
				godot3.append("%s: %s" % [path.get_file(), pattern])
	check("no-godot3-names", godot3.is_empty(), {"found": godot3})
	visual.free()
	completed = true

func _check_visibility(clip_name: String, clip: Animation, body_shown: bool) -> void:
	var tb := clip.find_track(NodePath("Body:visible"), Animation.TYPE_VALUE)
	var tr := clip.find_track(NodePath("Rig:visible"), Animation.TYPE_VALUE)
	var ok := tb >= 0 and tr >= 0 and clip.track_get_key_count(tb) == 1 and clip.track_get_key_count(tr) == 1
	ok = ok and at_frame(clip.track_get_key_time(tb, 0), 0) and at_frame(clip.track_get_key_time(tr, 0), 0)
	ok = ok and clip.track_get_key_value(tb, 0) == body_shown and clip.track_get_key_value(tr, 0) == (not body_shown)
	ok = ok and clip.value_track_get_update_mode(tb) == Animation.UPDATE_DISCRETE and clip.value_track_get_update_mode(tr) == Animation.UPDATE_DISCRETE
	check(clip_name + "-owns-visibility", ok, {"body_track": tb, "rig_track": tr})
