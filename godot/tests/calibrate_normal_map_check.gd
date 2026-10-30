extends SceneTree
## Calibration run for normal_map_check.gd on the Poly Haven GL/DX pair of Cobblestone Floor 08.
## Not a suite: it prints the four ratios that set the pass threshold. Decodes the source PNGs, not the imports.
const Check = preload("res://tests/normal_map_check.gd")
const DIR := "res://assets/textures/cobblestone_floor_08/"

func _initialize() -> void:
	for m in ["nor_gl", "nor_dx"]:
		var img := Image.load_from_file(ProjectSettings.globalize_path(DIR + "cobblestone_floor_08_%s_1k.png" % m))
		print("%s %dx%d: curl_ratio directx=false %.4f, directx=true %.4f" % [m, img.get_width(), img.get_height(),
			Check.curl_ratio(img, false), Check.curl_ratio(img, true)])
	quit()
