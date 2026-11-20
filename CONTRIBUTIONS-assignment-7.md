# Assignment 7 — Contributions

## Student

I chose the committing action and set its rules on 13 November 2026: "Add a dash. The dash is not invincible, but there is a time gap between every two dashes, and the dash has to be obtained through an in-game level-up card." Earlier the same day I asked Claude Code to read the assignment page and then to complete the assignment. Later I asked for the dash timing to change from 6 / 10 / 12 to 4 / 10 / 6 frames, and I kept it: "Keep 4/10/6."

On 18 November I rewrote CHANGE-BRIEF.md in my own words, with the predicted failures and the seven short answers. At my request Claude Code corrected two statements in it (the startup "compression" and the "brighter dash rig"); the brief lists each correction and the measurement behind it.

On 20 November I checked every reference in Claude Code's CLAUDE.md draft; nothing needed changing, so there is no correction commit, only this record.

On 20 November I reported the human checks, recorded the r1 and r2 frame strips and the film's take myself, made revision r2 from what I saw in play (my observation and prediction in TUNING.md; I approved the outline) and kept it: "Keep. It is clearer." I watched the whole final film (8:51, SHA-256 `3ce7f3f2…b131b`): "Watched it. Good." Not yet done, and mine to do: upload the film; push; submit on Canvas.

## AI assistance

Claude Code (one session, 13 November 2026) read the Canvas page and the lecture notes and drafted CHANGE-BRIEF.md, including the phase table and the keys, and the A7 CLAUDE.md. It also did the following:
- wrote the pin test and the Movie Maker replay, then the builder that saves the scene and clip library;
- wrote the read-back test, the switch from `_draw()` to the Sprite2D and AnimationPlayer, the state machine, the dash, the card and the input;
- wrote the structure and edge tests, the mutation script, the Godot 3 names probe, the capture and strip tools and the playtest launcher;
- ran every test and mutation, and the 13 November Movie Maker replays, from the terminal, and read the strips (the 30 fps strips and the film's take I recorded myself);
- made the film: the take driver and its command (I ran it), the beat sheet and narration text, the evidence beats, the edit and its checks (`youtube/claude-liam-walker-lanternfall-bao-x-animation-gamedev/SOURCES.md`);
- wrote README, TEST-REPORT, SUBMISSION and this file, and made the local commits on branch `assignment-7` (I push).

Codex reviewed the frame strips and wrote the 4 / 10 / 6 proposal that I asked for. Codex wrote its review files into the worktree, and they were moved to the Trash at my request; nothing else of Codex's is in the branch.

The three prompts in the assignment were not pasted one by one; the work was done from the brief in one session. The tuning prompt, filled in for this project, is in TEST-REPORT for the tuning cycle after play.

## Verification limits

Claude's reading of the frame strips is a claim, not a human check. Headless runs draw nothing; the pixel comparison and strips come from windowed Movie Maker runs on this Mac. I played the dash and reported the human checks on 20 November (TEST-REPORT, HUMAN CHECKS).

No other people contributed.
