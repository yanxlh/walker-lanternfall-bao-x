extends SceneTree
## Writes the hint experiment's 3 x 1 PNG: opaque grey texels 64, 128 and 192 (CHANGE-BRIEF.md, hint experiment).
## Run: Godot --headless --path godot --script res://a5/hint_experiment/make_hint_png.gd
const OUT := "res://a5/hint_experiment/hint_greys_3x1.png"
const GREYS := [64, 128, 192]

func _initialize() -> void:
	var img := Image.create(GREYS.size(), 1, false, Image.FORMAT_RGB8)
	for i in GREYS.size():
		img.set_pixel(i, 0, Color8(GREYS[i], GREYS[i], GREYS[i]))
	var err := img.save_png(OUT)
	print("saved %s (%s): %s" % [OUT, error_string(err), GREYS])
	quit(1 if err != OK else 0)
