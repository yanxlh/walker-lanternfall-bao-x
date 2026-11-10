# FACTCHECK — every claim and its source

| Beat | Claim on screen or in narration | Source |
|---|---|---|
| B00 | 327 automated checks; four tuning changes kept by Bao (A r1, A r2, B r1, celebration placement) | current-r2-validation/README.md; TUNING.md |
| B02 | purpose of the effects, quoted | CHANGE-BRIEF.md, "What I want to do" (supplement written by Bao) |
| B04 | amount 16, explosiveness 1.0, lifetime 0.45, point emission, spread 180, velocity 25–55, gravity (0, 12), additive material, 3 × 3 texture | godot/effects/defeat_sparks.tscn lines 19–33; assets/particles/ATTRIBUTION.md |
| B05 | first frame 14 × 14 px white; pale yellow to about 0.27 s; last pixel 0.40 s; extents per file | captures/defeat_sparks/comparison-r1-r2/COMPARISON.md; r2 strip |
| B06 | PLAYING only, cap 32, new instance per hit, world position, restart | particle_presentation.gd lines 47–57 |
| B07 | counter from the take's log; 40 hits, 32 bursts, 512 particles in the stress fixture | capture/take-main-seed11-dryrun.jsonl; current-r2-validation/particles_state.json |
| B08 | intent: compact cluster, spread by 0.20 s, gone by 0.45 s, about one height, at most two; r0 first frame 11 × 12 px = 0.35 of a 34 px courier | CHANGE-BRIEF.md (original Visual intent); TUNING.md r0 reading |
| B09 | r1: scale_amount_max 1.2 → 1.8; Bao "Done; no problem"; approved "Agreed"; came from Claude's strip reading | TUNING.md; CHANGE-BRIEF.md revision 29 October |
| B10 | 11 → 14 px (predicted 15); footprint +1 px (predicted +3–4); Bao "Keep it; it is clearer" | comparison-r0-r1/COMPARISON.md; TUNING.md |
| B11 | Bao "The hit sparks are not eye-catching enough"; r1 at 0.20 s mid-orange, 21 of 189 bright; middle stop 0.35:(1,.6,.2,.85) → 0.6:(1,.75,.3,1); test changed first and failed on the middle stop only; approved "Approve" | TUNING.md r2 entry; a-r2-tests/defeat_sparks_config-expected-failure.log; defeat_sparks.tscn lines 12–14 |
| B12 | file 15 luma 151 → 236, bright 21 → 189 of 189; file 17 bright 2 → 83; extents identical; last trace file 21; colour (255, 238, 163); Bao "Yes", "They don't get mixed up", kept | comparison-r1-r2/COMPARISON.md and manifest.json; TUNING.md |
| B13 | displacement, jump limit speed × Δt × 2 + 4, emit only PLAYING, visible, moving | particle_presentation.gd lines 121–131 |
| B14 | pushing into the stall: no displacement, no embers; sliding: embers | props take log (identical to its dry run) |
| B15 | sphere emission radius 3, shape 1, 24 embers, continuous; alpha 0.95 / 0.70 / 0 (was 0.55 / 0.30 / 0) | lantern_trail.tscn lines 14, 17–29; evidence/assignment-6/tuning/r0-source |
| B16 | Bao "The level-up sparks and movement trail are not obvious"; brighter, same footprint, both clear at 51/60; kept | TUNING.md; trail COMPARISON.md |
| B17–B18 | CanvasLayer 11, portrait anchor, cap 4; Bao "That works" | particle_presentation.gd 59–70; TUNING.md |
| B19–B20 | speed_scale 0 outside PLAYING; trail never spawns outside play or hidden; paused frames identical; LOST/WON first frames empty; Bao's check about stopping and pausing | particle_presentation.gd 107–119; clean main take; play checks; TUNING.md (Bao's recorded check) |
| B21–B22 | nine suites, 327, zero failures; Godot 3 name and spread drift exit 1; guard removal fails two checks (29 October run); the headless limits | current-r2-validation/*.json, godot3-name.log, wrong-spread.log, mutation-exit-codes.json; mutations/edges-no-displacement-guard.log |
| B23 | line 149 scale min/max ↔ 0.7 / 1.8; line 161 colour ramp ↔ r2 ramp; Bao's process/draw explanation | particles_generated.gdshader 148–161; TEST-REPORT.md |
| B24 | textures bound in a6-r2, ramp mirrored to r2; the GPU copy turns orange a little sooner; random spread differs | previews/shader_study/README.md; study capture frames 9–20 |
| B25–B26 | presentation freed for "off"; A +0.098 / +0.047 ms, B −0.007 / +0.007, celebration +0.009 / +0.016; why GPU particles read near zero headless | cost_effects.gd 58–63; cpu-r2.json; tests/cpu-r2-headless-20261109.json |
| B27 | Compatibility 0.000 ms; profiler frames 715 (GPU 0.62) and 782 (GPU 5.21); first pair +0.69; timer runs −0.06 to +0.39, 15-trial median +0.17; B −1.40; celebration +0.91 on 29 October | visual-profiler-a-r2-current/README.md and PNGs; gpu-r2.json; tests/gpu-*.json; cost/FINAL-COMPARISON.md |
| B28 | mistakes, agreement, uncertainty, next step, contributions, texture, revision | TEST-REPORT.md; TUNING.md; CONTRIBUTIONS-assignment-6.md; ATTRIBUTION.md; FILM-SOURCE.md |
| B29 | the verdict lines | the rows above |

## Corrections made while building

- The code panel shows at most 14 lines. B04 was cut to lines 19–32 and its narration re-voiced; the shader excerpt was cut to lines 148–161.
- B24 originally said the GPU copy's "life over time matches". The capture shows it turning orange a little sooner, so the line was re-voiced.
- The profiler screenshots show the editor's Chinese interface. B27 crops to the profiler rows and graph only, and its labels are English.
- B08's footer said 12× crops; the crops are 4×.
