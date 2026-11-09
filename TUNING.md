# Lanternfall — Particle Tuning

## Effect A — initial observation

The initial configuration is in `CHANGE-BRIEF.md` and `godot/effects/defeat_sparks.tscn`.
The observation, strips, revision and verdict are recorded in the dated entries below.

Before requesting a frame comparison, run the preview at 1280 x 720 and record:

- What the first burst looks like against the market floor and bright props.
- Its size compared with the courier, brightness, outward motion, and disappearance.
- Whether rapid repeats remain visible as two bursts.
- One specific visual problem worth changing, or an honest statement that none was observed.

Then capture `r0`, retaining frames 10, 12, 15, 20, 30, and 50.
If visible emission starts on frame 11 rather than 10, record that offset.
No revision is counted until its prediction, approval, before/after strips, comparison, and running-game verdict exist.

## Effect B

The movement trail's observation, revision, verdict and fixture comparison are recorded in the dated entries below.


## 29 October 2026 — design confirmation

The student confirmed weapon-hit sparks and level-up celebration, with the movement trail retained. This is confirmation of intended behavior, not a recorded judgment of the integrated game. The initial independent spark preview was reported visible. No size, brightness, timing, or in-game quality verdict was supplied, and no visual tuning change is counted.

## 29 October 2026 — first integrated-game observation

Student's report (English translation): “The level-up sparks and movement trail are not obvious” (the level-up sparks and movement trail are not obvious).

Code inspection: the upgrade HUD is on CanvasLayer 10, draws a full-screen dark overlay at alpha 0.6, and draws opaque cards over gameplay. Level-up particles currently belong to the world canvas, so the HUD is drawn above them. This is a plausible contributor, not a verified visual comparison.

Proposed upgrade revision: put the celebration on a dedicated overlay above the upgrade HUD, retaining its world-aligned origin and all particle settings. Predicted result: the same particles remain readable when the upgrade cards appear. Do not change damage, progression, HUD controls, or particle timing.

Proposed trail revision: change only its colour/alpha ramp: alpha 0.55 -> 0.95 at t=0 and 0.30 -> 0.70 at t=0.5, retaining RGB and the transparent endpoint. Predicted result: stronger amber visibility during movement and the first half of each particle's life; unchanged path, count, size, and disappearance time.

Approval is pending. Before/after captures and the student's post-change verdict are pending. These proposals have not been implemented or counted as completed revisions.


## 29 October 2026 — visibility trial r1 implemented

Approval: the student replied “Agreed” to the specific overlay and alpha proposals above.

Upgrade change: world canvas -> CanvasLayer 11, above HUD layer 10, with camera-transform synchronization. Prediction: unchanged sparks now render above the dark veil and opaque cards while remaining centered on the courier. Particle count, size, duration, colour and speed are unchanged.

B change: alpha ramp 0.55/0.30/0 -> 0.95/0.70/0 at t=0/0.5/1. Prediction: movement embers become easier to see through their early and middle life; movement path, size and fade-out duration are unchanged. Frames 10 and 12 should show a stronger startup, 20 and 39 a stronger steady trail, and 51 and 60 no additional persistence compared with the original lifetime.

Before source: `evidence/assignment-6/tuning/r0-source/`. No before strip had been captured; do not describe this source snapshot as an image comparison. Post-change frame comparison and human verdict: pending. This is not counted as a complete tuning evidence cycle yet.


## 29 October 2026 — approved upgrade portrait anchor

The student requested that upgrade sparks appear on the small character displayed in the upgrade UI instead of at the middle of the screen. This supersedes the earlier world-camera alignment for the celebration only. The shared portrait rectangle is (8,256,96,96); mapping the sprite torso origin (16,23) from its 32-pixel frame gives HUD-local anchor (56,325). The celebration overlay uses the HUD transform, independently of the game camera. The HUD reads the same portrait rectangle as before; its layout and card controls are unchanged. Particle size, count, timing, colour and motion remain unchanged. Movement and hit particles are unchanged. The post-change visual verdict is pending.


## 29 October 2026 — upgrade portrait placement accepted

After running the updated game with the celebration anchored to the upgrade UI portrait, the student replied “That works” to the request to check that position. Verdict: keep the portrait placement. This confirms the placement is acceptable; it does not establish a separate verdict on the movement trail, GPU performance, or before/after image evidence. Required frame strips remain pending.


### 29 October 2026 — movement trail accepted

The student explicitly confirmed that the revised movement trail is sufficiently visible. Keep the colour/alpha ramp at alpha 0.95/0.70/0 for t=0/0.5/1, with other values unchanged. This is a running-game verdict. Before/after fixture strips still need to be captured and compared; no such image evidence is claimed by this entry.


## 29 October 2026 — trail frame comparison recorded

Capture: `captures/lantern_trail/comparison-20261029-135607/`; the student ran the windowed capture and confirmed completion. Original-setting and revised-setting strips each contain frames 10,12,20,39,40,45,51,60, at 30 fps with fixed seed 7280. The baseline was re-rendered from its preserved original resource after the revision; it is not a historical pre-edit gameplay recording.

Comparison: r1 has stronger amber flecks at startup (10/12) and a clearer short trail during steady movement (20/39), with the same footprint. At stop (40) its residual sparks are brighter; by 45 both are almost gone, and at 51/60 neither leaves a trail. This supports the brightness prediction without supporting any claim of more particles or a longer lifetime. Differences are subtle at full frame and clearer in labelled magnified crops. Detailed frame reading and SHA-256 hashes are in `COMPARISON.md` and `manifest.json` alongside the captures.

The student's separate running-game verdict was to keep the visibility revision. No further setting change was made from this comparison. This supplies the missing B fixture comparison; it does not complete A's required observation-driven revision, upgrade screenshot evidence, performance measurements, shader study or film.


## 29 October 2026 — first running-game observation of weapon-hit sparks

The student ran the integrated game and watched the weapon-hit sparks. Report (English translation): “Done; no problem” (done; no problem). No specific size, brightness, spread, or disappearance problem was reported. No setting was changed from this observation.

Next: capture the `r0` fixture strip (frames 10, 12, 15, 20, 30, 50) with `scripts/capture-defeat-sparks.command` and read it against the brief's visual intent: initial span about one character height, widest point at most two, complete fade by 0.45 s, and readability on both dark floor and bright props. Any revision must cite a specific frame reading; none is proposed yet.


## 29 October 2026 — r0 fixture strip captured and read

Capture: `captures/defeat_sparks/r0/`, run from the terminal with `scripts/capture-defeat-sparks.command` (Godot 4.7.2, Compatibility, Apple M4, 1280 × 720, 30 fps, seed 7280). Strip: frames 10, 12, 15, 20, 30, 50; the full 60-frame sequence is retained locally.

Frame offset: the burst is first visible in file `frame00000009.png`, one file earlier than the trigger's frame-10 label, because Movie Maker file numbering starts at 0. Strip file 10 is therefore one frame after the first visible frame.

Reading (screen pixels; courier warm-pixel height 34 px; spark extents measured against file 8 with the text labels excluded):

| File | Time after first visible | Spark extent (w × h) | Notes |
|---|---:|---|---|
| 9 | 0.00 s | 11 × 12 | compact blob; 66 of 132 spark pixels pure white |
| 11 | 0.07 s | 23 × 22 | about 0.65 courier height; 35 pure-white pixels |
| 13 | 0.13 s | 34 × 33 | separate yellow-orange sparks, no pure white |
| 15 | 0.20 s | 45 × 43 | orange sparks spreading |
| 17–18 | 0.27–0.30 s | 53–60 × 51–52 | widest; dim specks only |
| 21 | 0.40 s | 1 px | last trace; none from file 22 |

Against the brief: the widest point (about 1.6–1.8 courier heights) is within the two-height limit, and the burst fades completely before 0.45 s; strip frames 30 and 50 contain no sparks. The initial cluster is smaller than "about one character height": 0.35 courier height on its first frame and 0.65 by 0.07 s. The first two frames read white rather than pale yellow, because 16 additive particles overlap at one point. The fixture shows only the dark floor, so the bright-prop check (predicted failure 6) is not covered by this capture.

No setting has been changed from this reading.


## 29 October 2026 — Effect A scale trial r1 implemented and compared

Approval: the student replied “Agreed” to the proposal to change `scale_amount_max` from 1.2 to 1.8, with the frame-by-frame prediction recorded in `CHANGE-BRIEF.md`.

Implementation: the config test expectation was changed first and failed on `setting-scale_amount_max` alone (actual 1.2, expected 1.8; `evidence/assignment-6/tuning/a-r1-tests/defeat_sparks_config-expected-failure.log`). The scene was then changed, after which every suite passed: logic 32, gameplay 65, audio 25 (realtime), A configuration 39, trail/upgrade configuration 79, real-input state 34. The existing ObjectDB/resource exit warnings remain. Pre-change source: `evidence/assignment-6/tuning/a-r0-source/`.

Capture: `captures/defeat_sparks/r1/`, run from the terminal with the same fixture as r0. Both strips now also retain file 9, the first visible frame. Comparison, measurements and hashes: `captures/defeat_sparks/comparison-r0-r1/`.

Result against prediction: the first frame grew from 11 × 12 to 14 × 14 (predicted about 15 × 15), and lit spark area grew 1.4–1.85× through 0.20 s. The footprint widened by only about 1 pixel, not the predicted 3–4, because particle positions set the extent. The widest point stays at or under 64 pixels (limit 68), and the fade ends on the same frame (file 21) with frames 30 and 50 empty. The initial cluster is still below one character height: 0.41 at the first frame and 0.71 by 0.07 s.

Running-game keep/revert verdict: pending.


## 29 October 2026 — Effect A scale trial r1 kept

After playing the game with `scale_amount_max` 1.8, the student replied “Keep it; it is clearer” (keep it; clearer). Verdict: keep r1. This running-game verdict is separate from the fixture comparison above, which measured a modest increase in lit spark area without a larger footprint or longer fade. No further A setting change is made. This completes A's observation-driven revision cycle: r0 strip, reading, prediction, approval, one-value edit, r1 strip, comparison and running-game verdict.

Quoted student feedback in this report is translated into English from the recorded conversation.


## Commit trace (added 9 November 2026)

Every revision above was committed in the same group of commits at 14:59 on 29 October, after the work. Git therefore does not separate the steps. GitHub IDs, with the course-repository IDs from SOURCE-REVISION.md in brackets:

| Revision | Scene, added already in its kept form | Pre-change source, strips and comparison | Records |
|---|---|---|---|
| B r1, trail alpha ramp 0.55/0.30/0 → 0.95/0.70/0 (kept) | `902a9f8` [`3a5be66`] | `8af1cf2` [`f85990b`]: `evidence/assignment-6/tuning/r0-source/`, `captures/lantern_trail/comparison-20261029-135607/` | `299668a` [`c3e1273`] |
| Celebration on overlay layer 11, then the UI portrait (kept) | `902a9f8` [`3a5be66`] | `8af1cf2` [`f85990b`]: `captures/play-checks/20261029-142138/upgrade-*` | `299668a` [`c3e1273`] |
| A r1, `scale_amount_max` 1.2 → 1.8 (kept) | `902a9f8` [`3a5be66`] | `8af1cf2` [`f85990b`]: `evidence/assignment-6/tuning/a-r0-source/`, `captures/defeat_sparks/r0/`, `r1/`, `comparison-r0-r1/` | `299668a` [`c3e1273`] |

Not met in this record (see TEST-REPORT.md, "Assignment 6 revision 3"):
- A's revision was not driven by something the student observed in the running game; it followed the student's "Done; no problem" and Claude's reading of r0.
- A's first verdict does not describe the effect in visual terms.
- B's before strip was re-rendered from the preserved r0 resource after the change, not captured before it.
- No point of agreement or disagreement between Claude's strip readings and the student's verdicts is recorded.


## 9 November 2026 — Effect A, revision r2

What I saw (running game; window size not yet stated): “The hit sparks are not eye-catching enough.”

Claude's reading of r1 (fixture capture, `captures/defeat_sparks/r1/strip/`). Measured in the burst region against file 30, which has no sparks, with the courier and text excluded. "Bright" means pixel luma above 150; the floor under the burst is luma 26–35.

| File | Time after first visible | Lit px | Extent | Mean colour (RGB) | Mean luma | Bright px |
|---:|---:|---:|---|---|---:|---:|
| 9 | 0.00 s | 121 | 14 × 14 | (255, 255, 246) | 254 | 121 |
| 10 | 0.03 s | 196 | 18 × 18 | (255, 252, 229) | 251 | 196 |
| 12 | 0.10 s | 244 | 30 × 29 | (252, 210, 152) | 215 | 244 |
| 15 | 0.20 s | 189 | 45 × 43 | (208, 140, 91) | 151 | 21 |
| 20 | 0.37 s | 6 | 38 × 57 | (70, 46, 53) | 51 | 0 |
| 30, 50 | — | 0 | — | — | — | — |

Against the intent:
- Files 9–10 are pure white, not pale yellow, because 16 additive sparks overlap. In play the white core coincides with the enemy's own pale hit flash (play checks `hit-dark-hit+00/+03`), so these frames do little to mark the hit.
- File 12 is the only frame that is both large and bright.
- By file 15 the burst has its full spread, but only 21 of 189 lit pixels are bright. The sparks have turned mid-orange at about 0.73 alpha.
- From 0.30 s they are dark specks barely above the floor.
- The "shrink and fade" phase therefore starts at about 0.20 s, but the sparks stop being readable at about the same moment. In a 1280 × 720 frame, the readable part is a 30–45 px cluster for roughly 0.07–0.20 s.
- Size and fade timing meet the brief: widest ≤ 64 px of the 68 px limit; last trace at 0.40 s.

Proposed change (one setting): `color_ramp`, middle stop moved from offset 0.35, RGBA (1, 0.6, 0.2, 0.85) to offset 0.6, RGBA (1, 0.75, 0.3, 1.0). The start stop (0: 1, 0.95, 0.65, 1) and the end stop (1: 0.65, 0.2, 0.05, 0) are unchanged. Nothing else changes: count, speed, spread, damping, gravity, scale range, scale curve, lifetime and texture.

Alternatives not proposed:
- A larger `scale_amount_max` was already tried in r1. It added lit area but not footprint or duration.
- A larger `amount` would change the 512-particle peak and its budget.
- A longer `lifetime` would break "gone by 0.45 s".

Claude's prediction for r2 (same fixture, seed 7280, files 9–50):
- Files 9–10: unchanged. Still about 14 × 14 and 18 × 18, still white from additive overlap.
- File 12 (0.10 s): same 30 × 29 extent and about 244 lit px, paler and brighter. Mean luma about 215 → 235–250, colour closer to pale yellow-white.
- File 15 (0.20 s): same 45 × 43 extent and about 190 lit px. Light yellow-orange instead of mid-orange: mean luma about 151 → 210–240, bright pixels 21 → 120 or more. This is the main visible difference.
- File 18 (0.30 s, not in the six-frame strip, read from the full sequence): orange specks clearly above the floor, mean luma about 80 → 150–180. Lit pixels similar (about 47–70), because the scale curve has shrunk most sparks to 1–3 px.
- File 20 (0.37 s): still nearly gone. At most a few more dim pixels (6 → about 6–15), because size is near zero by then.
- The last trace stays at file 21, or at most file 22 (≤ 0.43 s). Files 30 and 50 stay empty. The footprint and widest point do not change, because positions are unaffected.
- In play: the hit should read as a bright yellow burst for about twice as long, about 0.07–0.27 s instead of 0.07–0.20 s, at the same size. It ends orange and disappears at the same time as before.

Change: `color_ramp` middle stop 0.35:(1,0.6,0.2,0.85) → 0.6:(1,0.75,0.3,1.0), approved by the student (“Approve”). Pre-change source: `evidence/assignment-6/tuning/a-r1-source/`.
