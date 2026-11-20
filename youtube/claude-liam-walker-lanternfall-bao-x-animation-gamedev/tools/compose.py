#!/usr/bin/env python3
"""Compose a 4K beat video from layers: real engine footage, real files (sprites, raw model outputs, recorded test
output) and text, each revealed at a time. Used for the film's evidence beats; nothing here draws game content.

    python3 tools/compose.py spec.json

Spec: {"out": "media/B05.mp4", "duration": 21.3, "fps": 30, "bg": "#FAF9F5", "audio": "video" | null,
       "layers": [ {"kind": "text" | "image" | "rect" | "video", ...}, ... ]}
Coordinates are pixels on the 3840 x 2160 canvas. Every layer may carry "t": [t_in, t_out] and "fade" (seconds).
  text  : text, font (serif | sans | sans-medium | mono), size, color, x, y, w (wrap width), align, spacing
  image : src, x, y, w, h, fit (contain | stretch), resample (nearest | lanczos), pad_color
  rect  : x, y, w, h, fill, outline, width, radius
  video : src, ss (source seconds), x, y, w, h, crop [x, y, w, h] in source pixels (after "pad", if given),
          pad (px of dark margin added around the source first), resample (nearest | lanczos)
          (sources are the cleaned takes from tools/clean_take.py, so frame n of a take is game frame n)
A video layer is drawn above everything listed before it. Frames are composited in Python (Pillow) and piped to one
ffmpeg encoder; each video layer is decoded by its own ffmpeg process at its display size. Static stretches reuse
the previous frame, so memory stays low on a busy machine. Consecutive still layers with identical timing are
flattened into one image first (same order, same pixels). With "audio": "video" the first video layer's audio
(same span) is kept — used only for the game-sound-only beats.
"""
import json, math, os, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 3840, 2160
FONTS = Path(os.environ.get("ART_FONTS", "/Users/yxlh/brutalist.art/runtime/fonts"))
FONT_FILES = {
    "serif": FONTS / "EB_Garamond/static/EBGaramond-Regular.ttf",
    "serif-medium": FONTS / "EB_Garamond/static/EBGaramond-Medium.ttf",
    "serif-italic": FONTS / "EB_Garamond/static/EBGaramond-Italic.ttf",
    "sans": FONTS / "Inter/static/Inter_28pt-Regular.ttf",
    "sans-medium": FONTS / "Inter/static/Inter_28pt-Medium.ttf",
    "mono": FONTS / "PT_Mono/PTMono-Regular.ttf",
    "cjk": Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),   # Bao's own words, quoted in Chinese
}
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_FILES[name]), size)


def wrap(draw, text: str, f, width: int) -> list:
    lines = []
    for para in text.split("\n"):
        if not width or draw.textlength(para, font=f) <= width:   # fits: keep it as written (tables keep their spaces)
            lines.append(para)
            continue
        words, cur = para.split(" "), ""
        for w in words:
            nxt = w if not cur else cur + " " + w
            if width and draw.textlength(nxt, font=f) > width and cur:
                lines.append(cur)
                cur = w
            else:
                cur = nxt
        lines.append(cur)
    return lines


def render_text(L: dict) -> tuple:
    f = font(L.get("font", "sans"), int(L["size"]))
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines = wrap(probe, L["text"], f, int(L.get("w", 0)))
    lh = int(L["size"] * L.get("spacing", 1.25))
    width = int(L.get("w") or max(probe.textlength(s, font=f) for s in lines)) + 8
    height = lh * len(lines) + int(L["size"] * 0.35)
    im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, s in enumerate(lines):
        tw = d.textlength(s, font=f)
        x = {"left": 0, "center": (width - tw) / 2, "right": width - tw}[L.get("align", "left")]
        d.text((x, i * lh), s, font=f, fill=L.get("color", "#3D3929"))
    return im, int(L["x"]), int(L["y"])


def render_image(L: dict, base: Path) -> tuple:
    src = Image.open(base / L["src"]).convert("RGBA")
    w, h = int(L["w"]), int(L["h"])
    resample = Image.NEAREST if L.get("resample") == "nearest" else Image.LANCZOS
    if L.get("fit", "contain") == "stretch":
        im = src.resize((w, h), resample)
        ox = oy = 0
    else:
        s = min(w / src.width, h / src.height)
        if L.get("resample") == "nearest" and s >= 1:
            s = max(1, int(s))          # whole-number pixel scale keeps pixel art square
        im = src.resize((max(1, round(src.width * s)), max(1, round(src.height * s))), resample)
        ox, oy = (w - im.width) // 2, (h - im.height) // 2
    canvas = Image.new("RGBA", (w, h), L.get("pad_color", (0, 0, 0, 0)))
    canvas.alpha_composite(im, (ox, oy))
    return canvas, int(L["x"]), int(L["y"])


def render_rect(L: dict) -> tuple:
    w, h = int(L["w"]), int(L["h"])
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(L.get("radius", 0)), fill=L.get("fill"),
                        outline=L.get("outline"), width=int(L.get("width", 0)))
    return im, int(L["x"]), int(L["y"])


def _alpha(t_in, t_out, fade, t, dur):
    if t < t_in - 1e-9 or t > t_out + 1e-9:
        return 0.0
    a = 1.0
    if fade > 0:
        a = min(a, (t - t_in) / fade)
        if t_out < dur - 0.01:
            a = min(a, (t_out - t) / fade)
    return max(0.0, min(1.0, a))


class _Decoder:
    """Raw RGBA frames of one video layer, decoded at display size, read in order."""
    def __init__(self, L, base, fps):
        src = (base / L["src"]).resolve()
        vf = []
        if L.get("pad"):
            pd = int(L["pad"])
            vf.append(f"pad=iw+{2 * pd}:ih+{2 * pd}:{pd}:{pd}:color=0x0E1020")
        if L.get("crop"):
            cx, cy, cw, ch = L["crop"]
            vf.append(f"crop={cw}:{ch}:{cx}:{cy}")
        flags = "neighbor" if L.get("resample") == "nearest" else "lanczos"
        self.w, self.h = int(L["w"]), int(L["h"])
        vf.append(f"scale={self.w}:{self.h}:flags={flags}")
        vf.append("format=rgba")
        self.span = L["t"][1] - L["t"][0]
        n = math.ceil(self.span * fps) + 2
        self.p = subprocess.Popen([FFMPEG, "-v", "error", "-ss", f"{float(L.get('ss', 0)):.4f}", "-i", str(src),
                                   "-frames:v", str(n), "-vf", ",".join(vf), "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                                  stdout=subprocess.PIPE)
        self.size = self.w * self.h * 4
        self.cur, self.read = None, 0

    def frame(self, k):
        """Frame k of the layer (k counted from its t_in); None after the clip ends."""
        while self.read <= k:
            b = self.p.stdout.read(self.size)
            if len(b) < self.size:
                self.cur = None
                return None
            self.cur = Image.frombuffer("RGBA", (self.w, self.h), b, "raw", "RGBA", 0, 1)
            self.read += 1
        return self.cur

    def close(self):
        self.p.stdout.close()
        self.p.wait()


def main() -> None:
    spec_path = Path(sys.argv[1]).resolve()
    spec = json.loads(spec_path.read_text())
    base = Path(spec.get("base", spec_path.parent)).resolve()
    out = (base / spec["out"]).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    dur, fps = float(spec["duration"]), int(spec.get("fps", 30))
    frames = math.ceil(dur * fps - 1e-6)    # the compiler pads, never truncates: same frame count, so no retime
    dur = frames / fps
    bg = Image.new("RGBA", (W, H), spec.get("bg", "#FAF9F5"))
    merged, run = [], []

    def flush():
        if not run:
            return
        parts = []
        for L in run:
            if L["kind"] == "text":
                parts.append(render_text(L))
            elif L["kind"] == "image":
                parts.append(render_image(L, base))
            elif L["kind"] == "rect":
                parts.append(render_rect(L))
            else:
                raise SystemExit("unknown layer kind " + L["kind"])
        x0 = min(x for _im, x, _y in parts)
        y0 = min(y for _im, _x, y in parts)
        x1 = max(x + im.width for im, x, _y in parts)
        y1 = max(y + im.height for im, _x, y in parts)
        canvas = Image.new("RGBA", (max(1, x1 - x0), max(1, y1 - y0)), (0, 0, 0, 0))
        for im, x, y in parts:
            canvas.alpha_composite(im, (x - x0, y - y0))
        t = run[0].get("t") or [0, dur]
        merged.append({"kind": "_still", "im": canvas, "x": x0, "y": y0, "t": [float(t[0]), min(float(t[1]), dur)],
                       "fade": float(run[0].get("fade", 0.0)), "faded": {}})
        run.clear()
    for L in spec["layers"]:
        if L["kind"] == "video":
            flush()
            L = dict(L)
            L["t"] = [float(L["t"][0]), min(float(L["t"][1]), dur)]
            merged.append(L)
            continue
        if run and (L.get("t"), L.get("fade", 0.0)) != (run[0].get("t"), run[0].get("fade", 0.0)):
            flush()
        run.append(L)
    flush()
    decoders = {}
    with tempfile.TemporaryDirectory(prefix="compose-") as tmp:
        tmp = Path(tmp)
        silent = tmp / "v.mp4"
        enc = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                "-r", str(fps), "-i", "-", "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast",
                                "-crf", "14", "-x264-params", "rc-lookahead=8:threads=4:sliced-threads=0",
                                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(silent)],
                               stdin=subprocess.PIPE)
        last_key, last_bytes = None, None
        for i in range(frames):
            t = i / fps
            key, active = [], []
            for n, L in enumerate(merged):
                t_in, t_out = L["t"]
                if L["kind"] == "video":
                    if t_in - 1e-9 <= t < t_out:
                        if n not in decoders:
                            decoders[n] = _Decoder(L, base, fps)
                        k = int(round((t - t_in) * fps))
                        active.append((n, L, k))
                        key.append((n, k))
                    continue
                a = _alpha(t_in, t_out, L["fade"], t, dur)
                if a > 0:
                    q = round(a * 32)
                    active.append((n, L, q))
                    key.append((n, q))
            key = tuple(key)
            if key == last_key and not any(L["kind"] == "video" for _n, L, _k in active):
                enc.stdin.write(last_bytes)
                continue
            canvas = bg.copy()
            for n, L, k in active:
                if L["kind"] == "video":
                    fr = decoders[n].frame(k)
                    if fr is not None:
                        canvas.alpha_composite(fr, (int(L["x"]), int(L["y"])))
                    continue
                im = L["im"]
                if k < 32:
                    if k not in L["faded"]:
                        f2 = im.copy()
                        f2.putalpha(im.getchannel("A").point(lambda v, s=k / 32: int(v * s)))
                        L["faded"][k] = f2
                    im = L["faded"][k]
                canvas.alpha_composite(im, (L["x"], L["y"]))
            last_key, last_bytes = key, canvas.convert("RGB").tobytes()
            enc.stdin.write(last_bytes)
        enc.stdin.close()
        if enc.wait() != 0:
            raise SystemExit("encode failed")
        for d in decoders.values():
            d.close()
        audio_src = None
        if spec.get("audio") == "video":
            audio_src = next((L for L in merged if L["kind"] == "video"), None)
        if audio_src is not None:
            src = (base / audio_src["src"]).resolve()
            r = subprocess.run([FFMPEG, "-v", "error", "-y", "-i", str(silent), "-ss", f"{float(audio_src.get('ss', 0)):.4f}",
                                "-t", f"{dur:.4f}", "-i", str(src), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                                "-b:a", "256k", "-ar", "48000", "-t", f"{dur:.4f}", "-movflags", "+faststart", str(out)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit(r.stderr[-3000:])
        else:
            import shutil
            shutil.move(str(silent), str(out))
    print(out)


if __name__ == "__main__":
    main()
