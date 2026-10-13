# Project checks

## Checks

Rebuild the Assignment 3 prop with:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_lantern_gate.py
```

Import and test with:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import
gtimeout 120 /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tests/test_lantern_gate.gd --fixed-fps 60
```

Do not hand-write `.import` files or invent Godot UIDs. Do not change existing
2D movement tuning, audio rules, or earlier tests to make an A3 check pass.
