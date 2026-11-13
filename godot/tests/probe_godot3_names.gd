extends SceneTree
## Assignment 7 probe: what the Godot 3 animation names actually do in this engine (4.7.2), set from script and
## loaded from resource text, and what a continuous frame track shows between adjacent and distant cells.
## Prints one JSON line; the runs are recorded in evidence/assignment-7/godot3-names/. Not a test.

func _initialize() -> void:
	var out := {"engine": Engine.get_version_info().string}
	var a := Animation.new()
	a.set("loop", true)
	out["script_set_loop_true"] = {"loop_mode": a.loop_mode, "has_loop_property": "loop" in a, "get_loop": a.get("loop")}
	var text := "[gd_resource type=\"Animation\" format=3]\n\n[resource]\nlength = 1.0\nloop = true\n"
	var path := "user://probe_loop.tres"
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string(text)
	f.close()
	var loaded: Animation = ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE)
	out["tres_loop_true"] = {"loop_mode": loaded.loop_mode if loaded else -1}
	var p := AnimationPlayer.new()
	p.set("playback_speed", 2.0)
	out["script_set_playback_speed_2"] = {"speed_scale": p.speed_scale, "has_property": "playback_speed" in p}
	var s := AnimatedSprite2D.new()
	s.set("frames", SpriteFrames.new())
	s.set("playing", true)
	out["animated_sprite_frames_playing"] = {"sprite_frames_set": s.sprite_frames != null, "is_playing": s.is_playing(), "has_frames": "frames" in s, "has_playing": "playing" in s}
	p.free()
	s.free()

	# A continuous int frame track: adjacent keys (2 -> 3) and distant keys (2 -> 6), sampled each 1/60 s.
	for pair in [[2, 3], [2, 6]]:
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
		clip.value_track_set_update_mode(t, Animation.UPDATE_CONTINUOUS)
		clip.track_insert_key(t, 0.0, pair[0])
		clip.track_insert_key(t, 8 / 60.0, pair[1])
		var lib := AnimationLibrary.new()
		lib.add_animation("c", clip)
		player.add_animation_library("", lib)
		player.callback_mode_process = AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL
		player.play("c")
		var cells := []
		for tick in 9:
			player.seek(tick / 60.0, true)
			cells.append(sprite.frame)
		out["continuous_%d_to_%d" % pair] = cells
		root_node.free()
	print("PROBE ", JSON.stringify(out))
	quit()
