extends SceneTree
## Prints class, size, image format, mipmaps and compression of the four imported A5 textures.
## Run: Godot --headless --path godot --script "$PWD/tools/a5/probe_texture_formats.gd"
func _initialize() -> void:
	for m in ["diff", "nor_gl", "nor_dx", "rough"]:
		var p := "res://assets/textures/cobblestone_floor_08/cobblestone_floor_08_%s_1k.png" % m
		var t: Texture2D = load(p)
		var img := t.get_image()
		print(m, ": ", t.get_class(), " ", img.get_width(), "x", img.get_height(), " format ", img.get_format(), " (", ["L8","LA8","R8","RG8","RGB8","RGBA8"][img.get_format()] if img.get_format() < 6 else "other", ") mipmaps ", img.has_mipmaps(), " compressed ", img.is_compressed())
	quit()
