# Language notes — Assignment 5

Written by Bao. Line references are `file:line`, with shader paths relative to `godot/shaders/`.

## Generated shader: `standard_generated.gdshader`

From a StandardMaterial3D with an albedo texture, a normal map and a roughness texture, converted in the editor (Step 4, `43dfe20`).

| Item | Line(s) | What the line does |
|---|---|---|
| `shader_type` | 3 | Selects the 3D spatial shader pipeline. |
| `render_mode` | 4 | Sets blending, opaque depth writing, back-face culling and lighting models. |
| uniform for the Inspector's albedo colour | 6 | Exposes the base colour with colour-space semantics. |
| uniform for the Inspector's normal-map strength | 20 | Exposes the normal-map strength. |
| albedo sampler, with its hints | 7 | Samples colour with mipmap filtering and repeating UVs. |
| normal-map sampler, with its hints | 19 | Declares normal data used for roughness filtering, without source_color. |
| line that writes `ALBEDO` | 35 | Multiplies the albedo texture by the base colour. |
| line that writes `ROUGHNESS` | 43 | Multiplies sampled roughness by the roughness uniform. |
| line that writes `NORMAL_MAP` | 46 | Supplies the sampled tangent-space normal. |

## 1. What does `shader_type` decide?

shader_type selects the rendering pipeline and available built-ins. hurt_tint:1 uses canvas_item for 2D; cobblestone_surface:1 and hint_experiment:1 use spatial for 3D.

## 2. Which processor functions did you write, and when does each run? What would change if you moved your colour line into `vertex()`, and why?

Processors: All three define fragment() (hurt_tint:7, cobblestone_surface:17, hint_experiment:9), which processes rasterized fragments. Moving the hurt colour line (hurt_tint:8) to vertex() changes the result because vertex COLOR has not yet been multiplied by the sprite texture.

## 3. Name three built-ins you read and two you wrote. Which of the ones you read are read-only?

The shaders read UV (cobblestone_surface:18), COLOR (hurt_tint:8), and NORMAL (cobblestone_surface:22). In fragment(), UV is read-only, while canvas COLOR and spatial NORMAL are read/write. Two built-ins written are COLOR (hurt_tint:8) and ALBEDO (cobblestone_surface:19).

## 4. For each hint you used, does it change only the Inspector, or also the value the shader receives?

Hints: hint_range (hurt_tint:4) controls Inspector editing. source_color (hurt_tint:5, cobblestone_surface:3, hint_experiment:5) identifies colour data; hint_normal (cobblestone_surface:4) identifies normal data. Filtering and repeat hints (cobblestone_surface:3–5, hint_experiment:5–6) affect texture sampling. The hint capture (`captures/a5-materials/20261030-131056-hint/hint-experiment.png`) shows 64/128/192 on both quads under Compatibility.

| Hint | Inspector only, or affects shader values? |
|---|---|
| hint_range | Inspector editing range only; code values are not clamped. |
| source_color | Can change colour-space handling; not merely an Inspector hint. |
| hint_normal | Identifies normal-map sampling; not merely an Inspector label. |
| filter_nearest | Changes sampled values by selecting nearest texels. |
| filter_linear_mipmap | Changes filtering and mipmap sampling. |
| repeat_enable | Changes samples outside the base UV range by repeating the texture. |
| hint_default_white — generated line 12 | Supplies white when no texture is assigned. |
| hint_roughness_r — generated line 14 | Identifies the red roughness channel for import/mipmap processing; does not itself extract that channel. |
| hint_roughness_normal — generated line 19 | Identifies the normal map used in roughness filtering; does not mark it as sRGB colour. |

Reference the hint experiment: both quads rendered 64/128/192 under Compatibility. That observation does not establish identical behaviour in other renderers.

## 5. Does `hint_range` clamp a value set from code?

Runtime limits: hint_range (hurt_tint:4) does not clamp code assignments. Setting 2.0 read back as 2.0 (`captures/hurt-tint/20261030-125036/captures.json`); the yellow screenshot results from output saturation.

## 6. Which line of the generated shader makes the albedo sample as colour and the normal map as data, and what is the equivalent line in your textured shader?

In standard_generated.gdshader:7, source_color marks the albedo texture as colour. The normal sampler at line 19 has hint_roughness_normal and no source_color, so it remains normal data. Lines 34–35 sample and apply albedo; line 46 samples and writes the normal. My equivalents are cobblestone_surface.gdshader:3–4 for the declarations and lines 19/21 for their use.

## 7. Your `fragment()` runs for every pixel at once. Why can't it read what the neighbouring pixel's `fragment()` is computing, and how does game state reach it instead?

Fragment independence: Neighbouring fragment execution has no guaranteed order or shared unfinished output. GDScript passes game state through hurt_amount (hurt_tint:4, read at hurt_tint:8) using set_shader_parameter() at hurt_tint_presentation:30.

## 8. Name two things the Godot shading language provides that plain GLSL does not, or makes you write yourself.

Godot-specific facilities: Engine-connected outputs such as ALBEDO and NORMAL_MAP (cobblestone_surface:19, 21), plus uniform hints integrated with the Inspector (hurt_tint:4–5, cobblestone_surface:7–14).
