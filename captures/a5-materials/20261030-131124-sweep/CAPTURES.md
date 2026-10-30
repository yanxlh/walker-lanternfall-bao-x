# A5 sweep captures

- Engine 4.7.2-stable (official), renderer gl_compatibility (opengl3, Apple M4), revision `d01df00`
- Input: scripted (no human input; parameters set in memory, never saved).
- Capture: viewport image after `frame_post_draw`, window 1280x720, visible rect 640x360.
- Pose: camera at [-0.60000002384186, 1.89999997615814, 5.19999980926514] looking at [-2.79999995231628, 0.34999999403954, 1.29999995231628]; floor rectangle [682, 496, 56, 56] px around [-1.39999997615814, 0.0, 2.90000009536743]; stand-in rectangle [563, 316, 16, 32] px around [-3.5, 0.60000002384186, 1.5].

| File | Setting | Floor mean RGB | Stand-in mean RGB |
|---|---|---|---|
| `sweep-uv_scale-0.25.png` | { "uv_scale": "0.25", "is_material_value": false } | [89.66, 81.87, 108.15] | [31.63, 40.98, 74.74] |
| `sweep-uv_scale-2.00.png` | { "uv_scale": "2.0", "is_material_value": true } | [99.76, 90.44, 114.73] | [31.63, 40.98, 74.74] |
| `sweep-uv_scale-4.00.png` | { "uv_scale": "4.0", "is_material_value": false } | [91.8, 84.2, 108.26] | [31.63, 40.98, 74.74] |
| `sweep-roughness_min-0.00.png` | { "roughness_min": "0.0", "is_material_value": false } | [104.6, 89.98, 112.56] | [31.63, 40.98, 74.74] |
| `sweep-roughness_min-0.55.png` | { "roughness_min": "0.55", "is_material_value": true } | [99.76, 90.44, 114.73] | [31.63, 40.98, 74.74] |
| `sweep-roughness_min-1.00.png` | { "roughness_min": "1.0", "is_material_value": false } | [98.67, 90.56, 115.22] | [31.63, 40.98, 74.74] |
| `sweep-roughness_max-0.00.png` | { "roughness_max": "0.0", "is_material_value": false } | [108.45, 89.77, 110.76] | [31.63, 40.98, 74.74] |
| `sweep-roughness_max-0.95.png` | { "roughness_max": "0.95", "is_material_value": true } | [99.76, 90.44, 114.73] | [31.63, 40.98, 74.74] |
| `sweep-roughness_max-1.00.png` | { "roughness_max": "1.0", "is_material_value": false } | [99.57, 90.49, 114.89] | [31.63, 40.98, 74.74] |
| `sweep-normal_strength-0.00.png` | { "normal_strength": "0.0", "is_material_value": false } | [101.26, 92.19, 116.86] | [31.63, 40.98, 74.74] |
| `sweep-normal_strength-1.00.png` | { "normal_strength": "1.0", "is_material_value": true } | [99.76, 90.44, 114.73] | [31.63, 40.98, 74.74] |
| `sweep-normal_strength-2.00.png` | { "normal_strength": "2.0", "is_material_value": false } | [96.9, 87.26, 110.9] | [31.63, 40.98, 74.74] |
| `sweep-tint-1.00_0.92_0.80.png` | { "tint": "(1.0, 0.92, 0.8, 1.0)", "is_material_value": true } | [99.76, 90.44, 114.73] | [31.63, 40.98, 74.74] |
| `sweep-tint-1.00_1.00_1.00.png` | { "tint": "(1.0, 1.0, 1.0, 1.0)", "is_material_value": false } | [99.76, 98.26, 141.34] | [31.63, 40.98, 74.74] |
| `sweep-tint-0.00_0.00_0.00.png` | { "tint": "(0.0, 0.0, 0.0, 1.0)", "is_material_value": false } | [22.37, 15.7, 28.71] | [31.63, 40.98, 74.74] |

Measured values only; comparisons with the brief's predictions and any verdict belong to Bao.
