# COMPONENTS

What the film explains, beat by beat, and what it leaves out. The ledger with hashes is `gamedev-evidence.json` (98 files under `godot/`: 94 assigned to components, 4 excluded).

| Component | Files | Beats | Mechanism shown |
|---|---|---|---|
| presentation | `effects/particle_presentation.gd`, `game/session.gd` (weapon_hit, line 227), `game/game_state.gd` | B04–B05, B10–B11, B14–B17 | signals in, particles out; per-hit burst with cap 32; displacement-gated trail with a jump limit; celebration overlay at the portrait; freeze/clear policy |
| hit-sparks | `effects/defeat_sparks.tscn`, `assets/particles/spark.png` (+ import, attribution), `previews/defeat_sparks_preview.*` | B06–B09 | the burst as data; the r1 scale change, its prediction and measurement |
| trail | `effects/lantern_trail.tscn`, `previews/lantern_trail_preview.*`, `previews/baseline/lantern_trail_r0.tscn` | B10–B13 | sphere emission; the alpha change and its fixture comparison |
| celebration | `effects/level_up_sparks.tscn`, `effects/level_up_overlay.tscn`, `ui/hud.gd` | B14–B15 | layer 11 overlay, portrait anchor |
| tests | particle config, state and edge suites, harness, the original suites, play-check driver | B18–B19 (B13, B17 for play-check shots) | blocked input with zero displacement; recorded totals; mutations |
| shader-study | `shaders/particles_generated.gdshader`, `previews/shader_study/*`, `tests/build_shader_study.gd` | B20–B21 | process stage code; what the converted material draws |
| cost | `tests/cost_effects.gd` | B22–B23 | on/off with identical fixtures; CPU and GPU readings |
| game-context | the Assignment 2 game: session, player, weapons, enemies, gems, progression, world, HUD, audio, project settings and the generated assets | B05, B11, B15, B17 (in play; also B03, game sound only) | not read line by line here; the Assignment 2 film explains it |

## Left out, with reasons

- `tests/capture.gd`, `tests/capture_map.gd`, `tests/probe_balance.gd`, `tests/rasterize_storyboard.gd`: Assignment 2 development tools, neither used nor shown here.

## Not explained in depth

The Assignment 2 systems appear in every capture but are not taught again. A viewer who wants them should watch the Assignment 2 film linked in the repository README.
