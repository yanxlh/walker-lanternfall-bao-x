extends SceneTree
## Wrapper self-check fixture (Assignment 7): loads one missing resource and one scene whose external resource is
## missing, prints no SCRIPT ERROR, and quits 0. scripts/check-run-test.sh expects run-test.sh to exit 1 on it.
## Not a test suite and never loaded by the game.

func _initialize() -> void:
	var missing = load("res://tests/does_not_exist.tres")
	var path := "user://broken_ext.tscn"
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string("[gd_scene format=3]\n\n[ext_resource type=\"Texture2D\" path=\"res://assets/art/does_not_exist.png\" id=\"1\"]\n\n[node name=\"Broken\" type=\"Sprite2D\"]\ntexture = ExtResource(\"1\")\n")
	f.close()
	var broken = ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE)
	print("fixture: missing=%s broken_scene=%s" % [missing, broken])
	quit(0)
