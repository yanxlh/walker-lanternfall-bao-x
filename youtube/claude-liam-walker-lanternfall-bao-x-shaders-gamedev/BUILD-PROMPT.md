# BUILD-PROMPT — how to rebuild this film

Prompt for an agent with the brutalist.art toolkit (`$ART`), this repository (`$REPO`) and Godot 4.7.2:

> Use the godot-gamedev skill with the walker modifier on `$REPO/godot` at source revision 4246f94. Keep everything inside `$REPO/youtube/claude-liam-walker-lanternfall-bao-x-shaders-gamedev/` and never edit `godot/`. Read every game file through git at that revision, never the working tree. Rebuild the captures from CAPTURE.md, then run the steps below and stop on the first failure.

## Steps (from the reel folder `$REEL`)

1. **Copies**: `git archive 4246f94 godot` three times into a scratch folder: a capture copy (window override 3840 × 2160; copy in `capture/capture_driver.gd`, `capture_main.tscn`, `shader_pair_fixture.gd`, `shader_pair_fixture.tscn`; `--import` once), a test copy (`--import` once) and an unimported check copy.
2. **Take**: in the capture copy, `LF_LOG_TRACK=1 LF_CAPTURE_LOG=$REEL/capture/take-hurt-seed5-log.jsonl godot --always-on-top --path . res://capture_main.tscn --write-movie $REEL/capture/take-hurt-seed5.avi --fixed-fps 30 -- hurt 5`, then the same with `--headless` and no `--write-movie` into `take-hurt-seed5-dryrun.jsonl`; the two logs must be identical and list `"stale":[]`.
3. **Fixture**: `godot --always-on-top --path . res://shader_pair_fixture.tscn -- $REEL/capture/shader-pair <mode>` for `pair`, `control-generated`, `control-bao`; then `python3 tools/pair_diff.py`.
4. **Tests**: `capture/run_tests.sh` (expects the test copy beside it as `tests-copy/` and the revision in `REV`) → `capture/test-run-film-build-raw.txt` and `capture/test-run/`.
5. `python3 tools/make_reel.py` → `beat_sheet.json`.
6. `python3 $ART/runtime/scripts/generate_audio_kokoro.py $REEL` (Kokoro `am_onyx`), then `python3 tools/make_reel.py` again so Remotion durations and highlight times follow the measured narration. The outro audio `mp3/beat-B30.wav` is `logos/bear-brown/bear-brown-5.mp3` padded with 1.0 s of silence.
7. `python3 tools/build_media.py` → `media/<BID>.mp4` for every evidence and game-sound beat (B03, B06, B08, B10, B12, B14, B16, B18, B20, B22, B25, B26, B27). One beat at a time if memory is tight.
8. `python3 $ART/runtime/scripts/remotion_scenes.py $REEL --only <BID>` for every Remotion beat (B00, B01, B02, B04, B05, B07, B09, B11, B13, B15, B17, B19, B21, B23, B24, B28, B29, B30); delete `media/<BID>.mp4` first to re-render one. In this build one 22-second beat took 57 minutes at the script's fixed concurrency of 1, so B05 and B00 were rendered in the reel and the other sixteen by `tools/remotion_workers.sh <worker-root> <BIDs…>` in four queues: each beat runs the same `remotion_scenes.py --only` in its own worker folder holding a copy of `beat_sheet.json` (never two writers on one reel), its `media/<BID>.mp4` is moved into the reel, and `python3 tools/merge_remotion_stamps.py <worker-root>` copies the provenance stamps back. Renders crawled and hit Remotion's 30 s frame timeout whenever the Mac's display slept (the machine was on battery overnight); running a render under `caffeinate -d -i` brought a beat back to one or two minutes.
9. `python3 tools/level_audio.py`, `python3 tools/make_evidence.py`, `python3 tools/make_shotlist.py`, `python3 tools/make_script.py`.
10. `$ART/art godot-gamedev --check $REEL --game <check copy>/godot`, which must PASS.
11. `$ART/art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape`.
12. Visual QC: sample every beat (≥ 3 frames each plus the transitions), read them, log defects in `_qc/REPORT.md`; check loudness of every narration beat, the game-sound beat and the outro.

## Deviation from the template: the evidence-beat compositor

The Assignment 6 film's `tools/compose.py` built each evidence beat as one ffmpeg `filter_complex` with an input per layer. On this machine during the build (16 GB, heavy swapping from other applications) one 25-second beat took 8 to 22 minutes. `tools/compose.py` was rewritten for this film: the same layer spec, composited frame by frame in Pillow (still layers flattened by timing, static frames reused) and piped to one ffmpeg encoder (libx264 veryfast, CRF 14, small lookahead); each video layer is decoded by its own ffmpeg process at its display size, and a game-sound beat muxes the take's own audio for the same span. Only evidence/media beats use it. Remotion beats are rendered by `runtime/scripts/remotion_scenes.py` and the master by `./art final`, as the skill requires.

## Rules this build kept

- Code panels are verbatim excerpts read from git at 4246f94, labelled "Godot editor reconstruction", with path and lines on screen; the composed line pairs in B22 are read the same way.
- Every code beat is followed by its visible result; the result media are hashed in `gamedev-evidence.json`.
- No retiming of footage. Held frames and replays are labelled. Scripted input, controlled-value fixtures, the agent-made shader-pair fixture and the agent-run green study are labelled as such and never presented as play.
- Bao's words are quoted only where TEST-REPORT.md, PREDICTION.md, LANGUAGE-NOTES.md or SOURCES.md record them.
- Outro: the locked `ClaudeTitleOutro`, exact title, @NikBearBrown, stock jingle only.
