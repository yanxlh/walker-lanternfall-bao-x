# Assignment 6 revision 3

This revision corrects documents after an audit of a6-r2 on 9 November 2026. It changes no game, effect, shader, asset, test, script or project-setting file: `git diff --stat a6-r2 -- godot/ scripts/` is empty. The film therefore still shows the submitted game source.

## What changed

- **SUBMISSION.md:** now consistent with a6-r2 and the evidence. It gives eight suites and 313 assertions, not seven and 292. The stale "study copy lacks its ramp textures" limitation, fixed in a6-r2, is removed. The measured prices sit beside each budget, and the GPU proxy renderer is named. A note explains why this lineage does not descend from tag a5.
- **README.md:** a new Assignment 6 section at the top. It gives the project, engine, renderer, run, controls (no vsync debug key), what was added, tests, the film and limitations. The Assignment 2 README follows unchanged.
- **CLAUDE.md:** the three headless facts from the brief, the shader-study and cost commands, and updated "Unconfirmed" lines (tag a5 lineage, the a6-r2 Visual Profiler captures).
- **TEST-REPORT.md:** a new section, "Assignment 6 revision 3". It has the re-run results, the current prices against budget (superseding the 29 October coverage row), the edge-of-screen note, and a table of requirements that are not met or lack a recorded human check.
- **SOURCE-REVISION.md:** a map from the course-repository commit IDs cited in the reports to the GitHub commit IDs.
- **TUNING.md:** a commit trace for each revision, and the points of the tuning record that are not met.
- **CONTRIBUTIONS-assignment-6.md** and **FRICTIONAL.md:** entries for revisions 2 and 3.
- **evidence/assignment-6/revision-3-validation/:** logs, result JSON and exit codes for the re-run.

## Verification

From a fresh import of this branch: eight suites, 313 assertions, zero failures, no SCRIPT ERROR or SHADER ERROR. Both A mutations exit 1. The headless cost script exits 0 with every delta under budget. Details: TEST-REPORT.md, "Assignment 6 revision 3".

## Not changed by this revision

No document records a new student observation, verdict, disagreement or shader explanation. The requirements listed as not met in TEST-REPORT.md remain not met until the student does them.
