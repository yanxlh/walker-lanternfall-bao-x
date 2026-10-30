# Cobblestone Floor 08 — provenance

| Field | Value |
|---|---|
| Asset | Cobblestone Floor 08, https://polyhaven.com/a/cobblestone_floor_08 |
| Author and role | Rob Tuytel, all maps (Poly Haven API `authors`: "All") |
| Licence | CC0, https://polyhaven.com/license (attribution appreciated, not required) |
| Licence checked | 30 October 2026, by Bao (`CHANGE-BRIEF.md`, 3D material plan) |
| Downloaded | 30 October 2026, 1K PNG maps from `https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/cobblestone_floor_08/` |
| Normal convention | OpenGL (`_nor_gl`) is the one materials use; Godot expects OpenGL. `_nor_dx` is kept only to calibrate `godot/tests/normal_map_check.gd`. |

| File | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `cobblestone_floor_08_diff_1k.png` | 1951481 | `b59d5660021f7adfc303b2924f5351aa80c5c36fc73fe378a204f7f739602b0a` | colour, sampled with `source_color` |
| `cobblestone_floor_08_nor_gl_1k.png` | 2126688 | `0a6d3f1205c76ce64b01d04f22b570d239fd82b24df3be29791451f741ee4abb` | tangent-space normal (GL), `hint_normal` |
| `cobblestone_floor_08_rough_1k.png` | 627072 | `c44f6bc7b7280c36fe51c7c892d8413b09b61ae929df2169642e6c227429c93e` | roughness data, no `source_color` |
| `cobblestone_floor_08_nor_dx_1k.png` | 2126021 | `2879bd7d6d2d93c6a8ecefdab3c4582b988265898d7801b1a6bd526ac600ec86` | DirectX normal, calibration only |

Import settings are set by `tools/a5/set_texture_imports.py` on the `.import` files Godot generated.
