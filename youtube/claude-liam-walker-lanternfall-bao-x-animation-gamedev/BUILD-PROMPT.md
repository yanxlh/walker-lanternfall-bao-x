# BUILD-PROMPT — how to rebuild this film

Prompt for an agent with the brutalist.art toolkit (`$ART`), this repository (`$REPO`) and Godot 4.7.2:

> Use the godot-gamedev skill with the walker modifier on `$REPO/godot` at source revision 5f09b7f. Keep everything inside `$REPO/youtube/claude-liam-walker-lanternfall-bao-x-animation-gamedev/` and never edit `godot/`. Read every game file through git at that revision, never the working tree. The student records the take; then run the steps below and stop on the first failure.

Python: an environment with Pillow, numpy and kokoro-onnx (here `~/.venvs/general/bin/python`, Python 3.13).

## Steps (from the reel folder `$REEL`)

1. **Take** (the student runs it): `capture/capture-film-take.command`. It unpacks `git archive 5f09b7f godot` into `capture/copy/`, sets that copy's window to 3840 × 2160, adds `capture/film_driver.gd` and `capture/film_main.tscn`, imports once, records `capture/take-dash.avi` with `--write-movie … --fixed-fps 30`, repeats the script headless into `capture/take-dash-dryrun.jsonl`, compares the two logs, and writes `capture/takes.sha256`.
2. `python tools/make_reel.py` → `beat_sheet.json`.
3. `python $ART/runtime/scripts/generate_audio_kokoro.py $REEL` (Kokoro `am_onyx`), then `python tools/make_reel.py` again so Remotion durations and highlight times follow the measured narration. The outro audio `mp3/beat-B23.wav` is `$ART/logos/bear-brown/bear-brown-3.mp3` (slug char-sum 5288 mod 6 = 2) padded with 1.0 s of silence.
4. `caffeinate -d -i python $ART/runtime/scripts/remotion_scenes.py $REEL --only <BID>` for every Remotion beat (B00–B04, B06, B08, B10, B12, B14, B16, B18, B21–B23). Delete `media/<BID>.mp4` first to re-render one.
5. `python tools/build_media.py` → `media/<BID>.mp4` for the evidence beats (B05, B07, B09, B11, B13, B15, B17, B19, B20).
6. `python tools/level_audio.py`, `python tools/make_evidence.py`, `python tools/make_shotlist.py`, `python tools/make_script.py`.
7. `$ART/art godot-gamedev --check $REEL --game <unimported git archive of 5f09b7f>/godot`, which must PASS.
8. `PATH="<that environment>/bin:$PATH" $ART/art final $REEL --height 2160 --fps 30 --out $REEL/exports/landscape`. `art final` runs `python3` from `PATH`, and its final frame check needs Pillow and numpy. If they are missing, the check refuses the candidate and deletes it after the full encode.
9. Visual QC: sample every beat (three or more frames each, and the transitions), read them, and log defects in `_qc/REPORT.md`. Check the loudness of every narration beat and the outro.

## Rules this build kept

- Code panels are verbatim excerpts read from git at 5f09b7f, labelled "Godot editor reconstruction", with the path and lines on screen.
- Every code beat is followed by its visible result; the result media are hashed in `gamedev-evidence.json`.
- No retiming of footage. Replays are labelled. Scripted input and fixtures (no spawns, the card offer, the placed wraith) are labelled on screen and never presented as unscripted play. Bao's strips are labelled as fixture captures recorded by Bao.
- Bao's words are quoted only where TUNING.md, TEST-REPORT.md, CHANGE-BRIEF.md or CONTRIBUTIONS-assignment-7.md record them.
- Outro: the locked `ClaudeTitleOutro`, exact title, @NikBearBrown, stock jingle only.
