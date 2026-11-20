# SOURCES — what the film shows and where it comes from

## Engine capture

| Material | Path | Provenance |
|---|---|---|
| The take | `capture/take-dash.avi` (not committed; SHA-256 in `capture/takes.sha256`) | recorded by Bao on 20 November 2026 with `capture/capture-film-take.command`, isolated `git archive 5f09b7f godot` copy at 3840 × 2160, `capture/film_driver.gd` (CAPTURE.md) |
| The take's log | `capture/take-dash-log.jsonl`, dry run `capture/take-dash-dryrun.jsonl` | one row per movie frame, written by the driver |

## Repository material shown

| Material | Path | Who made it |
|---|---|---|
| The sheet | `godot/assets/art/pc_sheet.png` | Bao's own Assignment 2 sheet (ART-PC-01): FLUX.1-schnell `741f7c3`, run locally, Apache-2.0, licence checked 13 November 2026 (`godot/assets/art/ATTRIBUTION.md`) |
| Walk strip | `captures/walk/r1/` (frames, `frames.log`, `STRIP.md`) | fixture capture, recorded by Bao, 20 November 2026 |
| Dash strips | `captures/dash/r1/`, `captures/dash/r2/` | fixture captures, recorded by Bao, 20 November 2026 |
| Code panels | `godot/…` at `5f09b7f`, read with `git show` | Claude Code wrote the code; the phase table, the dash rules and revision r2 are Bao's (CHANGE-BRIEF.md, TUNING.md) |
| Recorded output | `evidence/courier_clips.json`, `evidence/dash_edges_{30,60,144}fps.json`, `evidence/assignment-7/mutations/mutations-required.json`, `evidence/assignment-7/godot3-names/probe.json` | test runs through `scripts/run-test.sh`; mutations in git worktrees |
| Bao's words | CHANGE-BRIEF.md (Bao's brief, answer 5), TUNING.md ("Keep 4/10/6.", "Keep. It is clearer."), TEST-REPORT.md ("Looked at it; no drift."; human checks) | Bao, in English as the records hold them |
| Roles | CONTRIBUTIONS-assignment-7.md, `prompts/assignment-7.md` | |

## Roles in this film

- **Bao:** recorded the take and the three 30 fps strips; wrote the brief and the seven answers; gave every verdict quoted; will watch the final export.
- **Claude Code (Claude Opus 5.5):** the film driver and its command, the beat sheet, the narration text, the evidence-beat compositor and every other tool in `tools/`, the edit and the checks.
- **Codex:** proposed the 4 / 10 / 6 phase table (shown as such in B09); no part of the film.

## Tools

- brutalist.art toolkit (`/Users/yxlh/brutalist.art`): `GodotDevWorkbench`, `GodotDesignBoard`, `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro` (Remotion); `generate_audio_kokoro.py`; `./art godot-gamedev --check`; `./art final`.
- Voice: Kokoro-82M (`kokoro-v1.0.onnx`, Apache-2.0), voice `am_onyx`, local. Liam, in for Bear; synthetic narration.
- Outro jingle: `logos/bear-brown/bear-brown-3.mp3` (stock @NikBearBrown jingle), picked by the slug seed.
- Godot 4.7.2 Movie Maker; ffmpeg; Pillow and numpy (`tools/compose.py`, `tools/build_media.py`).

No paid service or API was used. Nothing was uploaded or published by this build.
