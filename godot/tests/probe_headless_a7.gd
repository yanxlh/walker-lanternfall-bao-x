extends SceneTree
## Assignment 7 probe of the facts CLAUDE.md lists under "Headless facts". Not a test; output recorded in
## evidence/assignment-7/headless-facts/. Run: Godot --headless --path godot --script res://tests/probe_headless_a7.gd

var drawn := 0

func _initialize() -> void:
	RenderingServer.frame_post_draw.connect(func(): drawn += 1)
	call_deferred("_main")

func _main() -> void:
	var out := {"engine": Engine.get_version_info().string}
	# A headless run advances a clip: play and advance, then read the property it keys.
	var root_node := Node2D.new()
	var sprite := Sprite2D.new()
	sprite.name = "Body"
	sprite.hframes = 10
	root_node.add_child(sprite)
	var player := AnimationPlayer.new()
	root_node.add_child(player)
	get_root().add_child(root_node)
	var clip := Animation.new()
	clip.length = 16 / 60.0
	var t := clip.add_track(Animation.TYPE_VALUE)
	clip.track_set_path(t, "Body:frame")
	clip.value_track_set_update_mode(t, Animation.UPDATE_DISCRETE)
	clip.track_insert_key(t, 0.0, 2)
	clip.track_insert_key(t, 8 / 60.0, 3)
	var lib := AnimationLibrary.new()
	lib.add_animation("walk", clip)
	player.add_animation_library("", lib)
	player.play("walk")
	player.advance(9 / 60.0)
	out["headless_advances_clip"] = {"frame_after_9_ticks": sprite.frame}
	# Key times are 32-bit floats after a .tres round trip.
	ResourceSaver.save(lib, "user://probe_lib.tres")
	var back: AnimationLibrary = ResourceLoader.load("user://probe_lib.tres", "", ResourceLoader.CACHE_MODE_IGNORE)
	var k := back.get_animation("walk").track_get_key_time(0, 1)
	out["key_time_round_trip"] = {"written": 8 / 60.0, "read": k, "equal": k == 8 / 60.0, "abs_diff": absf(k - 8 / 60.0)}
	# value_track_get_update_mode on a non-value track.
	var c3 := Animation.new()
	var p3 := c3.add_track(Animation.TYPE_POSITION_3D)
	out["update_mode_on_position_3d_track"] = {"returned": c3.value_track_get_update_mode(p3), "UPDATE_CONTINUOUS": Animation.UPDATE_CONTINUOUS}
	for i in 30:
		await process_frame
	out["frame_post_draw_in_30_frames"] = drawn
	out["display_driver"] = DisplayServer.get_name()
	print("PROBE ", JSON.stringify(out))
	root_node.free()
	quit()
