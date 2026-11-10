extends Node2D
## Film fixture (isolated copy only): the game's CPU hit sparks and the editor-converted GPU study copy, side by
## side on the real market floor, triggered on the same frames with the same fixed seed. It shows what the
## generated process shader does with the material the editor produced. Not gameplay; labelled on screen.
##   godot --path . res://study_capture.tscn --write-movie out.avi --fixed-fps 30 --quit-after 90

const CpuBurst = preload("res://effects/defeat_sparks.tscn")
const Study = preload("res://previews/shader_study/hit_sparks_gpu.tscn")
const Ground = preload("res://features/world/ground.gd")
const TRIGGERS := [10, 50]
var frame := 0
var cpu: CPUParticles2D
var gpu: GPUParticles2D

func _ready() -> void:
	add_child(Ground.new())
	var camera := Camera2D.new()
	add_child(camera)
	cpu = CpuBurst.instantiate() as CPUParticles2D
	cpu.use_fixed_seed = true
	cpu.seed = 7280
	cpu.position = Vector2(-70, 0)
	add_child(cpu)
	var study := Study.instantiate()
	add_child(study)
	gpu = study.get_node("HitSparksGPU") as GPUParticles2D
	gpu.use_fixed_seed = true
	gpu.seed = 7280
	gpu.position = Vector2(70, 0)
	var layer := CanvasLayer.new()
	add_child(layer)
	for spec in [["CPU — the game's effect (defeat_sparks.tscn)", Vector2(120, 250)],
			["GPU copy — editor-converted shader", Vector2(360, 250)],
			["FIXTURE · real engine capture · same seed, same frames", Vector2(12, 330)]]:
		var l := Label.new()
		l.text = spec[0]
		l.add_theme_font_size_override("font_size", 10)
		l.position = spec[1] - Vector2(70 if spec[1].x > 100 else 0, 0)
		layer.add_child(l)

func _process(_d: float) -> void:
	frame += 1
	if frame in TRIGGERS:
		cpu.restart()
		gpu.restart()
		print("STUDY trigger at frame ", frame)
