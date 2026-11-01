#!/usr/bin/env python3
"""Build media/<BID>.mp4 for every evidence and game-sound beat of the shader film (4K, 30 fps).

Everything shown is real: the 4K Movie Maker take in capture/, the committed in-engine captures and recorded tool
output in the repository, the film's own labelled shader-pair fixture, and the take's own per-frame log. Held frames
and replays are labelled. Code lines shown here are read verbatim from git at the film revision (tools/src.py).
Layout follows the Assignment 6 film's evidence beats (same chrome, same compose.py).

    python3 tools/build_media.py [B06 B08 ...]
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
TOOLS = REEL / "tools"
WORK = REEL / "media" / "_work"
sys.path.insert(0, str(TOOLS))
from compose import FONT_FILES  # noqa: E402
from src import SHA as FULL_SHA, excerpt, repo_text  # noqa: E402

RECORDS_REV = "b295096"     # TEST-REPORT.md / PREDICTION.md with Bao's words in English (8490cfe, f9f0fd8)


def bao_quote(after: str) -> str:
    """Bao's words as TEST-REPORT.md records them, the text inside the quotes that follow `after`."""
    t = repo_text("TEST-REPORT.md", RECORDS_REV)
    i = t.index(after) + len(after)
    a = t.index("“", i)
    return t[a + 1:t.index("”", a)]

W, H, FPS = 3840, 2160, 30
PAD, TITLE_Y, TOP, BOT = 211, 97, 346, 1901
RIGHT = W - PAD
INK, SOFT, GHOST, SPARK, PAGE, CARD, BORDER = "#3D3929", "#73705F", "#A9A491", "#D97757", "#FAF9F5", "#FFFFFF", "#E5E2D9"
GOOD, DARK, AMBER = "#4F7A4A", "#202531", "#B8860B"
SHA = FULL_SHA[:7]
SHEET = json.loads((REEL / "beat_sheet.json").read_text())
BEATS = {b["beat_id"]: b for b in SHEET["beats"]}
REPO_REL = "../.."          # repository root, relative to the reel (compose.py resolves sources from the reel)
TAKE = "capture/take-hurt-seed5.avi"
TAKE_LOG = "capture/take-hurt-seed5-log.jsonl"
STATE = ["menu", "playing", "level-up cards", "paused", "won", "lost"]
CAP = REPO / "captures"


def font(name, size):
    return ImageFont.truetype(str(FONT_FILES[name]), size)


class Take:
    def __init__(self):
        self.events = [json.loads(l) for l in (REEL / TAKE_LOG).read_text().splitlines()]
        self.track = next(e for e in self.events if e["event"] == "track")["frames"]

    def find(self, event, **kw):
        return [e for e in self.events if e["event"] == event and all(e.get(k) == v for k, v in kw.items())]

    def row(self, frame):
        r = self.track[max(0, min(frame, len(self.track) - 1))]
        return {"x": r[0], "y": r[1], "zoom": r[2], "amount": r[3], "iframes": r[4], "red": r[5], "state": r[6],
                "hp": r[7], "contact": r[8], "tick": r[9]}


def dur(bid):
    return float(BEATS[bid]["actual_duration_s"])


def at(bid, phrase, lead=0.25):
    text_ = BEATS[bid]["narration_text"]
    i = text_.find(phrase)
    if i < 0:
        raise SystemExit(f"{bid}: phrase not in narration: {phrase!r}")
    return round(max(0.0, dur(bid) * i / len(text_) - lead), 2)


def text(t, x, y, size, color=INK, f="sans", w=0, align="left", t_in=0.0, t_out=None, fade=0.25, spacing=1.25):
    L = {"kind": "text", "text": t, "x": x, "y": y, "size": size, "color": color, "font": f, "w": w, "align": align,
         "spacing": spacing}
    if t_in or t_out is not None:
        L["t"] = [t_in, t_out if t_out is not None else 9999]
        L["fade"] = fade
    return L


def rect(x, y, w, h, fill=CARD, outline=BORDER, width=3, radius=28, t_in=0.0, t_out=None, fade=0.25):
    L = {"kind": "rect", "x": x, "y": y, "w": w, "h": h, "fill": fill, "outline": outline, "width": width, "radius": radius}
    if t_in or t_out is not None:
        L["t"] = [t_in, t_out if t_out is not None else 9999]
        L["fade"] = fade
    return L


def image(src, x, y, w, h, t_in=0.0, t_out=None, nearest=False, fade=0.25):
    L = {"kind": "image", "src": src, "x": x, "y": y, "w": w, "h": h}
    if nearest:
        L["resample"] = "nearest"
    if t_in or t_out is not None:
        L["t"] = [t_in, t_out if t_out is not None else 9999]
        L["fade"] = fade
    return L


def frame_chrome(title, source, extra_source=""):
    return [text(title, PAD, TITLE_Y, 120, INK, "serif"),
            text(source + (f" · {extra_source}" if extra_source else ""), PAD, 2005, 44, SOFT, "sans", w=3000),
            text("@NikBearBrown", W - PAD - 420, 1996, 58, INK, "serif", w=420, align="right")]


def spec_write(bid, layers, duration, audio=None):
    for L in layers:
        if "t" in L and L["t"][1] > duration:
            L["t"][1] = duration
    spec = {"out": f"media/{bid}.mp4", "duration": round(duration, 4), "fps": FPS, "bg": PAGE, "base": str(REEL),
            "audio": audio, "layers": layers}
    WORK.mkdir(parents=True, exist_ok=True)
    p = WORK / f"{bid}.json"
    p.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    subprocess.run([sys.executable, str(TOOLS / "compose.py"), str(p)], check=True)


def video(start_frame, x, y, w, h, t_in=0.0, t_out=None, crop=None, nearest=False):
    L = {"kind": "video", "src": TAKE, "ss": start_frame / FPS, "x": x, "y": y, "w": w, "h": h,
         "t": [t_in, t_out if t_out is not None else 9999]}
    if crop:
        L["crop"] = [int(round(c)) for c in crop]
    if nearest:
        L["resample"] = "nearest"
    return L


def render_panel(name, width, height, duration, draw):
    """draw(img, t) paints one panel frame; frames are piped to ffmpeg as RGBA and stored with alpha (png in mov)."""
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{name}.mov"
    n = round(duration * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{width}x{height}",
                          "-r", str(FPS), "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(out)], stdin=subprocess.PIPE)
    last, last_bytes = None, None
    for i in range(n):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        key = draw(img, i / FPS)
        if key is not None and key == last:
            p.stdin.write(last_bytes)
            continue
        b = img.tobytes()
        last, last_bytes = key, b
        p.stdin.write(b)
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit("panel encode failed: " + name)
    return str(out.relative_to(REEL))


def panel_layer(src, x, y, w, h, t0, t1):
    return {"kind": "video", "src": src, "ss": 0, "x": x, "y": y, "w": w, "h": h, "t": [t0, t1]}


def card_lines(x, y, w, lines, t_in, size=52, title=None, t_out=None, mono=False, line_h=None, fill=CARD, colors=None):
    """A white card with lines of text (title optional), revealed at t_in."""
    lh = line_h or int(size * 1.45)
    h = (lh * len(lines)) + (130 if title else 60)
    out = [rect(x, y, w, h, fill=fill, t_in=t_in, t_out=t_out)]
    yy = y + 40
    if title:
        out.append(text(title, x + 48, yy, 60, INK, "serif", w=w - 96, t_in=t_in, t_out=t_out))
        yy += 100
    for k, ln in enumerate(lines):
        colour = (colors[k] if colors else None) or (SPARK if ln.startswith("FAIL") else INK)
        out.append(text(ln, x + 48, yy, size, colour, "mono" if mono else "sans", w=w - 96, t_in=t_in, t_out=t_out))
        yy += lh
    return out, h


def save_png(im, name):
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{name}.png"
    im.save(out)
    return str(out.relative_to(REEL))


def crop_png(src, box, scale, name, rings=()):
    im = Image.open(src).convert("RGB").crop(box)
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for (px, py), colour in rings:      # rings mark sampled pixels (source pixel centres)
        cx, cy = (px - box[0] + 0.5) * scale, (py - box[1] + 0.5) * scale
        r = scale * 2.2
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=colour, width=max(3, scale // 2))
    return save_png(im, name)


def take_frame_png(frame, box, scale, name):
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{name}.png"
    x0, y0, x1, y1 = box
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{frame / FPS:.4f}", "-i", str(REEL / TAKE), "-vf",
                    f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0},scale={(x1 - x0) * scale}:{(y1 - y0) * scale}:flags=lanczos",
                    "-frames:v", "1", str(out)], check=True)
    return str(out.relative_to(REEL))


def rel(p: Path) -> str:
    return f"{REPO_REL}/{p.relative_to(REPO).as_posix()}"


# ---------------------------------------------------------------- beats

def readout_panel(name, take, frame_at, duration, width=614, height=1555):
    """Per-frame readout from the take's own track log; frame_at(t) gives the take frame shown at beat time t."""
    f_t, f_s, f_l = font("serif", 72), font("sans", 40), font("sans", 44)

    def draw(img, t):
        fr = frame_at(t)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, width - 1, height - 1), 28, fill=CARD, outline=BORDER, width=3)
        d.text((40, 36), "The tint, live", font=f_t, fill=INK)
        d.text((42, 130), "from the take's own", font=f_s, fill=SOFT)
        d.text((42, 178), "per-frame log", font=f_s, fill=SOFT)
        d.line((40, 248, width - 40, 248), fill=BORDER, width=3)
        if fr is None:
            return ("none",)
        r = take.row(fr)
        amt = r["amount"]
        rows = [("hurt_amount", f"{amt:.4f}", AMBER if amt > 0 else GHOST),
                ("player.iframes", str(r["iframes"]), INK if r["iframes"] else GHOST),
                ("red blink", "on" if r["red"] else "off", SPARK if r["red"] else GHOST),
                ("state", STATE[r["state"]], INK),
                ("hp", str(r["hp"]), INK),
                ("monster touching", "yes" if r["contact"] else "no", SPARK if r["contact"] else GHOST)]
        y = 285
        for label, value, colour in rows:
            d.text((44, y), label, font=f_l, fill=SOFT)
            size = 84
            while size > 44 and d.textlength(value, font=font("serif-medium", size)) > width - 88:
                size -= 4
            d.text((44, y + 50), value, font=font("serif-medium", size), fill=colour)
            y += 205
        d.text((44, height - 70), f"take frame {fr}", font=f_s, fill=GHOST)
        return (amt, r["iframes"], r["red"], r["state"], r["hp"], r["contact"], fr)
    return render_panel(name, width, height, duration, draw)


def curve_strip(name, take, f0, f1, frame_at, duration, width, height=200):
    """hurt_amount per frame for take frames f0..f1, as bars, with a playhead."""
    f_s = font("sans", 40)

    def draw(img, t):
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, width - 1, height - 1), 20, fill=CARD, outline=BORDER, width=3)
        d.text((28, 12), f"hurt_amount per frame, take frames {f0}–{f1} (from the take's log; 1.0 at the top)", font=f_s, fill=SOFT)
        x0, x1, y0, y1 = 28, width - 28, 70, height - 18
        n = f1 - f0
        for i in range(n):
            r = take.row(f0 + i)
            xa = x0 + (x1 - x0) * i / n
            xb = x0 + (x1 - x0) * (i + 1) / n
            d.rectangle((xa, y0, xb, y1), fill="#ECE9E0" if r["state"] == 1 else "#D9D6E8")
            if r["amount"] > 0:
                d.rectangle((xa, y1 - (y1 - y0) * r["amount"], xb, y1), fill="#E3B23C")
        fr = frame_at(t)
        if fr is not None and f0 <= fr < f1:
            xp = x0 + (x1 - x0) * (fr - f0) / n
            d.rectangle((xp - 4, y0 - 8, xp + 4, y1 + 8), fill=INK)
        return (fr,)
    return render_panel(name, width, height, duration, draw)


def b03():
    take = Take()
    f0, f1 = 1240, 1420
    d = (f1 - f0) / FPS
    panel = readout_panel("B03-readout", take, lambda t: f0 + int(t * FPS), d)
    layers = frame_chrome("The tint, with the game's sound", f"Real engine capture, hurt take · seed 5 · scripted input · source revision {SHA}",
                          "readout from the take's per-frame log")
    layers += [video(f0, PAD, TOP, 2764, 1555), panel_layer(panel, 3015, TOP, 614, 1555, 0, d)]
    spec_write("B03", layers, d, audio="video")


def b06():
    d = dur("B06")
    white = CAP / "hurt-tint/20261030-125036"
    red = CAP / "hurt-tint/20261030-125259-red"
    W_ = json.loads((white / "captures.json").read_text())["captures"]
    R_ = json.loads((red / "captures.json").read_text())["captures"]
    box, sc = (604, 310, 676, 382), 8                     # the courier at 2x, centred on the sampled texels
    rings = [((649, 347), (217, 119, 87)), ((641, 363), (80, 200, 255))]
    t_half, t_red, t_two = at("B06", "At one half"), at("B06", "red phase"), at("B06", "two point oh")
    layers = frame_chrome("Predicted, then measured",
                          "In-engine captures · captures/hurt-tint/20261030-125036 (white) and 20261030-125259-red",
                          "debug key, simulation frozen: a fixture, not play")
    cw = (box[2] - box[0]) * sc
    for row, (caps, t0, label, folder) in enumerate([(W_, 0.0, "white phase", white), (R_, t_red, "red phase · iframes 27", red)]):
        y = TOP + 70 + row * 740
        layers.append(text(label, PAD, y - 66, 48, SOFT, "sans-medium", t_in=t0))
        for k, c in enumerate([c for c in caps if c["hurt_amount_set"] in (0.0, 0.5, 1.0)]):
            src = crop_png(folder / c["file"], box, sc, f"B06-{row}-{k}", rings)
            x = PAD + k * (cw + 40)
            layers.append(image(src, x, y, cw, cw, t_in=t0, nearest=True))
            layers.append(text(f"hurt_amount {c['hurt_amount_set']:g}", x, y + cw + 8, 48, INK, t_in=t0))
    tx = PAD + 3 * (cw + 40) + 10
    tw = RIGHT - tx
    pred = {("w", 0): ("242, 184, 75", "46, 58, 89"), ("w", 0.5): ("248.5, 219.5, 37.5", "150.5, 156.5, 44.5"),
            ("w", 1): ("255, 255, 0", "255, 255, 0"), ("r", 0): ("242, 82.8, 33.75", "46, 26.1, 40.05"),
            ("r", 0.5): ("248.5, 168.9, 16.875", "150.5, 140.55, 20.025"), ("r", 1): ("255, 255, 0", "255, 255, 0")}
    meas = {}
    for ph, caps in (("w", W_), ("r", R_)):
        for c in caps:
            if c["hurt_amount_set"] in (0.0, 0.5, 1.0):
                meas[(ph, c["hurt_amount_set"])] = (", ".join(map(str, c["samples"]["lamp"]["rgb"])),
                                                    ", ".join(map(str, c["samples"]["coat"]["rgb"])))
    layers += [rect(tx, TOP, tw, 1170), text("Hand table → engine", tx + 44, TOP + 30, 64, INK, "serif"),
               text("orange ring: lamp texel (20, 16) · blue ring: coat texel (16, 24)", tx + 44, TOP + 112, 44, SOFT, w=tw - 88)]
    y = TOP + 200
    for ph, t0 in (("w", 0.0), ("r", t_red)):
        for a in (0, 0.5, 1):
            tt = t0 if a != 0.5 or ph == "r" else t_half
            pl, pc = pred[(ph, a)]
            ml, mc = meas[(ph, float(a))]
            layers.append(text(f"{'white' if ph == 'w' else 'red'} {a:g}", tx + 30, y, 44, SOFT, "sans-medium", t_in=tt))
            layers.append(text(f"lamp {pl} → {ml}", tx + 250, y, 44, INK, "mono", t_in=tt))
            layers.append(text(f"coat {pc} → {mc}", tx + 250, y + 58, 44, INK, "mono", t_in=tt))
            y += 156
    two = next(c for c in W_ if c["hurt_amount_set"] == 2.0)
    src2 = crop_png(white / two["file"], box, 3, "B06-two", rings)
    yb = TOP + 1200
    layers += [rect(tx, yb, tw, 1555 - 1200, t_in=t_two),
               image(src2, tx + 30, yb + 40, 216, 216, t_in=t_two, nearest=True),
               text(f"set {two['hurt_amount_set']:.1f} from code → read back {two['hurt_amount_read_back']:.1f}: not clamped",
                    tx + 280, yb + 36, 48, INK, "sans-medium", w=tw - 310, t_in=t_two),
               text("both texels (255, 255, 0), like 1.0: the ideal lamp (268, 326, −75) saturates in 8-bit output",
                    tx + 280, yb + 160, 44, SOFT, w=tw - 310, t_in=t_two)]
    spec_write("B06", layers, d)


def b08():
    take = Take()
    d = dur("B08")
    a0, a1 = 1490, 1700                     # real speed: hit 2, pause, resume, hit 3, ignored contact, zero
    real_a = (a1 - a0) / FPS
    holds = [1653, 1657, 1661, 1665, 1669, 1673, 1677]
    c0, c1 = 1645, 1711
    real_c = (c1 - c0) / FPS
    span = (d - real_a - real_c) / len(holds)
    segs = [(0.0, real_a, a0, True)] + [(real_a + k * span, real_a + (k + 1) * span, fr, False) for k, fr in enumerate(holds)] + \
           [(d - real_c, d + 1, c0, True)]

    def frame_at(t):
        for s0, s1, f, moving in segs:
            if s0 <= t < s1:
                return f + int((t - s0) * FPS) if moving else f
        return None
    hit3 = take.find("hit", n=3)[0]["pf"]
    r = take.row(a0)
    cx, cy = r["x"] * 6, r["y"] * 6
    cw, ch = 1280, 620
    crop = [cx - cw / 2, cy - ch / 2 - 20, cw, ch]
    vw, vh = 2764, round(2764 * ch / cw)
    panel = readout_panel("B08-readout", take, frame_at, d)
    strip_a = curve_strip("B08-curve", take, a0, c1, frame_at, d, vw)
    layers = frame_chrome("Yellow, then fading, in play", f"Real engine capture, hurt take · seed 5 · {cw}×{ch} crop of the 4K frame, 2.16× · source revision {SHA}",
                          "scripted input · held frames labelled")
    layers.append(video(a0, PAD, TOP, vw, vh, 0.0, real_a, crop=crop))
    layers.append(text("real engine capture · scripted input through the real input map · real speed", PAD, TOP - 66, 46, SOFT, t_out=real_a, fade=0.1))
    for k, fr in enumerate(holds):
        t0 = real_a + k * span
        src = take_frame_png(fr, (int(crop[0]), int(crop[1]), int(crop[0] + cw), int(crop[1] + ch)), 2, f"B08-h{fr}")
        layers.append(image(src, PAD, TOP, vw, vh, t0, t0 + span, fade=0.0))
        ms = (fr - hit3) / FPS
        layers.append(text(f"held frame · take frame {fr} · {ms:.2f} s after hit 3", PAD, TOP - 66, 46, SOFT, t_in=t0, t_out=t0 + span, fade=0.0))
    layers.append(video(c0, PAD, TOP, vw, vh, d - real_c, d, crop=crop))
    layers.append(text("replay of take frames 1645–1710, real speed", PAD, TOP - 66, 46, SOFT, t_in=d - real_c, fade=0.1))
    layers.append(panel_layer(strip_a, PAD, TOP + vh + 20, vw, 200, 0, d))
    layers.append(panel_layer(panel, 3015, TOP, 614, 1555, 0, d))
    spec_write("B08", layers, d)


def b10():
    d = dur("B10")
    cap = CAP / "a5-materials/20261030-170452-pair"
    meta = json.loads((cap / "captures.json").read_text())
    png = cap / "pair.png"
    im = Image.open(png).convert("RGB")
    d_ = ImageDraw.Draw(im)
    fl, st = [682, 496, 56, 56], [563, 316, 16, 32]
    big = im.resize((2560, 1440), Image.LANCZOS)
    dd = ImageDraw.Draw(big)
    for (x, y, w, h), col in ((fl, (217, 119, 87)), (st, (80, 200, 255))):
        dd.rectangle((x * 2 - 6, y * 2 - 6, (x + w) * 2 + 6, (y + h) * 2 + 6), outline=col, width=8)
    src = save_png(big, "B10-pair")
    floor_c = crop_png(png, (600, 440, 820, 600), 3, "B10-floor")
    stand_c = crop_png(png, (535, 280, 607, 380), 5, "B10-stand")
    t_f, t_s, t_c = at("B10", "The floor"), at("B10", "The stand-in"), at("B10", "fixed camera pose")
    layers = frame_chrome("The room, in the engine", "Real engine capture · a5-materials/20261030-170452-pair · capture_a5_materials.gd --pair",
                          f"revision {SHA} · scripted, no input")
    layers.append(image(src, PAD, TOP, 2560, 1440))
    x = PAD + 2600
    wr = RIGHT - x
    layers += [rect(x, TOP, wr, 1440),
               text("Floor/Mesh", x + 40, TOP + 30, 56, SPARK, "sans-medium", t_in=t_f),
               text("cobblestone_warm_floor.tres", x + 40, TOP + 100, 44, INK, w=wr - 80, t_in=t_f),
               image(floor_c, x + 40, TOP + 160, wr - 80, round((wr - 80) * 160 / 220), t_in=t_c),
               text("StandIn/Mesh", x + 40, TOP + 740, 56, "#3A8FC7", "sans-medium", t_in=t_s),
               text("cobblestone_cool_standin.tres", x + 40, TOP + 810, 44, INK, w=wr - 80, t_in=t_s),
               image(stand_c, x + 40 + (wr - 80 - 360) // 2, TOP + 880, 360, 500, t_in=t_c)]
    layers.append(text(f"floor mean RGB {tuple(meta['captures'][0]['floor_mean_rgb'])} · stand-in mean RGB {tuple(meta['captures'][0]['standin_mean_rgb'])} · "
                       "camera pose fixed in capture_a5_materials.gd", PAD, TOP + 1470, 44, SOFT, w=3418))
    spec_write("B10", layers, d)


def b12():
    d = dur("B12")
    cap = CAP / "a5-materials/20261030-170456-one-material"
    md = (cap / "CAPTURES.md").read_text()
    a, b = cap / "one-material-baseline.png", cap / "one-material-floor-uv_scale-4.0.png"
    t_c, t_m = at("B12", "smaller and denser"), at("B12", "single level")
    layers = frame_chrome("One material changed, one not", "Real engine captures · captures/a5-materials/20261030-170456-one-material",
                          f"revision {SHA} · value set in memory, never saved")
    layers += [image(rel(a), PAD, TOP, 1680, 945), image(rel(b), PAD + 1738, TOP, 1680, 945),
               text("floor uv_scale 2.0 (the material's value)", PAD, TOP + 960, 48, INK, "sans-medium"),
               text("floor uv_scale 4.0, in memory", PAD + 1738, TOP + 960, 48, SPARK, "sans-medium")]
    fa = crop_png(a, (560, 430, 860, 600), 3, "B12-fa")
    fb = crop_png(b, (560, 430, 860, 600), 3, "B12-fb")
    layers += [image(fa, PAD, TOP + 1040, 900, 510, t_in=t_c, nearest=True), image(fb, PAD + 940, TOP + 1040, 900, 510, t_in=t_c, nearest=True)]
    line = next(l for l in md.splitlines() if l.startswith("Max per-channel"))
    layers += [rect(PAD + 1900, TOP + 1040, RIGHT - PAD - 1900, 510, t_in=t_m),
               text("Measured, pixel by pixel", PAD + 1950, TOP + 1080, 60, INK, "serif", t_in=t_m),
               text(line, PAD + 1950, TOP + 1180, 50, INK, "sans-medium", w=RIGHT - PAD - 2000, t_in=t_m),
               text("the stand-in shares the shader, not the material", PAD + 1950, TOP + 1380, 44, SOFT, w=RIGHT - PAD - 2000, t_in=t_m)]
    spec_write("B12", layers, d)


def b14():
    d = dur("B14")
    pred_md = repo_text("evidence/assignment-5/bao-shader-edit/PREDICTION.md", RECORDS_REV).splitlines()
    pred = next(l for l in pred_md if l.startswith("> ")).lstrip("> ").strip()
    obs = bao_quote("Bao's observation: ")
    base = CAP / "a5-materials/20261030-131249-compare-shader-baseline/compare-shader-baseline.png"
    edit = CAP / "a5-materials/20261030-163723-compare-shader-bao-edit/compare-shader-bao-edit.png"
    green = CAP / "a5-materials/20261030-single-line-study/edited/compare-shader-edited.png"
    t1, t2, t3, t4 = (at("B14", "edited line nineteen"), at("B14", "Every pixel"), at("B14", "observation"),
                      at("B14", "earlier Codex run"))
    layers = frame_chrome("Change the shader, both move", "Real engine captures · a5-materials/…-131249 baseline, …-163723 Bao's edit",
                          "captured at e5c0272, before line 22 changed")
    layers += [rect(PAD, TOP, 3418, 945, fill=PAGE, outline=BORDER),
               text("Bao's prediction, recorded before the edit (PREDICTION.md, 16:32 EDT)", PAD + 60, TOP + 60, 52, SOFT, "serif", t_out=t1),
               text(f"“{pred}”", PAD + 60, TOP + 190, 64, INK, "serif", w=3300, spacing=1.35, t_out=t1)]
    layers += [image(rel(base), PAD, TOP, 1680, 945, t_in=t1), image(rel(edit), PAD + 1738, TOP, 1680, 945, t_in=t1),
               text("baseline", PAD, TOP + 960, 48, INK, "sans-medium", t_in=t1),
               text("Bao's edit: line 19 … * 0.5, then restored with git", PAD + 1738, TOP + 960, 48, SPARK, "sans-medium", t_in=t1)]
    yb, hb = TOP + 1050, 505
    lines = ["floor     (99.76, 90.44, 114.73) → (52.83, 46.55, 63.29)",
             "stand-in  (31.63, 40.98, 74.74)  → (12.36, 16.99, 35.66)",
             "every pixel in both rectangles changed"]
    card, _ = card_lines(PAD, yb, 1680, lines, t2, size=44, mono=True, title="Measured means (RGB)", line_h=72)
    layers += card
    layers += [rect(PAD + 1738, yb, 1680, hb, t_in=t3),
               text("Bao's observation (TEST-REPORT.md)", PAD + 1786, yb + 36, 52, SOFT, "serif", t_in=t3),
               text(f"“{obs}”", PAD + 1786, yb + 130, 54, INK, "serif", w=1590, spacing=1.3, t_in=t3)]
    layers += [rect(PAD - 10, yb - 10, 1700, hb + 30, fill=PAGE, outline=PAGE, radius=0, t_in=t4),
               rect(PAD, yb, 1680, hb, fill="#FBEFEA", outline=SPARK, t_in=t4),
               image(rel(green), PAD + 30, yb + 30, 790, 445, t_in=t4),
               text("AGENT RUN (Codex session)", PAD + 850, yb + 40, 46, SPARK, "sans-medium", t_in=t4),
               text("ALBEDO × vec3(0, 1, 0): both objects green. It edited Bao's cobblestone shader, then restored it byte for byte, "
                    "breaking the rule that no agent edits godot/shaders/.", PAD + 850, yb + 110, 44, INK, w=790, t_in=t4)]
    spec_write("B14", layers, d)


def b16():
    d = dur("B16")
    tex = REPO / "godot/assets/textures/cobblestone_floor_08"     # committed files; identical at the film revision
    sweep = CAP / "a5-materials/20261030-170453-sweep"
    t_curl, t_ns = at("B16", "curl ratio"), at("B16", "normal strength zero")
    layers = frame_chrome("Three files, three kinds of data", "godot/assets/textures/cobblestone_floor_08/ (Poly Haven, CC0) · curl-calibration.log",
                          f"sweep 20261030-170453 at {SHA}")
    maps = [("diff", ":3  color_tex · source_color", "colour"), ("nor_gl", ":4  normal_tex · hint_normal", "directions"),
            ("rough", ":5  roughness_tex · no colour hint", "raw numbers")]
    for k, (m, lab, kind) in enumerate(maps):
        x = PAD + k * 1209
        layers += [image(rel(tex / f"cobblestone_floor_08_{m}_1k.png"), x, TOP, 1000, 1000, t_out=t_ns),
                   text(lab, x, TOP + 1010, 44, INK, "mono", t_out=t_ns),
                   text(kind, x, TOP + 1070, 44, SOFT, t_out=t_ns)]
    log = (REPO / "evidence/assignment-5/textures/curl-calibration.log").read_text().splitlines()
    rows = [l for l in log if l.startswith("nor_")]
    card, _ = card_lines(PAD, TOP + 1150, 3418, rows + ["low = the file's own convention: the GL map is a real surface read the OpenGL way, as Godot expects"],
                         t_curl, size=46, mono=False, title="Recorded: curl_ratio, both conventions (normal_map_check.gd)", line_h=64)
    layers += [rect(PAD - 10, TOP + 1140, 3440, 430, fill=PAGE, outline=PAGE, radius=0, t_in=t_curl)] + card
    box = (520, 420, 1120, 700)
    for k, v in enumerate(("0.00", "1.00")):
        src = crop_png(sweep / f"sweep-normal_strength-{v}.png", box, 2, f"B16-ns{v}")
        x = PAD + k * 1738
        layers += [image(src, x, TOP, 1680, 784, t_in=t_ns),
                   text(f"floor normal_strength {float(v):g}" + (" (the material's value)" if v == "1.00" else ""), x, TOP + 800, 46, INK, "sans-medium", t_in=t_ns)]
    spec_write("B16", layers, d)


def b18():
    d = dur("B18")
    sweep = CAP / "a5-materials/20261030-170453-sweep"
    meta = json.loads((sweep / "captures.json").read_text())["captures"]
    rows = [("uv_scale", ["0.25", "2.00", "4.00"]), ("roughness_min", ["0.00", "0.55", "1.00"]),
            ("roughness_max", ["0.00", "0.95", "1.00"]), ("normal_strength", ["0.00", "1.00", "2.00"]),
            ("tint", ["0.00_0.00_0.00", "1.00_0.92_0.80", "1.00_1.00_1.00"])]
    by_file = {c["file"]: c for c in meta}
    t_uv, t_r, t_n, t_t, t_s = (at("B18", "U v scale"), at("B18", "roughness ends"), at("B18", "normal"),
                                at("B18", "black tint"), at("B18", "never moves"))
    t_n = at("B18", "normal strength sets")
    t_look = at("B18", "Bao's look")
    # (row shown, start, end): the five rows in narration order, then the normal_strength row again for Bao's look
    segs = [(0, 0.0, t_r), (1, t_r, t_r + (t_n - t_r) / 2), (2, t_r + (t_n - t_r) / 2, t_n), (3, t_n, t_t),
            (4, t_t, t_look), (3, t_look, d)]
    layers = frame_chrome("Five numbers, one at a time", "Real engine captures · a5-materials/20261030-170453-sweep · --sweep",
                          f"revision {SHA} · floor material only, values in memory")
    iw, ih = 1100, 619
    for k, s0, s1 in segs:
        name, vals = rows[k]
        for j, v in enumerate(vals):
            f = f"sweep-{name}-{v}.png"
            x = PAD + j * (iw + 59)
            layers.append(image(rel(sweep / f), x, TOP, iw, ih, s0, s1, fade=0.0))
            c = by_file[f]
            label = (v.replace("_", ", ") if name == "tint" else v) + (" · material" if c["setting"].get("is_material_value") else "")
            layers.append(text(f"{name} {label}", x, TOP + ih + 10, 44, SPARK if c["setting"].get("is_material_value") else INK,
                               "sans-medium", t_in=s0, t_out=s1, fade=0.0))
    ty = TOP + ih + 90
    layers.append(rect(PAD, ty, 3418, 1555 - ih - 90))
    layers.append(text("floor mean RGB: low / material / high", PAD + 50, ty + 30, 48, SOFT, "sans-medium"))
    layers.append(text("stand-in mean RGB", PAD + 2700, ty + 30, 48, SOFT, "sans-medium"))
    for k, s0, s1 in segs:
        y = ty + 110 + k * 120
        layers.append(rect(PAD + 20, y - 14, 3378, 104, fill="#F2E5D8", outline="#F2E5D8", radius=10, t_in=s0, t_out=s1, fade=0.0))
    for k, (name, vals) in enumerate(rows):
        y = ty + 110 + k * 120
        means = [tuple(by_file[f"sweep-{name}-{v}.png"]["floor_mean_rgb"]) for v in vals]
        st = tuple(by_file[f"sweep-{name}-{vals[0]}.png"]["standin_mean_rgb"])
        cells = "   ".join(f"({m[0]:.0f}, {m[1]:.0f}, {m[2]:.0f})" for m in means)
        layers.append(text(name, PAD + 50, y, 46, INK, "sans-medium"))
        layers.append(text(cells, PAD + 620, y, 44, INK, "mono"))
        layers.append(text(f"({st[0]:.2f}, {st[1]:.2f}, {st[2]:.2f})", PAD + 2700, y, 44, GOOD, "mono"))
    layers.append(text("tint row: black · warm (material) · white. The stand-in column never changes.",
                       PAD + 50, ty + 110 + 5 * 120, 44, SOFT, w=3300, t_in=t_s, t_out=t_look))
    look = bao_quote("Bao's look at the new `normal_strength` row: ")
    layers.append(text(f"Bao's look at the normal_strength row (TEST-REPORT.md): “{look}”",
                       PAD + 50, ty + 100 + 5 * 120, 44, INK, w=3300, t_in=t_look))
    spec_write("B18", layers, d)


def b20():
    d = dur("B20")
    cap = CAP / "a5-materials/20261030-131056-hint"
    meta = json.loads((cap / "captures.json").read_text())["captures"][0]
    t_m, t_p = at("B20", "Measured"), at("B20", "still a prediction")
    layers = frame_chrome("The hint, measured", "Real engine capture · a5-materials/20261030-131056-hint at d01df00 (hint shader unchanged at 4246f94)",
                          "predictions: CHANGE-BRIEF.md")
    layers += [rect(PAD, TOP, 3418, 520), text("Predicted (CHANGE-BRIEF.md, source-colour hint experiment)", PAD + 50, TOP + 30, 56, INK, "serif")]
    hdr = ["quad", "Compatibility (this project)", "Forward+ / Mobile (linear)", "measured, Compatibility"]
    xs = [PAD + 50, PAD + 700, PAD + 1600, PAD + 2500]
    for x, h in zip(xs, hdr):
        layers.append(text(h, x, TOP + 140, 44, SOFT, "sans-medium"))
    q = meta["quads"]
    rows = [("with source_color", "64 · 128 · 192", "64 · 128 · 192", q["QuadWithSourceColor"]),
            ("no hint", "64 · 128 · 192", "137 · 188 · 225", q["QuadWithoutHint"])]
    for k, (name, comp, fwd, quad) in enumerate(rows):
        y = TOP + 240 + k * 110
        m = " · ".join(str(b["rgb"][0]) for b in quad["bands"])
        layers += [text(name, xs[0], y, 50, INK, "mono"), text(comp, xs[1], y, 50, INK, "mono"),
                   text(fwd, xs[2], y, 50, INK, "mono"), text(m, xs[3], y, 50, GOOD, "sans-medium", t_in=t_m)]
    layers.append(text("predicted, not measured here", xs[2], TOP + 450, 44, SPARK, "sans-medium", t_in=t_p))
    img = Image.open(cap / "hint-experiment.png").convert("RGB")
    big = img.resize((1920, 1080), Image.NEAREST)
    dd = ImageDraw.Draw(big)
    f_ = font("sans-medium", 34)
    for quad in q.values():
        for b in quad["bands"]:
            x, y = b["pixel"][0] * 1.5, b["pixel"][1] * 1.5
            ink = (255, 255, 255) if b["rgb"][0] < 100 else (20, 20, 20)
            dd.ellipse((x - 14, y - 14, x + 14, y + 14), outline=(217, 119, 87), width=5)
            dd.text((x - 30, y + 30), str(b["rgb"][0]), font=f_, fill=ink)
    src = save_png(big.crop((0, 180, 1920, 900)), "B20-hint")
    layers += [image(src, PAD, TOP + 560, 2640, 990, t_in=t_m),
               text("band centres sampled 80 px from the edges · Linear tonemap, exposure 1 · rings: sampled pixels", PAD + 2700, TOP + 600,
                    44, SOFT, w=718, t_in=t_m)]
    spec_write("B20", layers, d)


def b22():
    d = dur("B22")
    D = REEL / "capture/shader-pair"
    diff = json.loads((D / "diff.json").read_text())
    t_f, t_face, t_tilt = at("B22", "labelled fixture"), at("B22", "Face-on"), at("B22", "Tilt the camera")
    layers = frame_chrome("Two writers, same jobs", "Lines verbatim from godot/shaders/ at " + SHA + " · fixture: capture/shader_pair_fixture.gd on an isolated copy",
                          "agent-made film fixture, not gameplay")
    pairs = [("generated :7 ", excerpt("shaders/standard_generated.gdshader", 7, 7)), ("Bao :3       ", excerpt("shaders/cobblestone_surface.gdshader", 3, 3)),
             ("generated :19", excerpt("shaders/standard_generated.gdshader", 19, 19)), ("Bao :4       ", excerpt("shaders/cobblestone_surface.gdshader", 4, 4)),
             ("generated :35", excerpt("shaders/standard_generated.gdshader", 35, 35).strip()), ("Bao :19      ", excerpt("shaders/cobblestone_surface.gdshader", 19, 19).strip())]
    layers.append(rect(PAD, TOP, 3418, 1555, t_out=t_f))
    layers.append(text("Verbatim lines, generated (standard_generated.gdshader) vs Bao's (cobblestone_surface.gdshader)", PAD + 50, TOP + 40, 52, INK, "serif", t_out=t_f))
    y = TOP + 170
    for k, (lab, line) in enumerate(pairs):
        layers.append(text(lab, PAD + 50, y, 44, SPARK if k % 2 else SOFT, "mono", t_out=t_f))
        layers.append(text(line, PAD + 450, y, 44, INK, "mono", w=2950, t_out=t_f))
        y += 120 if k % 2 == 0 else 200
    layers.append(text("hint_roughness_normal (generated :19) and hint_normal (Bao :4): both mark normal data, neither is source_color",
                       PAD + 50, TOP + 1400, 44, SOFT, w=3300, t_out=t_f))

    def side(pose, rect_key):
        g = np.asarray(Image.open(D / f"control-generated-{pose}.png").convert("RGB")).astype(int)
        b = np.asarray(Image.open(D / f"control-bao-{pose}.png").convert("RGB")).astype(int)
        x, y0, w, h = diff[f"{pose}-left"]["rect"]
        G, B = g[y0 + 2:y0 + h - 2, x + 2:x + w - 2], b[y0 + 2:y0 + h - 2, x + 2:x + w - 2]
        dm = np.clip(np.abs(G - B).max(axis=2) * 8, 0, 255).astype(np.uint8)
        heat = np.stack([dm, (dm * 0.47).astype(np.uint8), (dm * 0.34).astype(np.uint8)], axis=2)
        return (save_png(Image.fromarray(G.astype(np.uint8)), f"B22-{pose}-gen"), save_png(Image.fromarray(B.astype(np.uint8)), f"B22-{pose}-bao"),
                save_png(Image.fromarray(heat), f"B22-{pose}-diff"), G.shape)
    for pose, t0, t1 in (("straight", t_f, t_tilt), ("tilted", t_tilt, d)):
        g, b, h_, shape = side(pose, "left")
        hh, ww = shape[0], shape[1]
        size_w = 1100
        size_h = round(size_w * hh / ww)
        for k, (src, lab) in enumerate([(g, "editor-generated material (scratch scene)"), (b, "Bao's shader, neutral values"),
                                        (h_, "|difference| × 8")]):
            x = PAD + k * (size_w + 59)
            layers.append(image(src, x, TOP, size_w, size_h, t0, t1, fade=0.0))
            layers.append(text(lab, x, TOP + size_h + 10, 44, INK, "sans-medium", w=size_w, t_in=t0, t_out=t1, fade=0.0))
        m = [diff[f"{pose}-{s}"] for s in ("left", "right")]
        pct = [100 * v["within_2_px"] / v["compared_px"] for v in m]
        line = (f"{'face-on (|NORMAL.z| = 1)' if pose == 'straight' else 'camera tilted 50° (|NORMAL.z| = cos 50° ≈ 0.64)'}: "
                f"{min(pct):.0f}–{max(pct):.0f} % of pixels within 2 levels · mean |difference| {min(v['mean_abs_delta'] for v in m):.1f}–{max(v['mean_abs_delta'] for v in m):.1f} · "
                f"max {max(v['max_channel_delta'] for v in m)}")
        yb = TOP + size_h + 90
        layers += [rect(PAD, yb, 3418, 1555 - size_h - 90, t_in=t0, t_out=t1, fade=0.0),
                   text(line, PAD + 50, yb + 40, 46, INK, "sans-medium", w=3300, t_in=t0, t_out=t1, fade=0.0),
                   text("Compared plane by plane across two renders (same pixels). Same three maps, 2 × 2 m plane, one directional light, "
                        "orthographic camera; values set in memory, nothing saved.", PAD + 50, yb + 140, 44, SOFT, w=3300, t_in=t0, t_out=t1, fade=0.0)]
    spec_write("B22", layers, d)


def b25():
    d = dur("B25")
    run = (REEL / "capture/test-run-film-build-raw.txt").read_text().splitlines()
    t_all, t_mut, t_head = at("B25", "One twenty-seven"), at("B25", "three mutations"), at("B25", "no headless run")
    rows = ["fps   checks  first value  zero tick  game time  allowed"]
    for m in (30, 60, 144):
        j = json.loads((REEL / f"capture/test-run/json_test_hurt_tint_{m}.json").read_text())
        r = {x["id"]: x["observed"] for x in j["results"]}
        rows.append(f"{m:<5} {j['checks'] - j['failures']}/{j['checks']}   {r['hit-starts-window']['first_amount']:<11.4g}  "
                    f"{r['zero-after-48-ticks']['zero_tick']:<9}  {r['zero-after-48-ticks']['game_seconds']:.4f} s   {r['zero-after-48-ticks']['allowed']:.4f} s")
    card1, h1 = card_lines(PAD, TOP, 1990, rows, 0.0, size=44, mono=True, line_h=64,
                           title=f"Recorded: test_hurt_tint.gd, this film's run at {SHA}")
    suites = [l.split(" :: ")[1] for l in run if " :: " in l and "hurt_tint" not in l]
    card2, h2 = card_lines(PAD + 2050, TOP, 1368, suites + ["earlier ten: 332 checks, 0 failures"], t_all, size=40, mono=True, line_h=56,
                           title="Recorded: every other suite")
    mut_dir = REPO / "evidence/assignment-5/mutations"
    muts = []
    for f, label in (("semicolon_60fps.log", "semicolon removed from line 8"), ("rename_60fps.log", "hurt_amount renamed in the shader"),
                     ("source_color_60fps.log", "source_color removed from color_tex")):
        log = (mut_dir / f).read_text().splitlines()
        tot = next(l for l in log if " checks, " in l).split(" -> ")[0]
        muts.append(f"{label}:  {tot}")
    card3, h3 = card_lines(PAD, TOP + h1 + 40, 1990, muts + ["each made by Bao by hand, restored with git checkout"], t_mut, size=44, mono=False, line_h=66,
                           title="Recorded: Bao's three mutations (evidence/assignment-5/mutations)")
    head = next(l for l in repo_text("TEST-REPORT.md", "HEAD").splitlines() if l.startswith("Any colour, brightness"))
    card4, h4 = card_lines(PAD, TOP + h1 + h3 + 80, 3418, [head], t_head, size=46, line_h=130, fill="#FBEFEA",
                           title="What a headless run cannot show (TEST-REPORT.md)")
    layers = frame_chrome("What the tests proved", "Recorded tool output · capture/test-run-film-build-raw.txt (isolated copy at " + SHA + ")",
                          "evidence/assignment-5/mutations/*.log")
    layers += card1 + card2 + card3 + card4
    spec_write("B25", layers, d)


def b26():
    d = dur("B26")
    t_u, t_n = at("B26", "Still uncertain"), at("B26", "The next step")
    wrong = ["CLAUDE.md draft called the editor-generated particles shader hand-written · caught checking A6 records (8cd444a)",
             "driver test's one-frame tolerance was the window's largest delta (0.00806 s at 144) · caught reading the JSON (c0de4bd)",
             "audit's VRAM figure unmeasured; curl threshold 1.0 would pass a map with no surface · review (a3eaf2f)",
             "audit judged the Sky ambient source \"probably does not light\" the room · positive-control captures (481c703)",
             "first material room packed a copy of the A3 room; builder claimed Godot wrote UIDs · read before commit; audit",
             "evidence-split row put the hint experiment under the A3 lights · the audit (brief revision 10/30)",
             "a Codex session edited and restored godot/shaders/cobblestone_surface.gdshader (green study) · TEST-REPORT.md"]
    card1, h1 = card_lines(PAD, TOP, 2140, wrong, 0.0, size=44, line_h=170, title="What the agent got wrong (TEST-REPORT.md, rows shortened)")
    unc = ["source_color in Forward+/Mobile: predicted (137 / 188 / 225), not measured",
           "the F3 collision arc is tinted yellow too (accepted; player.gd out of scope)",
           "face-on, the fixture's two materials still differ by ~1 level on average: not isolated"]
    card2, h2 = card_lines(PAD + 2200, TOP, 1218, unc, t_u, size=44, line_h=175, title="Still uncertain")
    card3, h3 = card_lines(PAD + 2200, TOP + h2 + 40, 1218, ["Run the hint experiment on an isolated Forward+ copy and replace the prediction with numbers."],
                           t_n, size=44, line_h=180, title="One next step", fill="#EEF3EC")
    layers = frame_chrome("Mistakes, open questions, next", "TEST-REPORT.md, Assignment 5 · README.md Known limitations", "fixture residual: capture/shader-pair/diff.json")
    layers += card1 + card2 + card3
    spec_write("B26", layers, d)


def b27():
    d = dur("B27")
    t_c, t_p, t_r = at("B27", "Claude Code"), at("B27", "Poly Haven"), at("B27", "revision four")
    bao = ["hand-wrote hurt_tint (e0b47b4), cobblestone_surface (a8c804b), hint_experiment (5a7903a), and line 22 (0b91838)",
           "an earlier Codex draft of hurt_tint lived in a separate working copy; the yellow version is Bao's",
           "the brief: state, design, predictions, short answers; LANGUAGE-NOTES.md",
           "the three mutations, the editor conversion (43dfe20), the inherited scene, the PlaneMesh floor, the ambient decision",
           "every HUMAN CHECK, including the playtest report (TEST-REPORT.md):", ""]
    card1, h1 = card_lines(PAD, TOP, 1990, bao, 0.0, size=44, line_h=150, title="Bao (SOURCES.md, Assignment 5)")
    card1.append(text(f"“{bao_quote('after the playtest request: ')}”", PAD + 48, TOP + 140 + 5 * 150 - 24, 54, INK, "serif", w=1894))
    ai = ["Claude Code (Claude Opus 5.5): CLAUDE.md draft and review; the hurt-tint driver and test_hurt_tint.gd; the material audit and test_materials.gd; import script, builder, probes, capture tools, records — each plan approved by Bao",
          "Codex: set up the scratch conversion scene; the green single-line study",
          "This film (Claude Code): capture driver, shader-pair fixture, script and edit"]
    card2, h2 = card_lines(PAD + 2050, TOP, 1368, ai, t_c, size=44, line_h=290, title="AI contributions")
    credit = ["Texture: Cobblestone Floor 08 by Rob Tuytel, Poly Haven, CC0 (polyhaven.com/a/cobblestone_floor_08)",
              f"Source revision shown: {FULL_SHA}"]
    card3, h3 = card_lines(PAD, TOP + 1555 - 300, 3418, credit, t_p, size=44, line_h=72)
    layers = frame_chrome("Who did what", "SOURCES.md (Assignment 5) · godot/assets/textures/cobblestone_floor_08/ATTRIBUTION.md",
                          "Bao's words quoted as written")
    layers += card1 + card2 + card3
    spec_write("B27", layers, d)


BUILDERS = {"B03": b03, "B06": b06, "B08": b08, "B10": b10, "B12": b12, "B14": b14, "B16": b16, "B18": b18,
            "B20": b20, "B22": b22, "B25": b25, "B26": b26, "B27": b27}

if __name__ == "__main__":
    want = sys.argv[1:] or list(BUILDERS)
    for bid in want:
        BUILDERS[bid]()
