@AGENTS.md

# Project context

## Engine and renderer
- Godot 4.7 (`godot/project.godot:15`); the exact build is 4.7.2.stable.official.ed1daf0bf (`README.md:17`).
  Use Godot 4 class and property names for 4.7 only. Godot 3 names load without complaint and do nothing:
  `Animation.loop` (4.7: `loop_mode`), `playback_speed` (4.7: `speed_scale`), `AnimatedSprite.frames` /
  `playing = true` (4.7: `AnimatedSprite2D.sprite_frames` / `play()`). If unsure a property exists in 4.7, say so.
- Renderer: `gl_compatibility` for desktop and mobile (`godot/project.godot:34-35`).
  The 2D canvas uses nearest filtering (`godot/project.godot:33`). The viewport is 640 x 360, shown at 1280 x 720.

## Main scene
- `res://game/main.tscn` (`godot/project.godot:14`): one `Node2D` named Main with
  `res://game/session.gd` attached. The session builds everything in code, with no child scenes.
- The simulation is `session.tick()`, called once per physics frame from `_physics_process` while the run state is
  PLAYING, at `Tuning.TICK_HZ = 60` (`godot/features/tuning.gd:4`). Tests set `test_mode` and call `step_ticks(n)`.

## The animated object: the courier (player)
- Created in code: `PlayerScript.new()` in `session.gd`, script `godot/features/player/player.gd` (`Node2D`).
- Today it draws itself in `_draw()` from the 32 px cells of `res://assets/art/pc_sheet.png`, picking the cell
  from `pose` (`POSES`, `choose_pose()`); without the sheet it draws a placeholder.
- `player.material` holds the hurt-tint `ShaderMaterial` (`godot/effects/hurt_tint_presentation.gd`).
- Level-up cards live in `godot/features/progression/progression.gd` (`CARD_TEXT`, `eligible_cards()`,
  `apply()`); `session.choose_card()` applies the courier-side effects.
- Input actions are created in `session._ensure_inputs()`; one-shot presses are handled in
  `session._unhandled_input()`. Movement is read with `Input.get_vector` in `_physics_process`.

## Tests, all through `scripts/run-test.sh`
`./scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]`: the file sits in `godot/tests/`; a number
adds `--fixed-fps N`; timeout 120 s; log in `logs/<test>_<tag>.log`; exit 1 on `SHADER ERROR`/`SCRIPT ERROR`.
It does not import, so after any new asset or scene run
`/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import`.
Baseline (A7, `9ccf078`, after an import from an empty cache): `evidence/assignment-7/baseline/RUN.txt`.
`test_audio.gd realtime`; at `60`: `test_logic`, `test_gameplay`, `test_defeat_sparks_config`,
`test_extra_particles_config`, `test_particles_state`, `test_particles_edges`, `test_a3_assets`, `test_lantern_gate`,
`test_a3_camera`, `test_materials`; `test_hurt_tint` at 30, 60 and 144. Each extends `res://tests/harness.gd`,
writes `evidence/<suite>.json` and quits 1 on any failure or an unfinished `run()`.
Inject input with `Input.parse_input_event()`. `Input.action_press()` never reaches `_input` or `_unhandled_input`.
Parsed events are delivered on the next process frame, so await `process_frame` before stepping.

# Current change
@CHANGE-BRIEF.md

# Ownership
Bao chose the dash and its rules. Bao plays the build and gives every keep or change verdict, confirms or
changes the phase table, and watches the film. An agent never records a human check as done.
Bao hand-wrote `hurt_tint.gdshader` and `cobblestone_surface.gdshader`. An agent never edits, creates, renames or
deletes any file in `godot/shaders/`, `.uid` files included; it may read them and reference them.

# Headless facts
Confirmed on this Mac, Godot 4.7.2 (`godot/tests/probe_headless_facts.gd`, `evidence/assignment-5/headless-facts/`):
- A headless run draws nothing: `RenderingServer.frame_post_draw` fired 0 times in 288 frames. Frame strips and
  pixel checks need a window.
- `--fixed-fps N` keeps 60 physics ticks per game second: 1 per frame at 60, 2 at 30, 0 or 1 at 144.
  A headless run says nothing about colour or look.

# Out of scope
- Enemies, weapons, pickups, the run state machine in `game_state.gd`, movement speed, health, i-frames, knockback,
  progression numbers and the tick rate. The dash adds rules; it changes none of these.
- Every file in `godot/shaders/`, the particle effects, audio, and the A3 and A5 3D scenes.
- `pc_sheet.png` and every generated asset. No `.import` file written by hand and no invented UID.
- Existing tests and their expectations. New checks go in new test files. An existing pin changes only in its own
  re-pin commit, after play, with the old and new values recorded.
