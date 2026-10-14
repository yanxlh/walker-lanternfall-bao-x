# Blender window notes — Assignment 3

## Hand edit — OilGem, 2026-10-14

**What I saw.** I selected `OilGem` in the Outliner. After I rotated it, the
Item panel on the right showed Z rotation 20°. After I applied the rotation,
Z rotation read 0° again, but the gem kept its new orientation; it did not
turn back.

**What I changed.** I rotated `OilGem` 20° around the Z axis, applied it with
**Ctrl+A → Rotation**, saved `blender/a3/oil_shrine.blend`, and re-exported
`godot/a3/oil_shrine.glb` with **File > Export**.

**What I learned.**

- The Outliner selects an object exactly, by name.
- A shortcut can rotate around a chosen axis by a typed angle (`R`, `Z`, `20`).
- Applying a rotation does not undo the visible turn. It writes the turn into
  the mesh data, which is why the object's rotation value returns to zero.
- That keeps the model at a unit transform when Godot imports it, so
  orientation and scale problems do not appear later.
- After the re-export, every test still passed.

**Consequence for the repository.** `blender/a3/oil_shrine.blend` is now the
shrine's source. `tools/blender/build_oil_shrine.py` rebuilds only the
pre-edit MCP version and would overwrite this edit if run.

## Six parts of the interface

1. **3D Viewport**: the large work area for orbiting, panning and zooming.
   The selected object has an orange outline.
2. **Toolbar**: the vertical strip on the left of the viewport, with the
   select, move, rotate and scale tools. Choosing one switches the mouse from
   navigating the view to editing the selected object.
3. **Outliner**: the object list at the upper right. It selects an item by
   name and shows whether the scene holds extra cameras, lights or meshes.
4. **Properties editor**: the tabbed area at the lower right, with object,
   material, render and scene settings. Material colours and the scene's unit
   system are inspected here.
5. **Sidebar**: the panel toggled with `N` inside the viewport. Its Item tab
   shows the selected object's location, rotation, scale and dimensions. Scale
   and dimensions differ: after transforms are applied, a two-metre cube still
   shows scale 1.
6. **Mode selector**: the menu in the viewport header that switches between
   Object Mode and Edit Mode. Object Mode transforms a whole part; Edit Mode
   exposes its vertices, edges and faces.

## What the window exercise established

- Blender uses +Z as up. With `+Y Up` enabled, the glTF exporter converts this
  to Godot's +Y-up convention.
- A default cube has scale `(1, 1, 1)` and dimensions `2 x 2 x 2 m`. The brief
  is measured in dimensions.
- **Ctrl+A → Scale** keeps the visible dimensions and bakes the scale back to
  one, so Godot receives no unexpected transforms.
- Scene Statistics reports vertices, faces and triangles. The assignment
  limits triangles and the number of visible primitives; the Outliner's object
  count alone does not show either.

## Evidence

- `evidence/a3/blender-interface-session.png` is my screenshot of the
  Blender 5.2.2 learning session. It shows the cube selected, the `N`
  sidebar open with unit scale and 2 m dimensions, and Scene Statistics on
  (12 triangles).
- Measured check of the hand edit: rotating the MCP export's gem vertices by
  20.0° about Blender Z reproduces the re-exported gem to within 1.84e-8 m.
  The gem has 72° symmetry, so the angle is unique only up to that symmetry.
  Its node in the GLB has no rotation or scale.
