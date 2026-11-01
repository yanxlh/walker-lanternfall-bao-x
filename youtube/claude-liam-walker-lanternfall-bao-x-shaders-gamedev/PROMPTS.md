# PROMPTS

## B00 — the reconstructed Walker ask (on screen)

Reconstructed from Bao's CHANGE-BRIEF.md for the cold open; it is not a recorded session.

> Please use Walker to convert my game design document about Lanternfall, a lamp-headed courier surviving three minutes in a fog-bound night market, into two Godot 4 shaders: a yellow tint that shows his 48-tick protection after a hit, and a textured cobblestone material for the 3D room. Gameplay must not change. Predict every colour by hand first, then measure it in the engine.

The game description follows CONCEPT.md ("A lamp-headed courier is trapped in a fog-bound midnight market … survive three minutes"); the two shaders, the 48 ticks and "predict first" follow CHANGE-BRIEF.md.

## B29 — Your Turn (read aloud)

> Please use Walker to read godot/a5/materials/cobblestone_cool_standin.tres in my Lanternfall project. Change only uv_scale from 1.0 to 3.0. Before running anything, predict which rectangle of the pair capture changes, how the stand-in's stones change, and which check in test_materials.gd fails. Then capture the pair, compare it with your prediction, and put 1.0 back.

One bounded, material-only change with a prediction and a measurement. It tests the film's material-vs-shader claim from the other side (B12 changed the floor). `tests/test_materials.gd` line 47 expects the stand-in's `uv_scale` 1.0, so its material-values check fails until the value is restored; `tests/capture_a5_materials.gd --pair` (or `--one-material`, which edits the floor) provides the capture. The narration reads the prompt in full and says what it tests.

## The request that produced this film

On 2026-10-30 the coordinating session asked for Bao's Assignment 5 film: the godot-gamedev skill with the walker modifier on this repository, the Assignment 6 particle film package as template, a new real windowed gameplay capture of an enemy hitting the courier, the four questions answered at lines of Bao's code and kept consistent with LANGUAGE-NOTES.md, no edits under `godot/`, no commit, push or publication, and a native 4K landscape master. During the build the source revision moved from 61c9cbf to **4246f94** (Bao's hand edit of `cobblestone_surface.gdshader` line 22 and his completed LANGUAGE-NOTES.md); the coordinator named the material recaptures at that revision to use.
