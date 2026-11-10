# TEST-REPORT

## Current correction status

Current wrapper run: **327 assertions, zero failures across nine suites**; two deliberate A mutations fail as expected. Current r2 raw CPU/GPU timer outputs, copied-source hashes and limits are in [current r2 validation](evidence/assignment-6/current-r2-validation/README.md). Human observations and r2 acceptance appear under “My running-game check and r2 decision.” The process explanation is under “The process shader.” Older dated sections retain their original measurements and completion status; they are not the current checklist. Remaining gaps are listed in [CORRECTION-REVIEW.md](CORRECTION-REVIEW.md).

`walker-lanternfall-bao-x` · Bao Xing · CSYE 7270 Assignment 2

> **Status: 2026-10-02.** Source revision **`8a6f988`** (the revision the film shows; `godot/` is unchanged after it) for every automated check, capture and comparison below; engine **Godot 4.7.2.stable.official.ed1daf0bf**. My two full playtests (sound on, then muted) are in §4, with the build each was played on. The fresh clone from GitHub is done (§2). Nothing here is claimed before it was observed.

## 1. Environment

| | |
|---|---|
| Machine | MacBook, Apple M4 Pro, 16 GB, macOS 26 |
| Engine | Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility |
| Input | keyboard and gamepad bindings exist; my notes do not record a gamepad test |
| Generation / checks | Python 3.12 venvs from `gen/requirements-*.txt` |

## 2. Fresh copy

- **Local fresh clone of `1b24721`** (2026-10-01): `git clone` into an empty folder → `godot --headless --path godot --import` → all three suites: **logic 32/32, gameplay 63/63, audio 22/22**, no script errors; `audit_repo.py --stage final`: 0 problems. All 14 sprites, 7 sound effects and 2 music loops were present; nothing is downloaded at run time. (An earlier clone of `89ae6ed`, before the sounds and new props, also passed.)
- **Fresh clone from GitHub** (2026-10-02, commit `a600e65`; `godot/` identical to `8a6f988`): `git clone https://github.com/yanxlh/walker-lanternfall-bao-x.git` into an empty folder — a 63 MB checkout with no Godot cache, no file over 25 MB and no MP3/MP4 → `godot --headless --path godot --import --quit` (46 files imported, 0 errors) → **logic 32/32, gameplay 65/65 (including `generated-assets-load`), audio 25/25**, no script errors → `scripts/audit_repo.py --stage final`: 0 problems → all 23 asset files listed in `godot/assets/manifest.json` present → the game starts and runs (5 s launch, no errors in the log). Commits after `a600e65` change documents only.

## 3. Automated checks (all added for this project)

| Check | Result on `8a6f988` (re-run 2026-10-01/02) | What it proves | Evidence |
|---|---|---|---|
| `godot/tests/test_logic.gd` | 32 / 32 | state machine; branching cards, 5-level passives, damage/haste multipliers, evolution rule; XP needed always rises; SFX gate cooldowns, voice caps, once-per-run | `evidence/logic.json` |
| `godot/tests/test_gameplay.gd` | 65 / 65 | movement, diagonal normalisation, facing dead-zone, poses, nearest-enemy aim, bullets stop on visible contact, gems, level-up queue (incl. while paused), i-frames, win/lose incl. same-tick, evolution, restart, missing-art fallback, HUD text, hurtbox on the torso, HP growth, damage/haste cards, camera moves, map layout, solid props | `evidence/gameplay.json` |
| `godot/tests/test_audio.gd` | 25 / 25 (with the real sounds loaded) | once-per-event SFX, bursts, held/rapid input, music duck/filter/fade, restart during fade, mute, **sound-independence** | `evidence/audio.json` |
| `gen/checks/palette_check.py` | 14 / 14 sprites PASS | exact size, binary alpha, palette-only; enemy-vs-ground contrast | `evidence/palette-check.json` |
| `gen/checks/loop_check.py` | MUS-01, MUS-02 PASS; layer length PASS | loop wrap has no click or gap; layer = base length | `evidence/loop-check.json` |
| `gen/tile_process.py` seam metric | PASS (seam 7.52 vs interior 6.05) | the ground tile tiles without a visible seam | `evidence/tile-seam.json` |
| `scripts/audit_repo.py --stage final` | 0 problems (all 23 asset IDs present); order check PASS | no MP3/MP4/large files/caches/keys; every CHANGE-BRIEF asset exists; **every generation is newer than `design-v1`** (tag 2026-09-28 15:21 EDT; first generation commit `e384933`, 2026-09-29 16:57 EDT, a descendant of the tag) | `evidence/repo-audit.json` |
| balance probe `godot/tests/probe_balance.gd` | informational | scripted bots to compare tuning | `evidence/balance-probe-*.txt` |

The test harness fails a suite that stops early; my runner also fails on any `SCRIPT ERROR` (both added after a script error once aborted a helper silently).

Commands (from the repository root; Python checks use the venvs from `gen/requirements-*.txt`):

```
godot --headless --path godot --import --quit
godot --headless --path godot --script res://tests/test_logic.gd       # -> logic: 32 checks, 0 failures
godot --headless --path godot --script res://tests/test_gameplay.gd    # -> gameplay: 65 checks, 0 failures
godot --headless --path godot --script res://tests/test_audio.gd       # -> audio: 25 checks, 0 failures
gen/.venv-art/bin/python gen/checks/palette_check.py
gen/.venv-audio/bin/python gen/checks/loop_check.py godot/assets/music/mus_01_night_market.ogg godot/assets/music/mus_02_sunflare_layer.ogg
python3 scripts/audit_repo.py --stage final
```

The suites' full output on a fresh `git archive 8a6f988` copy is kept in `youtube/claude-liam-walker-lanternfall-bao-x-gamedev/capture/test-run-film-build-raw.txt` (122 PASS, 0 FAIL, no script errors).

## 4. My playtests

Full notes in my words: [`evidence/playtest/2026-09-29-bao-notes.md`](evidence/playtest/2026-09-29-bao-notes.md). Checklist for the final runs: [`evidence/playtest/sheet.md`](evidence/playtest/sheet.md).

| Session | Build | What I checked | Outcome |
|---|---|---|---|
| 1 — 2026-09-29, music only, no SFX yet | `40102ab` | first play of the greybox with generated art | bullets flew through monsters → loop L1 below; asked for a fuller map, rising XP cost, tougher monsters over time, more cards |
| 2 — 2026-09-29/30, music only | `79c2874` | re-test after the fixes | "Bullets work correctly" (bullets fixed), "Collisions feel fine" (collisions feel fine), "Not hard" (not hard), "I reached the evolution" (I reached the Sunflare); asked for a more broken-up map |
| **Run A — sound on** — 2026-10-01 | `1b24721` | the full sound checklist | "Each sound plays once, they do not run together, there are no extra sounds, and there is no gap" — each sound once, kills never machine-gun, no extra sounds from tapping/holding, no gap at the loop; pause, level-up duck, Sunflare layer, lose/win fade + stinger, R during the fade, M/9/0 all confirmed — [`evidence/playtest/2026-10-01-runs-A-B.md`](evidence/playtest/2026-10-01-runs-A-B.md) |
| **Run B — muted (M on the title screen)** — 2026-10-01 | `1b24721` | can I read every event without sound? | "All were readable in the second run" — hits, level-ups and the evolution all readable from the picture; wraiths and the courier visible |

## 5. Movement and state changes

- Automated: `move-speed` (90 px/s), `diagonal-normalized`, `facing-left`, `facing-deadzone` (no flip for |x| ≤ 0.1), `arena-clamp`, `walk-pose` / `idle-pose` / `cast-pose-on-fire`, `levelup-opens` / `choose-card`, `levelup-queue`, `levelup-while-paused`, `death-lost`, `won-at-3min`, `death-and-timer-same-tick`, `restart-resets`, `props-block-the-courier`, `courier-slides-along-props` — all PASS.
- In play (sessions 1–2), confirmed in my notes: bullets now stop on hit, blocking props feel fine, and I reached the Sunflare evolution. Other states were not called out in the notes; Run A/B use the full checklist.

## 6. Character vs character sheet

![sheet vs game](design/character/sheet-vs-game.png)

Blockout (design-v1) · generated frame · the frame captured in the running game · generated silhouette.

**Both facings and the hurtbox, in the engine (added 2026-10-02):**

![sheet vs game, facing left and with the F3 hurtbox](design/character/sheet-vs-game-facing.png)

Rows: blockout · generated frame · in game facing right · in game facing left · facing left with the F3 hurtbox (r = 10 at sprite origin (16, 23)). Captured on an isolated copy of `8a6f988` by `scripts/capture_facing.gd` (same seed and setup as `godot/tests/capture.gd`; screens `evidence/screens/pose-*-left*.png`). Facing left is the code's mirror of the right-facing frame for every pose, as the sheet specifies. Mismatches with the collision shape, pose by pose: in the standing poses (turn_front, idle, walk, cast, levelup, sunflare, victory) the circle covers the coat and also the lower half of the lamp; in **hurt** the lamp leans back outside the circle (in the courier's favour); in **defeat** the body lies partly outside it, which does not matter because the run has ended. Held: 32 × 32, palette-only, binary alpha, feet on row 31, lamp normalised to 12 px, right-facing master with code flip. Broke and fixed: the generated courier is shorter, so the torso sat 1.7–3.6 px below the hurtbox centre → sprite origin moved to (16, 23) (loop L8). Still open: an r = 10 hurtbox now also covers the lower lamp; silhouettes are less distinct than the blockout (levelup vs victory). Details: CHARACTER-SHEET R2–R3.

## 7. Storyboard vs game

![storyboard vs game](design/storyboard/storyboard-vs-game.png)

All nine panels were captured from the build (`godot/tests/capture.gd`). The first comparison showed none of the camera moves; they were then implemented (title push-in, hit tilt, Sunflare zoom-out, fog lifting at 3:00) and re-captured (STORYBOARD R1–R2). Remaining differences: the courier is far smaller on screen than drawn, and the fog-wraith is nearly invisible on the cobbles in P5.

## 8. Sound: once per event

Automated (the gate and the counts do not depend on the audio files; re-run with the real sounds loaded). Numbers are from the final build `8a6f988` (`evidence/audio.json`); the review fix that keeps spawns off-screen changed how seed 11 plays out, so builds before it reported 88 kills → 88 plays (min gap 117 ms), 73 pickups → 54 plays and an independence end state at tick 3850. The verdicts did not change.

| Check | Observed |
|---|---|
| `once-levelup` | one chime per card screen over a full run (count compared with card screens opened) |
| `once-hurt` | 14 hits → 14 plays (one per i-frame window) |
| `kill-throttled` | 80 kills → 78 plays, never closer than 60 ms (min gap 184 ms) |
| `pickup-merged` | 68 pickups → 50 plays (pickups within one 300 ms voice slot merge — CHANGE-BRIEF R6) |
| `burst-20-kills-one-sfx` | 20 kills in one tick → 1 play |
| `evolve-sfx-once` / `one-stinger` | 1 evolution sound; 1 stinger at the end |

**Run A (me):** each of the seven sounds played once on its event — "It plays only once" — and kills in dense waves did not run together — "They do not run together".

## 9. Rapid and held input

Automated: `hold-input-no-sfx` (100 ticks holding a direction → 0 sounds), `rapid-pause-no-sfx` (20 pause toggles → 0 sounds, state correct) — PASS. Key presses ignore key-repeat echo, and no sound is attached to input. **Run A (me):** tapping fast and holding a direction produced no extra sounds — "No".

## 10. Music loop seam

| Loop | Length | Wrap jump vs p99 step | Head / tail RMS vs mean | Result |
|---|---|---|---|---|
| MUS-01 night market | 20.004 s | 0.00104 vs 0.00917 | 1.28 / 0.50 | PASS |
| MUS-02 Sunflare layer | 20.004 s | 0.00844 vs 0.02508 | 1.74 / 2.29 | PASS |
| layer length = base length | 882176 = 882176 frames | — | — | PASS |

By ear: I listened to each of the four MUS-01 candidates as a loop played three times in a row and picked the one without audible clutter; I listened to three MUS-01 + MUS-02 mixes looped three times and picked s34. **Run A (me):** no click or gap at the loop point in the game — "There is no gap".

## 11. Pause and end behaviour

Automated: `pause-lowpass-and-duck` (low-pass on, −10 dB), `resume-restores`, `levelup-duck` / `levelup-unduck` (−6 dB), `lost-fades` → `lost-stops`, `restart-during-fade` (new run's music at full volume, filter off), `restart-from-pause`, `mute-flags`, `mute-no-state-change` — PASS. `independence`: a seeded run with every stream removed and the master bus muted ends in exactly the same state as the run with sound (same tick 3817, kills 80, level 7, position −220.11, 202.53 — build `8a6f988`). **Run A (me):** confirmed in play — pause muffles and quietens the music and resume restores it; level-up dips it; the Sunflare layer comes in; lose/win fade with the stinger; R during the fade restarts the music cleanly; M/9/0 work.

## 12. Understandable without sound

Design: every sound event has a visual — hit: red flash, screen tint, knockback, HP bar; pickup: the gem flies to the courier and the XP bar/number rises; level-up: the field freezes and cards appear; evolution: banner, zoom-out, brighter courier; end: result panel; the HUD shows `MUSIC on/off SFX on/off`. **Run B (me), muted from the title screen:** "All were readable in the second run" — I could tell being hit, levelling up and evolving without sound, and I could see the fog-wraiths and the courier. Measured contrast for the wraith is still the lowest (0.03), but in play it read well enough, so its colours stay as generated.

## 13. Observe → change → re-verify

| # | Observed (by) | Change | Re-verified (how) |
|---|---|---|---|
| L1 | Bullets flew on through monsters — **me, in play** | Weapons hit the visible sprite box (moth wing 11 px, wraith hood 19 px, was 6 / 14) and the bolt is a segment | `beam-stops-on-moth-wing`, `beam-stops-on-wraith-hood` RED → GREEN, control `beam-misses-when-clear-of-sprite`; **me, in play: "Bullets work correctly"** |
| L2 | First character images looked like a shaded 3D illustration — **me** | **Prompt** rewritten for 16-bit pixel art; 10 poses | new batch reviewed at game size; I accepted 10 frames |
| L3 | Reduced to 32 px, the navy coat turned black and the floor shadow cream — preview | **Palette** matching moved to Lab, ink reserved for outlines, grey shadows keyed out | preview re-checked; `palette_check.py` PASS |
| L4 | The lamp changed size from pose to pose at 32 px — review sheet | Frames scaled so the lamp is 12 px (sheet rule 11–13) | measured 12.0 px on all 10 frames |
| L5 | Two ground tiles failed the seam check; all were noisy at 64 px — seam metric | Centre 40 % crop before tiling; took the passing candidate | seam 7.52 vs interior 6.05 PASS |
| L6 | Three MUS-01 loops were "Too cluttered and noisy" — **me, listening** | MUS-02 **prompt** rewritten without shakers/tambourine | I listened to the new mixes and chose one |
| L7 | First MUS-02 layers were ~106 BPM or hiss — loop check | Model changed (melody → medium); **loop point** cut on the same 8 bars and stretched ≤ 10 % | `layer-length-match` PASS; stretch 0.9897 |
| L8 | Coat centre 1.7–3.6 px below the hurtbox centre — measurement | Sprite origin (16, 20) → (16, 23) | `hurtbox-centred-on-torso` RED → GREEN |
| L9 | Smooth HP growth made moths need two hits from the first second; bots died in 36–84 s — probe | Growth stepped per whole minute | gem-collecting bot evolved at ~1:30 and won 2 of 3; **me, in play: "Not hard", "I reached the evolution"** |
| L10 | First puddle batch: the prompt's "on dark cobblestones" made FLUX paint the stones, keying failed, the puddle became a blob — review sheet | Puddle **prompt** rewritten: isolated on white, no ground | second batch keyed cleanly; I accepted s37 (gold reflection survives at 32×16) |
| L11 | In the in-game preview the leaves were brighter than the courier's body and the puddles lighter than the ground — street capture | Decals drawn at 55 % opacity (`DECAL_ALPHA`) | `decals-are-subtle`; map overview re-captured; I approved |
| L12 | A fresh clone run by double-clicking the launcher showed placeholder art and no sound (no import cache) — **whole-branch code review** | Launcher imports on first run; new check `generated-assets-load` | ran the launcher in a brand-new clone: 46 files imported, 0 load errors; the check fails in an unimported clone and passes after |
| L13 | Two levels from one pickup played two stacked level-up chimes and a silent second card screen — code review | SFX-04 moved to the card screen opening | `levelup-sfx-on-card-screen` RED ([0,0] vs screens at [1,2]) → GREEN |
| L14 | Near walls and corners enemies could spawn on screen, even on the courier — code review | Spawn outside the view rectangle (seeded re-roll, then the widest off-screen strip) | `spawns-arrive-off-screen` RED (83/200 visible) → GREEN (0/200) |

## 14. CHANGE-BRIEF predictions, scored

| # | Prediction | What happened |
|---|---|---|
| 1 | Kill SFX machine-guns in dense waves | Did not happen: min gap 184 ms and 20 kills → 1 sound in the automated runs (8a6f988); by ear in Run A, "They do not run together". |
| 2 | Generated poses drift after downscaling | Happened, differently than predicted: identity held, but FLUX ignored the pose grid and the lamp size varied; fixed by per-pose prompts and lamp normalisation (L2–L4). |
| 3 | MusicGen loops click or drift | Did not happen after processing: all loops PASS; confirmed by ear on the candidates. |
| 4 | Enemies unreadable against the ground | Measured low for the wraith (contrast 0.03 vs 0.40 for the moth), but in my muted run it was readable ("All were readable in the second run"); kept. The props added later were made subtle (decals at 55 %) so the ground stays darkest. |
| 5 | MUS-02 drifts against MUS-01 | Happened with the melody-conditioned model; fixed with a second batch (L7). |

## 15. Code review

A fresh-context reviewer read the whole branch (Godot code, tests, pipeline, checks), ran every suite in an imported and an unimported clone, and probed the five Review Focus cases plus the engine's mixed audio across the loop point (sample-identical to the file). Verdict: ready with fixes. Fixed: L12–L14 above, plus restart silencing the lose/win stinger (`restart-silences-stingers`) and the missing-art check now rendering frames and comparing runs (`missing-art-same-run-and-draws`). Deferred (minor): the left stick can skip several cards on the card screen (gamepad untested); placeholder shapes do not match the hit/solid boxes; two checks are weaker than their names (`enemies-pass-through-props`, and the full-run audio comparison ends before an evolution).

## 16. Open questions and not yet verified

- Hurtbox kept at r = 10 (it reaches the lower lamp); it was not raised as a problem in play.
- The courier is small on screen (~20 px tall); readable in both runs, but worth revisiting if the camera ever zooms out further.
- No gamepad test is recorded.
- Balance is tuned against my own play and scripted bots only.


## Particle effects — 29 October 2026

This section records the new automated runs separately from the earlier Assignment 2 report. The starting local course-repository snapshot was `9fa5d88`; design and wrapper were recorded at `8eb16a2`, and initial project context at `a46c055`. No local `a5` tag or earlier shader directory was found. This is not a claim that the missing assignment has been completed.

Engine: Godot 4.7.2.stable.official.ed1daf0bf. Project renderer: GL Compatibility. Checks below ran headlessly with a dummy renderer and establish no visual quality or GPU cost.

### Existing-suite baseline

| Suite | Mode | Checks | Failures | Result |
|---|---|---:|---:|---|
| logic | 60 fps | 32 | 0 | `evidence/assignment-6/baseline/logic.json` |
| gameplay | 60 fps | 65 | 0 | `evidence/assignment-6/baseline/gameplay.json` |
| audio | realtime | 25 | 0 | `evidence/assignment-6/baseline/audio.json` |

Earlier `evidence/logic.json`, `gameplay.json`, and `audio.json` were preserved byte-for-byte. Baseline logs are alongside the JSON files above. Existing gameplay tests report resource/ObjectDB cleanup warnings; they still reach the suite end with all 65 assertions passing. The environment also reports a macOS certificate-store warning; this is not a shader or script error.

### Effect A configuration

`./scripts/run-test.sh test_defeat_sparks_config.gd 60`: 39 checks, 0 failures. Result: `evidence/defeat_sparks_config.json`; output: `logs/test_defeat_sparks_config_60fps.log`. The test checks the real instantiated scene, all brief parameters, scale and colour resources, the generated texture, and additive draw material.

| Mutation | Actual outcome | Evidence |
|---|---|---|
| Rename `initial_velocity_min` to `initial_velocity` | Exit 1; loaded minimum became 0 instead of 25 | `evidence/assignment-6/mutations/godot3-name.log` |
| Change spread 180 to 90 without updating the brief | Exit 1; spread read-back failed | `evidence/assignment-6/mutations/wrong-value.log` |

The scene was restored after each mutation. Its final configuration run passes again.

Windowed check of the old-name mutation, repeated on 29 October 2026 against the kept r1 scene: Godot loaded the renamed property without a warning and used 0 for `initial_velocity_min`. The burst still appeared with the same colours and fade timing, but spread about 10–15% tighter, with a few sparks lingering near the centre (e.g. 45 × 43 → 40 × 42 px at 0.20 s). The configuration test failed only on that setting. The scene was restored byte-identical and the test passed again (39/0). Frames, sheet and log: `captures/defeat_sparks/mutation-godot3-name/`.

### Preview smoke check

A headless run of `res://previews/defeat_sparks_preview.tscn` at 30 fps with `--retrigger` completed 60 frames and printed trigger events at frames 10 and 13. This checks that the fixture loads and schedules both events. It does not prove visible particles, independent burst appearance, or correct gameplay integration.

### Checks recorded later

The dated sections below record, in order: gameplay integration and the real-input state test; the visibility trial and the portrait anchor; the trail comparison; Effect A's r1 revision; the windowed play checks and edge suite; CPU and GPU cost; and the generated process shader. The brief coverage table is in the play-check section. Still open: the film, the final regression at the submission tag, and fresh-clone verification.


### Approved hit and upgrade integration — 29 October 2026

The design revision was recorded before implementation at `ec024c5`. Effect A now responds to `Session.weapon_hit`, emitted for each living enemy passed to the existing `damage()` method. It includes lethal and nonlethal hits. The historical `defeat_sparks` scene filename is retained; the new listener does not subscribe to `enemy_killed`, avoiding a double burst on lethal hits. A separate celebration follows `leveled_up`; B is the movement trail.

The session changes only add a signal publication and attach a presentation child. Damage arithmetic, collision queries, weapons, state transitions, input, and timing are unchanged.

Configuration runs at 60 fps: A 39/39; trail and celebration 78/78. Real-input state suite at 60 fps: 31/31 (`evidence/particles_state.json`, `logs/test_particles_state_60fps.log`). The suite starts with Enter, moves with D, pauses with P, chooses a card with 1, and restarts with R through parsed keyboard events and the actual physics loop. Enemies and pickups are seeded as fixtures; it never calls the damage or particle trigger functions.

Observed state evidence includes three beam hits within one particle lifetime, separate instances for lethal and nonlethal hits, positions matching the real hit signal, bursts surviving enemy removal, movement/idle/hidden/pause policies, celebration playback during LEVELUP, and restart cleanup. A stress fixture produced 40 hit events and 32 accepted instances (512 allocated particles). A real pickup awarded six levels, creating the specified maximum of four celebration instances.

An initial state-test run failed four assertions because its first projectile had already been created before the fixture set the beam's piercing value. The fixture now seeds the world on `run_started`, before the first physics tick; gameplay was not changed to accommodate it. The failing output is retained at `evidence/assignment-6/integration/initial-state-test-failure.log`.

The new state test reports resource/ObjectDB cleanup warnings at shutdown, as the earlier gameplay suite does. These remain a test-cleanup limitation, not a claimed clean shutdown. Logs must be reviewed alongside pass counts.

These checks do not prove screen appearance, trail readability, or whether the upgrade overlay obscures the celebration. No new human verdict, frame comparison, performance measurement, or completed tuning revision is recorded.

Post-integration regression: logic 32/32 at 60 fps, gameplay 65/65 at 60 fps, audio 25/25 in realtime. Results and complete logs are under `evidence/assignment-6/integration/`; earlier result files were restored after recording the new runs. Together with A configuration (39), extra configuration (78), and state checks (31), the current recorded suites pass 270 assertions. Cleanup warnings remain as described above.

### Visibility trial r1 — 29 October 2026

The student reported that level-up sparks and the movement trail were not obvious, then approved moving celebration particles above the upgrade HUD and increasing the trail's alpha ramp. The former now uses CanvasLayer 11 with the world camera transform; the latter uses alpha 0.95/0.70/0 at normalized t=0/0.5/1. No other particle settings were changed in this trial.

Recorded post-change suites under `evidence/assignment-6/tuning/r1-tests/`: logic 32, gameplay 65, audio 25 (realtime), A configuration 39, extra configuration 79, state 33; all zero failures (273 assertions total). Added assertions verify exact overlay layer 11, ordering above HUD, and screen-space alignment with the courier. Earlier shutdown cleanup warnings persist.

Headless checks establish configuration and state only. Before/after frame strips, post-change human judgment, and a kept/reverted decision are pending; this trial is not yet counted as a completed tuning evidence cycle.

### Upgrade portrait anchor — 29 October 2026

At the student's request, celebration particles now originate at the upgrade UI portrait's torso (HUD-local 56,325), rather than the gameplay courier at screen centre. The portrait's existing rectangle was factored into a shared constant without changing its layout. Overlay layer 11 now uses the HUD transform, independently of camera movement. Particle parameters are unchanged.

Targeted verification: 34 state assertions and 65 existing gameplay assertions passed. The added camera-independence assertion confirms the burst's screen position stays with the UI when the game camera moves. Evidence is under `evidence/assignment-6/tuning/portrait-anchor/`. Shutdown cleanup warnings persist; visual judgment is pending.


Human check update: the student accepted the upgraded celebration's placement on the UI portrait after running the updated game (“That works”). This is a placement verdict only. Before/after fixture strips, a separate movement-trail verdict, and performance measurements are not yet recorded.


### 29 October 2026 — movement trail accepted

The student explicitly confirmed that the revised movement trail is sufficiently visible. Keep the colour/alpha ramp at alpha 0.95/0.70/0 for t=0/0.5/1, with other values unchanged. This is a running-game verdict. Before/after fixture strips still need to be captured and compared; no such image evidence is claimed by this entry.


## 29 October 2026 — trail frame comparison recorded

Capture: `captures/lantern_trail/comparison-20261029-135607/`; the student ran the windowed capture and confirmed completion. Original-setting and revised-setting strips each contain frames 10,12,20,39,40,45,51,60, at 30 fps with fixed seed 7280. The baseline was re-rendered from its preserved original resource after the revision; it is not a historical pre-edit gameplay recording.

Comparison: r1 has stronger amber flecks at startup (10/12) and a clearer short trail during steady movement (20/39), with the same footprint. At stop (40) its residual sparks are brighter; by 45 both are almost gone, and at 51/60 neither leaves a trail. This supports the brightness prediction without supporting any claim of more particles or a longer lifetime. Differences are subtle at full frame and clearer in labelled magnified crops. Detailed frame reading and SHA-256 hashes are in `COMPARISON.md` and `manifest.json` alongside the captures.

The student's separate running-game verdict was to keep the visibility revision. No further setting change was made from this comparison. This supplies the missing B fixture comparison; it does not complete A's required observation-driven revision, upgrade screenshot evidence, performance measurements, shader study or film.


## 29 October 2026 — Effect A scale revision r1

The student reported no problem with the hit sparks in the integrated game. The r0 fixture strip, read against the brief, showed an initial cluster of 0.35 courier height on its first frame, below "about one character height". The approved change was `scale_amount_max` 1.2 → 1.8. The configuration expectation was edited first and failed on that setting alone (`evidence/assignment-6/tuning/a-r1-tests/defeat_sparks_config-expected-failure.log`). After the scene edit, every suite passed: logic 32, gameplay 65, audio 25, A configuration 39, extra configuration 79, state 34 (274). The r1 capture matched the prediction for first-frame size, unchanged spread and fade timing. It did not match the predicted 3–4 px wider footprint: the footprint grew about 1 px while lit area grew 1.4–1.85×. Comparison: `captures/defeat_sparks/comparison-r0-r1/COMPARISON.md`. The student kept the change after playing (“Keep it; it is clearer”).

## 29 October 2026 — windowed play checks and edge suite

`godot/tests/capture_play_checks.gd` ran 12 scripted scenes in a real 1280 × 720 window and saved 56 shots with per-shot effect state. It covered the celebration, hits on plain floor and the brightest props, the trail on the floor and through a light pool, pushing into a stall, restart while moving, pause, the hidden toggle, the card screen, death and victory. Readings, measurements and the items still needing human play are in `captures/play-checks/20261029-142138/PLAY-CHECKS.md`.

The new headless suite `./scripts/run-test.sh test_particles_edges.gd 60` passes 18/18 (`evidence/particles_edges.json`). It covers blocked input with zero displacement and zero emitting frames, sliding along the blocker, a one-frame position discontinuity, restart history, LOST and WON cleanup, and a clean restart from LOST. Its first run failed one fixture assertion: after sliding up, the courier was still against the stall, so moving right correctly produced no trail. The fixture was changed to walk away from the stall; presentation code was not changed.

Mutation: removing `distance > 0.01 and distance <= teleport_limit` from the trail condition in `particle_presentation.gd` made `blocked-push-never-emits` (30 emitting frames) and `jump-frame-no-emission` fail. The file was then restored byte-identical (`evidence/assignment-6/mutations/edges-no-displacement-guard.log`).

Regression after restore: edges 18, state 34, extra configuration 79, A configuration 39, logic 32, gameplay 65, audio 25 (realtime). All have zero failures, 292 assertions in total (`evidence/assignment-6/play-checks/`). Existing shutdown cleanup warnings persist.

### Brief coverage

| Brief rule | Evidence | Kind |
|---|---|---|
| A fires on every weapon hit, lethal and nonlethal, at the hit position | state: `real-beam-hits`, `nonlethal-hit-also-bursts`, `hit-event-position`, `one-instance-per-accepted-hit` | test |
| A survives enemy removal; repeats are independent; cap 32 / 512 particles | state: `lethal-hit-survives-enemy-free`, `rapid-hits-overlap`, `hit-cap-*` | test |
| A settings equal the brief (with the kept r1 value); no fixed seed in play | A configuration 39 checks; mutations `godot3-name`, `wrong-value` | test |
| A timing: compact, then spread by 0.20 s, gone by 0.45 s | r0/r1 strips: last trace 0.40 s, none from 0.43 s | frames |
| A size: about one height initially, at most two at widest | r1: 0.41 → 0.71 height in the first 0.07 s (below the initial target, recorded); widest ≤ 64 px of a 68 px limit | frames |
| A pale-yellow centre, orange dissipation; readable on dark floor and bright props | first 2 frames white from additive overlap; play checks `hit-dark`, `hit-bright-cart`, `hit-bright-post` | frames; human pending |
| A frozen outside PLAYING, cleared on terminal states and restart | state: `pause-freezes-hit`, `restart-clears-bursts`; edges: `lost-clears-hit-bursts`, `won-clears-hit-bursts`; play checks pause and card; student: pause/card/death/win/restart normal | test + frames + human |
| B emits only while PLAYING, visible and actually moving | state: `idle-no-trail`, `real-movement-starts-trail`, `hidden-stops-emission-keeps-simulation`, `upgrade-stops-freezes-trail`; edges: `blocked-*`, `slide-along-blocker-emits` | test + frames |
| B: no emission on teleport; restart leaves no line | edges: `jump-frame-no-emission`, `restart-history-at-new-origin`; play checks `restart-*`; mutation | test + frames |
| B world-space trail; gone within 0.35 s of stopping | state: `trail-world-coordinates`, `idle-stops-trail`; play checks: none at 0.20 s; B fixture comparison | test + frames |
| B dimmer and smaller than A; about 1–2 heights long | play checks: 2–4 px dim flecks vs 6–11 px sparks; visible length 26–35 px (0.8–1.0 height, low end) | frames |
| B does not hide enemies, pickups or the courier | play checks: no overlap in fixtures; student after a normal run: “Nothing is obscured; everything behaves normally” | frames + human |
| B sphere emission radius 3 and other settings | extra configuration checks | test |
| Celebration: real level-up, UI portrait, above HUD, independent of camera | state: `real-pickup-causes-levelup`, `upgrade-*`; play checks `upgrade-*`; student verdict “That works” | test + frames + human |
| Celebration continues in LEVELUP, cap 4, cleared on restart/WON | state: `upgrade-celebration-continues-on-card-screen`, `level-cap-*`, `restart-clears-bursts`; edges: `won-clears-hit-bursts` | test |
| Effects never write gameplay state | unchanged logic/gameplay/audio counts; presentation code reads only (`particle_presentation.gd`) | test + review |
| CPU and GPU budgets | `evidence/assignment-6/cost/COST-REPORT.md`: headless CPU deltas A +0.025 ms (cycle) / +0.009 ms (32 live), B +0.004 ms, celebration +0.009 ms. GPU is unreadable on Compatibility: 0 on every frame via RenderingServer, and 0.0 ms with an empty GPU graph in the editor's Visual Profiler (game window minimized). On the Mobile/Vulkan proxy, GPU deltas are within ±0.1 ms noise. All are under budget. | measured; GPU via proxy renderer |

## 29 October 2026 — CPU and GPU cost

`godot/tests/cost_effects.gd` measured off/on pairs on identical fixtures (empty control, idle, A at its 32-burst cap, B continuous movement, celebration at its cap of 4), interleaved over 5 trials of 300 frames. Headless CPU deltas: A +0.025 ms per frame over a volley cycle, +0.009 ms with 32 live bursts, and about +0.10 ms at the p95 spawn spike; B +0.004 ms; celebration +0.009 ms. All are far under the predictions (0.8 / 0.15 / 0.25 ms) and budgets (1.0 / 0.25 / 0.4 ms).

GPU time could not be read under the project's GL Compatibility renderer on this Mac: `viewport_get_measured_render_time_gpu` returned 0 on every frame, as did Movie Maker's GPU line, and the Mobile/Metal override behaved the same. In the editor's Visual Profiler, recorded for about 17 s with the game window minimized, every GPU entry read 0.0 ms at frame 3743 and the GPU graph was empty, while the CPU entries had values (Render Viewports 3.11 ms). Those are selected-frame readings, and they show that no usable GPU timings were provided, not that GPU cost is zero (`evidence/assignment-6/cost/VISUAL-PROFILER-COMPATIBILITY.md`). The same scenes under the Mobile renderer with Vulkan/MoltenVK, a command-line override with project settings unchanged, gave readable GPU times. Every off/on median delta (A +0.01, B −0.05, celebration +0.09 ms) was within about ±0.1 ms of run-to-run noise. This is a proxy for, not a measurement of, the shipped renderer. FPS and CPU time are not reported as GPU time. Full method, tables and limits: `evidence/assignment-6/cost/COST-REPORT.md`.

## The process shader

The game's A/B effects use CPU nodes without a custom process shader. `godot/shaders/particles_generated.gdshader` is a separate GPU study copy, not code used by the gameplay effects. The connections between processing and visual goals are:

- Line 3, `shader_type particles`, declares a shader that updates particle state, not a canvas_item shader that draws the spark texture.
- Lines 225–275, `start()`, initialize position, random velocity, and other birth parameters. Random velocity at line 139 corresponds to A's 25–55 range; random scale at line 149 corresponds to 0.7–1.8.
- Lines 277–379, `process()`, update particles each frame. Gravity at lines 311/324 and damping at lines 328–336 implement the intent to spread first and slow down afterward.
- Line 160 samples the scale curve; line 161 samples the color ramp. They implement shrinking and the pale-yellow-to-orange fade. Line 352 writes COLOR, and lines 364–371 apply scale to the transform. Both textures must actually be bound; sampling code alone does not establish the correct appearance. The missing bindings in the earlier study were fixed in r2.
- Lines 293–299 and 376–378 handle age and deactivation, corresponding to the 0.45-second end. The `spark.png` texture and additive CanvasItemMaterial belong to drawing; the process shader cannot compensate for HUD obstruction or a missing texture.

Line explanations and repair evidence are in `TEST-REPORT.md` and `evidence/assignment-6/shader-study-fixed/README.md`.

## 29 October 2026 — editor-generated particle process shader

`godot/previews/shader_study/hit_sparks_gpu.tscn` was built from the kept hit sparks with `GPUParticles2D.convert_from_particles()` (`godot/tests/build_shader_study.gd`). Codex, operating the Godot 4.7.2 editor for the student, converted its ParticleProcessMaterial to a ShaderMaterial in the Inspector and saved the shader as `godot/shaders/particles_generated.gdshader` (379 lines, SHA-256 `2e64ebae4b965173f775951abe52f1f8f6d0eac98713cbb72c486231b83723c4`); the student relayed the result (`CONTRIBUTIONS-assignment-6.md`). Line 1 is the editor converter's header: “Shader automatically converted from Godot Engine 4.7.2.stable's ParticleProcessMaterial.” Only the study scene references the shader. The hashes of every file under `godot/effects/` match those recorded in `evidence/assignment-6/cost/COST-REPORT.md`, so the game's effects are unchanged.

The converted material's parameters match the CPU effect: direction (1,0,0), spread 180, initial linear velocity 25–55, gravity (0,12,0), damping 20–30, scale 0.7–1.8. It carries no `color_ramp` or `scale_curve` texture, and the study scene no longer contains the Gradient or Curve resources that `convert_from_particles()` had created. The code still samples both (lines 160–161). With them unassigned, the converted GPU copy would not reproduce the CPU effect's colour fade and shrink. This was not checked visually. The game does not use this scene.

| Item | Lines | What the code does |
|---|---|---|
| `shader_type` | 3 (`render_mode disable_velocity` on 4) | Declares a particles (process) shader, not a canvas_item draw shader |
| Uniforms from the material | 6–45 | Inspector values arrive as uniforms, e.g. `initial_linear_velocity_min/max` 10–11, `damping_min/max` 26–27, `scale_min/max` 30–31, `color_value` 42, `gravity` 43, `color_ramp` 44, `scale_curve` 45 |
| Per-particle randomness | 75–99, 227, 282 | `hash(NUMBER + 1 + RANDOM_SEED)` seeds `rand_from_seed`, so each particle draws the same random values in `start()` and every `process()` call |
| `start()` | 225–275 | Runs when a particle (re)spawns: initial colour, position and velocity |
| Emission position | 165–172, 257–260 | Point emission: position 0, then `EMISSION_TRANSFORM` |
| Initial velocity | 139, 193–201, 264, 271 | Random speed between min and max (139) times a direction within ±spread of `direction` (197–199), stored in `USERDATA1` (264), then rotated into world space (271) |
| `process()` | 277–379 | Runs every frame per live particle: age, forces, motion, colour, scale |
| Age and expiry | 293–299, 376–378 | `CUSTOM.y` advances by `DELTA / LIFETIME`; the particle deactivates past its lifetime |
| Gravity | 43, 311, 324 | `force = gravity`, added to velocity as `force * DELTA` |
| Damping | 131, 328–336 | Reduces speed by `damping * DELTA` and clamps at zero |
| Position update | 340–345 | `TRANSFORM[3].xyz += final_velocity * DELTA` |
| Colour | 42, 44, 155, 161, 248, 347, 352 | Base `color_value` multiplied by `color_ramp` sampled at normalized age (161); written to `COLOR` at spawn (248) and every frame (352) |
| Scale | 30–31, 45, 149, 160, 359–372 | Random scale between min and max (149) times `scale_curve` at normalized age (160), applied to the transform basis (364–371) |

Student explanation of the process stage and the draw stage (29 October 2026):

> The process stage decides how a particle changes. It computes each particle's speed and direction at birth, and afterwards its position, gravity, damping, colour, transparency and size. For example, the hit sparks first spread outward, then slow down, shrink and fade out; all of that belongs to the process stage.
>
> The draw stage decides what the particle looks like. It uses the texture and the draw material to show the particles computed by the process stage on screen. For example, my sparks use a small cross texture and additive blending so they look like bright points; the colour, transparency and size given by the process stage appear when they are drawn.
>
> So even if the particle motion is computed correctly, the result can still be hard to see if the texture, blend mode or draw layer is wrong.

In this project, the process side is the generated shader's `start()` and `process()` (lines 225–379), which write `TRANSFORM`, `VELOCITY` and `COLOR`. The draw side is the GPUParticles2D's `texture` (`spark.png`), its additive `CanvasItemMaterial` and its canvas layer. The level-up celebration's earlier visibility fix worked on the draw side. The particles had been on the world canvas below the upgrade HUD (layer 10); they were moved to an overlay on layer 11, and their process settings did not change.

Quoted student feedback in this report is translated into English from the recorded conversation.

## Final submission verification — 29 October 2026

A clean imported checkout passed all seven suites: logic 32, gameplay 65, audio 25 (realtime), hit configuration 39, extra configuration 79, state 34 and edges 18: 292 assertions, zero failures. No SCRIPT ERROR or SHADER ERROR appeared. Raw logs and exact exit codes are in evidence/assignment-6/final-validation/. Existing resource-in-use shutdown diagnostics are retained.

The final off/on comparison is in evidence/assignment-6/cost/FINAL-COMPARISON.md. Headless CPU increments were A +0.0222 ms, B +0.0030 ms and celebration +0.0070 ms. Mobile/Vulkan GPU increments were A +0.5392 ms, B +0.1077 ms and celebration +0.9103 ms. A and B are within the declared budgets in this test; the extra celebration exceeds its 0.4 ms GPU budget and has broad trial variation. Compatibility returned all-zero GPU timings, which are not counted as zero cost. No source settings were changed. The final Godot tree matches the film source (SOURCE-REVISION.md).


## Assignment 6 revision 2: study textures and editor GPU capture

The earlier missing-ramp finding is resolved in this revision. Both shader texture uniforms are bound, with 21 new configuration checks and a windowed CPU/GPU lifecycle comparison. See `evidence/assignment-6/shader-study-fixed/README.md`. Editor Visual Profiler evidence and its precise scope are in `evidence/assignment-6/cost/visual-profiler-r2/README.md`. Earlier measurements above are retained as historical evidence.


## Assignment 6 revision 3 — audit of the submitted revision, 9 November 2026

Claude Code checked a6-r2 against the Assignment 6 brief. Only documents changed in this revision: `git diff --stat a6-r2 -- godot/ scripts/` is empty. The sections above are kept as they were; where a number below differs from one above, this section is the current record.

### Suites re-run

The submitted source ZIP (SHA-256 `3647667320f9724ae8fa65d24e516adb78a0c6f3b0e4931fe7a717d0fe465a93`) is identical to `git archive 09070e2`. A fresh copy of it, and then this branch, were imported once and run through the wrapper. Both runs gave the same counts:

| Command | Mode | Checks | Failures | Exit |
|---|---|---:|---:|---:|
| `./scripts/run-test.sh test_logic.gd 60` | 60 fps | 32 | 0 | 0 |
| `./scripts/run-test.sh test_gameplay.gd 60` | 60 fps | 65 | 0 | 0 |
| `./scripts/run-test.sh test_audio.gd realtime` | realtime | 25 | 0 | 0 |
| `./scripts/run-test.sh test_defeat_sparks_config.gd 60` | 60 fps | 39 | 0 | 0 |
| `./scripts/run-test.sh test_extra_particles_config.gd 60` | 60 fps | 79 | 0 | 0 |
| `./scripts/run-test.sh test_particles_state.gd 60` | 60 fps | 34 | 0 | 0 |
| `./scripts/run-test.sh test_particles_edges.gd 60` | 60 fps | 18 | 0 | 0 |
| `./scripts/run-test.sh test_shader_study_config.gd 60` | 60 fps | 21 | 0 | 0 |

Total 313 assertions, zero failures. No log contains SCRIPT ERROR or SHADER ERROR. The gameplay, audio, state and edge logs still end with the engine's "resources still in use at exit" diagnostics. Logs, result JSON and exit codes: `evidence/assignment-6/revision-3-validation/`.

### Mutations re-run

On the fresh copy, `initial_velocity_min = 25.0` renamed to `initial_velocity = 25.0` made the A configuration test exit 1 (`FAIL setting-initial_velocity_min {"actual":"0.0","expected":"25.0"}`). `spread = 180.0` changed to `90.0` made it exit 1 (`FAIL setting-spread {"actual":"90.0","expected":"180.0"}`). The scene was restored byte-identical after each.

### Headless CPU price re-run

`./scripts/run-test.sh cost_effects.gd 60 300` exited 0 (5 trials × 300 frames; `revision-3-validation/cost_effects_headless.json`):

| Case | Off mean (ms) | On mean (ms) | Delta (ms) | CPU budget (ms) |
|---|---:|---:|---:|---:|
| Empty scene (control) | 0.0185 | — | — | — |
| Idle game | 0.0987 | 0.1029 | +0.0042 | — |
| A at 32 live bursts | 0.2135 | 0.2514 | +0.0379 | 1.0 |
| B continuous movement | 0.0737 | 0.0789 | +0.0052 | 0.25 |
| Celebration at 4 bursts | 0.1778 | 0.2047 | +0.0269 | 0.4 |

The absolute frame times are two to three times those of 29 October, and the trial ranges are wider (A off 0.18–0.28 ms). Other applications were running during this re-run. The control differs from every game case, so the script is measuring the scenes, not itself. Every delta stays under its budget. A reached 32 bursts; B emitted on all 300 frames of each trial.

### Current prices against the budgets

The brief-coverage row "CPU and GPU budgets" (29 October) and the film's price beat were written before `cost/FINAL-COMPARISON.md` and the a6-r2 Visual Profiler captures. They report Mobile/Vulkan deltas "within ±0.1 ms"; the later measurements do not. Current figures:

| Effect | Headless CPU delta | CPU budget | GPU delta, viewport timer (3 trials) | Visual Profiler, Render Viewports GPU, selected frames | GPU budget | Against budget |
|---|---:|---:|---:|---|---:|---|
| A | +0.022 ms | 1.0 | +0.539 ms | off 0.58 ms; on 0.68 ms at frame 1200, 8.32 ms at frame 1599 | 0.75 | CPU and timer GPU within; profiler spike unexplained |
| B | +0.003 ms | 0.25 | +0.108 ms | off 0.50 ms; on 0.68 ms (+0.18 ms) | 0.25 | within |
| Celebration (extra) | +0.007 ms | 0.4 | +0.910 ms | not captured | 0.4 | GPU over budget |

All GPU figures come from a command-line Mobile/Vulkan (MoltenVK) override on the Apple M4. Under the shipped GL Compatibility renderer every GPU reading on this Mac is 0.000 ms, which is not counted as zero cost. No FPS comparison was made, and the game has no vsync debug key.

### Edge of screen

Both in-game effects are CPUParticles2D. In Godot 4.7.2, `ClassDB.class_get_property_list("CPUParticles2D")` has no `visibility_rect`; GPUParticles2D has one. The only GPU particle node is the study scene, which gameplay never loads. No in-game effect has a visibility rectangle that could cull it. No human edge-of-screen check is recorded.

### Audit snapshot before the later r2 corrections

| Requirement (Assignment 6 brief) | State in the record |
|---|---|
| At least one revision per effect driven by something observed in the running game | B: "not obvious" led to its alpha change. Later A r2: "not eye-catching enough" led to the approved color-ramp change and keep decision; see TUNING.md and commits f55159e through c6e6343. The earlier A scale trial had a different basis. |
| First verdict in visual terms, before Claude reads a strip | A's first verdicts were "visible" and "Done; no problem", with no visual description. |
| Each effect over the darkest and lightest level art (human check) | Confirmed in my November 9 running-game check: both effects are readable on dark floor and bright market backgrounds. |
| Effect B on the first frames after scene load (human check) | Confirmed in my November 9 running-game check: no trail before movement. |
| Size verdict for both effects at the project's window size (human check) | My November 9 running-game check found the sizes appropriate and no obstruction; this is a qualitative judgment, not a new pixel measurement. |
| "Claude against you": a disagreement, or a statement that there was none | The later r2 keep entry in TUNING.md records agreement with the brighter, longer-readable burst and no disagreement; the earlier audit had no such record. |
| Student authorship of the brief and predictions | This is an authorship requirement, not a test result. Current rewriting cannot establish the authorship of historical drafts. |
| The student writes the process-shader line references | The line table was drafted by Claude (line numbers re-checked on 9 November and correct). The process/draw explanation is the student's. |
| CLAUDE.md: unedited agent draft and the student's review committed separately | One commit (`093cac0`). |
| Commits in the order the work happened | Build, both tuning cycles, captures and shader study are in five commits made together at 14:59 (SOURCE-REVISION.md). |
| Agent prompts and session transcripts in the repository | Only the film prompts are committed (`youtube/…particles-gamedev/PROMPTS.md`). |
| Film: three parts named, each with a line; why a GPU effect's headless price is near zero; two shader lines beside the brief settings they implement; agent mistakes caught; overruled readings; one next step; texture sources | Not narrated in SCRIPT.md. The film's price beat shows the earlier GPU summary. |

Requirements met and re-checked on 9 November: both configuration tests and both mutations; both state tests with modes stated, including two hits inside one lifetime and the 32-burst cap; the generated shader's line references; the headless price with an empty-scene control; the budget comparison; the texture provenance record.


## 9 November 2026 — brief coverage follow-up

The configuration expectations now read back A z_index=3, B z_index=1, and the extra celebration z_index=3. The independent `test_particles_tree_pause.gd` checks whole-tree pause and resume separately from the existing P/Esc game-state pause. Targeted rerun: A configuration 40, extra configuration 81, particle state 34, whole-tree pause 11; 166 assertions, zero failures. All four exit codes were 0 with no SCRIPT ERROR or SHADER ERROR. Logs, result JSON and method: [brief coverage evidence](evidence/assignment-6/brief-coverage-20261109/README.md). Earlier eight-suite totals remain historical, rather than being relabelled as a new full run.

Vsync prediction: off/on FPS should both read the display refresh rate when both workloads finish within the refresh interval (for example 60/60 on a 60 Hz display), falling below it when deadlines are missed. This explains why capped FPS can conceal particle cost; it is not an FPS measurement.

### My running-game check and r2 decision

When hits arrive rapidly, I can still recognize the repeated spark bursts. They overlap without becoming a solid bright patch that hides enemies or pickups. The brighter r2 sparks make successive hits easier to notice.

When I stop moving, B stops producing new embers. The few embers already behind the courier fade away quickly rather than leaving a persistent line. When I pause, the remaining sparks and trail stay frozen instead of continuing to move or fade. After I resume, they continue normally, and the trail follows movement again without an extra burst or a long streak.

The recorded project launch window is 1280 × 720.

I checked the effects in the running game. B has no trail before I start moving. A and B remain readable on both dark floor and bright parts of the market. Their sizes feel appropriate relative to the courier, and they do not obscure the courier, enemies, or pickups. The upgrade sparks fit around the small portrait without obstructing the cards.

I am keeping r2 because the sparks are more noticeable and make attack feedback clearer. When a monster is killed, the burst also helps me notice the kill. The same effect appears on nonlethal hits, so I read it as hit feedback rather than proof of a kill on its own.


### Evidence scope: hidden state and r2 cost

Hidden-state behavior was checked through the scripted windowed capture, not by a manual in-game toggle: the game has no hide/show control. See `captures/play-checks/20261029-142138/pause-hidden+08.png`, `shown+08.png`, and `PLAY-CHECKS.md`. State tests supplement those screenshots.

The GPU prices listed above are historical measurements of A before the r2 color-ramp change (r1). Neither the viewport GPU timer nor the Visual Profiler was remeasured for A r2. I reran the headless cost check on r2 and found it within the CPU budget; that does not establish r2 GPU cost. Only the color ramp changed, so I expect similar GPU work, but this is a prediction rather than a new GPU measurement. The directory name `cost/visual-profiler-r2/` refers to the earlier submission revision, not this Effect A r2 color trial.


### A color-ramp r2: reported headless CPU rerun — 9 November 2026

The following figures are transcribed from the two supplied screenshots. Units are ms/frame; parentheses show the range of trial means.

| Condition | Off mean (trial range) | On mean (trial range) | Delta | CPU budget |
|---|---:|---:|---:|---:|
| Empty-scene control | 0.0089 (0.0086–0.0093) | — | — | — |
| Idle game | 0.0581 (0.0578–0.0584) | 0.0620 (0.0618–0.0622) | +0.0039 | — |
| A r2, 32 live bursts | 0.1641 (0.1631–0.1649) | 0.2112 (0.2099–0.2157) | +0.0471 | 1.0 |
| B, continuous movement | 0.0582 (0.0580–0.0586) | 0.0650 (0.0646–0.0658) | +0.0068 | 0.25 |
| Celebration, 4 live bursts | 0.0901 (0.0851–0.0912) | 0.1065 (0.1035–0.1095) | +0.0164 | 0.4 |

All three effect CPU deltas are below budget. The supplied report states that A reached its 32-burst cap, B emitted through each 300-frame trial, and the celebration reached its four-burst cap. A's on-trial means span 0.0058 ms (approximately 0.006 ms) across five trials. The empty-scene control is below every game condition.

For comparison, A's earlier CPU deltas were +0.0222 ms in the October 29 r1 comparison and +0.0379 ms in the November 9 r1 rerun; the r2 result is +0.0471 ms. These separate runs do not isolate the color-ramp change from machine load or other timing variation, so their difference is not established as the cost of r2.

Evidence scope: the screenshots are saved in `evidence/assignment-6/cost/a-color-r2-reported-20261109/`. They report that the raw run remained in a temporary copy; raw logs, per-trial JSON, exact invocation, and source hash were not supplied with these images. This is a reported result with screenshot evidence, not a newly reproduced benchmark or a claim that its raw logs are archived. A r2 GPU timing has not been rerun. All existing A GPU figures remain r1 measurements; the expectation of similar GPU cost after a color-only change remains a prediction.


## Current r2 validation and cost evidence

Nine suites were run using `bash scripts/run-test.sh <suite> <mode>` on an imported copy of the current source. Modes: audio `realtime`; every other suite `60`. Counts: logic 32, gameplay 65, audio 25, A configuration 40, extra configuration 81, particle state 34, edges 18, shader-study configuration 21, whole-tree pause 11. Total: **327 assertions, zero failures**. Both deliberate A mutations exited **1**, and the scene was restored byte-for-byte before the final passing A configuration run. Original assertions were retained.

The current original brief and dated revisions are retained. Initial particle brief/wrapper commit: `04ef18a`; event-design update: `6d88e4b`; later A r2 approval/test/change/comparison/decision: `f55159e`, `7439dda`, `389c369`, `39f8943`, `c6e6343`. The current supplemental explanation is separate from those original records.

### Reproduced CPU cost

Command: `bash scripts/run-test.sh cost_effects.gd 60 300`. The retained serial run took place after the windowed GPU workload had exited; concurrent exploratory output is not used here. Godot 4.7.2, Apple M4, macOS 26.6.2, headless, five interleaved trials of 300 frames after 30 warm-up frames (celebration: ten short trials of 38 frames). The empty-scene control is 0.004647 ms/frame. All times below are ms/frame.

| Condition | CPU off mean (trial range) | CPU on mean (trial range) | Delta | Budget |
|---|---:|---:|---:|---:|
| Idle game | 0.031918 (0.029203–0.038263) | 0.032721 (0.031303–0.035563) | +0.000803 | — |
| A r2, cap 32 | 0.085517 (0.083377–0.087763) | 0.183205 (0.106723–0.453600) | +0.097687 | 1.0 |
| B, continuous movement | 0.045263 (0.029323–0.099813) | 0.038083 (0.032807–0.051003) | -0.007179 | 0.25 |
| Celebration, cap 4 | 0.053516 (0.045211–0.077263) | 0.062542 (0.053158–0.078132) | +0.009026 | 0.4 |

A's positive delta is below its 1.0 ms CPU budget; celebration is below 0.4 ms. B's negative delta does not mean particles save CPU time: off/on trial ranges overlap substantially, so its incremental cost is not resolved by this run. Earlier reported r2 screenshots show +0.0068 ms, below 0.25 ms. Keep both results rather than selecting a favorable one. The current original logs and per-trial JSON are archived here, closing the previous absence of raw logs for a reproduced current-source run; they do not retroactively supply the raw logs of the earlier screenshot run.

### Reproduced windowed GPU timer

Command: `Godot --path <copied-godot> --rendering-method mobile --rendering-driver vulkan --fixed-fps 60 --script res://tests/cost_effects.gd -- --out <gpu-r2.json> --rev c6e6343-plus-coverage-tests --trials 5`. Renderer overrides do not edit project settings. GPU values below come from RenderingServer viewport timestamps on the Apple M4, not CPU durations or FPS.

| Condition | GPU off mean (trial range) | GPU on mean (trial range) | Delta | Budget |
|---|---:|---:|---:|---:|
| A r2 | 0.833148 (0.403693–1.082033) | 0.776605 (0.642473–1.047647) | -0.056543 | 0.75 |
| B | 0.878415 (0.246000–3.095000) | 0.685109 (0.249000–2.043000) | -0.193306 | 0.25 |
| Celebration | 0.596518 (0.373474–1.169711) | 0.606526 (0.449632–0.823316) | +0.010008 | 0.4 |

Negative A/B deltas and broad trial spread make this run inconclusive for incremental GPU cost. Do not count it as evidence that A/B are free or that their r2 GPU budgets have been reverified. The extra celebration's small delta here does not erase the earlier +0.910 ms over-budget result. These current measurements are viewport-timer results, **not new editor Visual Profiler captures**. Existing editor captures remain historical. The newer screenshot supplied by the student reports r2 A GPU deltas +0.17 to +0.39 ms within 0.75 ms, but its raw data and exact command have not been supplied. The screenshot is supplementary evidence, not a replacement for those missing records.

### Reproduction and identity

Raw stdout, engine logs, nine suite JSON files, mutation exit codes, `cpu-r2.json`, and `gpu-r2.json` are archived with this file. `source-sha256.json` identifies the exact copied Godot files; it is more precise than the benchmark's descriptive revision label. The headless wrapper leaves `source_revision=unknown` in the cost JSON, so that value is not silently replaced. Original automatic UTC timestamps are retained. Exit codes for the nine suites are in `exit-codes.json`; all are zero. CPU wrapper and GPU process also exited zero. Existing resource-at-exit warnings remain; no warning-free claim is made. These tests and measurements do not add new human observations.


Full files: [current r2 evidence](evidence/assignment-6/current-r2-validation/README.md).


## Current r2 editor Visual Profiler capture

Current A and B off/on editor screenshots, original runtime logs and reading method are now archived in [current r2 Visual Profiler captures](evidence/assignment-6/cost/visual-profiler-a-r2-current/README.md). A selected-frame differences were +0.69 ms in the initial layout and +4.59 ms in the final matched layout; B was -1.40 ms in the final layout. The latter measurements show substantial variation and do not establish typical incremental cost. This closes the missing-current-screenshot item, not the budget uncertainty. Two empty captures are retained as rejected evidence. No celebration Visual Profiler rerun or vsync-off FPS comparison is claimed.
