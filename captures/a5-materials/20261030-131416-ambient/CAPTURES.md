# A5 ambient captures

- Engine 4.7.2-stable (official), renderer gl_compatibility (opengl3, Apple M4), revision `df44cdd`
- Input: scripted (no human input; parameters set in memory, never saved).
- Capture: viewport image after `frame_post_draw`, window 1280x720, visible rect 640x360.
- Pose: camera at [-0.60000002384186, 1.89999997615814, 5.19999980926514] looking at [-2.79999995231628, 0.34999999403954, 1.29999995231628]; floor rectangle [682, 496, 56, 56] px around [-1.39999997615814, 0.0, 2.90000009536743]; stand-in rectangle [563, 316, 16, 32] px around [-3.5, 0.60000002384186, 1.5].

| File | Setting | Floor mean RGB | Stand-in mean RGB |
|---|---|---|---|
| `ambient-source-3-as-loaded.png` | { "ambient_light_source": 3, "sky": false, "ambient_light_energy": 0.80000001192093 } | [99.76, 90.44, 114.73] | [31.63, 40.98, 74.74] |
| `ambient-source-2-color.png` | { "ambient_light_source": 2, "ambient_light_energy": 0.80000001192093 } | [99.76, 90.44, 114.73] | [31.63, 40.98, 74.74] |
| `ambient-source-1-disabled.png` | { "ambient_light_source": 1, "ambient_light_energy": 0.80000001192093 } | [96.85, 86.92, 109.84] | [27.7, 34.82, 63.02] |
| `ambient-source-2-color-energy-0.0.png` | { "ambient_light_source": 2, "ambient_light_energy": 0.0 } | [96.85, 86.92, 109.84] | [27.7, 34.82, 63.02] |
| `ambient-source-3-as-loaded-energy-0.0.png` | { "ambient_light_source": 3, "ambient_light_energy": 0.0 } | [96.85, 86.92, 109.84] | [27.7, 34.82, 63.02] |
| `ambient-source-3-as-loaded-energy-2.0.png` | { "ambient_light_source": 3, "ambient_light_energy": 2.0 } | [103.93, 95.43, 121.61] | [36.57, 48.4, 88.19] |

Measured values only; comparisons with the brief's predictions and any verdict belong to Bao.
