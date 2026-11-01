# SCRIPT — Lanternfall, Shaded

Narrator: Liam (in for Bear), Kokoro `am_onyx`. Source revision shown: `4246f94`. Timings are the measured narration (or the clip itself for game-sound beats).

## B00 · ASK · 0:00.0 (19.2 s)

*On screen:* composer card on cream; greeting 'Ciao, Liam'; the reconstructed Walker prompt types in; send arms; running line names the brief and the shader files; three result lines: the tint, the material, checks and revision

Ciao, this is Liam, in for Bear. Bao Xing's shader assignment for Lanternfall: write a shader from code that shows a game state, give a 3D object a textured shader, and answer four questions about shaders, materials, textures and Godot's shading language, each one pointing at a line of Bao's own code. Here's the ask, rebuilt from Bao's change brief.

## B01 · BLUF · 0:19.2 (11.5 s)

*On screen:* cream page; 'Shaders are magic' types; 'magic' struck in terracotta, 'arithmetic' typed in; 'a line, a number, a hint' and 'predicted, then measured' type in

The short version. Shaders aren't magic, they're arithmetic. Here, one line of code, one number from the game and one texture hint decide what you see. Each was predicted by hand, then measured in the engine.

## B02 · ASSIGNMENT · 0:30.7 (20.6 s)

*On screen:* CHANGE-BRIEF.md · State and purpose excerpt beside 4 cards; card 1 highlights; card 2 highlights; card 3 highlights; card 4 highlights

What the assignment asks for, and how Bao answered it. A shader from code that communicates a state: here, the courier turns yellow after an accepted hit and fades back as his forty-eight ticks of protection run out. A textured shader on a 3D object: the floor and the stand-in of the Assignment 3 room. Four questions, each answered at a line of code. And tests, with an honest list of what they can't show.

## B03 · LISTEN · 0:51.3 (6.0 s)

*On screen:* the run under way at 0:37: the courier walks toward the nearest monster; a level-up card screen, held 2 s by the script, then a card is picked; a moth reaches him: the hurt sound, the courier yellow, the yellow fading

**[Game sound only — no narration.]** Game sound only, no narration: frames 1240-1419 of the hurt take (seed 5), real speed.

## B04 · PREDICT · 0:57.3 (26.3 s)

*On screen:* CHANGE-BRIEF.md · 2D shader design excerpt beside 4 cards; card 1 highlights; card 2 highlights; card 3 highlights; card 4 highlights

Before any code ran, Bao's brief fixed the colour line and worked out the answers by hand. The line mixes the incoming colour toward yellow by hurt amount: at zero the drawing passes through, at one it's yellow. Halfway, the lamp head should land at two forty-eight point five, two nineteen point five, thirty-seven point five, and the coat at one fifty point five, one fifty-six point five, forty-four point five. In the red blink the same mix keeps more red. And two point oh, set from code, should not be clamped.

## B05 · CODE · 1:23.6 (22.1 s)

*On screen:* Godot editor reconstruction opens on shaders/hurt_tint.gdshader, lines 1-9; line 1 highlights — shader_type canvas_item: the 2D pipeline; line 4 highlights — hurt_amount: the game's one number in; line 7 highlights — fragment(): runs per rasterized fragment; line 8 highlights — mix(incoming COLOR, yellow, hurt_amount); source-notes panel (not Inspector values) lists related lines

Here's Bao's hand-written shader, all nine lines. Line one makes it a canvas item shader, for 2D sprites. Line four declares hurt amount, the one number the game sends in; its hint range only shapes the Inspector slider. Then fragment, on line seven, runs for every pixel the courier covers, and line eight is the whole effect: the incoming colour, mixed toward yellow. That's what a shader does: a small function, run for every pixel.

## B06 · RESULT · 1:45.7 (25.5 s)

*On screen:* white phase: courier crops at hurt_amount 0 / 0.5 / 1, sampled texels ringed; predicted vs measured table, lamp and coat; red-phase crops at 0 / 0.5 / 1 (iframes 27); the 2.0 capture: read back 2.0, both texels (255, 255, 0)

Now the engine's answer, from in-engine captures with the simulation frozen and the value set by a debug key. At zero, the lamp and the coat match their stored colours exactly. At one half, the lamp reads two forty-nine, two twenty, thirty-seven: inside one byte of the hand table. In the red phase the same line keeps more red, and at one both phases are the same yellow. And two point oh, set from code, reads back as two point oh. The hint didn't clamp it; the output just saturates.

## B07 · CODE · 2:11.2 (21.9 s)

*On screen:* Godot editor reconstruction opens on effects/hurt_tint_presentation.gd, lines 18-30; line 22 highlights — _process: refresh every frame; line 26 highlights — iframes / 48, clamped to 0..1; line 27 highlights — MENU, WON, LOST: 0.0; line 30 highlights — set_shader_parameter("hurt_amount", …); source-notes panel (not Inspector values) lists related lines

The driver connects the game to that uniform. Every frame, line twenty-two calls refresh. Line twenty-six turns the courier's remaining invulnerability ticks into a fraction: forty-eight ticks is one, zero is zero, clamped. Outside playing, paused or the level-up screen, it's forced to zero, so a lethal hit can't leave him yellow. And line thirty sets the shader parameter. The driver only reads the game; it never writes it.

## B08 · RESULT · 2:33.1 (22.2 s)

*On screen:* real 4K capture, hurt take (seed 5): hit 2 at run 0:41.9, the courier yellow; PAUSED: hurt_amount held at 0.4792 for 45 frames, readout from the take's log; hit 3: a monster keeps touching him (frames 1661–1666), hp stays 7; held frames of hit 3, labelled, from 1.0 to 0.0; readout: blink on/off beside the tint

Now the running game, with scripted input through the real input map. A monster connects, and the courier is yellow at once. The script presses pause, and the tint holds at twenty-three forty-eighths, because the counter stops with the simulation. Resume, and it drains. On the next hit a monster keeps touching him while he's protected, and nothing restarts. Frame by frame: one to zero in forty-eight ticks, eight tenths of a second, with the red blink still showing through.

## B09 · CODE · 2:55.3 (19.9 s)

*On screen:* Godot editor reconstruction opens on a5/material_room.tscn, lines 7-18; line 10 highlights — instance of res://a3/lantern_gate_room.tscn; line 8 highlights — PlaneMesh 8 × 8 m for the floor; line 14 highlights — Floor/Mesh ← cobblestone_warm_floor.tres; line 18 highlights — StandIn/Mesh ← cobblestone_cool_standin.tres; source-notes panel (not Inspector values) lists related lines

The textured shader goes on a 3D object. Bao's Assignment 5 room doesn't copy the Assignment 3 room: line ten instances it, and only a few things change. The floor's mesh becomes an eight by eight metre plane, line fourteen gives the floor the warm cobblestone material, and line eighteen gives the stand-in the cool one. The A3 room file itself stays untouched.

## B10 · RESULT · 3:15.3 (18.2 s)

*On screen:* real engine capture: the material room from the fixed pose (captures/a5-materials/20261030-170452-pair); floor rectangle marked: cobblestone_warm_floor.tres; stand-in rectangle marked: cobblestone_cool_standin.tres; enlarged crops of both rectangles

Here's that room in the engine, at the film's revision. The floor is repeated warm paving, two by two tiles of square stones. The stand-in wears the same stones, larger and cooler, catching the lantern's light. Both are lit by the A3 room's own lights, from a fixed camera pose, so every later capture can be compared pixel for pixel.

## B11 · CODE · 3:33.4 (19.6 s)

*On screen:* Godot editor reconstruction opens on a5/materials/cobblestone_warm_floor.tres, lines 8-18; line 10 highlights — shader = cobblestone_surface.gdshader; line 11 highlights — the three maps: colour, normal, roughness; line 15 highlights — uv_scale = 2.0; line 16 highlights — roughness 0.55–0.95; source-notes panel (not Inspector values) lists related lines

So what's a material? This file. Line ten points at the shader. Lines eleven to thirteen hand it the three maps. And lines fourteen to eighteen are just values: a warm tint, the map repeated twice, a matte roughness range. The stand-in's file points at the same shader with different values: cooler, larger, shinier. The shader is the code; each material is a set of numbers for it.

## B12 · RESULT · 3:53.0 (17.3 s)

*On screen:* real engine captures: baseline (uv_scale 2) beside floor uv_scale 4 (captures/a5-materials/20261030-170456-one-material); floor crops, before and after; measured: floor max difference 72, stand-in 0

The proof that values live in the material. The capture tool changes only the floor's u v scale, from two to four, in memory. The floor's stones get smaller and denser, and its pixels change by up to seventy-two levels. The stand-in, wearing the same shader, doesn't change by a single level. Shared code, separate numbers.

## B13 · CODE · 4:10.3 (20.3 s)

*On screen:* Godot editor reconstruction opens on shaders/cobblestone_surface.gdshader, lines 17-24; line 18 highlights — uv = UV × uv_scale; line 19 highlights — ALBEDO = colour sample × tint; line 21 highlights — NORMAL_MAP = the normal sample; line 22 highlights — depth × mix(0.5, 1.0, |NORMAL.z|)  (0b91838); source-notes panel (not Inspector values) lists related lines

Now the shader side, Bao's fragment function. Line eighteen scales the u v coordinates. Line nineteen samples the colour map and multiplies by the tint: that's the albedo. Line twenty-one hands the normal map to the engine. And line twenty-two is Bao's latest edit: the relief's depth is scaled by how squarely the surface faces the camera, half strength edge-on, full strength face-on.

## B14 · RESULT · 4:30.6 (26.6 s)

*On screen:* Bao's prediction, recorded before the edit (PREDICTION.md, his words); real engine captures: baseline beside Bao's ALBEDO × 0.5 edit (captured at e5c0272, before line 22 changed); measured means: floor and stand-in both fall; every pixel changed; Bao's observation, verbatim; agent run, labelled: ALBEDO × (0, 1, 0), both green, shader restored byte for byte

Change the shader instead, and both objects move. Bao wrote his prediction first: multiply the end of the albedo line by one half, and the floor and the stand-in both darken, because they share this shader, while stone size and relief stay the same. He edited line nineteen by hand, captured, and restored it. Every pixel in both rectangles changed, and his observation matched the prediction. An earlier Codex run made a similar edit, turning both green, and broke the rule that agents never touch Bao's shaders.

## B15 · CODE · 4:57.2 (20.4 s)

*On screen:* Godot editor reconstruction opens on shaders/cobblestone_surface.gdshader, lines 1-5; line 3 highlights — color_tex : source_color — colour data; line 4 highlights — normal_tex : hint_normal — directions; line 5 highlights — roughness_tex: no colour hint — raw numbers; line 1 highlights — shader_type spatial: the 3D pipeline; source-notes panel (not Inspector values) lists related lines

Why is a texture information? Because the same kind of file can hold three kinds of data, and only the hint tells the engine which. Line three marks the colour map source color: these bytes are colour. Line four marks the normal map hint normal: these are directions. Line five, roughness, has no colour hint at all: raw numbers. And line one, shader type spatial, puts all of it in the 3D pipeline.

## B16 · RESULT · 5:17.6 (23.2 s)

*On screen:* the three source PNGs, each labelled with its line and hint; recorded output: curl_ratio for nor_gl and nor_dx, both conventions; real engine crops: floor at normal_strength 0 and 1 (20261030-170453-sweep)

Here are the three files: colour, a purple-blue map of directions, and grey numbers. A map of directions can be checked like data. This normal map's curl ratio is zero point two two in the OpenGL convention and one point seven eight read as DirectX, and the DirectX calibration file is its mirror image, so it's a real surface in the right convention. And on the floor, normal strength zero against one changes how the stone joints are shaded.

## B17 · CODE · 5:40.8 (17.4 s)

*On screen:* Godot editor reconstruction opens on shaders/cobblestone_surface.gdshader, lines 7-15; line 7 highlights — group_uniforms Surface; line 11 highlights — group_uniforms Response; line 9 highlights — uv_scale : hint_range(0.25, 4.0) = 1.0; line 14 highlights — tint · uv_scale · roughness min / max · normal_strength; source-notes panel (not Inspector values) lists related lines

The rest of the top is the material's interface. Group uniforms, on lines seven and eleven, sort the settings into Surface and Response panels in the Inspector. Each hint range sets a slider's limits, not a rule: line nine lets u v scale run from a quarter to four. These five numbers are everything a material can change.

## B18 · RESULT · 5:58.2 (30.8 s)

*On screen:* fifteen real engine captures in a 5 × 3 grid (captures/a5-materials/20261030-170453-sweep, values in memory); uv_scale row highlighted: 0.25 / 2 / 4; roughness rows highlighted; tint row highlighted: black; stand-in mean (31.42, 40.97, 74.83) in every capture; normal_strength row again, with Bao's look quoted from TEST-REPORT.md

The sweep moves each of those five numbers, one at a time, on the floor only: low, the material's own value, then high. U v scale changes the stones' size, the roughness ends move the warm highlight, normal strength sets the relief, and a black tint takes the stone colour away. Through all fifteen captures the stand-in never moves. Bao's look at the new normal strength row: at zero, the surface is flatter and the normal relief is off; at one, the stone edges and joints look more three-dimensional; at two, stronger light and dark relief, deeper joints, an exaggerated bump.

## B19 · CODE · 6:28.9 (17.6 s)

*On screen:* Godot editor reconstruction opens on shaders/hint_experiment.gdshader, lines 5-14; line 5 highlights — color_sample : source_color; line 6 highlights — raw_sample: no hint; line 7 highlights — use_color picks the sampler; line 11 highlights — ALBEDO = the chosen sample; source-notes panel (not Inspector values) lists related lines

The cleanest test of a hint is Bao's own experiment. One three-pixel grey image, bound to two samplers: line five with source color, line six without. Line seven picks which one a quad uses, and line eleven or thirteen writes the sample straight to albedo, unshaded. Same bytes in, so any difference out is the hint.

## B20 · RESULT · 6:46.5 (22.6 s)

*On screen:* the brief's prediction table: Compatibility vs Forward+/Mobile; real engine capture of the hint scene (captures/a5-materials/20261030-131056-hint), band centres sampled; Forward+ column marked: predicted, not measured

The prediction depended on the renderer. In Forward plus or Mobile, the unhinted quad should come out lighter, about one thirty-seven, one eighty-eight, two twenty-five. Under this project's Compatibility renderer, both should read sixty-four, one twenty-eight, one ninety-two. Measured: sixty-four, one twenty-eight, one ninety-two, on both quads. That matches the Compatibility prediction. The Forward plus difference is still a prediction; it wasn't measured here.

## B21 · CODE · 7:09.2 (17.9 s)

*On screen:* Godot editor reconstruction opens on shaders/standard_generated.gdshader, lines 1-7; line 1 highlights — automatically converted from StandardMaterial3D; line 3 highlights — shader_type spatial — Bao's :1; line 7 highlights — texture_albedo : source_color — Bao's :3; source-notes panel (not Inspector values) lists related lines

For comparison, Godot can write a shader itself. Bao converted a standard material holding the same three maps, and the editor produced this. Line one says it's automatic. Line three is the same spatial shader type as Bao's line one, and line seven marks the albedo sampler source color, exactly like Bao's line three.

## B22 · RESULT · 7:27.0 (26.4 s)

*On screen:* verbatim line pairs, generated vs Bao's, from the hashed files; film fixture renders: editor-generated material vs Bao's shader, neutral values; difference map ×8, face-on: 87–93 % of pixels within 2 levels; difference map ×8, tilted 50°: mean 2.4–2.8 levels

Lined up: generated line seven against Bao's line three, nineteen against four, thirty-five against nineteen. Different names, same jobs. To see whether they draw the same, this film rendered both on the same plane under one light, as a labelled fixture. Face-on, about nine pixels in ten agree within two levels of two fifty-five. Tilt the camera fifty degrees and they drift apart, by nearly three levels on average, which is consistent with Bao's line twenty-two weakening his relief at a slant.

## B23 · ANSWERS · 7:53.4 (22.5 s)

*On screen:* LANGUAGE-NOTES.md · Bao's answer 8 excerpt beside 4 cards; card 1 highlights; card 2 highlights; card 3 highlights; card 4 highlights

So, the four questions, each at a line. What a shader does: hurt tint line eight, a function run for every fragment. How a material differs from a shader: one shader, two material files of values. Why a texture is information: lines three to five say colour, directions, or raw numbers. And what Godot's shading language adds: shader types, hints wired to the Inspector, and outputs like albedo and normal map that plug straight into Godot's lighting.

## B24 · CODE · 8:15.9 (18.0 s)

*On screen:* Godot editor reconstruction opens on tests/test_hurt_tint.gd, lines 155-166; line 155 highlights — fixture: a wraith 20 px to the right; line 157 highlights — parsed key event: Enter starts the run; line 159 highlights — wait for an accepted hit; line 162 highlights — parsed key event: W walks away; source-notes panel (not Inspector values) lists related lines

The tests drive the real game. This run places one wraith twenty pixels away, presses a real Enter key to start, waits for a real contact to land, then holds W to walk away. A sampler that runs after everything else records the uniform every frame. The test never calls the driver or sets the value itself.

## B25 · RESULT · 8:33.9 (32.1 s)

*On screen:* recorded: test_hurt_tint at 30 / 60 / 144 fps, first value, zero tick, game time, allowed; recorded: test_materials 127/0 and the ten earlier suites, 332/0; recorded mutation logs: semicolon 4/28, rename 3/28, source_color 1/127; what a headless run cannot show

Recorded output, re-run for this film on a clean copy of the film's revision. Twenty-eight of twenty-eight at thirty, sixty and a hundred forty-four frames per second: the tint reaches zero forty-eight ticks after the hit, eight tenths of a second of game time, within one frame. One twenty-seven of one twenty-seven material checks, and the three hundred thirty-two earlier checks unchanged. Then Bao's three mutations: a missing semicolon fails four checks, a renamed uniform fails three, a dropped source color fails one. What no headless run can show is the colour on screen; that's why the captures exist.

## B26 · LIMITS · 9:06.0 (30.2 s)

*On screen:* TEST-REPORT.md 'What the agent got wrong (Assignment 5)', six rows, plus the Codex shader edit; open items from TEST-REPORT.md and README.md; one next step

**[Outro card — stock jingle only, no narration.]**

## B27 · ROLES · 9:36.1 (28.8 s)

*On screen:* SOURCES.md, Assignment 5: Bao's work and decisions; SOURCES.md: what Claude Code wrote, prompts in evidence/assignment-5/agent/; texture credit: Cobblestone Floor 08, Rob Tuytel, CC0; source revision 4246f94

Who did what. Bao hand-wrote the three shaders and the line twenty-two edit; an earlier Codex draft of the tint lived in another copy. He wrote the brief, the predictions and the language notes, ran the mutations, made the editor conversion and the scene decisions. Claude Code wrote the driver and its tests, the material audit, the builder and the capture tools, after Bao approved each plan. The texture is Poly Haven's Cobblestone Floor zero eight, by Rob Tuytel, released CC zero. The code you saw is revision four two four six f nine four.

## B28 · VERDICT · 10:04.9 (20.5 s)

*On screen:* artifact card 'Verdict', heading with the source revision; implemented line; prediction line; limits line; human-judgment line

The verdict. Implemented: a nine-line tint that shows the courier's protection, and a textured shader with two materials, with no gameplay rule changed and every number predicted before it was measured. The limits are written down: Compatibility can't show what source color changes elsewhere, and a headless test can't see colour. The human judgments, the playtest and the looks, are Bao's own, quoted where he gave them.

## B29 · HANDOFF · 10:25.4 (22.0 s)

*On screen:* composer card; greeting 'Your turn.'; the paste-ready prompt types in; three output lines: prediction first, capture, revert

Your turn. Paste this: Please use Walker to read the cool stand-in material in my Lanternfall project. Change only u v scale from one to three. Before running anything, predict which rectangle of the pair capture changes, how the stand-in's stones change, and which material check fails. Then capture the pair, compare it with your prediction, and put one back. It tests whether you really believe a material is just numbers. Write the prediction first. Liam, in for Bear.

## B30 · OUTRO · 10:47.4 (9.5 s)

*On screen:* title 'Lanternfall, Shaded'; @NikBearBrown; slug-seeded mascot



Total: 10 min 56.9 s.
