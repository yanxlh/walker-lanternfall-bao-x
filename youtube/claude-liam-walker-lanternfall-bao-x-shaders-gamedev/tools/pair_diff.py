#!/usr/bin/env python3
"""Measure the shader-pair fixture (capture/shader-pair/). The two plane positions do not sample the texture on the
same pixel grid, so left and right of one picture are never compared with each other. Instead the same plane is
compared across two renders: control-generated (both planes wear the editor-generated material) against control-bao
(both planes wear Bao's shader with neutral values), pose by pose. Writes capture/shader-pair/diff.json."""
import json
from pathlib import Path
import numpy as np
from PIL import Image

REEL = Path(__file__).resolve().parents[1]
D = REEL / "capture" / "shader-pair"


def load(name, pose):
    return np.asarray(Image.open(D / f"{name}-{pose}.png").convert("RGB")).astype(int)


def rects(a):
    bg = a[2, 2]
    fg = np.abs(a - bg).sum(axis=2) > 12
    cols = np.where(fg.any(axis=0))[0]
    rows = np.where(fg.any(axis=1))[0]
    gap = np.where(np.diff(cols) > 1)[0][0]
    return {"left": (cols[0], rows[0], cols[gap], rows[-1]), "right": (cols[gap + 1], rows[0], cols[-1], rows[-1])}


out = {}
for pose in ("straight", "tilted"):
    g, b = load("control-generated", pose), load("control-bao", pose)
    for side, (x0, y0, x1, y1) in rects(g).items():
        G = g[y0 + 2:y1 - 2, x0 + 2:x1 - 2]
        B = b[y0 + 2:y1 - 2, x0 + 2:x1 - 2]
        d = np.abs(G - B).max(axis=2)
        out[f"{pose}-{side}"] = {"rect": [int(x0), int(y0), int(x1 - x0 + 1), int(y1 - y0 + 1)], "compared_px": int(d.size),
                                 "identical_px": int((d == 0).sum()), "within_2_px": int((d <= 2).sum()),
                                 "max_channel_delta": int(d.max()), "mean_abs_delta": round(float(np.abs(G - B).mean()), 3),
                                 "p99_channel_delta": int(np.percentile(d, 99)),
                                 "generated_mean_rgb": [round(float(x), 2) for x in G.reshape(-1, 3).mean(0)],
                                 "bao_mean_rgb": [round(float(x), 2) for x in B.reshape(-1, 3).mean(0)]}
(D / "diff.json").write_text(json.dumps(out, indent=1))
for k, v in out.items():
    print(k, {x: v[x] for x in ("identical_px", "within_2_px", "compared_px", "max_channel_delta", "p99_channel_delta",
                                "mean_abs_delta", "generated_mean_rgb", "bao_mean_rgb")})
