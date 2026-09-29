#!/usr/bin/env python3
"""Make ART-ENV-01 seamless, downscale to 64x64, lock to the environment palette, and measure the seam.

    python gen/tile_process.py gen/accepted/ART-ENV-01/<run>.png
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
from art_process import lock_palette, rgb

ROOT = Path(__file__).resolve().parents[1]
src = Image.open(sys.argv[1]).convert("RGB")
side = min(src.size)
src = src.crop(((src.width - side) // 2, (src.height - side) // 2, (src.width + side) // 2, (src.height + side) // 2))
a = np.asarray(src).astype(np.float32)
rolled = np.roll(np.roll(a, side // 2, 0), side // 2, 1)
yy, xx = np.mgrid[0:side, 0:side] / (side - 1)
w = (np.sin(np.pi * yy) * np.sin(np.pi * xx))[..., None]
tile = (a * w + rolled * (1 - w)).clip(0, 255).astype(np.uint8)
small = Image.fromarray(tile).resize((64, 64), Image.LANCZOS).convert("RGBA")
palette = [rgb(c) for c in json.loads((ROOT / "godot/assets/art/palettes.json").read_text())["environment"]]
locked = lock_palette(small, palette)
out = ROOT / "godot/assets/art/env_ground_tile.png"
locked.save(out)
t = np.asarray(locked).astype(np.int32)[..., :3]
seam = float(np.abs(t[:, 0] - t[:, -1]).mean() + np.abs(t[0] - t[-1]).mean()) / 2
interior = float(np.abs(np.diff(t, axis=1)).mean() + np.abs(np.diff(t, axis=0)).mean()) / 2
report = {"seam_mean_abs": round(seam, 2), "interior_mean_abs": round(interior, 2), "pass": seam <= interior * 1.25}
(ROOT / "evidence" / "tile-seam.json").write_text(json.dumps(report, indent=2) + "\n")
Image.fromarray(np.tile(np.asarray(locked), (3, 3, 1))).resize((576, 576), Image.NEAREST).save(ROOT / "evidence" / "tile-3x3-preview.png")
print(report)
