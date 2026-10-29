# Particle cost measurements — 29 October 2026

## Environment

- Machine: Apple M4 (CPU and GPU), macOS 26.6.2, built-in display (vsync 120 Hz under Compatibility, 60 Hz under the Vulkan run).
- Engine: Godot 4.7.2.stable.official.ed1daf0bf. Project renderer: GL Compatibility (OpenGL 4.1 on Metal).
- Source: commit `ec024c5` plus the uncommitted A6 working tree. Measured file hashes (SHA-256):
  - `godot/effects/defeat_sparks.tscn` `dc431c0d16f3618f99809931f836f62d10f9a2a1e0c650d4a5141709615db797` (kept r1, `scale_amount_max` 1.8)
  - `godot/effects/lantern_trail.tscn` `7085f05a074160ccc2918e6ddea8bec5c7b75652ac89a2cd225338ea5f20e075`
  - `godot/effects/level_up_sparks.tscn` `c044281a962a1585500ff1319068957d53a4b0f70573286835b0b050d679a584`
  - `godot/effects/level_up_overlay.tscn` `d3a82e798a874abbf144b44ad5ad7d15939932c961fd880d5ef7b9b715865a7e`
  - `godot/effects/particle_presentation.gd` `9234e70b1fadf3f1e3c9ee6a5cce7667b0e68b2a0fd69bcdf65fa8261238b475`
  - `godot/tests/cost_effects.gd` `468fa8d43122bbfecaf83b951c0dd03b57e615768fc4d9187db44071e341b274`

The headless and Compatibility windowed runs used `cost_effects.gd` before the `--trials` option and the renderer/driver metadata fields were added. The measurement code was otherwise identical. The hash above is the version used for the Metal probe and the Vulkan run.

## Method

`godot/tests/cost_effects.gd` runs nine conditions on fresh Sessions. "On" keeps the particle presentation. "Off" frees it before the run starts, which disconnects its signals, so gameplay, enemies and input are otherwise identical. Conditions are interleaved over 5 trials of 300 frames after 30 warm-up frames. The celebration runs 10 trials of 38 frames, because its four bursts live 0.7 s.

| Condition | Fixture |
|---|---|
| empty | a bare Node2D, no game |
| idle | game running, courier still, no enemies |
| acap | stress fixture from the state test: 40 pinned wraiths, beam pierce 40. Every volley gives 40 hits, of which 32 bursts are accepted (512 particles). Bursts are at the cap on 188 of 300 frames. |
| move | courier moving right under a held D key; trail emitting on all 300 frames |
| celebration | one real pickup worth six levels; four celebrations live on the card screen |

CPU: wall time between consecutive frames in a headless run with `--fixed-fps 60`. The loop is unthrottled with a dummy renderer, so this is the CPU cost of a whole frame: physics, process and particle simulation, but no real draw submission. `Performance.TIME_PROCESS` read 0 under this script main loop and was not used.

GPU: `RenderingServer.viewport_get_measured_render_time_gpu` on the root viewport in windowed runs. This is the source the editor's Visual Profiler reads.

## CPU results (headless)

Means over 5 trials (10 for the celebration). ± is the standard deviation of trial means.

| Condition | Off (ms/frame) | On (ms/frame) | Delta | Prediction | Budget |
|---|---:|---:|---:|---|---|
| empty control | 0.0043 ± 0.0001 | — | — | — | — |
| idle | 0.0287 ± 0.0011 | 0.0299 ± 0.0013 | +0.001 (within noise) | — | — |
| A at cap, whole volley cycle | 0.0813 ± 0.0021 | 0.1059 ± 0.0019 | +0.025 | < 0.8 | ≤ 1.0 |
| A, frames with 32 live bursts | 0.0813 (off, all frames) | 0.0900 ± 0.0019 | +0.009 | | |
| A spawn spike (p95 of frames) | 0.13 | 0.23–0.25 | about +0.10 | | |
| B continuous movement | 0.0288 ± 0.0010 | 0.0324 ± 0.0007 | +0.004 | < 0.15 | ≤ 0.25 |
| Celebration at cap (4) | 0.0446 ± 0.0012 | 0.0533 ± 0.0018 | +0.009 | < 0.25 | ≤ 0.4 |

At cap, most of A's CPU cost falls on the frames where 32 bursts are instanced at once. Simulating 32 live bursts adds about 0.009 ms per frame. Every CPU delta is one to two orders of magnitude under its prediction and budget.

## GPU results

| Renderer / driver | GPU time readable? | Result |
|---|---|---|
| GL Compatibility (project renderer), OpenGL 4.1 on Metal | No | 0.000 ms on every frame of every condition. Movie Maker captures also report "GPU render time: 0.00", and the editor's Visual Profiler shows 0.0 ms for every GPU entry (`visual-profiler-compatibility.png`). The windowed render-CPU timing is noisy and repeats a stale 0.372 ms in several trials, so it is not used. |
| Mobile, Metal (command-line override) | No | 0.000 ms on every frame (1-trial probe, `probe_mobile_metal_1trial.json`). |
| Mobile, Vulkan via MoltenVK (command-line override) | Yes | Values below. |

The proxy run used `--rendering-method mobile --rendering-driver vulkan`. The project settings were not changed. Values are the median of per-trial medians; outlier frames near 1.6 ms appear in several "off" trials.

| Condition | Off GPU (ms) | On GPU (ms) | Median delta | Budget |
|---|---:|---:|---:|---|
| empty control | 0.217 | — | — | — |
| idle | 0.478 | 0.497 | +0.02 | — |
| A, 32 live bursts | 0.424 | 0.434 | +0.01 | ≤ 0.75 |
| B continuous movement | 0.475 | 0.423 | −0.05 | ≤ 0.25 |
| Celebration at cap | 0.699 | 0.785 | +0.09 | ≤ 0.4 |

Every GPU delta lies within the run-to-run spread of about ±0.1 ms. B's negative delta is noise, not a saving. The effects' GPU cost is not resolvable on this machine with this method. It is below about 0.1 ms per frame on the proxy renderer, and no measurement approaches a budget.

## Limits

- The project renderer exposes no GPU timing on this Mac. The GPU figures come from a different renderer and driver (Mobile, Vulkan/MoltenVK) running the same scenes. They are a proxy for the shipped Compatibility renderer, not a measurement of it.
- Neither FPS nor CPU time is presented as GPU time. Windowed frame times are vsync-limited (8.33 ms at 120 Hz, 16.67 ms at 60 Hz) and carry no cost information.
- Headless CPU numbers exclude real draw submission.
- Editor check: the student ran the project from the Godot 4.7.2 editor and recorded the Visual Profiler (`visual-profiler-compatibility.png`, frame 3743, "CPU: Apple M4 / GPU: Apple M4"). Every GPU entry reads 0.0 ms: Frame Begin, Prepare Render, Render Viewport, Render View, Cull 2D, each Render Canvas and its Cull/Render children. The CPU entries have values (Render Viewport 3.11 ms, Render Canvas 1.85 / 0.38 / 0.8 / 0.22 ms), and the frame graph sits at the 16.67 ms vsync line. This confirms in the editor that GPU time is not measurable under GL Compatibility on this Mac, so no off/on GPU comparison was possible there.

## Files

`cost_effects_headless.json`, `cost_effects_windowed.json` (Compatibility), `cost_effects_windowed_mobile_vulkan.json`, `probe_mobile_metal_1trial.json`, and the matching `cost-*.log` files.
