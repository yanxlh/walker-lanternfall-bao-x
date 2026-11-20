# Visual QC: frame-level pass on the final export

`REPORT.md` and `contact_sheet.png` in this folder are the toolkit's own Gate V output. `master-sheet.png` (one frame at 50 % of every beat), `master-cuts/` (the first, middle and last frame of every beat) and `master-audio.json` (loudness per beat) come from `tools/master_qc.py`. This file records the frame-level pass, which was checked by eye.

Master: `exports/landscape/claude-liam-walker-lanternfall-bao-x-animation-gamedev.mp4`, 3840 × 2160, 30 fps, H.264 + AAC 48 kHz stereo. Duration 530.77 s (8:51), 100,385,291 bytes. SHA-256 `3ce7f3f2579b8acad07f1a9155b1bbcc5cca062049ca56b2f7663595aa2b131b`, which matches `.verified.json` (status `ready`).

## Procedure

1. During the build:
   - every media beat was sampled at 15/50/85 % and at its last frame;
   - every code beat was sampled after its last highlight;
   - before the final export, Gate V was run on 48 frames taken from `media/` at 50 % and 85 % of every beat: 0 BLOCKER, 0 MAJOR.

   The defects found and fixed are in `../CHECKS-REPORT.md`.
2. On the export:
   - Gate V sampled 48 frames: 0 BLOCKER, 0 MAJOR;
   - `master-sheet.png` and `master-cuts/` were read. All 24 beats are present, in order, with the right content.
3. The whole master was scanned at 2 fps (1,062 frames):
   - **near-uniform frames** (luma standard deviation < 4) appear only at 0.0 s and 489.5 s. These are the cream page on the first frames of B00 and B22, before the composer card fades in, and are expected;
   - **stretches with no change for 6 s or more** fall only on cards and code panels held while the narration continues. None falls inside a take segment of B07, B11 or B13.

## Exports refused before this master

- **First export:** `art final` ran its frame check with Homebrew's `python3`, which no longer had Pillow, and refused the candidate. The export now runs with the toolkit's environment first on `PATH` (`../BUILD-PROMPT.md`, step 8).
- **Second export:** Gate V found B01 underfilled (52 % of the safe area). Looking at B01 for that showed the real defect: the on-screen line never changed from "An animation is a movie". Then every beat was reviewed again, which led to the fixes for B03, B06, B07, B11, B13, B15, B17, B19 and B20 listed in `../CHECKS-REPORT.md`.

## Minor, left as it is in this master

- **Evidence beats B05, B07, B09, B11, B13, B15, B17, B19 and B20, last ≈ 0.25 s:** layers that appear during the beat fade out just before the cut, and the title and footer stay. `tools/compose.py` fades a layer out when its end time falls before the clip's last frame, and `tools/build_media.py` clamps every end time to the beat's duration. That duration is a few milliseconds shorter than the frame-rounded clip. The result reads as a short dissolve before each hard cut. Nothing is lost: every layer is fully visible for the rest of the beat.
- **Outro B23:** the true peak is +0.2 dBTP in the AAC master, against −0.4 dBTP in the stock jingle `bear-brown-3.mp3`. This is overshoot from lossy encoding. The jingle is left as it is.

## 9-point rubric

| Check | Result |
|---|---|
| Edge bleed / clipping | none; every code panel shows its whole excerpt and every highlighted line |
| Title-safe margins | titles, footers and @NikBearBrown inside SAFE; footers single-line |
| Container overflow | none after the build fixes (B03 excerpt, B06/B14 panels, card padding) |
| Collision | none |
| Off-screen anchors | none |
| Legibility | card text 50–56 px at 4K in B15, B17, B19 and B20; take tiles at 340–380 px; code at 22–30 px in the 1920-wide Remotion frame |
| Brand mark | @NikBearBrown on every beat but B01, and on the outro; one handle per beat |
| Aspect | 16:9 throughout; pixel art scaled with nearest neighbour |
| Canvas fill | Gate V clean on the export; B05, B09 and B17 fill their lower half only once the narration reaches the card that goes there |

## Sound

- Narration (B00–B22): EBU R128, −18.5 to −17.5 LUFS integrated per beat in the master, with true peaks at −4.2 dBTP or lower and no silence longer than 1.2 s inside any narration beat (`master-audio.json`). Before and after levelling: `../audio-levels.json`.
- There are no game-sound beats. The evidence beats carry no take audio, so no sync check applies (`tools/check_sync.py` is for game-sound beats).
- Outro: the stock jingle `bear-brown-3.mp3`, uncut, followed by 1.0 s of silence; −15.5 LUFS.

## Not covered by this pass

Bao has not yet watched or listened to the whole film (content, pacing, voice, every narration transition). Only Bao can do that.
