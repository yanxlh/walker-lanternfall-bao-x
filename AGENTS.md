# Project checks

## Checks

Rebuild the three Assignment 3 assets with:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_lantern_gate.py
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_supply_stack.py
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_oil_shrine.py
```

`tools/blender/build_<asset>.py` holds the Blender MCP `execute_blender_code`
bodies, verbatim and in order; it also runs headless. The pre-MCP headless
scripts are kept in `tools/blender/script_route/`. In a live Blender reached
through the MCP, never call `bpy.ops.wm.read_factory_settings`: it resets
preferences and drops the add-on connection. Clear scenes through `bpy.data`.

Import and test with:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import
gtimeout 120 /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tests/test_a3_assets.gd --fixed-fps 60
```

Do not hand-write `.import` files or invent Godot UIDs. Do not change existing
2D movement tuning, audio rules, or earlier tests to make an A3 check pass.
