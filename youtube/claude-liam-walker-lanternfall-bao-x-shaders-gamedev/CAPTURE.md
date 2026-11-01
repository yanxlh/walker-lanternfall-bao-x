# CAPTURE — how the film's new footage, fixture and test run were made

Film: `claude-liam-walker-lanternfall-bao-x-shaders-gamedev` · game source revision **4246f94bd3db51c0644ecc3bef9b3a8c8427911b** (`FILM-SOURCE-REVISION.txt`) · Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility (OpenGL 4.1 Metal), macOS 26, Apple M4.

The film shows one new gameplay take, one new film fixture and one new test run, all made here. Everything else it shows is committed repository material (in-engine captures, recorded logs), listed in SOURCES.md. Nothing is drawn, re-enacted or retimed. Held frames and replays are labelled on screen.

## Isolated copies, never the repository

Every Godot run used `git archive 4246f94 godot` unpacked into a scratch folder, never `$REPO/godot`. While the film was being built, `godot/shaders/cobblestone_surface.gdshader` in the working tree was edited (Bao's line-22 change, later committed as `0b91838`); the film reads every file through git at the film revision (`tools/src.py`) and never from the working tree.

- **capture copy**: `project.godot` window override 1280 × 720 → **3840 × 2160** (so Movie Maker writes 4K), and `capture/capture_driver.gd`, `capture/capture_main.tscn`, `capture/shader_pair_fixture.gd`, `capture/shader_pair_fixture.tscn` copied in; `--import` once (exit 0, no `ERROR` lines).
- **test copy**: unchanged archive, `--import` once (exit 0), then `capture/run_tests.sh`.
- **check copy**: unchanged archive, not imported; `./art godot-gamedev --check` runs against it.

## The hurt take (`capture/take-hurt-seed5.avi`)

Driver `capture/capture_driver.gd`, adapted from the Assignment 6 film's driver. It plays Lanternfall through the **real input map** (`Input.action_press` for movement, `InputEventAction` for `pause` and the card keys). One disclosed shortcut: the run starts with `game.start_run(5)` instead of Enter, so the take is reproducible from its seed. Every frame carries the game-side label "Real engine capture · scripted input".

Steering: walk to the nearest monster until a hit is accepted; then let go of every key until `player.iframes` is back to 0 (the protection window, so the fade can be watched); then walk away from the nearest monster for 1 s; repeat for three accepted hits. On the second hit the script presses `pause` when 24 ticks of protection are left and presses it again 1.5 s later. Card screens are held 2 s before a fixed-priority pick.

Read-only diagnostics, which never change the game: every accepted hit (`player.damaged`), and, in `_process` at `process_priority` 100000 (after the tint driver at 200), one row per engine iteration: the courier's viewport position and zoom, the `hurt_amount` stored on his material, `player.iframes`, whether the red blink is on, the run state, hp, monster contact and the tick. Row *i* is movie frame *i*: on the first accepted hit the row and the AVI both turn yellow at frame 1335 (checked by sampling the frame). The occlusion guard of the earlier drivers is kept; this take logged **no stale frames**.

    LF_LOG_TRACK=1 LF_CAPTURE_LOG=<reel>/capture/take-hurt-seed5-log.jsonl \
      godot --always-on-top --path . res://capture_main.tscn --write-movie <reel>/capture/take-hurt-seed5.avi --fixed-fps 30 -- hurt 5

| | |
|---|---|
| Frames | 1739 movie frames (3840 × 2160 MJPEG, 30 fps, 48 kHz PCM), 1738 track rows, `"stale": []` |
| Events | run starts at movie frame 60; level-ups at 642, 1271, 1432 (cards picked 2 s later); hit 1 at 1335 (run 0:38.5, hp 10 → 9); hit 2 at 1500 (hp 9 → 8); pause 1512–1557, `hurt_amount` held at 0.4792 (23/48); hit 3 at 1653 (hp 8 → 7), a monster touching him during protection at frames 1661–1666 with hp unchanged; tint 0 again at 1677 (24 frames, 48 ticks after the hit) |
| Dry run | `--headless --fixed-fps 30`, same arguments → `capture/take-hurt-seed5-dryrun.jsonl`, **identical** to the take's log (27 lines, every event and every track row) |
| Hash | `capture/takes.sha256` |

A first windowed attempt (from a 61c9cbf copy, before the film revision existed) logged hundreds of stale iterations before the run began and was stopped and deleted; the macOS window could not draw at the time. The take used in the film was recorded afterwards from the 4246f94 copy.

## The shader-pair fixture (`capture/shader-pair/`)

`capture/shader_pair_fixture.gd` is an **agent-made film fixture**, not gameplay and not Bao's work. It builds two 2 × 2 m planes (the scratch scene's default PlaneMesh size) under one directional light and an orthographic camera, and renders three modes, each at two camera poses (straight down; pitched 50°):

- `pair`: left plane wears the editor-converted material exactly as saved in `godot/a5/scratch/standard_conversion.tscn`; right plane wears a new ShaderMaterial on `godot/shaders/cobblestone_surface.gdshader` with the same three maps and neutral values (tint white, uv_scale 1, roughness 0–1, normal_strength 1), set in memory, never saved;
- `control-generated` and `control-bao`: the same material on both planes.

Comparing left with right inside one picture is **not** valid: the two plane positions sample the texture on different pixel grids, and the controls show left/right differences of the same size as the pair (mean ≈ 4.4–4.6 levels face-on). So `tools/pair_diff.py` compares the same plane across the two control renders (generated vs Bao's, identical pixel positions). Window size 2940 × 1653 (macOS limited the window to the display). Results in `capture/shader-pair/diff.json`:

| Pose | Plane | Pixels within 2 levels | Mean abs. difference | Max |
|---|---|---:|---:|---:|
| straight (`abs(NORMAL.z)` = 1) | left | 92.6 % | 0.62 | 23 |
| straight | right | 87.2 % | 1.00 | 25 |
| tilted 50° (`abs(NORMAL.z)` ≈ 0.64) | left | 62.0 % | 2.80 | 48 |
| tilted 50° | right | 68.8 % | 2.43 | 50 |

    godot --always-on-top --path . res://shader_pair_fixture.tscn -- <reel>/capture/shader-pair <pair|control-generated|control-bao>

## The film's test run (`capture/test-run-film-build-raw.txt`)

`capture/run_tests.sh` on the test copy: every suite headless with the modes in CLAUDE.md, each under a 180 s watchdog, `SHADER ERROR`/`SCRIPT ERROR` counted as failure. All exit 0: `test_hurt_tint.gd` 28/0 at 30, 60 and 144 fps; `test_materials.gd` 127/0; logic 32, gameplay 65, audio 25, defeat_sparks_config 39, extra_particles_config 79, particles_state 34, particles_edges 18, a3-assets 17, a3-lantern-gate 14, a3-camera 9 (332, 0 failures). The JSON results of the four new-suite runs are in `capture/test-run/`. Scratch paths in the text file are shortened to `<scratch>`.

## Not committed

The AVI take and every rendered video (`media/`, `exports/`, `mp3/`) stay out of git (`.gitignore`). The driver, the fixture, the commands, the seed and the source revision regenerate them.
