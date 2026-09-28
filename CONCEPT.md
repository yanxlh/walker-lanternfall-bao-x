# Lanternfall — Concept

`walker-lanternfall-bao-x` · Bao Xing · CSYE 7270 Assignment 2 · **v1 written 2026-09-28, before any generation**

> Frozen at tag `design-v1`. Later changes go under **Revisions** at the bottom; nothing above that line is rewritten.

## In two sentences

A lamp-headed courier is trapped in a fog-bound midnight market, and the light on his shoulders is his only weapon. Keep moving, grow the light, and survive three minutes until the fog lifts.

## Core loop

1. **Move** — the only thing the player does moment to moment (WASD / arrows / left stick).
2. **Weapons fire on their own** — the Beam shoots along the direction of travel; Lamp-Moths orbit the courier.
3. **Enemies break into lamp-oil gems**; walking near a gem pulls it into the satchel.
4. **A full oil gauge levels you up**: the run pauses and you pick 1 of 3 upgrade cards.
5. **The fog thickens** every 30 seconds — more moths, then fog-wraiths.
6. **Both weapons at level 3 → the Sunflare Lighthouse card appears**; taking it fuses them into one pulsing burst of light.
7. **Survive 3:00 to win, or lose all HP** — either way, R starts a fresh run instantly.

## Design pillars

1. **Light is power.** Everything that helps you is warm light; everything that hurts you is cool fog. Growing stronger literally makes the screen brighter around you.
2. **Feet, not fingers.** Movement is the only verb. Every real decision lives in the level-up cards: which weapon, which branch, when to take the evolution.
3. **Readable in silence.** Every event that has a sound also has a visual: hit flash, knockback, gem flight, pause-and-cards, banner, result panel. Sound adds feeling, never information you need.
4. **Three-minute runs.** A run is short, a loss costs nothing, retry is one key. The player should always want "one more".

## Systems in this slice

| System | Details |
|---|---|
| Beam | Starts at level 1. Branches: **Quick Wick** (fire 25 % faster) or **Long Wick** (+1 pierce). Max level 3. |
| Lamp-Moths | Unlocked by a card (2 moths). Branches: **Another Wing** (+1 moth) or **Wider Flight** (larger orbit). Max level 3. |
| Passives | Light Boots (speed), Magnet Satchel (pickup range), Thick Glass (max HP). Two levels each. |
| Evolution | Beam 3 + Moths 3 → **Sunflare Lighthouse**: both weapons are replaced by a radial light burst every 2 s; the courier's colours brighten; the music gains a layer. |
| Enemies | **Moth** — fast, fragile, 1 damage. **Fog-wraith** — slow, tough, 2 damage. |
| Pacing | Spawn density rises in six 30-second steps. |
| Health | 10 HP, 0.8 s of invulnerability after each hit, with knockback. |

## Art direction

- **View:** 3/4 top-down; camera follows the courier inside a bounded market square.
- **Form:** flat-vector shapes with a thick dark outline, reduced to small pixel sprites (courier 32 × 32) and locked to fixed palettes so every frame matches.
- **Warm vs cool:** the courier, his weapons and pickups use the warm character palette; enemies and the ground use the cool fog palette.
- **Value rule:** player and pickups are the brightest things on screen, enemies are mid-value, the ground is darkest. Readability is checked with muted play.

Character palette: `#F2B84B` lamp gold · `#FFF1C9` glow cream · `#2E3A59` coat navy · `#8A5A3C` satchel brown · `#14121C` outline ink.
Environment palette: `#0E1020` night · `#1F2540` deep fog · `#3B4A6B` mid fog · `#6E7FA3` light fog · `#C7D0E0` mist · `#F2B84B` lantern gold · `#B5523B` stall red · `#14121C` ink.

## Audio direction

- **Good events** (kill, pickup, level-up, evolution, win) are soft, warm and glassy — bells, chimes, small pops.
- **Harm** (hurt, lose) is dull, low and muffled — a thud, a guttering flame.
- **No harsh high transients**, because kills and pickups happen many times a minute; frequent sounds are short and throttled so they never machine-gun.

## Music: when it plays, changes and stops

| Moment | Music |
|---|---|
| Title menu | Silent (the fog is quiet until you step in). |
| Run starts / restarts | Night-market loop starts from the top; a second "Sunflare" layer runs silently in sync. |
| Level-up cards | Loop ducks by 6 dB so the choice feels like a held breath. |
| Pause | Loop keeps playing, muffled (low-pass) and 10 dB quieter. |
| Sunflare evolution | The Sunflare layer fades in over 2 s. |
| Lose | Loop fades out over 0.5 s, then the lose stinger. |
| Win (3:00) | Loop fades out over 1 s, then the win stinger. |

Mute: **M** all audio, **9** music only, **0** effects only. The game is fully playable muted.

## Semester goal (outside this slice)

More weapons and evolution recipes, a boss at the end of the fog, between-run progression, saving, and more than one market map.

## Starting point and tools

- Started from a **blank Godot 4.7.2 project**. The Lamp-Head Courier is carried over from my Assignment 1, [walker-jumpman-bao-x](https://github.com/yanxlh/walker-jumpman-bao-x), which extended [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman).
- This concept was worked out in a brainstorming session with Claude; the Walker `/gdd` skill was not used. The choices of genre, weapons, branching upgrades, evolution rule, theme, scope and local models were mine.

## Revisions

_None yet._
