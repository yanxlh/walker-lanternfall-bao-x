# CHECKS-REPORT

## Beat classification

27 beats: 27 SHOW / 0 justified HOLD / 0 PUNT-flagged.

- SHOW (Remotion): B00 composer ask, B01 hesitant writer, B02 requirements board, B04 B06 B08 B10 B12 B14 B16 B18 B20 B22 code (verbatim excerpts, line highlights on the spoken phrase), B24 verdict, B25 Your Turn, B26 outro.
- SHOW (real media): B03 game sound only; B05 B07 B09 B11 B13 B15 B17 B19 B21 B23 results, each the next beat after its code beat.

Teaching arc: FRAMEWORK ✓ (B01–B02: the feedback contract and the requirements) | WORKED EXAMPLE ✓ (B08–B09: observation, prediction, one change, measured result, verdict) | FALSIFIABILITY ✓ (B09 records the missed prediction; B19 the mutations that make tests fail) | SCAFFOLDED TASK ✓ (B25: one bounded change, a prediction, a capture, a revert) | BOOKENDS ✓ (B00 ask, B01 BLUF, B24 verdict, B25 handoff, B26 outro) | NO-SOURCE-NO-VERDICT ✓ (every verdict line maps to FACTCHECK.md).

## Checker

`./art godot-gamedev --check $REEL --game $REPO/godot`: **PASS**. 94 source files, 4 exclusions, 8 components, 10 exact excerpts, 10 code/result pairs. Teaching contract code-then-result-v1. Its scope is hashes, inventory, source lines and associations, not semantic or visual approval.

## Visual QC during the build

Each evidence beat was sampled at 15/50/85 % and each code beat at its last highlight; defects were fixed in the scene sources and re-rendered:

| Beat | Defect | Fix |
|---|---|---|
| B07 and others | captions at 40–46 px (below the ~24 px-at-1080p floor) | caption floor 48 px at 4K; footer kept at 44 px and single-line |
| B05 | 2× follow crop lost the courier (camera clamped at the arena corner) | full frame plus a labelled ring at each logged hit |
| B09 | table and verdict box crossed the footer; "lit area" marked matched | re-laid out; status "more than predicted" |
| B13 | trail contact sheet too small to see embers | 4× crops of r0/r1 frames 12, 20, 39 located on the lamp |
| B15 | portrait crop cut the driver's on-screen label in half | crop above the label |
| B17 | paused-frame crops dominated by the PAUSED text | 7× crops of the frozen embers; pixel-identical check shown |
| B19 | mutation image crossed the footer; wrapped mono line overlapped | resized; shortened first line |
| B19, B21, B23 | two-line footers | shortened to one line (measured) |
| B06, B12, B16, B18 | code panel shows ~13 rows and does not scroll; highlighted lines 29 / 69 / 119 off screen | excerpts cut to lines 23–35, 17–29, 110–119, 57–69; last highlight verified visible |
| B04 and code beats | source-note values wrapped mid-word; fourth note clipped | notes shortened, three per beat |

The final export's frame QC: `_qc/VISUAL-QC.md` (manual 2 fps pass, sound and sync) and `_qc/REPORT.md` (the toolkit's Gate V: 54 frames, 0 BLOCKER, 0 MAJOR). One more defect was found in the first export (B21's last 0.4 s blank) and fixed before the final master.
