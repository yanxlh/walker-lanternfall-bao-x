extends SceneTree

func _initialize() -> void:
	call_deferred("capture")

func capture() -> void:
	var show_colliders := OS.get_environment("A3_COLLISIONS") == "1"
	debug_collisions_hint = show_colliders
	var room = load("res://a3/lantern_gate_room.tscn").instantiate()
	root.add_child(room)
	if show_colliders:
		room.get_node("StandIn").position.x = -0.65
	for i in 8:
		await process_frame
	await RenderingServer.frame_post_draw
	var image := root.get_viewport().get_texture().get_image()
	var filename := "lantern-gate-colliders.png" if show_colliders else "lantern-gate-room.png"
	var path := ProjectSettings.globalize_path("res://../evidence/a3/" + filename)
	var err := image.save_png(path)
	print("A3_CAPTURE path=%s size=%s error=%d" % [path, image.get_size(), err])
	quit(0 if err == OK else 1)
