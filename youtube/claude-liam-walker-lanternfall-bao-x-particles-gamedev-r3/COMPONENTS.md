# COMPONENTS

This file lists what the film explains, beat by beat, and what it leaves out. The ledger with hashes is `gamedev-evidence.json`; it covers every authored file under the snapshot's `godot/`.

| Component | Files | Beats | Mechanism shown |
|---|---|---|---|
| presentation | `effects/particle_presentation.gd`, `game/session.gd` (weapon_hit), `game/game_state.gd` | B06–B07, B13–B14, B17–B20 | signals in, particles out; one burst per accepted hit (overlap, cap 32); a displacement-gated trail with a jump limit; the celebration overlay at the portrait; the freeze and clear policy |
| hit-sparks | `effects/defeat_sparks.tscn`, `assets/particles/spark.png` (+ import, attribution), `previews/defeat_sparks_preview.*` | B04–B05, B08–B12 | emission, process and draw in one scene; the intent and the first strip; r1 (scale) and r2 (colour ramp) with predictions, strips and verdicts |
| trail | `effects/lantern_trail.tscn`, `previews/lantern_trail_preview.*`, `previews/baseline/lantern_trail_r0.tscn` | B13–B16 | sphere emission, the feature A doesn't use; the alpha change and its fixture comparison |
| celebration | `effects/level_up_sparks.tscn`, `effects/level_up_overlay.tscn`, `ui/hud.gd` | B17–B18 | layer-11 overlay, portrait anchor |
| tests | config, state, edge and whole-tree-pause suites, harness, the original suites, the play-check driver | B21–B22 (B16, B20 for play-check shots) | blocked input with zero displacement; recorded totals (327); mutations; what headless cannot show |
| shader-study | `shaders/particles_generated.gdshader`, `previews/shader_study/*`, `tests/build_shader_study.gd`, `tests/test_shader_study_config.gd` | B23–B24 | two shader lines tied to brief settings; the study copy now drawing the ramp and curve |
| cost | `tests/cost_effects.gd`, `previews/visual_profiler_fixture.tscn`, `tests/visual_profiler_fixture.gd` | B25–B27 | on and off runs with identical fixtures; CPU twice; why headless reads near zero for GPU particles; GPU on the proxy, unresolved |
| game-context | the Assignment 2 game: session, player, weapons, enemies, gems, progression, world, HUD, audio, project settings and the generated assets | B07, B14, B18, B20 in play (also B03, game sound only) | not read line by line here; the Assignment 2 film explains it |

## Left out, with reasons

`tests/capture.gd`, `tests/capture_map.gd`, `tests/probe_balance.gd` and `tests/rasterize_storyboard.gd` are Assignment 2 development tools. The film neither uses nor shows them.

## Not explained in depth

The Assignment 2 systems appear in every capture but are not taught again. The Assignment 2 film, linked in the repository README, explains them.
