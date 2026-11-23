# BUILD-PROMPT — how to rebuild the pitch film

## The prompt

Give this prompt to an agent that has the brutalist.art toolkit at `$ART`, this repository at `$REPO`, and Godot 4.7.2:

> Use the godot-gdd skill's structure to make a 2–4 minute pitch film for my final project from `$REPO/pitch/gdd/GDD-v0.3.md` and `$REPO/pitch/PROJECT-BRIEF.md`. The narration speaks as me in the first person and says that it is an AI voice. Use no instructor name, persona, handle or outro. Show what exists only as real captures of tag a7, with the revision named on screen. Label every picture of an unbuilt feature as constructed. Keep everything inside `$REPO/pitch/` and never edit `godot/`. Then run the steps below, stopping at the first failure.

Python is an environment with Pillow, numpy, soundfile, kokoro-onnx and faster-whisper; here that is `~/.venvs/general/bin/python` (3.13). python-docx is needed only for step 1.

## Steps (run from `$REPO/pitch`)

1. `python gdd/docx_to_md.py gdd/Lanternfall_Game_Design_Document.docx > gdd/GDD-v0.3.md`
   - The output must keep SHA-256 `50bb1789…` (the value is in `gdd-evidence.json`).
2. `capture/capture-pitch-take.command 21` runs the take. It:
   - unpacks `git archive a7 godot` into `capture/copy/` and sets the copy's window to 1920 × 1080;
   - adds `pitch_driver.gd` and `pitch_main.tscn`, then imports once;
   - records `capture/take-pitch-seed21.avi` with `--write-movie … --fixed-fps 30`;
   - repeats the run headless and compares the two logs (264 rows, identical);
   - writes `capture/takes.sha256`.

   Seeds 5 and 21 win with Sunflare; 3, 7, 11 and 14 lose (headless dry runs on 23 November 2026). Keep the window uncovered: frames written while it cannot draw are held and logged as stale.
3. `python tools/clean_take.py capture/take-pitch-seed21.avi` writes `capture/clean/take-pitch-seed21.mov`, with the stale frames dropped (6,127 frames).
4. `python3 tools/make_reel.py` writes `beat_sheet.json` and `gdd-evidence.json`.
5. Generate and level the narration:
   - `python $ART/runtime/scripts/generate_audio_kokoro.py .` (Kokoro `am_onyx`);
   - `python tools/level_audio.py`: loudness to -16 LUFS, plus B00's 0.6 s lead and the tails of B01 (1.5 s) and B13 (1.0 s);
   - `python tools/word_times.py`: word starts, and the pronunciation transcript;
   - `python3 tools/make_reel.py` again, so the reveal times follow the measured words.
6. `python tools/build_media.py` writes `media/B00.mp4` … `media/B13.mp4`.
7. `python3 tools/make_evidence.py`, then `$ART/art godot-gdd --check . --gdd gdd/GDD-v0.3.md`, which must PASS.
8. `PATH="<python env>/bin:$PATH" $ART/art final . --height 2160 --fps 30 --out exports/landscape` runs the gates and writes the master `exports/landscape/lanternfall-first-delivery-pitch.mp4`.
9. Visual QC: sample frames from every beat in the master and read them. Notes are in `CHECKS-REPORT.md`.

## Rules this build kept

- Gameplay is never retimed: four cuts at real speed, labelled.
- Scripted input is labelled on screen, and so is the shortcut in the driver (`game.start_run(seed)` instead of a random-seeded Enter).
- GDD excerpts are exact lines. Only outer table pipes and list dashes are dropped for display.
- Bao's own answers are marked as Bao's on screen ("Bao's answers, 23 November 2026").
- No Remotion composer, design board or title outro is used, because each one prints the instructor's handle.
