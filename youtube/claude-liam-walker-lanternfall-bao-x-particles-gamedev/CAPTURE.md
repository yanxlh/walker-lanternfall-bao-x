# CAPTURE — how the footage was made

Film: `claude-liam-walker-lanternfall-bao-x-particles-gamedev` · source revision **c3e12737d9b38679efa61622cb62c793935aff59** (`FILM-SOURCE-REVISION.txt`) · Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility, macOS 26.6.2, Apple M4.

Every gameplay shot in the film is a real engine capture. Nothing is drawn, re-enacted or retimed. Held frames and replays are labelled on screen.

## Isolated copy, never the repository

`git archive c3e1273 godot` into a scratch folder, then two changes in the copy only:

- `project.godot` window override 1280 × 720 → **3840 × 2160**, so Movie Maker writes 4K;
- `capture_driver.gd`, `capture_main.tscn`, `study_capture.gd` and `study_capture.tscn` (this folder) copied in, then `--import` once.

`godot/` in the repository was not edited for the film: `git diff c3e1273 HEAD -- godot/` is empty.

## The driver (`capture/capture_driver.gd`)

Adapted from the Assignment 2 film's driver. It plays the game through the **real input map**: movement with `Input.action_press`, discrete keys (cards, pause) as `InputEventAction` events. One shortcut is disclosed: the run starts with `game.start_run(seed)` instead of Enter, so a take is reproducible from its seed. Every frame carries the label "Real engine capture · scripted input". Steering: flee anything within 90 px, else walk to the nearest gem, else circle. Card choice follows a fixed priority list, and **each card screen is held 2 s before the pick**.

Read-only particle diagnostics, which never change the game:

- every `weapon_hit` with its viewport position and the live burst count, and every `leveled_up`;
- with `LF_LOG_TRACK=1`, for every movie frame: the courier's viewport position and zoom, live hit bursts, live celebrations, whether the trail is emitting, and the game state.

The occlusion guard from the Assignment 2 driver is kept. If macOS stops drawing the window, the tree is paused and the frames are logged as stale. None of the three takes had a stale frame.

## Takes

| Take | Seed · command (in the isolated copy) | Movie frames | What happens |
|---|---|---|---|
| `take-main-seed11.avi` | `godot --always-on-top --path . res://capture_main.tscn --write-movie … --fixed-fps 30 -- main 11 80` | 2961 | 80 s of run time: 236 weapon hits, 7 level-ups (cards held 2 s), pause at run 0:30 for 2.5 s, Sunflare taken at level 7 |
| `take-props-seed11.avi` | `… -- props 11` | 420 | walk to the nearest stall, hold right into it (180 ticks), hold down-right to slide (120 ticks), stand |
| `study-cpu-vs-gpu.avi` | `godot --always-on-top --path . res://study_capture.tscn --write-movie … --fixed-fps 30 --quit-after 90` | 90 | the game's CPU hit sparks beside the editor-converted GPU study copy, both seed 7280, triggered on frames 10 and 50 |

MJPEG 3840 × 2160 at 30 fps with 48 kHz PCM, written by Godot's Movie Maker (`--fixed-fps 30`: two physics ticks per frame, deterministic). Hashes: `capture/takes.sha256`.

## Dry runs

Each gameplay take has a headless dry run of the same driver (`--headless --fixed-fps 30`): `capture/take-*-dryrun.jsonl`. Their event logs and per-frame tracks are **identical** to the takes' own logs (`capture/take-*-log.jsonl`): main 260 events and 2960 track frames, props 14 events and 419 track frames.

## Fixture and play-check material reused

Committed with the assignment at the same source revision and labelled as fixtures or scripted play checks on screen:

- `captures/defeat_sparks/r0`, `r1`, `comparison-r0-r1`, `mutation-godot3-name` (1280 × 720 Movie Maker, seed 7280);
- `captures/lantern_trail/comparison-20261029-135607` (r0 re-rendered from its preserved resource);
- `captures/play-checks/20261029-142138` (scripted windowed play checks, 1280 × 720).

The full fixture frame sequences under `captures/defeat_sparks/r*/` are kept locally only; B07 uses `r1` frames 0–47.

## Not committed

The AVI takes and the rendered `media/*.mp4` are large and stay out of git (`.gitignore`). The driver, the scenes, the commands above, the seeds and the source revision are enough to regenerate them.
