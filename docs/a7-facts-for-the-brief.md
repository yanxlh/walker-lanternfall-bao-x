# Assignment 7 — facts from the code, for Bao's CHANGE-BRIEF.md

Claude Code read these from the repository at `f86b625` (13 November 2026), for Bao to use while rewriting the brief. This is not the brief. It holds no prediction, verdict or answer. Choices still open to Bao are marked **Bao**.

## The two clips

| | `walk` | `dash` |
|---|---|---|
| Object | the courier (player) | the courier (player) |
| Node | `Body` (Sprite2D), `godot/features/player/courier_visual.tscn:9` | `Rig` and its parts, `courier_visual.tscn:17-57` |
| Scene | `courier_visual.tscn`, instanced under the courier by `godot/features/player/player.gd:57`; the courier lives in `res://game/main.tscn` | same |
| Route | Sprite2D with an AnimationPlayer frame track | cutout rig, baked from code (`godot/features/player/build_courier_visual.gd`, `ResourceSaver.save()`) |
| Clip resource | `godot/animations/courier_clips.tres:387` | `godot/animations/courier_clips.tres:43` |
| Cycle or commit | cycle | committing action |
| Authority | the AnimationPlayer (`courier_visual.tscn:65`), driven only by `player.gd` `_show()` (`:211-218`) | same |
| State it reads | `current_state()` == `"walk"` (`player.gd:175`), from `walk_ticks` | `dash_phase` != `""`, from `dash_ticks` |
| What it communicates, why the player needs it | **Bao** | **Bao** |
| Why this route | **Bao** | **Bao** |

## The sheet

- `godot/assets/art/pc_sheet.png`, 320 × 32 px, the project's own generated sheet (ART-PC-01). Credits, model, licence (Apache-2.0, checked 13 November 2026) and SHA-256: `godot/assets/art/ATTRIBUTION.md`.
- Cell 32 × 32 px; grid `hframes = 10`, `vframes = 1`; no padding. Frame order: 0 turn_front, 1 idle, 2 walk_contact, 3 walk_passing, 4 cast, 5 hurt, 6 levelup, 7 sunflare, 8 defeat, 9 victory (`player.gd:15-16`).
- Registration measured from the PNG: walk cells 2 and 3 have the foot line at y = 31; coat centroids are (16.2, 22.3) and (16.3, 22.5). The drift is under one pixel.
- The file as committed is the editable source: it is generated, not downloaded. Its prompts and mapping are in `gen/log/ART-PC-01/` and `gen/mappings/ART-PC-01.json`.

## Cycle spec facts (`walk`)

- 2 frames (cells 2, 3), each held 8 ticks at 60 ticks per second: 7.5 frames per second; length 16 / 60 s.
- `loop_mode = Animation.LOOP_LINEAR` (`courier_clips.tres:389`); frame track `UPDATE_DISCRETE`, `INTERPOLATION_NEAREST`.
- Frame-track seam, measured by the read-back (`walk-seam`): first key 2, last key 3; gap from the last key to the length 8 frames = key interval 8 frames.

## Phase table facts (`dash`, revision r1)

- Rate 60 per second. `Animation.step` = 1 / 60 s; it is stored as `0.016666668` (`courier_clips.tres:45`). The default step is 1 / 30 s.
- Phases begin on frame 0 (startup, 4 frames), 4 (active, 10 frames) and 14 (recovery, 6 frames). The dash ends on frame 20. Ticks are in `godot/features/tuning.gd:20-24`.
- What the code lets the player do: in startup and recovery the courier does not move and movement input is ignored. In active it moves 5.5 px per tick (330 px/s) in the direction locked on frame 0. A dash press during a dash or the 60-tick cooldown is dropped (`player.gd:123-165`).
- What the game reads, and when: `dash_phase` and `dash_ticks`, advanced in `player.step()` on the physics tick (`player.gd:88`, `:133`), and hits in `session._step_enemies()` on the same tick (`godot/game/session.gd:313-321`). No gameplay fact is keyed in a clip, and there is no method track.
- Interrupts, as built (`player.gd:226` and below): a hit in startup cancels with no cooldown; in active the dash carries on (damage and i-frames apply); in recovery the hit cancels and the cooldown starts. A level-up, pause, win or loss freezes the dash with the simulation.
- Keys: 0 / 3 / 4 / 14 / 16 / 20 on `Rig:position` and `Rig/Hips:rotation`; 0 / 3 / 4 / 10 / 14 / 16 / 18 / 20 on `Rig/Hips/Chest/Neck:rotation`. Transitions 2.0 in startup, 1.0 in active, 0.5 in recovery.
- r0 was 6 / 10 / 12 (CHANGE-BRIEF Revisions). No reference dash has been measured: **Bao**.

## State machine facts

Visual states in priority order (`player.gd:22`); the first whose condition holds is shown:

| State | Condition (`player.gd:175`) | Clip, time |
|---|---|---|
| override | `override_pose != ""`, set by the session: levelup (`session.gd:154`), sunflare (`:361`), defeat (`:373`), victory (`:149`); cleared at `:147` and `:338` | the clip of that name, 0 |
| dash | `dash_phase != ""` | `dash`, `dash_ticks / 60` |
| hurt | `iframes > 48 - 12` | `hurt`, 0 |
| cast | `cast_ticks > 0` | `cast`, 0 |
| walk | `walk_ticks > 0` (moving and not dashing) | `walk`, `(walk_ticks % 16) / 60` |
| idle | otherwise | `idle`, 0 |

Dash phase transitions (`DASH_TRANSITIONS`, `player.gd:24`):
- `""` → startup: a press accepted while `can_dash()`, consumed on the next tick.
- startup → active: `dash_ticks` reaches 4.
- startup → `""`: an accepted hit.
- active → recovery: `dash_ticks` reaches 14.
- recovery → `""`: `dash_ticks` reaches 20, or an accepted hit (the cooldown starts).

No AnimationTree, so there is no `advance_expression_base_node` or `advance_mode`.

## Two clocks facts

- One AnimationPlayer, `callback_mode_process = 2` (manual, `courier_visual.tscn:66`). It moves only when `_show()` seeks it, which happens in `player.step()` on the physics tick and in `set_override()`. There is no AnimatedSprite2D.
- Measured by `two-clocks-at-<rate>` in `test_dash_edges.gd`, on every rendered frame of a real-loop dash:
  - clip position against the gameplay tick: 0 s at 30, 60 and 144 fps;
  - render frame against physics step: a span of 0 s, 0 s and 0.0153 s at 30, 60 and 144 fps. That is under one tick (0.0167 s).

## Other writers that exist near the courier

- `player.gd:215` writes `CourierVisual.scale.x` (facing); no clip keys it.
- `player.gd:112` writes the courier's `modulate` (blink).
- The hurt tint writes the courier's `material` (`godot/effects/hurt_tint_presentation.gd:17`).
- `godot/tests/capture.gd:25` calls `set_override()` for every pose. It is a capture script, not the game.

## Evidence that exists for each rule

| Rule | Check |
|---|---|
| tracks resolve, key times, step, loop modes, discrete, frames inside the sheet, seam | read-back `test_courier_clips.gd` |
| states, priority, clips per state, one authority in source, tuning = clip boundaries | structure `test_courier_states.gd` |
| what the courier showed before the change still holds | pins `test_courier_pin.gd`, `test_courier_pin_input.gd` |
| dash rules, interrupts before/on/after each boundary, two clocks | edges `test_dash_edges.gd` at 30, 60, 144 |
| the motion reads; the cycle wraps cleanly; no drift; readable over dark and light ground | frame strip (`scripts/capture-strip.command`) and Bao in the running game |

## Frame strip facts

- Preview: `godot/previews/courier_preview.tscn`. Background: the real market ground; the courier starts at (60, 0), the plaza edge, walking right into the stalls. The dash key is parsed on tick 10, so the dash starts on tick 11.
- At 30 fps, frame N shows tick 2N + 1. The kept frames are 4 (before), 5 (trigger, dash frame 0), 7 (active begins), 12 (recovery begins) and 15 (dash ended): headless smoke test, not a capture.

## Facts the seven short answers can point at (answers are Bao's)

- Continuous frame track, `probe_godot3_names.gd`: keys 2 → 3 show 2,2,2,2,3,3,3,3,3 over 0–8 frames; keys 2 → 6 sweep through 2,3,3,4,4,5,5,5,6.
- `Animation.step` left at the default 1/30: the mutation `walk-step-left-at-default` fails `walk-step` (`evidence/assignment-7/mutations/mutations-required.json`).
- Godot 3 names in 4.7.2: `loop = true` loads as `LOOP_LINEAR` (it loops); `playback_speed` and `playing` are ignored (`evidence/assignment-7/godot3-names/probe.json`).
- The rig is not imported, so question 7 concerns a route this project does not use. The empty-cache mutation passes (`required-4-reimport-from-empty-cache`).
