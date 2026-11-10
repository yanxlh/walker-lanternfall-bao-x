# CAPTURE — how the footage was made

Film: `claude-liam-walker-lanternfall-bao-x-particles-gamedev-r3` · game source: `godot/` tree `14e6b2c` (FILM-SOURCE.md) · Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility, macOS 26.6.2, Apple M4.

Every gameplay shot in the film is a real engine capture. Nothing is drawn, re-enacted or retimed. Held frames and replays are labelled on screen.

## Isolated copy, never the repository

The snapshot's `godot/` was copied to a scratch folder, and only the copy was changed:
- `project.godot` window override changed from 1280 × 720 to **3840 × 2160**, so Movie Maker writes 4K;
- `capture_driver.gd`, `capture_main.tscn`, `study_capture.gd` and `study_capture.tscn` (this folder) copied in, then `--import` run once.

## The driver

`capture/capture_driver.gd` is unchanged from the first particle film. It plays the game through the real input map. One shortcut is disclosed: the run starts with `game.start_run(seed)`, so a take is reproducible from its seed. Every frame carries "Real engine capture · scripted input". Card screens are held 2 s before the scripted pick. The particle diagnostics are read-only.

## Takes (9 November 2026)

| Take | Command (in the isolated copy) | Movie frames written | Stale frames | Used as |
|---|---|---:|---:|---|
| main, seed 11 | `godot --always-on-top --path . res://capture_main.tscn --write-movie … --fixed-fps 30 -- main 11 80` | 10464 | 7503 | `capture/clean/take-main-seed11.mov`, 2961 frames |
| props, seed 11 | `… -- props 11` | 421 | 0 | the AVI as written |
| study | `godot --always-on-top --path . res://study_capture.tscn --write-movie … --fixed-fps 30 --quit-after 90` | 90 | — | the AVI as written |

During the main take, macOS often reported the window as unable to draw, most likely because it was hidden or covered while other work ran on the same desktop. The driver's occlusion guard paused the whole game for each such engine iteration and logged it as stale. Movie Maker still wrote a repeated picture for it. `tools/clean_take.py` dropped exactly those 7503 frames and their audio chunks, with a 4 ms crossfade at each splice. Its record is `capture/clean/take-main-seed11.json`. No game frame was dropped or retimed.

## Dry runs and identity checks

Each gameplay take has a headless dry run of the same driver (`--headless --fixed-fps 30`):
- **props:** the take's log is byte-identical to its dry run.
- **main:** all 262 events are identical to the dry run except their process-frame numbers, which include the stale iterations. The clean video's frame n is the dry run's frame n, so the evidence beats index the clean video with `take-main-seed11-dryrun.jsonl`.
- **Both dry runs** are byte-identical to the 29 October take logs of the first particle film. The r2 colour-ramp change and the new tests changed nothing in play: the same hits, positions, level-ups and burst counts.

## Fixture, profiler and play-check material reused

All of it is labelled on screen:
- `captures/defeat_sparks/r0`, `r1`, `r2`, `comparison-r0-r1`, `comparison-r1-r2`, `mutation-godot3-name` (1280 × 720 Movie Maker fixtures, seed 7280). The full r0 and r1 sequences are local; their strip frames match the committed strips byte for byte.
- `captures/lantern_trail/comparison-20261029-135607` (r0 re-rendered from its preserved resource).
- `captures/play-checks/20261029-142138` (scripted windowed play checks, 1280 × 720, r1 sparks).
- `evidence/assignment-6/cost/visual-profiler-a-r2-current/a-off-visible.png`, `a-on-visible.png`: editor screenshots captured by Codex. Only the profiler rows and graph are shown, cropped, not edited.

## Not committed

The AVI takes, the clean MOV and the rendered `media/*.mp4` stay out of git. The driver, the scenes, the commands above, the seeds and the source tree id are enough to regenerate them.
