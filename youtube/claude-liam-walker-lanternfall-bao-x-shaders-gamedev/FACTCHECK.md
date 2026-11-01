# FACTCHECK

Every factual claim in the narration and on screen, with where it was checked. Game source revision: **4246f94** (`FILM-SOURCE-REVISION.txt`). "Take" means the real 4K engine capture `capture/take-hurt-seed5.avi` (CAPTURE.md).

## Source revision and the working tree

- The film started at 61c9cbf. At 16:54 on 30 October an uncommitted edit appeared in the working tree's `godot/shaders/cobblestone_surface.gdshader` (line 22 reading `NORMAL`), together with an untracked `evidence/test_materials.json` written at 20:54:05 UTC, before this film's own test run began (16:55 EDT, in a scratch copy). Neither was this film's work, and neither was touched.
- Bao kept the edit and committed it (`0b91838`); `7d38e92` and `4246f94` are document commits (a brief revision, Bao's completed LANGUAGE-NOTES.md). The film moved to **4246f94** for every excerpt, hash, isolated copy and `--check`.
- Every code panel and ledger hash is read with `git show 4246f94:godot/<path>` (`tools/src.py`); `--check` runs against an unimported `git archive 4246f94 godot`. `git diff 4246f94 3c45f06 -- godot` (HEAD when the film was built) is empty.
- `git diff 61c9cbf 4246f94 -- godot` touches only `shaders/cobblestone_surface.gdshader`; the hurt take was nevertheless recorded from a 4246f94 copy (an earlier attempt from a 61c9cbf copy was stopped and deleted, CAPTURE.md).

## Bao's words

Every quotation of Bao in the film is in English, as the repository records it at `b295096` (TEST-REPORT.md and `evidence/assignment-5/bao-shader-edit/PREDICTION.md`, translated in `8490cfe`; his look at the sweep recorded in `f9f0fd8`): his prediction and observation in B14, his look at the `normal_strength` row in B18, his playtest report in B27, and his LANGUAGE-NOTES.md answers. The film shows no Chinese originals and no translation label. The quotes are read from those files by `tools/build_media.py`, not retyped.

## Corrections made while building the film

| Where | First draft | Why it was wrong | Now |
|---|---|---|---|
| B22 fixture measurement | left plane vs right plane of one render | the two positions sample the texture on different pixel grids; control renders with the *same* material on both planes differed as much (mean 4.4–4.6) | the same plane compared across the `control-generated` and `control-bao` renders; the narration's numbers come from that |
| capture driver | per-frame row recorded at the first physics step | in the dry run the row's `hurt_amount` lagged the drawn frame by one | row recorded in `_process` at priority 100000, after the tint driver; row 1335 and AVI frame 1335 both turn yellow |
| capture driver | resume sent every frame while paused | in one dry run (seed 9) the repeated presses never resumed | resume sent once |
| B04 narration | "the coat at one fifty and a half" | names one channel of three | "one fifty point five, one fifty-six point five, forty-four point five" |
| B06, B14, B16, B20, B22, B25–B27 | captions at 34–42 px, footers on two lines | below the 48 px floor at 4K | 44–48 px, one-line footers |

## Visual QC during the build (frames read, defect, fix)

| Beat | Defect seen in sampled frames | Fix |
|---|---|---|
| B01 | the line "one line, one number, one hint" ran off both edges at 170 px | font 136 px; re-rendered and checked |
| B06 | table at 38 px mono; label "white · 0.5" collided with the lamp column | 44 px mono table, separate label column, larger crops |
| B10, B18 | builder crashed on the capture JSON keys; then footers wrapped to a second line | read `floor_mean_rgb` / `standin_mean_rgb`; footers shortened |
| B11, B15, B21 | the third source note was clipped at the panel bottom | notes shortened; the three beats re-rendered and checked |
| B14 | Bao's observation wrapped badly; the agent-run caption overflowed; footer on two lines | quote set as one wrapped serif paragraph; caption reworded; footer shortened |
| B16, B20 | footer on two lines; band labels in orange on grey were low-contrast | footers shortened; white / near-black labels |
| B22 | the tilted-pose caption wrapped into the line below | caption split onto two separate lines |
| B27 | Bao's playtest quote rendered as empty glyph boxes | quote set separately in the serif face |
| B18, B26 (after handoff) | B18 ended on "Bao's look … is still pending" and B26 listed it as uncertain; Bao has since given his look | B18's last sentence now gives his look and the screen quotes it; B26 names the fixture residual instead; both narrations regenerated with Kokoro and the beats rebuilt to the new measured length |
| B14, B27 (after handoff) | Bao's quotes shown in Chinese with an English line beneath | English only, as recorded at b295096 |
| B04, B13, B21 | Remotion's 30 s per-frame timeout failed renders while the Mac's display slept | renders retried one at a time with the display kept awake (`caffeinate -d`) |

## Repository evidence discrepancy found while building

The mutation JSON first stored as `semicolon_60fps.json` held the **rename** mutation's results (3 failures, `hurt_strength` in the uniform list), not the semicolon run's; the repository has since renamed it `rename_60fps.json`. The semicolon log (`evidence/assignment-5/mutations/semicolon_60fps.log`) shows `SHADER ERROR: Expected a ';'.` and **4** failures, matching TEST-REPORT.md. The film cites the three mutation logs only.

## Claims by beat

| Beat | Claim | Checked against |
|---|---|---|
| B00 | lamp-headed courier, fog-bound night market, three minutes | CONCEPT.md "In two sentences" |
| B00 | 28 + 127 new checks; 332 earlier unchanged; revision 4246f94 | `capture/test-run-film-build-raw.txt` |
| B02 | yellow after an accepted hit, fading over 48 ticks; Floor and StandIn of the inherited A3 room | CHANGE-BRIEF.md line 21; `features/tuning.gd:14`; `a5/material_room.tscn` |
| B04 | colour line and equation; lamp 0.5 → (248.5, 219.5, 37.5); coat 0.5 → (150.5, 156.5, 44.5); red phase keeps more red; 2.0 not clamped | CHANGE-BRIEF.md lines 34–40, Hand calculations table, short answer 7 |
| B05 | canvas_item (1), hurt_amount with hint_range (4), fragment (7), mix line (8); hint shapes the Inspector only | `shaders/hurt_tint.gdshader`; LANGUAGE-NOTES Q4/Q5 (Bao) |
| B06 | white 0.5 lamp (249, 220, 37), coat (151, 157, 44); red 0.5 lamp (249, 169, 17), coat (151, 141, 20); 1.0 → (255, 255, 0) both phases; 2.0 read back 2.0 | `captures/hurt-tint/20261030-125036/captures.json`, `20261030-125259-red/captures.json`; TEST-REPORT.md Controlled values |
| B07 | refresh every frame (22); iframes / 48 clamped (26); 0 outside PLAYING/PAUSED/LEVELUP (25, 27); set_shader_parameter (30); own material (15–17); accepted hit sets 48 | `effects/hurt_tint_presentation.gd`; `features/player/player.gd:98` |
| B08 | yellow on the hit frame; pause holds 23/48 (0.4792) for 45 frames; touching monster at 1661–1666 with hp unchanged; 0 after 48 ticks, 0.8 s, 24 frames | take log rows 1500–1569, 1653–1677 |
| B09 | line 10 instances the A3 room; 8 × 8 PlaneMesh; materials on lines 14 and 18; A3 file untouched | `a5/material_room.tscn` 3–18; brief revision "the floor mesh in the A5 scene" (Bao's decision) |
| B10 | 2 × 2 repeats of square stones at uv_scale 2; fixed pose | brief revision 10/30; `captures/a5-materials/20261030-170452-pair/CAPTURES.md` |
| B11 | shader (10), maps (11–13), tint, uv 2, roughness 0.55–0.95; stand-in cooler, uv 1, 0.2–0.55, normal 0.5 | both `.tres` files; brief answer 6 |
| B12 | uv_scale 2 → 4 on the floor in memory; floor max difference 72; stand-in 0 | `20261030-170456-one-material/CAPTURES.md` |
| B13 | lines 18, 19, 21, 22; line 22 scales depth by mix(0.5, 1.0, abs(normalize(NORMAL).z)) | `shaders/cobblestone_surface.gdshader` at 4246f94; `0b91838`; brief revision of line 22 |
| B14 | Bao's prediction first; edit of line 19 by hand; every pixel of both rectangles changed; means; his observation; Codex green run broke the rule | `evidence/assignment-5/bao-shader-edit/PREDICTION.md`; TEST-REPORT.md "One shader, two materials"; `20261030-single-line-study/EXPERIMENT.json` |
| B15 | line 3 source_color, line 4 hint_normal, line 5 no colour hint, line 1 spatial | `shaders/cobblestone_surface.gdshader` 1–5; LANGUAGE-NOTES Q4 |
| B16 | curl 0.2236 / 1.7764 and the DX mirror; normal_strength 0 vs 1 crops | `evidence/assignment-5/textures/curl-calibration.log`; `20261030-170453-sweep/` |
| B17 | group_uniforms 7 and 11; hint_range sets slider limits; uv_scale 0.25–4 | lines 7–15 |
| B18 | five uniforms × low / material / high; stand-in (31.42, 40.97, 74.83) throughout; Bao's look at the new normal_strength row (zero flatter, relief off; one more three-dimensional edges and joints; two stronger relief, deeper joints, an exaggerated bump), quoted on screen verbatim | `20261030-170453-sweep/CAPTURES.md`; TEST-REPORT.md at f9f0fd8 (recorded) and b295096 (English, as quoted) |
| B19 | one 3 × 1 grey image, two samplers (5, 6), use_color (7), ALBEDO (11/13), unshaded | `shaders/hint_experiment.gdshader`; `a5/hint_experiment/*.tres` |
| B20 | Forward+/Mobile prediction 137/188/225; Compatibility prediction and measurement 64/128/192 | CHANGE-BRIEF.md hint table; `20261030-131056-hint/CAPTURES.md` |
| B21 | line 1 automatic conversion; 3 spatial; 7 source_color; 19 hint_roughness_normal, no source_color; 35 ALBEDO | `shaders/standard_generated.gdshader`; LANGUAGE-NOTES generated-shader table and Q6 (Bao); conversion by Bao, `43dfe20` |
| B22 | face-on 87–93 % of pixels within 2 levels, mean 0.6–1.0; tilted 50°: mean 2.4–2.8 | `capture/shader-pair/diff.json`; the tilted gap is *consistent with* line 22, not isolated |
| B23 | the four answers at lines; Bao's answer 8 verbatim | LANGUAGE-NOTES.md at 4246f94 |
| B24 | one wraith 20 px away (155), Enter (157), real hit (159), W (162); sampler at priority 100000; test never writes hurt_amount except a second material | `tests/test_hurt_tint.gd` 2–5, 13–38, 155–166 |
| B25 | 28/28 at 30, 60, 144; first values 0.9792 / 1 / 1; zero tick 50 / 49 / 49; game time 0.7958 / 0.8000 / 0.7992 s; 127/127; 332/0; mutations 4/28, 3/28, 1/127; headless limits | `capture/test-run/*.json`, `capture/test-run-film-build-raw.txt`; mutation logs; TEST-REPORT.md "What a headless run cannot show" |
| B26 | agent mistakes (six rows) and the Codex edit; uncertain items (Forward+ hint difference predicted, not measured; the fixture's face-on residual unexplained; the tinted F3 arc); next step | TEST-REPORT.md A5 tables; README.md Known limitations; `capture/shader-pair/diff.json` |
| B27 | roles, texture credit, revision; Bao's playtest report quoted in English | SOURCES.md Assignment 5; `godot/assets/textures/cobblestone_floor_08/ATTRIBUTION.md`; TEST-REPORT.md at b295096 |
| B28 | verdict lines | the beats above |
| B29 | test_materials expects the stand-in's uv_scale 1.0 | `tests/test_materials.gd` lines 46–47 and 215–218 |

## What the film does not claim

That anyone has watched this film; that the tint or the stones look good in general (Bao's reported playtest and his observation of his edit are the only human judgments shown); that `source_color` makes no difference outside Compatibility (predicted, not measured); that line 22 alone causes the fixture's tilted difference.
