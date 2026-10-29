# Windowed play checks — 29 October 2026

Command, run from the terminal:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --path godot --fixed-fps 60 --script res://tests/capture_play_checks.gd -- --out captures/play-checks/20261029-142138
```

Environment: Godot 4.7.2, GL Compatibility, Apple M4, 1280 × 720 window (640 × 360 viewport), audio muted. Kept effect settings: A `scale_amount_max` 1.8, B alpha 0.95/0.70/0, celebration at the UI portrait.

Each scene is a fresh `Session` with `test_no_spawn`. Fixtures place the courier, pin enemies (speed 0, high HP), drop gems, or set the clock for the win case. Hits come from the real beam; movement, pause, cards and restart come from parsed key events through the normal physics loop. The script never calls `damage()` or a particle trigger. `states.json` records effect state for every shot (state, trail emitting, speed scale, live burst counts, courier position) and trail emission for every frame.

These are recorded image readings from scripted play, not the student's running-game judgment. The items marked **human** below still need the student's own play.

## Readings

| Check | Shots | Reading |
|---|---|---|
| Upgrade celebration in real game | `upgrade-f01…f40`, `sheets/upgrade-portrait-1.5x.png` | A real gem pickup enters LEVELUP. Sparks burst white on the card-screen portrait (f01), turn yellow (f12), go orange and disperse around it (f24), and are gone by f40 (0.67 s). They draw above the dark veil and do not overlap the cards. After choosing card 1 none remain. |
| A on plain floor | `hit-dark-*` | Clearly visible as yellow-orange sparks over the dark wraith and floor at +08 frames. At +00/+03 the white core coincides with the enemy's own 3-tick hit flash (sprite modulated ×2.5, pale blue-white), so the core and the flash merge. |
| A on the brightest props | `hit-bright-cart-*`, `hit-bright-post-*`, `sheets/hit-cart-3x.png` | The level's brightest areas are small. The lantern heads and cart lamp are 3–19 px sprites with luminance up to 188–207; the floor tile peaks at 73. The light pool is a 0.07-alpha circle. A pinned enemy covers most of the prop, so the burst's background is mainly the enemy sprite plus the muted cart roof or light pool. Sparks stay distinct from +03 to +16. Predicted failure 6 (yellow lost on bright props) was not observed in this level. |
| B on plain floor | `trail-dark-move*` | A short, broken amber trail at the feet, about 26–29 px (0.8–0.9 courier heights) of visible flecks. Flecks are 2–4 screen px. The pinned wraith (30 px above the path), the moth and the gems are not overlapped. |
| B through a light pool | `trail-bright-move*` | Still readable against the slightly warmer pool, about 35 px long; flecks are not lost. |
| B stops | `trail-dark-stop+01…+22` | Spawning stops on the release frame. A few flecks remain at +06 (0.10 s), none behind the courier at +12 (0.20 s), within the 0.35 s limit. |
| B dimmer and smaller than A | `trail-dark-move45` vs `hit-dark-hit+08` | Trail flecks are 2–4 px dim amber; hit sparks are 6–11 px bright yellow-orange. Still holds after B's alpha revision. |
| Pushing into a stall | `blocked-*`, `states.json` | Holding D against the stall's left edge for 30 frames moved the courier 0.5 px: the fixture started 0.5 px from contact, and one trail frame was emitted for that first real step. No later frame moved or emitted. `blocked-push30` shows no trail. Sliding up with W emits normally. |
| Restart while moving | `restart-*` | R with D still held: the old trail disappears on the restart frame and a new short trail starts at the plaza centre. No line joins the old and new positions. |
| Pause | `pause-paused+01`, `+31` | Hit burst and trail freeze under the PAUSED veil; the two frames are pixel-identical. Resume continues both. |
| Hidden presentation | `pause-hidden+08`, `shown+08` | Hidden: no trail or burst drawn and no emission. Shown: the trail resumes while moving. In `shown+08` the red tint is the existing hurt overlay; the courier had walked into the pinned wraith. It is not a particle effect. |
| Card screen over live effects | `card-levelup+02`, `+32`, `chosen+04` | Between +02 and +32 only the portrait region changes (648 px; the celebration plays as specified). The hit burst and trail stay frozen and resume after the card is chosen. |
| Death | `death-lost+00`, `+30`, `restart+04` | Entering LOST clears hit bursts and the trail in the first LOST frame. R from LOST starts clean. |
| Victory | `win-won+00`, `+30` | Entering WON clears bursts and the trail. The camera's existing win zoom-out (0.97 at +30) shows no leftover particles. |

## Student's running-game verdict

After playing a normal run, the student replied “没有挡住都正常” (nothing is hidden; everything is normal). Recorded verdict: the trail does not hide enemies, pickups or the courier in ordinary play, and the effects behave normally through pause, card choice, death, victory and restart. The student made no separate comment on bright-prop visibility; the reading above remains the only record for that case.

## Files

- 56 PNG shots named `<scene>-<moment>.png`; `states.json`; labelled crops under `sheets/`; `SHA256SUMS`.
- Driver: `godot/tests/capture_play_checks.gd`. Headless edge assertions added alongside: `godot/tests/test_particles_edges.gd`.
