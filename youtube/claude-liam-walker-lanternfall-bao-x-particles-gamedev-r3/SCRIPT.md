# SCRIPT — Lanternfall, Sparked Again

Narrator: Liam (in for Bear), Kokoro `am_onyx`. Source revision shown: `14e6b2c`. Timings are the measured narration (or the clip itself for game-sound beats).

## B00 · ASK · 0:00.0 (17.8 s)

*On screen:* composer card on cream; greeting 'Bonjour, Liam'; the reconstructed Walker prompt types in; send arms; running line names the brief and the session file; three result lines: effects, checks, kept changes

Bonjour — this is Liam, in for Bear. Bao Xing's particle assignment, revised: two effects in a Godot game that already works, each tuned from what Bao actually saw, tested, taken down to the shader Godot generates, and priced on the CPU and the GPU. The game is Lanternfall. Here is the ask, rebuilt from Bao's change brief.

## B01 · BLUF · 0:17.8 (14.5 s)

*On screen:* cream page; 'Particles are decoration' types; 'decoration' struck in terracotta, 'feedback' typed in; 'each one answers an event' and 'the rules stay untouched' type in

The short version. These particles are feedback, not decoration. Each one answers a real event in the game: a hit, a step, a new level. None of them may change a single rule. And the one change that counts was made because Bao looked at the game and said the sparks weren't enough.

## B02 · ASSIGNMENT · 0:32.3 (21.9 s)

*On screen:* CHANGE-BRIEF.md 'What I want to do' excerpt beside four requirement cards; card 1 highlights; card 2 highlights; card 3 highlights; card 4 highlights

What the assignment asks for, and what Bao's brief answers. Effect A, a burst of sparks on every weapon hit. Effect B, a short ember trail, only while the courier really moves. One change to each, driven by something seen in the running game, with a prediction and real frames before and after. Tests that read every setting back. And under the hood: the process shader Godot writes, and a price on the CPU and the GPU against a budget set in advance.

## B03 · REPORT · 0:54.2 (13.0 s)

*On screen:* the run under way: beam hits spark, the trail follows the courier; a level-up: the celebration on the card-screen portrait, cards held 2 s; card taken, play resumes

**[Game sound only — no narration.]** Game sound only, no narration: a stretch of the main take (seed 11, r2 sparks) with all three effects.

## B04 · CODE · 1:07.2 (27.1 s)

*On screen:* Godot editor reconstruction opens on effects/defeat_sparks.tscn, lines 19-32; line 21 highlights — EMISSION · amount = 16; line 26 highlights — EMISSION · explosiveness = 1.0: all on one frame; line 23 highlights — EMISSION · lifetime = 0.45 s; line 28 highlights — EMISSION · emission_shape = 0: point; line 30 highlights — PROCESS · spread = 180°; line 32 highlights — PROCESS · initial_velocity_min 25 (max 55 on line 33); line 31 highlights — PROCESS · gravity (0, 12); line 22 highlights — DRAW · texture = spark.png, 3 × 3; line 19 highlights — DRAW · CanvasItemMaterial, blend_mode 1 (add); source-notes panel (not Inspector values) lists the related lines

A particle system is one node that spawns many short-lived, slightly different copies, and it decides three things. Emission: when, and how many. Sixteen sparks, all on one frame, because explosiveness is one, each living forty-five hundredths of a second, from a single point. Process: how each one moves and changes. Spread one-eighty, speed from twenty-five, a little gravity; further down the file, damping, the scale curve and the colour ramp. Draw: what each one looks like. A three-pixel spark texture, through an additive material.

## B05 · RESULT · 1:34.4 (22.7 s)

*On screen:* r2 fixture strip, files 9–22, magnified 12×; courier on the left for scale; file 9 · EMISSION + DRAW: sixteen at once, added to white; files 12–17 · PROCESS: spread, damping, ramp; files 18–20 · PROCESS: scale curve to zero; file 21: last trace; file 22 empty

Those three decisions, in a real fixture capture of the current version. Emission puts all sixteen out on one frame, so the first frame is one white cluster: the additive draw adds overlapping sparks until they read as white. Process spreads them, slows them, and walks each one along the colour ramp and the scale curve: pale yellow through a quarter of a second, then shrinking orange specks. At four tenths of a second the last one is gone, because its lifetime ran out.

## B06 · CODE · 1:57.1 (20.4 s)

*On screen:* Godot editor reconstruction opens on effects/particle_presentation.gd, lines 47-57; line 49 highlights — PLAYING only · at most 32 live bursts; line 51 highlights — a new instance per accepted hit (overlap); line 53 highlights — global_position = the hit, in world space; line 56 highlights — restart(): one-shot burst; source-notes panel (not Inspector values) lists the related lines

Effect A starts with a signal. The session's damage function, which every weapon calls, announces each hit and where it landed. This listener answers it. Line forty-nine drops the hit unless the game is playing and fewer than thirty-two bursts are alive. Then a fresh burst is placed at the hit, in world space, and restarted. A new node per hit is the brief's overlap rule: a second hit never cuts off the first.

## B07 · RESULT · 2:17.4 (19.3 s)

*On screen:* real 4K capture, main take: beam hits spark at the monster; live-burst counter from the take's per-frame log; recorded state-test lines: 40 hits seen, 32 bursts, 512 particles

Here it is in the running game. Every time the beam connects, a small burst lands on the monster, and it keeps playing after the monster is gone. The counter comes from the take's own log: when hits land a few frames apart, it climbs, because bursts overlap instead of restarting each other. A stress test with forty hits in one volley confirms the cap: thirty-two bursts, never more.

## B08 · INTENT · 2:36.8 (17.0 s)

*On screen:* CHANGE-BRIEF.md visual intent, original 29 October text; r0 fixture strip, files 9, 11, 15, 21: the first strip; file 9: 11 × 12 px against a 34 px courier

Before any tuning, the brief said how the burst should read: a compact flash on the first frame, a fast spread by a fifth of a second, gone by forty-five hundredths, about one character high at the start and never more than two. The first strip, r zero, met the ceiling and the fade. Its first frame was a third of a character high.

## B09 · CODE · 2:53.7 (19.1 s)

*On screen:* Godot editor reconstruction opens on effects/defeat_sparks.tscn, lines 36-39; line 37 highlights — scale_amount_max 1.2 → 1.8; line 36 highlights — scale_amount_min 0.7 unchanged; source-notes panel (not Inspector values) lists the related lines

The first change, r one. In play Bao saw no problem; the strip disagreed with the brief's starting size. So one value moved, on line thirty-seven: the largest spark scale, from one point two to one point eight. That change came from Claude's reading of a strip, not from Bao's eyes in the game, which is why it is not the observed change the assignment asks for.

## B10 · RESULT · 3:12.8 (16.7 s)

*On screen:* r0 (top) vs r1 (bottom) contact sheet, 3× crops; prediction vs measured, row by row; the miss marked: predicted +3–4 px, measured +1 px; Bao's verdict: “Keep it; it is clearer”

Before on top, after below, same seed, same frames. The first frame grew from eleven to fourteen pixels, close to the predicted fifteen. The sparks got chunkier. But the footprint widened by one pixel, not the predicted three or four, because positions set the spread. Bao played it and kept it: clearer.

## B11 · CODE · 3:29.5 (19.7 s)

*On screen:* Godot editor reconstruction opens on effects/defeat_sparks.tscn, lines 12-14; line 13 highlights — offsets 0, 0.35, 1 → 0, 0.6, 1; line 14 highlights — middle colour (1, .6, .2, .85) → (1, .75, .3, 1); source-notes panel (not Inspector values) lists the related lines

The change that counts. Bao played the game and said the hit sparks weren't eye-catching enough. Claude's reading of the r one strip: bright for only a tenth of a second, mid-orange by a fifth. One setting: the colour ramp's middle stop moves from point three five to point six, and turns brighter and fully opaque. Prediction, written before the edit: brighter for longer, the same size, the same last frame.

## B12 · RESULT · 3:49.2 (21.5 s)

*On screen:* r1 (top) vs r2 (bottom) contact sheet, 3× crops; file 15: luma 151 → 236; bright px 21 → 189; file 17: bright px 2 → 83; predicted yellow-orange, measured pale yellow (255, 238, 163); Bao's verdict: “Yes” · “They don't get mixed up” · kept

Same seed, same frames. At a fifth of a second the sparks went from mid-orange to pale yellow, and every lit pixel crossed the brightness line: one hundred eighty-nine, against twenty-one. At a quarter second they are still bright. The footprint and the last frame did not move. The miss: Claude predicted yellow-orange, and additive overlap made it paler, close to white. Bao played it, checked it against the courier's lamp and the yellow gems, and kept it.

## B13 · CODE · 4:10.7 (20.3 s)

*On screen:* Godot editor reconstruction opens on effects/particle_presentation.gd, lines 121-131; line 126 highlights — distance actually moved; line 127 highlights — jump limit = speed × Δt × 2 + 4 ≈ 7 px; line 129 highlights — PLAYING · visible · 0.01 < distance ≤ limit; source-notes panel (not Inspector values) lists the related lines

Effect B, the trail, is decided once per physics frame. Line one twenty-six measures how far the courier actually moved since the last frame. Holding a key is not enough. Line one twenty-seven sets a jump limit, twice a frame's walk plus four pixels, so a teleport or a restart never draws a streak. Line one twenty-nine emits only while playing, visible, and genuinely moving.

## B14 · RESULT · 4:31.0 (16.3 s)

*On screen:* real 4K capture, props take: walking to the nearest stall; pushing into the stall: no displacement, no embers; down-right: sliding along the edge, trail back; per-frame strip: trail emitting yes / no, from the take's log

The proof is a wall. The script walks the courier up to a stall and holds right. The key is down, but he can't move, so no embers. Then it holds down and right: he slides along the edge, and the trail is back behind his feet. The line under the footage is the trail's emitting flag, read from the take's own per-frame log.

## B15 · CODE · 4:47.3 (18.9 s)

*On screen:* Godot editor reconstruction opens on effects/lantern_trail.tscn, lines 17-29; line 29 highlights — emission_sphere_radius = 3.0 (radius, px); line 28 highlights — emission_shape = 1: sphere (A uses 0: point); line 21 highlights — amount = 24 · continuous (one_shot = false); source-notes panel (not Inspector values) lists the related lines

The trail's scene shows the feature the burst doesn't use. It emits continuously from a sphere with a three-pixel radius, emission shape one, where the burst uses a single point. Twenty-four embers drift upward and fade from amber to dark orange in a third of a second. Its tuning change lives on line fourteen: the alpha at the start and the middle of each ember's life.

## B16 · RESULT · 5:06.2 (19.3 s)

*On screen:* trail fixture r0 (top) vs r1 (bottom), frames 12–39, crops; frames 20 and 39 marked; frames 51 and 60: both clear; play-check crop: trail flecks beside a hit spark

Bao's first look at the integrated game: the trail wasn't obvious. Raising only those two alpha values gave brighter embers at startup and in steady movement, with the same footprint, and both versions clear by the same frame after stopping. Bao played it and kept it. In normal play the trail stays two to four pixels per ember, still smaller and dimmer than a hit spark.

## B17 · CODE · 5:25.5 (18.5 s)

*On screen:* Godot editor reconstruction opens on effects/particle_presentation.gd, lines 59-70; line 59 highlights — leveled_up(level) signal; line 65 highlights — level_overlay: CanvasLayer 11, above HUD layer 10; line 66 highlights — position = the card-screen portrait; line 61 highlights — PLAYING only · ≤ 4 live celebrations; source-notes panel (not Inspector values) lists the related lines

The extra effect: a gold celebration on every level-up. Its first version was drawn in the world, under the upgrade screen's dark veil, and Bao found it hard to see. Now it goes into its own overlay layer, eleven, above the HUD, and line sixty-six anchors it to the little courier portrait on the card screen. At most four can be alive at once.

## B18 · RESULT · 5:44.0 (15.7 s)

*On screen:* real 4K capture, main take: level-up, card screen opens; crop of the portrait: white → gold → gone; Bao's verdict: “That works”

In the real take, the level-up arrives and the card screen opens. The burst lands on the small courier in the lower-left portrait, white first, then gold, and it's gone well before the scripted pick two seconds later. The cards stay readable. Bao looked at exactly this placement and said: that works.

## B19 · CODE · 5:59.7 (17.4 s)

*On screen:* Godot editor reconstruction opens on effects/particle_presentation.gd, lines 107-119; line 113 highlights — hit bursts: speed_scale 0 outside PLAYING; line 116 highlights — celebration: runs in PLAYING and LEVELUP; line 118 highlights — no spawning outside play or while hidden; source-notes panel (not Inspector values) lists the related lines

One policy runs every frame, and it only reads the game. When the game isn't playing, hit bursts and the trail get a speed scale of zero, so they freeze exactly where they are. The celebration keeps playing on the card screen. Outside play, or while the effect is hidden, the trail never spawns. On a loss or a win, everything is cleared.

## B20 · RESULT · 6:17.2 (20.1 s)

*On screen:* real 4K capture, main take: pause at run 0:30, held 2.5 s; two paused frames a second apart, side by side: 0 pixels differ; resume: the trail carries on; play-check shots: lost+00 and won+00, particles cleared (scripted, 1280 × 720); Bao's recorded check (TUNING.md)

At thirty seconds the script presses pause. Under the pause screen, the embers hang exactly where they were: two frames a second apart match pixel for pixel. Then play resumes and they carry on. The scripted play checks cover the endings: on the first frame of a loss or a win, every particle is gone. Bao's own check in the game: stop moving and the trail stops; pause and everything stays frozen.

## B21 · CODE · 6:37.2 (18.3 s)

*On screen:* Godot editor reconstruction opens on tests/test_particles_edges.gd, lines 57-69; line 57 highlights — fixture: courier touching the stall's left edge; line 60 highlights — real key event: D; line 69 highlights — blocked-push-never-emits; source-notes panel (not Inspector values) lists the related lines

Tests catch what a glance misses. This edge test puts the courier against a stall, holds the right key for thirty frames through the real input system, and counts two things: how far he moved, and how many frames the trail emitted. Both must be zero. Separately, the configuration tests read every value the brief names back from the loaded scenes.

## B22 · RESULT · 6:55.5 (24.9 s)

*On screen:* recorded suite totals: current-r2-validation; mutation: initial_velocity_min → initial_velocity, exit 1; windowed frames 45 × 43 → 40 × 42 px; mutation: spread 180 → 90, exit 1; edge suite with the guard removed: two FAILs; what no headless run can show

Recorded output, on this exact source: nine suites, three hundred twenty-seven checks, no failures, with the original game's tests unchanged. Then the proof the tests are real. Rename one property to its Godot three name, and the scene still loads, the burst still fires, a little tighter, and only the test notices. Change the spread without changing the brief, and it fails again. Delete the movement guard, and exactly two trail checks fail. None of this can say whether the effect looks right.

## B23 · CODE · 7:20.4 (26.7 s)

*On screen:* Godot editor reconstruction opens on shaders/particles_generated.gdshader, lines 148-161; line 149 highlights — scale_min/max ← brief scale_amount 0.7 / 1.8; line 161 highlights — color_ramp at age ← brief ramp, middle stop 0.6 (r2); line 155 highlights — COLOR starts from color_value; drawing happens elsewhere; source-notes panel (not Inspector values) lists the related lines

Under the hood. Converting a GPU copy of the burst in the editor produced this process shader. Two lines map straight onto the brief. Line one forty-nine picks each spark's size between scale min and max: the brief's point seven to one point eight. Line one sixty-one samples the colour ramp by the spark's age: the ramp whose middle stop r two moved to point six. Bao's explanation: this is the process stage, how a particle changes. The texture and the additive blend belong to the draw stage.

## B24 · RESULT · 7:47.1 (21.6 s)

*On screen:* real 4K fixture capture: CPU burst (left) vs GPU study copy (right); both pale yellow, then orange, shrinking; different random positions: CPU and GPU draw different random numbers

And what that shader does now. In the first film, the GPU copy stayed white and full-size, because its ramp and curve textures were missing. They were bound in the second revision, and the copy carries the current ramp. Same seed, same frames: the GPU copy now shrinks and turns from pale yellow to orange, like the CPU burst. Its random spread differs, and it turns orange a little sooner; the fade and the shrink are back.

## B25 · CODE · 8:08.7 (19.9 s)

*On screen:* Godot editor reconstruction opens on tests/cost_effects.gd, lines 58-63; line 58 highlights — a fresh Session for each condition; line 61 highlights — effects off: game.particles.free(); line 63 highlights — same fixture via run_started; source-notes panel (not Inspector values) lists the related lines

Last, the price. The cost script builds the same game twice for every condition. Line sixty-one is the switch: with effects off, the presentation node is freed before the run starts, so gameplay, enemies and input stay identical. Then it times interleaved trials of three hundred frames: idle, at the burst cap, moving, and on the card screen, with an empty scene as the control.

## B26 · RESULT · 8:28.6 (25.8 s)

*On screen:* CPU deltas against budgets: two r2 runs; B: +0.007 and −0.007 ms; ranges overlap; why headless ≈ 0 for GPU particles: no renderer, no process shader

The CPU price, from two separate runs on the current version: thirty-two live bursts add between five and ten hundredths of a millisecond a frame, against a budget of one. The trail's difference is so small that its sign flips between runs. Why trust a headless number here? Because these are CPU particles: the simulation runs on the processor even with nothing drawn. A GPU particle node would read near zero headless by construction, since a dummy renderer never runs its shader.

## B27 · PRICE · 8:54.4 (25.2 s)

*On screen:* GPU under GL Compatibility: 0.000 ms; editor Visual Profiler screenshots, A off / A on, Mobile + Vulkan, current r2; selected frames 715 / 782: GPU 0.62 → 5.21 ms; viewport-timer runs: A r2 −0.06 … +0.39 ms; budget verdict: unresolved

The GPU price is the honest part. Under the game's own renderer this Mac reports zero on every frame, which means no timing, not no cost. Under a Mobile Vulkan proxy, the editor's Visual Profiler gave A plus point seven of a millisecond on one pair of frames and plus four point six on another, against a budget of point seven five. Averaged timer runs ranged from about zero to plus point four. So A's GPU budget is not settled, and the trail's readings are noise.

## B28 · LEDGER · 9:19.6 (35.3 s)

*On screen:* ledger: mistakes caught; Claude against Bao: no disagreement; two prediction misses; uncertain: GPU budget; first-frame size; r2 paler than the brief; next step; human and AI contributions; texture source and revision shown

What else the record says. Mistakes caught along the way: a shader study missing its textures, two test fixtures that ran before their setup, a narrated width that was a radius, and a report that kept an old GPU line. No strip reading of Claude's was overruled; the strips corrected Claude's predictions twice. Still uncertain: the GPU budget, and a first frame under one character high. The next step: measure A on the GPU over many frames, not one. Bao made every observation and every keep decision, and rewrote the brief; Claude Code built and measured; Codex worked the editor and wrote two tests. The only particle texture is a three-by-three cross, written by a script.

## B29 · VERDICT · 9:54.9 (21.6 s)

*On screen:* artifact card 'Verdict', heading with the source tree; implemented line; tuning-evidence line; limits line; human-judgment line

The verdict. Implemented: three effects that answer real events and never write game state, with three hundred twenty-seven checks behind them. Each effect has one change driven by what Bao saw, with a prediction, real frames before and after, and the part of the prediction that missed. The limits stay written down: no GPU time on the shipped renderer, and an unsettled GPU budget on the proxy. Every keep-or-revert call was Bao's.

## B30 · HANDOFF · 10:16.5 (21.9 s)

*On screen:* composer card; greeting 'Your turn.'; the paste-ready prompt types in; three output lines: prediction first, capture, revert

Your turn. Paste this: Please use Walker to read the hit-spark scene in my Lanternfall project. Change only amount, from sixteen to twenty-four. Before running anything, predict the first visible frame and the frame at a fifth of a second in the fixture strip, which configuration check fails, and the new peak particle count at thirty-two bursts. Then capture the strip, compare, and put sixteen back. Write the prediction first; the miss is the lesson. Liam, in for Bear.

## B31 · OUTRO · 10:38.4 (13.7 s)

*On screen:* title 'Lanternfall, Sparked Again'; @NikBearBrown; slug-seeded mascot



Total: 10 min 52.1 s.
