# Weapon-hit sparks — r1/r2 fixture comparison

Both runs are fixture captures from `res://previews/defeat_sparks_preview.tscn`: real market floor, original courier scale, 1280 × 720, 30 fps, fixed seed 7280, Godot 4.7.2, Compatibility, Apple M4. `r2` was captured on 9 November 2026 with `scripts/capture-defeat-sparks.command r2`, run from the terminal, after the colour-ramp change:
- before: middle stop 0.35:(1,0.6,0.2,0.85)
- after: middle stop 0.6:(1,0.75,0.3,1.0)

Files 0–8 are byte-identical between r1 and r2.

The r1 frames that are not in the committed r1 strip (11, 13, 17, 18, 19, 21) come from the full local r1 sequence. Its strip frames match `../r1/strip/` byte for byte (`manifest.json`). These are deterministic fixture renders, not gameplay recordings.

## Measured reading

Region around the burst, courier and text excluded, compared with file 8. Lit = brighter than file 8 by more than 30 summed RGB levels; bright = luma above 150; white = all channels at 250 or more.

| File | Time | r1 lit / extent / RGB / luma / bright | r2 lit / extent / RGB / luma / bright |
|---:|---:|---|---|
| 9 | 0.00 s | 121 / 14 × 14 / (255,255,246) / 254 / 121 | 121 / 14 × 14 / (255,255,246) / 254 / 121 |
| 10 | 0.03 s | 196 / 18 × 18 / (255,252,229) / 251 / 196 | 196 / 18 × 18 / (255,255,236) / 254 / 196 |
| 12 | 0.10 s | 244 / 30 × 29 / (252,210,152) / 215 / 244 | 244 / 30 × 29 / (255,248,198) / 246 / 244 |
| 15 | 0.20 s | 189 / 45 × 43 / (208,140,91) / 151 / 21 | 189 / 45 × 43 / (255,238,163) / 236 / 189 |
| 17 | 0.27 s | 83 / 54 × 52 / (148,94,73) / 104 / 2 | 83 / 54 × 52 / (255,224,133) / 224 / 83 |
| 18 | 0.30 s | 47 / 60 × 55 / (118,75,67) / 83 / 0 | 47 / 60 × 55 / (226,170,108) / 177 / 47 |
| 19 | 0.33 s | 18 / 64 × 55 / (93,59,58) / 66 / 0 | 18 / 64 × 55 / (170,120,84) / 128 / 0 |
| 20 | 0.37 s | 6 / 38 × 57 / (70,46,53) / 51 / 0 | 6 / 38 × 57 / (120,80,66) / 87 / 0 |
| 21 | 0.40 s | 1 px | 1 px |
| 22, 30, 50 | — | none | none |

White pixels at files 11/12/13: r1 71/11/0, r2 96/67/57.

## Prediction against result

| Claude's prediction before the edit | Result |
|---|---|
| Files 9–10 unchanged | Same extent and lit count. File 10 is marginally whiter (B 229 → 236). Matches. |
| File 12: same extent, luma 215 → 235–250, paler | 30 × 29, 244 px, luma 246. Matches. It is closer to white than expected: 67 white pixels against 11. |
| File 15: same extent and ~190 px; luma 151 → 210–240; bright 21 → ≥120; "light yellow-orange" | 45 × 43, 189 px, luma 236, bright 189 of 189. Brightness matches; bright count beat the prediction. The colour is pale yellow (255,238,163), not yellow-orange. |
| Bright yellow until about 0.27 s instead of 0.20 s | File 17 (0.27 s): 83 of 83 lit pixels bright, against 2 in r1. Matches. |
| File 18: luma 80 → 150–180, lit about 47–70 | Luma 83 → 177, lit 47. Matches; lit count at the low end. |
| File 20: nearly gone, 6 → 6–15 px | 6 px, dim orange. Matches, low end. |
| Last trace at file 21 (at most 22); 30 and 50 empty | Last trace at file 21; 22, 30 and 50 empty. Matches. |
| Footprint and widest point unchanged | Every extent is identical, frame for frame; widest 64 px of the 68 px limit. Matches. |

What the prediction missed:
- It treated each spark's ramp colour on its own.
- Additive overlap and the floor push the early and middle frames further toward pale yellow and white.
- The "orange dissipation" in the brief now begins only at about 0.30 s, when most sparks are 1–3 px.

Questions for the running-game verdict:
- Does the paler, longer-bright burst read better?
- Is it now too close in colour to the courier's lamp head or the yellow lamp-oil gems?

## Files

- `../r2/strip/`: files 9, 10, 12, 15, 18, 20, 21, 22, 30, 50 (windowed PNG); the full r2 sequence is kept locally, not in git.
- `comparison-contact-sheet.png`: 3× crops of files 9, 12, 15, 17, 18, 20; r1 top, r2 bottom; courier on the left for scale.
- `manifest.json`: SHA-256 of every frame used and of the sheet.

Running-game verdict: pending.
