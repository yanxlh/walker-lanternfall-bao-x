# Lanternfall — Animation Change Brief (Assignment 7)

Date: 13 November 2026. This brief is the contract for the Assignment 7 change. It replaces the Assignment 5 brief, which stays in git history (`9ccf078:CHANGE-BRIEF.md`).

Provenance: Bao chose the committing action and its rules in chat on 13 November 2026 (quoted under "Design decisions"). Claude Code drafted the rest of this brief from those decisions and from the project files, including the phase table, which is a draft for Bao to confirm or change after playing. Sections marked HUMAN are Bao's to perform or judge.

Engine: Godot 4.7.2.stable.official.ed1daf0bf, renderer `gl_compatibility` (`godot/project.godot`). Use Godot 4 names only: `Animation.loop_mode` (not `loop`), `AnimationMixer.speed_scale` (not `playback_speed`), `AnimatedSprite2D.sprite_frames` and `play()` (not `frames` and `playing`). If unsure that a property exists in 4.7, say so instead of guessing.

## Design decisions (Bao, 13 November 2026)

> "Add a dash. The dash is not invincible, but there is a time gap between every two dashes, and the dash has to be obtained through an in-game level-up card."

- The committing action is a dash.
- Hits during a dash are accepted as usual: damage, i-frames and knockback all apply.
- After every dash there is a cooldown before the next dash can start.
- The dash is locked at the start of every run and unlocked by a new level-up card.

## Project facts

- The courier has no scene. `godot/game/session.gd` creates it with `PlayerScript.new()` and calls `player.step()` once per simulation tick from `tick()`, which runs only in PLAYING, from `_physics_process` at 60 ticks per second (`godot/features/tuning.gd` `TICK_HZ`).
- Today the courier draws itself in `_draw()` with `draw_texture_rect_region` from the 32 px cells of `res://assets/art/pc_sheet.png`, choosing the cell from `pose` (`godot/features/player/player.gd`, `POSES`, `choose_pose()`). There is no AnimationPlayer anywhere in the game.
- The hurt tint (Assignment 5) assigns a `ShaderMaterial` to `player.material` (`godot/effects/hurt_tint_presentation.gd`). Anything that draws the courier must use that material.
- Without the sheet (`Art.disabled`), the courier draws a placeholder from `pose`; `test_gameplay.gd` checks that a missing asset changes only the look.

## Clip 1 — `walk` (looping sprite cycle, player state machine)

| Item | Value |
|---|---|
| Route | Sprite2D with an AnimationPlayer frame track |
| Node | `Body` (Sprite2D) in `res://features/player/courier_visual.tscn` |
| Sheet | `res://assets/art/pc_sheet.png`, 320 x 32 px |
| Cell size, grid | 32 x 32 px, 10 columns x 1 row (`hframes = 10`, `vframes = 1`), no padding, no margin |
| Frame order | 0 turn_front, 1 idle, 2 walk_contact, 3 walk_passing, 4 cast, 5 hurt, 6 levelup, 7 sunflare, 8 defeat, 9 victory (the order of `POSES` in `player.gd`) |
| Registration | `centered = false`, `offset = (-16, -23)`: cell pixel (16, 23) sits on the courier's origin, the centre of the r = 10 hurtbox (`SPRITE_ORIGIN`) |
| Frames | 2 (walk_contact), 3 (walk_passing) |
| Frame rate | each frame held 8 ticks at 60 ticks per second (7.5 frames per second) |
| Keys | frame 2 at 0 / 60 s, frame 3 at 8 / 60 s |
| Length | 16 / 60 s |
| Loop | `Animation.LOOP_LINEAR` |
| Update mode | `Animation.UPDATE_DISCRETE` |
| Seam rule | frame track: no duplicate frame across the wrap (last key 3, first key 2), and the gap from the last key to the length (8 / 60 s) equals the key interval (8 / 60 s) |

The other sprite states get one-key clips on the same frame track, `LOOP_NONE`, length 1 / 60 s: `turn_front` 0, `idle` 1, `cast` 4, `hurt` 5, `levelup` 6, `sunflare` 7, `defeat` 8, `victory` 9.

Source and licence: the sheet is the project's own generated art from Assignment 2 (ART-PC-01; `ASSET-LOG.md`, `gen/mappings/ART-PC-01.json`, `SOURCES.md`). It is already committed and follows Assignment 2's rules; no found sheet is used. The file is not edited for this change; the rig below uses region rectangles of it, not a derivative file.

Registration check (measured from the PNG, 13 November 2026): the two walk cells have the same foot line (y = 31), coat centroids (16.2, 22.3) and (16.3, 22.5), lamp centroids (20.0, 14.8) and (20.2, 14.7). The drift is under one pixel, so no offset track is needed. The frame strip must confirm this.

The cells the courier shows today must not change. The pin decides what "today" is, tick by tick, including when the first walk frame appears and how long it holds.

## Clip 2 — `dash` (committing rig action, player state machine)

| Item | Value |
|---|---|
| Route | Cutout rig, baked from code: `res://features/player/build_courier_visual.gd` runs headless, builds the rig and every clip, and saves the scene and the clip library with `ResourceSaver.save()`. Both files are committed; the game and the tests load the saved files, never the builder. |
| Rig | `Rig` (Node2D) > `Legs` sprite and `Hips` (Node2D pivot) > `Coat` sprite and `Chest` (Node2D pivot) > `Arm` sprite and `Neck` (Node2D pivot) > `Head` sprite. Each part draws before the pivots beside it. |
| Parts | region rectangles of pc_sheet cell 2 (walk_contact), cell-local: Head x 17–24, y 8–19; Arm x 12–16, y 13–19; Coat x 11–24, y 20–27; Legs x 11–24, y 28–31. The rectangles do not overlap and cover every opaque pixel of the cell. |
| Pivots (cell-local) | Hips (16, 27), Chest (16, 20), Neck (18, 19) |
| Keyed properties | `Rig:position`, `Rig/Hips:rotation`, `Rig/Hips/Chest/Neck:rotation`, and `Body:visible` / `Rig:visible` (discrete) |
| Length | 28 / 60 s |
| Loop | `Animation.LOOP_NONE` |

Every clip keys `Body:visible` and `Rig:visible` at 0, so whichever clip plays owns the whole visual. The sprite clips show `Body` and hide `Rig`; `dash` does the opposite.

### Phase table (frames at 60 per second; Claude's draft, HUMAN: Bao confirms or changes it after playing)

| Phase | Frames | Ticks | Gameplay | Pose |
|---|---|---|---|---|
| Startup | 0–5 | 6 | the courier stops; input ignored; dash direction already locked | crouch and lean back (anticipation) |
| Active | 6–15 | 10 | moves at `DASH_SPEED` 330 px/s in the locked direction: 5.5 px per tick, 55 px in all | lean hard into the dash, lamp trailing |
| Recovery | 16–27 | 12 | the courier stops; input ignored | settle upright with one overshoot |
| Cooldown | after recovery | 60 | a new dash cannot start | normal states |

Reference: none measured yet. HUMAN: Bao picks a reference dash (a game clip or a Mixamo animation), measures its startup, active and recovery frames, and changes this table if they disagree. The keys follow the table, not the other way round.

### Keys (frame : value; transition)

| Track | Keys |
|---|---|
| `Rig:position` | 0 : (0, 0); 4 : (0, 1); 6 : (0, -1); 16 : (0, 0); 20 : (0, 1); 28 : (0, 0) |
| `Rig/Hips:rotation` | 0 : 0.0; 4 : -0.15; 6 : 0.35; 16 : 0.30; 20 : -0.08; 28 : 0.0 |
| `Rig/Hips/Chest/Neck:rotation` | 0 : 0.0; 4 : 0.10; 6 : -0.30; 12 : -0.20; 16 : -0.25; 20 : 0.15; 24 : -0.05; 28 : 0.0 |

There is a key at every phase boundary (0, 6, 16, 28) on every continuous track. Spacing: keys inside startup use transition 2.0 (ease in, accelerating into the active frames); keys inside recovery use 0.5 (ease out, settling); active keys use 1.0. Rotation is in radians; positive leans forward for a right-facing courier. The whole visual is mirrored with the courier's facing.

## The dash rules

Tuning (`godot/features/tuning.gd`): `DASH_STARTUP_TICKS = 6`, `DASH_ACTIVE_TICKS = 10`, `DASH_RECOVERY_TICKS = 12`, `DASH_SPEED = 330.0`, `DASH_COOLDOWN_TICKS = 60`.

- Input: a new action `dash` on Shift and Space (keyboard) and B (joypad). `session._unhandled_input` turns a press into a request only in PLAYING; `player.step()` consumes it on the next tick. A press while locked, during a dash or during the cooldown is dropped, not queued. Space still starts a run from the menu.
- Direction: the movement input at the tick the dash starts, normalised; with no input, the facing direction. Facing follows the dash direction's x the same way it follows movement. Both stay locked until the dash ends.
- Unlock: a new card `dash`, "Courier's Dash", offered while the dash is locked. Choosing it unlocks the dash for the rest of the run; `start_run()` locks it again.
- Not invincible: `take_hit()` is unchanged. Knockback still adds to movement in every phase.
- Interrupts:

| Phase | Accepted hit | Level-up, pause | Death | Restart |
|---|---|---|---|---|
| Startup | cancels the dash; no cooldown starts | the dash freezes with the simulation and resumes on the same tick | `defeat` | dash, cooldown and unlock cleared |
| Active | the dash continues; damage, i-frames and knockback apply | same | `defeat` | same |
| Recovery | cancels the rest of the recovery; the cooldown starts | same | `defeat` | same |

- Cooldown: starts on the tick the dash ends, whether recovery completes or a hit cancels it, and lasts 60 ticks. A press on the last cooldown tick is dropped; a press on the next tick starts a dash.
- Walls: the arena clamp and the market blocker apply during the dash exactly as during walking.
- Weapons keep firing during a dash. The dash pose has priority over the cast pose.

## State machine and authority

One authority: `player.gd` is the only code that calls `play()` or `seek()` on the courier's AnimationPlayer. Nothing else keys or sets `Body.frame`.

Visual priority, highest first: override (`levelup`, `sunflare`, `defeat`, `victory`, set by the session through `set_override()`) > dash (startup, active, recovery) > `hurt` > `cast` > `walk` > `idle`. Hits cancel startup and recovery, so `hurt` shows after those; during active the dash pose stays and the existing blink and tint show the hit.

| State | Clip | Clip time |
|---|---|---|
| idle, cast, hurt and the overrides | the one-key clip of the same name | 0 |
| walk | `walk` | walk ticks mod 16, divided by 60 |
| dash (any phase) | `dash` | dash ticks since the press, divided by 60 |

## Two clocks

- The courier's AnimationPlayer uses `callback_mode_process = ANIMATION_CALLBACK_MODE_PROCESS_MANUAL`. It never advances on the idle or physics clock by itself. `player.step()` (one physics tick) and `set_override()` select the clip and `seek()` it to the time in the table above, computed from integer tick counters. A paused, level-up, won or lost simulation therefore freezes the animation.
- There is no AnimatedSprite2D, no AnimationTree and no method track.
- No gameplay fact is keyed in a clip. Gameplay reads dash phases from the tick counters and `Tuning`; the read-back test pins the clip's boundary keys to the same tick times.
- Input arrives on the process side (`_unhandled_input`) and is consumed on the next physics tick.

## Checks

| Check | How |
|---|---|
| Pin (before any change) | `test_courier_pin.gd` at 60: the cell shown, the mirroring and the tint path, tick by tick, for walking, stopping, cast, hurt, level-up, evolve, defeat, victory, restart and the missing-art placeholder. It passes on the unchanged code and must pass unchanged after the refactor. |
| Pixel pin | `capture_courier_pin.gd` (windowed): the same scripted ticks captured before and after the refactor; the crops must match pixel for pixel. |
| Read-back | `test_courier_clips.gd` at 60: every track resolves to a real node and property; key times match this brief; loop modes; discrete frame tracks with every key below `hframes * vframes`; the seam rule; a key at every phase boundary; transitions; `callback_mode_process`; the region rectangles. |
| State machine structure | `test_courier_states.gd` at 60: the state table against the clips and the code. |
| Edges | `test_dash_edges.gd` at 30, 60 and 144: the rules above at every phase boundary, through `Input.parse_input_event`. |
| Mutations | in a `git worktree`: a frame track set to continuous, a track path renamed, the walk loop mode changed, a phase key moved one frame; each must fail the read-back. |
| Frame strips | Movie Maker at 60 fps with `--debug-collisions`, one PNG per tick and one log line per tick, for the walk cycle and the dash. |
| HUMAN | Bao plays at normal speed and with `--time-scale 0.25` and says, in visual terms, whether the walk cycle and the dash read, whether the cooldown gap is felt, and whether any registration drift shows. Keep or change the phase table. |

Existing tests and their expectations are not changed to make the new code pass. If the dash card changes a seeded card sequence that an existing test pins, that test is re-pinned in its own commit, after play, with the old and new values recorded.

## Out of scope

- Enemies, weapons, pickups, progression numbers other than adding the card, movement speed, health, i-frames, knockback, the tick rate and the run state machine in `game_state.gd`.
- Every file in `godot/shaders/` (never edited by an agent), the particle effects and their scenes, audio (no dash sound), the A3 and A5 3D scenes.
- `pc_sheet.png` and every other generated asset. No `.import` file written by hand; no invented UID.

## Revisions

### 2026-11-13 — the legs hang from the rig root
The first version put `Legs` under `Hips`, so leaning the hips would also have swung the feet. `Legs` now hangs from `Rig`, so the lean pivots above planted feet. Regions, pivots and keys are unchanged.

### 2026-11-13 — a clip for every cell
`turn_front` (cell 0) gets a one-key clip too. The game never selects it, but `set_override()` accepts any name in `POSES` (the storyboard capture `godot/tests/capture.gd` shows all ten), and a missing clip would leave the previous cell on screen.
