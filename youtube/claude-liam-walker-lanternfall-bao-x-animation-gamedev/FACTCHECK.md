# FACTCHECK — every claim the narration makes, and its source

Game source: `5f09b7f` (read with `git show`). Records: the repository at `9e2e958` or later (Bao's words in English, as TUNING.md, TEST-REPORT.md and CONTRIBUTIONS record them).

| Beat | Claim | Source |
|---|---|---|
| B00 | two clips, one sprite and one rig; one loops, one commits; one authority | CHANGE-BRIEF.md (Bao's brief, 18 Nov); `courier_clips.tres` (walk LOOP_LINEAR, dash LOOP_NONE); `player.gd:211–218` |
| B00 | pin 23 · read-back 86 · edges 51 at 30/60/144 | `evidence/assignment-7/r2/RUN.txt` |
| B02 | the walk uses cells 2 and 3 of Bao's own Assignment 2 sheet | `courier_clips.tres:425`; `godot/assets/art/ATTRIBUTION.md` |
| B02 | the dash is cut into head, arm, coat and legs from cell 2 | `build_courier_visual.gd` PARTS; read-back `rig-regions-cover-the-cell` |
| B03 | startup 4 frames, active 10 (55 px at 330 px/s), recovery 6, cooldown 60 | Bao's phase table, CHANGE-BRIEF.md lines 187–192; `tuning.gd:20–24` |
| B03 | the interrupt rules and predicted failures | Bao's brief (same section) |
| B04 | Body's texture is the sheet; offset (−16, −23); hframes 10 | `courier_visual.tscn:11–14` |
| B05 | ten 32-pixel cells | `pc_sheet.png` is 320 × 32; read-back `body-slices-the-sheet` |
| B05 | frames 1–3 of Bao's walk strip are the cast pose; then 3 × 4 frames, 2 × 4 frames | `captures/walk/r1/frames.log` |
| B05 | Bao: "Looked at it; no drift." | TEST-REPORT.md, HUMAN CHECKS (20 Nov) |
| B06 | the path names Body:frame; keys at 0 and 8/60 s; values 2 and 3; update 1 = discrete (excerpt lines 415–425) | `courier_clips.tres:418, 422, 424, 425` |
| B06 | a missing property fails silently | the assignment text; the read-back exists to catch it (`test_courier_clips.gd:64`) |
| B07 | the cell changes every four movie frames (eight ticks) in the take | `capture/take-dash-log.jsonl` |
| B07 | seam: last key 3, interval 8, tail 8 | `evidence/courier_clips.json` `walk-seam` |
| B07 | Bao reported no problem with the cycle seam | TEST-REPORT.md HUMAN CHECKS (20 Nov) |
| B08 | 4/10/6 at 60 per second; keys at 0, 4, 14, 20; transitions 2.0/1.0/0.5 | `build_courier_visual.gd:46–52, 58–60` |
| B09 | 4/60, 14/60, 20/60 s | arithmetic from the table; `courier_clips.tres` dash times (0.06666667, 0.23333333, 0.33333334) |
| B09 | Bao's 30 fps strip, frames 5/7/12/15 at dash frames 0/4/14/after | `captures/dash/r1/frames.log`, `STRIP.md` |
| B09 | the table started at 6/10/12; a Codex reading; Bao asked for 4/10/6 and kept it | CHANGE-BRIEF Revisions (r1); TUNING.md r0 → r1; prompts/assignment-7.md |
| B10 | `_show()` is the only code that plays or seeks; manual mode | `player.gd:211–218`; `courier_visual.tscn:66`; structure test `one-authority-in-source` |
| B11 | the card is put first by a fixture and picked with a real key 1 | `capture/film_driver.gd`; take log events |
| B11 | 0 s between clip time and gameplay tick at 30/60/144 | `evidence/dash_edges_{30,60,144}fps.json` `two-clocks-at-*` |
| B12 | a hit lands in every phase; startup cancels with no cooldown; recovery ends with the cooldown; active carries on | `player.gd:233–240` |
| B13 | three hits on startup frame 2, active frame 8, recovery frame 16; outcomes | `capture/take-dash-log.jsonl` (events, phase, cooldown, hp) |
| B13 | the edge tests check before/on/after each boundary at three rates | `evidence/dash_edges_*fps.json` `hit-before/on/after-*` |
| B14 | the bone, blend-shape and property branches of `track_problems` | `test_courier_clips.gd:56–66` |
| B15 | 86/86; the four required mutations and their results | `evidence/courier_clips.json`; `evidence/assignment-7/mutations/mutations-required.json` |
| B15 | `loop = true` loads as LOOP_LINEAR in 4.7.2 | `evidence/assignment-7/godot3-names/probe.json` |
| B16 | Bao's observation and prediction; the outer ring next to coat and legs | TUNING.md r1 → r2; `build_courier_visual.gd:200–219` |
| B17 | logs identical; outline on frames 5, 7, 12; Claude's reading; Bao's verdict "Keep. It is clearer." | TUNING.md r1 → r2; `captures/dash/r1`, `captures/dash/r2` |
| B18 | the four answers | as above, each with its line |
| B19 | the agent mistakes and the open items | TEST-REPORT.md "Agent mistakes caught while building", "Departures"; README Known limitations |
| B20 | roles; Codex proposed 4/10/6; the sheet's model and licence | CONTRIBUTIONS-assignment-7.md; prompts/assignment-7.md; ATTRIBUTION.md |
| B21 | the verdict lines | the sources above |

Corrections made while building: B01's on-screen line read "An animation is a movie" in the first renders, because the two-word trigger never fired; it now types "movie" and replaces it with "list of keys", as the narration says. The code panels of B08, B10, B12, B14 and B16 were shortened after the first renders showed the highlighted lines outside the visible panel, and B14 once more (to lines 56–66) when its last line still fell below the panel, and B06 to lines 415–425. The B17 comparison was rebuilt from tight crops of Bao's two strips because the first version was too small to read.
