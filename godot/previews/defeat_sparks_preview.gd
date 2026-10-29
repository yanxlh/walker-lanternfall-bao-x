extends Node2D
## Fixture only: this scene never creates a game Session or changes gameplay.

const Burst = preload("res://effects/defeat_sparks.tscn")
const Ground = preload("res://features/world/ground.gd")
const Player = preload("res://features/player/player.gd")

@export var retrigger := false
@export var trigger_frame := 10
@export var repeat_frame := 13
@export var fixed_seed := 7280
var frame := 0
var active_bursts: Array[CPUParticles2D] = []
var status_label: Label

func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	retrigger = retrigger or "--retrigger" in args
	add_child(Ground.new())
	var courier := Player.new()
	courier.position = Vector2(-24, 0)
	add_child(courier)
	var camera := Camera2D.new()
	add_child(camera)
	var overlay := CanvasLayer.new()
	add_child(overlay)
	status_label = Label.new()
	status_label.position = Vector2(12, 12)
	status_label.add_theme_font_size_override("font_size", 12)
	overlay.add_child(status_label)
	var instructions := Label.new()
	instructions.position = Vector2(12, 310)
	instructions.text = "FIXTURE: real market background, original courier scale\nSpace: burst   R: rapid pair   Esc: exit"
	instructions.add_theme_font_size_override("font_size", 12)
	overlay.add_child(instructions)

func _process(_delta: float) -> void:
	frame += 1
	if frame == trigger_frame or (retrigger and frame == repeat_frame):
		spawn_burst()
	status_label.text = "WEAPON HIT SPARKS / FIXTURE / frame %d / bursts %d" % [frame, active_bursts.size()]

func spawn_burst() -> void:
	var burst := Burst.instantiate() as CPUParticles2D
	# Seed is deliberately confined to the fixture instance.
	burst.use_fixed_seed = true
	burst.seed = fixed_seed
	add_child(burst)
	burst.position = Vector2(8, -2)
	active_bursts.append(burst)
	burst.finished.connect(func():
		active_bursts.erase(burst)
		burst.queue_free())
	burst.restart()
	print("FIXTURE burst at frame ", frame)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_SPACE:
				spawn_burst()
			KEY_R:
				spawn_burst()
				await get_tree().create_timer(0.1).timeout
				spawn_burst()
			KEY_ESCAPE:
				get_tree().quit()
