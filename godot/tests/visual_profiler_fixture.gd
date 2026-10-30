extends Node
## Editor-connected measurement fixture. Never loaded by the main game.
var game
var condition := "acap"
var effects := false
var tick := 0
var moving_right := true
var status_label: Label
func key(code: int, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)
func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	var i := args.find("--condition")
	if i >= 0: condition = args[i + 1]
	effects = "--effects-on" in args
	AudioServer.set_bus_mute(0,true)
	call_deferred("start")
func start() -> void:
	game = load("res://game/session.gd").new()
	game.test_no_spawn = true
	add_child(game)
	if not effects: game.particles.free()
	game.run_started.connect(setup_fixture, CONNECT_ONE_SHOT)
	await get_tree().process_frame
	key(KEY_ENTER,true)
	await get_tree().process_frame
	key(KEY_ENTER,false)
	await get_tree().process_frame
	if condition == "move": key(KEY_D,true)
	var layer := CanvasLayer.new()
	layer.layer = 50
	add_child(layer)
	status_label = Label.new()
	status_label.position = Vector2(10,275)
	status_label.add_theme_font_size_override("font_size",12)
	layer.add_child(status_label)
	print("VISUAL PROFILER FIXTURE ",condition," ","ON" if effects else "OFF"," renderer=",RenderingServer.get_current_rendering_method()," driver=",RenderingServer.get_current_rendering_driver_name())
func setup_fixture() -> void:
	if condition == "acap":
		game.prog.beam_pierce = 40
		for i in 40:
			var enemy = game.spawn_enemy("wraith",Vector2(70+i*0.2,0))
			enemy.hp = 999999.0
			enemy.speed = 0.0
	elif condition == "move": game.player.position = Vector2(-400,0)
func _process(_delta: float) -> void:
	if not is_instance_valid(game) or not is_instance_valid(status_label):return
	tick += 1
	if condition == "move" and tick % 90 == 0:
		key(KEY_D,false)
		key(KEY_A,false)
		moving_right = not moving_right
		key(KEY_D if moving_right else KEY_A,true)
	var hits: int = game.particles.hit_bursts.size() if effects else 0
	var trail: bool = game.particles.trail.emitting if effects else false
	status_label.text = "MEASUREMENT FIXTURE / %s / effects %s\nhit bursts %d / trail %s / tick %d" % [condition,"ON" if effects else "OFF",hits,str(trail),tick]
