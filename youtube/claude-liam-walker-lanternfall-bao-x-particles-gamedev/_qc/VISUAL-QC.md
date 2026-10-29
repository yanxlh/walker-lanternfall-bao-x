# Visual QC — manual pass on the final export

`REPORT.md` and `contact_sheet.png` in this folder are the toolkit's own Gate V output. This file records the manual frame-level pass.

Master: `exports/landscape/claude-liam-walker-lanternfall-bao-x-particles-gamedev.mp4` · 3840 × 2160, 30 fps, H.264 + AAC 48 kHz stereo · 487.73 s · 138,586,012 bytes · SHA-256 `4d4d590039ff8a6dfd26571018120ecec9be324a7a8b1df16cb923020eeb6417` (matches `.verified.json`, status `ready`).

## Procedure

1. The first export was sampled at 2 fps: 974 frames, read as 16 contact sheets of 64 frames each.
2. Near-uniform frames were flagged (luma standard deviation < 4). Only 0.0 s and 453.0 s were flagged: the cream page on the first frame of B00 and of B25, before the composer card fades in. Both are expected.
3. One defect was found (below). B21 was fixed and the master re-exported. Only B21's media changed, so the re-export's B21 span (372–396 s) was sampled again at 2 fps and read.
4. During the build, every media beat was sampled at 15/50/85 % and every code beat at its last highlight. Those defects and fixes are in `../CHECKS-REPORT.md`.

## Defect found in the first export, fixed

- **B21, last ≈ 0.4 s (around 394.5 s):** the closing real-speed play of the 90-frame (3.00 s) study clip was given 3.4 s, so the video area went blank before the cut. It was shortened to 2.9 s. In the re-export the video area is filled at 394.0 and 394.3 s, and B22 starts at 395.0 s.

## Bao's review of the second master, fixed

- **B12, about 3:27:** the narration said "a sphere three pixels wide"; `emission_sphere_radius = 3.0` is a radius (6 px across). The line now reads "a sphere with a three-pixel radius" and the highlight label "(radius, px)". B12's narration was regenerated and re-rendered, and the master re-exported. A local Whisper transcription of the new master reads at 209.6 s: "It emits continuously from a sphere with a three-pixel radius". The B11–B13 span (203–229 s) was sampled again at 2 fps. Only B12 changed, so every later beat moved by +0.57 s.

## 9-point rubric

| Check | Result |
|---|---|
| Edge bleed / clipping | none; code panels show every highlighted line |
| Title-safe margins | titles, footers and the @NikBearBrown mark inside SAFE; footers single-line (measured) |
| Container overflow | none after the build fixes |
| Collision | none remaining (B05 ring label moved off the HUD) |
| Off-screen anchors | none |
| Legibility | caption floor 48 px at 4K; code at the Assignment 2 film's sizes |
| Brand mark | @NikBearBrown on evidence beats and the outro; one handle per beat |
| Aspect | 16:9 throughout; pixel art scaled with nearest neighbour |
| Canvas fill | evidence beats fill the safe area; B23 opens on an empty card for about 1.6 s until the first bar is spoken (an intentional reveal) |

## Sound

- Narration: EBU R128, −18.6 to −17.6 LUFS integrated (`../audio-levels.json`).
- Game-sound beat B03: one constant gain of −5.5 dB (−17.4 LUFS), no other processing. `tools/check_sync.py` against `capture/take-main-seed11.avi`: offset 0.04 ms, correlation 0.999, **SYNC OK**.
- Outro: stock jingle `bear-brown-4.mp3`, uncut, with 1.0 s of silence.

## Not covered by this pass

A human viewing and listening of the whole film (content, pacing, voice, every narration transition). That is Bao's review.
