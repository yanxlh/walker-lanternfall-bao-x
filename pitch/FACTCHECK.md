# FACTCHECK — Lanternfall: First Delivery (pitch film)

Every spoken or on-screen claim, checked on 23 November 2026. Verdicts: PASS (checked against the source), CORRECTED (wording changed to match the source), EXEMPT (a stated plan or Bao's own answer, labelled as such on screen).

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B00 | The narration is an AI voice reading Bao's script | PASS | Kokoro `am_onyx`, `beat_sheet.json` metadata | — |
| 2 | B00 | The title screen shown is a real capture of tag a7 | PASS | `capture/clean/take-pitch-seed21.json` (clean take, 1.0 s) | — |
| 3 | B01 | Real capture of the game at tag a7, scripted input | PASS | `capture/take-pitch-seed21-log.jsonl`; `capture-pitch-take.command` archives `a7`; label names `pitch_driver.gd`, seed 21 | — |
| 4 | B01 | "I only move. The Beam fires on its own." | PASS | `godot/features/player`, weapons fire automatically (CONCEPT.md core loop); driver presses only move and card actions | — |
| 5 | B01 | Enemies break into lamp oil; a full gauge pauses the run for three cards | PASS | take at 0:10 (card screen); GDD Game Flow | — |
| 6 | B01 | Maxed weapons fuse into Sunflare | PASS | log: card `sunflare` picked at frame 5336 after Beam 3/3, Moths 3/3 (HUD at 1:11) | — |
| 7 | B01 | Survive three minutes and the fog lifts | PASS | log: `ended`, `won`, `run_s` 180.0; result panel "3:00 — The fog lifts" | — |
| 8 | B01 | Four excerpts at real speed, game sound off | PASS | `tools/build_media.py` b01: four `video` layers, no speed filter, `audio: null` | — |
| 9 | B02 | The build is the next milestone from my GDD, version 0.3, 17 October | PASS | `gdd/GDD-v0.3.md` lines 5 and 201 | — |
| 10 | B02 | Post office menu, one contract, Lantern Gate at the end, the Engineer with turrets | EXEMPT | PROJECT-BRIEF.md (proposed; labelled PROPOSED on screen) | — |
| 11 | B03 | A successful delivery changes the destination; my doc calls it a visible consequence | PASS | GDD line 35 (PX-03) | — |
| 12 | B03 | The change survives a restart | EXEMPT | proposed: one saved record (final project brief requires one piece of data that survives a restart) | — |
| 13 | B03 | The Lantern Gate model exists today in a separate 3D room | PASS | `godot/a3/lantern_gate_room.tscn`, `evidence/a3/lantern-gate-room.png` (tag a3) | — |
| 14 | B04 | I have played Vampire Survivors, Brotato, 20 Minutes Till Dawn and Halls of Torment | EXEMPT | Bao's answer, 23 November 2026 | — |
| 15 | B04 | In Vampire Survivors a run's goal is to outlast the clock; in Brotato, twenty waves | PASS | the games' standard run goals (a timed stage; 20 waves) | — |
| 16 | B04 | Lanternfall gives a destination and a place that remembers | EXEMPT | proposed; labelled "(proposed)" | — |
| 17 | B05 | Roster rule: one advantage, one rule change, one weakness | PASS | GDD line 92 | — |
| 18 | B05 | The Engineer's turret holds an area at the cost of lower damage and speed | PASS | GDD line 86 | — |
| 19 | B05 | The turret will run on a state machine; the plan for A9's technique | EXEMPT | proposal; Final Portfolio brief lists the state-machine option | — |
| 20 | B06 | Target role gameplay programmer | EXEMPT | Bao's answer, 23 November 2026 | — |
| 21 | B06 | Post office menu with focus set; keys on screen | EXEMPT | proposed; storyboard labelled constructed | — |
| 22 | B06 | The test command exists: `scripts/run-all-a7.sh`, 23 runs | PASS | `evidence/a7-suite-20261123/RUN.txt` | — |
| 23 | B06 | Godot 4.7.2, Compatibility renderer, exported for macOS | PASS / EXEMPT | `godot/project.godot` (gl_compatibility); the export is planned | — |
| 24 | B07 | Hand-written shaders at tag a5 | PASS | `godot/shaders/hurt_tint.gdshader`, `cobblestone_surface.gdshader` (README, Assignment 5) | — |
| 25 | B07 | Particle effects with a cost report at tag a6 | PASS | `godot/effects/`, `evidence/a6-COST-REPORT.md` | — |
| 26 | B07 | Animation driven by state at tag a7 | PASS | `godot/animations/`, TEST-REPORT Assignment 7 | — |
| 27 | B07 | 23 headless runs pass from a fresh clone | PASS | `evidence/a7-fresh-clone-b744a09-RUN.txt`; repeated today in `evidence/a7-suite-20261123/RUN.txt` | — |
| 28 | B07 | 8 of 8 mutations are caught | PASS | `evidence/a7-mutations-r1.json` (8 entries, all caught) | — |
| 29 | B07 | It cannot prove that the game is fun; no playtest is claimed | PASS | no playtest is cited anywhere in the film | — |
| 30 | B07 | The A5 tile is the hand-written cobblestone shader on the material-room floor | PASS | `captures/a5-materials/20261030-131249-compare-shader-baseline/CAPTURES.md` (revision d01df00) | — |
| 31 | B08 | In and out lists | EXEMPT | PROJECT-BRIEF.md (proposed scope) | — |
| 32 | B08 | "One screen, one contract and the Engineer, before anything else" is my own risk table | PASS | GDD line 232 (R-01 mitigation) | — |
| 33 | B09 | My doc left open how a delivery ends | PASS | GDD line 240 (Q-01) | — |
| 34 | B09 | For this slice: survive until the fog lifts, then reach the gate | EXEMPT | Bao's pitch decision for this slice (PROJECT-BRIEF §6); labelled proposed | — |
| 35 | B09 | Today the run ends with the result panel at 3:00 | PASS | take at 3:00, tag a7 | — |
| 36 | B10 | Turrets are a risk the GDD names | PASS | GDD line 234 (R-03) | — |
| 37 | B10 | On my Mac, Godot reports 0 ms GPU time under Compatibility | PASS | `evidence/a6-COST-REPORT.md`, GPU results: "0.000 ms on every frame of every condition" (Apple M4) | Machine named as Apple M4, as the report states |
| 38 | B10 | Sparks at the cap cost +0.025 ms CPU per frame; budget 1.0 ms | PASS | `evidence/a6-COST-REPORT.md`, CPU results, "A at cap, whole volley cycle" | — |
| 39 | B10 | The A6 cost test's method; a Vulkan proxy for GPU | PASS | `godot/tests/cost_effects.gd`; COST-REPORT "Mobile, Vulkan via MoltenVK" | — |
| 40 | B11 | New to me: Godot and GDScript, shaders and materials, particles; already had: animation, state machines, testing | EXEMPT | Bao's answers, 23 November 2026 | — |
| 41 | B11 | Tag a7 is the evidence for the skills already had | PASS | items 26–28 | — |
| 42 | B12 | Left column exists with tags; right column does not exist; no export yet | PASS | `git tag`, `8a6f988`; no `godot/export_presets.cfg` at a7 | — |
| 43 | B12 | Due 20 December 2026, tag a10 | PASS | Canvas, Final Portfolio Piece (read 23 November 2026) | — |
| 44 | narration | "tag A-five" etc. are voiced as letters and numbers | CORRECTED | first takes were heard as "tag of five" by a whisper transcript | hyphenated in the script, re-voiced, re-checked (`word-times.json`) |
