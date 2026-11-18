# Lanternfall — Animation Change Brief (Assignment 7)

**Current contract: Bao's rewrite of 18 November 2026, the last section of this file.** The text from here to the Revisions is the 13 November agent draft, kept as the original.

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
| Length | 20 / 60 s |
| Loop | `Animation.LOOP_NONE` |

Every clip keys `Body:visible` and `Rig:visible` at 0, so whichever clip plays owns the whole visual. The sprite clips show `Body` and hide `Rig`; `dash` does the opposite.

### Phase table (frames at 60 per second; revision r1, 13 November 2026, requested and kept by Bao; see Revisions)

| Phase | Frames | Ticks | Gameplay | Pose |
|---|---|---|---|---|
| Startup | 0–3 | 4 | the courier stops; input ignored; dash direction already locked | crouch and lean back (anticipation) |
| Active | 4–13 | 10 | moves at `DASH_SPEED` 330 px/s in the locked direction: 5.5 px per tick, 55 px in all | lean hard into the dash, lamp trailing |
| Recovery | 14–19 | 6 | the courier stops; input ignored | settle upright with one overshoot |
| Cooldown | after recovery | 60 | a new dash cannot start | normal states |

Reference: none measured yet. HUMAN: Bao picks a reference dash (a game clip or a Mixamo animation), measures its startup, active and recovery frames, and changes this table if they disagree. The keys follow the table, not the other way round.

### Keys (frame : value; transition)

| Track | Keys |
|---|---|
| `Rig:position` | 0 : (0, 0); 3 : (0, 1); 4 : (0, -1); 14 : (0, 0); 16 : (0, 1); 20 : (0, 0) |
| `Rig/Hips:rotation` | 0 : 0.0; 3 : -0.15; 4 : 0.35; 14 : 0.30; 16 : -0.08; 20 : 0.0 |
| `Rig/Hips/Chest/Neck:rotation` | 0 : 0.0; 3 : 0.10; 4 : -0.30; 10 : -0.20; 14 : -0.25; 16 : 0.15; 18 : -0.05; 20 : 0.0 |

There is a key at every phase boundary (0, 4, 14, 20) on every continuous track. Spacing: keys inside startup use transition 2.0 (ease in, accelerating into the active frames); keys inside recovery use 0.5 (ease out, settling); active keys use 1.0. Rotation is in radians; positive leans forward for a right-facing courier. The whole visual is mirrored with the courier's facing.

## The dash rules

Tuning (`godot/features/tuning.gd`): `DASH_STARTUP_TICKS = 4`, `DASH_ACTIVE_TICKS = 10`, `DASH_RECOVERY_TICKS = 6`, `DASH_SPEED = 330.0`, `DASH_COOLDOWN_TICKS = 60`.

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

### 2026-11-13 — dash phase table r1: 6 / 10 / 12 → 4 / 10 / 6 (requested by Bao)
Bao asked for startup 6 → 4 ticks and recovery 12 → 6 ticks. Active stays at 10 ticks, so the speed (330 px/s) and the distance (55 px) do not change; the 60-tick cooldown after the dash does not change either. The reason given: in r0 the courier stood still in recovery for longer than it moved (12 against 10 ticks), and hits still land in recovery. The proposal text came from a Codex review. No reference dash has been measured.

| Phase | r0 (ticks, seconds) | r1 (ticks, seconds) |
|---|---|---|
| Startup | 6, 0.100 | 4, 0.067 |
| Active | 10, 0.167 | 10, 0.167 |
| Recovery | 12, 0.200 | 6, 0.100 |
| Whole dash | 28, 0.467 | 20, 0.333 |

The keys move with the phases. The boundaries go from 0 / 6 / 16 / 28 to 0 / 4 / 14 / 20, and each inner key keeps its place within its phase: startup frame 4 → 3; active frame 12 → 10; recovery frames 20 and 24 → 16 and 18. Every value and transition is unchanged. The clip and its read-back expectations change together. The behaviour pins (`test_dash_edges.gd`, `test_courier_states.gd`) are re-pinned in their own commit, with the r0 values kept in this table and in git. The r0 captures stay where they are; the r1 captures go in new folders.

### 2026-11-13 — r1 kept (Bao)
Bao's verdict on r1: "Keep 4/10/6." The behaviour pins were re-pinned in their own commit (`eef8ce8`), and the mutation run was repeated on r1. No reference dash has been measured; the r0 values stay in the table above.

## 2026-11-18 — Bao's brief (student rewrite): the current contract

Written by Bao; Bao confirmed in chat on 18 November 2026: "Confirmed, I wrote it." Claude Code added the paragraph breaks and, at Bao's request ("fix those two statements for me"), corrected two statements: the startup "compression" and the "brighter dash rig". The corrections are listed at the end of this section. Every other word is Bao's.

This animation design gives the courier two distinct movement presentations: walking communicates continuous movement, while dashing communicates preparation, active movement, and recovery of control. Walking uses Sprite2D with an AnimationPlayer frame track, alternating between the existing walk_contact and walk_passing poses. This preserves the original pixel art and permits direct readback of frame order, hold duration, and the loop seam. The target is Body in godot/features/player/courier_visual.tscn. In godot/features/player/player.gd, current_state() selects the state, clip_and_time() derives time from walk_ticks, and _show() drives AnimationPlayer.

Dashing uses a cutout rig with separate head, arm, coat, and leg sprites. Pivot rotations and root movement create a slight dip with a backward lean, a forward lean, and recovery. This route allows independent body-part motion while reusing the existing artwork instead of relying only on whole-sprite changes. godot/features/player/build_courier_visual.gd saves the scene and godot/animations/courier_clips.tres; the game loads these resources rather than building animations at runtime.

Both clips use godot/assets/art/pc_sheet.png, generated for this project in Assignment 2 with FLUX.1-schnell. The model licence is Apache-2.0. The image is 320×32 pixels, divided into a 10×1 grid of 32×32 cells without padding. Frame order is 0 turn_front, 1 idle, 2 walk_contact, 3 walk_passing, 4 cast, 5 hurt, 6 levelup, 7 sunflare, 8 defeat, and 9 victory. Source and processing records are in godot/assets/art/ATTRIBUTION.md, gen/log/ART-PC-01/, and gen/mappings/ART-PC-01.json. The source image remains unchanged, and the dash uses regions of cell 2.

Walking alternates cells 2 and 3, holding each for eight simulation ticks in a 16/60-second cycle. It uses Animation.LOOP_LINEAR, Animation.UPDATE_DISCRETE, and Animation.INTERPOLATION_NEAREST. The first key is cell 2 and the last key is cell 3; the final-key-to-end interval is eight ticks, matching the earlier interval. An additional first-frame hold at the end could create a recurring hesitation.

All timing uses 60 simulation ticks per second, with Animation.step = 1/60. This is an editing increment, not the runtime frame rate, and it does not automatically rewrite saved keys.

Dash startup occupies ticks 0–3, dipping one pixel and leaning back while the direction is locked. Active movement occupies ticks 4–13, travelling 55 pixels at 330 pixels per second. Recovery occupies ticks 14–19, returning upright while ordinary movement remains locked. At tick 20, the dash ends, ordinary states resume, and a 60-tick cooldown begins. Existing knockback remains applicable during every phase. Gameplay reads dash_phase, dash_ticks, and dash_cooldown on simulation ticks rather than inferring behavior from the animation. The dash requires an upgrade card and grants no invulnerability. A startup hit cancels without cooldown; an active hit applies damage while the dash continues; a recovery hit cancels the remaining recovery and starts cooldown.

Root-position, hip-rotation, and neck-rotation tracks have keys at boundaries 0, 4, 14, and 20. Startup uses transition 2.0, active movement 1.0, and recovery 0.5.

State priority is override, dash, hurt, cast, walk, then idle. A nonempty override_pose selects the corresponding levelup, sunflare, defeat, or victory clip. A nonempty dash_phase selects dash at dash_ticks/60. The initial hurt period selects hurt, positive cast_ticks selects cast, positive walk_ticks selects walk at (walk_ticks%16)/60, and otherwise idle is selected. Single-frame states use time zero. Legal dash transitions are none to startup, startup to active, active to recovery, and recovery to completion, with hit cancellation also permitted during startup and recovery. Casting has priority over walking but not dashing. The base attack interval is 40 ticks; casting sets an eight-tick counter that decreases during subsequent player steps, producing seven visible casting ticks in the current presentation. Casting frames must therefore be identified through pose=cast, rather than automatically classified as walking-loop errors.

AnimationPlayer alone owns Body.frame, Body/Rig visibility, and keyed rig transforms; _show() alone calls its play() and seek() methods. Facing writes CourierVisual.scale.x, hit flashing writes the courier’s modulate, and the existing material system controls yellow hurt tint. These writers own different properties.

The player uses AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL, with no AnimatedSprite2D or AnimationTree. Both clips are manually positioned from the 60 Hz simulation. Existing timing tests report zero difference between clip time and gameplay tick time and a 15.3-millisecond render/physics sampling span at 144 fps; these measurements come from tests, not visual estimation.

Existing collision, ordinary movement speed, health, invulnerability frames, knockback, enemies, weapons, pickups, simulation rate, A6 effects, audio, source artwork, and existing shaders remain unchanged. Presentation may read gameplay state but must not write it through tracks or presentation code.

Verification maps directly to rules: test_courier_clips.gd checks sheet configuration, paths, keys, loop and update modes, editing step, pivots, and regions; test_courier_states.gd checks priority and clip selection; test_courier_pin.gd, test_courier_pin_input.gd, and pixel pins check preserved presentation; test_dash_edges.gd checks unlocking, input, phases, displacement, damage, cooldown, and clocks at 30, 60, and 144 fps. Strips and live inspection evaluate posture, seams, contrast, and rhythm.

The preview uses the actual market floor, starting at the plaza edge (60,0) and moving right toward the stalls. Capture is 1280×720 at 30 fps. The dash request is sent on tick 10 and startup begins on tick 11. Inspect capture frames 4, 5, 7, 12, and 15 for pre-trigger, startup, active movement, recovery, and completion, confirming phases against frames.log.

Predicted failures and detection methods are: body/background blending, checked through dark-ground full-size and close-up views; an abrupt-looking switch from the dash rig back to the walking sprite, checked through frames 12–15 and continuous playback; the dash pose obscuring hurt feedback, checked through hit/no-hit recordings, iframes, flashing, and yellow tint; coat–leg gaps, checked in both directions during active movement and recovery at normal and enlarged scale; recurring loop hesitation, checked through key intervals and five uninterrupted walking cycles; casting interruptions, identified through pose logs and attack timing; and animation/gameplay disagreement, detected through key readback and multi-rate boundary tests. Passing scripted tests does not complete visual or feel checks. Five uninterrupted walking cycles, hits in each dash phase, dark- and bright-ground readability, and the final keep/change decision still require separately recorded results.

### Short answers (Bao, 18 November 2026)

1. *Which route does each clip use, and what does that route's read-back see that the other route's does not?*

   Walking uses Sprite2D with an AnimationPlayer frame track, alternating Body.frame between cells 2 and 3. Readback checks paths, frame indices, key times, discrete updates, loop mode, and seam spacing. An AnimatedSprite2D route instead checks images, order, and durations in SpriteFrames. Dashing uses a cutout rig saved by a builder. Its readback checks hierarchy, regions, pivots, transform keys, phase boundaries, and easing—information unavailable from a simple sprite-frame list. Both routes still require rendered inspection for clarity and smoothness.

2. *If your frame track is left on continuous updates, what does the sprite show between two keys, and why?*

   With continuous updates and linear interpolation, the track calculates intermediate values and assigns them to the integer frame index. The project probe shows that 2→3 switches early, while 2→6 passes through cells 3, 4, and 5. This selects other sheet images rather than creating intermediate artwork, so the track should use Animation.UPDATE_DISCRETE. Casting poses in the walking strip are logged as pose=cast; they are normal state changes, not interpolation failures. The faulty behavior was established by the probe, not a live failure.

3. *Your brief is in frames at your stated frame rate. What will Animation.step be, and what happens to your key times if you leave it at its default?*

   The brief uses 60 animation frame units per second, so Animation.step should be 1/60 second, approximately 0.0166667. The default is approximately 1/30 second; snapping to that editing grid cannot represent every odd simulation tick, such as tick 3 at 3/60 seconds. However, step is an editing increment, not the runtime frame rate. It does not automatically rewrite saved keys or halve playback speed. The mutation fails because the resource violates the specified editing step.

4. *Which node is the one authority over each animated node, and what else in your project could write to it?*

   AnimationPlayer alone controls Body.frame, Body/Rig visibility, and keyed rig transforms. At runtime, _show() in player.gd alone calls its play() and seek() methods. Other writers own separate properties: facing writes CourierVisual.scale.x, hit flashing writes the courier’s modulate, and hurt presentation controls its material. The strip shows the ordinary sprite switching to the dash rig and back, consistent with the visibility tracks. Poor background contrast does not itself indicate competing writers.

5. *Which tick does each clip advance on, and which tick does gameplay read the fact your committing action's active window depends on? If they differ, what is the largest disagreement in seconds?*

   Both animations follow the 60 Hz simulation: walking uses walk_ticks, and dashing uses dash_ticks. AnimationPlayer uses manual mode and is positioned by _show() rather than advancing independently with rendering. Gameplay evaluates the active window from dash_phase and dash_ticks on physics simulation ticks, where damage is also processed. Existing tests measured zero clip/gameplay-time difference at 30, 60, and 144 fps. At 144 fps, the render/physics sampling span was 15.3 milliseconds, below one approximately 16.7-millisecond simulation tick. The strip shows the action order; the timing measurements come from tests.

6. *For your cycle: what is the seam rule for its track type, and what would a duplicated frame at the wrap look like in play?*

   Walking uses a discrete frame track. The first key is cell 2, the last key is cell 3, and the last-key-to-end interval is eight ticks, matching the preceding interval. An extra first-frame hold at the end could join the next cycle’s opening hold, causing a recurring hesitation. Verification must inspect key times and rendered loop boundaries while distinguishing casting interruptions from loop defects.

7. *If your rig is imported: where does loop mode have to live so that a reimport keeps it, and how will you prove it survived an empty import cache?*

   Imported-rig loop configuration is not applicable because this project saves its cutout scene and animation resources directly. For an imported rig, set the loop mode in the source asset’s Advanced Import Settings and preserve the import configuration instead of modifying only regenerated cached resources. Verify persistence by clearing the .godot import cache, reimporting, and reading back the loop mode, tracks, and keys. The passing empty-cache check establishes reproducibility of the current cutout route, not correctness of an unused imported-rig configuration.

### Still to add (Bao)

- The date the sheet's licence was checked (13 November 2026, recorded in `godot/assets/art/ATTRIBUTION.md`).
- The phase table in the template's form: Phase | Frames | What the player may do | What the game reads, with the frame each phase begins on.

### Corrections made at Bao's request (Claude Code, 18 November 2026)

| Bao's text | Now | Why |
|---|---|---|
| "Pivot rotations and root movement create compression, forward lean, and recovery." | "… create a slight dip with a backward lean, a forward lean, and recovery." | No clip keys scale. Startup keys `Rig:position` y +1 and `Rig/Hips:rotation` −0.15 (`godot/animations/courier_clips.tres`). |
| "Dash startup occupies ticks 0–3, compressing the body and locking direction." | "… dipping one pixel and leaning back while the direction is locked." | Same keys. |
| "an abrupt transition from the brighter dash rig to the darker walking sprite" | "an abrupt-looking switch from the dash rig back to the walking sprite" | Measured: the rig uses only colours of the walk cell, and mean luminance stays between 63.6 and 66.15 across walk and dash frames, at most 2.5 % above walk frame 0 (`evidence/assignment-7/rig-brightness/clip-strips-r1.json`, `scripts/measure_rig_brightness.py`). |
| "dash brightening obscuring hurt feedback" | "the dash pose obscuring hurt feedback" | Same measurement. |
| "“Brightness discontinuity” specifically means the transition from the brightened dash rig to the original walking sprite, not the existing hit flash or yellow tint." | removed | It defined a term on the measured-false premise. |
