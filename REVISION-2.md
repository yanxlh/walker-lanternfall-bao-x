# Assignment 6 revision 2

This supplement addresses the editor GPU evidence and incomplete generated-shader study resources after the original a6 submission. The original a6 tag remains intact; the supplemental source is identified by a6-r2 and the exact SHA in the Canvas comment.

- GPU evidence: actual Godot Visual Profiler recordings, connected to the same game through a reproducible test fixture on Mobile/Vulkan. See evidence/assignment-6/cost/visual-profiler-r2/README.md. Compatibility remains the shipped renderer.
- Shader study: restored color-ramp and scale-curve texture bindings; unchanged generated shader; isolated CPU/GPU rendered comparison and 21 configuration assertions. See evidence/assignment-6/shader-study-fixed/README.md.
- Validation: all eight suites passed, 313 assertions, zero failures. Shutdown resource-cleanup warnings remain in the raw logs under evidence/assignment-6/revision-2-validation/.

No gameplay code, production effect scene, project setting, source texture or generated shader changed from a6. The original film therefore still shows the submitted gameplay; only the isolated study, test fixtures, reports and evidence were supplemented. New fixture generation, resource repair and capture work in this supplement were performed by Codex. No new student play verdict or shader explanation is attributed to the student.
