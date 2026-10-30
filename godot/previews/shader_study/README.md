# Particle shader study scene

`hit_sparks_gpu.tscn` is a GPUParticles2D built from the game's CPU hit sparks (`res://effects/defeat_sparks.tscn`, kept r1 settings) by Godot's own `GPUParticles2D.convert_from_particles()`, via `res://tests/build_shader_study.gd`. It has the same amount, lifetime, one-shot burst, direction, spread, velocity, gravity, damping, scale range and curve, colour ramp, texture and additive material. The game never loads it.

## Editor steps (student)

1. Open `godot/project.godot` in Godot 4.7.2 and open `res://previews/shader_study/hit_sparks_gpu.tscn`.
2. Select `HitSparksGPU`. In the Inspector, open the dropdown next to **Process Material** (a ParticleProcessMaterial) and choose **Convert to ShaderMaterial**.
3. Open the new ShaderMaterial, open the dropdown next to **Shader**, and choose **Save As…** → `res://shaders/particles_generated.gdshader`. Create the `shaders` folder if asked.
4. Save the scene. Only this study scene changes; do not convert any scene under `res://effects/`.

The saved shader is the editor-generated study artifact referred to in `CLAUDE.md`. It is not hand-written and gameplay does not use it.

## Revision 2 state

The editor conversion is already complete. Do not repeat the ParticleProcessMaterial conversion steps above on the saved ShaderMaterial. The generated shader remains unchanged; color_ramp and scale_curve now bind explicit textures. Run comparison_preview.tscn for the isolated CPU/GPU lifecycle comparison. See evidence/assignment-6/shader-study-fixed/README.md for captures and the 21-check regression test.
