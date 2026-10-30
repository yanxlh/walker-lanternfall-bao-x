# Hurt tint controlled-value captures

- Engine 4.7.2-stable (official), renderer gl_compatibility (opengl3, Apple M4), revision `2df4c4b`
- Input: scripted-input. Fixtures: test_no_spawn = true; simulation frozen with test_mode = true while capturing.
- Capture: viewport image after `frame_post_draw`, driver stopped, 1280x720 px.
- Self-check (hurt_amount 0.0 reproduces the stored texel colours): PASS

| File | Set | Read back | Lamp (20,16) pixel | Lamp RGB | Coat (16,24) pixel | Coat RGB |
|---|---|---|---|---|---|---|
| `hurt-amount-0.0.png` | 0.0 | 0.0 | [649, 347] | [242, 184, 75] | [641, 363] | [46, 58, 89] |
| `hurt-amount-0.5.png` | 0.5 | 0.5 | [649, 347] | [249, 220, 37] | [641, 363] | [151, 157, 44] |
| `hurt-amount-1.0.png` | 1.0 | 1.0 | [649, 347] | [255, 255, 0] | [641, 363] | [255, 255, 0] |
| `hurt-amount-2.0.png` | 2.0 | 2.0 | [649, 347] | [255, 255, 0] | [641, 363] | [255, 255, 0] |

Measured values only; the comparison with the hand-computed table and any verdict belong to Bao.
