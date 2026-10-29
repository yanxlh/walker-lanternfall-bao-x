# Weapon-hit sparks — r0/r1 fixture comparison

Both strips come from the same preview scene, with the real market floor, original courier scale, 1280 × 720, 30 fps and fixed seed 7280 (Godot 4.7.2, Compatibility, Apple M4). `r0` was captured on 29 October 2026 before the edit; `r1` was captured after `scale_amount_max` changed from 1.2 to 1.8. Both runs used `scripts/capture-defeat-sparks.command` from the terminal. Files 0–8 are pixel-identical between runs, so the background and courier match. These are deterministic fixture renders, not gameplay recordings.

The burst first appears in file 9 because Movie Maker numbers files from 0. Times below are measured from that frame. The courier's warm-pixel height is 34 screen pixels.

## Prediction made before editing

On the first visible frame the cluster grows from 11 × 12 to about 15 × 15 (about 0.45 courier height), with more pure-white pixels. Early sparks are 3–4 pixels wider and the largest sparks visibly bigger. At 0.20 s the spread stays about 45 pixels wide with about 1.5 times as many lit pixels. The widest point is about 55–62 pixels, still under 68. Fade timing is unchanged, and strip frames 30 and 50 are empty. The first frame does not reach a full character height.

## Measured reading

Spark pixels are those brighter than file 8 by more than 30 summed RGB levels, with the text labels excluded.

| File | Time | r0 lit px / extent / white | r1 lit px / extent / white |
|---:|---:|---|---|
| 9 | 0.00 s | 88 / 11 × 12 / 66 | 121 / 14 × 14 / 91 |
| 10 | 0.03 s | 134 / 17 × 16 / 65 | 196 / 18 × 18 / 115 |
| 11 | 0.07 s | 137 / 23 × 22 / 35 | 228 / 24 × 24 / 71 |
| 12 | 0.10 s | 159 / 29 × 28 / 3 | 244 / 30 × 29 / 11 |
| 15 | 0.20 s | 102 / 45 × 43 / 0 | 189 / 45 × 43 / 0 |
| 18 | 0.30 s | 29 / 60 × 52 / 0 | 47 / 60 × 55 / 0 |
| 19 | 0.33 s | 13 / 26 × 55 / 0 | 18 / 64 × 55 / 0 |
| 20 | 0.37 s | 5 / 38 × 57 / 0 | 6 / 38 × 57 / 0 |
| 21 | 0.40 s | 1 / 1 × 1 / 0 | 1 / 1 × 1 / 0 |
| 22–59 | — | none | none |

## Prediction against result

| Prediction | Result |
|---|---|
| First frame about 15 × 15, more white | 14 × 14 (0.41 courier height); white pixels 66 → 91. Matches. |
| Early sparks 3–4 px wider | Only about 1 px wider (17 → 18, 23 → 24, 29 → 30). Over-predicted: particle positions set the footprint, and larger sprites mostly fill in the existing cluster. Lit area grew 1.4–1.7×. |
| Spread at 0.20 s unchanged, about 1.5× lit pixels | Spread 45 × 43 in both; lit pixels 102 → 189 (1.85×). More than predicted. |
| Widest 55–62 px, under 68 | 60 × 55 at file 18. File 19 reaches 64 px with only 18 sparse pixels. Under 68. |
| Fade unchanged; frames 30 and 50 empty | Last trace at file 21 in both; nothing from file 22; 30 and 50 empty. Matches. |
| No full character height at start | 0.41 courier height at first frame, 0.71 by 0.07 s. Matches. |

In the contact sheet the r1 sparks read as chunkier yellow-orange squares from 0.03 to 0.27 s. The burst occupies the same footprint and disappears on the same frame. The change is visible in the 3× and 6× crops but modest at full frame. Do not describe r1 as a wider, longer or denser burst.

## Human verdict

After playing the revised game, the student replied “保留 更清晰了” (keep it; clearer). Keep r1. The measured reading above is the image comparison, distinct from this running-game verdict.

## Files

- `../r0/strip/`, `../r1/strip/`: seven original windowed PNG frames each (9, 10, 12, 15, 20, 30, 50).
- `comparison-contact-sheet.png`: 3× crops, files 9, 10, 12, 15, 17, 20; r0 top, r1 bottom; courier on the left for scale.
- `comparison-detail.png`: 6× crops of files 9, 11, 13.
- `manifest.json`: SHA-256 for every strip frame and sheet.
