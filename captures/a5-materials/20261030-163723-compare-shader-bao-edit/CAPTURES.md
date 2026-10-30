# A5 compare-shader captures

- Engine 4.7.2-stable (official), renderer gl_compatibility (opengl3, Apple M4), revision `e5c0272`
- Input: scripted (no human input; parameters set in memory, never saved).
- Capture: viewport image after `frame_post_draw`, window 1280x720, visible rect 640x360.
- Pose: camera at [-0.60000002384186, 1.89999997615814, 5.19999980926514] looking at [-2.79999995231628, 0.34999999403954, 1.29999995231628]; floor rectangle [682, 496, 56, 56] px around [-1.39999997615814, 0.0, 2.90000009536743]; stand-in rectangle [563, 316, 16, 32] px around [-3.5, 0.60000002384186, 1.5].

| File | Setting | Floor mean RGB | Stand-in mean RGB |
|---|---|---|---|
| `compare-shader-bao-edit.png` | {  } | [52.83, 46.55, 63.29] | [12.36, 16.99, 35.66] |

Measured values only; comparisons with the brief's predictions and any verdict belong to Bao.
