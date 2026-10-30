# Hurt tint controlled-value captures

- Engine 4.7.2-stable (official), renderer gl_compatibility (opengl3, Apple M4), revision `a8c804b`
- Input: scripted-input. Fixtures: test_no_spawn = true; one wraith spawned 40 px right of the courier with hp 1000 so the beam cannot kill it; after its real hit it is freed and the simulation frozen with test_mode = true while capturing.
- Capture: viewport image after `frame_post_draw`, driver stopped, 1280x720 px.
- Red phase, hurt_amount 0.0 sampled vs stored x (1, 0.45, 0.45) rounded: lamp [242, 83, 33] vs [242, 83, 34], coat [46, 26, 40] vs [46, 26, 40]

| File | Set | Read back | iframes | Modulate | Camera rot | Lamp (20,16) pixel | Lamp RGB | Coat (16,24) pixel | Coat RGB |
|---|---|---|---|---|---|---|---|---|---|
| `hurt-amount-0.0.png` | 0.0 | 0.0 | 27 | [1.0, 0.44999998807907, 0.44999998807907] | 0.0 | [649, 347] | [242, 83, 33] | [641, 363] | [46, 26, 40] |
| `hurt-amount-0.5.png` | 0.5 | 0.5 | 27 | [1.0, 0.44999998807907, 0.44999998807907] | 0.0 | [649, 347] | [249, 169, 17] | [641, 363] | [151, 141, 20] |
| `hurt-amount-1.0.png` | 1.0 | 1.0 | 27 | [1.0, 0.44999998807907, 0.44999998807907] | 0.0 | [649, 347] | [255, 255, 0] | [641, 363] | [255, 255, 0] |

Measured values only; the comparison with the hand-computed table and any verdict belong to Bao.
