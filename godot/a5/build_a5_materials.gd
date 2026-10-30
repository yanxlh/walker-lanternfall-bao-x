extends SceneTree
## Builds the A5 material resources and scenes from CHANGE-BRIEF.md (3D material plan, hint experiment, 10/30 revision).
## Saves through ResourceSaver; no UID is typed by hand. Godot wrote none for these files, so they reference each other
## by path. Fails, writing nothing, if a shader or a uniform is missing.
## Run: Godot --headless --path godot --script res://a5/build_a5_materials.gd

const SURFACE := "res://shaders/cobblestone_surface.gdshader"
const HINT := "res://shaders/hint_experiment.gdshader"
const TEX := "res://assets/textures/cobblestone_floor_08/cobblestone_floor_08_%s_1k.png"
const HINT_PNG := "res://a5/hint_experiment/hint_greys_3x1.png"
const ROOM := "res://a3/lantern_gate_room.tscn"

## Material A (Floor) and B (StandIn), values from the brief's material plan.
const MATERIALS := {
	"res://a5/materials/cobblestone_warm_floor.tres": {
		"tint": Color(1.0, 0.92, 0.80, 1.0), "uv_scale": 2.0,
		"roughness_min": 0.55, "roughness_max": 0.95, "normal_strength": 1.0,
	},
	"res://a5/materials/cobblestone_cool_standin.tres": {
		"tint": Color(0.72, 0.85, 1.0, 1.0), "uv_scale": 1.0,
		"roughness_min": 0.20, "roughness_max": 0.55, "normal_strength": 0.5,
	},
}
const HINT_MATERIALS := {
	"res://a5/hint_experiment/hint_with_source_color.tres": true,
	"res://a5/hint_experiment/hint_without_source_color.tres": false,
}

func _initialize() -> void:
	var surface: Shader = _shader(SURFACE, ["color_tex", "normal_tex", "roughness_tex", "tint", "uv_scale", "roughness_min", "roughness_max", "normal_strength"])
	var hint: Shader = _shader(HINT, ["color_sample", "raw_sample", "use_color"])
	if surface == null or hint == null:
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://a5/materials"))
	var saved := {}
	for path in MATERIALS:
		var mat := ShaderMaterial.new()
		mat.shader = surface
		mat.set_shader_parameter("color_tex", load(TEX % "diff"))
		mat.set_shader_parameter("normal_tex", load(TEX % "nor_gl"))
		mat.set_shader_parameter("roughness_tex", load(TEX % "rough"))
		for k in MATERIALS[path]:
			mat.set_shader_parameter(k, MATERIALS[path][k])
		_save(mat, path)
		saved[path] = load(path)
	for path in HINT_MATERIALS:
		var mat := ShaderMaterial.new()
		mat.shader = hint
		var png: Texture2D = load(HINT_PNG)
		mat.set_shader_parameter("color_sample", png)
		mat.set_shader_parameter("raw_sample", png)
		mat.set_shader_parameter("use_color", HINT_MATERIALS[path])
		_save(mat, path)
	_build_material_room(saved)
	_build_hint_scene()
	print("build_a5_materials: done")
	quit()

func _shader(path: String, uniforms: Array) -> Shader:
	if not ResourceLoader.exists(path):
		push_error("missing shader %s" % path)
		return null
	var s: Shader = load(path)
	var names := s.get_shader_uniform_list().map(func(u): return u.name)
	for n in uniforms:
		if not n in names:
			push_error("%s does not declare %s (declares %s)" % [path, n, names])
			return null
	return s

func _save(res: Resource, path: String) -> void:
	var err := ResourceSaver.save(res, path)
	print("saved %s: %s" % [path, error_string(err)])

## An inherited scene: the A3 room unchanged, with the two material_override properties replaced and, from the
## 10/30 revision, the floor's BoxMesh swapped for an 8 x 8 PlaneMesh at the box's top (y = 0): the box's top face
## uses only 1/3 x 1/2 of UV space, which stretched the stones 1.5:1 and showed less than one tile.
## Packing an instance made with GEN_EDIT_STATE_MAIN_INHERITED from a script saved a full copy of the room, so the
## inherited scene is written as text (paths only, no UIDs) and then loaded and re-saved so Godot normalizes it.
func _build_material_room(_saved: Dictionary) -> void:
	var path := "res://a5/material_room.tscn"
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string("\n".join([
		"[gd_scene format=3]", "",
		"[ext_resource type=\"PackedScene\" path=\"%s\" id=\"1_room\"]" % ROOM,
		"[ext_resource type=\"Material\" path=\"res://a5/materials/cobblestone_warm_floor.tres\" id=\"2_floor\"]",
		"[ext_resource type=\"Material\" path=\"res://a5/materials/cobblestone_cool_standin.tres\" id=\"3_standin\"]", "",
		"[sub_resource type=\"PlaneMesh\" id=\"PlaneMesh_floor\"]", "size = Vector2(8, 8)", "",
		"[node name=\"LanternGateRoom\" instance=ExtResource(\"1_room\")]", "",
		"[node name=\"Mesh\" parent=\"Floor\"]", "transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)",
		"material_override = ExtResource(\"2_floor\")", "mesh = SubResource(\"PlaneMesh_floor\")", "",
		"[node name=\"Mesh\" parent=\"StandIn\"]", "material_override = ExtResource(\"3_standin\")", ""]))
	f.close()
	var packed: PackedScene = ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE)
	_save(packed, path)

## Two unshaded quads facing an orthographic camera, Linear tonemap at exposure 1, glow, fog and adjustments off.
func _build_hint_scene() -> void:
	var root := Node3D.new()
	root.name = "HintExperiment"
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0, 0, 0)
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.tonemap_exposure = 1.0
	env.glow_enabled = false
	env.fog_enabled = false
	env.adjustment_enabled = false
	var world := WorldEnvironment.new()
	world.name = "WorldEnvironment"
	world.environment = env
	_add(root, world)
	var cam := Camera3D.new()
	cam.name = "Camera3D"
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 4.5
	cam.position = Vector3(0, 0, 5)
	cam.current = true
	_add(root, cam)
	var quads := [["QuadWithSourceColor", -1.75, "res://a5/hint_experiment/hint_with_source_color.tres", "source_color"],
		["QuadWithoutHint", 1.75, "res://a5/hint_experiment/hint_without_source_color.tres", "no hint"]]
	for q in quads:
		var quad := MeshInstance3D.new()
		quad.name = q[0]
		var mesh := QuadMesh.new()
		mesh.size = Vector2(3.0, 1.0)
		quad.mesh = mesh
		quad.position = Vector3(q[1], 0, 0)
		quad.material_override = load(q[2])
		_add(root, quad)
		var label := Label3D.new()
		label.name = q[0] + "Label"
		label.text = q[3]
		label.position = Vector3(q[1], 0.9, 0)
		label.font_size = 48
		_add(root, label)
	var packed := PackedScene.new()
	packed.pack(root)
	_save(packed, "res://a5/hint_experiment/hint_experiment.tscn")
	root.free()

func _add(root: Node, child: Node) -> void:
	root.add_child(child)
	child.owner = root
