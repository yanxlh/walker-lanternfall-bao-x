# Lanternfall: First Delivery — final project pitch

**Bao Xing · CSYE 7270 Assignment 8 · 23 November 2026**

| | |
|---|---|
| Working title | Lanternfall: First Delivery |
| Target role | Gameplay programmer (reader: a hiring manager or a lead gameplay engineer) |
| Runtime | Godot 4.7.2 (`4.7.2.stable.official.ed1daf0bf`), GDScript, GL Compatibility renderer; export target macOS desktop (Apple Silicon) |
| Game shown | tag `a7` (`godot/` = `5f09b7f`); `godot/` is unchanged on this branch |
| Design source | my Assignment 4 GDD v0.3, 17 October 2026: [`gdd/`](gdd/) |
| Film | Google Drive: https://drive.google.com/file/d/1tM613ITsd_7WqycibXfJFZx7mFv35mDY/view (anyone with the link can view) |
| File | `exports/landscape/lanternfall-first-delivery-pitch.mp4` (not in git) |
| SHA-256 | `02e49cb8605ef5babc4e575d2ee10a653862adfab021dafa3d4b684629aa5bbb` |
| Length, format | 3:45.5 (225.53 s), H.264 3840 × 2160, 30 fps, AAC stereo, 126,312,291 bytes |

## Read in this order

1. [PROJECT-BRIEF.md](PROJECT-BRIEF.md): the seven answers on one page, ending with **exists today** (with tags) and **will exist**.
2. The film: link above.
3. [FACTCHECK.md](FACTCHECK.md): every claim and its source. [GDD-COVERAGE.md](GDD-COVERAGE.md): where each GDD section went.
4. [SOURCES.md](SOURCES.md): what I used, what I made, what Claude contributed. [FRICTIONAL.md](FRICTIONAL.md): the log.
5. [CHECKS-REPORT.md](CHECKS-REPORT.md): the gate results and the visual check.

## What is real in the film

- Gameplay (B00, B01, B06, B09) is a Movie Maker capture of an isolated copy of tag `a7`, driven by scripted input (`capture/pitch_driver.gd`, seed 21), cut into four excerpts at real speed, with game sound off.
- Evidence tiles (B07) are captures already committed for Assignments 5, 6 and 7.
- Everything that does not exist yet (post office menu, Engineer, turret, delivery, saved record, lit gate, export) is a constructed diagram, labelled PROPOSED on screen.
- The voice is an AI voice (Kokoro `am_onyx`) reading my script, and says so.

## Rebuild the film

See [BUILD-PROMPT.md](BUILD-PROMPT.md). In short, from this folder:

```bash
capture/capture-pitch-take.command 21
python tools/clean_take.py capture/take-pitch-seed21.avi
python3 tools/make_reel.py && python $ART/runtime/scripts/generate_audio_kokoro.py . && python tools/level_audio.py
python tools/word_times.py && python3 tools/make_reel.py && python tools/build_media.py && python3 tools/make_evidence.py
$ART/art godot-gdd --check . --gdd gdd/GDD-v0.3.md
$ART/art final . --height 2160 --fps 30 --out exports/landscape
```

## Folder

| Path | What |
|---|---|
| `beat_sheet.json` | narration and visual plan, measured durations, cue times |
| `gdd-evidence.json`, `GDD-COVERAGE.md` | GDD hash, section coverage, exact excerpts, evidence hashes |
| `gdd/` | the A4 GDD (docx, pdf), its Markdown conversion and the converter |
| `capture/` | capture kit, driver, take logs, clean-take record (video not in git) |
| `tools/` | the scripts that build the film |
| `evidence/` | today's a7 suite run; copies of the A6 cost report and A7 records the film cites |
| `CHECKS-REPORT.md`, `final-export.log`, `audio-levels.json`, `word-times.json` | gate reports and measurements |
