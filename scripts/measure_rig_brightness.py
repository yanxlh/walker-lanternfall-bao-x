#!/usr/bin/env python3
"""Assignment 7: is the dash rig brighter than the walk sprite? Reads the 8x clip frames in a clip-strip folder
(godot/tests/capture_courier_clip_strip.gd, flat grey ground) and reports, per frame, the courier's pixel count,
mean luminance (Rec. 709) and mean RGB, and whether the rig uses any colour the walk cell does not.
Usage: python3 -I scripts/measure_rig_brightness.py captures/assignment-7/clip-strips-r1 > out.json  (needs Pillow)
"""
import json
import sys
from pathlib import Path

from PIL import Image

GROUND = (158, 158, 168)  # Color(0.62, 0.62, 0.66) in the clip-strip capture


def courier_pixels(path: Path) -> list:
    im = Image.open(path).convert("RGB")
    data = im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()
    return [p for p in data if max(abs(p[i] - GROUND[i]) for i in range(3)) > 12]


def main() -> int:
    d = Path(sys.argv[1])
    out = {"folder": str(d), "frames": {}}
    for f in ["walk-00", "walk-08", "dash-00", "dash-02", "dash-04", "dash-05", "dash-10", "dash-14", "dash-16", "dash-20"]:
        px = courier_pixels(d / (f + ".png"))
        lum = [0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in px]
        out["frames"][f] = {"pixels": len(px), "mean_luminance": round(sum(lum) / len(lum), 2),
                            "mean_rgb": [round(sum(p[i] for p in px) / len(px), 1) for i in range(3)]}
    walk = set(courier_pixels(d / "walk-00.png"))
    out["rig_colours_not_in_walk_cell"] = sorted({c for f in ("dash-04", "dash-05", "dash-10") for c in courier_pixels(d / (f + ".png"))} - walk)
    lums = [v["mean_luminance"] for v in out["frames"].values()]
    out["luminance_range"] = [min(lums), max(lums)]
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
