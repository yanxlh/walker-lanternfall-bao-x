# FACTCHECK

Every factual claim in the narration and on screen, with where it was checked. Source revision of the game: **c3e1273** (`FILM-SOURCE-REVISION.txt`). "Take" means a real 4K engine capture in `capture/` (CAPTURE.md).

## Corrections made while building the film

| Beat | First draft said | Why it was wrong | Now says |
|---|---|---|---|
| B08 | the "Bao saw no problem" cue highlighted line 36 | line 36 is `scale_amount_min`; the quote does not belong to a code line | both highlights are on the changed/unchanged scale lines; Bao's words sit in the notes panel |
| B14 | "so Bao couldn't see it" | the record says the celebration was "Not obvious" (not obvious); the veil was a code-inspection hypothesis, not a verified cause | "Bao found it hard to see" |
| B17 | "the embers and the last spark hang in mid-air" | at the pause frame the take's log shows 0 live hit bursts; only trail embers were on screen | "the trail's embers hang exactly where they were"; paused frames 1143 and 1180 shown, 0 pixels differ |
| B17 | "presses escape" | the driver sends the `pause` action (bound to Esc and P) | "presses pause" |
| B21 | "the motion is right; the look is lost" | the capture shows the GPU copy's sparks staying visible farther out; matching motion was not established | "the sparks still fly out; the colour fade and the shrink are gone" |
| B09 table | "lit area: matched" | measured 1.4–1.85× against a predicted ≈ 1.5× | "more than predicted" |
| B12 | "a sphere three pixels wide" (found in Codex's sampled review of the master delivered for review, SHA-256 4769b141…, relayed by Bao; about 3:27) | `emission_sphere_radius = 3.0` is a radius; the sphere is 6 px across | "a sphere with a three-pixel radius"; the line-29 highlight reads "(radius, px)"; narration regenerated and the master re-exported |
| B05 | a 2× crop following the courier | the camera was clamped at the arena corner in that stretch, so the courier and most hits left the crop | full frame, with a labelled diagnostic ring at each logged hit position |

## Claims by beat

| Beat | Claim | Checked against |
|---|---|---|
| B00 | three effects; 292 checks; source revision c3e1273 | `godot/effects/`; `evidence/assignment-6/final-precommit/*.json` (32 + 65 + 25 + 39 + 79 + 34 + 18) |
| B00 | three tuning changes, each kept after play | TUNING.md: portrait placement “That works”; trail kept; A r1 “Keep it; it is clearer” |
| B01 | effects answer events and never write game state | `particle_presentation.gd` (signals in; writes only particle nodes); logic/gameplay/audio counts unchanged |
| B02 | excerpt | CHANGE-BRIEF.md "Tuning and acceptance", verbatim; brief committed at 8eb16a2 before implementation |
| B04 | weapon_hit before health changes; PLAYING only; cap 32; world position; restart | `game/session.gd` 227; `particle_presentation.gd` 49, 53, 56; `MAX_HIT_BURSTS` line 9 |
| B05 | bursts overlap; counter from the take's log | `capture/take-main-seed11-log.jsonl` track (up to 8 live in this stretch) |
| B05 | 40 hits → 32 bursts, 512 particles; burst survives the enemy | `evidence/assignment-6/final-precommit/particles_state.json` (hit-cap-*, lethal-hit-survives-enemy-free) |
| B06 | 16 sparks, explosiveness 1, 0.45 s, point, spread 180, speed 25–55, damping 20–30, gravity (0, 12) | `effects/defeat_sparks.tscn` lines 21–35 |
| B07 | 14 × 14 first frame; separate sparks by 0.20 s; widest 64 px under 68; last pixel 0.40 s | `captures/defeat_sparks/comparison-r0-r1/COMPARISON.md` measured table |
| B08 | in play, no problem; first frame 0.35 height; scale_amount_max 1.2 → 1.8; nothing else changed | TUNING.md entries of 29 October; `a-r0-source/defeat_sparks.tscn` vs current scene (one line differs) |
| B09 | 11 → 14 px, predicted 15; up to 85% more lit area; footprint +1 px (predicted 3–4); fade unchanged; kept | COMPARISON.md; CHANGE-BRIEF.md trial r1 prediction; TUNING.md verdict |
| B10 | distance moved; limit = speed × Δt × 2 + 4 ≈ 7 px; emit when PLAYING, visible, moving | `particle_presentation.gd` 126, 127, 129; `Tuning.PLAYER_SPEED` 90 |
| B11 | pushing into the stall: no movement, no embers; sliding: embers | `take-props-seed11-log.jsonl` track: after contact 0 emitting frames; slide 58/58 |
| B12 | sphere radius 3 px, shape 1, 24 embers, ~1/3 s, alpha on line 14 | `effects/lantern_trail.tscn` lines 17–29 (lifetime 0.35 on line 23; alpha on line 14, named in the notes panel) |
| B13 | first look “The level-up sparks and movement trail are not obvious”; brighter, same footprint, clear by the same frame; kept; 2–4 px vs 6–11 px | TUNING.md; `captures/lantern_trail/comparison-*/COMPARISON.md`; PLAY-CHECKS.md |
| B14 | overlay layer 11 above HUD 10; portrait anchor; at most 4 | `level_up_overlay.tscn` (layer 11); `particle_presentation.gd` 61, 65, 66; `MAX_LEVEL_BURSTS` line 10 |
| B15 | burst on the portrait, gone before the 2 s pick; “That works” | main take frames after level 2 (pf 316, pick pf 377); TUNING.md |
| B16 | speed_scale 0 outside PLAYING; celebration runs in LEVELUP; trail stops outside play; cleared on WON/LOST | `particle_presentation.gd` 107–119 and 99–105 |
| B17 | pause at run 0:30; paused frames identical; LOST/WON first frames have no particles; “Nothing is obscured; everything behaves normally” | take log (pause pf 1142–1217); pixel comparison in `tools/build_media.py` b17; `captures/play-checks/20261029-142138/states.json`; PLAY-CHECKS.md |
| B18 | stall fixture, 30 frames of real key input, both counts zero | `tests/test_particles_edges.gd` 54–69 |
| B19 | seven suites, 292 checks, 0 failures; guard removed → exactly two failures; Godot 3 name loads silently, 45 × 43 → 40 × 42 px | `evidence/assignment-6/final-precommit/`; `evidence/assignment-6/mutations/edges-no-displacement-guard.log`; `captures/defeat_sparks/mutation-godot3-name/README.md` |
| B20 | generated by the editor; velocity, move, colour ramp and scale curve at age on 347; COLOR to the draw stage | `shaders/particles_generated.gdshader` line 1 header, lines 340–352; Bao's explanation in TEST-REPORT.md |
| B21 | CPU shrinks and fades; GPU copy stays white and full-size; ShaderMaterial has no color_ramp / scale_curve | `capture/study-cpu-vs-gpu.avi`; `previews/shader_study/hit_sparks_gpu.tscn` (no texture parameters) |
| B22 | same fixture twice, presentation freed for "off", 5 trials × 300 frames | `tests/cost_effects.gd` 58–63, constants lines 11–14 |
| B23 | +0.009 ms at 32 live; ≈ +0.10 ms spike; trail +0.004 ms; GPU 0 under Compatibility; Vulkan proxy within ±0.1 ms | `evidence/assignment-6/cost/COST-REPORT.md` and its JSON |
| B24 | verdict lines | the beats above |
| B25 | the trail config test checks emission_sphere_radius 3.0 | `tests/test_extra_particles_config.gd` line 39 |

## What the film does not claim

That the effects look good in every situation (Bao's verdicts cover their own play); that the GPU proxy measures the shipped renderer (it does not); or that the first frame now reaches one character height (it does not: 0.41).

Student feedback quotations above are English translations of the recorded statements.
