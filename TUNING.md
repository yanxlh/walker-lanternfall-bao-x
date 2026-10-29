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
