"""Set the A5 texture import settings from CHANGE-BRIEF.md on the .import files Godot generated.

Only existing [params] keys are changed; a missing key is an error, so no key the importer ignores
can be added. Enum values were checked against Godot 4.7.2-stable
editor/import/resource_importer_texture.cpp:
  compress/mode         Lossless=0, Lossy=1, VRAM Compressed=2, VRAM Uncompressed=3, Basis Universal=4
  compress/normal_map   Detect=0, Enable=1, Disabled=2
  roughness/mode        Detect=0, Disabled=1, ...
  detect_3d/compress_to Disabled=0, VRAM Compressed=1, Basis Universal=2
detect_3d/compress_to and roughness/mode are set too, so a real editor that sees the textures in 3D
has nothing to switch.

Usage: python3 -I tools/a5/set_texture_imports.py   (from the repository root), then reimport.
"""
from pathlib import Path

TEX = Path("godot/assets/textures/cobblestone_floor_08")
COMMON = {"compress/mode": "0", "mipmaps/generate": "true", "detect_3d/compress_to": "0", "roughness/mode": "1"}
PER_FILE = {
    "cobblestone_floor_08_diff_1k.png": {"compress/normal_map": "2"},
    "cobblestone_floor_08_nor_gl_1k.png": {"compress/normal_map": "1"},
    "cobblestone_floor_08_nor_dx_1k.png": {"compress/normal_map": "1"},
    "cobblestone_floor_08_rough_1k.png": {"compress/normal_map": "2"},
}

for name, extra in PER_FILE.items():
    path = TEX / (name + ".import")
    wanted = {**COMMON, **extra}
    lines = path.read_text().splitlines()
    start = lines.index("[params]")
    seen = set()
    for i in range(start + 1, len(lines)):
        key = lines[i].split("=", 1)[0]
        if key in wanted:
            lines[i] = f"{key}={wanted[key]}"
            seen.add(key)
    missing = set(wanted) - seen
    if missing:
        raise SystemExit(f"{path}: keys not present in the generated file: {sorted(missing)}")
    path.write_text("\n".join(lines) + "\n")
    print(f"{name}: " + ", ".join(f"{k}={v}" for k, v in wanted.items()))
