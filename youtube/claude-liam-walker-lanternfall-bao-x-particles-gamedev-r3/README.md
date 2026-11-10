# Lanternfall, Sparked Again — the revised particle-effects film

A 4K landscape teardown of this repository's particle-effects assignment as it stands after Effect A's observed r2 change. It was made with the **godot-gamedev skill + walker modifier**: Walker bookends, then Verdict → Your Turn → the regular outro. Narrated by Liam, in for Bear (Kokoro `am_onyx`, synthetic narration). The game source shown is `godot/` tree `14e6b2c` (commit `c6e6343` plus uncommitted tests; FILM-SOURCE.md). The first particle film, `../claude-liam-walker-lanternfall-bao-x-particles-gamedev/`, is unchanged.

What the first film did not have, and this one does:
- the three parts of a particle system, each with lines of the scene file (B04–B05);
- Effect A's intent and first strip (B08);
- the observed change r2, with its prediction, strips and verdict (B11–B12);
- two shader lines beside the brief settings they implement (B23);
- why a GPU effect's headless price is near zero (B26);
- the GPU price as it currently stands, unresolved (B27);
- mistakes caught, Claude against Bao, uncertainty, the next step, contributions, texture source and revision shown (B28);
- 327 checks instead of 292.

| File | What it is |
|---|---|
| `beat_sheet.json` | the film, beat by beat: narration, what is on screen, scene props, measured durations |
| `gamedev-evidence.json` | every file of the snapshot's `godot/` hashed and tied to a component; verbatim excerpts; each code beat paired with its hashed result clip |
| `COMPONENTS.md` | the components the film explains, and the four files it leaves out |
| `SHOTLIST.md` · `SCRIPT.md` | what each beat shows; the narration with timings |
| `FACTCHECK.md` | every claim and its source; the corrections made while building |
| `CAPTURE.md` · `FILM-SOURCE.md` | how the footage was captured; exactly which source it shows |
| `SOURCES.md` · `RIFF.md` · `PROMPTS.md` | material and hashes; the judgments; the prompts |
| `BUILD-PROMPT.md` · `CHECKS-REPORT.md` | how to rebuild; checker results and visual QC |
| `capture/` | driver and scenes, take logs and dry runs, the clean-take record, hashes (videos not committed) |
| `tests/` | this film's own CPU and GPU cost runs (JSON) |
| `tools/` | the scripts that build the sheet, the evidence beats, the ledger, the shot list and the script |

The rendered film (`exports/landscape/…mp4`) and every intermediate video stay out of git.

## Uploaded master

[Watch the revised film](https://drive.google.com/file/d/1AMPOgsAAzkMnPbl0OFWOPsQ2y_F3aN5h/view?usp=drivesdk) — anyone with the link can view (verified). Size: 149,420,723 bytes. SHA-256: `1a06751d82b91360f93ca3bcf6e4702d447388fd56cabddb77f3ba84ff1e3ded`.

See [_qc/codex-review/REVIEW.md](_qc/codex-review/REVIEW.md) for the additional visual and full-stream technical checks, their limits, and the corrected B26 script entry.

## Budget interpretation update

The unchanged master uses the phrase "unsettled GPU budget." The submission now gives an explicit measured-sample verdict: A measured +0.69 ms (within 0.75 ms) and +4.59 ms (over 0.75 ms), so it did not consistently meet budget in these samples. The source measurements, film bytes and SHA-256 are unchanged. These selected frames do not establish a multi-frame cost for the shipped renderer.
