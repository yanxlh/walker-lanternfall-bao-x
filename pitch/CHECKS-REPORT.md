# CHECKS-REPORT — Lanternfall: First Delivery

All checks run on 23 November 2026 on an Apple M4 Mac (macOS 26).

## The master

| | |
|---|---|
| File | `exports/landscape/lanternfall-first-delivery-pitch.mp4` (not in git) |
| SHA-256 | `02e49cb8605ef5babc4e575d2ee10a653862adfab021dafa3d4b684629aa5bbb` |
| Size | 126,312,291 bytes |
| Video | H.264, 3840 × 2160, 30 fps |
| Audio | AAC, 48 kHz, stereo; integrated loudness -17.9 LUFS, peak -3.9 dBFS |
| Length | 225.53 s (3:45.5), inside the assignment's 2–4 minutes |
| Toolkit record | `exports/landscape/lanternfall-first-delivery-pitch.verified.json` (status `ready`, input hashes) |

## Reviewer access to the film

- Link: https://drive.google.com/file/d/1tM613ITsd_7WqycibXfJFZx7mFv35mDY/view
- Checked on 23 November 2026 with `curl` and no Google cookies:
  - The view page answered 200 with the title `lanternfall-first-delivery-pitch.mp4 - Google Drive`.
  - The download answered 200, `video/mp4`, 126,312,291 bytes.
  - Its SHA-256 was `02e49cb8605ef5babc4e575d2ee10a653862adfab021dafa3d4b684629aa5bbb`, the same as the master.

## Gates

| Gate | Result | Report |
|---|---|---|
| GATE F: FACTCHECK, SHOTLIST and PROMPTS present | pass | `art final` refused nothing at preflight |
| `beat_lint.py`, `gate_shape.py` (final preflight) | pass | `final-export.log` |
| Render integrity: 14 of 14 slots filled, no slate | pass | `final-export.log`: "slots: 14/14 filled" |
| Gate V, frame QC (28 steady-state samples: edge-bleed, fill, contrast) | pass: 0 BLOCKER, 0 MAJOR | `_qc/REPORT.md`, `_qc/contact_sheet.png` |
| `art godot-gdd --check . --gdd gdd/GDD-v0.3.md` | PASS: 16 sections, 8 exact excerpts, 9 evidence files | output below |

```
GDD evidence check PASS: {"sections": 16, "excerpts": 8, "evidence_files": 9}
Structural coverage only; editorial accuracy and human judgment are separate.
```

### Failed attempts, kept

- **First `art final`** (same day): Gate V refused the candidate with 24 BLOCKER and 4 MAJOR findings.
  - The boards ran about 12 px past the right title-safe edge and the footer past the bottom edge.
  - B01's full-width footage crossed every edge, and its whole-frame contrast was 0.09 to 0.18.
  - B13 filled only 18% of the safe area.
- **Fixes:**
  - Every board is scaled by 0.96 about the centre.
  - The footage is shown at 3200 × 1800 inside the safe area. B01 declares its two added text regions for the regional contrast check, with a written reason in `beat_sheet.json`.
  - B13 gained three real stills.
  - B00 gained a footer line, because it measured exactly at the 55% fill floor.
- **Second run:** clean.

### Advisory lines (not gates)

`art final` prints three SKIN LINT lines:
- no Remotion or Manim beats;
- B00 is not a ClaudeComposerAsk;
- B13 is not a ClaudeTitleOutro.

All three are deliberate. Those components print the instructor's handle, and Assignment 8 forbids the instructor's name, persona or credit line.

## Visual check of the master

I read three frames per beat from the master: 0.6 s in, the middle, and 0.35 s before the end.

- Every board's reveals land in order.
- No text overlaps.
- Every status chip is legible.
- B01's four excerpts appear with their chips.
- The win panel is on screen for the last 2 s of B01.

Fixed earlier, in the beat renders:
- B01's chips covered the game HUD, so they were moved to the bottom right.
- B12's section title overlapped its excerpt; it was shortened.

## Narration

- Kokoro `am_onyx`, levelled per beat to -16 LUFS (`audio-levels.json`: -18.5 to -16.3 measured after levelling).
- A transcript (faster-whisper `base.en`, `word-times.json`) was checked against the script.
- "Tag A five", "A six" and "A ten" were first heard as "tag of five" and similar. They were re-voiced as "A-five" etc. and re-checked.
- Remaining transcript differences come from the recogniser, not from mispronounced claims:
  - the name is heard as "Bousing" in B00 and as "Bao Xing" in B13;
  - "Godot" is heard as "got out" twice;
  - "doc" is heard as "dock".

## Source game check

- `scripts/run-all-a7.sh` ran in the a8 worktree at `124086c` (`godot/` = tag a7) after a headless import from an empty cache.
- 23 of 23 runs exited 0, and no import or test log has SCRIPT ERROR, SHADER ERROR or "Failed loading resource".
- `git status godot` was clean before and after (`evidence/a7-suite-20261123/`).
- The run rewrote the timestamps in the tracked `evidence/*.json` files; they were restored with `git checkout`.

## What these checks do not show

- Whether the pitch persuades anyone.
- Whether the proposed scope fits four weeks.
- Whether the AI voice sounds like the student's intent.

Bao's viewing is recorded in FRICTIONAL.md, in Bao's words.
