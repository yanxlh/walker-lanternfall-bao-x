# BUILD-PROMPT — how to rebuild this film

Prompt for an agent with the brutalist.art toolkit (`$ART`), this repository (`$REPO`) and Godot 4.7.2:

> Use the godot-gamedev skill with the walker modifier on `$REPO/godot` at source revision c3e1273. Keep everything inside `$REPO/youtube/claude-liam-walker-lanternfall-bao-x-particles-gamedev/` and never edit `godot/`. Rebuild the captures from CAPTURE.md, then run the steps below and stop on the first failure.

## Steps (from the reel folder `$REEL`)

1. **Captures**: `git archive c3e1273 godot` into a scratch folder. Set the window override to 3840 × 2160, copy `capture/capture_driver.gd`, `capture_main.tscn`, `study_capture.gd` and `study_capture.tscn` in, and import once. Then:
   - `godot --always-on-top --path . res://capture_main.tscn --write-movie $REEL/capture/take-main-seed11.avi --fixed-fps 30 -- main 11 80` (with `LF_LOG_TRACK=1 LF_CAPTURE_LOG=…/take-main-seed11-log.jsonl`);
   - the same for `props 11` → `take-props-seed11.avi`;
   - `godot --always-on-top --path . res://study_capture.tscn --write-movie $REEL/capture/study-cpu-vs-gpu.avi --fixed-fps 30 --quit-after 90`;
   - the headless dry runs (`--headless`, same arguments), whose logs must match the takes' logs.
2. `python3 tools/make_reel.py` → `beat_sheet.json`.
3. `python3 $ART/runtime/scripts/generate_audio_kokoro.py $REEL` (Kokoro `am_onyx`), then `python3 tools/make_reel.py` again so Remotion durations and highlight times follow the measured narration. The outro audio `mp3/beat-B26.wav` is `logos/bear-brown/bear-brown-4.mp3` padded with 1.0 s of silence.
4. `python3 tools/build_media.py` → `media/<BID>.mp4` for every evidence and game-sound beat.
5. `python3 $ART/runtime/scripts/remotion_scenes.py $REEL` → the Remotion beats (delete `media/<BID>.mp4` first after a change).
6. `python3 tools/level_audio.py`, `python3 tools/make_evidence.py`, `python3 tools/make_shotlist.py`, `python3 tools/make_script.py`.
7. `$ART/art godot-gamedev --check $REEL --game $REPO/godot`, which must PASS.
8. `$ART/art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape`.
9. Visual QC: sample frames (≥ 2 fps plus each beat at 15/50/85 %), read them, log defects in `_qc/REPORT.md`; listen to the game-sound beat and every narration transition.

## Rules this build kept

- Code panels are verbatim excerpts, labelled "Godot editor reconstruction", with path and lines on screen.
- Every code beat is followed by its visible result, and the result media are hashed in `gamedev-evidence.json`.
- No retiming of footage. Held frames and replays are labelled. The diagnostic rings in B05 are labelled and computed from the take's logged hit positions.
- Fixture and play-check material is labelled as such and is never presented as played gameplay.
- Outro: the locked `ClaudeTitleOutro`, exact title, @NikBearBrown, stock jingle only.
