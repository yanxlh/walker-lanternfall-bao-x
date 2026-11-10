# Current r2 verification

## Current r2 validation and cost evidence

Nine suites were run using `bash scripts/run-test.sh <suite> <mode>` on an imported copy of the current source. Modes: audio `realtime`; every other suite `60`. Counts: logic 32, gameplay 65, audio 25, A configuration 40, extra configuration 81, particle state 34, edges 18, shader-study configuration 21, whole-tree pause 11. Total: **327 assertions, zero failures**. Both deliberate A mutations exited **1**, and the scene was restored byte-for-byte before the final passing A configuration run. Original assertions were retained.

The current original brief and dated revisions are retained. Initial particle brief/wrapper commit: `04ef18a`; event-design update: `6d88e4b`; later A r2 approval/test/change/comparison/decision: `f55159e`, `7439dda`, `389c369`, `39f8943`, `c6e6343`. The current supplemental explanation is separate from those original records.

### Reproduced CPU cost

Command: `bash scripts/run-test.sh cost_effects.gd 60 300`. The retained serial run took place after the windowed GPU workload had exited; concurrent exploratory output is not used here. Godot 4.7.2, Apple M4, macOS 26.6.2, headless, five interleaved trials of 300 frames after 30 warm-up frames (celebration: ten short trials of 38 frames). The empty-scene control is 0.004647 ms/frame. All times below are ms/frame.

| Condition | CPU off mean (trial range) | CPU on mean (trial range) | Delta | Budget |
|---|---:|---:|---:|---:|
| Idle game | 0.031918 (0.029203–0.038263) | 0.032721 (0.031303–0.035563) | +0.000803 | — |
| A r2, cap 32 | 0.085517 (0.083377–0.087763) | 0.183205 (0.106723–0.453600) | +0.097687 | 1.0 |
| B, continuous movement | 0.045263 (0.029323–0.099813) | 0.038083 (0.032807–0.051003) | -0.007179 | 0.25 |
| Celebration, cap 4 | 0.053516 (0.045211–0.077263) | 0.062542 (0.053158–0.078132) | +0.009026 | 0.4 |

A's positive delta is below its 1.0 ms CPU budget; celebration is below 0.4 ms. B's negative delta does not mean particles save CPU time: off/on trial ranges overlap substantially, so its incremental cost is not resolved by this run. Earlier reported r2 screenshots show +0.0068 ms, below 0.25 ms. Keep both results rather than selecting a favorable one. The current original logs and per-trial JSON are archived here, closing the previous absence of raw logs for a reproduced current-source run; they do not retroactively supply the raw logs of the earlier screenshot run.

### Reproduced windowed GPU timer

Command: `Godot --path <copied-godot> --rendering-method mobile --rendering-driver vulkan --fixed-fps 60 --script res://tests/cost_effects.gd -- --out <gpu-r2.json> --rev c6e6343-plus-coverage-tests --trials 5`. Renderer overrides do not edit project settings. GPU values below come from RenderingServer viewport timestamps on the Apple M4, not CPU durations or FPS.

| Condition | GPU off mean (trial range) | GPU on mean (trial range) | Delta | Budget |
|---|---:|---:|---:|---:|
| A r2 | 0.833148 (0.403693–1.082033) | 0.776605 (0.642473–1.047647) | -0.056543 | 0.75 |
| B | 0.878415 (0.246000–3.095000) | 0.685109 (0.249000–2.043000) | -0.193306 | 0.25 |
| Celebration | 0.596518 (0.373474–1.169711) | 0.606526 (0.449632–0.823316) | +0.010008 | 0.4 |

Negative A/B deltas and broad trial spread make this run inconclusive for incremental GPU cost. Do not count it as evidence that A/B are free or that their r2 GPU budgets have been reverified. The extra celebration's small delta here does not erase the earlier +0.910 ms over-budget result. These current measurements are viewport-timer results, **not new editor Visual Profiler captures**. Existing editor captures remain historical. The newer screenshot supplied by the student reports r2 A GPU deltas +0.17 to +0.39 ms within 0.75 ms, but its raw data and exact command have not been supplied. The screenshot is supplementary evidence, not a replacement for those missing records.

### Reproduction and identity

Raw stdout, engine logs, nine suite JSON files, mutation exit codes, `cpu-r2.json`, and `gpu-r2.json` are archived with this file. `source-sha256.json` identifies the exact copied Godot files; it is more precise than the benchmark's descriptive revision label. The headless wrapper leaves `source_revision=unknown` in the cost JSON, so that value is not silently replaced. Original automatic UTC timestamps are retained. Exit codes for the nine suites are in `exit-codes.json`; all are zero. CPU wrapper and GPU process also exited zero. Existing resource-at-exit warnings remain; no warning-free claim is made. These tests and measurements do not add new human observations.
