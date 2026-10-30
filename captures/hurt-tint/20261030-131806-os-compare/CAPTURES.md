# Hurt tint controlled-value captures

- Engine 4.7.2-stable (official), renderer gl_compatibility (opengl3, Apple M4), revision `5636e5a`
- Input: scripted-input. Fixtures: test_no_spawn = true; simulation frozen with test_mode = true while capturing.
- Capture: viewport image after `frame_post_draw`, driver stopped, 1280x720 px.
- Self-check (hurt_amount 0.0 reproduces the stored texel colours): PASS

| File | Set | Read back | iframes | Modulate | Camera rot | Lamp (20,16) pixel | Lamp RGB | Coat (16,24) pixel | Coat RGB |
|---|---|---|---|---|---|---|---|---|---|
| `hurt-amount-0.0.png` | 0.0 | 0.0 | 0 | [1.0, 1.0, 1.0] | 0.0 | [649, 347] | [242, 184, 75] | [641, 363] | [46, 58, 89] |
| `hurt-amount-0.5.png` | 0.5 | 0.5 | 0 | [1.0, 1.0, 1.0] | 0.0 | [649, 347] | [249, 220, 37] | [641, 363] | [151, 157, 44] |
| `hurt-amount-1.0.png` | 1.0 | 1.0 | 0 | [1.0, 1.0, 1.0] | 0.0 | [649, 347] | [255, 255, 0] | [641, 363] | [255, 255, 0] |
| `hurt-amount-2.0.png` | 2.0 | 2.0 | 0 | [1.0, 1.0, 1.0] | 0.0 | [649, 347] | [255, 255, 0] | [641, 363] | [255, 255, 0] |

Measured values only; the comparison with the hand-computed table and any verdict belong to Bao.

## In-engine capture vs OS screenshot of the same frame (hurt_amount 0.5, white phase)

- Held frame: driver stopped at 0.5, window moved to (80, 80) px; content rect [80, 130] px, [1280, 720] px; screen scale 2.0.
- OS screenshot: `screencapture -x -o -R40,65,640,360` (points) -> `os-screenshot.png`, 1280 x 720 px at 144 dpi, so 1 OS pixel per Godot pixel. Embedded profile (`sips -g profile`): Display P3. The in-engine `hold-hurt-amount-0.5.png` is tagged sRGB IEC61966-2.1.
- Whole-frame mean absolute difference (R, G, B): 0.87, 0.11, 1.74; maximum 26, 27, 45. The OS image shows the game window, not wallpaper.

| Texel | In-engine RGB | OS RGB | OS - in-engine |
|---|---|---|---|
| lamp (20,16) at pixel [649, 347] | (249, 220, 37) | (244, 221, 82) | (-5, 1, 45) |
| coat (16,24) at pixel [641, 363] | (151, 157, 44) | (152, 157, 65) | (1, 0, 21) |

Each value is the same across the texel's 2 x 2 pixel block in both images. Commands: `commands.txt`. Measured values only; which image to trust is Bao's call.
