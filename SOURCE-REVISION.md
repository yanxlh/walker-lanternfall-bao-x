# Source revision identity

Current correction: historical tree-equality statements below describe the earlier film/release. A r2 changes are identified in “Current corrected source scope” at the end; exact current copied-source hashes are in evidence/assignment-6/current-r2-validation/source-sha256.json.

Film game source in the course repository: `c3e12737d9b38679efa61622cb62c793935aff59`.

Course project prefix: `fall-2026/xinghe-b/assignment-2/walker-lanternfall-bao-x/`.

The project was exported with `git subtree split`, retaining project-specific commit order, author information and messages while removing unrelated course files. Subtree commits consequently have different IDs. The imported project-history head is `ab2a082f2689505f9b4c69e12de51310f764163c`. The original film revision is identified by its exact Godot tree, rather than asserting identical commit IDs.

Film Godot tree: `57f2d8e7e6402c49d03fcb11c215cdc888b01af2`.
Imported Godot tree: `57f2d8e7e6402c49d03fcb11c215cdc888b01af2`.

The trees are identical. Final preparation changes reports, verification outputs and submission metadata only; it does not change game source, shaders or project settings. The final commit is identified in the Canvas comment.

Earlier standalone Assignment 3 work remains on the existing master branch and a3 tag. The a6 submission branch imports the particle prototype that was filmed; it does not replace that earlier history.


## Revision 2 source scope

The complete Godot tree identity described above applies to a6. In a6-r2, the independent GPU study and new test/preview fixtures change the Godot tree; game code, production effects, shaders, assets and project settings still match a6 byte for byte. The film remains an accurate demonstration of gameplay, but does not demonstrate the newly repaired independent study.


## Commit-ID map (added 9 November 2026)

TEST-REPORT, TUNING and FRICTIONAL cite commit IDs from the course repository, where the work was first committed. Those IDs do not exist on GitHub. The subtree export kept each commit's message, author and time, so every cited ID maps one-to-one, by message, to a commit on this branch:

| Course repository | GitHub (this branch) | Time (EDT) | Message |
|---|---|---|---|
| `9fa5d88` | `2a4a9d0` | 10-10 02:14 | Add Xinghe Bao Assignment 2 Lanternfall submission |
| `8eb16a2` | `04ef18a` | 10-29 13:03 | Record particle effect design and test wrapper before implementation |
| `a46c055` | `093cac0` | 10-29 13:04 | Add project context and boundaries for particle implementation |
| `ec024c5` | `6d88e4b` | 10-29 13:37 | Record approved weapon-hit, level-up and movement effect design |
| `3a5be66` | `902a9f8` | 10-29 14:59 | Add weapon-hit sparks, movement trail and level-up celebration |
| `8535049` | `7a28cd6` | 10-29 14:59 | Add particle config, state, edge-case and cost tests with capture tools |
| `f85990b` | `8af1cf2` | 10-29 14:59 | Add particle tuning captures, play checks, test results and cost data |
| `c930886` | `18f11c3` | 10-29 14:59 | Add editor-generated particle process shader study |
| `c3e1273` | `299668a` | 10-29 14:59 | Record particle tuning, play checks, cost, shader study and diary |
| `4eedf34` | `59c366d` | 10-29 16:10 | Add the particle-effects film build (godot-gamedev + walker) |
| `b7b4e48` | `929ca5f` | 10-29 17:08 | Fix the trail-sphere wording in the particle film (radius, not width) |
| `4bec76e` | `f848c21` | 10-29 17:29 | Record the editor Visual Profiler check: GPU 0.0 ms under Compatibility |
| `0bb97f6` | `61e11bb` | 10-29 17:29 | Align cost records with the Visual Profiler note |
| `15aaf06` | `4451950` | 10-29 17:36 | Credit Codex for the editor conversion and the sampled film review |
| `5d518b2` | `5baaeee` | 10-29 17:38 | Add the Assignment 6 contribution statement |
| `3c18a0d` | `23f24a2` | 10-29 17:41 | Link the particle film on Google Drive |
| `26ab741` | `ab2a082` | 10-29 17:44 | Record Bao's full review of the particle film |

Commits made after the export (`f592d33` tag a6, `09070e2` tag a6-r2, and the revision 3 commits) exist only on GitHub.

The five 14:59 commits hold the build, the tests, both tuning cycles, the play checks, the cost data and the shader study. They were committed together after the work, so the git history does not show each tuning step as its own commit. The order of the steps is in the dated entries of `TUNING.md` and `CHANGE-BRIEF.md`.


## Current corrected source scope

The historical tree equality above applies to the earlier filmed release. The later A r2 trial changes the production hit-spark ramp and the GPU-study copy ramp (389c369); its captured comparison and keep decision are 39f8943 and c6e6343. Current documentation and test additions are further corrections. The film remains an earlier-version demonstration, not an exact recording of the current r2 source. The corrected delivery goes directly to the TA via Teams; its exact final commit and ZIP checksum must be recorded when packaged.
