# Corrected Assignment 6 review guide

## Current work

Start with the 8 November supplement at the end of CHANGE-BRIEF.md for current design values, and the original brief and dated revisions above it for history. A r2 changes only the middle color-ramp stop, approved before editing. The study copy mirrors that ramp; the generated shader source is unchanged. TUNING.md contains predictions, before/after fixture comparisons and the student's keep decision. TEST-REPORT.md contains The process shader and the current verification section.

## Evidence

- Current wrapper verification: nine suites, 327 assertions, zero failures; two expected mutation failures. See evidence/assignment-6/current-r2-validation/README.md for raw logs, JSON and exact copied source hashes.
- Current CPU cost has original output. Current GPU viewport-timer results are inconclusive due to noise; the screenshot-only additional GPU report is separate. Historical editor captures remain labelled as earlier evidence; new current-r2 captures are also archived with their measurement limits.
- Human visual checks are the student's reported observations in TUNING.md and TEST-REPORT.md. Hidden behavior uses scripted screenshots and state tests.
- The film URL, filename, SHA-256 and filmed source revision remain in SUBMISSION.md. The revised 10:52.1 film shows A r2 and matches godot/ tree 14e6b2c. Bao confirmed complete viewing and listening.

## Still unresolved

1. Current r2 editor Visual Profiler off/on captures are now saved in evidence/assignment-6/cost/visual-profiler-a-r2-current/. GPU measurements are complete. Effect A's selected-frame increments were +0.69 ms and +4.59 ms against a 0.75 ms budget: one comparison was within budget and the other exceeded it, so A did not consistently meet the budget in these samples. B's measured increment was -1.40 ms against a 0.25 ms budget; that sample did not exceed the budget, but the negative difference is not evidence that particles improve performance. These are selected-frame measurements under the Mobile/Vulkan proxy, not a multi-frame estimate for the shipped GL Compatibility renderer.
2. The revised film is rendered, uploaded with link-reader access, and identified by SHA-256 in SUBMISSION.md. Its 32-beat checklist and student viewing/listening confirmation are recorded in the film directory.
3. The assignment requires the student to write the brief, predictions, verdicts and process-shader explanation. Assistance and rewriting cannot establish that authorship or the original pre-build chronology; historical records must remain accurate.
4. Original agent prompts/transcripts were not provided. A reconstructed prompt must not be represented as the original session.
5. B's baseline strip was re-rendered after the change. That historical order cannot be repaired by renaming files or dates.
6. Final source is being committed and published on assignment-6-r3, with a matching git-archive ZIP and delivery manifest. Sending the materials to the TA remains a separate step; corrected Teams delivery has been authorized without a late penalty.

No code, test, source log or measurement timestamp was backdated. No delivery has been made by this review guide.
