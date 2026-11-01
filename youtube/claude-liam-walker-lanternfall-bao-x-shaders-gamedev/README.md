# Lanternfall, Shaded — the shader and material film

A 4K landscape teardown of this repository's Assignment 5 (shaders, materials and the Godot shading language), made with the **godot-gamedev skill + walker modifier** (Walker bookends; Verdict → Your Turn → the regular outro). Narrated by Liam, in for Bear (Kokoro `am_onyx`). Game source revision shown: **4246f94** (`FILM-SOURCE-REVISION.txt`), read through git, never from the working tree. The earlier films in `../` are unchanged.

| File | What it is |
|---|---|
| `beat_sheet.json` | the film, beat by beat: narration, what is on screen, scene props, measured durations |
| `gamedev-evidence.json` | every file of `godot/` at 4246f94 hashed and tied to a component; verbatim excerpts; each code beat paired with its hashed result clip |
| `COMPONENTS.md` | the components the film explains, and the files it leaves out (with reasons) |
| `SHOTLIST.md` | what each beat shows and where it came from |
| `SCRIPT.md` | the narration, beat by beat, with timings and what is on screen |
| `FACTCHECK.md` | every claim and its source; the revision change; corrections made while building |
| `CAPTURE.md` | the new take, the shader-pair fixture and the test re-run (isolated copies, driver, seed, dry run) |
| `SOURCES.md` | captures with hashes, repository material shown, roles, texture licence, tools, voice |
| `RIFF.md` | the judgments the narration makes and what each rests on |
| `PROMPTS.md` | the reconstructed Walker ask, the Your Turn prompt, the request that produced the film |
| `BUILD-PROMPT.md` | how to rebuild everything, including why the evidence-beat compositor differs from the template |
| `_qc/REPORT.md` | visual and audio QC of the master: defects found and fixed |
| `capture/` | capture driver and fixture, take log and identical dry run, fixture renders and measurements, the film's test run (the AVI is not committed) |
| `tools/` | the scripts that build the sheet, the evidence beats, the ledger, the shot list and the script |

## The master

| | |
|---|---|
| File | `exports/landscape/claude-liam-walker-lanternfall-bao-x-shaders-gamedev.mp4` (not in git) |
| Format | 3840 × 2160, 30 fps, H.264 + AAC 48 kHz stereo, 103,739,791 bytes |
| Duration | 656.9 s (10 min 57 s), 31 beats |
| SHA-256 | `c6f001c100758306c45d279ee52ed207d43900db72e001b7328d1fa99e50a1b7` (receipt: `.verified.json` beside it) |
| Source revision shown | `4246f94bd3db51c0644ecc3bef9b3a8c8427911b` (`godot/` unchanged through `b295096`) |
| Bao's words | quoted in English as recorded at `b295096` (TEST-REPORT.md, PREDICTION.md); no Chinese originals |
| Checks | `./art godot-gamedev --check` PASS against `git archive 4246f94 godot`; `./art final` Gate V 62 frames, 0 BLOCKER, 0 MAJOR |
| Audio | narration beats −17.3 to −19.0 LUFS, game-sound beat −16.9, outro jingle −16.2; true peaks ≤ −2.0 dBFS (`_qc/master-audio.json`) |

The rendered film and every intermediate video stay out of git. Nothing was committed, pushed or published by this build, and no one has reviewed the film yet.
