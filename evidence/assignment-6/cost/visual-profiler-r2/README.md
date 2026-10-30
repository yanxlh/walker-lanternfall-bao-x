# Editor Visual Profiler measurements (revision 2)

Actual windowed game processes were connected to Godot 4.7.2's editor debugger on Apple M4 / macOS 26.6.2. Each capture was started and stopped with the Visual Profiler buttons, with more than ten seconds of collection. CPU and GPU columns contain real millisecond values. The game window was not minimized. Renderer: Mobile; driver: Vulkan via MoltenVK. Both were command-line overrides; project.godot remains byte-identical to a6. This supplements the earlier scripted measurements and the preserved all-zero Compatibility screenshot. It does not make Compatibility timings available.

The isolated `visual_profiler_fixture.tscn` loads the actual Session, sends Enter, and uses unchanged production effects. `acap` supplies 40 stationary durable enemies and beam pierce 40 to exercise the 32-burst overlap cap on repeated weapon hits. `move` alternates actual A/D input every 90 frames. Off removes the presentation controller; on retains it. The fixture is never loaded by the main game. The table below transcribes the top-level **Render Viewports** row of the stopped screenshots. These are selected frames, not whole-run averages or an isolated particle-only timer.

| Capture | Frame | CPU ms | GPU ms |
|---|---:|---:|---:|
| A off, a-off.png | 15743 | 0.08 | 0.58 |
| A on, a-on.png | 1599 | 0.10 | 8.32 |
| A on, a-on-frame1200.png | 1200 | 0.08 | 0.68 |
| B off, b-off.png | 2988 | 0.06 | 0.50 |
| B on, b-on.png | 2484 | 0.07 | 0.68 |

The stopped-frame differences are A +7.74 ms GPU / +0.02 ms render CPU, and B +0.18 ms GPU / +0.01 ms render CPU. A's capture contains a large spike: the retained mid-recording frame reads 0.68 ms GPU. Neither that lower frame nor the spike alone establishes A's typical cost or budget compliance. The graph visibly varies; these screenshots establish a functioning editor GPU measurement path and off/on comparisons. Keep the interleaved multi-trial measurements in `../FINAL-COMPARISON.md` for the separate statistical comparison. CPU here is render-thread work, not total game-frame CPU. Do not add nested GPU rows; they overlap. The exact live-burst count was not recorded alongside each selected profiler frame, so the A screenshot is a cap-exercising workload, not proof of 32 live bursts at that exact selected frame.

Reproduce with a Godot editor open, determine its debugger port, and run:

```sh
/Applications/Godot.app/Contents/MacOS/Godot --path godot --rendering-method mobile --rendering-driver vulkan --remote-debug tcp://127.0.0.1:6007 --position 0,0 --resolution 640x360 res://previews/visual_profiler_fixture.tscn -- --condition acap
```

Add `--effects-on` for on; replace `acap` with `move` for B. Wait for a disconnected process to leave the editor before reconnecting. Select the connected debugger session, Visual Profiler, Start, collect at least ten seconds, then Stop. Keep all window/render conditions matched.

Logs identify each renderer/condition. `a-off-clean.log` is the corrected A-off capture; `a-off.log` preserves an earlier rejected SceneTree-script attempt with initialization errors and is not measurement evidence. `b-on.log` was an unsuccessful editor reconnection; `b-on-reconnected.log` accompanies the retained B-on screenshot. The debugger's yellow warning count is retained in screenshots; no clean-warning claim is made.
