# A5 hint captures

- Engine 4.7.2-stable (official), renderer gl_compatibility (opengl3, Apple M4), revision `d01df00`
- Input: scripted (no human input; parameters set in memory, never saved).
- Capture: viewport image after `frame_post_draw`, window 1280x720, visible rect 640x360.

| Quad | use_color | Left band | Middle band | Right band |
|---|---|---|---|---|
| QuadWithSourceColor | true | [64, 64, 64] at [200, 360] | [128, 128, 128] at [360, 360] | [192, 192, 192] at [520, 360] |
| QuadWithoutHint | false | [64, 64, 64] at [760, 360] | [128, 128, 128] at [920, 360] | [192, 192, 192] at [1080, 360] |

Measured values only; comparisons with the brief's predictions and any verdict belong to Bao.
