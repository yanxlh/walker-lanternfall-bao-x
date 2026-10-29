# SCRIPT — Lanternfall, Sparked

Narrator: Liam (in for Bear), Kokoro `am_onyx`. Source revision shown: `c3e1273`. Timings are the measured narration (or the clip itself for game-sound beats).

## B00 · ASK · 0:00.0 (17.3 s)

*On screen:* composer card on cream; greeting 'Bonjour, Liam'; the reconstructed Walker prompt types in; send arms; running line names the brief and the session file; three result lines: effects, checks and revision, verdicts

Bonjour — this is Liam, in for Bear. Bao Xing's particle assignment: add two effects to a Godot game that already works, tune each one from what you actually see, test it, read the shader Godot generates, and price it on the CPU and the GPU. The game is Lanternfall again. Here is the ask, rebuilt from Bao's change brief.

## B01 · BLUF · 0:17.3 (12.9 s)

*On screen:* cream page; 'Particles are decoration' types; 'decoration' struck in terracotta, 'feedback' typed in; 'each one answers an event' and 'the rules stay untouched' type in

The short version. These particles are feedback, not decoration. Each one answers a real event in the game: a hit, a step, a new level. And none of them is allowed to change a single rule. That contract is what the rest of this film checks.

## B02 · ASSIGNMENT · 0:30.2 (17.8 s)

*On screen:* CHANGE-BRIEF.md 'Tuning and acceptance' excerpt beside four requirement cards; card 1 highlights; card 2 highlights; card 3 highlights; card 4 highlights

What the assignment asks for. Two effects that use different particle features. One change to each, driven by something observed, with real frames before and after. Tests that read every setting back. And a look under the hood: the process shader Godot writes, plus the cost on the CPU and the GPU against a budget written down in advance.

## B03 · REPORT · 0:47.9 (13.0 s)

*On screen:* the run under way: beam hits spark, the trail follows the courier; a level-up: the celebration on the card-screen portrait, cards held 2 s; card taken, play resumes

**[Game sound only — no narration.]** Game sound only, no narration: a stretch of the main take (seed 11) with all three effects.

## B04 · CODE · 1:00.9 (18.0 s)

*On screen:* Godot editor reconstruction opens on effects/particle_presentation.gd, lines 47-57; line 49 highlights — PLAYING only · at most 32 live bursts; line 53 highlights — global_position = the hit, in world space; line 56 highlights — restart(): one-shot burst; source-notes panel (not Inspector values) lists the related lines

Effect A starts with a signal. The session's damage function, which every weapon calls, now announces each hit and where it landed, before any health comes off. This listener answers it. Line forty-nine drops the hit unless the game is playing and fewer than thirty-two bursts are alive. Then a fresh burst is placed at the hit, in world space, and restarted.

## B05 · RESULT · 1:18.9 (18.5 s)

*On screen:* real 4K capture, main take: beam hits spark at the monster; crop follows the courier; live-burst counter from the take's per-frame log; recorded state-test lines: 40 hits seen, 32 bursts, 512 particles

Here it is in the running game. Every time the beam connects, a small burst lands on the monster, and it keeps playing after the monster is gone. The counter is read from the take's own log: when hits come close together, bursts overlap instead of restarting each other. A stress test with forty hits in one volley confirms the cap: thirty-two bursts, never more.

## B06 · CODE · 1:37.4 (18.3 s)

*On screen:* Godot editor reconstruction opens on effects/defeat_sparks.tscn, lines 23-35; line 26 highlights — explosiveness = 1.0: one frame; line 23 highlights — lifetime = 0.45 s; line 28 highlights — emission_shape = 0: point; line 30 highlights — spread = 180°; line 34 highlights — damping 20–30; source-notes panel (not Inspector values) lists the related lines

The burst itself is data in a scene file, not code. Sixteen sparks, all released on the same frame, because explosiveness is one. They live forty-five hundredths of a second. They start from a single point and fly in any direction, with spread at one-eighty. Speed is twenty-five to fifty-five, damping slows them, and a little gravity pulls them down.

## B07 · RESULT · 1:55.7 (19.1 s)

*On screen:* r1 fixture strip, files 9–21, magnified 3×; courier on the left for scale; file 9: 14 × 14 px cluster; file 15: 45 × 43 px, separate sparks; 64 px of a 68 px limit; file 21: last trace; file 22 empty

What those numbers make, frame by frame, from a real fixture capture on the market floor. On its first visible frame the burst is a compact white cluster. By a fifth of a second it has spread into separate yellow-orange sparks. At its widest it reaches sixty-four pixels, under the two-character limit of sixty-eight, and the last pixel goes out at four tenths of a second.

## B08 · CODE · 2:14.8 (16.1 s)

*On screen:* Godot editor reconstruction opens on effects/defeat_sparks.tscn, lines 36-39; line 37 highlights — scale_amount_max 1.2 → 1.8; line 36 highlights — scale_amount_min 0.7, curve and ramp unchanged; source-notes panel (not Inspector values) lists the related lines

Now the tuning. In the game, Bao saw no problem. The frame strip disagreed with the brief: on its first frame, the cluster was a third of a character high, not about one. So one value changed, on line thirty-seven: the largest spark scale, from one point two to one point eight. Nothing else moved.

## B09 · RESULT · 2:30.8 (19.6 s)

*On screen:* r0 (top) vs r1 (bottom) contact sheet, 3× crops; prediction vs measured table, row by row; the miss marked: predicted +3–4 px, measured +1 px; Bao's verdict: Keep it; it is clearer

Before on top, after below, same seed, same frames. The first frame grew from eleven to fourteen pixels, close to the predicted fifteen. The sparks got chunkier, with up to eighty-five percent more lit area. But the footprint widened by one pixel, not the predicted three or four, because positions set the spread. Fade timing didn't change. Bao played it and kept it: clearer.

## B10 · CODE · 2:50.4 (20.2 s)

*On screen:* Godot editor reconstruction opens on effects/particle_presentation.gd, lines 121-131; line 126 highlights — distance actually moved; line 127 highlights — jump limit = speed × Δt × 2 + 4 ≈ 7 px; line 129 highlights — PLAYING · visible · 0.01 < distance ≤ limit; source-notes panel (not Inspector values) lists the related lines

Effect B, the trail, is decided once per physics frame. Line one twenty-six measures how far the courier actually moved since the last frame. Holding a key isn't enough. Line one twenty-seven sets a jump limit, twice a frame's walk plus four pixels, so a teleport or a restart never draws a streak. Line one twenty-nine emits only while playing, visible, and genuinely moving.

## B11 · RESULT · 3:10.6 (16.3 s)

*On screen:* real 4K capture, props take: walking to the nearest stall; pushing into the stall: no displacement, no embers; down-right: sliding along the edge, trail back; per-frame strip: trail emitting yes / no, from the take's log

The proof is a wall. The script walks the courier up to a stall and holds right. The key is down, but he can't move, so no embers. Then it holds down and right: he slides along the edge, and the trail is back behind his feet. The line under the footage is the trail's emitting flag, read from the take's own per-frame log.

## B12 · CODE · 3:26.9 (19.0 s)

*On screen:* Godot editor reconstruction opens on effects/lantern_trail.tscn, lines 17-29; line 29 highlights — emission_sphere_radius = 3.0 (radius, px); line 28 highlights — emission_shape = 1: sphere (A uses 0: point); line 21 highlights — amount = 24 · continuous (one_shot = false); source-notes panel (not Inspector values) lists the related lines

The trail's scene shows what makes it a different effect. It emits continuously from a sphere with a three-pixel radius, emission shape one, where the burst used a point. Twenty-four embers drift slightly upward and fade from amber to dark orange in a third of a second. Its tuning change lives on line fourteen: the alpha at the start and the middle of each ember's life.

## B13 · RESULT · 3:45.9 (19.3 s)

*On screen:* trail fixture r0 (top) vs r1 (bottom), frames 10–60, crops; frames 20 and 39 marked; frames 51 and 60: both clear; play-check crop: trail flecks beside a hit spark

Bao's first look at the integrated game: the trail wasn't obvious. Raising only those two alpha values gave brighter embers at startup and in steady movement, with the same footprint, and both versions clear by the same frame after stopping. Bao played it and kept it. In normal play, the trail stays two to four pixels per ember, still smaller and dimmer than a hit spark.

## B14 · CODE · 4:05.2 (18.5 s)

*On screen:* Godot editor reconstruction opens on effects/particle_presentation.gd, lines 59-70; line 59 highlights — leveled_up(level) signal; line 65 highlights — level_overlay: CanvasLayer 11, above HUD layer 10; line 66 highlights — position = the card-screen portrait; line 61 highlights — PLAYING only · ≤ 4 live celebrations; source-notes panel (not Inspector values) lists the related lines

The extra effect: a gold celebration on every level-up. Its first version was drawn in the world, under the upgrade screen's dark veil, and Bao found it hard to see. Now it goes into its own overlay layer, eleven, above the HUD, and line sixty-six anchors it to the little courier portrait on the card screen. At most four can be alive at once.

## B15 · RESULT · 4:23.7 (15.7 s)

*On screen:* real 4K capture, main take: level-up, card screen opens; crop of the portrait: white → gold → gone; Bao's verdict: That works

In the real take, the level-up arrives and the card screen opens. The burst lands on the small courier in the lower-left portrait, white first, then gold, and it's gone well before the scripted pick two seconds later. The cards stay readable. Bao looked at exactly this placement and said: that works.

## B16 · CODE · 4:39.4 (18.1 s)

*On screen:* Godot editor reconstruction opens on effects/particle_presentation.gd, lines 110-119; line 113 highlights — hit bursts: speed_scale 0 outside PLAYING; line 116 highlights — celebration: runs in PLAYING and LEVELUP; line 118 highlights — trail.emitting = false outside play; source-notes panel (not Inspector values) lists the related lines

One policy runs every frame, and it only reads the game. When the game isn't playing, hit bursts and the trail get a speed scale of zero, so they freeze exactly where they are. The celebration keeps playing on the card screen, so it doesn't stall on its first frame. And outside play, the trail never spawns. On a loss or a win, everything is cleared.

## B17 · RESULT · 4:57.5 (19.7 s)

*On screen:* real 4K capture, main take: pause at run 0:30, held 2.5 s; two paused frames a second apart, side by side: 0 pixels differ; resume: the trail carries on; play-check shots: lost+00 and won+00, particles cleared (scripted, 1280 × 720); Bao's verdict: Nothing is obscured; everything behaves normally

At thirty seconds the script presses pause. Under the pause screen, the trail's embers hang exactly where they were: two frames a second apart match pixel for pixel. Then play resumes and they carry on. The scripted play checks cover the endings: on the first frame of a loss or a win, every particle is gone. And after a normal run of their own, Bao's note was that nothing got in the way.

## B18 · CODE · 5:17.3 (18.2 s)

*On screen:* Godot editor reconstruction opens on tests/test_particles_edges.gd, lines 57-69; line 57 highlights — fixture: courier touching the stall's left edge; line 60 highlights — real key event: D; line 69 highlights — blocked-push-never-emits; source-notes panel (not Inspector values) lists the related lines

Tests catch what a glance misses. This edge test puts the courier against a stall, holds the right key for thirty frames through the real input system, and counts two things: how far he moved, and how many frames the trail emitted. Both must be zero. A configuration test, separately, reads every value in every effect scene back from the engine.

## B19 · RESULT · 5:35.5 (19.2 s)

*On screen:* recorded suite totals, final pre-commit run; mutation output: blocked-push-never-emits (30 frames), jump-frame-no-emission; mutation frames: r1 vs initial_velocity, 45 × 43 → 40 × 42 px

Recorded output from the committed build: seven suites, two hundred ninety-two checks, no failures, with the original game's tests unchanged. Then the experiment that shows the test is real: delete the movement guard, and exactly two trail checks fail. And an old Godot 3 property name loads without a warning; the burst just spreads a little tighter. Only the test noticed.

## B20 · CODE · 5:54.7 (19.2 s)

*On screen:* Godot editor reconstruction opens on shaders/particles_generated.gdshader, lines 340-352; line 345 highlights — TRANSFORM[3].xyz += final_velocity × DELTA; line 347 highlights — process_display_param: colour ramp + scale curve at age; line 352 highlights — COLOR handed to the draw stage; source-notes panel (not Inspector values) lists the related lines

Under the hood. Godot turned a GPU copy of the burst into this generated process shader. Every frame, for every spark, it adds up the velocity, moves the spark, and then samples the colour ramp and the scale curve by the spark's age, on line three forty-seven. In Bao's words, this is the process stage: how a particle changes. Drawing it is a separate stage.

## B21 · RESULT · 6:13.9 (21.5 s)

*On screen:* real 4K fixture capture: CPU burst (left) vs editor-converted GPU copy (right); left: yellow → orange, shrinking; right: white, full-size; callout: ShaderMaterial has no color_ramp / scale_curve

And here's what that shader does with the material the editor produced, same seed, same frames. On the left, the game's CPU burst shrinks and fades through yellow to orange. On the right, the GPU copy stays white and full-size until it vanishes: the conversion left the ramp and curve textures off, so line three forty-seven has nothing to sample. The sparks still fly out; the colour fade and the shrink are gone.

## B22 · CODE · 6:35.4 (18.8 s)

*On screen:* Godot editor reconstruction opens on tests/cost_effects.gd, lines 58-63; line 58 highlights — a fresh Session for each condition; line 61 highlights — effects off: game.particles.free(); line 63 highlights — same fixture via run_started; source-notes panel (not Inspector values) lists the related lines

Last, the price. The cost script builds the same game twice for every condition. Line sixty-one is the switch: with effects off, the whole presentation node is freed before the run starts, so gameplay, enemies and input stay identical. Then it times five interleaved trials of three hundred frames, idle, at the burst cap, moving, and on the card screen.

## B23 · RESULT · 6:54.2 (19.2 s)

*On screen:* CPU deltas as bars against their budgets (headless, 5 trials); A spawn p95 ≈ +0.10 ms; GPU under GL Compatibility: 0.000 ms, every frame; Mobile/Vulkan proxy deltas within ±0.1 ms, labelled proxy

The measured price. On the CPU, thirty-two live bursts add about nine thousandths of a millisecond a frame, a tenth at the spawn spike, and the trail four thousandths, all far under budget. The GPU number is the honest part: under the game's renderer, this Mac reports zero on every frame. A Vulkan proxy can measure it, and the difference stays inside the noise.

## B24 · VERDICT · 7:13.4 (20.1 s)

*On screen:* artifact card 'Verdict', heading with the source revision; implemented line; tuning-evidence line; limits line; human-judgment line

The verdict. Implemented: three effects that answer real events and never write game state, with two hundred ninety-two checks behind them. Each tuning change has a prediction, real frames and a verdict, including the part of the prediction that missed. The limits are written down: no readable GPU time on this renderer, and a first frame still under one character high. The keep-or-revert calls were Bao's.

## B25 · HANDOFF · 7:33.5 (20.5 s)

*On screen:* composer card; greeting 'Your turn.'; the paste-ready prompt types in; three output lines: prediction first, capture, revert

Your turn. Paste this: Please use Walker to read the trail scene in my Lanternfall project. Change only the emission sphere radius from three to eight. Before running anything, predict how the trail's width and brightness change at fixture frames twenty and thirty-nine, and which configuration check fails. Then capture both strips, compare, and put three back. Write the prediction first; the miss is the lesson. Liam, in for Bear.

## B26 · OUTRO · 7:54.0 (13.7 s)

*On screen:* title 'Lanternfall, Sparked'; @NikBearBrown; slug-seeded mascot

**[Outro card — stock jingle only, no narration.]**

Total: 8 min 7.7 s.

Student feedback quotations above are English translations of the recorded statements.
