# RIFF — the judgments the narration makes, and what they rest on

Teardown register: describe the mechanism, then judge it. Every judgment points at something on screen in the same beat.

| Artifact · range | Visible observation | Judgment in the narration | Suggested next experiment |
|---|---|---|---|
| B06 · controlled captures 125036 / 125259-red | lamp and coat texels land within one byte of the hand table; red phase keeps more red at 0.5; 2.0 reads back 2.0 and looks like 1.0 | "a shader is arithmetic": the hand table is the test; hint_range is an Inspector hint, not a clamp | set 0.25 and 0.75 and predict them first |
| B08 · hurt take frames 1490–1711 | yellow on the hit frame, held at 23/48 for 45 paused frames, drained to 0 in 24 frames; a touching monster changes nothing | the fade is the counter: no timer, so pause and ignored hits need no extra code | try `Engine.time_scale = 0.5` in a copy: the record says the tint follows unscaled time |
| B10 · pair 170452 | warm repeated paving, cooler larger stones on the stand-in | an inherited scene with three overrides keeps the A3 room's tests intact | — |
| B12 · one-material 170456 | floor changes up to 72 levels, stand-in 0 | values live in the material; the code is shared | the Your Turn change on the stand-in |
| B14 · 131249 vs 163723 | both rectangles darker in every pixel; the green agent run beside it | a shader edit moves every material that uses it; the prediction came first; the agent run broke a stated rule | multiply only ROUGHNESS and predict what changes |
| B16 · maps, curl log, sweep crops | three different-looking files; curl 0.22 vs 1.78 and the mirror file; joints shade differently at strength 0 and 1 | a texture's meaning is declared by its hint, and a normal map can be checked like data | look at the DX map on the floor under a grazing light (the brief's open human check) |
| B18 · sweep 170453 | each uniform moves the floor; the stand-in mean never moves | five numbers are the whole material interface | sweep the stand-in's uv_scale the same way |
| B20 · hint 131056 | 64/128/192 on both quads | matches the Compatibility prediction; the Forward+ difference is still only a prediction | the Forward+ copy (B26's next step) |
| B22 · fixture renders | face-on the two materials agree within 2 levels on 87–93 % of pixels; tilted, the difference grows | the editor's lines and Bao's do the same jobs; the tilted gap is *consistent with* line 22, not proven by it | render Bao's shader with line 22 reverted on a copy to isolate it |
| B25 · recorded output | 28/28 at three frame rates, 127/127, 332 unchanged; mutations fail 4, 3, 1 | the tests run the real loop and catch what they should; none can see colour | rename `hurt_color` and see whether any check notices |

The film does not judge whether the tint is pleasant or the cobblestones attractive. Bao's playtest report and his observation of his own edit are the human judgments, quoted as given in TEST-REPORT.md.
