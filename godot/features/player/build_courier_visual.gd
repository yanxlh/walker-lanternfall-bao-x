extends SceneTree
## Builds the courier's visual scene and clip library from CHANGE-BRIEF.md (Assignment 7) and saves both with
## ResourceSaver, so the editor shows them and every key is reviewable as text. Run headless:
##   Godot --headless --path godot --script res://features/player/build_courier_visual.gd
## The game and the tests load the saved files, never this script.

const SHEET := "res://assets/art/pc_sheet.png"
const SCENE := "res://features/player/courier_visual.tscn"
const LIBRARY := "res://features/player/courier_clips.tres"
const FPS := 60.0
const HFRAMES := 10
const VFRAMES := 1
## Cell pixel that sits on the courier's origin (player.gd SPRITE_ORIGIN).
const ORIGIN := Vector2(16, 23)
## The rig is cut from this cell (walk_contact).
const RIG_CELL := 2

## Sprite clips on Body:frame. keys: [frame, tick]; length in ticks.
const SPRITE_CLIPS := {
	"idle": {"keys": [[1, 0]], "length": 1, "loop": false},
	"walk": {"keys": [[2, 0], [3, 8]], "length": 16, "loop": true},
	"cast": {"keys": [[4, 0]], "length": 1, "loop": false},
	"hurt": {"keys": [[5, 0]], "length": 1, "loop": false},
	"levelup": {"keys": [[6, 0]], "length": 1, "loop": false},
	"sunflare": {"keys": [[7, 0]], "length": 1, "loop": false},
	"defeat": {"keys": [[8, 0]], "length": 1, "loop": false},
	"victory": {"keys": [[9, 0]], "length": 1, "loop": false},
}

## Rig parts: region of the rig cell (cell-local), and the node they hang from.
const PARTS := {
	"Legs": {"region": Rect2(11, 28, 14, 4), "parent": "Rig"},
	"Coat": {"region": Rect2(11, 20, 14, 8), "parent": "Rig/Hips"},
	"Arm": {"region": Rect2(12, 13, 5, 7), "parent": "Rig/Hips/Chest"},
	"Head": {"region": Rect2(17, 8, 8, 12), "parent": "Rig/Hips/Chest/Neck"},
}
## Pivots, cell-local.
const PIVOTS := {
	"Rig/Hips": Vector2(16, 27),
	"Rig/Hips/Chest": Vector2(16, 20),
	"Rig/Hips/Chest/Neck": Vector2(18, 19),
}

## Dash phase table (ticks at 60 per second) and keys: [tick, value].
const DASH_STARTUP := 6
const DASH_ACTIVE := 10
const DASH_RECOVERY := 12
const DASH_TRACKS := {
	"Rig:position": [[0, Vector2(0, 0)], [4, Vector2(0, 1)], [6, Vector2(0, -1)], [16, Vector2(0, 0)], [20, Vector2(0, 1)], [28, Vector2(0, 0)]],
	"Rig/Hips:rotation": [[0, 0.0], [4, -0.15], [6, 0.35], [16, 0.30], [20, -0.08], [28, 0.0]],
	"Rig/Hips/Chest/Neck:rotation": [[0, 0.0], [4, 0.10], [6, -0.30], [12, -0.20], [16, -0.25], [20, 0.15], [24, -0.05], [28, 0.0]],
}
## Spacing per phase: ease in through startup, linear through active, ease out through recovery.
const STARTUP_TRANSITION := 2.0
const ACTIVE_TRANSITION := 1.0
const RECOVERY_TRANSITION := 0.5

func _initialize() -> void:
	var sheet: Texture2D = load(SHEET)
	var library := AnimationLibrary.new()
	for clip_name in SPRITE_CLIPS:
		library.add_animation(clip_name, _sprite_clip(SPRITE_CLIPS[clip_name]))
	library.add_animation("dash", _dash_clip())
	var err := ResourceSaver.save(library, LIBRARY)
	if err != OK:
		push_error("could not save %s: %d" % [LIBRARY, err])
		quit(1)
		return
	library = ResourceLoader.load(LIBRARY, "", ResourceLoader.CACHE_MODE_REPLACE)
	var visual := _visual(sheet, library)
	var packed := PackedScene.new()
	err = packed.pack(visual)
	if err == OK:
		err = ResourceSaver.save(packed, SCENE)
	visual.free()
	if err != OK:
		push_error("could not save %s: %d" % [SCENE, err])
		quit(1)
		return
	print("saved %s and %s" % [SCENE, LIBRARY])
	quit(0)

func _visibility_tracks(clip: Animation, body: bool) -> void:
	for path in ["Body:visible", "Rig:visible"]:
		var t := clip.add_track(Animation.TYPE_VALUE)
		clip.track_set_path(t, path)
		clip.value_track_set_update_mode(t, Animation.UPDATE_DISCRETE)
		clip.track_insert_key(t, 0.0, body if path == "Body:visible" else not body)

func _sprite_clip(spec: Dictionary) -> Animation:
	var clip := Animation.new()
	clip.length = spec["length"] / FPS
	clip.loop_mode = Animation.LOOP_LINEAR if spec["loop"] else Animation.LOOP_NONE
	clip.step = 1.0 / FPS
	_visibility_tracks(clip, true)
	var t := clip.add_track(Animation.TYPE_VALUE)
	clip.track_set_path(t, "Body:frame")
	clip.value_track_set_update_mode(t, Animation.UPDATE_DISCRETE)
	clip.track_set_interpolation_type(t, Animation.INTERPOLATION_NEAREST)
	for key in spec["keys"]:
		clip.track_insert_key(t, key[1] / FPS, int(key[0]))
	return clip

func _transition_for(tick: int) -> float:
	if tick < DASH_STARTUP:
		return STARTUP_TRANSITION
	if tick < DASH_STARTUP + DASH_ACTIVE:
		return ACTIVE_TRANSITION
	return RECOVERY_TRANSITION

func _dash_clip() -> Animation:
	var clip := Animation.new()
	clip.length = (DASH_STARTUP + DASH_ACTIVE + DASH_RECOVERY) / FPS
	clip.loop_mode = Animation.LOOP_NONE
	clip.step = 1.0 / FPS
	_visibility_tracks(clip, false)
	for path in DASH_TRACKS:
		var t := clip.add_track(Animation.TYPE_VALUE)
		clip.track_set_path(t, path)
		clip.value_track_set_update_mode(t, Animation.UPDATE_CONTINUOUS)
		clip.track_set_interpolation_type(t, Animation.INTERPOLATION_LINEAR)
		for key in DASH_TRACKS[path]:
			clip.track_insert_key(t, key[0] / FPS, key[1], _transition_for(key[0]))
	return clip

func _visual(sheet: Texture2D, library: AnimationLibrary) -> Node2D:
	var visual := Node2D.new()
	visual.name = "CourierVisual"
	visual.use_parent_material = true
	var body := Sprite2D.new()
	body.name = "Body"
	body.texture = sheet
	body.hframes = HFRAMES
	body.vframes = VFRAMES
	body.frame = 1
	body.centered = false
	body.offset = -ORIGIN
	body.use_parent_material = true
	visual.add_child(body)
	var rig := Node2D.new()
	rig.name = "Rig"
	rig.visible = false
	rig.use_parent_material = true
	visual.add_child(rig)
	# Pivots in parent-first order; each is placed relative to its parent pivot (the rig root is the origin).
	for path in ["Rig/Hips", "Rig/Hips/Chest", "Rig/Hips/Chest/Neck"]:
		var pivot := Node2D.new()
		pivot.name = path.get_file()
		pivot.use_parent_material = true
		pivot.position = PIVOTS[path] - _pivot_of(path.get_base_dir())
		visual.get_node(path.get_base_dir()).add_child(pivot)
	for part in PARTS:
		var spec: Dictionary = PARTS[part]
		var region: Rect2 = spec["region"]
		var sprite := Sprite2D.new()
		sprite.name = part
		sprite.texture = sheet
		sprite.region_enabled = true
		sprite.region_rect = Rect2(region.position + Vector2(RIG_CELL * 32, 0), region.size)
		sprite.centered = false
		sprite.use_parent_material = true
		sprite.position = region.position - _pivot_of(spec["parent"])
		var parent := visual.get_node(spec["parent"])
		parent.add_child(sprite)
		# Each part draws before the pivots under the same parent, so the head and arm stay over the coat and legs.
		parent.move_child(sprite, 0)
	var player := AnimationPlayer.new()
	player.name = "AnimationPlayer"
	player.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
	player.add_animation_library("", library)
	visual.add_child(player)
	for n in visual.find_children("*", "", true, false):
		n.owner = visual
	return visual

## Cell-local position of a pivot path; the rig root sits on the courier's origin.
func _pivot_of(path: String) -> Vector2:
	return PIVOTS.get(path, ORIGIN)
