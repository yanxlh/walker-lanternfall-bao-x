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

Revisions are listed below in the order they were made. The design above is the initial record.

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


### 29 October 2026 — approved visibility trial r1

Human observation: “The level-up sparks and movement trail are not obvious”. The student approved the following two independent revisions before editing:

- Upgrade celebration: change its draw layer from the world canvas below HUD layer 10 to a dedicated CanvasLayer 11 (`godot/effects/level_up_overlay.tscn`). Synchronize the overlay transform with the world canvas transform so the burst remains aligned with the courier as the camera moves. Its particle settings, lifetime and trigger are unchanged. Predict that it remains visible above the dark upgrade veil and cards instead of being covered.
- Effect B: change only its colour/alpha ramp. At normalized t=0 alpha is 0.95 instead of 0.55; at t=0.5 alpha is 0.70 instead of 0.30; the t=1 alpha remains 0. All RGB values, timing, count, scale and motion remain unchanged. Predict stronger amber visibility from startup through steady movement, with the same stop/fade duration.

This is an approved trial, pending the student's post-change verdict. Earlier source is preserved in `evidence/assignment-6/tuning/r0-source/`. It is source evidence, not a captured frame strip. Before/after windowed captures remain required before claiming a completed tuning cycle.


## 29 October 2026 — approved upgrade portrait anchor

The student requested that upgrade sparks appear on the small character displayed in the upgrade UI instead of at the middle of the screen. This supersedes the earlier world-camera alignment for the celebration only. The shared portrait rectangle is (8,256,96,96); mapping the sprite torso origin (16,23) from its 32-pixel frame gives HUD-local anchor (56,325). The celebration overlay uses the HUD transform, independently of the game camera. The HUD reads the same portrait rectangle as before; its layout and card controls are unchanged. Particle size, count, timing, colour and motion remain unchanged. Movement and hit particles are unchanged. The post-change visual verdict is pending.


### 29 October 2026 — portrait placement kept

The student accepted the upgrade portrait placement after viewing the updated game (“That works”). Keep the celebration at the UI portrait torso, HUD-local (56,325), above the upgrade UI. No additional particle parameter changes are made. The movement-trail visibility trial still awaits its own explicit verdict.


### 29 October 2026 — movement trail accepted

The student explicitly confirmed that the revised movement trail is sufficiently visible. Keep the colour/alpha ramp at alpha 0.95/0.70/0 for t=0/0.5/1, with other values unchanged. This is a running-game verdict. Before/after fixture strips still need to be captured and compared; no such image evidence is claimed by this entry.


### 29 October 2026 — approved Effect A scale trial r1

Observation: the student watched the weapon-hit sparks in the integrated game and reported no problem (“Done; no problem”). The `r0` fixture strip (`captures/defeat_sparks/r0/`) was then read against this brief. The widest point (about 1.6–1.8 courier heights) and the complete fade before 0.45 s match. The initial cluster is smaller than "about one character height": 0.35 courier height on the first visible frame and 0.65 by 0.07 s.

The student approved one change: `scale_amount_max` 1.2 → 1.8. Count, speed, spread, damping, gravity, colour ramp, scale curve, `scale_amount_min` (0.7) and lifetime are unchanged.

Prediction: on the first visible frame the cluster grows from 11 × 12 to about 15 × 15 screen pixels (about 0.45 courier height), with more pure-white pixels. Early sparks are 3–4 pixels wider and the largest sparks are visibly bigger. At 0.20 s the spread stays about 45 pixels wide, with about 1.5 times as many lit pixels. The widest point is about 55–62 pixels, still under two courier heights (68 pixels). Fade timing is unchanged, with no sparks at strip frames 30 and 50. The change is not expected to make the first frame a full character height. A faster initial speed would breach the two-height limit, and sphere emission would remove A's contrast with B.

This is an approved trial, pending the r1 capture comparison and the student's running-game verdict. Pre-change source is preserved in `evidence/assignment-6/tuning/a-r0-source/`.


### 29 October 2026 — Effect A scale r1 kept

The student played the revised game and kept the change (“Keep it; it is clearer”). Effect A's current `scale_amount_max` is 1.8; `scale_amount_min` remains 0.7 and every other value in the initial settings table is unchanged. The scene, `godot/tests/test_defeat_sparks_config.gd` and this entry agree. Comparison: `captures/defeat_sparks/comparison-r0-r1/COMPARISON.md`.

Quoted student feedback in this report is translated into English from the recorded conversation.

---

### 9 November 2026 — approved Effect A colour-ramp trial r2

Observation: the student looked at the weapon-hit sparks in the running game and reported “The hit sparks are not eye-catching enough.” Claude's reading of the kept r1 strip:
- The sparks are bright only until about 0.10 s.
- At 0.20 s they are mid-orange, with 21 of 189 lit pixels bright.
- From 0.30 s they are dark specks.
- The first white frames coincide with the enemy's own hit flash.

The full reading is in `TUNING.md`.

The student approved one change ("Approve"): the colour ramp's middle stop moves from 0.35:(1,0.6,0.2,0.85) to 0.6:(1,0.75,0.3,1.0). The start stop 0:(1,0.95,0.65,1) and the end stop 1:(0.65,0.2,0.05,0) are unchanged. Count, speed, spread, damping, gravity, scale range, scale curve, lifetime and texture are unchanged.

Prediction (full version in `TUNING.md`): the burst stays bright yellow until about 0.27 s instead of 0.20 s. At 0.20 s it is light yellow-orange, with roughly six times as many bright pixels. It then turns orange and disappears by the same frame as before. Footprint and widest point are unchanged.

This is an approved trial, pending the r2 capture comparison and the student's running-game verdict. Pre-change source is preserved in `evidence/assignment-6/tuning/a-r1-source/`.

---

## 8 November 2026 — current design and running-game supplement

Current settings and observations follow. Earlier tables above retain their original values.

### What I want to do

I want players to understand two things without relying on sound: whether an attack connected, and which way the courier is moving. Effect A is a weapon-hit spark burst. Effect B is a trail of embers near the courier's feet. A originally represented kills, but now triggers on every successful hit, including nonlethal hits. It therefore communicates a hit rather than exclusively an enemy's death.

The event is `weapon_hit(pos)` in `godot/game/session.gd`, emitted by `damage()` after the dead-enemy guard. `godot/effects/particle_presentation.gd` listens and creates the visuals. B reads `session.player.global_position`, player speed, and `state.current`, comparing positions across physics frames. Holding a movement key against an obstacle must not produce a trail when the courier has not actually moved.

B is a movement trail, not an ambient effect or a value-driven feedback loop. I do not map health or speed to `amount_ratio`. B uses a sphere emission region with a radius of 3 logical pixels, flattened to a disk in 2D, while A uses point emission. This is their distinct emission feature. Calling B a trail describes its visual role; it does not mean it uses built-in GPU particle trails.

### A: the hit sparks I want to see

I want the hit position to light up first, showing where the attack landed. It should then separate into sparks that shrink, darken, and disappear. The effect should feel brief rather than become a persistent glow that hides enemies or lamp-oil pickups.

- **About 0–0.07 seconds:** a compact pale-yellow cluster marks the hit position. Nearby hits can overlap, but each accepted hit has its own burst.
- **About 0.07–0.20 seconds:** the cluster spreads into distinct yellow-orange sparks that gradually slow down.
- **About 0.20–0.45 seconds:** the sparks turn deeper orange, shrink, and become transparent, leaving no bright residue at the end.

I will judge A against the darkest blue cobblestones and near lanterns, bright stall details, and puddles, rather than only against the editor's gray background. The important difference is luminance, not simply that yellow and blue are different hues. I also need to check whether the hit sparks can be confused with yellow lamp-oil pickups.

I use the courier as the size reference and judge the effect in the actual 1280 × 720 project window. The original target was about one character height at the start and no more than two at maximum spread. Existing r1 strip measurements put the initial cluster at only about 0.41 character heights. I accept this more compact initial cluster after checking it in the running game: its size is appropriate, and the brighter r2 burst makes hits and kills noticeable without obscuring the character. This replaces the original one-character initial-size preference; the historical measurements remain unchanged.

I do not want every burst to have the same pattern. Direction, speed, and size vary, and normal gameplay does not use a fixed random seed. There is no additional random hue or rotation variation; changing color with age is different from randomizing each particle's hue. A has one spark emitter responsible for the short flash, spread, and fade. There are no separate flash or smoke emitters. If play shows that one emitter is insufficient, I will make a separate design change rather than claim that multiple layers already exist.

### B: the movement trail I want to see

When the courier moves, a few small embers should appear near the feet and disappear quickly after stopping. I want them to reinforce movement direction without competing with the courier's lamp head.

- **About 0–0.10 seconds after movement starts:** sparse amber particles appear gradually near the feet rather than filling the trail immediately.
- **During steady movement:** older particles stay behind along the route, forming a short broken line. The visual target is about one to two character heights; I checked the length in the game window and found it appropriate.
- **Within 0–0.35 seconds after stopping:** new emission stops immediately, while existing particles darken, shrink, and disappear. No lasting light path remains.

I will check B on the same dark floor, bright lanterns, stalls, and puddles as A. B should be smaller and more restrained than A, but still visible without enlarging a screenshot. Particles grow slightly at first, then shrink, shift from amber to dark orange, and lose opacity. This gives them more variation over their lifetime than simply fading an otherwise unchanged bright dot. Speed and size have small random ranges. One emitter currently produces the short trail; there is no separate smoke layer.

### Current settings and their visual purpose

A is `godot/effects/defeat_sparks.tscn`; B is `godot/effects/lantern_trail.tscn`. A retains its historical filename, but its event now means a weapon hit.

| Category | Setting | A: current value | B: current value |
|---|---|---|---|
| Node | Type and reason | CPUParticles2D; small particle count, retaining the existing 2D Compatibility rendering path | Same |
| Emission | `amount` | 16 | 24 |
| Emission | `one_shot` / initial `emitting` | true / false | false / false |
| Emission | `explosiveness` / `lifetime` | 1 / 0.45 s | 0 / 0.35 s |
| Emission | Shape | point (0) | sphere (1), radius 3 logical pixels |
| Process | `direction` / `spread` | (1,0) / 180° | (0,-1) / 25° |
| Process | `initial_velocity_min/max` | 25 / 55 | 2 / 6 |
| Process | `gravity` | (0,12) | (0,-4) |
| Process | `damping_min/max` | 20 / 30 | 1 / 3 |
| Process | `scale_amount_min/max` | 0.7 / 1.8 | 0.35 / 0.7 |
| Process | Scale curve, normalized age:multiplier | 0:1, 0.2:0.85, 1:0 | 0:0.7, 0.2:1, 1:0 |
| Process | Color and opacity, normalized age:RGBA | 0:(1,.95,.65,1); .6:(1,.75,.3,1); 1:(.65,.2,.05,0) | 0:(1,.7,.25,.95); .5:(.8,.35,.08,.70); 1:(.3,.1,.02,0) |
| Draw | Texture and filtering | `res://assets/particles/spark.png`, a 3 × 3 hard-edged spark, nearest filtering | Same |
| Draw | Material and blending | CanvasItemMaterial, additive (`blend_mode=1`) | Same |
| Draw | `z_index` | 3 | 1 |
| Coordinates | `local_coords` | false; emitted particles remain in world space | false; old embers remain behind as the courier moves |
| Startup | `preprocess` | 0 | 0; no trail is filled before movement |
| Variation | Fixed seed | Not fixed in normal gameplay; fixed in comparison fixtures | Same |

Velocity is measured in logical pixels per second. Curve points use the scene resources' zero-tangent interpolation. Both effects are 2D, so there are no 3D billboard or mesh settings. They also have no GPU `visibility_rect` or `visibility_aabb`; GPU-only properties must not be assigned to CPU nodes. Configuration tests read the named scene settings above.

### Rules and how I check them

| Rule | Implementation or acceptance condition | Evidence and check |
|---|---|---|
| A responds only to accepted hits | Create a burst on `weapon_hit(pos)` during PLAYING when below the cap; no emission at scene load | `test_particles_state.gd` checks nonlethal and lethal hits produced by normal gameplay, positions, and startup; configuration tests read `emitting=false` |
| Repeated hits do not cut off earlier bursts | Overlap: a new instance per event; two events within one lifetime produce two instances | State tests check instances; the 30 fps fixture triggers at frames 10 and 13, and strips show visual overlap |
| A has a cap | At most 32 live bursts; ignore additional events while full and accept them again after slots are freed | State and edge tests check the cap; peak allocation is 32 × 16 = 512 particles |
| Freeing an enemy does not remove A | A belongs to a persistent presentation root, not to the enemy | State tests check survival after the enemy is freed; check for abrupt disappearance in play |
| Moving A's parent does not drag old sparks | `local_coords=false` keeps emitted particles in world space | Configuration read-back plus a windowed parent-motion fixture; headless state alone cannot prove appearance |
| A handles pause, restart, and terminal states | Speed is zero outside PLAYING; restart, MENU, WON, and LOST clear old bursts | State and edge tests; check that resuming does not replay hits |
| B starts and stops with actual movement | Emit only while PLAYING, visible, and displacement is >0.01 and within the teleport threshold; stop spawning otherwise | State and edge tests cover movement, idle, and pushing against obstacles; strips check the fade after stopping |
| B does not connect teleport positions | Displacement above `player.speed × delta × 2 + 4` is a discontinuity: skip emission that frame and update the sample | Edge tests cover teleports and restart; check for long streaks in play |
| B handles pause and hiding | PAUSED/LEVELUP stops spawning and freezes simulation; hiding stops spawning, while old particles age without drawing during PLAYING; simultaneous pause freezes them | State tests read `emitting` and `speed_scale`; windowed fixtures check hidden/visible transitions for delayed emission |
| Whole-tree pause is distinct | P/Esc changes game state rather than `SceneTree.paused`; inherited default pause processing also stops updates when the tree is paused | `test_particles_tree_pause.gd` checks processing eligibility, frozen player position and emission state, and movement/emission after resume; the GPU-free run does not prove rendered particle appearance |
| B has an empty first frame | At load there has been no movement, `emitting=false`, and no existing trail | Startup state tests and my running-game check: no trail before movement |
| Contrast, size, and obstruction remain acceptable | A does not hide lamp oil; B does not hide the courier or enemies; both read on dark and bright backgrounds | Judge in the actual game window, supported by strips; headless tests cannot prove readability |

Headless tests establish settings, signals, instance counts, and state policies, but do not draw particles. Strips support frame-by-frame comparisons of size, spread, and disappearance. Playing the game shows whether the eye can identify the effect in time, whether bright props interfere, and whether repeated hits become cluttered. These forms of evidence serve different purposes.

### How I read the frame strips

The background must be a real night-market area, with the courier visible as a size reference. Check dark floor and bright props separately. The existing standalone A fixture mainly shows dark floor and does not establish bright-background readability.

For A at 30 fps, let the trigger be T=10. Read T, T+2, T+5, T+10, T+20, and T+40: frames 10, 12, 15, 20, 30, and 50.

| Frame | What I expect to read |
|---|---|
| 10 | A compact initial highlight identifying the position; this is not the maximum-size frame |
| 12 | About 0.067 s: sparks start separating, without becoming an obstruction |
| 15 | About 0.167 s: yellow-orange sparks spreading outward, with shrinking and fading underway |
| 20 | About 0.333 s: sparse dark-orange residue, rather than an intact white cluster |
| 30 | About 0.667 s: A has disappeared |
| 50 | About 1.333 s: no residue or spontaneous new emission |

Use a second event at frame 13 to inspect overlap. Movie Maker filenames start at zero; the existing record places the first visible emission in file 9. Record the offset between filenames and trigger labels rather than treating them as identical times.

For B, movement starts at frame 10 and stops at frame 40. Read 10/12 for startup, 20/39 for the steady short trail and foot position, 40 for stopped spawning, 45 for weakened residue, and 51/60 for disappearance. Capture pause/resume and hidden/visible transitions separately; a steady-state image does not prove the stop policy.

### Failures I expect and how to catch them

1. **A Godot 3 property name silently leaves a default.** Read configurations back. The existing mutation that changes `initial_velocity_min` to `initial_velocity` fails the test; restore the scene before retesting.
2. **A second hit is dropped.** Setting `emitting=true` on one still-emitting one-shot node may not create a new burst. Check for two instances within one lifetime, then inspect the rapid-hit strip.
3. **The burst disappears with its enemy.** Check instance survival after enemy release and look for abrupt disappearance at the kill in play.
4. **Bright backgrounds hide sparks, or sparks resemble lamp oil.** Trigger near lanterns, bright stall details, puddles, and dark cobblestones, comparing luminance and recognition. My running-game check found the effects readable on dark and bright backgrounds without confusing or obscuring pickups.
5. **The trail emits against a wall or bridges a teleport.** Check actual displacement, blocker and teleport edge tests, and strips after movement stops.
6. **Material or layer settings hide correctly simulated particles.** Check a nonempty texture, additive material, draw layer, and opacity curve. The celebration's earlier HUD obstruction illustrates why process and draw checks are separate.
7. **Cost exceeds budget.** Compare matched off/on deltas rather than inferring GPU time from capped FPS. Identify proxy-renderer results explicitly.

### Cost predictions, budgets, and recorded measurements

The predictions retain the original brief's numbers rather than turning known measurements into retrospective predictions. CPU effects are compared on both CPU and GPU cost. Times are ms/frame.

| Effect | Peak allocation | Original CPU prediction / budget | Original GPU prediction / budget | Recorded measurements |
|---|---:|---|---|---|
| A | 32 × 16 = 512 | <0.8 / ≤1.0 | <0.5 / ≤0.75 | October 29: CPU +0.0222; Mobile/Vulkan GPU +0.5392; GPU exceeds the prediction but stays within budget |
| B | 24 | <0.15 / ≤0.25 | <0.15 / ≤0.25 | Same comparison: CPU +0.0030; proxy GPU +0.1077; within budget |
| Upgrade celebration, extra | 4 × 32 = 128 | <0.25 / ≤0.4 | <0.25 / ≤0.4 | Same comparison: CPU +0.0070; proxy GPU +0.9103; GPU exceeds budget |

The GPU figures use a Mobile/Vulkan (MoltenVK) override, not the shipped GL Compatibility renderer. Compatibility returns zero GPU readings on this Mac, indicating unavailable timing rather than zero cost. A also has an unexplained 8.32 ms selected-frame spike in the Visual Profiler; the mean alone does not establish acceptable cost in every case. The November 9 headless CPU deltas for A/B/celebration are +0.0379/+0.0052/+0.0269. They must not be presented as paired measurements with October's GPU results. Methods, trial ranges, and records are in `evidence/assignment-6/cost/FINAL-COMPARISON.md` and the revision 3 section of `TEST-REPORT.md`.

The GPU prices listed above are historical measurements of A before the r2 color-ramp change (r1). Neither the viewport GPU timer nor the Visual Profiler was remeasured for A r2. I reran the headless cost check on r2 and found it within the CPU budget; that does not establish r2 GPU cost. Only the color ramp changed, so I expect similar GPU work, but this is a prediction rather than a new GPU measurement. The directory name `cost/visual-profiler-r2/` refers to the earlier submission revision, not this Effect A r2 color trial.

The subsequent A color-ramp r2 CPU rerun, reported in the supplied November 9 screenshots, gives A +0.0471 ms (budget 1.0), B +0.0068 ms (0.25), and celebration +0.0164 ms (0.4): all CPU deltas are within budget. Full off/on means, trial ranges, and evidence limits are in [TEST-REPORT.md](TEST-REPORT.md#a-color-ramp-r2-reported-headless-cpu-rerun--9-november-2026). Raw benchmark logs were not supplied; the screenshots are preserved in `evidence/assignment-6/cost/a-color-r2-reported-20261109/`. No r2 GPU rerun is implied.

### The extra upgrade celebration

The celebration is separate from B. It listens to `leveled_up(level)` and appears on the small character in the upgrade UI at HUD position (56,325), on CanvasLayer 11. It spreads during the first 0–0.2 seconds, then turns orange and shrinks, disappearing by 0.7 seconds. It should frame the portrait without interfering with card reading. I checked its size and readability in play: it fits the portrait and does not obstruct the cards.

Settings: CPUParticles2D, amount=32, one_shot=true, emitting=false, explosiveness=1, lifetime=.7, sphere radius=12, direction=(0,-1), spread=180°, velocity=35–65, gravity=(0,8), damping=15–25, scale=.8–1.5, scale curve 0:1/.25:.9/1:0; RGBA ramp 0:(1,1,.8,1)/.4:(1,.75,.2,.8)/1:(1,.4,.05,0). Texture and additive material match A; local_coords=false and preprocess=0. Allow at most four overlapping celebrations. Continue during LEVELUP, freeze during PAUSED, and clear on restart and terminal states. I accepted the portrait position earlier; that does not establish compliance with the performance budget.

### Boundaries

Collision, movement, input, the state machine and its timing, existing test expectations, Assignment 5 hand-written shaders, and all other objects remain unchanged. Presentation reads game state without writing it.

### A's problem, tuning prediction, and decision

I find the hit sparks insufficiently noticeable. This trial addresses recognition of hit feedback, rather than increasing particle count or total lifetime.

Claude's r1 strip reading is that the initial white cluster coincides with the enemy's hit flash; by about 0.20 seconds the sparks are mid-orange, with only 21 of 189 lit pixels meeting its brightness threshold; by about 0.30 seconds mostly dark specks remain. Detailed measurements are in `TUNING.md`. This supports examining whether the bright phase is too short, while strip measurements and subjective gameplay impressions remain separate records.

The November 9 trial changes only `color_ramp`: move its middle stop from normalized age .35, RGBA (1,.6,.2,.85), to .6, RGBA (1,.75,.3,1). Keep the start and end stops, count, velocity, spread, scale curve, texture, and 0.45-second lifetime unchanged. Pre-change resources are preserved in `evidence/assignment-6/tuning/a-r1-source/`.

I predict that the sparks will remain bright yellow-orange briefly after spreading instead of quickly becoming dark specks. File 12 should be paler and brighter. File 15 should retain an extent of about 45 × 43 pixels, but its bright-pixel count should rise from 21 to at least 120. File 18 should retain clearer orange residue; files 30 and 50 should remain empty. These were the predictions for the comparison. My running-game decision: I am keeping r2 because the sparks are more noticeable and make attack feedback clearer. When a monster is killed, the burst also helps me notice the kill. The same effect appears on nonlethal hits, so I read it as hit feedback rather than proof of a kill on its own.

A's maximum scale was previously increased from 1.2 to 1.8 and kept. For B, the observation that the trail was not obvious led to an opacity-ramp change from .55/.30/0 to .95/.70/0, which was then kept. Both histories are in `TUNING.md`.

### My visual check

When hits arrive rapidly, I can still recognize the repeated spark bursts. They overlap without becoming a solid bright patch that hides enemies or pickups. The brighter r2 sparks make successive hits easier to notice.

When I stop moving, B stops producing new embers. The few embers already behind the courier fade away quickly rather than leaving a persistent line. When I pause, the remaining sparks and trail stay frozen instead of continuing to move or fade. After I resume, they continue normally, and the trail follows movement again without an extra burst or a long streak.

The recorded project launch window is 1280 × 720.

I checked the effects in the running game. B has no trail before I start moving. A and B remain readable on both dark floor and bright parts of the market. Their sizes feel appropriate relative to the courier, and they do not obscure the courier, enemies, or pickups. The upgrade sparks fit around the small portrait without obstructing the cards.

Hidden-state behavior was checked through the scripted windowed capture, not by a manual in-game toggle: the game has no hide/show control. See `captures/play-checks/20261029-142138/pause-hidden+08.png`, `shown+08.png`, and `PLAY-CHECKS.md`. State tests supplement those screenshots.

### Six short answers

1. **Node types and unavailable features.** A and B use CPUParticles2D. A November 9 check of the installed Godot 4.7.2 `ClassDB.class_get_property_list` found `emission_shape` and `scale_amount_min`, but no `amount_ratio`, `visibility_rect`, `sub_emitter`, or `trail_enabled`; the GPU node has the latter four. Using those features would require a separate design, not copying GPU properties onto a CPU node. The online [CPU class reference](https://docs.godotengine.org/en/stable/classes/class_cpuparticles2d.html) is supplementary; the version-specific 4.7 page was inaccessible during this check.
2. **Parent movement.** With `local_coords=false`, already-emitted A particles remain in world space instead of following parent translation. Camera movement still changes their screen positions.
3. **Retriggering and peak count.** Each accepted hit creates a new instance, up to 32 live bursts and 512 allocated particles. Further events are ignored at the cap. This is a capacity limit, not a guarantee that all 512 particles are visible in every frame.
4. **Headless GPU cost and vsync.** Headless mode does not draw particles or execute GPU particle processing, so that GPU-effect workload has near-zero headless cost, although node and script management can still cost CPU time. A and B are CPU nodes and still simulate headlessly. My prediction with vsync enabled is that effects off and effects on both read the display refresh rate, provided each frame finishes within that refresh interval: for example, 60/60 FPS on a 60 Hz display. Either can fall below that rate if it misses the frame budget. The refresh cap can therefore hide the extra particle cost; compare CPU and GPU frame times instead. This is a prediction, not a measured FPS result.
5. **B at startup, with preprocessing, paused, and hidden.** With `emitting=false, preprocess=0`, there is no trail on the first frame. A nonzero preprocess value alone does not satisfy the movement condition or establish a trail at load. A separate continuously emitting, prewarmed fixture would start populated, while its non-prewarmed counterpart would fill from empty. No new windowed comparison of that toggle is recorded. Game pause/level-up stops spawning and freezes particles. Hidden during PLAYING, the effect does not draw or spawn, while old particles expire. Whole-tree pause must be recorded separately from game-state pause.
6. **Emission, process, and draw settings.** Emission determines how many particles are born, when, and where: amount, one_shot, explosiveness, lifetime, and emission_shape. Process controls subsequent motion and change: velocity, direction, spread, gravity, damping, and color/opacity/scale curves. Draw controls presentation: texture, CanvasItemMaterial, additive blending, filtering, and layers. local_coords is a coordinate policy; preprocess is a startup policy.

### The process shader

See [The process shader in TEST-REPORT.md](TEST-REPORT.md#the-process-shader) for the explanation and line references connecting the study shader to this brief.


### Current verification results

See [current r2 validation](evidence/assignment-6/current-r2-validation/README.md): nine suites, 327 assertions, zero failures; both A mutations exit 1. The current-source CPU and windowed GPU raw logs are now archived. GPU timer variability prevents a new budget conclusion; the editor Visual Profiler still needs a current r2 capture. This supersedes earlier statements that no current-source CPU raw logs or GPU timer rerun exist.


### Current editor GPU screenshots

Current A r2 and B off/on Visual Profiler screenshots are available in [current r2 Visual Profiler captures](evidence/assignment-6/cost/visual-profiler-a-r2-current/README.md). The initial A selected-frame delta is +0.69 ms, but a later matched-layout pair gives +4.59 ms; B's selected-frame delta is -1.40 ms. These variable readings do not establish a typical GPU cost or a new budget pass. They supersede the earlier statement that no current r2 editor captures exist; historical prices and their revision labels remain unchanged.
