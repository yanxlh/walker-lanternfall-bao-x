# BUILD-PROMPT — how to rebuild this film

Prompt for an agent with the brutalist.art toolkit (`$ART`), this repository (`$REPO`) and Godot 4.7.2:

> Use the godot-gamedev skill with the walker modifier on the game whose `godot/` tree id is in `FILM-SOURCE-REVISION.txt` (see FILM-SOURCE.md). Keep everything inside `$REPO/youtube/claude-liam-walker-lanternfall-bao-x-particles-gamedev-r3/` and never edit `godot/`. Rebuild the captures from CAPTURE.md, then run the steps below and stop on the first failure.

## Steps (from the reel folder `$REEL`)

1. Point `FILM-SOURCE-PATH.txt` at a checkout whose `git rev-parse HEAD:godot` equals `FILM-SOURCE-REVISION.txt`.
2. **Captures** (CAPTURE.md): copy that `godot/` to a scratch folder, set the window override to 3840 × 2160, add the four files in `capture/`, import once, and run the main, props and study takes and the headless dry runs. If a take logs stale frames, run `tools/clean_take.py`; the clean video's frame n is dry-run frame n.
3. `python3 tools/make_reel.py` → `beat_sheet.json`.
4. `python3 $ART/runtime/scripts/generate_audio_kokoro.py $REEL` (Kokoro `am_onyx`), then `python3 tools/make_reel.py` again, so Remotion durations and highlight times follow the measured narration. The outro audio `mp3/beat-B31.wav` is `logos/bear-brown/bear-brown-4.mp3` padded with 1.0 s of silence.
5. `python3 tools/build_media.py` → `media/<BID>.mp4` for every evidence and game-sound beat.
6. `python3 $ART/runtime/scripts/remotion_scenes.py $REEL` → the Remotion beats. After a change, delete `media/<BID>.mp4` first.
7. `python3 tools/level_audio.py`, then `make_evidence.py`, `make_shotlist.py` and `make_script.py` (all in `tools/`).
8. `$ART/art godot-gamedev --check $REEL --game <checkout>/godot`, which must PASS.
9. `$ART/art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape`.
10. Visual QC: sample frames, read them, and log defects in `_qc/REPORT.md`. Listen to the game-sound beat and every narration transition.

## Rules this build kept

- Code panels are verbatim excerpts of at most 14 lines, labelled "Godot editor reconstruction", with path and lines on screen.
- Every code beat is followed by its visible result; the result media are hashed in `gamedev-evidence.json`.
- No retiming of footage. Held frames and replays are labelled, and stale capture frames are dropped, not retimed.
- Fixture, profiler-screenshot and play-check material is labelled as such and never presented as played gameplay.
- Bao's words appear in English, as recorded in TUNING.md and PLAY-CHECKS.md.
- Outro: the locked `ClaudeTitleOutro`, exact title, @NikBearBrown, stock jingle only.
