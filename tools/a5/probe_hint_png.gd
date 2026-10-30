extends SceneTree
## Prints the imported hint PNG: size, format, mipmaps, compression and the three texel values.
## Run: Godot --headless --path godot --script "$PWD/tools/a5/probe_hint_png.gd"
func _initialize() -> void:
	var t: Texture2D = load("res://a5/hint_experiment/hint_greys_3x1.png")
	var img := t.get_image()
	print("hint: ", img.get_width(), "x", img.get_height(), " format ", img.get_format(), " mipmaps ", img.has_mipmaps(), " compressed ", img.is_compressed(), " texels ", [img.get_pixel(0, 0).r8, img.get_pixel(1, 0).r8, img.get_pixel(2, 0).r8])
	quit()
