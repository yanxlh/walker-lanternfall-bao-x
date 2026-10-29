# Godot 3 property-name mutation — windowed observation

On 29 October 2026, `initial_velocity_min = 25.0` in `godot/effects/defeat_sparks.tscn` was temporarily renamed to the Godot 3 name `initial_velocity = 25.0`. The rest of the kept r1 scene was unchanged, including `scale_amount_max` 1.8. The same fixture was then captured from the terminal (1280 × 720, 30 fps, seed 7280), and the configuration test was run. The scene was restored from a copy and checked byte-identical, and the configuration test passed again (39 checks, 0 failures).

Engine behaviour: Godot loaded the scene without any warning in `logs/capture-defeat-sparks-mutation.log`. The unknown property was ignored, and `initial_velocity_min` fell back to 0. The configuration test failed only on `setting-initial_velocity_min` (actual 0.0, expected 25.0; `config-test-during-mutation.log`).

Visible result compared with r1 (`mutation-vs-r1-sheet.png`, r1 top, mutation bottom, 3× crops):

| File | Time | r1 extent | mutation extent |
|---:|---:|---|---|
| 9 | 0.00 s | 14 × 14 | 12 × 13 |
| 12 | 0.10 s | 30 × 29 | 27 × 28 |
| 15 | 0.20 s | 45 × 43 | 40 × 42 |
| 18 | 0.30 s | 60 × 55 | 52 × 52 |
| 22+ | — | none | none |

The burst still appears, keeps its colours and fades on the same schedule. Its speed range is now 0–55 instead of 25–55, so the spread is about 10–15% tighter and a few sparks linger near the centre. At full frame this would be easy to miss. The read-back test catches a mistake that does not visibly break the effect.

Files: `strip/` (files 9, 10, 12, 15, 20, 30, 50), `mutation-vs-r1-sheet.png`, `config-test-during-mutation.log`. The full 60-frame sequence is retained locally only.
