# Current Effect A r2 — editor Visual Profiler screenshots

## What was captured

Actual Godot 4.7.2 editor Visual Profiler recordings were started and stopped through its UI. Screenshots were saved with **Editor → Take Screenshot**, then inspected from the original PNGs. The computer-use preview lagged behind the actual tab; the retained native screenshots show the real profiler. Images have not been edited. Device: Apple M4, macOS 26.6.2. Runtime renderer: Mobile with Vulkan/MoltenVK overrides; the shipped project remains GL Compatibility. These are proxy-renderer results, not Compatibility GPU costs.

The existing `res://previews/visual_profiler_fixture.tscn` loads the current Session and production r2 hit-spark scene. `acap` supplies forty durable stationary enemies and a high-pierce beam to exercise the 32-burst cap. `move` alternates real A/D input. Off frees the presentation controller; on keeps it. The precise number of live bursts at each selected profiler frame was not captured, so the screenshots show a cap-exercising workload rather than proving 32 live bursts at that exact frame.

The initial game window was at (0,0), with an editor window covering much of the screen. Two B-off captures saved no profiler data and are explicitly rejected. A later layout put the editor at the left and the runtime at (800,50), with the runtime resolution set to 640×360 in both off/on conditions. Those fixture dimensions are separate from the project's 1280×720 human-play window. No game settings or effect resources were changed for these runs. No viewport-timer cost script ran concurrently, but other desktop applications were not closed or controlled.

## Readings from the saved screenshots

Use the top-level **Render Viewports** row, not a sum of nested rows. Values are selected-frame readings, not means, medians, or isolated particle times.

| Capture | Profiler frame | Render CPU ms | GPU ms | Context |
|---|---:|---:|---:|---|
| a-off-initial.png | 260 | 0.15 | 0.95 | initial layout |
| a-on-initial.png | 2621 | 0.25 | 1.64 | initial layout |
| b-on-before-layout-change.png | 1145 | 0.13 | 4.33 | initial layout; not paired with an empty off capture |
| b-off-after-layout-change.png | 930 | 0.06 | 0.49 | after editor resize, before runtime repositioning |
| b-off-visible.png | 355 | 0.13 | 1.91 | final matched window setup |
| b-on-visible.png | 548 | 0.07 | 0.51 | final matched window setup |
| a-off-visible.png | 715 | 0.30 | 0.62 | final matched window setup |
| a-on-visible.png | 782 | 0.61 | 5.21 | final matched window setup |

A's initial selected-frame difference is +0.69 ms, below its 0.75 ms GPU budget. Its later selected-frame difference is +4.59 ms, above budget. B's final selected-frame difference is -1.40 ms, which does not establish a speed benefit or a reliable incremental cost. The graphs visibly vary. Neither selecting the low A reading nor selecting the high reading alone establishes typical cost; the high reading must remain visible in the record. The sampled budget conclusion is explicit: A did not consistently meet its 0.75 ms budget (one pass, one exceedance). B did not exceed its 0.25 ms budget in the recorded negative-difference sample, with no performance benefit inferred. The earlier viewport-timer run was also noisy; its raw results remain in `../../current-r2-validation/`.

## Capture procedure and duration

The editor was launched with `--editor --accessibility always --debug-server tcp://127.0.0.1:6017 --rendering-method mobile --rendering-driver vulkan` against the imported temporary current-source copy. It used a renamed local copy of the installed Godot application solely to separate its identity from an already-open game window; the version is still 4.7.2. The first failed remote connection on port 6007 and early empty captures are troubleshooting attempts, not valid prices.

Runtime command, final setup:

```
/Applications/Godot.app/Contents/MacOS/Godot --path <current-copy>/godot --rendering-method mobile --rendering-driver vulkan --remote-debug tcp://127.0.0.1:6017 --position 800,50 --resolution 640x360 --log-file <condition-engine.log> res://previews/visual_profiler_fixture.tscn -- --condition acap
```

Add `--effects-on` for A on; replace `acap` with `move` for B. The stdout logs identify each condition and renderer. Old samples were cleared before each new recording. Successful A/B on recordings and final visible off recordings each included at least twelve seconds of intentional collection before stopping; measured UI intervals where available were about 20–27 seconds. A-off initial was left recording during the longer UI investigation. The two rejected B-off images have frame zero and no GPU rows and are never used as measurements.

Eight debugger issues are visibly retained in the screenshot badge; no warning-free claim is made. The runtime stdout logs identify renderer/condition and show no SCRIPT ERROR or SHADER ERROR. The original logs, including failed connection attempts, are kept rather than rewritten. Current source identity is the copied-source hash manifest in `../../current-r2-validation/source-sha256.json`; the profiler fixture copy is preserved alongside these images.

This supplies current r2 editor off/on screenshots for A and B. It does not supply a new celebration profiler run, establish an average GPU budget pass, measure vsync-off FPS, or replace the student's visual observations.
