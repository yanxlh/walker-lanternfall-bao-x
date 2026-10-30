I've written `godot/MATERIALS.md` and `godot/tests/test_materials.gd`. `./scripts/run-test.sh test_materials.gd 60` gives **126 checks, 0 failures, exit status 0**; the full log is above and in `logs/test_materials_60fps.log`. No shader, material, scene or `.import` file was changed, and nothing is committed.

**How the test is built**
- It extends `res://tests/harness.gd`, which itself extends SceneTree. That matches the other suites: one PASS/FAIL line per check, exit 1 on any failure, and a record in `evidence/test_materials.json`.
- Running Godot's import created `godot/tests/test_materials.gd.uid`; I didn't write that file by hand.
- My first two runs failed because of bugs in my own checks, not in the assets. Fixing one of them uncovered finding 1 below.

**What the audit found** (full list with line references in `MATERIALS.md`)
1. **The material room's ambient light is probably not the colour it looks like.** The A3 room sets `ambient_light_source = 3` (`lantern_gate_room.tscn:11`). In Godot 4.7, 3 means "Sky" (the test prints the enum values), but the room has no sky. Godot's documentation says the ambient colour is only used when the sky contribution is below 1.0, and here it is 1.0. So the bluish ambient colour probably doesn't light the cobblestones. This line has been in the A3 file since 13 October and is out of scope for me to change.
2. **The floor stones are stretched and don't repeat.** The floor box's top face uses only a third of the texture's width and half its height. At the floor's `uv_scale` of 2, one copy of the texture covers 12 m × 8 m. So the 8 m floor shows less than one tile, stretched 1.5:1, which doesn't match the brief's "repeated paving".
3. **The roughness range rule isn't enforced anywhere.** The brief asks for `0 ≤ roughness_min ≤ roughness_max ≤ 1` to be validated, but nothing in `build_a5_materials.gd` checks it. The current values meet it, and the test now checks it.
4. **A comment in the build script is wrong.** `build_a5_materials.gd:3` claims Godot writes every UID, but none of the generated `.tres`/`.tscn` files has one. References are by path only, so moving a file will break them.
5. **The import settings were set by a script, not in Godot's editor.** The brief (line 122) asks for the editor. The resulting values do match the brief.
6. **Cost notes:**
   - The DirectX normal map is imported but nothing binds it at runtime, so it would ship unused in an export.
   - By my estimate (not measured), the three bound textures take about 9.8 MB of uncompressed video memory.
   - The brief's download sizes are MiB labelled as MB.
7. **Smaller points:**
   - The hint scene's tonemap, exposure, glow, fog and adjustment settings come from engine defaults rather than being written in the file.
   - The brief says to capture the hint experiment "under the fixed A3 lights", but that scene is unshaded and has no lights.
   - The stand-in loses its A3 emission.

All import keys, sampler hints, material values and texture bindings match the brief. The curl check reads `nor_gl` as the GL convention: 0.2236 without the DirectX flag and 1.7764 with it. The DirectX control map gives the reverse. The pass threshold is 1.0, set from that pair.

**What the headless test cannot establish**
A headless run draws nothing. So it can't show:
- any colour or brightness on screen;
- whether the stones read as raised (the grazing-light check);
- what the Sky ambient setting actually does to the room;
- how visible the UV stretch is;
- whether the Compatibility renderer shows 64/128/192 with and without `source_color`;
- the roughness and `uv_scale` sweeps;
- what the GPU actually allocates for the textures.

Two narrower limits: the curl check reads the source PNG, not the imported texture the shader samples. And the hints and defaults come from the shader source text, because `get_shader_uniform_list()` reports every sampler only as `Texture2D` and doesn't return defaults.

The ambient source (1) and the floor UVs (2) look like the two that will change how the room looks. Fixing either one would mean editing the A3 room file or the meshes, which is your call.