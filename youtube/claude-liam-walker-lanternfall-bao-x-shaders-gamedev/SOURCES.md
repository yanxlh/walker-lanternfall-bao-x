# SOURCES

Film: `claude-liam-walker-lanternfall-bao-x-shaders-gamedev` · game source revision **4246f94** (`FILM-SOURCE-REVISION.txt`). Every code panel and every `godot/` hash is read with `git show 4246f94:godot/<path>`, not from the working tree. The repository records quoted (TEST-REPORT.md, the material recaptures, `evidence/assignment-5/after-line22/`) were read at `3c45f06`, and Bao's quoted words at `b295096` (English); `git diff 4246f94 b295096 -- godot` is empty.

## Made for this film (this folder)

| File | What |
|---|---|
| `capture/take-hurt-seed5.avi` | real 4K Movie Maker take of the isolated 4246f94 copy, scripted input, seed 5 (SHA-256 in `capture/takes.sha256`) |
| `capture/take-hurt-seed5-log.jsonl`, `-dryrun.jsonl` | the take's event and per-frame log; the identical headless dry run |
| `capture/shader-pair/*.png`, `diff.json` | the agent-made shader-pair fixture renders and their measured differences |
| `capture/test-run-film-build-raw.txt`, `capture/test-run/*.json` | every suite re-run on an isolated 4246f94 copy for this film |

CAPTURE.md has the commands, the driver and the fixture.

## Repository material shown

| File | SHA-256 (first 16) | Committed in |
|---|---|---|
| `captures/hurt-tint/20261030-125036/hurt-amount-0.0.png` | `1216a036a8a23aca…` | ab48cab |
| `captures/hurt-tint/20261030-125036/hurt-amount-0.5.png` | `9c8e0d696598a1b5…` | ab48cab |
| `captures/hurt-tint/20261030-125036/hurt-amount-1.0.png` | `a0e570d450d642d8…` | ab48cab |
| `captures/hurt-tint/20261030-125036/hurt-amount-2.0.png` | `a0e570d450d642d8…` (byte-identical to 1.0) | ab48cab |
| `captures/hurt-tint/20261030-125259-red/hurt-amount-0.0.png` | `1069374526fe406d…` | ab718a6 |
| `captures/hurt-tint/20261030-125259-red/hurt-amount-0.5.png` | `0efdbb8fe476efe0…` | ab718a6 |
| `captures/hurt-tint/20261030-125259-red/hurt-amount-1.0.png` | `28f8636f5efef40c…` | ab718a6 |
| `captures/a5-materials/20261030-170452-pair/pair.png` (at 4246f94) | `c922cb9c9141e50c…` | eea7798 |
| `captures/a5-materials/20261030-170456-one-material/one-material-baseline.png` | `c922cb9c9141e50c…` (same as pair) | eea7798 |
| `captures/a5-materials/20261030-170456-one-material/one-material-floor-uv_scale-4.0.png` | `9f6607eb7fbe5a8d…` | eea7798 |
| `captures/a5-materials/20261030-170453-sweep/` (15 PNGs, at 4246f94) | see its `captures.json`; material-value files equal the pair | eea7798 |
| `captures/a5-materials/20261030-131249-compare-shader-baseline/compare-shader-baseline.png` (d01df00) | `f9146ae9b36eaad1…` | df44cdd |
| `captures/a5-materials/20261030-163723-compare-shader-bao-edit/compare-shader-bao-edit.png` (e5c0272, Bao's edit) | `0a76504a4c7b80bd…` | 99bb6f6 |
| `captures/a5-materials/20261030-single-line-study/edited/compare-shader-edited.png` (agent run) | `a9d730d01bf0bcde…` | 6729208 |
| `captures/a5-materials/20261030-131056-hint/hint-experiment.png` (d01df00) | `3767bfddb3cf1642…` | df44cdd |

Other records quoted or drawn on: CHANGE-BRIEF.md (state line 21, colour line 34–40, Hand calculations table, short answers 6 and 7, hint prediction table) at 4246f94; LANGUAGE-NOTES.md at 4246f94 (Bao's answers Q2, Q3, Q4, Q6, Q8); `evidence/assignment-5/bao-shader-edit/PREDICTION.md` (Bao's prediction) and TEST-REPORT.md Assignment 5 (controlled values, the agent-mistakes table, what a headless run cannot show), and Bao's quoted words — prediction, observation of his edit, look at the `normal_strength` row, playtest report — in English as recorded at `b295096`; `evidence/assignment-5/mutations/*.log`; `evidence/assignment-5/textures/curl-calibration.log`; `godot/assets/textures/cobblestone_floor_08/ATTRIBUTION.md` and the four map PNGs; SOURCES.md and README.md (Assignment 5 sections).

## Human and AI contributions (repository SOURCES.md, Assignment 5)

- **Bao:** hand-wrote `hurt_tint.gdshader` (e0b47b4), `cobblestone_surface.gdshader` (a8c804b) and its line-22 edit (0b91838), `hint_experiment.gdshader` (5a7903a); the brief's state, design, predictions and short answers; the three mutations; the approval of each agent plan; the inherited A5 scene, the PlaneMesh floor, keeping the A3 ambient source; the editor conversion (43dfe20); LANGUAGE-NOTES.md; every HUMAN CHECK. An earlier `hurt_tint.gdshader` written by Codex lived in a separate working copy; Bao reports writing the yellow version himself.
- **Claude Code (Claude Opus 5.5):** CLAUDE.md draft and review, the hurt-tint driver and `test_hurt_tint.gd`, the material audit (`godot/MATERIALS.md`, `test_materials.gd`), the import-settings script, the material and scene builder, the probes, both capture tools, the record files. Prompts and transcripts: `evidence/assignment-5/agent/`.
- **Codex:** set up the scratch conversion scene's PlaneMesh and StandardMaterial3D; the green single-line study that edited and restored `godot/shaders/cobblestone_surface.gdshader`.
- **This film (Claude Code):** the capture driver, the shader-pair fixture, the test re-run, the narration script, the composition and the edit. No human has reviewed the film yet.

## Texture

Cobblestone Floor 08 by Rob Tuytel, Poly Haven, https://polyhaven.com/a/cobblestone_floor_08, CC0 (https://polyhaven.com/license; licence checked 30 October 2026 by Bao). File bytes and SHA-256 in `godot/assets/textures/cobblestone_floor_08/ATTRIBUTION.md`.

## Tools and voice

- Godot 4.7.2 Movie Maker and viewport capture for the take and the fixture; ffmpeg, Pillow and NumPy for measurement and composition (`tools/compose.py`, a Pillow frame compositor written for this film from the Assignment 6 film's layer format).
- The brutalist.art toolkit at local vendor revision `71a36c7`: Remotion scenes `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDesignBoard`, `GodotDevWorkbench`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro`, rendered through `runtime/scripts/remotion_scenes.py`; the master through `./art final`.
- Narration: Kokoro-82M, preset voice `am_onyx` ("Liam, in for Bear"), run locally; no voice cloning, no paid service.
- Outro jingle: the stock `logos/bear-brown/bear-brown-5.mp3`, picked by the slug seed (character sum 5074 mod 6 = 4), padded with 1.0 s of silence.

No upstream Godot documentation was quoted; hint meanings are Bao's own (LANGUAGE-NOTES.md) and the brief's.
