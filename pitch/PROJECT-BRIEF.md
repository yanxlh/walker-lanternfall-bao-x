# Lanternfall: First Delivery — project brief

Bao Xing · CSYE 7270 Assignment 8 · 23 November 2026 · design source: my Assignment 4 GDD v0.3 (17 October 2026, [`gdd/`](gdd/GDD-v0.3.md))

Stack: Godot 4.7.2, GDScript, GL Compatibility renderer. Export target: a macOS desktop build (Apple Silicon), the platform I can run and check. Final project due 20 December 2026 (tag `a10`).

## 1. What is it?

Lanternfall: First Delivery will be a playable macOS desktop build of my Godot survivors-like, taken from a three-minute survival run to one complete delivery: a post office menu, one contract across the fog market, a delivery that ends at the Lantern Gate, and a second courier, the Engineer, who places turrets. It is the "next playable milestone" in my GDD's Development Scope, cut down by risk R-01.

## 2. Why would anyone care?

A run will be a delivery, not only a fight against a clock. When it succeeds, the destination changes, and the change is still there the next time you play (GDD PX-03, "a destination change the player can recognize on the next visit"). The Engineer changes the plan within the first thirty seconds (PX-02): you choose where the defence goes instead of only where you walk.

## 3. What makes it different?

I have played Vampire Survivors, Brotato, 20 Minutes Till Dawn and Halls of Torment. In Vampire Survivors a run's goal is to outlast the clock; in Brotato it is to outlast twenty waves. Lanternfall gives a player who likes short survivors-like runs a destination: each run is a delivery to a named place, and a successful one leaves that place visibly changed, saved across restarts.

## 4. Who opens it, and what do they do?

Target role: gameplay programmer. Reader: a hiring manager or a lead gameplay engineer. First sixty seconds: open the macOS build, land on the post office menu with keyboard focus already on the first courier, read the keys on that screen, press Enter, and be moving, with the Beam firing on its own, inside a minute. No manual to read first. Then the lead engineer runs the one test command at the top of the README. I do not yet know whether the macOS unsigned-app warning costs a stranger more than a minute; I will time it on a fresh macOS user account.

## 5. What does it prove about me?

That I can extend a working game with new systems — a delivery state, one saved record, a turret that runs on its own state machine — and pin each one with headless tests that a stranger reruns from a clean clone. Course skills with existing evidence: shaders and materials (`a5`), particle effects (`a6`), animation and state (`a7`), profiling (the A6 cost report), and the verification habits (pinned tests, mutations that the tests catch, human checks recorded separately, a `CLAUDE.md` that scopes the agent). What a reviewer cannot conclude: that the game is fun, or that the export runs on a machine I did not run it on.

## 6. In, out, first, and risk

- **In:** delivery objective and result (F-04); a keyboard-only post office menu as the front door; one contract; the Engineer with a turret (my planned Assignment 9 technique: a state machine with idle, track, fire and cooldown, hysteresis on the range, and a read-only mode tests read); one delivery record that survives a restart, under save rules written before any save code; the Lantern Gate from Assignment 3 lit after a delivery; the macOS export.
- **Out (deliberately):** the other four couriers in the GDD roster, a difficulty selector, more maps and the fog boss, any progression beyond that one record, multiplayer, web, mobile and XR.
- **First:** the delivery objective on the existing market route. My answer to the GDD's open question Q-01 for this slice: survive until the fog lifts, then reach the gate. Someone knows it ran when a seeded headless test drives a run to the delivered state and the result panel says so in a capture.
- **Risk (GDD R-03):** turrets add hits, and every hit can spawn A6's sparks, at the busiest minute of the run. On my Mac, Godot reports 0.0 ms GPU time under GL Compatibility (A6 cost report), so I cannot read GPU cost there. What I will do: cap active turrets, reuse turret shots, measure CPU frame time headless with the same method as `godot/tests/cost_effects.gd` at the peak wave with the cap reached, use the Vulkan proxy run for GPU, and cut turret sparks first if the frame goes over budget.

## 7. Why this project?

Both learning and showing what I have. New to me in this course: Godot and GDScript, shaders and materials, particle effects. Skills I already had: animation, state machines and testing; my evidence for them is tag `a7` (23 headless runs pass from a fresh clone; 8 of 8 mutations caught). The delivery, save and turret code will be new code in this game.

## Exists today

| Item | Where to see it |
|---|---|
| Three-minute survival run: movement, automatic Beam and Lamp-Moths, lamp-oil gems, three-card level-ups, Sunflare evolution, win and loss, one-key restart | since Assignment 2 (`8a6f988`); current at `a7` |
| Generated sprites, sound effects and music | Assignment 2 (`8a6f988`) |
| Lantern Gate, Supply Stack and Lamp-oil Shrine from Blender, in a separate 3D room (F4) | `a3` |
| GDD v0.3 with stable IDs, priorities, risks and open questions | Assignment 4 (17 October 2026), copied into `pitch/gdd/` at `a8` |
| Two hand-written shaders (`hurt_tint`, `cobblestone_surface`) and a material audit | `a5` |
| Hit sparks, movement trail and level-up celebration, with a CPU/GPU cost report | `a6`, `a6-r2` |
| Walk and dash animation driven by the courier's state; the dash card | `a7` |
| Headless test suites with a run script; 23 runs pass from a fresh clone | `a7` |
| An export | none yet; no `export_presets.cfg` exists |

## Will exist (by `a10`, 20 December 2026)

1. Delivery objective and result on the market route, with a pinned headless test (first).
2. A keyboard-only post office menu, focus set on load, choosing a courier and starting the one contract.
3. The Engineer courier and a capped turret on a state machine (Assignment 9 technique, planned).
4. One delivery record saved across restarts, with save rules for missing, corrupt, newer-version and unwritable files written first.
5. The Lantern Gate lit on the next visit after a delivery.
6. A turret load measurement at the peak wave, against a frame budget.
7. A macOS export: committed `export_presets.cfg`, an inspected `--export-pack`, the exported build run on my Mac; a clean clone of `a10` passes every documented check.

Drafted with Claude from my answers on 23 November 2026 and my A4 GDD; see SOURCES.md.
