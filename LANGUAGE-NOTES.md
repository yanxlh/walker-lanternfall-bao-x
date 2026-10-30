# Language notes — Assignment 5

Written by Bao. Line references are `file:line`, with shader paths relative to `godot/shaders/`.

## Generated shader: `standard_generated.gdshader`

From a StandardMaterial3D with an albedo texture, a normal map and a roughness texture, converted in the editor (Step 4). To be filled from the saved file.

| Item | Line(s) | What the line does |
|---|---|---|
| `shader_type` | | |
| `render_mode` | | |
| uniform for the Inspector's albedo colour | | |
| uniform for the Inspector's normal-map strength | | |
| albedo sampler, with its hints | | |
| normal-map sampler, with its hints | | |
| line that writes `ALBEDO` | | |
| line that writes `ROUGHNESS` | | |
| line that writes `NORMAL_MAP` | | |

## 1. What does `shader_type` decide?

shader_type selects the rendering pipeline and available built-ins. hurt_tint:1 uses canvas_item for 2D; cobblestone_surface:1 and hint_experiment:1 use spatial for 3D.

## 2. Which processor functions did you write, and when does each run? What would change if you moved your colour line into `vertex()`, and why?

Processors: All three define fragment() (hurt_tint:7, cobblestone_surface:17, hint_experiment:9), which processes rasterized fragments. Moving the hurt colour line (hurt_tint:8) to vertex() changes the result because vertex COLOR has not yet been multiplied by the sprite texture.

## 3. Name three built-ins you read and two you wrote. Which of the ones you read are read-only?

Built-ins: The current code explicitly reads UV (cobblestone_surface:18, hint_experiment:11) and COLOR (hurt_tint:8), and writes COLOR (hurt_tint:8) and ALBEDO (cobblestone_surface:19). Fragment UV is read-only; canvas COLOR is read/write. A third distinct explicit read is still missing.

## 4. For each hint you used, does it change only the Inspector, or also the value the shader receives?

Hints: hint_range (hurt_tint:4) controls Inspector editing. source_color (hurt_tint:5, cobblestone_surface:3, hint_experiment:5) identifies colour data; hint_normal (cobblestone_surface:4) identifies normal data. Filtering and repeat hints (cobblestone_surface:3–5, hint_experiment:5–6) affect texture sampling. The hint capture (`captures/a5-materials/20261030-131056-hint/hint-experiment.png`) shows 64/128/192 on both quads under Compatibility.

## 5. Does `hint_range` clamp a value set from code?

Runtime limits: hint_range (hurt_tint:4) does not clamp code assignments. Setting 2.0 read back as 2.0 (`captures/hurt-tint/20261030-125036/captures.json`); the yellow screenshot results from output saturation.

## 6. Which line of the generated shader makes the albedo sample as colour and the normal map as data, and what is the equivalent line in your textured shader?

Texture roles: In cobblestone_surface, line 3 declares colour sampling, line 4 declares normal sampling, and lines 19/21 use them. Generated-shader references remain unavailable until conversion succeeds.

## 7. Your `fragment()` runs for every pixel at once. Why can't it read what the neighbouring pixel's `fragment()` is computing, and how does game state reach it instead?

Fragment independence: Neighbouring fragment execution has no guaranteed order or shared unfinished output. GDScript passes game state through hurt_amount (hurt_tint:4, read at hurt_tint:8) using set_shader_parameter() at hurt_tint_presentation:30.

## 8. Name two things the Godot shading language provides that plain GLSL does not, or makes you write yourself.

Godot-specific facilities: Engine-connected outputs such as ALBEDO and NORMAL_MAP (cobblestone_surface:19, 21), plus uniform hints integrated with the Inspector (hurt_tint:4–5, cobblestone_surface:7–14).
