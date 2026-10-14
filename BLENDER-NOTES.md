# Blender window notes — Assignment 3

These notes describe the short Blender 5.2.2 session used before the
three-asset rebuild. Claude organized the wording; Bao must review it against
the real window and keep only statements Bao can explain.

## Six parts of the interface

1. **3D Viewport** — the large work area where I orbit, pan and zoom around the
   scene and see the selected object's orange outline.
2. **Toolbar** — the vertical strip on the left of the viewport with select,
   move, rotate and scale tools. It changes the mouse from navigating the view
   to editing the selected object.
3. **Outliner** — the object list at the upper right. It lets me select an item
   by name and check whether a scene contains extra cameras, lights or meshes.
4. **Properties editor** — the tabbed area at lower right for object, material,
   render and scene settings. This is where a material colour or the scene unit
   system can be inspected.
5. **Sidebar** — the panel toggled with `N` inside the viewport. Its Item tab
   shows the selected object's location, rotation, scale and dimensions; scale
   and dimensions are different, so a two-metre default cube can still show a
   scale of one after transforms are applied.
6. **Mode selector** — the menu in the viewport header that switches Object
   Mode and Edit Mode. Object Mode transforms the whole asset part; Edit Mode
   exposes its vertices, edges and faces.

## What the window exercise established

- Blender uses +Z as up. The glTF exporter converts this to Godot's +Y-up
  convention when `+Y Up` is enabled.
- A default cube has scale `(1, 1, 1)` but dimensions `2 x 2 x 2 m`. Dimensions
  are the useful measurement for the brief.
- `Ctrl+A` then **Scale** preserves visible dimensions while baking the scale
  back to one, which avoids unexpected transforms in Godot.
- Scene Statistics reports vertices, faces and triangles. The assignment limit
  applies to triangles and visible primitive count, not just the number shown
  in the Outliner.

## Evidence

- `evidence/a3/blender-interface-session.png` shows the Blender 5.2.2 learning
  session with the cube selected, the `N` sidebar open, unit scale and 2 m
  dimensions visible, and Scene Statistics enabled (12 triangles).
- On 2026-10-14, `OilGem` was selected by name in Blender, rotated **20° around
  Z**, then **Ctrl+A → Rotation** was applied and `oil_shrine.blend` was saved.
  The Item transform first showed Z = 20° and then returned to Z = 0° after
  applying it: applying a transform preserves the visible orientation by
  baking it into the mesh data rather than leaving an object-level rotation.
- A read-only vertex comparison recovered the applied angle as exactly 20°
  (maximum vertex delta `1.49e-8`). The saved file was re-exported to GLB;
  `test_a3_assets.gd` remained 17/17 PASS and the gate suite 14/14 PASS.
