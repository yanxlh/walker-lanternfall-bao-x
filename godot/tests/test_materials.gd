extends "res://tests/harness.gd"
## A5 material audit (godot/MATERIALS.md), pinned headlessly: shader source hints, uniform list, the four
## ShaderMaterials, the .import keys, the two scenes' lights and environment, and the normal-map curl check.
## A headless run draws nothing, so nothing here says how any of it looks.
const NormalMapCheck = preload("res://tests/normal_map_check.gd")

const SURFACE := "res://shaders/cobblestone_surface.gdshader"
const HINT := "res://shaders/hint_experiment.gdshader"
const TEX := "res://assets/textures/cobblestone_floor_08/cobblestone_floor_08_%s_1k.png"
const HINT_PNG := "res://a5/hint_experiment/hint_greys_3x1.png"
const FLOOR := "res://a5/materials/cobblestone_warm_floor.tres"
const STANDIN := "res://a5/materials/cobblestone_cool_standin.tres"
const HINT_WITH := "res://a5/hint_experiment/hint_with_source_color.tres"
const HINT_WITHOUT := "res://a5/hint_experiment/hint_without_source_color.tres"
const ROOM := "res://a5/material_room.tscn"
const A3_ROOM := "res://a3/lantern_gate_room.tscn"
const HINT_SCENE := "res://a5/hint_experiment/hint_experiment.tscn"
## Set from the calibration pair (evidence/assignment-5/textures/curl-calibration.log): the right convention
## gave 0.2236, the wrong one 1.7764, and the script's own scale puts "no surface" at 1.
const CURL_THRESHOLD := 1.0

## Declarations as written in the source: type, hints (spaces removed), default, group_uniforms group.
const SURFACE_UNIFORMS := {
	"color_tex": ["sampler2D", ["source_color", "filter_linear_mipmap", "repeat_enable"], "", ""],
	"normal_tex": ["sampler2D", ["hint_normal", "filter_linear_mipmap", "repeat_enable"], "", ""],
	"roughness_tex": ["sampler2D", ["filter_linear_mipmap", "repeat_enable"], "", ""],
	"tint": ["vec4", ["source_color"], "vec4(1.0,1.0,1.0,1.0)", "Surface"],
	"uv_scale": ["float", ["hint_range(0.25,4.0)"], "1.0", "Surface"],
	"roughness_min": ["float", ["hint_range(0.0,1.0)"], "0.2", "Response"],
	"roughness_max": ["float", ["hint_range(0.0,1.0)"], "0.8", "Response"],
	"normal_strength": ["float", ["hint_range(0.0,2.0)"], "1.0", "Response"],
}
const HINT_UNIFORMS := {
	"color_sample": ["sampler2D", ["source_color", "filter_nearest"], "", ""],
	"raw_sample": ["sampler2D", ["filter_nearest"], "", ""],
	"use_color": ["bool", [], "true", ""],
}
const VARIANT_TYPE := {"sampler2D": TYPE_OBJECT, "vec4": TYPE_COLOR, "float": TYPE_FLOAT, "bool": TYPE_BOOL}

## Every parameter each material sets; a String is the bound texture's path.
const MATERIALS := {
	FLOOR: [SURFACE, {"color_tex": "diff", "normal_tex": "nor_gl", "roughness_tex": "rough",
		"tint": Color(1.0, 0.92, 0.80, 1.0), "uv_scale": 2.0,
		"roughness_min": 0.55, "roughness_max": 0.95, "normal_strength": 1.0}],
	STANDIN: [SURFACE, {"color_tex": "diff", "normal_tex": "nor_gl", "roughness_tex": "rough",
		"tint": Color(0.72, 0.85, 1.0, 1.0), "uv_scale": 1.0,
		"roughness_min": 0.20, "roughness_max": 0.55, "normal_strength": 0.5}],
	HINT_WITH: [HINT, {"color_sample": HINT_PNG, "raw_sample": HINT_PNG, "use_color": true}],
	HINT_WITHOUT: [HINT, {"color_sample": HINT_PNG, "raw_sample": HINT_PNG, "use_color": false}],
}

## compress/mode, compress/normal_map, mipmaps/generate; then the imported image format, from CHANGE-BRIEF.md.
const IMPORTS := {
	"diff": [0, 2, true, Image.FORMAT_RGB8],
	"nor_gl": [0, 1, true, Image.FORMAT_RGB8],
	"rough": [0, 2, true, Image.FORMAT_L8],
	"nor_dx": [0, 1, true, Image.FORMAT_RGB8],
	"hint": [0, 2, false, Image.FORMAT_RGB8],
}

func run() -> void:
	suite = "test_materials"
	_check_shader(SURFACE, SURFACE_UNIFORMS)
	_check_shader(HINT, HINT_UNIFORMS)
	_check_materials()
	_check_imports()
	_check_material_room()
	_check_hint_scene()
	_check_normal_maps()
	completed = true

# --- shader source and uniform list ---------------------------------------------------------------

func _check_shader(path: String, expected: Dictionary) -> void:
	var name := path.get_file()
	var src := FileAccess.get_file_as_string(path)
	check("%s: source readable" % name, src != "", {"bytes": src.length()})
	var parsed := _parse_uniforms(src)
	check("%s: declared uniforms (source)" % name, _sorted(parsed.keys()) == _sorted(expected.keys()),
		{"declared": _sorted(parsed.keys())})
	for u in expected:
		var e: Array = expected[u]
		var got: Dictionary = parsed.get(u, {})
		var row := {"type": got.get("type"), "hints": got.get("hints"), "default": got.get("default"),
			"group": got.get("group"), "line": got.get("line")}
		check("%s: %s %s : %s = %s [group %s] (source)" % [name, e[0], u, ", ".join(e[1]), e[2], e[3]],
			got.get("type") == e[0] and got.get("hints") == e[1] and got.get("default") == e[2] and got.get("group") == e[3], row)

	var shader: Shader = load(path)
	var list := shader.get_shader_uniform_list()
	var api := {}
	for entry in list:
		api[entry.name] = entry
	check("%s: get_shader_uniform_list names match the source" % name, _sorted(api.keys()) == _sorted(expected.keys()),
		{"names": _sorted(api.keys())})
	for u in expected:
		var e: Array = expected[u]
		var entry: Dictionary = api.get(u, {})
		var ok: bool = entry.get("type") == VARIANT_TYPE[e[0]]
		if e[0] == "sampler2D":
			ok = ok and entry.get("hint") == PROPERTY_HINT_RESOURCE_TYPE and entry.get("hint_string") == "Texture2D"
		for h in e[1]:
			if h.begins_with("hint_range("):
				var lim: PackedStringArray = h.trim_prefix("hint_range(").trim_suffix(")").split(",")
				var api_lim: PackedStringArray = str(entry.get("hint_string", "")).split(",")
				ok = ok and entry.get("hint") == PROPERTY_HINT_RANGE and api_lim.size() >= 2 \
					and is_equal_approx(api_lim[0].to_float(), lim[0].to_float()) and is_equal_approx(api_lim[1].to_float(), lim[1].to_float())
		check("%s: %s in uniform list" % [name, u], ok,
			{"type": entry.get("type"), "hint": entry.get("hint"), "hint_string": entry.get("hint_string")})
	# Groups as the API reports them, against group_uniforms in the source.
	var api_groups := {}
	var current := ""
	for entry in shader.get_shader_uniform_list(true):
		if entry.usage & PROPERTY_USAGE_GROUP:
			current = entry.name
		elif entry.usage & PROPERTY_USAGE_SUBGROUP:
			pass
		else:
			api_groups[entry.name] = current
	var src_groups := {}
	for u in parsed:
		src_groups[u] = parsed[u].group
	check("%s: uniform groups (get_shader_uniform_list(true)) match group_uniforms" % name, api_groups == src_groups,
		{"api": api_groups})

## Parses `uniform <type> <name> [: hints] [= default];` lines and the group_uniforms in force for each.
func _parse_uniforms(src: String) -> Dictionary:
	var re_uniform := RegEx.create_from_string("^uniform\\s+(\\w+)\\s+(\\w+)\\s*(?::\\s*([^=;]*?))?\\s*(?:=\\s*([^;]*?))?\\s*;")
	var re_group := RegEx.create_from_string("^group_uniforms\\s*(\\w*)\\s*;")
	var out := {}
	var group := ""
	var lines := src.split("\n")
	for i in lines.size():
		var line := lines[i].strip_edges()
		var g := re_group.search(line)
		if g:
			group = g.get_string(1)
			continue
		var m := re_uniform.search(line)
		if m == null:
			continue
		out[m.get_string(2)] = {"type": m.get_string(1), "hints": _split_hints(m.get_string(3)),
			"default": m.get_string(4).replace(" ", ""), "group": group, "line": i + 1}
	return out

## Splits a hint list at top-level commas, so hint_range(a, b) stays one hint.
func _split_hints(s: String) -> Array:
	var out := []
	var depth := 0
	var cur := ""
	for c in s:
		if c == "(":
			depth += 1
		elif c == ")":
			depth -= 1
		if c == "," and depth == 0:
			out.append(cur.replace(" ", ""))
			cur = ""
		else:
			cur += c
	if cur.strip_edges() != "":
		out.append(cur.replace(" ", ""))
	return out

# --- materials ------------------------------------------------------------------------------------

func _check_materials() -> void:
	var re_param := RegEx.create_from_string("(?m)^shader_parameter/(\\w+)\\s*=")
	for path in MATERIALS:
		var name: String = path.get_file()
		var shader_path: String = MATERIALS[path][0]
		var want: Dictionary = MATERIALS[path][1]
		var mat = load(path)
		check("%s: is a ShaderMaterial" % name, mat is ShaderMaterial, {"class": mat.get_class() if mat else null})
		if not mat is ShaderMaterial:
			continue
		check("%s: shader is %s" % [name, shader_path], mat.shader != null and mat.shader.resource_path == shader_path,
			{"shader": mat.shader.resource_path if mat.shader else null})
		# The parameters written in the file: each one declared, and every declared uniform set.
		var written := []
		for m in re_param.search_all(FileAccess.get_file_as_string(path)):
			written.append(m.get_string(1))
		check("%s: sets exactly the declared uniforms" % name, _sorted(written) == _sorted(want.keys()), {"written": _sorted(written)})
		for k in want:
			var v = mat.get_shader_parameter(k)
			var e = want[k]
			var ok := false
			var seen = v
			if e is String:
				var tex_path: String = e if e.begins_with("res://") else TEX % e
				ok = v is Texture2D and v.resource_path == tex_path
				seen = v.resource_path if v is Resource else v
				e = tex_path
			elif e is Color:
				ok = v is Color and v.is_equal_approx(e)
			elif e is float:
				ok = (v is float or v is int) and is_equal_approx(float(v), e)
			else:
				ok = v == e
			check("%s: %s = %s" % [name, k, e], ok, {"value": str(seen)})
		if shader_path == SURFACE:
			var lo: float = mat.get_shader_parameter("roughness_min")
			var hi: float = mat.get_shader_parameter("roughness_max")
			check("%s: 0 <= roughness_min <= roughness_max <= 1 (brief's validation rule)" % name,
				0.0 <= lo and lo <= hi and hi <= 1.0, {"min": lo, "max": hi})
	var floor_mat: ShaderMaterial = load(FLOOR)
	var standin_mat: ShaderMaterial = load(STANDIN)
	check("both surface materials reference the same shader path",
		floor_mat.shader.resource_path == standin_mat.shader.resource_path and floor_mat.shader.resource_path == SURFACE,
		{"floor": floor_mat.shader.resource_path, "standin": standin_mat.shader.resource_path})
	check("both surface materials share one Shader resource instance", floor_mat.shader == standin_mat.shader, {})
	check("the two surface materials are distinct resources", floor_mat != standin_mat, {})
	# In memory only, never saved: a parameter change on one material leaves the other unchanged.
	floor_mat.set_shader_parameter("uv_scale", 3.0)
	var other = standin_mat.get_shader_parameter("uv_scale")
	floor_mat.set_shader_parameter("uv_scale", 2.0)
	check("changing floor uv_scale in memory leaves the stand-in at 1.0", is_equal_approx(float(other), 1.0), {"standin": other})

# --- imports --------------------------------------------------------------------------------------

func _check_imports() -> void:
	for key in IMPORTS:
		var res_path: String = HINT_PNG if key == "hint" else TEX % key
		var name := res_path.get_file()
		var e: Array = IMPORTS[key]
		var cfg := ConfigFile.new()
		var err := cfg.load(res_path + ".import")
		check("%s.import: readable with ConfigFile" % name, err == OK, {"error": error_string(err)})
		var got := {
			"compress/mode": cfg.get_value("params", "compress/mode", null),
			"compress/normal_map": cfg.get_value("params", "compress/normal_map", null),
			"mipmaps/generate": cfg.get_value("params", "mipmaps/generate", null),
		}
		check("%s.import: compress/mode=%d compress/normal_map=%d mipmaps/generate=%s" % [name, e[0], e[1], e[2]],
			got["compress/mode"] == e[0] and got["compress/normal_map"] == e[1] and got["mipmaps/generate"] == e[2], got)
		var extra := {
			"importer": cfg.get_value("remap", "importer", null),
			"process/normal_map_invert_y": cfg.get_value("params", "process/normal_map_invert_y", null),
			"detect_3d/compress_to": cfg.get_value("params", "detect_3d/compress_to", null),
			"roughness/mode": cfg.get_value("params", "roughness/mode", null),
		}
		check("%s.import: texture importer, no Y flip, no 3D auto-compress, no roughness baking" % name,
			extra.importer == "texture" and extra["process/normal_map_invert_y"] == false
			and extra["detect_3d/compress_to"] == 0 and extra["roughness/mode"] == 1, extra)
		var tex: Texture2D = load(res_path)
		var img: Image = tex.get_image() if tex else null
		var info := {"class": tex.get_class() if tex else null}
		if img:
			info.merge({"size": "%dx%d" % [img.get_width(), img.get_height()], "format": img.get_format(),
				"mipmaps": img.has_mipmaps(), "compressed": img.is_compressed()})
		check("%s: imported image format %d, mipmaps %s, uncompressed" % [name, e[3], e[2]],
			img != null and img.get_format() == e[3] and img.has_mipmaps() == e[2] and not img.is_compressed(), info)

# --- scenes ---------------------------------------------------------------------------------------

func _check_material_room() -> void:
	var room: Node = (load(ROOM) as PackedScene).instantiate()
	print("material_room: AMBIENT_SOURCE_BG=%d DISABLED=%d COLOR=%d SKY=%d" % [Environment.AMBIENT_SOURCE_BG,
		Environment.AMBIENT_SOURCE_DISABLED, Environment.AMBIENT_SOURCE_COLOR, Environment.AMBIENT_SOURCE_SKY])
	var floor_mesh: MeshInstance3D = room.get_node("Floor/Mesh")
	var standin_mesh: MeshInstance3D = room.get_node("StandIn/Mesh")
	check("material_room: Floor/Mesh material_override is %s" % FLOOR.get_file(),
		floor_mesh.material_override != null and floor_mesh.material_override.resource_path == FLOOR,
		{"path": floor_mesh.material_override.resource_path if floor_mesh.material_override else null})
	check("material_room: StandIn/Mesh material_override is %s" % STANDIN.get_file(),
		standin_mesh.material_override != null and standin_mesh.material_override.resource_path == STANDIN,
		{"path": standin_mesh.material_override.resource_path if standin_mesh.material_override else null})
	check("material_room: the two meshes hold distinct materials", floor_mesh.material_override != standin_mesh.material_override, {})
	check("material_room: floor mesh is BoxMesh 8 x 0.2 x 8, stand-in is CapsuleMesh r 0.25 h 1.2",
		floor_mesh.mesh is BoxMesh and floor_mesh.mesh.size.is_equal_approx(Vector3(8, 0.2, 8))
		and standin_mesh.mesh is CapsuleMesh and is_equal_approx(standin_mesh.mesh.radius, 0.25) and is_equal_approx(standin_mesh.mesh.height, 1.2),
		{"floor": floor_mesh.mesh.get_class(), "standin": standin_mesh.mesh.get_class()})
	# The A3 room keeps its own StandardMaterial3D overrides (the A5 scene only overrides them).
	var a3: Node = (load(A3_ROOM) as PackedScene).instantiate()
	check("lantern_gate_room (A3): Floor and StandIn still use StandardMaterial3D",
		a3.get_node("Floor/Mesh").material_override is StandardMaterial3D and a3.get_node("StandIn/Mesh").material_override is StandardMaterial3D, {})
	a3.free()

	var env: Environment = (room.get_node("WorldEnvironment") as WorldEnvironment).environment
	var env_expected := {
		"background_mode": Environment.BG_COLOR, "background_color": Color(0.035, 0.045, 0.09, 1),
		# Finding: lantern_gate_room.tscn:11 stores 3, which is AMBIENT_SOURCE_SKY (COLOR is 2), with no Sky
		# resource and sky contribution 1, so ambient_light_color below may not be what lights the room.
		"ambient_light_source": Environment.AMBIENT_SOURCE_SKY, "sky": null, "ambient_light_sky_contribution": 1.0,
		"ambient_light_color": Color(0.18, 0.22, 0.38, 1),
		"ambient_light_energy": 0.8, "reflected_light_source": Environment.REFLECTION_SOURCE_BG,
		"tonemap_mode": Environment.TONE_MAPPER_LINEAR, "tonemap_exposure": 1.0,
		"glow_enabled": false, "fog_enabled": false, "volumetric_fog_enabled": false, "adjustment_enabled": false,
	}
	for k in env_expected:
		var v = env.get(k)
		var e = env_expected[k]
		var ok: bool = v.is_equal_approx(e) if e is Color else (is_equal_approx(v, e) if e is float else v == e)
		check("material_room environment: %s = %s" % [k, e], ok, {"value": str(v)})
	check("material_room: no CameraAttributes on WorldEnvironment or Camera3D",
		room.get_node("WorldEnvironment").camera_attributes == null and room.get_node("Camera3D").attributes == null, {})
	var lights := {
		"Moon": [DirectionalLight3D, Color(0.55, 0.65, 1, 1), 1.2, 0.0],
		"LanternLight": [OmniLight3D, Color(1, 0.34, 0.08, 1), 5.0, 4.0],
		"OilShrine/ShrineLight": [OmniLight3D, Color(1, 0.25, 0.04, 1), 3.0, 2.5],
	}
	var found := []
	for n in room.find_children("*", "Light3D", true, false):
		found.append(str(room.get_path_to(n)))
	check("material_room: exactly three lights (Moon, LanternLight, OilShrine/ShrineLight)", _sorted(found) == _sorted(lights.keys()), {"lights": found})
	for p in lights:
		var l: Light3D = room.get_node_or_null(p)
		var e: Array = lights[p]
		var row := {}
		var ok := l != null and is_instance_of(l, e[0])
		if ok:
			row = {"color": l.light_color, "energy": l.light_energy, "shadow": l.shadow_enabled}
			ok = l.light_color.is_equal_approx(e[1]) and is_equal_approx(l.light_energy, e[2]) and not l.shadow_enabled
			if l is OmniLight3D:
				row["range"] = l.omni_range
				ok = ok and is_equal_approx(l.omni_range, e[3])
		check("material_room light %s: colour %s, energy %s, range %s, shadows off" % [p, e[1], e[2], e[3]], ok, row)

	# Floor UVs: PrimitiveMesh arrays build without a renderer.
	var box := _face_uv_span(floor_mesh.mesh, Vector3.UP)
	check("finding: BoxMesh top face spans 1/3 x 1/2 of UV space, so stones stretch 1.5:1 (x vs z)",
		is_equal_approx(box.du, 1.0 / 3.0) and is_equal_approx(box.dv, 0.5), box)
	for m in [floor_mesh, standin_mesh]:
		var arrays: Array = m.mesh.get_mesh_arrays()
		var tangents = arrays[Mesh.ARRAY_TANGENT]
		check("%s mesh has tangents for NORMAL_MAP" % m.get_parent().name, tangents != null and tangents.size() > 0,
			{"tangent_floats": tangents.size() if tangents != null else 0})
	room.free()

func _check_hint_scene() -> void:
	var scene: Node = (load(HINT_SCENE) as PackedScene).instantiate()
	var with_quad: MeshInstance3D = scene.get_node("QuadWithSourceColor")
	var without_quad: MeshInstance3D = scene.get_node("QuadWithoutHint")
	check("hint_experiment: QuadWithSourceColor uses %s" % HINT_WITH.get_file(),
		with_quad.material_override != null and with_quad.material_override.resource_path == HINT_WITH, {})
	check("hint_experiment: QuadWithoutHint uses %s" % HINT_WITHOUT.get_file(),
		without_quad.material_override != null and without_quad.material_override.resource_path == HINT_WITHOUT, {})
	var env: Environment = (scene.get_node("WorldEnvironment") as WorldEnvironment).environment
	check("hint_experiment environment: black background, Linear tonemap, exposure 1, no glow/fog/adjustments",
		env.background_mode == Environment.BG_COLOR and env.background_color.is_equal_approx(Color(0, 0, 0, 1))
		and env.tonemap_mode == Environment.TONE_MAPPER_LINEAR and is_equal_approx(env.tonemap_exposure, 1.0)
		and not env.glow_enabled and not env.fog_enabled and not env.adjustment_enabled, _env_row(env))
	var cam: Camera3D = scene.get_node("Camera3D")
	check("hint_experiment: orthographic camera, size 4.5, no CameraAttributes, no lights",
		cam.projection == Camera3D.PROJECTION_ORTHOGONAL and is_equal_approx(cam.size, 4.5) and cam.attributes == null
		and scene.get_node("WorldEnvironment").camera_attributes == null and scene.find_children("*", "Light3D", true, false).is_empty(),
		{"projection": cam.projection, "size": cam.size})
	scene.free()

func _env_row(env: Environment) -> Dictionary:
	return {"background_mode": env.background_mode, "background_color": env.background_color,
		"ambient_source": env.ambient_light_source, "ambient_color": env.ambient_light_color, "ambient_energy": env.ambient_light_energy,
		"reflected_source": env.reflected_light_source, "tonemap_mode": env.tonemap_mode, "exposure": env.tonemap_exposure,
		"glow": env.glow_enabled, "fog": env.fog_enabled, "adjustment": env.adjustment_enabled}

## UV extent of the faces whose normal is `normal`, with their size in metres.
func _face_uv_span(mesh: PrimitiveMesh, normal: Vector3) -> Dictionary:
	var arrays := mesh.get_mesh_arrays()
	var verts: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
	var norms: PackedVector3Array = arrays[Mesh.ARRAY_NORMAL]
	var uvs: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV]
	var umin := INF; var umax := -INF; var vmin := INF; var vmax := -INF
	var xmin := INF; var xmax := -INF; var zmin := INF; var zmax := -INF
	var seen := {}
	for i in verts.size():
		seen[str(norms[i].snappedf(0.001))] = true
		if norms[i].dot(normal) > 0.999:
			umin = minf(umin, uvs[i].x); umax = maxf(umax, uvs[i].x)
			vmin = minf(vmin, uvs[i].y); vmax = maxf(vmax, uvs[i].y)
			xmin = minf(xmin, verts[i].x); xmax = maxf(xmax, verts[i].x)
			zmin = minf(zmin, verts[i].z); zmax = maxf(zmax, verts[i].z)
	return {"normals_seen": seen.keys(), "u": [umin, umax], "v": [vmin, vmax], "du": umax - umin, "dv": vmax - vmin,
		"metres_x": xmax - xmin, "metres_z": zmax - zmin,
		"metres_per_texture_x": (xmax - xmin) / maxf(umax - umin, 1e-9), "metres_per_texture_z": (zmax - zmin) / maxf(vmax - vmin, 1e-9)}

# --- normal maps ----------------------------------------------------------------------------------

func _check_normal_maps() -> void:
	for m in ["nor_gl", "nor_dx"]:
		var path: String = TEX % m
		var img := Image.load_from_file(ProjectSettings.globalize_path(path))
		check("%s: source PNG decodes" % path.get_file(), img != null and not img.is_empty(),
			{"size": "%dx%d" % [img.get_width(), img.get_height()] if img else "null"})
		if img == null or img.is_empty():
			continue
		var gl := NormalMapCheck.curl_ratio(img, false)
		var dx := NormalMapCheck.curl_ratio(img, true)
		print("curl_ratio %s: directx=false %.4f, directx=true %.4f" % [path.get_file(), gl, dx])
		if m == "nor_gl":
			check("nor_gl reads as the GL convention (directx=false < %.1f < directx=true)" % CURL_THRESHOLD,
				gl < CURL_THRESHOLD and dx > CURL_THRESHOLD, {"directx_false": gl, "directx_true": dx})
		else:
			check("nor_dx control reads as DirectX (directx=true < %.1f < directx=false)" % CURL_THRESHOLD,
				dx < CURL_THRESHOLD and gl > CURL_THRESHOLD, {"directx_false": gl, "directx_true": dx})
	var bound := []
	for path in [FLOOR, STANDIN]:
		bound.append((load(path) as ShaderMaterial).get_shader_parameter("normal_tex").resource_path)
	check("every material binds nor_gl, never nor_dx, to normal_tex", bound.all(func(p): return p == TEX % "nor_gl"), {"bound": bound})

func _sorted(a: Array) -> Array:
	var b := a.duplicate()
	b.sort()
	return b
