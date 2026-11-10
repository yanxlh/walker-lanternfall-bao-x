#!/usr/bin/env python3
"""Sample media/<BID>.mp4 at 15/50/85 % of its span into _qc/beats/<BID>.png (three frames stacked, 1280 wide)."""
import subprocess, sys
from pathlib import Path
from PIL import Image

REEL = Path(__file__).resolve().parents[1]
OUT = REEL / "_qc" / "beats"
OUT.mkdir(parents=True, exist_ok=True)
for bid in sys.argv[1:]:
    src = REEL / "media" / f"{bid}.mp4"
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                             capture_output=True, text=True).stdout)
    tiles = []
    for frac in (0.15, 0.5, 0.85):
        p = OUT / f"{bid}-{int(frac * 100)}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{d * frac:.2f}", "-i", str(src), "-frames:v", "1",
                        "-vf", "scale=1280:720", str(p)], check=True)
        tiles.append(Image.open(p))
    s = Image.new("RGB", (1280, 720 * 3 + 8), (255, 0, 255))
    for i, t in enumerate(tiles):
        s.paste(t, (0, i * 724))
    s.save(OUT / f"{bid}.png")
    print(bid, f"{d:.2f}s")
