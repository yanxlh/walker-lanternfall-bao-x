# SOURCES — Assignment 8 pitch film

## What I used

| Item | What it is | Licence / rights |
|---|---|---|
| My game, tag `a7` (`godot/` = `5f09b7f`) | the playable build shown in B00, B01, B06, B09 | my own work; asset credits in the repository's root `SOURCES.md` and `ASSET-LOG.md` |
| My A4 GDD v0.3 (17 October 2026) | `gdd/Lanternfall_Game_Design_Document.docx` and `.pdf`, converted to `gdd/GDD-v0.3.md` | my own design document, submitted for Assignment 4. The .docx was produced by a Python script, `build_lanternfall_gdd.py`, kept outside this repository |
| Earlier captures in this repository | A3 gate room (`evidence/a3/`), A5 material room (`captures/a5-materials/`), A6 sparks (`captures/defeat_sparks/`), A7 dash strip (`captures/dash/r1/`) | my own project's captures |
| A6 cost report | `evidence/assignment-6/cost/COST-REPORT.md`, copied to `evidence/a6-COST-REPORT.md` | my own project's record |
| Godot 4.7.2 | engine; Movie Maker for the capture | MIT |
| brutalist.art (local copy at `~/brutalist.art`, vendored 17 September 2026) | the godot-gdd skill's structure, `art godot-gdd --check`, `art final`, `generate_audio_kokoro.py`, fonts | course toolkit |
| Kokoro-82M via kokoro-onnx 0.6.1, voice `am_onyx` | the narration, run locally | Apache-2.0 model |
| faster-whisper `base.en` | transcripts for the pronunciation check and word timings | MIT |
| EB Garamond, Inter, PT Mono | board typography | SIL Open Font License (`OFL.txt` in each font folder) |
| Pillow, NumPy, soundfile, ffmpeg | drawing, audio cleanup, encoding | open source |

The four comparable games (Vampire Survivors, Brotato, 20 Minutes Till Dawn, Halls of Torment) appear by name only. No footage, logo or art from them is used. The names belong to their owners.

## What I made

- The project choice and its direction (Lanternfall, taken to its GDD's next milestone).
- The answers only I can give, on 23 November 2026: the four games I have played; the target role, gameplay programmer; that Godot and GDScript, shaders and materials, and particle effects are new to me in this course; that I already had animation, state machines and testing; and that I picked the project for both learning and showing what I have.
- The game itself, at tags `a3` to `a7`, and the A4 GDD.
- The instruction to base the pitch on my GDD.

## What Claude contributed (Claude Code, Opus 5.5, 23 November 2026)

- Drafted `PROJECT-BRIEF.md` from my answers, the GDD and the Final Portfolio brief on Canvas. That includes the proposed scope, the answer to GDD question Q-01 for this slice, the turret state machine as the planned A9 technique, and the save idea.
- Wrote the narration script, the beat sheet and every board, written as me speaking.
- Adapted the Assignment 2 capture driver (`capture/pitch_driver.gd`) and the A2/A7 film tools (`tools/clean_take.py`, `tools/compose.py`).
- Wrote `tools/make_reel.py`, `build_media.py`, `level_audio.py`, `word_times.py`, `make_evidence.py` and `gdd/docx_to_md.py`.
- Ran the seed search, the capture (from the terminal), the test suite, the narration, the checks and the render.
- Wrote FACTCHECK, SHOTLIST, GDD-COVERAGE, RIFF, PROMPTS, BUILD-PROMPT, README and the FRICTIONAL draft.

## AI narration

The voice is Kokoro `am_onyx`. It speaks as me, in the first person, and says so in the first beat. It is not my voice. The film uses no instructor name, persona or credit line.
