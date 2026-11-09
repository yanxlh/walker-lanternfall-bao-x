# Revision 3 validation — 9 November 2026

Run from a fresh import of branch a6-r3 (documents differ from a6-r2; `godot/` and `scripts/` are identical), on Apple M4, macOS 26.6.2, `godot-version.txt`. Commands and exit codes: `exit-codes.txt`. Engine import: `import.log`.

- Suite logs: `test_*_60fps.log`, `test_audio_realtime.log`. Results: one JSON per suite, copied from `evidence/*.json`, whose committed versions were restored after the run.
- Headless price: `cost_effects_60fps.log`, `cost_effects_headless.json` (5 trials × 300 frames, 30 warm-up frames).

Totals: logic 32, gameplay 65, audio 25 (realtime), A configuration 39, extra configuration 79, state 34, edges 18, shader-study configuration 21. That is 313 assertions with zero failures, and no SCRIPT ERROR or SHADER ERROR. The gameplay, audio, state and edge logs end with the engine's "resources still in use at exit" diagnostics, as in earlier runs.
