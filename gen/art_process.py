#!/usr/bin/env python3
"""Cut frames out of accepted raws, fit them to game size, lock them to a palette and assemble a strip.

    python gen/art_process.py gen/mappings/ART-PC-01.json

Mapping file:
{
  "out": "godot/assets/art/pc_sheet.png", "preview": "design/character/pc_sheet_x8.png",
  "palette": "character", "frame": [32, 32], "fill": 0.95, "anchor": "bottom", "bg_threshold": 235, "outline": true,
  "frames": [{"name": "turn_front", "src": "gen/accepted/ART-PC-01/<run>.png", "grid": [3, 4], "cell": [0, 0]}, ...]
}
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cut(src: Image.Image, grid, cell, inset=0.02) -> Image.Image:
    rows, cols = grid
    r, c = cell
    cw, ch = src.width / cols, src.height / rows
    box = (int(c * cw + cw * inset), int(r * ch + ch * inset), int((c + 1) * cw - cw * inset), int((r + 1) * ch - ch * inset))
    return src.crop(box)


def key_background(im: Image.Image, threshold: int) -> Image.Image:
    a = np.array(im.convert("RGBA"))
    bg = (a[..., 0] > threshold) & (a[..., 1] > threshold) & (a[..., 2] > threshold)
    a[bg, 3] = 0
    return Image.fromarray(a)


def fit(im: Image.Image, fw: int, fh: int, fill: float, anchor: str) -> Image.Image:
    bbox = im.getbbox()
    if bbox is None:
        raise SystemExit("empty cell after background keying — wrong cell or threshold")
    im = im.crop(bbox)
    s = min(fw * fill / im.width, fh * fill / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    canvas = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    x = (fw - im.width) // 2
    y = fh - im.height if anchor == "bottom" else (fh - im.height) // 2
    canvas.alpha_composite(im, (x, y))
    return canvas


def lock_palette(im: Image.Image, palette, outline_rgb=None) -> Image.Image:
    a = np.array(im).astype(np.int32)
    pal = np.array(palette)
    opaque = a[..., 3] >= 128
    d = ((a[..., None, :3] - pal[None, None, :, :]) ** 2).sum(-1)
    nearest = pal[d.argmin(-1)]
    out = np.zeros_like(a)
    out[opaque, :3] = nearest[opaque]
    out[opaque, 3] = 255
    if outline_rgb is not None:
        o = opaque
        edge = np.zeros_like(o)
        edge[1:, :] |= o[:-1, :]; edge[:-1, :] |= o[1:, :]; edge[:, 1:] |= o[:, :-1]; edge[:, :-1] |= o[:, 1:]
        ring = edge & ~o
        out[ring, :3] = outline_rgb
        out[ring, 3] = 255
    return Image.fromarray(out.astype(np.uint8))


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    palettes = json.loads((ROOT / "godot/assets/art/palettes.json").read_text())
    palette = [rgb(c) for c in palettes[spec["palette"]]]
    fw, fh = spec["frame"]
    frames = []
    for f in spec["frames"]:
        src = Image.open(ROOT / f["src"]).convert("RGBA")
        cell = cut(src, f.get("grid", [1, 1]), f.get("cell", [0, 0])) if "grid" in f else src
        cell = key_background(cell, spec.get("bg_threshold", 235))
        cell = fit(cell, fw, fh, spec.get("fill", 0.95), spec.get("anchor", "bottom"))
        if f.get("mirror"):
            cell = cell.transpose(Image.FLIP_LEFT_RIGHT)
        frames.append(lock_palette(cell, palette, rgb("#14121C") if spec.get("outline") else None))
    strip = Image.new("RGBA", (fw * len(frames), fh), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        strip.paste(fr, (i * fw, 0))
    out = ROOT / spec["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    strip.save(out)
    if spec.get("preview"):
        prev = ROOT / spec["preview"]
        prev.parent.mkdir(parents=True, exist_ok=True)
        strip.resize((strip.width * 8, strip.height * 8), Image.NEAREST).save(prev)
    print(f"{out.relative_to(ROOT)}: {len(frames)} frames")


if __name__ == "__main__":
    main()
