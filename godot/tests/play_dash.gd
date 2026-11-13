extends SceneTree
## Assignment 7 playtest launcher: the real main scene, played by hand, with the dash already unlocked at the start
## of every run (Enter, R) so it can be tried without waiting for the card. Nothing else differs from the game,
## and the game never loads this script. Run windowed, optionally slowed:
##   Godot --path godot --script res://tests/play_dash.gd [--time-scale 0.25]

func _initialize() -> void:
	call_deferred("_main")

func _main() -> void:
	var game = load("res://game/main.tscn").instantiate()
	root.add_child(game)
	game.run_started.connect(func():
		game.prog.apply("dash")
		game.player.dash_unlocked = true)
	print("play_dash: the dash is unlocked at the start of every run (Shift / Space / B)")
