# CHECKS-REPORT

## Beat classification

24 beats: 24 SHOW / 0 justified HOLD / 0 PUNT-flagged.

- SHOW (Remotion): B00 composer ask, B01 hesitant writer, B02 requirements board, B03 Bao's phase table, B04 B06 B08 B10 B12 B14 B16 code (verbatim excerpts at 5f09b7f, line highlights on the spoken phrase), B18 the four ideas, B21 verdict, B22 Your Turn, B23 outro.
- SHOW (real media): B05 B07 B09 B11 B13 B15 B17 results, each the next beat after its code beat (Bao's take, Bao's strips, recorded test output); B19 agent mistakes and open items; B20 roles and credits.

Teaching arc: FRAMEWORK ✓ (B01–B03: a clip is a list of keys; the brief and the phase table in frames) | WORKED EXAMPLE ✓ (B16–B17: Bao's observation, Bao's prediction, one change, the same-position strips, Bao's verdict) | FALSIFIABILITY ✓ (B13 hits before, on and after each boundary; B15 the four required mutations that make the read-back fail; B17 records where Claude's reading of r2 differs from the prediction) | SCAFFOLDED TASK ✓ (B22: one change through the phase table, a prediction, a strip) | BOOKENDS ✓ (B00 ask, B01 BLUF, B21 verdict, B22 handoff, B23 outro) | NO-SOURCE-NO-VERDICT ✓ (every verdict line maps to FACTCHECK.md).

## Checker

`./art godot-gamedev --check $REEL --game <dir>/godot`, where `<dir>` holds `git archive 5f09b7f godot` unpacked and never imported: **PASS**. 139 source files, 24 exclusions, 6 components, 7 exact excerpts, 7 code/result pairs. Teaching contract code-then-result-v1. Its scope is hashes, inventory, source lines and associations, not semantic or visual approval.

## Visual QC during the build

Each evidence beat was sampled at 15/50/85 % (`tools/qc_beats.py`) and each code beat at its last highlight; defects were fixed in the scene sources and re-rendered:

| Beat | Defect | Fix |
|---|---|---|
| B08 B10 B12 B14 B16 | code panel shows about 13 rows and does not scroll; highlighted lines below the panel | excerpts cut to `build_courier_visual.gd` 45–53 and 208–218, `player.gd` 209–218 and 233–240, `test_courier_clips.gd` 53–66; re-rendered; last highlight checked visible |
| B14 | after the first cut, line 66 still fell below the panel | excerpt started at line 56 (the bone, blend-shape and property branches); highlights on lines 57, 61 and 64 |
| B10 | third source note clipped at the panel's bottom | first note shortened to one line |
| code beats | source-note values wrapped and clipped | notes shortened |
| B07 B13 | the courier was too small in the full 4K take frame | B07 and B13 show a labelled 3× centre crop of the take (the camera follows the courier, so the centre is the courier) |
| B11 | frame 20 of the take still shows the random level-up offer before the fixture reorders it | the beat starts at frame 21; disclosed in `CAPTURE.md` |
| B13 | cooldown text shown twice | duplicate removed |
| B17 | r1/r2 comparison too small to see the outline | rebuilt from tight crops of Bao's two strips around the courier |
| B15 | "1 checks fail" on a mutation line | singular and plural from the count |
| B01 | the writer matches single words, so the two-word trigger "a movie" never fired: the page kept "An animation is a movie", the opposite of the narration; content filled 52 % of the safe area (Gate V MAJOR) | trigger "movie", replaced by "list of keys"; type 145 px, line spacing 1.9 (a 130 px try still filled 52 %) |
| B03 | the brief's phase table, shown as raw Markdown, ran out of its excerpt box into the footer | the excerpt is Bao's rules paragraph (brief line 194, first three sentences, verbatim); the table stays on the four cards |
| B06 | line 426 (`}`) cut in half at the panel's bottom | excerpt 415–425 |
| B07 B11 B13 | strip tiles shrank the 1:1 take crops to 180–250 px; the courier was hard to see | tiles at 340–380 px, two rows in B07 and B11, labelled with take frame numbers |
| B15 B17 B19 B20 | card text at 44–46 px, below the 48 px floor, with large empty areas | 50–56 px, line heights recomputed for the wraps |
| evidence beats | the last line of a card touched the card's bottom border | 20 px more padding at the bottom of every card |

## Final export

`art final … --height 2160 --fps 30` wrote `exports/landscape/claude-liam-walker-lanternfall-bao-x-animation-gamedev.mp4`: 3840 × 2160, 30 fps, 530.77 s, SHA-256 `3ce7f3f2579b8acad07f1a9155b1bbcc5cca062049ca56b2f7663595aa2b131b`, Gate V 48 frames 0 BLOCKER / 0 MAJOR. Two earlier exports were refused, the first for a missing Pillow and the second for B01's underfill. The frame-level pass on the master, the two minor items left as they are, and the sound are in `_qc/VISUAL-QC.md`.
