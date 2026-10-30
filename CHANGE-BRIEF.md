# Lanternfall — Shader and Material Change Brief

Date: 30 October 2026. This brief defines the intended behaviour and numerical predictions. Rendered checks and the Use It experiment remain to be performed; predictions below are not measured results.

Provenance: Bao's brief, moved on 30 October 2026 from the working copy `~/Documents/ChatGPT/csye 7280/assignment-5`. Claude Code re-pointed the project-fact line references to this repository and wrote the parts marked † from Bao's decisions in chat (idle-frame pixels, hold under a tree pause, the numeric curl check) and from the design below (tolerance, time scale, evidence split). In that working copy Codex wrote a first `hurt_tint.gdshader` at Bao's request on 29 October; Bao reports writing the yellow version by hand afterwards (saved 30 October 11:46, before this brief was committed). See FRICTIONAL.md.

## Project facts

Paths below are relative to this project folder.

- `godot/project.godot:26–27` selects `gl_compatibility` for desktop and mobile. The 2D canvas uses nearest filtering (`:28`). † `rendering/viewport/hdr_2d` is not set, so 2D blending is not done in linear space.
- `godot/features/tuning.gd:4,14` defines 60 simulation ticks per second and 48 invulnerability ticks: 48 / 60 = 0.8 seconds of active simulation.
- `godot/features/player/player.gd:94–104` rejects hits while `iframes > 0`, then assigns 48 on an accepted hit, including a lethal hit.
- `godot/features/player/player.gd:44` clears `iframes` on reset. `:68–69` decrements it in `step()`; `:74–75` applies the existing red/white blink, alternating every four ticks. The empowered branch can apply a separate warm modulation.
- `godot/game/session.gd:111–115,121–129` runs player steps only in PLAYING. PAUSED, LEVELUP, WON and LOST freeze the counter. This is a simulation gate; the game does not pause the whole SceneTree or change `Engine.time_scale`.
- `godot/features/player/player.gd:118–124` defines the fallback palette: lamp head `#F2B84B`, coat `#2E3A59`, brown `#8A5A3C`, outline `#14121C`. The controlled calculations use the first two opaque colours with no 2D lighting. † In play the player draws `godot/assets/art/pc_sheet.png` (`player.gd:106–110`); the fallback runs only without that texture. The sheet's `idle` and `hurt` frames use the same four opaque colours (measured from the PNG).
- `godot/a3/lantern_gate_room.tscn:63–66,112–114` assigns the Floor and StandIn mesh materials. Those two overrides may be replaced. The three GLB props, their material names, geometry and collisions remain unchanged because the A3 checks depend on them.

## State and purpose

The courier turns yellow after an accepted hit, then gradually returns to its incoming colour as protection expires. This communicates temporary invulnerability and gives the player a visible warning that the next collision will soon cause damage again. It confirms an actual damage event rather than merely proximity to an enemy. The existing red blink continues to signal the hit; the yellow tint shows the remaining protection.

This is presentation only. The driver reads game state and `iframes`; it never writes health, damage, collision, movement, progression, audio or simulation timing. Do not edit `player.gd`.

## 2D shader design

File: `godot/shaders/hurt_tint.gdshader`. Use `shader_type canvas_item;` and `render_mode unshaded;`. The yellow target matches the shader currently saved in the repository.

| Uniform | Type | Hint | Default | Purpose |
|---|---|---|---|---|
| `hurt_amount` | float | `hint_range(0.0, 1.0)` | `0.0` | Remaining protection fraction, set by the presentation driver |
| `hurt_color` | vec4 | `source_color` | `vec4(1.0, 1.0, 0.0, 1.0)` | Yellow target, editable in the material Inspector |

Exact colour line inside `fragment()`:

```glsl
COLOR.rgb = mix(COLOR.rgb, hurt_color.rgb, hurt_amount);
```

The equation is `out_rgb = (1 − a) × incoming_rgb + a × target_rgb`. Leave `COLOR.a` unchanged; `hurt_color.a` does not control opacity. At zero the original drawing passes through, at one the opaque sprite is yellow, and intermediate values retain some original colour. Transparent sprite pixels retain zero alpha.

Incoming fragment `COLOR` includes the texture sample, primitive colour, `modulate` and `self_modulate`. Mixing this value preserves the influence of the existing blink, progressively reducing its visible difference as `hurt_amount` increases. At one, red and white phases have identical yellow RGB. Multiplying by `texture(TEXTURE, UV)` again would apply the texture twice. Replacing the input with a fresh texture sample would lose modulation and primitive colour. See the [CanvasItem shader reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html).

## Driver and lifecycle rules

- In PLAYING, PAUSED and LEVELUP, set `hurt_amount = clamp(float(player.iframes) / 48.0, 0.0, 1.0)`. Read after the session's simulation work so the rendered value reflects the latest counter. On a state change, refresh the value before the next draw.
- There is no independent fade timer or shader `TIME` animation. The decreasing counter itself supplies the fade. An accepted hit begins at one; zero remaining ticks means zero tint. The active window is 48 ticks, subject to the sample position within a tick/frame.
- Hits during protection are ignored by `take_hit()`. They neither restart nor extend the effect. Once protection ends, the next accepted hit starts a new 48-tick window. There is no separate tail during which retrigger policy could differ.
- PAUSED and LEVELUP hold the current value and blink phase because the simulation counter and player step are frozen. Resume continues from that counter. The driver can keep processing while simulation is stopped.
- In MENU, WON and LOST, force `hurt_amount = 0.0`. In particular, a lethal hit may leave `iframes = 48` forever in LOST; the terminal-state override prevents permanent yellow protection feedback. The unchanged base modulation may still be visible in a terminal pose.
- On restart, write `0.0` immediately and then resume normal sampling after `player.reset()`. Do not wait for a decrement to clear a stale material parameter.
- Each player receives a distinct ShaderMaterial; the Shader resource may be shared. Do not alter the existing `modulate` blink to compensate for the tint.
- † Duration: an accepted hit takes `hurt_amount` from 1 to 0 over 48 simulation ticks, 0.8 s of game time, within one frame period of the sampling rate (1/30, 1/60 or 1/144 s), and the same game time at 30, 60 and 144 fps.
- † Time scale: the duration is defined in simulation ticks, the game's own clock, and no presentation timer adds to it. The game never changes `Engine.time_scale`; the driver test sets 0.5 and records ticks, scaled game time and real time, so the report states which one the 0.8 s follows in Godot 4.7.
- † Tree pause (Bao's choice, 30 October): while `get_tree().paused` is true the driver pauses with the tree and `hurt_amount` holds its last value, as in the PAUSED state. The game never pauses the tree; the driver test does it to check the rule.

## † Evidence split

| Rule | Evidence | How |
|---|---|---|
| Uniform names and types; no sampler uniforms | Headless | `get_shader_uniform_list()`; defaults read from the shader source text |
| Shader parses | Headless | Non-empty uniform list and no `SHADER ERROR` line; the semicolon mutation exits 1 |
| 1 on an accepted hit, 0 after 48 ticks, 0.8 s within one frame period at 30/60/144 fps | Headless | Real enemy contact through the game loop; the uniform sampled every frame by a high-`process_priority` node |
| Ignored hits neither restart nor extend | Headless | A second contact during protection leaves the sampled curve unchanged |
| PAUSED and LEVELUP hold, resume continues | Headless | Enter each state mid-window through real input; compare before, during and after |
| MENU, WON and LOST force 0, including a lethal hit | Headless | Real lethal contact; assert LOST, `iframes == 48` and `hurt_amount == 0` |
| Restart writes 0 | Headless | The restart action mid-window; the first sampled frame reads 0 |
| Time scale and tree pause | Headless | `Engine.time_scale = 0.5` run with ticks, game and real time recorded; `get_tree().paused` mid-window holds the value |
| Each player has its own material | Headless | The player's material is a distinct resource from any other |
| Colours at 0, 0.5 and 1 match the hand table; 2.0 from code | Human (Bao) | In-engine captures from a debug key; named pixels sampled beside the table; the stored 2.0 read back |
| The tint reads in play; boundaries hold | Human (Bao) | Own playtest with several hits |
| Material wiring, sampler hints, import settings | Headless | `test_materials.gd` after a fresh import; the `source_color` mutation exits 1 |
| Normal map is a real surface in the GL convention | Headless | `curl_ratio` under both conventions, calibrated on the GL/DX pair |
| Hint experiment, interface sweep, one shader with two materials | Human (Bao) | Captures under the fixed A3 lights; sampled values beside the predictions |

## Hand calculations

Use an unempowered courier, normal non-HDR Compatibility canvas, nearest filtering, no lights and no extra canvas tint. Values below are RGB in 0–255 display units before integer rounding; divide by 255 for shader values. Both selected pixels have alpha one, so `display = output × 1 + background × 0 = output`. No background-contrast claim is made.

Lamp input: `(242,184,75) / 255`. Coat input: `(46,58,89) / 255`. Target: `(255,255,0) / 255`. For example, the lamp at 0.5 is `0.5 × (242,184,75) + 0.5 × (255,255,0) = (248.5,219.5,37.5)`.

| Pixel | `hurt_amount` | White modulation: incoming → output | Red modulation: incoming → output |
|---|---:|---|---|
| Lamp head | 0 | `(242,184,75)` → `(242,184,75)` | `(242,82.8,33.75)` → `(242,82.8,33.75)` |
| Lamp head | 0.5 | `(242,184,75)` → `(248.5,219.5,37.5)` | `(242,82.8,33.75)` → `(248.5,168.9,16.875)` |
| Lamp head | 1 | `(242,184,75)` → `(255,255,0)` | `(242,82.8,33.75)` → `(255,255,0)` |
| Coat | 0 | `(46,58,89)` → `(46,58,89)` | `(46,26.1,40.05)` → `(46,26.1,40.05)` |
| Coat | 0.5 | `(46,58,89)` → `(150.5,156.5,44.5)` | `(46,26.1,40.05)` → `(150.5,140.55,20.025)` |
| Coat | 1 | `(46,58,89)` → `(255,255,0)` | `(46,26.1,40.05)` → `(255,255,0)` |

The red input multiplies RGB by `(1,0.45,0.45)` before the mix. Zero with red modulation is an isolated shader fixture, not the normal zero-counter gameplay state. † Named pixels (Bao's choice, 30 October): controlled captures use the sheet's `idle` frame (sheet x 32–63), facing right, on the market background: the lamp head at frame texel (20,16), stored `#F2B84B`, and the coat at frame texel (16,24), stored `#2E3A59`. All eight neighbours of each texel share its colour, so a one-texel misplacement still samples the same stored colour. Capture both blink phases separately.

## Source-colour hint experiment

Use a lossless 3 × 1 PNG with opaque grey bands 64, 128 and 192. Bind the same image to two nearest-filtered samplers, one with `source_color` and one without. Use an unshaded spatial shader on two quads, writing the selected sample to `ALBEDO`. Use Linear tonemapping, exposure one, no fog, glow or adjustments. Capture band centres, away from edges.

For the linear-rendering comparison let `s = byte / 255`, `decode(s) = ((s + 0.055) / 1.055)^2.4` for these inputs, and `encode(L) = 1.055 × L^(1/2.4) − 0.055`. The full encode function uses `12.92 × L` when `L ≤ 0.0031308`. Correct colour sampling gives `255 × encode(decode(s))`; unhinted raw data incorrectly used as linear colour gives `255 × encode(s)`.

| Stored grey | Normalized `s` | Decoded linear value | With hint, linear renderer | Without hint, linear renderer |
|---:|---:|---:|---:|---:|
| 64 | 0.250980 | 0.051269 | 64 | 137.21 ≈ 137 |
| 128 | 0.501961 | 0.215861 | 128 | 187.84 ≈ 188 |
| 192 | 0.752941 | 0.527115 | 192 | 225.00 ≈ 225 |

These encode predictions describe Forward+/Mobile's linear colour path. The current project uses Compatibility, whose spatial output is sRGB; do not apply another encode to its already sRGB output. The expected Compatibility control is 64/128/192 with either sampler hint under these conditions. Record the actual renderer and observed pixels during Use It. A lack of difference there does not establish that roughness or normal data should carry `source_color`. Godot documents that the hint is optional in Compatibility but required for colour textures in Forward+/Mobile; see [shading language: source colour](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#using-source-color).

## 3D material plan

Use one new `godot/shaders/cobblestone_surface.gdshader` with `shader_type spatial;` and two separate ShaderMaterials assigned to Floor/Mesh and StandIn/Mesh in an independent A5 presentation scene. Reuse the A3 room lights and camera. Do not rename or edit materials inside the three GLB props, modify collisions, or weaken A3 tests.

Texture: [Cobblestone Floor 08](https://polyhaven.com/a/cobblestone_floor_08), by Rob Tuytel, Poly Haven. The asset page names the author and links CC0. The [Poly Haven asset license](https://polyhaven.com/license) was opened and checked on 30 October 2026: assets are CC0, permitting use, modification and redistribution, including commercial use; attribution is appreciated but not required. Keep this credit and both links with the downloaded maps. This license check covers the texture assets, not unrelated website content.

Use the 1K PNG diffuse (about 1.9 MB), OpenGL normal (2.0 MB), and roughness (0.6 MB) maps for rendering, about 4.5 MB of source downloads. Retain the DirectX normal (2.0 MB) only as a calibration fixture, bringing the four-map download total to about 6.5 MB. These are compressed download sizes, not GPU-memory estimates. No displacement or AO map is needed.

| Map | Sampler hint / role | `compress/mode` | `compress/normal_map` | `mipmaps/generate` |
|---|---|---:|---:|---|
| diff | `source_color`, base colour | 0 (Lossless) | 2 (Disabled) | true |
| nor_gl | `hint_normal`, tangent-space normals; no `source_color` | 0 (Lossless) | 1 (Enabled) | true |
| rough | raw scalar data; no `source_color` | 0 (Lossless) | 2 (Disabled) | true |
| nor_dx | `hint_normal`, calibration only; no `source_color` | 0 (Lossless) | 1 (Enabled) | true |

Create imports through Godot's editor and set these keys explicitly; do not hand-write `.import` files. Use repeat and linear mipmap filtering on the production samplers. The tiny hint PNG uses Lossless, normal mode Disabled, mipmaps false and nearest sampling. Inspect imported values after reimport.

| Group | Uniform | Type / hint | Default | Role |
|---|---|---|---|---|
| Surface | `tint` | vec4 / `source_color` | `(1,1,1,1)` | Multiply diffuse RGB |
| Surface | `uv_scale` | float / `hint_range(0.25,4.0)` | 1.0 | Tile all three maps together |
| Response | `roughness_min` | float / `hint_range(0.0,1.0)` | 0.2 | Lower end of roughness remap |
| Response | `roughness_max` | float / `hint_range(0.0,1.0)` | 0.8 | Upper end of roughness remap |
| Response | `normal_strength` | float / `hint_range(0.0,2.0)` | 1.0 | Normal-map depth |

Declare groups with `group_uniforms Surface;` and `group_uniforms Response;`. Sample at `uv = UV × uv_scale`. Set `ALBEDO = texture(color_tex, uv).rgb × tint.rgb`, `ROUGHNESS = mix(roughness_min, roughness_max, texture(roughness_tex, uv).r)`, `NORMAL_MAP = texture(normal_tex, uv).rgb`, and `NORMAL_MAP_DEPTH = normal_strength`. Keep metallic zero and opaque rendering. Enforce `0 ≤ roughness_min ≤ roughness_max ≤ 1` in configuration/driver validation.

Material A, Floor: tint `(1.0,0.92,0.80,1)`, UV scale 2, roughness 0.55–0.95, normal strength 1.0: warm, repeated, matte paving. Material B, StandIn: tint `(0.72,0.85,1.0,1)`, UV scale 1, roughness 0.20–0.55, normal strength 0.5: cooler, larger stones with a stronger specular response and gentler relief. Both materials share the Shader and textures but keep independent parameter values.

At default roughness endpoints, samples 0/0.5/1 produce 0.2/0.5/0.8. Setting both endpoints to zero gives zero everywhere; setting both to one gives one everywhere. UV scale 0.25/1/4 gives quarter/default/fourfold repetition. Normal strength 0/1/2 predicts flat/default/exaggerated relief. These require visual confirmation under fixed lighting.

† Normal-map check (Bao's decision, 30 October): commit the assignment's `godot/tests/normal_map_check.gd` before the material audit and calibrate it on this material's `nor_gl`/`nor_dx` pair. The GL file should come out low with `directx = false` and near 2 with `directx = true`; the pass threshold is set from that pair. If the results come out reversed, the sign convention is flipped and TEST-REPORT.md says so. The grazing-light look stays as an extra human check: hold camera, UVs, light and strength fixed while moving a grazing light across recognisable stones; the GL map should read as raised stones and the DX control should reverse the relevant slopes.

## Predicted failures and checks

| Failure | Check that should expose it |
|---|---|
| Tint stays yellow forever after a lethal hit | Cause a real lethal collision; assert LOST and `hurt_amount == 0` even with `iframes == 48` |
| LEVELUP or PAUSED consumes the protection fade | Enter each state mid-window, wait, compare counter and uniform before/after; both must hold and resume together |
| Restart displays a stale tint | Restart during protection; inspect the first rendered frame and assert zero uniform |
| Fresh texture sampling bypasses the blink, or double sampling darkens the sprite | Compare controlled lamp/coat pixels in both modulation phases with the calculation table |
| Shared ShaderMaterial couples objects | Change one material parameter; verify the other remains unchanged and resource identities differ |
| Misspelled uniform silently fails | Audit declared names/types with `get_shader_uniform_list`; intentionally rename a parameter in a disposable copy and require the contract check to fail |
| Wrong normal convention turns stones into dents | † `curl_ratio` under both conventions, calibrated on the GL/DX pair; grazing-light look as a human check |
| Roughness is decoded as colour or import defaults drift | Audit sampler hints and imported keys; compare roughness samples 0/0.5/1 against the remap and perform a fixed-light sweep |
| Shader fails to compile | Remove a semicolon in a disposable copy; require an error and failed check, then restore it |

Run the existing gameplay, audio and A3 checks unchanged after implementation. Drive timing checks through real session processing at 30, 60 and 144 rendering fps, including accepted and ignored hits; do not substitute direct driver calls for gameplay integration. Headless checks can verify wiring and state but cannot establish visible colour, readability or material relief.

## Seven short answers

1. **Which renderer does project.godot name, and what does it rule out?** It names `gl_compatibility`. Decals and compute shaders require Forward+ or Mobile, so they are unavailable here. VoxelGI, SDFGI and SSIL are also unavailable in Compatibility (and Mobile). This plan uses canvas and spatial shaders, textures and the existing lights. See Godot's [renderer feature comparison](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html).

2. **What colour arrives in your fragment function before you change it, and what would the tempting alternative give you?** In this canvas shader, incoming `COLOR` is the sampled sprite multiplied by primitive colour, modulation and self-modulation. For a red-phase lamp it is `(242,82.8,33.75)/255`, alpha one. A fresh `texture(TEXTURE, UV)` gives the original texture texel, bypassing those multipliers; multiplying that sample by incoming `COLOR` would texture it twice.

3. **For canvas_item, what would texture(TEXTURE, UV) give you instead of COLOR?** Only the texture sample, including its own alpha. It would discard the existing red blink and any primitive/self-modulation, including their alpha factors. This is why the mix reads incoming `COLOR`.

4. **For spatial, what does ALBEDO hold if you never write it, and what does COLOR hold?** `ALBEDO` defaults to white `(1,1,1)`; the spatial shader does not automatically sample an albedo texture. `COLOR` holds interpolated mesh vertex colour, normally white when no vertex colours are supplied. It is not the canvas sprite colour or an automatically populated base texture. The material shader explicitly writes ALBEDO. See the [spatial shader reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html).

5. **How long would a frame-counting version last at 30, 60 and 144 fps?** Counting 48 rendered frames gives `48/30 = 1.6 s`, `48/60 = 0.8 s`, and `48/144 = 0.3333 s`. The intended counter instead lasts 0.8 seconds of active 60 Hz simulation, with wall-clock time extended by PAUSED/LEVELUP. Terminal states clear the visual early.

6. **Which resource holds the uniform default, which holds its current value, and what happens when objects share a material?** The Shader resource's uniform declaration stores the default. ShaderMaterial stores current overrides set in the Inspector or by `set_shader_parameter()`; an unset parameter falls back to the Shader default. Two objects sharing a ShaderMaterial share those overrides, so changing one affects both. Separate materials can share the Shader while keeping independent values.

7. **Does hint_range clamp a value set by code?** Prediction: no. It supplies Inspector editing metadata, not runtime validation. Setting `hurt_amount` to 2 from code can make `mix` extrapolate beyond the target. The driver explicitly clamps its computed value. During Use It, set 2 in an isolated fixture, read it back and inspect the rendered result, then restore the production value; this has not yet been measured.

## Revisions

### 2026-10-30 — where the two materials go

Project facts line 17 and the material plan disagreed: one replaced the Floor and StandIn overrides in `lantern_gate_room.tscn`, the other used an independent A5 scene. Decision (Bao): a new scene `godot/a5/material_room.tscn` inherits `godot/a3/lantern_gate_room.tscn` and overrides only the `material_override` of Floor/Mesh and StandIn/Mesh with the two ShaderMaterials. The A3 room file, its lights and camera, and the A3 tests stay unchanged; the inherited scene reuses those lights and that camera.

### 2026-10-30 — what the material audit corrected in this brief

- Import route: the import keys in the material plan were set by `tools/a5/set_texture_imports.py` on the `.import` files Godot generated, then reimported, not in the editor's Import dock. The values are the planned ones, plus `detect_3d/compress_to=0` and `roughness/mode=1` so a real editor has nothing to switch. They are checked in the Import dock during the Step 4 editor session, and `git status` afterwards records any rewrite.
- Evidence split (the † table): the hint experiment is captured in its own unshaded scene, `godot/a5/hint_experiment/hint_experiment.tscn`, which has no lights. Only the interface sweep and the two-material comparison use the fixed A3 lights.
- Download sizes in the material plan were rounded from KiB. The exact sizes are 1,951,481 (diff), 2,126,688 (nor_gl), 2,126,021 (nor_dx) and 627,072 (rough) bytes, 6.83 MB in all (`godot/assets/textures/cobblestone_floor_08/ATTRIBUTION.md`).

