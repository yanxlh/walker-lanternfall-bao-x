# A5 sweep captures

- Engine 4.7.2-stable (official), renderer gl_compatibility (opengl3, Apple M4), revision `4246f94`
- Input: scripted (no human input; parameters set in memory, never saved).
- Capture: viewport image after `frame_post_draw`, window 1280x720, visible rect 640x360.
- Pose: camera at [-0.60000002384186, 1.89999997615814, 5.19999980926514] looking at [-2.79999995231628, 0.34999999403954, 1.29999995231628]; floor rectangle [682, 496, 56, 56] px around [-1.39999997615814, 0.0, 2.90000009536743]; stand-in rectangle [563, 316, 16, 32] px around [-3.5, 0.60000002384186, 1.5].

| File | Setting | Floor mean RGB | Stand-in mean RGB |
|---|---|---|---|
| `sweep-uv_scale-0.25.png` | { "uv_scale": "0.25", "is_material_value": false } | [91.22, 85.0, 112.25] | [31.42, 40.97, 74.83] |
| `sweep-uv_scale-2.00.png` | { "uv_scale": "2.0", "is_material_value": true } | [100.5, 91.25, 115.7] | [31.42, 40.97, 74.83] |
| `sweep-uv_scale-4.00.png` | { "uv_scale": "4.0", "is_material_value": false } | [93.08, 85.82, 110.25] | [31.42, 40.97, 74.83] |
| `sweep-roughness_min-0.00.png` | { "roughness_min": "0.0", "is_material_value": false } | [106.67, 90.91, 113.48] | [31.42, 40.97, 74.83] |
| `sweep-roughness_min-0.55.png` | { "roughness_min": "0.55", "is_material_value": true } | [100.5, 91.25, 115.7] | [31.42, 40.97, 74.83] |
| `sweep-roughness_min-1.00.png` | { "roughness_min": "1.0", "is_material_value": false } | [99.32, 91.32, 116.12] | [31.42, 40.97, 74.83] |
| `sweep-roughness_max-0.00.png` | { "roughness_max": "0.0", "is_material_value": false } | [114.23, 91.35, 111.79] | [31.42, 40.97, 74.83] |
| `sweep-roughness_max-0.95.png` | { "roughness_max": "0.95", "is_material_value": true } | [100.5, 91.25, 115.7] | [31.42, 40.97, 74.83] |
| `sweep-roughness_max-1.00.png` | { "roughness_max": "1.0", "is_material_value": false } | [100.28, 91.3, 115.85] | [31.42, 40.97, 74.83] |
| `sweep-normal_strength-0.00.png` | { "normal_strength": "0.0", "is_material_value": false } | [101.26, 92.19, 116.86] | [31.42, 40.97, 74.83] |
| `sweep-normal_strength-1.00.png` | { "normal_strength": "1.0", "is_material_value": true } | [100.5, 91.25, 115.7] | [31.42, 40.97, 74.83] |
| `sweep-normal_strength-2.00.png` | { "normal_strength": "2.0", "is_material_value": false } | [98.91, 89.48, 113.57] | [31.42, 40.97, 74.83] |
| `sweep-tint-1.00_0.92_0.80.png` | { "tint": "(1.0, 0.92, 0.8, 1.0)", "is_material_value": true } | [100.5, 91.25, 115.7] | [31.42, 40.97, 74.83] |
| `sweep-tint-1.00_1.00_1.00.png` | { "tint": "(1.0, 1.0, 1.0, 1.0)", "is_material_value": false } | [100.5, 99.11, 142.51] | [31.42, 40.97, 74.83] |
| `sweep-tint-0.00_0.00_0.00.png` | { "tint": "(0.0, 0.0, 0.0, 1.0)", "is_material_value": false } | [22.77, 15.81, 28.86] | [31.42, 40.97, 74.83] |

Measured values only; comparisons with the brief's predictions and any verdict belong to Bao.
