# FRICTIONAL — Assignment 8, final project pitch film

Bao Xing. Roles: Bao chose the project, answered the questions only Bao can answer, and checks the film. Claude Code drafted the brief and the script, built the film and ran the checks. The entries list what was done each day.

## 23 November 2026

- Assignment 8 read on Canvas: due Tuesday 24 November, 23:59; 50 points.
- Project: Lanternfall, taken to the next playable milestone in my Assignment 4 GDD (v0.3, 17 October). Instruction to Claude: "Read the memory and do it according to the GDD."
- My answers, given on a question card:
  - Games I have played: Vampire Survivors, Brotato, 20 Minutes Till Dawn, Halls of Torment.
  - Target role: gameplay programmer.
  - New to me in this course: Godot and GDScript, shaders and materials, particle effects.
  - Why this project: both learning and showing what I have.
- The Final Portfolio brief on Canvas sets four requirements for the final: the A9 game-AI technique, one piece of data that survives a restart, a start or pause menu, and an export. The pitch maps the GDD's next milestone onto them:
  - post office menu → front door;
  - one saved delivery record → persistence;
  - the Engineer's turret on a state machine → planned A9 technique;
  - macOS export.
- Cut from the GDD's milestone, by its own risk R-01: the difficulty selector and the other four couriers.
- The GDD was copied into `pitch/gdd/` (docx and pdf) and converted to Markdown for the checker. The GDD text was not changed.
- Capture of tag a7 with a scripted driver (adapted from the Assignment 2 film):
  - Headless seed search: seeds 5 and 21 win with Sunflare; 3, 7, 11 and 14 lose. Seed 21 recorded.
  - About half the Movie Maker frames were written while the window could not draw (5,897 of 12,023). The driver had paused the game for those frames, so dropping them leaves a continuous 3:24 take.
- Today's run of the a7 suite in the a8 worktree: 23 of 23 runs exit 0; no tracked file under `godot/` changed.
- Narration problem: the AI voice reads "tag A five" as "tag of five". Fix: hyphenate to "A-five"; re-voiced and checked with a transcript.
- The brutalist components that print the instructor's handle (the title outro, the design board, the composer) were not used: the assignment forbids the instructor's name, persona or credit line. The boards are drawn with Pillow instead.
- `art godot-gdd --check` passes: 16 sections, 8 exact excerpts, 9 evidence files.
- First `art final`: Gate V refused the film.
  - The boards crossed the title-safe edge by about 12 px.
  - The full-width footage crossed every edge and failed whole-frame contrast.
  - The closing card was too empty.
- Fixes: the boards were scaled into the safe area; the footage was framed inside it, with its two text regions declared for the contrast check; real stills were added to the closing card.
- Second run: clean. Master: 3:45.5, 3840 × 2160, SHA-256 `02e49cb8…aa5bbb`.

## Still to do (Bao)

- Watch the whole film with sound, and say what is wrong or what to keep.
- Read PROJECT-BRIEF.md. The scope decisions in it were drafted by Claude from my answers; change anything I do not agree with.
- Upload the MP4 to Google Drive, push the branch and tag `a8`, and submit on Canvas.
