# Lanternfall, Sparked — the particle-effects film

A 4K landscape teardown of this repository's particle-effects assignment, made with the **godot-gamedev skill + walker modifier** (Walker bookends; Verdict → Your Turn → the regular outro). Narrated by Liam, in for Bear (Kokoro `am_onyx`). Game source revision shown: **c3e1273** (`FILM-SOURCE-REVISION.txt`). The Assignment 2 film in `../claude-liam-walker-lanternfall-bao-x-gamedev/` is unchanged.

| File | What it is |
|---|---|
| `beat_sheet.json` | the film, beat by beat: narration, what is on screen, scene props, measured durations |
| `gamedev-evidence.json` | every file of `godot/` hashed and tied to a component; verbatim excerpts; each code beat paired with its hashed result clip |
| `COMPONENTS.md` | the components the film explains, and the four files it leaves out (with reasons) |
| `SHOTLIST.md` | what each beat shows and where it came from |
| `SCRIPT.md` | the narration, beat by beat, with timings and what is on screen |
| `FACTCHECK.md` | every claim and its source; the corrections made while building |
| `CAPTURE.md` | how the footage was captured (isolated copy, driver, seeds, dry runs) |
| `SOURCES.md` | captures with hashes, repository material shown, tools, voice |
| `RIFF.md` | the judgments the narration makes and what each rests on |
| `PROMPTS.md` | the reconstructed Walker ask, the Your Turn prompt, the request that produced the film |
| `BUILD-PROMPT.md` | how to rebuild everything |
| `CHECKS-REPORT.md` | checker results, beat classification, teaching-arc checklist, visual QC |
| `capture/` | capture driver and scenes, take logs and dry runs, take hashes (the AVI files are not committed) |
| `tools/` | the scripts that build the sheet, the evidence beats, the ledger, the shot list and the script |

The rendered film (`exports/landscape/…mp4`) and every intermediate video stay out of git.

## Source revision in this repository

`c3e1273` is a commit of the course repository (github.com/nikbearbrown/csye-7270-building-virtual-environments, branch `xinghe-b/assignment-2`), where this film was built. In this repository the same commits were replayed onto tag `a3`; `c3e1273` corresponds to **`7637dbf`**. Its `godot/` is c3e1273's plus Assignment 3's files and two A3 edits that the film does not show (TEST-REPORT, "Assignment 6 moved onto this repository"). Every code excerpt in the film is identical at both. `./art godot-gamedev --check` was run against the course copy at c3e1273 (PASS), because it hashes the whole `godot/` and needs the rendered `media/`, which is not in git.
