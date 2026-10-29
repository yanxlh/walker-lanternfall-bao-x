# SOURCES

Film: `claude-liam-walker-lanternfall-bao-x-particles-gamedev` · game source revision **c3e1273** (`FILM-SOURCE-REVISION.txt`).

## Engine captures (this folder)

| File | SHA-256 | What |
|---|---|---|
| `capture/take-main-seed11.avi` | `1b26af9673854d92fa160a4a626873f85f6384ab0419c11c4360b95ef372d101` | main take, seed 11, 80 s of run time |
| `capture/take-props-seed11.avi` | `305f0cee685a04c217f60c03870ade08560f32918ab9425b74ccb5345ddfcdf2` | stall push and slide, seed 11 |
| `capture/study-cpu-vs-gpu.avi` | `cecb61f94adb28ddc528966c2741ed161bada308825ceae4d24b3c53d261cae8` | CPU sparks beside the editor-converted GPU copy |

Logs, identical dry runs and the driver are in `capture/` (CAPTURE.md). The runtime facts the film uses come from the take logs: hit positions, live counts and trail emission.

## Repository material shown (same revision)

- Fixture strips and comparisons: `captures/defeat_sparks/` (r0, r1, comparison-r0-r1, mutation-godot3-name), `captures/lantern_trail/comparison-20261029-135607/`, each with its own README/COMPARISON and hashes.
- Scripted play checks: `captures/play-checks/20261029-142138/` (PLAY-CHECKS.md, SHA256SUMS).
- Recorded test output: `evidence/assignment-6/final-precommit/`, `evidence/assignment-6/mutations/edges-no-displacement-guard.log`.
- Cost measurements: `evidence/assignment-6/cost/` (COST-REPORT.md and JSON).
- Bao's words and verdicts: TUNING.md, PLAY-CHECKS.md and TEST-REPORT.md (the stage explanation, quoted in B20's narration as the process stage deciding "how a particle changes").
- Requirements excerpt: CHANGE-BRIEF.md, "Tuning and acceptance".

Code panels are verbatim excerpts of `godot/` at c3e1273, with path and lines on screen and hashes in `gamedev-evidence.json`.

## Tools and voice

- Godot 4.7.2 Movie Maker for every capture; ffmpeg and Pillow for composition (`tools/compose.py`, from the Assignment 2 film).
- The brutalist.art toolkit at local vendor revision `71a36c7`: Remotion scenes `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDesignBoard`, `GodotDevWorkbench`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro`.
- Narration: Kokoro-82M, preset voice `am_onyx` ("Liam, in for Bear"), run locally; no voice cloning, no paid service.
- Outro jingle: the stock `logos/bear-brown/bear-brown-4.mp3`, picked by the slug seed (character sum 5295 mod 6).

No upstream documentation was quoted; Godot property names come from the project's own scenes and configuration tests.
