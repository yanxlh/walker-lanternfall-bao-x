extends Node3D

@onready var stand_in: CharacterBody3D = $StandIn

func _ready() -> void:
	_ensure_inputs()
	$Camera3D.look_at(Vector3(0.0, 1.25, 0.0))

func _physics_process(_delta: float) -> void:
	var axis := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	stand_in.velocity = Vector3(axis.x, 0.0, axis.y) * 2.0
	stand_in.move_and_slide()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("debug_collision"):
		get_tree().debug_collisions_hint = not get_tree().debug_collisions_hint
	elif event.is_action_pressed("ui_cancel"):
		get_tree().change_scene_to_file("res://game/main.tscn")

func _ensure_inputs() -> void:
	var keys := {
		"move_left": [KEY_A, KEY_LEFT],
		"move_right": [KEY_D, KEY_RIGHT],
		"move_up": [KEY_W, KEY_UP],
		"move_down": [KEY_S, KEY_DOWN],
		"debug_collision": [KEY_F3],
	}
	for action in keys:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		for code in keys[action]:
			var key := InputEventKey.new()
			key.physical_keycode = code
			InputMap.action_add_event(action, key)
