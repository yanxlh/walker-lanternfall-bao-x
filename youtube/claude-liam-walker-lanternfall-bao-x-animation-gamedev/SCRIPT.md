# SCRIPT — Lanternfall in Frames

Narrator: Liam (in for Bear), Kokoro `am_onyx`. Source revision shown: `5f09b7f`. Timings are the measured narration (or the clip itself for game-sound beats).

## B00 · ASK · 0:00.0 (17.4 s)

*On screen:* composer card on cream; greeting 'Hola, Liam'; the reconstructed Walker prompt types in; send arms; running line names the brief and the player script; three result lines: the walk, the dash, checks and revision

Hola, this is Liam, in for Bear. Bao Xing's animation assignment for Lanternfall: two clips, one made from a sprite sheet and one that moves a rig. One loops, one commits. One authority drives them both. And four ideas to explain, each at a line of Bao's own clip, test or brief. Here's the ask, rebuilt from Bao's change brief.

## B01 · BLUF · 0:17.4 (13.4 s)

*On screen:* cream page; 'An animation is a movie' types; 'movie' typed in terracotta, deleted, 'list of keys' typed in its place; 'tracks, a driver, a table' and 'judged in play' type in

The short version. An animation isn't a movie, it's a list of keys. Here, a few tracks of numbers, one driver and a phase table written in frames decide what you see. And whether the motion reads is something only Bao, playing the game, could judge.

## B02 · ASSIGNMENT · 0:30.8 (22.3 s)

*On screen:* CHANGE-BRIEF.md · Bao's brief excerpt beside 4 cards; card 1 highlights; card 2 highlights; card 3 highlights; card 4 highlights

What the assignment asks, and how Bao answered it. One clip from a sprite sheet: the courier's walk, two cells of Bao's own sheet from Assignment 2. One clip that moves a rig: a dash, cut from one of those cells into head, arm, coat and legs. The walk loops; the dash commits, with startup, active and recovery. One authority drives both. And four ideas Bao has to explain: what a clip is, one authority, two clocks, and feel designed in frames.

## B03 · PREDICT · 0:53.1 (30.8 s)

*On screen:* CHANGE-BRIEF.md · Bao's dash rules excerpt beside 4 cards; card 1 highlights; card 2 highlights; card 3 highlights; card 4 highlights

Bao's brief, rewritten in Bao's own words, sets the dash down in frames at sixty a second. Startup, four frames: the courier dips and leans back, direction locked. Active, ten frames: fifty-five pixels at three hundred thirty a second. Recovery, six frames, still locked. Then a one-second cooldown. It's not invincible: each phase has its own rule for a hit. And the predicted failures, each with the check that would catch it: the body blending into dark ground, a gap between coat and legs, a hesitation at the loop, and cast frames mistaken for loop errors.

## B04 · CODE · 1:23.8 (19.6 s)

*On screen:* Godot editor reconstruction opens on features/player/courier_visual.tscn, lines 9-15; line 11 highlights — texture = Bao's pc_sheet.png; line 13 highlights — offset (-16, -23): cell pixel (16, 23) on the origin; line 14 highlights — hframes = 10, vframes left at 1; source-notes panel (not Inspector values) lists related lines

Here's the slicing, in the scene file. Body is a Sprite two D, and this line points it at Bao's sheet. Centered false, with that offset, puts the cell's pixel sixteen, twenty-three on the courier's origin, the centre of the courier's hurtbox. Then hframes ten cuts the sheet into ten frames across. Which picture frame three is, is decided by that number, not by the image.

## B05 · RESULT · 1:43.4 (19.0 s)

*On screen:* pc_sheet.png, 8x, with the 10 x 1 grid and cell numbers; captures/walk/r1, Bao's 30 fps fixture strip, frames labelled with cell and pose from frames.log; Bao's verdict on the strip, quoted

Here's the sheet, cut the way hframes says: ten cells, thirty-two pixels each. The walk uses cells two and three. In Bao's own strip at thirty frames a second, the first three frames are the cast pose, the auto-attack firing, and the log says pose equals cast: not a broken loop. Then cell three for four frames, cell two for four. Bao checked the strip for drift: none.

## B06 · CODE · 2:02.4 (19.7 s)

*On screen:* Godot editor reconstruction opens on animations/courier_clips.tres, lines 415-425; line 418 highlights — NodePath("Body:frame"); line 422 highlights — keys at 0 and 8/60 s; line 424 highlights — update 1 = UPDATE_DISCRETE; line 425 highlights — cells 2 and 3; source-notes panel (not Inspector values) lists related lines

A clip is a list of keys, not a movie. This is the walk's frame track, in the clip resource. The path line names a node and a property: Body, frame. The times are zero and eight sixtieths of a second; the values, cells two and three. Update one means discrete: hold each value until the next key. And if the path named a property that didn't exist? Nothing would complain. The track would just do nothing.

## B07 · RESULT · 2:22.1 (19.3 s)

*On screen:* take, 4K, walking: courier and the live cell readout from the take's log; read-back numbers: last key 3, interval 8, tail 8 (test_courier_clips walk-seam); Bao's human check, quoted

In the running game, from a scripted take: the walk under the courier, with the clip's cell beside it, read from the take's own per-frame log. Two, then three, every four movie frames, which is eight ticks. The seam rule for a frame track: no duplicate across the wrap, and the gap from the last key to the end equals the key interval. Eight and eight. Bao watched it wrap at normal speed: no stutter.

## B08 · CODE · 2:41.4 (22.2 s)

*On screen:* Godot editor reconstruction opens on features/player/build_courier_visual.gd, lines 45-53; line 46 highlights — DASH_STARTUP 4 · ACTIVE 10 · RECOVERY 6; line 50 highlights — Rig:position keys at 0, 3, 4, 14, 16, 20; line 51 highlights — Hips keys on the same boundaries; source-notes panel (not Inspector values) lists related lines

Feel is designed in frames. The builder carries Bao's phase table: four, ten, six, at sixty a second. Every track has a key at each phase boundary: zero, four, fourteen and twenty. The spacing follows the phase: transition two through startup, an ease-in that accelerates into the push; one, linear, while active; point five through recovery, settling. When play says the timing is wrong, the table changes, and the keys follow.

## B09 · RESULT · 3:03.6 (27.6 s)

*On screen:* phase table rows beside key times in seconds; captures/dash/r1, Bao's fixture strip: frames 5, 7, 12, 15 with tick and dash frame from frames.log; the r0 → r1 revision, from CHANGE-BRIEF Revisions and TUNING

Here's the table beside the keys built from it: frame four is four sixtieths of a second, fourteen is fourteen sixtieths, twenty is a third. And Bao's strip at thirty frames a second, read at each boundary against the log: the trigger frame, upright; active begins, leaning in; recovery begins, settling; then back on the walk sprite. The table started at six, ten, twelve. A Codex reading pointed out that recovery stood still longer than the dash moved, and Bao asked for four, ten, six, and kept it.

## B10 · CODE · 3:31.2 (21.3 s)

*On screen:* Godot editor reconstruction opens on features/player/player.gd, lines 209-218; line 216 highlights — clip_and_time(): clip and time from tick counters; line 217 highlights — anim.play(clip); anim.seek(time, true); line 209 highlights — manual mode: moves only when the simulation ticks; source-notes panel (not Inspector values) lists related lines

One authority. This function is the only code that plays or seeks the courier's Animation Player. It asks the state machine for a clip and a time, both from integer tick counters: the walk ticks, or the dash ticks over sixty. Then play, and seek. The player is in manual mode, so it never advances on a clock of its own. The clip moves only when the sixty-hertz simulation ticks, which is the same tick gameplay reads the dash on.

## B11 · RESULT · 3:52.5 (22.8 s)

*On screen:* take: level-up screen, the Courier's Dash card first (fixture), key 1; take: the first dash, with state, phase and dash frame from the take's log; recorded output: two-clocks-at-30/60/144fps

The real game, through the real input map, from the scripted take. A level-up offers the Courier's Dash card. The fixture puts it first, and a real one key picks it. The courier walks, then dashes: startup, active, recovery, read live from the take's log, and the rig replaces the sprite. Measured by the edge tests on every rendered frame: zero seconds between the clip's time and the gameplay tick, at thirty, sixty and a hundred forty-four frames per second.

## B12 · CODE · 4:15.3 (15.4 s)

*On screen:* Godot editor reconstruction opens on features/player/player.gd, lines 233-240; line 233 highlights — the hit lands in every phase; line 236 highlights — startup: cancel, no cooldown; line 239 highlights — recovery: end the dash, cooldown starts; source-notes panel (not Inspector values) lists related lines

Not invincible. A hit lands in every phase. Then the match on the dash phase applies Bao's rules: in startup, the dash is cancelled and no cooldown starts, because no dash happened. In recovery, the rest is cut, and the cooldown starts. An active dash carries on, damage and all.

## B13 · RESULT · 4:30.8 (21.4 s)

*On screen:* take: dash with a hit on startup frame 2 (placed wraith, fixture); take: hit on active frame 8, the dash continues; take: hit on recovery frame 16, cancelled, cooldown 60; recorded output: hit-before/on/after at boundaries 4, 14, 20

In play, three more dashes, each hit once. A wraith is placed on the courier for one step, a disclosed fixture. Hit on startup frame two: the dash is gone, the hurt pose shows, no cooldown. Hit on active frame eight: damage, and the dash keeps going. Hit on recovery frame sixteen: cancelled, and the sixty-tick cooldown starts. The edge tests check every boundary a frame before, on, and a frame after, at three frame rates.

## B14 · CODE · 4:52.2 (18.7 s)

*On screen:* Godot editor reconstruction opens on tests/test_courier_clips.gd, lines 56-66; line 57 highlights — 3D transform tracks name a bone, not a property; line 61 highlights — blend-shape tracks name a shape on the mesh; line 64 highlights — property tracks: sub in node; source-notes panel (not Inspector values) lists related lines

The read-back. This check walks every track of every clip and resolves it: first the node, then the property, or a bone for a 3D transform track, or a blend shape. The last branch is the one that matters here: a property name that isn't on the node gets reported, instead of failing in silence. It proves a track points at something real, not that it points at the right thing.

## B15 · RESULT · 5:10.8 (32.4 s)

*On screen:* recorded: courier_clips 86/0, assertion groups; recorded mutations-required.json: 5, 1, 3 failures; empty cache passes; recorded probe: loop = true loads as LOOP_LINEAR in 4.7.2; what a headless run cannot show

Recorded output: eighty-six of eighty-six read-back checks. Then the assignment's four mutations, each in its own git worktree. Rename the rotation property, and track problems reports it. Switch the walk's loop off, and the loop check fails. Key cell ten on a ten-cell sheet, and three checks fail. Reimport from an empty cache, and everything still passes, because a cutout rig has no importer setting to lose. One surprise: in Godot four point seven, a Godot three style loop equals true still loops; only the name scan catches it. What no headless run can show is whether the motion reads.

## B16 · CODE · 5:43.2 (19.4 s)

*On screen:* Godot editor reconstruction opens on features/player/build_courier_visual.gd, lines 208-218; line 208 highlights — every pixel of the cell, and one beyond each edge; line 210 highlights — skip opaque pixels; test the four neighbours; line 216 highlights — neighbour inside the part's region; source-notes panel (not Inspector values) lists related lines

Revision two came from Bao's own eyes. On the dark slate, the coat and legs disappeared; only the lamp read. Bao predicted a thin, low-brightness outline would separate the body. This function finds the outer ring of the cell's silhouette: transparent pixels touching an opaque one. Then it keeps only the ring pixels next to the coat and the legs, and the builder draws them behind each part.

## B17 · RESULT · 6:02.6 (20.4 s)

*On screen:* Bao's strips r1 (top) and r2 (bottom), frames 4, 5, 7, 12, 15; TUNING.md: Claude's comparison, a claim; TUNING.md: Bao's verdict, quoted

Bao's two strips, same position, same ticks: r one above, r two below. The logs match tick for tick; the outline appears on frames five, seven and twelve. Claude's reading: on the back of the coat, the sheet's dark ink sits between the outline and the visible coat, so the edge can look detached. Bao judged it in the running game: keep it, it's clearer. That's the disagreement, recorded, and the verdict is Bao's.

## B18 · ANSWERS · 6:23.1 (28.2 s)

*On screen:* CHANGE-BRIEF.md · Bao's answer 5 excerpt beside 4 cards; card 1 highlights; card 2 highlights; card 3 highlights; card 4 highlights

So, the four ideas, each at a line. What a clip is: keys on a node and a property, and a missing property fails silently unless the read-back resolves it. What one authority means: only the show function plays and seeks; a second writer would win by node order, not by design. What the two clocks are: the clip is seeked on the same sixty-hertz tick gameplay reads, measured zero seconds apart. And what feel in frames means: Bao's table, four, ten, six, became keys at zero, four, fourteen and twenty.

## B19 · LIMITS · 6:51.3 (28.4 s)

*On screen:* TEST-REPORT.md 'Agent mistakes caught while building'; TEST-REPORT.md departures and README Known limitations; one next step

What the agent got wrong, as the test report lists it: a pin that read the hit sixty ticks late, an edge test that read the phase after the hit, a structure test that compared the clip with the wrong moment, a re-pin that missed a hard-coded five, and a header edit lost in a chained command. Still uncertain: no reference dash was measured, the four, ten, six timing came from a reading rather than from play, and the real-input pin was added after the change. The next step: measure a reference dash, and retime from it.

## B20 · ROLES · 7:19.6 (28.6 s)

*On screen:* CONTRIBUTIONS-assignment-7.md: Bao's work and decisions; what Claude Code wrote; prompts in prompts/assignment-7.md; godot/assets/art/ATTRIBUTION.md; source revision 5f09b7f

Who did what. Bao chose the dash and its rules, wrote the brief and the seven answers, saw the body vanish on dark ground and predicted the fix, approved it, recorded every thirty-frame strip, and gave every verdict. Claude Code wrote the builder, the clips, the state machine, the dash, the tests and this film. Codex proposed the four, ten, six timing. The sheet is Bao's own, generated in Assignment two with FLUX one schnell, Apache two point oh. The code you saw is revision five f zero nine b seven f.

## B21 · VERDICT · 7:48.2 (21.1 s)

*On screen:* artifact card 'Verdict', heading with the source revision; implemented line; checked line; limits line; human-judgment line

The verdict. Implemented: a walk on a frame track and a dash on a cutout rig, driven by one authority, with Bao's rules for every phase. Checked: pins before and after, eighty-six read-back checks, edges at three frame rates, four mutations, and two clocks measured zero seconds apart. The limits are written down. And the human judgments, the strips, the play checks, keep four, ten, six, keep the outline, are Bao's own.

## B22 · HANDOFF · 8:09.3 (30.8 s)

*On screen:* composer card; greeting 'Your turn.'; the paste-ready prompt types in; three output lines: prediction first, strip, re-pin

Your turn. Paste this: Please use Walker to read the dash in my Lanternfall clip library. In my phase table, change only the recovery from six frames to nine, and let it flow down: the builder's keys, the read-back's expected times, and a re-pin of the edge tests in its own commit. Before running anything, predict which strip frames change and what the courier shows on dash frame sixteen. Then record strip r three and compare it with your prediction. It tests whether you believe the table, not the keys, is the design. Write the prediction first. Liam, in for Bear.

## B23 · OUTRO · 8:40.0 (10.4 s)

*On screen:* title 'Lanternfall in Frames'; @NikBearBrown; slug-seeded mascot

**[Outro card — stock jingle only, no narration.]**

Total: 8 min 50.4 s.
