extends Node2D
## Render fixture, not gameplay. Compare lifecycle, not identical random trajectories.
const Ground = preload("res://features/world/ground.gd")
var frame := 0
var cpu: CPUParticles2D
var gpu: GPUParticles2D
func _ready() -> void:
	add_child(Ground.new())
	var camera := Camera2D.new()
	add_child(camera)
	cpu = (load("res://effects/defeat_sparks.tscn") as PackedScene).instantiate()
	add_child(cpu)
	cpu.position = Vector2(-80, 0)
	var study := (load("res://previews/shader_study/hit_sparks_gpu.tscn") as PackedScene).instantiate()
	add_child(study)
	gpu = study.get_node("HitSparksGPU")
	gpu.position = Vector2(80, 0)
	for node in [cpu,gpu]:
		node.use_fixed_seed = true
		node.seed = 7280
	var overlay := CanvasLayer.new()
	add_child(overlay)
	var label := Label.new()
	label.position = Vector2(12,12)
	label.text = "STUDY FIXTURE: CPU (left) / generated GPU shader (right)"
	label.add_theme_font_size_override("font_size",12)
	overlay.add_child(label)
func _process(_delta: float) -> void:
	frame += 1
	if frame == 10:
		cpu.restart()
		gpu.restart()
