# COMPONENTS — what the film explains, and what it leaves out

Source revision shown: `5f09b7f` (`FILM-SOURCE-REVISION.txt`). Every file under `godot/` at that revision is hashed and assigned in `gamedev-evidence.json`.

| Component | Beats | Files | What the film shows |
|---|---|---|---|
| sprite-walk | B04 → B05, B06 → B07 | `features/player/courier_visual.tscn` (Body), `animations/courier_clips.tres` (walk), `assets/art/pc_sheet.png` + `.import`, `assets/art/ATTRIBUTION.md` | the slicing (hframes 10, offset −16, −23), the frame track (Body:frame, 2 at 0 and 3 at 8/60 s, discrete, nearest, LOOP_LINEAR, step 1/60), Bao's walk strip, the walk in the take, the seam numbers |
| dash-rig | B08 → B09, B16 → B17 | `features/player/build_courier_visual.gd`, `courier_visual.tscn` (Rig), `courier_clips.tres` (dash) | the phase table in the builder and its keys at 0/4/14/20, Bao's dash strip r1 at each boundary, revision r1 (6/10/12 → 4/10/6), revision r2 (the outline) with Bao's r1 and r2 strips |
| state-machine | B10 → B11, B12 → B13 | `features/player/player.gd`, `game/session.gd`, `features/progression/progression.gd`, `features/tuning.gd` | `_show()` as the one authority in manual mode, the card unlock, a clean dash, a hit in each phase in the take; the measured clocks |
| tests | B14 → B15 (also B11, B13) | the pins, read-back, structure and edge suites, the probes, the wrapper fixture, the harness, the earlier suites | `track_problems`, the read-back's 86 checks, the four required mutations, the Godot 3 names probe, the two-clocks numbers, the edge results |
| captures | B05, B09, B17 | `previews/courier_preview.*`, `tests/capture_courier*.gd`, `tests/play_dash.gd` | the fixture preview behind Bao's 30 fps strips |
| earlier-layers | B11, B13 | everything else the game runs on (session systems, weapons, enemies, ground, HUD, audio, A3/A5 scenes, A5 shaders, A6 effects, generated assets) | seen in the take; unchanged by A7; explained in the earlier films |

Excluded (listed with reasons in `gamedev-evidence.json`): development and capture tools of Assignments 2–6, the A6 previews and study scenes, and the two editor-generated study shaders.
