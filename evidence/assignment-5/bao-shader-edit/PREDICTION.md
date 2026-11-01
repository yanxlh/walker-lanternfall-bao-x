# Bao's one-line shader edit — prediction

Recorded 2026-10-30 16:32:54 EDT, before the edit, at revision 6729208. Bao's words:

> Multiply the end of the ALBEDO line by 0.5. Floor and StandIn both get darker diffuse colour, because they share this shader. Stone size and normal detail stay the same; highlights need not darken in proportion; other props are unaffected.

Line to edit: `godot/shaders/cobblestone_surface.gdshader:19`. Baseline for comparison: `captures/a5-materials/20261030-131249-compare-shader-baseline/`.
