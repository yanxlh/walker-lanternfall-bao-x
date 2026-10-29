# PROMPTS

## B00 — the reconstructed Walker ask (on screen)

Reconstructed from Bao's CHANGE-BRIEF.md for the cold open; it is not a recorded session.

> Please use Walker to convert my game design document about particle effects for Lanternfall, warm sparks on every weapon hit and a short ember trail behind the courier, into Godot 4 CPUParticles2D scenes. Gameplay must not change. Test every setting, and show me real before-and-after frames for each tuning change.

## B25 — Your Turn (read aloud)

> Please use Walker to read godot/effects/lantern_trail.tscn in my Lanternfall project. Change only emission_sphere_radius from 3.0 to 8.0. Before running anything, predict how the trail's width and brightness change at fixture frames 20 and 39, and which configuration check fails. Then capture both strips, compare them with your prediction, and put 3.0 back.

It is one bounded change with a prediction and a measurement. `tests/test_extra_particles_config.gd` line 39 asserts the radius 3.0, so the check will fail until the value is restored.

## The request that produced this film

On 2026-10-29 Bao approved the diary entry, asked for the work to be committed and then for the film to be made. The assignment checklist names the godot-gamedev + walker workflow for this step. The skill was run with: one 4K landscape film covering the game, Effect A, Effect B, the level-up celebration, the tuning prediction against real before/after frames, Bao's verdicts, tests, the generated process shader, and CPU/GPU cost against budget; no minimum length, no second video, no Short, no publishing.
