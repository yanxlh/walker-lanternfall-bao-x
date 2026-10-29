# Visual Profiler compatibility check

Date: 2026-10-29
Engine: Godot 4.7.2.stable.official.ed1daf0bf
Device: Apple M4
Renderer: Compatibility (OpenGL API 4.1 Metal)

Started the main game from the editor, pressed Enter, moved the player, and observed enemies, a weapon hit and movement particles. Returned to the editor by minimizing the separate game window. Started Visual Profiler and stopped after approximately 17 seconds (frame counter advanced from about 2695 to 3743). An upgrade-card transition was not verified during this capture. This is a compatibility check, not a controlled particle-cost benchmark; the game window was minimized during collection.

At stopped frame 3743, every listed GPU entry reads 0.0 ms; the GPU graph is empty. The CPU Render Viewports entry reads 3.11 ms; Frame Begin 0.06 ms; Prepare Rendering 0.07 ms. These are the displayed selected-frame readings, not recording-wide averages, and nested entries must not be added together.

The all-zero GPU values do not establish zero GPU cost. They show that this Compatibility session did not provide usable GPU timings in Visual Profiler.

Screenshot: visual-profiler-compatibility.png

No project settings were changed. project.godot SHA-256 before and after: 5d01ae07d7107498904a64a2ff7efead4502cfdd757bed3c7acf1ae79fc52051.
