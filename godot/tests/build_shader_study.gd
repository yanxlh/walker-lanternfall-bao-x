extends SceneTree
## Builds godot/previews/shader_study/hit_sparks_gpu.tscn: a GPUParticles2D converted from the game's CPU hit
## sparks with Godot's own GPUParticles2D.convert_from_particles(). Study scene only; the game never loads it.
func _initialize() -> void:
	call_deferred("_main")

func _main() -> void:
	var cpu := (load("res://effects/defeat_sparks.tscn") as PackedScene).instantiate() as CPUParticles2D
	var root_node := Node2D.new()
	root_node.name = "ShaderStudy"
	var gpu := GPUParticles2D.new()
	gpu.name = "HitSparksGPU"
	root_node.add_child(gpu)
	gpu.owner = root_node
	gpu.convert_from_particles(cpu)
	gpu.material = cpu.material
	gpu.texture_filter = cpu.texture_filter
	var packed := PackedScene.new()
	packed.pack(root_node)
	var err := ResourceSaver.save(packed, "res://previews/shader_study/hit_sparks_gpu.tscn")
	print("save error: ", err)
	var m := gpu.process_material as ParticleProcessMaterial
	print("process material: ", m)
	for p in ["direction", "spread", "initial_velocity_min", "initial_velocity_max", "gravity", "damping_min", "damping_max", "scale_min", "scale_max", "emission_shape"]:
		print("  ", p, " = ", m.get(p))
	print("  amount=", gpu.amount, " lifetime=", gpu.lifetime, " one_shot=", gpu.one_shot, " explosiveness=", gpu.explosiveness, " local_coords=", gpu.local_coords, " texture=", gpu.texture)
	cpu.free()
	root_node.free()
	quit()
