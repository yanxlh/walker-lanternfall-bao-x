# Final particle cost comparison — 29 October 2026

## Setup

Godot 4.7.2.stable.official.ed1daf0bf on Apple M4, macOS 26.6.2. The same unchanged game source and cost script were run headlessly, in windowed Compatibility, and with a command-line Mobile/Vulkan override. Project settings were not edited. Each ordinary condition used three interleaved trials of 300 measured frames after 30 warm-up frames. Celebration used six trials of 38 frames after two warm-up frames. No other Godot test workload ran concurrently with the windowed measurements.

The off fixture removes the particle presentation before starting; the on fixture keeps it. Gameplay fixtures otherwise match. A attempts 40 hits and reaches the cap of 32 simultaneous bursts (512 particles). B holds movement input. Celebration reaches its cap of four bursts on the upgrade-card screen. The empty scene is the CPU control.

## Headless CPU comparison

Values are averages of the three trial means, with trial-to-trial range of those means. They measure whole-frame CPU work in an unthrottled fixed-rate simulation, not GPU work.

| Condition | Off mean (ms) | Off trial range | On mean (ms) | On trial range | Delta (ms) | CPU budget (ms) |
|---|---:|---:|---:|---:|---:|---:|
| Idle control | 0.0296 | 0.0290–0.0305 | 0.0318 | 0.0307–0.0326 | +0.0022 | control |
| A: hit sparks | 0.0844 | 0.0828–0.0853 | 0.1065 | 0.1055–0.1077 | +0.0222 | 1.0 |
| B: movement trail | 0.0299 | 0.0295–0.0306 | 0.0329 | 0.0325–0.0333 | +0.0030 | 0.25 |
| Upgrade celebration | 0.0489 | 0.0459–0.0510 | 0.0559 | 0.0537–0.0583 | +0.0070 | 0.4 |

Empty-scene CPU control: 0.0043 ms/frame. All measured CPU deltas are within the predeclared CPU budgets.

## Windowed GPU comparison

GPU values come from RenderingServer.viewport_get_measured_render_time_gpu on the root viewport. These are GPU timestamps, not FPS or CPU durations. The readable run used Mobile/Vulkan (MoltenVK); the shipped project renderer remains Compatibility.

| Effect | Off GPU mean (ms) | Off trial range | On GPU mean (ms) | On trial range | Delta (ms) | GPU budget (ms) |
|---|---:|---:|---:|---:|---:|---:|
| A: hit sparks | 0.7248 | 0.5113–0.8397 | 1.2640 | 0.5725–1.6489 | +0.5392 | 0.75 |
| B: movement trail | 0.4675 | 0.4337–0.4854 | 0.5752 | 0.4065–0.8588 | +0.1077 | 0.25 |
| Upgrade celebration | 0.9507 | 0.6676–1.4094 | 1.8610 | 0.9662–2.3437 | +0.9103 | 0.4 |

A and B remain below their GPU budgets in this Mobile/Vulkan rerun. The extra upgrade celebration exceeds its 0.4 ms budget: measured mean delta +0.9103 ms. Its broad trial spread means the magnitude should be treated cautiously, but the measured overrun is not marked as a pass. No effect settings were changed during final preparation, so the game still matches the approved film. A negative delta represents measurement variation, not a claim that particles save GPU time. The raw JSON includes per-trial sample standard deviations, medians, p95 values, and the subset of A frames actually at the burst cap.

Compatibility returned 0.000 ms in every GPU condition. Those readings are not used as GPU-cost estimates. The positive GPU readings above identify the tested renderer explicitly and do not establish the cost of the Compatibility renderer. Vsync-limited frame durations are not used to infer GPU cost. This rerun uses the viewport timing API; the separately saved editor Visual Profiler screenshot remains the earlier Compatibility check.

## Evidence

Raw outputs and exact commands: final-comparison/headless.json, compatibility.json, mobile-vulkan.json, matching logs, and commands.json. Configuration, state and regression results: ../final-validation/. The source revision recorded in the JSON is the imported project-history head; the Godot source tree matches the filmed revision as checked in SOURCE-REVISION.md.
