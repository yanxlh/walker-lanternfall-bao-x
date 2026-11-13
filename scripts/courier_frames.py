#!/usr/bin/env python3
"""Assignment 7 frame tools for captures written by godot/tests/capture_courier.gd.

strip <capture-dir> <first> <last> <out.png> [--every N] [--scale S]
    Crops the courier from movie frames first..last (inclusive), centred on the logged screen position, and tiles
    them left to right. Each tile is labelled with the frame number and the logged cell and dash phase, so tile N
    lines up with log line N.
compare <before-dir> <after-dir> <out.json>
    Compares every movie frame pixel for pixel (whole frame and the courier crop) and the two frames.log files'
    cell, pose and position columns. Exit 1 on any difference.
"""
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

CROP = 48  # half-size of the courier crop, in window pixels (1280 x 720 window, 640 x 360 viewport)


def read_log(capture: Path) -> list:
    rows = []
    for line in (capture / "frames.log").read_text().splitlines():
        rows.append(dict(kv.split("=", 1) for kv in line.split()))
    return rows


def frame_path(capture: Path, n: int) -> Path:
    return capture / "movie" / ("frame%08d.png" % n)


def crop(capture: Path, row: dict, n: int) -> Image.Image:
    im = Image.open(frame_path(capture, n)).convert("RGB")
    scale = im.width / 640
    cx, cy = float(row["sx"]) * scale, float(row["sy"]) * scale
    return im.crop((int(cx - CROP), int(cy - CROP), int(cx + CROP), int(cy + CROP)))


def strip(args: list) -> int:
    capture, first, last, out = Path(args[0]), int(args[1]), int(args[2]), Path(args[3])
    every = int(args[args.index("--every") + 1]) if "--every" in args else 1
    scale = int(args[args.index("--scale") + 1]) if "--scale" in args else 2
    rows = read_log(capture)
    frames = list(range(first, last + 1, every))
    tile = CROP * 2 * scale
    sheet = Image.new("RGB", (tile * len(frames), tile + 30), (14, 16, 32))
    draw = ImageDraw.Draw(sheet)
    for i, n in enumerate(frames):
        c = crop(capture, rows[n], n).resize((tile, tile), Image.NEAREST)
        sheet.paste(c, (i * tile, 30))
        label = "%d c%s %s" % (n, rows[n]["cell"], rows[n].get("phase", "-"))
        draw.text((i * tile + 4, 4), label, fill=(255, 241, 201))
        draw.text((i * tile + 4, 16), "t%s %s" % (rows[n]["tick"], rows[n]["pose"]), fill=(200, 200, 210))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print("wrote %s: frames %s" % (out, frames))
    return 0


def compare(args: list) -> int:
    a, b, out = Path(args[0]), Path(args[1]), Path(args[2])
    ra, rb = read_log(a), read_log(b)
    result = {"before": str(a), "after": str(b), "frames_before": len(ra), "frames_after": len(rb),
              "whole_frame_diffs": [], "crop_diffs": [], "log_diffs": []}
    for n in range(min(len(ra), len(rb))):
        for key in ("tick", "state", "pose", "cell", "x", "y", "iframes", "hp", "facing"):
            if ra[n].get(key) != rb[n].get(key):
                result["log_diffs"].append({"frame": n, "key": key, "before": ra[n].get(key), "after": rb[n].get(key)})
        ia = Image.open(frame_path(a, n)).convert("RGB")
        ib = Image.open(frame_path(b, n)).convert("RGB")
        box = ImageChops.difference(ia, ib).getbbox()
        if box:
            result["whole_frame_diffs"].append({"frame": n, "bbox": box})
        ca, cb = crop(a, ra[n], n), crop(b, rb[n], n)
        diff = ImageChops.difference(ca, cb)
        changed = diff.convert("L").point(lambda v: 255 if v else 0).histogram()[255]
        if changed:
            result["crop_diffs"].append({"frame": n, "pixels": changed})
    result["identical"] = (len(ra) == len(rb) and not result["whole_frame_diffs"] and not result["crop_diffs"]
                           and not result["log_diffs"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in result.items()}))
    return 0 if result["identical"] else 1


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("strip", "compare"):
        print(__doc__)
        sys.exit(2)
    sys.exit(strip(sys.argv[2:]) if sys.argv[1] == "strip" else compare(sys.argv[2:]))
