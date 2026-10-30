# A5 materials audit

Audited 30 October 2026 by Claude Code against `CHANGE-BRIEF.md`; no shader, material, scene or `.import`
file was changed. `godot/tests/test_materials.gd` pins every table below
(`./scripts/run-test.sh test_materials.gd 60`). Renderer: `gl_compatibility` (`project.godot:26-27`).

## Materials

| Material | Shader | Uniform values set | Textures bound |
|---|---|---|---|
| `res://a5/materials/cobblestone_warm_floor.tres` (Material A, Floor/Mesh) | `res://shaders/cobblestone_surface.gdshader` | `tint = Color(1, 0.92, 0.8, 1)`, `uv_scale = 2.0`, `roughness_min = 0.55`, `roughness_max = 0.95`, `normal_strength = 1.0` (`:14-18`) | `color_tex` = `cobblestone_floor_08_diff_1k.png`, `normal_tex` = `cobblestone_floor_08_nor_gl_1k.png`, `roughness_tex` = `cobblestone_floor_08_rough_1k.png` (`:11-13`) |
| `res://a5/materials/cobblestone_cool_standin.tres` (Material B, StandIn/Mesh) | `res://shaders/cobblestone_surface.gdshader` | `tint = Color(0.72, 0.85, 1, 1)`, `uv_scale = 1.0`, `roughness_min = 0.2`, `roughness_max = 0.55`, `normal_strength = 0.5` (`:14-18`) | same three textures as Material A (`:11-13`) |
| `res://a5/hint_experiment/hint_with_source_color.tres` (QuadWithSourceColor) | `res://shaders/hint_experiment.gdshader` | `use_color = true` (`:11`) | `color_sample` and `raw_sample` = `res://a5/hint_experiment/hint_greys_3x1.png` (`:9-10`) |
| `res://a5/hint_experiment/hint_without_source_color.tres` (QuadWithoutHint) | `res://shaders/hint_experiment.gdshader` | `use_color = false` (`:11`) | `color_sample` and `raw_sample` = `hint_greys_3x1.png` (`:9-10`) |

The cobblestone textures sit in `res://assets/textures/cobblestone_floor_08/`. Every material sets every uniform
its shader declares and nothing else, so no value falls back to a shader default. Both surface materials load the
same Shader instance and are distinct resources. A change to one material's `uv_scale` made in memory leaves the
other unchanged.

Shader defaults, from the source: `tint = vec4(1.0, 1.0, 1.0, 1.0)`, `uv_scale = 1.0`, `roughness_min = 0.2`,
`roughness_max = 0.8`, `normal_strength = 1.0` (`cobblestone_surface.gdshader:8-14`), and `use_color = true`
(`hint_experiment.gdshader:7`). `tint` and `uv_scale` are in group `Surface`; the three Response uniforms are in
group `Response`; the samplers are ungrouped. `get_shader_uniform_list(true)` reports the same grouping.

Not shown in the table: both scenes also contain Label3D nodes, which use their own default materials.

## Samplers

Import keys come from each texture's `.import` `[params]`. The format column is what `get_image()` returns after import.

| Shader | Sampler (line) | Hints as written | Bound by | Texture | `compress/mode` | `compress/normal_map` | `mipmaps/generate` | Imported format |
|---|---|---|---|---|---:|---:|---|---|
| cobblestone_surface | `color_tex` (`:3`) | `source_color, filter_linear_mipmap, repeat_enable` | Floor, StandIn | `cobblestone_floor_08_diff_1k.png` | 0 | 2 | true | RGB8 1024², mipmaps |
| cobblestone_surface | `normal_tex` (`:4`) | `hint_normal, filter_linear_mipmap, repeat_enable` | Floor, StandIn | `cobblestone_floor_08_nor_gl_1k.png` | 0 | 1 | true | RGB8 1024², mipmaps |
| cobblestone_surface | `roughness_tex` (`:5`) | `filter_linear_mipmap, repeat_enable` | Floor, StandIn | `cobblestone_floor_08_rough_1k.png` | 0 | 2 | true | L8 1024², mipmaps |
| hint_experiment | `color_sample` (`:5`) | `source_color, filter_nearest` | both hint materials | `hint_greys_3x1.png` | 0 | 2 | false | RGB8 3×1, no mipmaps |
| hint_experiment | `raw_sample` (`:6`) | `filter_nearest` | both hint materials | `hint_greys_3x1.png` | 0 | 2 | false | RGB8 3×1, no mipmaps |
| (none) | (none) | (none) | no material | `cobblestone_floor_08_nor_dx_1k.png` (calibration only) | 0 | 1 | true | RGB8 1024², mipmaps |

On every one of these imports: `process/normal_map_invert_y=false`, `detect_3d/compress_to=0` and `roughness/mode=1`.
All of these values match the brief's import table (`CHANGE-BRIEF.md:115-122`) and its sampler hints.

Normal-map convention: `normal_map_check.gd` `curl_ratio` on the source PNGs. The pass threshold is 0.5, set from
this GL/DX pair: about halfway between the right convention's 0.2236 and the no-surface value 1 (see Review):

| Map | `directx = false` | `directx = true` | Reads as |
|---|---:|---:|---|
| `nor_gl` (bound to both materials) | 0.2236 | 1.7764 | GL, as the brief expects |
| `nor_dx` (bound to none) | 1.7764 | 0.2236 | DirectX control |

## Lights and environment that change the look

**`res://a5/material_room.tscn`** inherits `res://a3/lantern_gate_room.tscn` and overrides only the two
`material_override` properties (`material_room.tscn:9-13`). Everything below therefore comes from the A3 room.

| Item | Setting (`lantern_gate_room.tscn`) |
|---|---|
| Environment background | `background_mode = 1` (Color), `background_color = (0.035, 0.045, 0.09)` (`:9-10`) |
| Ambient | `ambient_light_source = 3` (**Sky**, see finding 1), `ambient_light_color = (0.18, 0.22, 0.38)`, `ambient_light_energy = 0.8` (`:11-13`); no Sky resource; `ambient_light_sky_contribution` 1.0 (default) |
| Reflections | `reflected_light_source` 0 (Background, default); no ReflectionProbe |
| Tonemap / exposure | Linear (`tonemap_mode` 0), exposure 1.0. Both are defaults, not written in the file. No CameraAttributes on the WorldEnvironment or the camera |
| Glow, fog, volumetric fog, adjustments | all off (defaults) |
| Moon | DirectionalLight3D, rotation `(-52, -28, 0)`°, colour `(0.55, 0.65, 1)`, energy 1.2, shadows off (`:44-47`) |
| LanternLight | OmniLight3D at `(-2, 2.15, 0)`, colour `(1, 0.34, 0.08)`, energy 5.0, range 4.0, shadows off (`:49-53`) |
| ShrineLight | OmniLight3D under OilShrine, world `(2, 1.25, 0)`, colour `(1, 0.25, 0.04)`, energy 3.0, range 2.5, shadows off (`:94-98`) |
| Camera3D | saved at `(5.8, 3.8, 7.6)` (`:56`). `lantern_gate_room.gd:23-30` aims it at `(0, 1.15, 0)` on `_ready` and lets Q/E/R/F/Z/X move it. It hides the floor mesh whenever the camera is below y = 0 (`:54`) |
| Meshes | Floor: BoxMesh 8 × 0.2 × 8. StandIn: CapsuleMesh r 0.25, h 1.2. Both generate tangents |

**`res://a5/hint_experiment/hint_experiment.tscn`**: Environment with `background_mode = 1` only (`:6-7`). Loaded,
it gives a black background, Linear tonemapping, exposure 1.0 and no glow, fog or adjustments; all of these except
the background mode are engine defaults. The camera is orthographic, size 4.5, at z = 5. The scene has no lights;
both quads are unshaded (`hint_experiment.gdshader:2`).

## Findings

1. **The material room's ambient source is Sky, with no sky.** `lantern_gate_room.tscn:11` stores
   `ambient_light_source = 3`. In Godot 4.7, `AMBIENT_SOURCE_COLOR` is 2 and `AMBIENT_SOURCE_SKY` is 3 (the test
   prints the enum). The Environment has no `sky`, and `ambient_light_sky_contribution` is 1.0. Godot documents
   that `ambient_light_color` is only effective when the sky contribution is below 1.0, so the bluish ambient
   at `:12-13` probably does not light the cobblestones as written. This line has been in the A3 file since
   `e3c214f` (13 October). It is out of scope here, and I have not measured its rendered effect.
   *Measured 30 October (`captures/a5-materials/20261030-131416-ambient/`): with the source as loaded (Sky, no
   sky) and with Color the floor and stand-in means are identical; Disabled, or energy 0, darkens both; energy 2
   brightens both. So under Compatibility the Sky source without a sky still applies `ambient_light_color` and
   energy, and this finding's "probably does not light" is wrong. Kept unchanged, as Bao decided.*
2. **The floor's UVs stretch the stones and do not repeat them.** The BoxMesh top face uses u 1/3–2/3 and
   v 0.5–1 (measured from `get_mesh_arrays()`). So one texture repeat covers 24 m in x and 16 m in z at
   `uv_scale` 1, or 12 m × 8 m at the floor's `uv_scale` 2. The stones are stretched 1.5:1 along x, and the
   8 m floor shows only 2/3 × 1 of one tile. The brief's "warm, repeated, matte paving" (`CHANGE-BRIEF.md:134`)
   does not hold on this mesh. `uv = UV * uv_scale` (`cobblestone_surface.gdshader:18`) assumes UVs that span
   the face. *Resolved 30 October (Bao): the A5 scene overrides the floor mesh with an 8 x 8 PlaneMesh at
   y = 0; the A3 room keeps its BoxMesh (`CHANGE-BRIEF.md` revision).*
3. **The roughness range rule is not enforced.** `CHANGE-BRIEF.md:132` asks for
   `0 ≤ roughness_min ≤ roughness_max ≤ 1` "in configuration/driver validation".
   `build_a5_materials.gd:13-22,36-44` writes the values without checking them, and no runtime driver exists.
   The current values satisfy the rule; `test_materials.gd` now checks it.
4. **A build-script comment claims UIDs that the files do not have.** `build_a5_materials.gd:3` says "Saves
   through ResourceSaver so Godot writes every UID". However, none of the four `.tres` files or two `.tscn` files
   has a `uid=` in its header or on its `ext_resource` lines (for example `cobblestone_warm_floor.tres:1-6`,
   `material_room.tscn:1-5`). References are by path only, so moving a texture or material breaks them. Not
   inventing UIDs was right; the comment is wrong.
5. **The import settings were set by a script, not in the editor.** Godot generated the `.import` files.
   `tools/a5/set_texture_imports.py` then rewrote their existing `[params]` keys (`ATTRIBUTION.md:19`, commit
   `dc5c53a`). `CHANGE-BRIEF.md:122` says "Create imports through Godot's editor and set these keys explicitly".
   The resulting values match the brief; the route differs from it.
6. **The DirectX map is imported but never used at runtime.** `nor_dx` is imported as a 1K lossless texture with
   mipmaps, but no material binds it. The calibration script (`calibrate_normal_map_check.gd:9`) and this test
   both decode the source PNG with `Image.load_from_file`. The import follows the brief's table
   (`CHANGE-BRIEF.md:120`), but its imported copy serves no purpose and would ship in an export.
7. **Lossless import keeps the textures uncompressed in VRAM.** `get_image()` reports RGB8 for `diff` and
   `nor_gl` and L8 for `rough`, uncompressed with mipmaps. What the GPU allocates was not measured. This is the
   brief's choice (`CHANGE-BRIEF.md:115-120`), so it is a cost note rather than a defect.
8. **The brief's download sizes are in MiB but labelled MB.** The actual files total 6,831,262 bytes, which is
   6.83 MB or 6.51 MiB (`ATTRIBUTION.md:14-17`). The brief says "about 6.5 MB", with 2.0 MB for each normal map
   (`CHANGE-BRIEF.md:113`); each is 2.13 MB.
9. **Each hint material binds one sampler it never reads.** Both hint materials bind the PNG to both samplers,
   but `use_color` selects only one of them (`hint_experiment.gdshader:10-14`). This is what the brief asks for
   (`:95`) and costs one 3×1 texture.
10. **The hint scene's capture conditions rely on engine defaults.** Linear tonemapping, exposure 1 and glow, fog
    and adjustments off are not written in `hint_experiment.tscn:6-7`; they are engine defaults. The build script
    set them explicitly (`build_a5_materials.gd:100-104`), but default values are not serialised. The test pins
    the loaded values, so a change of default would show up.
11. **The brief asks for A3 lights in a scene that cannot use them.** `CHANGE-BRIEF.md:74` says the hint
    experiment is captured "under the fixed A3 lights". The hint scene has no lights, and its shader is
    `unshaded`, so lights could not change it. This inconsistency is in the brief, not in the scene.
12. **The StandIn loses its A3 emission.** The A3 StandIn material was orange with emission
    (`lantern_gate_room.tscn:29-32`); Material B has none. Together with finding 1 and the colour background as
    the reflection source, the StandIn's "stronger specular response" (`CHANGE-BRIEF.md:134`) can only appear as
    highlights from the Moon and the lantern, plus a flat dark-blue reflection. No light casts shadows. Only a
    rendered capture can show how this reads.

## Attribution

Texture: [Cobblestone Floor 08](https://polyhaven.com/a/cobblestone_floor_08), by Rob Tuytel, Poly Haven. The
asset page names the author and links CC0. The [Poly Haven asset license](https://polyhaven.com/license) was opened
and checked on 30 October 2026: assets are CC0, permitting use, modification and redistribution, including
commercial use; attribution is appreciated but not required. This license check covers the texture assets, not
unrelated website content.

## What the headless test cannot establish

A headless run draws nothing. So the test cannot show any of these:

- any colour, brightness or tint on screen;
- whether the stones read as raised (the brief's grazing-light check);
- what the Sky ambient source actually does to the room (finding 1);
- how visible the UV stretch is (finding 2);
- whether the Compatibility renderer shows 64/128/192 with and without `source_color`;
- the roughness and `uv_scale` sweeps;
- what the GPU actually allocates for the textures.

`curl_ratio` checks the source PNG's slope field, not the imported texture as the shader samples it. Hint strings
and defaults are read from the source text, because `get_shader_uniform_list()` reports samplers only as
`Texture2D` resource hints and does not report defaults.

## Review (30 October 2026)

Reviewed in the main Claude Code session after the agent's audit was committed unedited (`52ee2db`), for Bao:
- Integer enums looked up: `compress/mode` and `compress/normal_map` against Godot 4.7.2-stable
  `resource_importer_texture.cpp` (Lossless 0; Detect 0, Enable 1, Disabled 2); `ambient_light_source` from the
  test's own print (`BG=0 DISABLED=1 COLOR=2 SKY=3`); tonemap, background and reflection checks compare against the
  engine constants. Formats are the ones `get_image().get_format()` returned (RGB8 = 4, L8 = 0).
- Removed: the unmeasured VRAM estimate in finding 7.
- Changed: the curl threshold from 1.0 to 0.5. At 1.0 a map with no surface behind it (ratio near 1) could pass.
- Corrected in `build_a5_materials.gd:3`: the comment claimed Godot writes every UID (finding 4).
- Findings 5, 8 and 11 are recorded as a dated revision in `CHANGE-BRIEF.md`. Findings 1 (ambient source Sky) and 2
  (floor UV stretch) change the look and are Bao's decisions; nothing was changed for them in this review.

