# RIFF — the judgments the narration makes, and what they rest on

Teardown register: describe the mechanism, then judge it. Every judgment points at something on screen in the same beat.

| Artifact · range | Visible observation | Judgment in the narration | Suggested next experiment |
|---|---|---|---|
| B05 · main take frames 2134–2688 | rings mark logged hits; bursts outlive dying moths; the live counter rises to several at once | overlapping, independent bursts are the point of instancing per hit | lower the cap to 4 and watch which hits go unmarked |
| B07 · r1 files 9–21 | white cluster → yellow-orange sparks → gone by 0.40 s | the burst follows the brief's three phases | none needed; the measurement is the check |
| B09 · r0/r1 sheets | chunkier sparks, same footprint, same fade frame | the prediction missed the footprint; the miss is kept, not hidden | predict the effect of raising `initial_velocity_max` the same way |
| B11 · props take | pushing into the stall: no embers; sliding: embers | displacement, not input, is the right trigger | try a teleport: the jump limit should eat one frame |
| B13 · trail fixture | brighter embers, same footprint and fade | an alpha-only change brightens without lengthening | the Your Turn radius change |
| B15 · main take, level 2 | burst on the card-screen portrait, gone before the pick | putting it on the portrait answers Bao's report | none; Bao accepted it |
| B17 · main take pause; play checks | paused frames identical; LOST/WON first frames empty | freeze, don't fake | — |
| B19 · recorded output | 292 / 0; guard removed → 2 failures; Godot 3 name loads silently | tests catch what a glance misses | rename another property and see whether a test notices |
| B21 · study capture | CPU fades and shrinks; GPU copy stays white and large | conversion kept the motion code but lost the look | assign the ramp and curve textures in the study scene and recapture |
| B23 · cost bars | CPU deltas a few percent of budget; GPU 0 under Compatibility | the honest part is the zero | try the Visual Profiler in the editor; it reads the same value |

The film does not judge whether the effects are fun or attractive in general; Bao's verdicts after play are the human judgments, quoted as given.
