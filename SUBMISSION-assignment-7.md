Assignment: Assignment 7 - Doing Animation with Claude and Godot
Student: Bao Xing
Project name: walker-lanternfall-bao-x (Lanternfall)
GitHub repository URL: https://github.com/yanxlh/walker-lanternfall-bao-x
Git tag and submitted commit SHA: a7 — not tagged yet (tag after the human checks); give the SHA from `git rev-list -n 1 a7` in the Canvas note
Godot version, renderer, and operating system: Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility; macOS 26 on Apple M4
Clip 1, sprite, looping: `walk` on the courier. Route: Sprite2D with an AnimationPlayer frame track (`Body:frame`, discrete updates, nearest interpolation), cells 2 and 3 of pc_sheet.png held 8 ticks each, length 16 / 60 s, LOOP_LINEAR. Driven by the courier's state machine in godot/features/player/player.gd.
Clip 2, rig, committing action: `dash` on the courier. Route: cutout rig baked from code. godot/features/player/build_courier_visual.gd builds Head, Arm, Coat and Legs (region rectangles of cell 2) under Hips, Chest and Neck pivots and saves courier_visual.tscn and courier_clips.tres with ResourceSaver. Phases: startup 6, active 10, recovery 12 ticks; keys at every phase boundary; LOOP_NONE. Driven by the same state machine.
Sprite source, author and licence: godot/assets/art/pc_sheet.png, my own generated sheet from Assignment 2 (ART-PC-01: FLUX.1-schnell, Apache-2.0, run locally, processed by gen/art_process.py; ASSET-LOG.md and SOURCES.md), committed since Assignment 2. No found sheet; the file was not edited.
Slicing: 32 x 32 px cells, 10 columns x 1 row, no padding; frame order as POSES in player.gd; cell pixel (16, 23) on the courier's origin. Registration measured: drift under one pixel between the walk cells.
The dash (my design): unlocked by a new level-up card, Courier's Dash; Shift / Space / B; 55 px at 330 px/s; not invincible; a 60-tick gap after every dash.
Clocks: the AnimationPlayer runs in ANIMATION_CALLBACK_MODE_PROCESS_MANUAL and is seeked once per 60 Hz simulation tick from integer tick counters; no AnimatedSprite2D, AnimationTree or method track; no gameplay fact keyed in a clip.
Final film URL and filename: pending
Final film SHA-256: pending
Summary of my work: I chose the committing action and its rules (a dash; not invincible; a gap between dashes; obtained through a level-up card). Still to do: play the build at normal speed and at 0.25, measure a reference dash and keep or change the phase table, judge the walk and the dash, and watch the film. Claude Code drafted the brief and CLAUDE.md and wrote the pin, the builder, the clips, the state machine, the dash, every test, the captures, the mutation run and these records. Details: CONTRIBUTIONS-assignment-7.md and TEST-REPORT.md (Assignment 7).
Checks run: at 9ccf078 after an import from an empty cache, 14 baseline runs pass (459 checks; 543 with test_hurt_tint at three rates). Pin test_courier_pin 23/23 before the change, after the refactor and after the dash. A Movie Maker replay of the pin timeline is pixel-identical after the refactor (216/216 frames). Read-back test_courier_clips 73/73; structure test_courier_states 9/9; test_dash_edges 41/41 at 30, 60 and 144 fps. All 14 baseline runs pass after the dash. Mutations: 8/8 caught.
Known limitations: the phase table is Claude's draft and no reference has been measured; at the strongest lean the coat separates from the legs; adding the card changes seeded card offers; no dash sound or cooldown display; the human checks are pending.
Changed games since Assignment 2 (yes/no; if yes, FRICTIONAL.md entry): no — the same Lanternfall.
