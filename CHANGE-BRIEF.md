# Lanternfall — Particle Effects Change Brief

## Project and scope

This change adds two visual effects to Lanternfall, my 2D survival game set in a midnight market. Effect A confirms an enemy kill. Effect B makes the courier's movement easier to follow. Neither effect changes damage, collision, movement, enemy spawning, progression, input, or state-machine timing.

The current source is this game directory. The working snapshot was copied into the course repository at commit `9fa5d88`; no local `a5` tag or prior shader files are present. The previous asset brief is preserved at `design/CHANGE-BRIEF-assignment-2.md`. `godot/game/session.gd` owns the `enemy_killed(pos: Vector2)` signal, player reference, and game state. `godot/game/game_state.gd` defines MENU, PLAYING, LEVELUP, PAUSED, WON, and LOST. `godot/project.godot` sets a 640 × 360 logical viewport, a 1280 × 720 window, and the GL Compatibility renderer. The existing README records Godot 4.7.2.stable.official.ed1daf0bf; the installed executable was confirmed as the same version on 29 October 2026.

The proposed nodes are CPUParticles2D, retaining the existing renderer. Their property names were read from the installed 4.7.2 runtime before building. CPU particle scale uses `scale_amount_min`, `scale_amount_max`, and `scale_amount_curve`. A separate scratch GPU material will be converted for the required process-shader study; it will not replace the CPU effects or be used by gameplay.

## Alignment with the game design document

The reference is the Assignment 4 Game Design Document, version 0.3, dated 17 October 2026. This change supports P-02, Position over firing, by clarifying movement without adding an attack input. It supports P-03, Readable light, by using warm sparks against the cool market and keeping kill feedback understandable without sound.

Both effects retain the hard-edged pixel-art style and nearest-neighbor filtering described in Graphics and Styling. Avoid soft photographic textures or a large opaque glow. The courier and pickups must remain the brightest sustained objects; A may be briefly bright, while B stays subordinate to them. Check that A does not obscure the lamp-oil gem created by the same kill.

The post office, delivery contracts, persistent settlement improvements, additional couriers, and engineer turrets are planned features in the GDD. This assignment adds presentation to the existing three-minute prototype and does not claim to implement those systems.

## Effect A — Enemy-defeat sparks

### Job and trigger

A small burst of warm sparks marks the exact position where an enemy dies. It helps distinguish a kill from an ordinary hit during crowded play. The existing `Session.enemy_killed(pos)` signal supplies the event and position. The presentation layer listens to this signal and does not call `damage()` or change enemy state.

### Visual intent

- First 0.07 seconds: a compact, bright cluster establishes the event position.
- From 0.07 to 0.20 seconds: sparks spread outward and slow down.
- From 0.20 to 0.45 seconds: sparks shrink and fade completely.
- Use a pale yellow centre and orange dissipation against the dark market floor. Check the effect against bright lantern props and puddles as well as the darkest floor.
- The burst should span about one character height initially and no more than two character heights near its widest point. Judge it at the actual 1280 × 720 window size.
- Speed and size vary between particles. Normal gameplay repeats must not use a fixed seed.
- One spark emitter is sufficient initially. Additional layers require a documented design revision.

### Initial settings

| Part | Setting | Initial value |
|---|---|---|
| Node | type | CPUParticles2D |
| Emission | amount | 16 |
| Emission | one_shot | true |
| Emission | emitting at scene load | false |
| Emission | explosiveness | 1.0 |
| Emission | lifetime | 0.45 s |
| Emission | shape | point |
| Process | direction | (1, 0) |
| Process | spread | 180 degrees |
| Process | initial velocity min / max | 25 / 55 logical pixels per second |
| Process | gravity | (0, 12) |
| Process | damping min / max | 20 / 30 |
| Process | scale_amount_min / scale_amount_max | 0.7 / 1.2 |
| Process | scale curve, normalized time:value | 0:1, 0.2:0.85, 1:0 |
| Process | colour ramp, normalized time:RGBA | 0:(1,0.95,0.65,1), 0.35:(1,0.6,0.2,0.85), 1:(0.65,0.2,0.05,0) |
| Draw | texture | new code-generated 3 × 3 hard-edged pixel spark texture |
| Draw | material | CanvasItemMaterial, additive blend |
| Coordinates | local_coords | false |
| Startup | preprocess | 0 |

Store these settings in `godot/effects/defeat_sparks.tscn`. Commit the texture-generation script and its output; do not modify existing source textures.

### Retrigger and lifecycle rules

Use overlap: every accepted event creates a separate burst at the signal's position. Each burst belongs to a persistent presentation root, not the enemy that is about to be freed. Parent motion must not drag previously emitted sparks.

Permit at most 32 live bursts, for a maximum of 512 allocated particles. When all slots are occupied, ignore additional events until a slot is free. This cap is part of the acceptance rule and must be tested explicitly. Two events 0.10 seconds apart must produce two separate live instances below the cap. No burst fires on scene load. Restart clears all old instances. Burst processing freezes outside PLAYING and resumes without replaying the event.

### Preview and evidence

Use a representative portion of the real market floor with the courier visible for scale. Trigger at frame 10; enable a second event at frame 13 for the retrigger fixture. Capture at 30 fps. Read frames 10, 12, 15, 20, 30, and 50. If first visible emission occurs one frame later, record the offset. Label these captures as fixtures.

The configuration test reads every setting above from the instantiated scene and its resources. The state test drives kills through normal gameplay processing and input, rather than directly calling the presentation trigger. Check event position, no emission at load, two-event overlap, cap behavior, restart cleanup, and survival after the enemy is freed. Visibility and readability require my own check in the running game.

## Effect B — Courier lantern trail

### Job and condition

A short trail of fading embers reinforces the courier's direction of travel without hiding nearby enemies. It is a trail, not a second burst. Read the player position and displacement from the existing session. Emit only while the game is PLAYING, the effect is visible, and the player has actually moved. Stop when any condition ends. Actual position displacement prevents emission while input pushes the player against a blocker.

### Visual intent

- First 0.10 seconds after movement begins: a few embers appear close to the courier's feet.
- During steady movement: embers remain behind in world space, making a short broken trail rather than a continuous beam.
- After stopping: stop spawning immediately; existing particles disappear within 0.35 seconds.
- Keep the trail dimmer and smaller than Effect A. Its length should remain around one to two character heights at normal speed.
- Fade from amber to dark orange while shrinking. Vary particle scale and speed slightly.
- Use a spherical emission region with a 3-pixel radius, a process feature absent from A's point emission.

### Initial settings

| Part | Setting | Initial value |
|---|---|---|
| Node | type | CPUParticles2D |
| Emission | amount | 24 |
| Emission | one_shot | false |
| Emission | emitting at scene load | false |
| Emission | explosiveness | 0 |
| Emission | lifetime | 0.35 s |
| Emission | shape / sphere radius | sphere / 3 logical pixels |
| Process | direction / spread | (0,-1) / 25 degrees |
| Process | initial velocity min / max | 2 / 6 logical pixels per second |
| Process | gravity | (0,-4) |
| Process | damping min / max | 1 / 3 |
| Process | scale_amount_min / scale_amount_max | 0.35 / 0.7 |
| Process | scale curve, normalized time:value | 0:0.7, 0.2:1, 1:0 |
| Process | colour ramp, normalized time:RGBA | 0:(1,0.7,0.25,0.55), 0.5:(0.8,0.35,0.08,0.3), 1:(0.3,0.1,0.02,0) |
| Draw | texture | same code-generated spark texture |
| Draw | material | CanvasItemMaterial, additive blend |
| Coordinates | local_coords | false |
| Startup | preprocess | 0 |

Store these settings in `godot/effects/lantern_trail.tscn`. This effect is not a value-driven feedback loop; runtime code does not change `amount`.

### Pause, hiding, and startup

The first scene frame contains no trail because the player has not moved. Preprocessing is zero intentionally: a movement trail must not appear before movement. Freeze particle simulation during PAUSED and LEVELUP. While hidden, stop emission and allow existing particles to expire when simulation is active. On becoming visible, do not replay movement that happened while hidden. Reset the previous-position sample on restart or teleport so neither creates a streak.

### Preview and evidence

Use the same real background and camera scale. Begin movement at frame 10 and stop at frame 40. Inspect frames 10, 12, 20, 39, 40, 45, 51, and 60 at 30 fps. Separate fixtures cover pause/resume and hidden/visible transitions.

Read back every configured value, including the sphere emission shape. Test movement start/stop, pushing against a blocker, paused and hidden behavior, and restart. Check visually that the trail stays in world space and does not cover the player or obscure enemies.

## Predicted failures and checks

1. An obsolete Godot property name leaves a default value. A configuration read-back test should detect the mismatch. Intentionally rename one A property to a Godot 3 name, run the test, inspect the running effect, record the outcome, and restore it.
2. Scene values drift from this brief. Intentionally alter one A value without changing the brief; the configuration test must fail. Restore the original value afterward.
3. A burst disappears with the killed enemy. A state test must confirm the burst remains alive after the enemy is freed.
4. A second kill restarts the first burst. The rapid-repeat fixture and state test must show two independent instances below the cap.
5. The trail emits while stationary or after a teleport. Test the actual-displacement condition and reset behavior.
6. Yellow sparks disappear against bright props. Compare real captures on dark and bright market backgrounds and record my running-game verdict.

## Performance predictions and budgets

| Effect | Peak allocation | Predicted extra headless CPU time | Predicted extra GPU time | Budget |
|---|---:|---:|---:|---|
| A, 32 overlapping bursts | 512 particles | below 0.8 ms/frame | below 0.5 ms/frame | CPU delta ≤ 1.0 ms and GPU delta ≤ 0.75 ms |
| B, continuous movement | 24 particles | below 0.15 ms/frame | below 0.15 ms/frame | CPU delta ≤ 0.25 ms and GPU delta ≤ 0.25 ms |

These are predictions, not measurements. Compare CPU effects on both CPU and GPU time. Measure an empty-scene control, game with effects off, A at its cap, and B during continuous movement. Report means and spread, hardware, engine, renderer, and source revision. Use the Visual Profiler on a real GPU for off/on GPU comparisons. If this renderer or machine does not expose that measurement, record the limitation rather than relabeling CPU time or FPS as GPU time.

A headless run draws no particles. A GPU-particle process therefore has a near-zero headless processing price by construction; that number cannot establish its on-screen cost. CPU particles still perform CPU processing headlessly. Vsync may make off/on FPS identical even when rendering cost differs.

## Tuning and acceptance

For each effect, preserve a first strip and record my first running-game observation. Make at least one observation-driven revision per effect. Before each edit, record the old and new value and predict the visible difference. Change one setting, recapture, compare, and keep or revert after actual play. If kept, append a dated revision here so the scene, test, and brief agree.

Existing tests must retain their assertions and baseline counts. Effects may read gameplay state but never write it. Existing shaders, collision, movement, inputs, state timing, and source textures stay unchanged. Record results only after the corresponding check is performed.

## Revisions

No tuning revision has been performed yet.

### 29 October 2026 — approved event revision and gameplay integration

The confirmed gameplay design now triggers Effect A on every successful weapon hit, including nonlethal hits, rather than only on a kill. The original design above remains as the initial record. The particle values are unchanged; this is an event/design revision, not an observation-driven visual tuning revision. The existing resource and preview filenames `defeat_sparks` are retained to preserve the first fixture and configuration evidence; they now serve the weapon-hit effect.

`Session.damage()` will publish a new read-only `weapon_hit(pos: Vector2)` signal after its existing dead-enemy guard. The listener spawns A at that enemy position. No damage amount, hit detection, cooldown, death order, or input behavior changes. Beam, Lamp-Moths, and Sunflare all use this same existing damage method. The overlap cap remains 32 and includes lethal and nonlethal hits together.

The presentation controller is attached once to Session. It owns transient bursts independently of enemies, clears them on restart and terminal states, and freezes A outside PLAYING. Level-up celebrations use the separate policy below. Tests drive normal physics and real input; fixture setup may seed enemies or place gems but may not invoke the presentation trigger or the damage function directly.

#### Extra effect — level-up celebration

This additional one-shot effect marks each `Session.leveled_up(level)` event at the courier. It does not replace Effect B. It uses CPUParticles2D, 32 particles, one_shot=true, emitting=false at load, lifetime=0.7 s, explosiveness=1, preprocess=0, sphere emission with radius=12, direction=(0,-1), spread=180, initial velocity=35..65, gravity=(0,8), damping=15..25, scale_amount=0.8..1.5, and local_coords=false. Its scale curve is (0,1), (0.25,0.9), (1,0), with the same zero-tangent interpolation as A. Its colour ramp is 0:(1,1,0.8,1), 0.4:(1,0.75,0.2,0.8), 1:(1,0.4,0.05,0). Use the existing generated spark texture, nearest filtering, and an additive CanvasItemMaterial.

It should read as a wider gold celebration around the courier, spread rapidly for the first 0.2 s, then shrink and disappear by 0.7 s. It continues during LEVELUP so the card overlay does not freeze it on its first frame, freezes during PAUSED, and clears on restart, MENU, WON, or LOST. Overlap is allowed up to four celebrations (128 particles), after which further events are ignored until a slot is free. The ordinary A budget remains separate. Predict celebration CPU delta below 0.25 ms/frame and GPU delta below 0.25 ms/frame; budget both at 0.4 ms/frame at four simultaneous bursts. These numbers are unmeasured predictions.

#### Effect B integration details

The approved movement trail uses the settings specified above. Attach its emitter to the presentation root, tracking the courier's global position plus (0,7) logical pixels to place it at the feet. Previously emitted particles stay in world space. Compare actual displacement once per physics frame after Session has stepped. A discontinuity greater than twice the expected per-frame movement plus 4 pixels is treated as a teleport and resets the sample without emission. Stop spawning outside PLAYING; freeze its simulation in PAUSED and LEVELUP. While hidden, stop spawning but allow existing particles to expire whenever the game is PLAYING. Restart clears old particles and resets position history.

Configuration tests read every named setting for all three scenes. State checks cover nonlethal/lethal hits, rapid hit overlap, upgrade celebrations, actual movement, idle, pause, hidden state, and restart. A human still judges whether the effects are visible, distinct, well-sized, and legible behind the card screen and against the real level.
