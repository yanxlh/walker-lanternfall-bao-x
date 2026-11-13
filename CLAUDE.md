@AGENTS.md

# Project context
- Engine: Godot 4.7 (`godot/project.godot:15`), build 4.7.2.stable.official.ed1daf0bf (`README.md:17`).
  Renderer `gl_compatibility` for desktop and mobile (`godot/project.godot:34-35`); nearest canvas filter
  (`godot/project.godot:33`); viewport 640 x 360 shown at 1280 x 720 (`godot/project.godot:19-22`).
- Main scene `res://game/main.tscn` (`godot/project.godot:14`). The session builds the world in code and creates the
  courier with `PlayerScript.new()` (`godot/game/session.gd:66`). The simulation is `tick()` (`godot/game/session.gd:125`),
  called from `_physics_process` (`godot/game/session.gd:115`) while the run is PLAYING, at `TICK_HZ = 60`
  (`godot/features/tuning.gd:4`).
- The player's state machine is in `godot/features/player/player.gd`: visual states `STATES` (`:22`), the dash phase
  table `DASH_TRANSITIONS` (`:24`), `current_state()` (`:175`), `clip_and_time()` (`:198`), `_show()` (`:211`), the dash
  step (`:133`) and hits (`:226`). Dash timings are `DASH_*` in `godot/features/tuning.gd:20-24`.
- Both clips appear in `res://features/player/courier_visual.tscn`, which `player.gd:57` instances under the courier.
  Clip resources: `res://animations/courier_clips.tres`, saved by the headless builder
  `godot/features/player/build_courier_visual.gd`.
  - `walk` (cycle): Sprite2D with an AnimationPlayer frame track on `Body` (`courier_visual.tscn:9`), sheet
    `res://assets/art/pc_sheet.png` (`courier_visual.tscn:3`); clip at `courier_clips.tres:387`.
  - `dash` (committing action): cutout rig `Rig` > `Legs`, `Hips` > `Coat`, `Chest` > `Arm`, `Neck` > `Head`
    (`courier_visual.tscn:17-57`); clip at `courier_clips.tres:43`.
  - One AnimationPlayer (`courier_visual.tscn:65`) with `callback_mode_process = 2`, manual (`courier_visual.tscn:66`).
- Dash input: action `dash` on Shift / Space / B (`godot/game/session.gd:415`), handled in PLAYING
  (`godot/game/session.gd:381`); unlocked by the `dash` card (`godot/features/progression/progression.gd:23,94,137`,
  `godot/game/session.gd:350`).
- The hurt tint puts a ShaderMaterial on the courier (`godot/effects/hurt_tint_presentation.gd:17`); every node of the
  visual uses its parent's material.

## Tests, all through `scripts/run-test.sh`
`./scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]`; the file is in `godot/tests/`; a number adds
`--fixed-fps N`; log in `logs/<test>_<tag>.log`. Exit 1 on a failing suite, a hang (124), `SHADER ERROR`,
`SCRIPT ERROR` or a resource-load failure such as `Failed loading resource` (`scripts/run-test.sh:37-39`);
`scripts/check-run-test.sh` checks the wrapper itself. Import first after a clone or a new asset:
`/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import`.
- `test_audio.gd realtime`; at `60`: `test_logic`, `test_gameplay`, `test_defeat_sparks_config`,
  `test_extra_particles_config`, `test_particles_state`, `test_particles_edges`, `test_a3_assets`, `test_lantern_gate`,
  `test_a3_camera`, `test_materials`; `test_hurt_tint` at 30, 60 and 144 (baseline:
  `evidence/assignment-7/baseline/RUN.txt`).
- A7: `test_courier_pin`, `test_courier_pin_input`, `test_courier_clips`, `test_courier_states` at 60;
  `test_dash_edges` at 30, 60 and 144.
- Inject input with `Input.parse_input_event()`; `Input.action_press()` never reaches `_input` or `_unhandled_input`.

# Current change
@CHANGE-BRIEF.md

# Ownership
- Bao writes CHANGE-BRIEF.md, the phase table, the cycle spec, every prediction and every verdict, approves every
  change before it is made, and runs every capture. An agent never records a human check as done.
- Bao hand-wrote the shaders. An agent never edits, creates, renames or deletes any file in `godot/shaders/`,
  `.uid` files included.
- Clips live as resources in `godot/animations/` or in the scene that owns them, and are never built in code at
  runtime. A headless tool script may build a clip and save it with `ResourceSaver.save()`; the game loads the file.

# One authority
Exactly one node writes to each animated node. Never add a second writer to a node that already has one.
- `Body`, `Rig` and every rig part (`courier_visual.tscn`): only the AnimationPlayer, through its clips.
- The AnimationPlayer: only `player.gd` `_show()` calls `play()` and `seek()` (`player.gd:217-218`).
- `CourierVisual.scale.x` (facing): only `player.gd` `_show()` (`player.gd:215`); no clip keys it.
- The courier's `modulate` (blink): only `player.gd:112`. Its `material`: only the hurt-tint presentation.

# Godot 4 names
Use Godot 4 class and property names for 4.7 only: `Animation.loop_mode`, not a boolean `loop`;
`AnimationMixer.speed_scale`, not `playback_speed`; `AnimatedSprite2D` with `sprite_frames` and `play()`, not
`AnimatedSprite`, `frames` or `playing`. If unsure a property exists in 4.7, say so instead of guessing.

# Sessions and git
- Git: read-only commands (`status`, `diff`, `log`, `show`) at any time. Commit only on the assignment branch, one
  completed step per commit. Never push, tag, reset, rebase, force or rewrite history; Bao pushes.
- After every agent session: read the final `result` event of a `claude -p --output-format stream-json` run (stop
  if `is_error` or not `success`); a desktop session has none, so run `python3 -I scripts/session_check_a7.py
  <session.jsonl> <base> <out.json>`. Then `git diff --stat godot/shaders/` must print nothing, and read
  `git diff scripts/run-test.sh`.
- Resuming an interrupted session: do not continue it. Re-run the tests to establish what is true, read
  `git status --short`, `git diff` and `git log --oneline -10`, and start a new session that states what is done and
  what is not. Bao records the interruption in FRICTIONAL.md.

# Headless facts
Confirmed on this Mac, Godot 4.7.2 (`evidence/assignment-7/headless-facts/probe.log`):
- A headless run advances clips and reads their structure. It draws nothing (`frame_post_draw` 0 times in 30 frames),
  so whether the motion reads is not observable here.
- Key times are 32-bit floats (8/60 reads back as 0.13333334); compare them with a tolerance.
- `value_track_get_update_mode` applies only to value tracks; on a 3D position track it errors and answers
  `UPDATE_CONTINUOUS`.
- Frame strips come from a windowed Movie Maker run, which Bao starts.
- `--fixed-fps N` keeps 60 physics ticks per game second: 2 per frame at 30, 1 at 60, 0 or 1 at 144
  (`evidence/assignment-5/headless-facts/`).

# Out of scope
- Collision, movement speed, health, i-frames, knockback, progression numbers, the tick rate, enemies, weapons,
  pickups and the run state machine (`godot/game/game_state.gd`). The dash adds rules; it changes none of these.
- `godot/shaders/`, the Assignment 6 effects (`godot/effects/`), audio, the A3 and A5 scenes.
- `pc_sheet.png` as committed, and every generated asset. No hand-written `.import` file, no invented UID.
- Existing tests and pins. New checks go in new files; a pin changes only in its own commit, with the reason.
- Presentation code may read game state; it never writes it.

# Unconfirmed
- The course sprite set's path and licence: the assignment page leaves both as placeholders; this project uses its own
  Assignment 2 sheet instead.
- No reference dash has been measured for the phase table.
