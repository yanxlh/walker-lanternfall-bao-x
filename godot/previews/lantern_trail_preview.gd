extends Node2D
## Isolated movement fixture, not a recording of a gameplay run.
const Ground = preload("res://features/world/ground.gd")
const Player = preload("res://features/player/player.gd")
const TrailScene = preload("res://effects/lantern_trail.tscn")
const BaselineTrailScene = preload("res://previews/baseline/lantern_trail_r0.tscn")
var baseline := false
var frame := 0
var courier: Node2D
var trail: CPUParticles2D
var auto_repeat := false
var status_label: Label

func _ready() -> void:
	auto_repeat = "--repeat" in OS.get_cmdline_user_args()
	baseline = "--baseline" in OS.get_cmdline_user_args()
	add_child(Ground.new())
	courier = Player.new()
	courier.position = Vector2(-45, 0)
	add_child(courier)
	trail = (BaselineTrailScene if baseline else TrailScene).instantiate() as CPUParticles2D
	trail.use_fixed_seed = true
	trail.seed = 7280
	add_child(trail)
	add_child(Camera2D.new())
	var overlay := CanvasLayer.new()
	add_child(overlay)
	status_label = Label.new()
	status_label.position = Vector2(12, 12)
	status_label.add_theme_font_size_override("font_size", 12)
	overlay.add_child(status_label)
	var label := Label.new()
	label.position = Vector2(12, 320)
	label.text = "FIXTURE: movement frames 10..39 / Space: replay / Esc: exit"
	label.add_theme_font_size_override("font_size", 12)
	overlay.add_child(label)

func _process(delta: float) -> void:
	frame += 1
	var moving := frame >= 10 and frame < 40
	if moving:
		courier.position.x += 90.0 * delta
	trail.global_position = courier.global_position + Vector2(0, 7)
	trail.emitting = moving
	status_label.text = "LANTERN TRAIL / FIXTURE / %s / frame %d / moving %s" % ["r0 original" if baseline else "r1 accepted", frame, moving]
	if auto_repeat and frame >= 90:
		reset_fixture()

func reset_fixture() -> void:
	frame = 0
	courier.position = Vector2(-45, 0)
	trail.restart()
	trail.emitting = false

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_SPACE:
			reset_fixture()
		elif event.keycode == KEY_ESCAPE:
			get_tree().quit()
