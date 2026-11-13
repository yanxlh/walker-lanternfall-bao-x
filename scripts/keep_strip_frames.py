#!/usr/bin/env python3
"""Assignment 7: after a Movie Maker capture of godot/previews/courier_preview.tscn, keep the frames the brief lists
and delete the rest of the sequence (the assignment's Step 7). Usage:
    python3 -I scripts/keep_strip_frames.py <capture-dir> dash|walk
dash keeps the frame before the trigger, the trigger frame (dash frame 0) and the first frame at or after each phase
boundary (active, recovery, end); walk keeps two whole cycles. Writes STRIP.md (fixture capture, frame N = log line N)
and strip.png when Pillow is available. Only frameNNNNNNNN.png files and frame.wav in <capture-dir> are deleted.
"""
import re
import sys
from pathlib import Path

STARTUP, ACTIVE, RECOVERY = 4, 10, 6  # CHANGE-BRIEF phase table r1, ticks at 60 per second
WHAT = {
    "before trigger": "walking right, the sprite (cell 2 or 3)",
    "trigger": "dash frame 0: the rig replaces the sprite, upright",
    "active begins": "the lean into the dash, lamp trailing",
    "recovery begins": "the end of the push, starting to settle",
    "dash ends": "back on the walk sprite",
}


def main() -> int:
    cap, clip = Path(sys.argv[1]), sys.argv[2]
    rows = [dict(kv.split("=", 1) for kv in l.split()) for l in (cap / "frames.log").read_text().splitlines()]
    keep = {}
    if clip == "dash":
        start = next(i for i, r in enumerate(rows) if r["phase"] == "startup")
        keep[start - 1] = "before trigger"
        keep[start] = "trigger"
        for label, tick in (("active begins", STARTUP), ("recovery begins", STARTUP + ACTIVE)):
            keep[next(i for i in range(start, len(rows)) if rows[i]["phase"] != "" and int(rows[i]["dash_ticks"]) >= tick)] = label
        keep[next(i for i in range(start, len(rows)) if rows[i]["phase"] == "")] = "dash ends"
    else:
        first = next(i for i, r in enumerate(rows) if r["pose"].startswith("walk"))
        for i in range(first, min(first + 16, len(rows))):
            keep[i] = "walk cycle"
    frames = sorted(cap.glob("frame[0-9]*.png"))
    for f in frames:
        n = int(re.search(r"(\d+)", f.name).group(1))
        if n not in keep:
            f.unlink()
    wav = cap / "frame.wav"
    if wav.exists():
        wav.unlink()
    lines = ["# Frame strip (fixture capture)", "",
             "Movie Maker, 30 fps, `godot/previews/courier_preview.tscn` (fixtures in its header). Frame N is line N of `frames.log`.", "",
             "| Frame | Tick | Dash frame | Phase | Label | Should show |", "|---|---|---|---|---|---|"]
    for n in sorted(keep):
        r = rows[n]
        lines.append("| %d | %s | %s | %s | %s | %s |" % (n, r["tick"], r["dash_ticks"] if r["phase"] else "-", r["phase"] or "-", keep[n], WHAT.get(keep[n], "cells alternate 2 and 3")))
    lines += ["", "What I see (Bao):", "", "Claude's reading (a claim, not a check):", ""]
    (cap / "STRIP.md").write_text("\n".join(lines) + "\n")
    try:
        from PIL import Image
        ims = [Image.open(cap / ("frame%08d.png" % n)).convert("RGB") for n in sorted(keep)]
        w = 384
        sheet = Image.new("RGB", (w * len(ims), w), (14, 16, 32))
        for i, im in enumerate(ims):
            s = im.width / 640
            cx, cy = float(rows[sorted(keep)[i]]["sx"]) * s, float(rows[sorted(keep)[i]]["sy"]) * s
            sheet.paste(im.crop((int(cx - 96), int(cy - 96), int(cx + 96), int(cy + 96))).resize((w, w), Image.NEAREST), (i * w, 0))
        sheet.save(cap / "strip.png")
    except ImportError:
        print("Pillow not available: STRIP.md written, strip.png skipped")
    print("kept frames %s in %s" % (sorted(keep), cap))
    return 0


if __name__ == "__main__":
    sys.exit(main())
