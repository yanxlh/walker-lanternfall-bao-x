# COMPONENTS

What the film explains, beat by beat, and what it leaves out. The ledger with hashes is `gamedev-evidence.json` (146 files under `godot/` at 4246f94, read from git: 129 assigned to components, 17 excluded with reasons).

| Component | Files | Beats | Mechanism shown |
|---|---|---|---|
| hurt-tint | `shaders/hurt_tint.gdshader`, `effects/hurt_tint_presentation.gd`, `game/session.gd` (lines 91–93 add the driver), `features/player/player.gd` (iframes), `features/tuning.gd` (IFRAME_TICKS 48), `game/game_state.gd`, `tests/capture_hurt_tint.gd` | B05–B08 (B03 game sound) | canvas_item fragment mixing incoming COLOR toward yellow by `hurt_amount`; the driver writes clamp(iframes / 48) every frame in PLAYING, PAUSED, LEVELUP and 0 otherwise; controlled captures against the hand table; the effect in play |
| material-room | `a5/material_room.tscn` and the inherited A3 room (`a3/lantern_gate_room.*`, gate, shrine, stack) | B09–B10, B12 | inherit, then override Floor/Mesh (PlaneMesh 8 × 8) and the two `material_override` slots |
| materials | `a5/materials/*.tres`, `a5/build_a5_materials.gd`, `MATERIALS.md`, the four Cobblestone Floor 08 maps with `.import` sidecars and `ATTRIBUTION.md` | B10–B12, B16 | a material is a shader reference plus values; a material-only `uv_scale` change moves only the floor |
| cobblestone-shader | `shaders/cobblestone_surface.gdshader` | B13–B18, B22 | samplers whose hints say colour / directions / raw numbers; grouped uniforms with hint ranges; fragment() writing ALBEDO, ROUGHNESS, NORMAL_MAP and NORMAL_MAP_DEPTH (line 22, Bao's `0b91838`); Bao's one-line ALBEDO × 0.5 edit darkening both objects |
| hint-experiment | `shaders/hint_experiment.gdshader`, `a5/hint_experiment/*` | B19–B20 | the same bytes through a source_color and an unhinted sampler; 64/128/192 on both quads under Compatibility |
| generated-shader | `shaders/standard_generated.gdshader`, `a5/scratch/standard_conversion.tscn` | B21–B22 | the editor's lines 3, 7, 19, 35 beside Bao's 1, 3, 4, 19; the film's fixture draws both on one plane |
| tests | `tests/test_hurt_tint.gd`, `test_materials.gd`, `harness.gd`, `normal_map_check.gd`, `calibrate_normal_map_check.gd`, `probe_headless_facts.gd`, `capture_a5_materials.gd`, and the ten earlier suites | B24–B25 (B16 curl output, B18 sweep tool) | real keys and real contact through the game loop, sampled every frame; recorded totals at 4246f94; the three mutations |
| game-context | the Assignment 2 game (session, player, weapons, enemies, gems, progression, world, HUD, audio, project settings, generated art, sound, music) and the Assignment 6 particle effects | B03, B08 (in play) | not read line by line; the earlier films explain them |

## Left out, with reasons

- Assignment 2 tools: `tests/capture.gd`, `tests/capture_map.gd`, `tests/probe_balance.gd`, `tests/rasterize_storyboard.gd`.
- Assignment 3 capture tools: `tests/capture_a3_orbit.gd`, `tests/capture_lantern_gate.gd`.
- Assignment 6 tools and studies, explained in the particle film: `tests/capture_play_checks.gd`, `tests/cost_effects.gd`, `tests/build_shader_study.gd`, `shaders/particles_generated.gdshader`, `previews/*` (fixture previews, the preserved trail baseline, the GPU study scene and its README).

None of these is loaded by the playable game or shown in this film.

## Not explained in depth

The Assignment 2 systems and the Assignment 6 particles appear in the hurt take but are not taught again. `godot/MATERIALS.md` (the material audit) is associated with the materials component; the film shows its consequences (test_materials, the PlaneMesh decision), not the document itself.
