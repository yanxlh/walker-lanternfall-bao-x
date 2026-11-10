# SOURCES

## Engine captures (this film, 9 November 2026)

Hashes are in `capture/takes.sha256`. The video files themselves are not committed.

| File | SHA-256 | What |
|---|---|---|
| `capture/take-main-seed11.avi` | `d4b5eaaa…3062` | main take as written (10464 frames, 7503 stale) |
| `capture/clean/take-main-seed11.mov` | `ad240a14…c4f` | main take with stale frames dropped (2961 frames), used in the film |
| `capture/take-props-seed11.avi` | `17c9db20…3354` | props take (421 frames, none stale) |
| `capture/study-cpu-vs-gpu.avi` | `d8903b3e…669f` | CPU burst beside the GPU study copy, seed 7280 (90 frames) |

The game source is the snapshot's `godot/`, tree `14e6b2ced0edbfc6d5db4686824af4903b9a5d7b` (FILM-SOURCE.md). The capture method is in CAPTURE.md.

## Repository material shown (from the snapshot)

- Fixture strips and comparisons: `captures/defeat_sparks/{r0,r1,r2,comparison-r0-r1,comparison-r1-r2,mutation-godot3-name}`, `captures/lantern_trail/comparison-20261029-135607`.
- Scripted play checks: `captures/play-checks/20261029-142138`.
- Recorded test output: `evidence/assignment-6/current-r2-validation/` (nine suites, 327 assertions, both mutations) and `evidence/assignment-6/mutations/edges-no-displacement-guard.log` (29 October).
- CPU cost: `evidence/assignment-6/current-r2-validation/cpu-r2.json`, and this film's `tests/cpu-r2-headless-20261109.json`.
- GPU cost: `evidence/assignment-6/cost/visual-profiler-a-r2-current/` (editor screenshots, captured by Codex; profiler rows and graph cropped); `evidence/assignment-6/current-r2-validation/gpu-r2.json`; this film's `tests/gpu-*.json` (windowed Mobile/Vulkan viewport-timer runs, r1 and r2 alternated); `evidence/assignment-6/cost/final-comparison/` (Compatibility zeros, celebration +0.91 ms).
- Human words: Bao's verdicts and checks as recorded in English in `TUNING.md` and `captures/play-checks/20261029-142138/PLAY-CHECKS.md`. Bao's process/draw explanation is in `TEST-REPORT.md`.
- Brief: `CHANGE-BRIEF.md`, the original 29 October intent and the current supplement.

## Tools and voice

- Godot 4.7.2 Movie Maker for every engine image.
- brutalist.art toolkit: GodotDevWorkbench, GodotDesignBoard, ClaudeComposerAsk, BrutalistHesitantWriter, ClaudeVerdictArtifact and ClaudeTitleOutro (Remotion), rendered locally.
- Narration: Liam (in for Bear), Kokoro-82M `am_onyx`, local and free. It is synthetic narration.
- Outro jingle: `logos/bear-brown/bear-brown-4.mp3` (stock @NikBearBrown jingle), seeded by the slug.
- No paid service, no upload.
