#!/usr/bin/env python3
"""Build media/<BID>.mp4 for every evidence and game-sound beat of the particle film (4K, 30 fps).

Everything shown is real: the 4K Movie Maker takes in capture/, the committed fixture strips, play-check shots and
recorded tool output in the repository, and the takes' own per-frame logs. Held frames and replays are labelled.
Layout follows the Assignment 2 film's evidence beats (same chrome, same compose.py).

    python3 tools/build_media.py [B05 B07 ...]
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
TOOLS = REEL / "tools"
WORK = REEL / "media" / "_work"
sys.path.insert(0, str(TOOLS))
from compose import FONT_FILES  # noqa: E402

W, H, FPS = 3840, 2160, 30
PAD, TITLE_Y, TOP, BOT = 211, 97, 346, 1901
INK, SOFT, GHOST, SPARK, PAGE, CARD, BORDER = "#3D3929", "#73705F", "#A9A491", "#D97757", "#FAF9F5", "#FFFFFF", "#E5E2D9"
GOOD, DARK = "#4F7A4A", "#202531"
SHA = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()[:7]
SHEET = json.loads((REEL / "beat_sheet.json").read_text())
BEATS = {b["beat_id"]: b for b in SHEET["beats"]}
REPO_REL = "../.."          # repository root, relative to the reel (compose.py resolves sources from the reel)
TAKES = {"main": ("capture/take-main-seed11.avi", "capture/take-main-seed11-log.jsonl"),
         "props": ("capture/take-props-seed11.avi", "capture/take-props-seed11-log.jsonl"),
         "study": ("capture/study-cpu-vs-gpu.avi", None)}
TAKE_NOTE = {"main": "main take · seed 11", "props": "props take · seed 11", "study": "study fixture · seed 7280"}
STATE = ["menu", "playing", "level-up cards", "paused", "won", "lost"]


def font(name, size):
    return ImageFont.truetype(str(FONT_FILES[name]), size)


class Take:
    def __init__(self, key):
        src, log = TAKES[key]
        self.key, self.src = key, src
        self.events = [json.loads(l) for l in (REEL / log).read_text().splitlines()]
        self.track = next(e for e in self.events if e["event"] == "track")["frames"]

    def find(self, event, **kw):
        return [e for e in self.events if e["event"] == event and all(e.get(k) == v for k, v in kw.items())]

    def row(self, frame):
        return self.track[max(0, min(frame, len(self.track) - 1))]

    def pos4k(self, frame):
        r = self.row(frame)
        return r[0] * 6, r[1] * 6


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


def rect(x, y, w, h, fill=CARD, outline=BORDER, width=3, radius=28, t_in=0.0, t_out=None):
    L = {"kind": "rect", "x": x, "y": y, "w": w, "h": h, "fill": fill, "outline": outline, "width": width, "radius": radius}
    if t_in or t_out is not None:
        L["t"] = [t_in, t_out if t_out is not None else 9999]
        L["fade"] = 0.25
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


def video(take, start_frame, x, y, w, h, t_in=0.0, t_out=None, crop=None, nearest=False, pad=0):
    L = {"kind": "video", "src": TAKES[take][0], "ss": start_frame / FPS, "x": x, "y": y, "w": w, "h": h,
         "t": [t_in, t_out if t_out is not None else 9999]}
    if crop:
        L["crop"] = [int(round(c)) for c in crop]
    if nearest:
        L["resample"] = "nearest"
    if pad:
        L["pad"] = pad
    return L


PADX = 700


def follow(take_key, take, f0, x, y, w, h, cw, ch, t_in=0.0, t_out=None):
    """A crop centred on the courier at the clip's first frame (the camera already follows him, so he stays put)."""
    cx, cy = take.pos4k(f0)
    x0 = min(max(0, cx - cw / 2 + PADX), W + 2 * PADX - cw)
    y0 = min(max(0, cy - ch / 2 + PADX), H + 2 * PADX - ch)
    return video(take_key, f0, x, y, w, h, t_in, t_out, crop=[x0, y0, cw, ch], pad=PADX)


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


def state_panel(name, take, segments, duration, width=614, height=1555, title="Effects, live"):
    """Per-frame readout from the take's own track log. segments: [(t0, t1, first_take_frame), ...]."""
    f_t, f_s, f_l, f_v = font("serif", 72), font("sans", 36), font("sans", 40), font("serif-medium", 92)
    hits = sorted(e["pf"] for e in take.find("hit"))

    def frame_at(t):
        for t0, t1, f0 in segments:
            if t0 <= t < t1:
                return f0 + int((t - t0) * FPS)
        return None

    def draw(img, t):
        fr = frame_at(t)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, width - 1, height - 1), 28, fill=CARD, outline=BORDER, width=3)
        d.text((40, 36), title, font=f_t, fill=INK)
        d.text((42, 130), "from the take's own", font=f_s, fill=SOFT)
        d.text((42, 178), "per-frame log", font=f_s, fill=SOFT)
        d.line((40, 248, width - 40, 248), fill=BORDER, width=3)
        if fr is None:
            return ("none",)
        r = take.row(fr)
        n_hits = sum(1 for h in hits if h <= fr)
        rows = [("Hit bursts alive", str(r[3]), SPARK if r[3] else GHOST),
                ("Trail", "emitting" if r[5] else "not emitting", SPARK if r[5] else GHOST),
                ("Celebrations alive", str(r[4]), SPARK if r[4] else GHOST),
                ("Game state", STATE[r[6]], INK),
                ("Hits so far", str(n_hits), INK)]
        y = 290
        for label, value, colour in rows:
            d.text((44, y), label, font=f_l, fill=SOFT)
            size = 92
            while size > 48 and d.textlength(value, font=font("serif-medium", size)) > width - 88:
                size -= 4
            d.text((44, y + 54), value, font=font("serif-medium", size), fill=colour)
            y += 246
        return (r[3], r[4], r[5], r[6], n_hits)
    return render_panel(name, width, height, duration, draw)


def emit_strip(name, take, f0, f1, segments, duration, width, height=150):
    """Timeline of the trail's emitting flag for take frames f0..f1, with a playhead."""
    f_s = font("sans", 34)

    def frame_at(t):
        for t0, t1, s in segments:
            if t0 <= t < t1:
                return s + int((t - t0) * FPS)
        return None

    def draw(img, t):
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, width - 1, height - 1), 20, fill=CARD, outline=BORDER, width=3)
        d.text((28, 14), "Trail emitting (per frame, from the take's log)", font=f_s, fill=SOFT)
        x0, x1, y0, y1 = 28, width - 28, 70, height - 24
        n = f1 - f0
        for i in range(n):
            on = take.row(f0 + i)[5]
            xa = x0 + (x1 - x0) * i / n
            xb = x0 + (x1 - x0) * (i + 1) / n
            d.rectangle((xa, y0, xb, y1), fill=SPARK if on else "#ECE9E0")
        fr = frame_at(t)
        if fr is not None and f0 <= fr < f1:
            xp = x0 + (x1 - x0) * (fr - f0) / n
            d.rectangle((xp - 4, y0 - 10, xp + 4, y1 + 10), fill=INK)
        return (fr,)
    return render_panel(name, width, height, duration, draw)


def card_lines(x, y, w, lines, t_in, size=52, title=None, t_out=None, mono=False, line_h=None):
    """A white card with lines of text (title optional), revealed at t_in."""
    lh = line_h or int(size * 1.45)
    h = (lh * len(lines)) + (130 if title else 60)
    out = [rect(x, y, w, h, t_in=t_in, t_out=t_out)]
    yy = y + 40
    if title:
        out.append(text(title, x + 48, yy, 64, INK, "serif", t_in=t_in, t_out=t_out))
        yy += 100
    for ln in lines:
        colour = SPARK if ln.startswith("FAIL") else INK
        out.append(text(ln, x + 48, yy, size, colour, "mono" if mono else "sans", w=w - 96, t_in=t_in, t_out=t_out))
        yy += lh
    return out, h


def strip_video(name, frames_dir, first, last, crop, scale):
    """Encode fixture PNG frames first..last (inclusive) into a real-speed 30 fps clip (cropped, nearest scale)."""
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{name}.mp4"
    x, y, w, h = crop
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-start_number", str(first),
                    "-i", str(frames_dir / "frame%08d.png"), "-frames:v", str(last - first + 1),
                    "-vf", f"crop={w}:{h}:{x}:{y},scale={w * scale}:{h * scale}:flags=neighbor",
                    "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(out)], check=True)
    return str(out.relative_to(REEL))


def crop_png(src, box, scale, name):
    WORK.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB").crop(box)
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    out = WORK / f"{name}.png"
    im.save(out)
    return str(out.relative_to(REEL))


def take_frame_png(take_key, frame, box, scale, name):
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{name}.png"
    x0, y0, x1, y1 = box
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(REEL / TAKES[take_key][0]), "-vf",
                    f"select=eq(n\\,{frame}),crop={x1 - x0}:{y1 - y0}:{x0}:{y0},scale={(x1 - x0) * scale}:{(y1 - y0) * scale}:flags=neighbor",
                    "-frames:v", "1", str(out)], check=True)
    return str(out.relative_to(REEL))


# ---------------------------------------------------------------- beats

def b03():
    take = Take("main")
    lv = take.find("levelup", level=5)[0]["pf"]
    f0, f1 = lv - 100, lv - 100 + 390
    d = (f1 - f0) / FPS
    panel = state_panel("B03-state", take, [(0, d, f0)], d)
    layers = frame_chrome("All three, with the game's sound", f"Real engine capture, {TAKE_NOTE['main']} · source revision {SHA}",
                          "readout from the take's per-frame log")
    layers += [video("main", f0, PAD, TOP, 2764, 1555), panel_layer(panel, 3015, TOP, 614, 1555, 0, d)]
    spec_write("B03", layers, d, audio="video")


def hit_rings(name, take, f0, duration, w, h):
    """Diagnostic overlay: a thin ring at each logged weapon_hit position for 0.35 s (positions from the take's log,
    in viewport pixels, scaled to the shown frame). It marks where to look; the sparks underneath are the engine's."""
    hits = [(e["pf"], e["view"]) for e in take.find("hit")]
    sx, sy = w / 640, h / 360

    def draw(img, t):
        fr = f0 + int(t * FPS)
        d = ImageDraw.Draw(img)
        live = [(pf, v) for pf, v in hits if 0 <= fr - pf < 11]
        for pf, (vx, vy) in live:
            r = 34 + 3 * (fr - pf)
            cx, cy = vx * sx, vy * sy
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(217, 119, 87, 230), width=5)
        return tuple(live)
    return render_panel(name, w, h, duration, draw)


def b05():
    take = Take("main")
    f0 = 2134
    d = dur("B05")
    vw, vh = 2764, 1555
    panel = state_panel("B05-state", take, [(0, d, f0)], d)
    rings = hit_rings("B05-rings", take, f0, d, vw, vh)
    t_s = at("B05", "A stress test")
    state = json.loads((REPO / "evidence/assignment-6/final-precommit/particles_state.json").read_text())
    res = {r["id"]: r for r in state["results"]}
    lines = [f"{res[k]['status']} {k} {json.dumps(res[k]['observed'])}".strip() for k in
             ("hit-cap-sees-all-events", "hit-cap-limits-instances", "hit-cap-allocation", "lethal-hit-survives-enemy-free")]
    card, _h = card_lines(PAD + 60, 1240, 2640, lines, t_s, size=46, mono=True,
                          title="Recorded: test_particles_state.gd (stress fixture: 40 hits in one volley)")
    layers = frame_chrome("Every hit, its own burst", f"Real engine capture, {TAKE_NOTE['main']} · full frame · source revision {SHA}",
                          "rings: logged hit positions · stress test: evidence/assignment-6")
    layers += [video("main", f0, PAD, TOP, vw, vh), panel_layer(rings, PAD, TOP, vw, vh, 0, d),
               panel_layer(panel, 3015, TOP, 614, 1555, 0, d),
               text("ring = a logged weapon_hit position (diagnostic overlay)", PAD, TOP - 66, 48, SOFT, t_out=t_s)]
    layers += card
    spec_write("B05", layers, d)


def b07():
    d = dur("B07")
    frames = REPO / "captures/defeat_sparks/r1"
    crop = (560, 300, 200, 112)          # courier on the left for scale, the burst on the right (1280 x 720 fixture)
    real = strip_video("B07-real", frames, 0, 47, crop, 12)
    rows = [(9, "0.00 s", "14 × 14 px · compact white cluster"), (11, "0.07 s", "24 × 24 px"),
            (13, "0.13 s", "35 × 34 px · separate sparks"), (15, "0.20 s", "45 × 43 px · yellow-orange"),
            (17, "0.27 s", "54 × 52 px · dim specks"), (19, "0.33 s", "64 × 55 px · widest (limit 68)"),
            (21, "0.40 s", "last pixel · file 22 empty")]
    layers = frame_chrome("Compact, spread, gone", "Real windowed fixture capture · captures/defeat_sparks/r1 · 30 fps · seed 7280",
                          "12× crop, nearest neighbour · measurements: COMPARISON.md")
    layers.append(video_raw(real, 0, PAD, TOP, 2400, 1344, 0, 1.6))
    layers.append(text("real speed (1.6 s)", PAD, TOP + 1370, 48, SOFT, t_in=0.0, t_out=1.6, fade=0.1))
    span = (d - 1.6) / len(rows)
    for k, (fr, ts, label) in enumerate(rows):
        t0 = 1.6 + k * span
        src = crop_png(frames / f"frame{fr:08d}.png", (crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]), 12, f"B07-f{fr}")
        layers.append(image(src, PAD, TOP, 2400, 1344, t0, t0 + span, nearest=True, fade=0.0))
        layers.append(text(f"held frame · file {fr} · {ts}", PAD, TOP + 1370, 48, SOFT, t_in=t0, t_out=t0 + span, fade=0.0))
    x = PAD + 2460
    layers.append(rect(x, TOP, 3629 - x, 1555))
    layers.append(text("r1, measured", x + 44, TOP + 36, 72, INK, "serif"))
    for k, (fr, ts, label) in enumerate(rows):
        t0 = 1.6 + k * span
        y = TOP + 160 + k * 190
        layers.append(text(f"{ts}", x + 44, y, 60, SPARK, "sans-medium", t_in=t0, fade=0.2))
        layers.append(text(label, x + 44, y + 76, 48, INK, w=3629 - x - 88, t_in=t0, fade=0.2))
    spec_write("B07", layers, d)


def video_raw(src, ss, x, y, w, h, t0, t1):
    return {"kind": "video", "src": src, "ss": ss, "x": x, "y": y, "w": w, "h": h, "t": [t0, t1]}


def b09():
    d = dur("B09")
    sheet = f"{REPO_REL}/captures/defeat_sparks/comparison-r0-r1/comparison-contact-sheet.png"
    layers = frame_chrome("Before and after, measured", "Real fixture captures r0 / r1 · captures/defeat_sparks/comparison-r0-r1",
                          "same seed 7280, same frames · Bao's verdict from TUNING.md")
    layers.append(image(sheet, PAD, TOP, 3418, 744))
    rows = [("first visible frame", "≈ 15 × 15 px", "14 × 14 px", "matched", "predicted fifteen"),
            ("lit area to 0.20 s", "≈ 1.5×", "1.4–1.85×", "more than predicted", "chunkier"),
            ("footprint", "+3–4 px", "+1 px", "missed", "one pixel"),
            ("fade, frames 30 / 50", "unchanged, empty", "unchanged, empty", "matched", "Fade timing")]
    y0 = TOP + 770
    layers.append(rect(PAD, y0, 3418, 520))
    for i, h in enumerate(["top: r0 (1.2) · bottom: r1 (1.8)", "Predicted", "Measured", ""]):
        layers.append(text(h, PAD + [60, 1150, 2050, 3000][i], y0 + 30, 48, SOFT, "sans-medium"))
    for k, (name, pred, meas, ok, cue) in enumerate(rows):
        t = at("B09", cue)
        y = y0 + 110 + k * 95
        layers += [text(name, PAD + 60, y, 52, INK, t_in=t), text(pred, PAD + 1150, y, 52, INK, t_in=t),
                   text(meas, PAD + 2050, y, 52, SPARK if ok == "missed" else INK, "sans-medium", t_in=t),
                   text(ok, PAD + 2800, y, 52, {"matched": GOOD, "missed": SPARK}.get(ok, INK), "sans-medium", t_in=t)]
    tv = at("B09", "Bao played it")
    layers.append(rect(PAD, y0 + 550, 3418, 200, t_in=tv))
    layers.append(text("Bao, after playing:", PAD + 60, y0 + 600, 64, SOFT, "serif", t_in=tv))
    layers.append(text("保留 更清晰了", PAD + 760, y0 + 588, 80, INK, "cjk", t_in=tv))
    layers.append(text("(keep it; clearer)", PAD + 1400, y0 + 604, 56, SOFT, t_in=tv))
    spec_write("B09", layers, d)


def b11():
    take = Take("props")
    d = dur("B11")
    ph = {e["name"]: e["pf"] for e in take.find("phase")}
    f_start, f_end = 60, 419
    real = (f_end - f_start) / FPS
    r0, r1 = ph["push_right"] - 8, ph["stand"] - 10
    replay = d - real
    segs = [(0, real, f_start), (real, d, r0)]
    strip = emit_strip("B11-emit", take, f_start, f_end, segs, d, 2764)
    layers = frame_chrome("No movement, no trail", f"Real engine capture, {TAKE_NOTE['props']} · 2× crop · source revision {SHA}",
                          "scripted input through the input map · flag from the take's log")
    layers.append(follow("props", take, f_start, PAD, TOP, 2764, 1555 - 180, 1920, 970, 0, real))
    layers.append(follow("props", take, r0, PAD, TOP, 2764, 1555 - 180, 1920, 970, real, d))
    layers.append(panel_layer(strip, PAD, TOP + 1555 - 150, 2764, 150, 0, d))
    x = PAD + 2804
    layers.append(rect(x, TOP, 3629 - x, 1555))
    layers.append(text("Input held", x + 40, TOP + 36, 64, INK, "serif"))
    steps = [(0.0, "walk to the stall", "→ moves · embers"), ((ph["push_right"] - f_start) / FPS, "hold right into it", "after contact: no displacement · no embers"),
             ((ph["slide_down_right"] - f_start) / FPS, "hold down-right", "slides along · embers"),
             ((ph["stand"] - f_start) / FPS, "release", "standing · no embers"), (real, "replay", "push and slide again")]
    for k, (t, a, b) in enumerate(steps):
        y = TOP + 150 + k * 260
        layers += [text(a, x + 40, y, 52, SPARK if k else INK, "sans-medium", w=3629 - x - 80, t_in=t),
                   text(b, x + 40, y + 70, 48, INK, w=3629 - x - 80, t_in=t)]
    layers.append(text(f"replay of frames {r0}–{r0 + round(replay * FPS)}, real speed", PAD, TOP - 64, 48, SOFT, t_in=real, fade=0.1))
    spec_write("B11", layers, d)


def lamp_centre(png):
    """Centre of the courier's lamp (bright warm pixels) in a 1280 x 720 fixture frame."""
    im = Image.open(png).convert("RGB")
    px = im.load()
    pts = [(x, y) for y in range(0, im.height, 1) for x in range(0, im.width, 1)
           if px[x, y][0] > 220 and px[x, y][1] > 150 and px[x, y][2] < 110]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return sum(xs) // len(xs), sum(ys) // len(ys)


def b13():
    d = dur("B13")
    cmp_dir = REPO / "captures/lantern_trail/comparison-20261029-135607"
    pc = REPO / "captures/play-checks/20261029-142138"
    layers = frame_chrome("A trail you can see", "Real fixture captures · captures/lantern_trail/comparison-20261029-135607",
                          "r0 re-rendered from its preserved resource · 4× crops")
    cw, ch, sc = 200, 110, 4
    for k, fr in enumerate((12, 20, 39)):
        for j, rev in enumerate(("r0", "r1")):
            src = cmp_dir / rev / "strip" / f"frame{fr:08d}.png"
            cx, cy = lamp_centre(src)
            box = (cx - 150, cy - 45, cx + 50, cy + 65)
            img = crop_png(src, box, sc, f"B13-{rev}-{fr}")
            x, y = PAD + j * 860, TOP + 70 + k * 500
            layers.append(image(img, x, y, cw * sc, ch * sc, nearest=True))
            if k == 0:
                layers.append(text(["r0 · alpha 0.55 / 0.30 / 0", "r1 · alpha 0.95 / 0.70 / 0"][j], x, TOP, 52, INK, "sans-medium"))
        layers.append(text(f"frame {fr}", PAD + 1720, TOP + 70 + k * 500 + 190, 48, SOFT))
    x = PAD + 1960
    wr = 3629 - x
    layers += [rect(x, TOP, wr, 390),
               text("Bao's first look:", x + 50, TOP + 40, 60, SOFT, "serif"),
               text("升级火花不明显 移动也不明显", x + 50, TOP + 130, 72, INK, "cjk"),
               text("(the level-up sparks and the movement aren't obvious)", x + 50, TOP + 250, 48, SOFT, w=wr - 100)]
    t1 = at("B13", "Raising only")
    layers += [rect(x, TOP + 430, wr, 330, t_in=t1),
               text("Only line 14 changed: start and middle alpha", x + 50, TOP + 470, 52, INK, "sans-medium", w=wr - 100, t_in=t1),
               text("Brighter at frames 10–39, same footprint, both clear at frames 51 and 60.", x + 50, TOP + 570, 48, SOFT, w=wr - 100, t_in=t1)]
    t2 = at("B13", "Bao played it")
    layers += [text("Bao played it and kept the brighter trail.", x, TOP + 800, 54, GOOD, "sans-medium", w=wr, t_in=t2)]
    t3 = at("B13", "In normal play")
    trail = crop_png(pc / "trail-dark-move45.png", (560, 330, 680, 400), 6, "B13-trail")
    spark = crop_png(pc / "hit-dark-hit+08.png", (690, 320, 810, 390), 6, "B13-spark")
    layers += [image(trail, x, TOP + 920, 720, 420, t3, nearest=True), image(spark, x + 750, TOP + 920, 720, 420, t3, nearest=True),
               text("play check · trail: 2–4 px, dim", x, TOP + 1360, 48, SOFT, w=720, t_in=t3),
               text("play check · hit spark: 6–11 px", x + 750, TOP + 1360, 48, SOFT, w=720, t_in=t3)]
    spec_write("B13", layers, d)


def b15():
    take = Take("main")
    d = dur("B15")
    lv = take.find("levelup", level=2)[0]["pf"]
    pick = take.find("card")[0]["pf"]
    f0 = lv - 45
    real = (pick + 30 - f0) / FPS
    box = (0, 1440, 900, 1995)             # lower-left: the card-screen portrait (4K take pixels), above the driver's label
    holds = [lv + 1, lv + 4, lv + 8, lv + 14, lv + 22, lv + 34]
    layers = frame_chrome("The celebration lands on the portrait", f"Real engine capture, {TAKE_NOTE['main']} · source revision {SHA}",
                          "held frames labelled · Bao's verdict from TUNING.md")
    layers.append(video("main", f0, PAD, TOP, 2040, 1148, 0, real))
    layers.append(video("main", f0, PAD + 2100, TOP, 1318, 813, 0, real, crop=[box[0], box[1], box[2], box[3] - box[1]]))
    layers.append(text("real speed · portrait enlarged", PAD + 2100, TOP + 840, 48, SOFT, t_out=real))
    span = (d - real - 3.0) / len(holds)
    for k, fr in enumerate(holds):
        t0 = real + k * span
        src = take_frame_png("main", fr, box, 2, f"B15-h{k}")
        layers.append(image(src, PAD + 300, TOP, 2800, 1555 - 200, t0, t0 + span, fade=0.0))
        layers.append(text(f"held frame · {(fr - lv) / FPS:.2f} s after the level-up", PAD + 600, TOP + 1370, 48, SOFT, t_in=t0, t_out=t0 + span, fade=0.0))
    tv = d - 3.0
    layers += [video("main", lv + 40, PAD, TOP, 2040, 1148, tv, d),
               rect(PAD + 2100, TOP + 300, 1318, 420, t_in=tv),
               text("Bao, on this placement:", PAD + 2150, TOP + 340, 56, SOFT, "serif", t_in=tv),
               text("可以的", PAD + 2150, TOP + 440, 110, INK, "cjk", t_in=tv),
               text("(that works)", PAD + 2150, TOP + 600, 50, SOFT, t_in=tv)]
    spec_write("B15", layers, d)


def b17():
    take = Take("main")
    d = dur("B17")
    p0 = take.find("action", action="pause")[0]["pf"]
    f0, real = p0 - 40, 6.0
    box = (1760, 1040, 2000, 1175)        # the courier's feet and the frozen embers, 7x
    a = take_frame_png("main", p0 + 1, box, 7, "B17-pa")
    b = take_frame_png("main", p0 + 38, box, 7, "B17-pb")
    same = (Image.open(REEL / a).tobytes() == Image.open(REEL / b).tobytes())
    pc = f"{REPO_REL}/captures/play-checks/20261029-142138"
    layers = frame_chrome("Frozen, then cleared", f"Real engine capture, {TAKE_NOTE['main']} · source revision {SHA}",
                          "play-check shots: captures/play-checks/20261029-142138 (scripted, 1280 × 720)")
    layers.append(video("main", f0, PAD, TOP, 2764, 1555, 0, real))
    t1 = at("B17", "two frames")
    layers += [image(a, PAD, TOP, 1680, 945, t1, nearest=True), image(b, PAD + 1738, TOP, 1680, 945, t1, nearest=True),
               text(f"take frame {p0 + 1} · paused", PAD, TOP + 1000, 48, SOFT, t_in=t1),
               text(f"take frame {p0 + 38} · paused, 1.2 s later", PAD + 1738, TOP + 1000, 48, SOFT, t_in=t1),
               text("0 pixels differ" if same else "frames differ", PAD, TOP + 1090, 72, GOOD if same else SPARK, "sans-medium", t_in=t1)]
    t2 = at("B17", "The scripted play checks")
    layers += [rect(PAD - 20, TOP - 20, 3460, 1600, fill=PAGE, outline=PAGE, radius=0, t_in=t2),
               image(f"{pc}/death-lost+00.png", PAD, TOP, 1680, 945, t2), image(f"{pc}/win-won+00.png", PAD + 1738, TOP, 1680, 945, t2),
               text("lost+00 · first frame in LOST · hit bursts 0, trail stopped", PAD, TOP + 965, 48, SOFT, t_in=t2),
               text("won+00 · first frame in WON · hit bursts 0, trail stopped", PAD + 1738, TOP + 965, 48, SOFT, t_in=t2)]
    t3 = at("B17", "And after a normal run")
    layers += [rect(PAD, TOP + 1080, 3418, 300, t_in=t3),
               text("Bao, after a normal run:", PAD + 60, TOP + 1130, 60, SOFT, "serif", t_in=t3),
               text("没有挡住都正常", PAD + 900, TOP + 1118, 84, INK, "cjk", t_in=t3),
               text("(nothing is hidden; everything is normal)", PAD + 1700, TOP + 1140, 52, SOFT, t_in=t3)]
    spec_write("B17", layers, d)
    if not same:
        print("WARNING B17: paused frames differ")


def b19():
    d = dur("B19")
    ev = REPO / "evidence/assignment-6/final-precommit"
    lines = []
    for n in ["logic", "gameplay", "audio", "defeat_sparks_config", "extra_particles_config", "particles_state", "particles_edges"]:
        j = json.loads((ev / f"{n}.json").read_text())
        lines.append(f"{j['suite']}: {j['checks']} checks, {j['failures']} failures")
    lines.append("total: 292 checks, 0 failures")
    card1, h1 = card_lines(PAD, TOP, 1660, lines, 0.0, size=46, mono=True, title="Recorded: final pre-commit run")
    mut = (REPO / "evidence/assignment-6/mutations/edges-no-displacement-guard.log").read_text().splitlines()
    fails = [l for l in mut if l.startswith("FAIL")] + [l for l in mut if "checks," in l][:1]
    fails = [l.split(" -> ")[0] for l in fails]
    t1 = at("B19", "delete the movement guard")
    card2, h2 = card_lines(PAD + 1720, TOP, 1698, ["removed: distance > 0.01 and <= limit"] + fails,
                           t1, size=44, mono=True, title="Recorded: edge suite, guard removed")
    t2 = at("B19", "an old Godot 3 property name")
    sheet = f"{REPO_REL}/captures/defeat_sparks/mutation-godot3-name/mutation-vs-r1-sheet.png"
    layers = frame_chrome("The tests are real", "Recorded tool output · evidence/assignment-6/final-precommit and mutations",
                          "capture: captures/defeat_sparks/mutation-godot3-name")
    layers += card1 + card2
    layers += [image(sheet, PAD, TOP + 930, 3418, 600, t2),
               text("top: kept r1 · bottom: initial_velocity_min renamed to the Godot 3 name; loads without a warning, spreads 45 × 43 → 40 × 42 px",
                    PAD, TOP + 1550, 48, SOFT, w=3418, t_in=t2)]
    spec_write("B19", layers, d)


def b21():
    d = dur("B21")
    crop = [1080, 780, 1680, 600]
    layers = frame_chrome("What the generated shader draws", f"Real engine fixture capture · capture/study_capture.gd · source revision {SHA}",
                          "seed 7280 · held frames labelled")
    real = 3.0
    for k in range(2):
        layers.append(video("study", 0, PAD, TOP, 3418, 1221, k * real, (k + 1) * real, crop=crop, nearest=True))
    layers.append(text("real speed, played twice", PAD, TOP + 1240, 48, SOFT, t_out=2 * real, fade=0.1))
    holds = [9, 11, 13, 15, 18, 21, 24]
    t_hold_end = d - 2.9          # the study clip is 90 frames (3.00 s): the closing real-speed play must not outrun it
    span = (t_hold_end - 2 * real) / len(holds)
    for k, fr in enumerate(holds):
        t0 = 2 * real + k * span
        src = take_frame_png("study", fr, (crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]), 2, f"B21-h{fr}")
        layers.append(image(src, PAD, TOP, 3418, 1221, t0, t0 + span, nearest=True, fade=0.0))
        layers.append(text(f"held frame {fr} · {(fr - 9) / FPS:.2f} s after the trigger", PAD, TOP + 1240, 48, SOFT, t_in=t0, t_out=t0 + span, fade=0.0))
    layers.append(video("study", 0, PAD, TOP, 3418, 1221, t_hold_end, d, crop=crop, nearest=True))
    layers += [text("CPU · the game's defeat_sparks.tscn", PAD + 300, TOP + 1320, 52, INK, "sans-medium"),
               text("GPU copy · editor-converted ShaderMaterial", PAD + 1900, TOP + 1320, 52, INK, "sans-medium")]
    t1 = at("B21", "the conversion left")
    layers += [rect(PAD + 1700, TOP + 1400, 1718, 140, t_in=t1),
               text("hit_sparks_gpu.tscn: ShaderMaterial has no color_ramp, no scale_curve", PAD + 1740, TOP + 1440, 48, SPARK,
                    "sans-medium", w=1640, t_in=t1)]
    spec_write("B21", layers, d)


def b23():
    d = dur("B23")
    head = json.loads((REPO / "evidence/assignment-6/cost/cost_effects_headless.json").read_text())["conditions"]

    def mean(name, field="frame_ms"):
        tr = head[name]["trials"]
        return sum(t[field]["mean"] for t in tr) / len(tr)
    rows = [("A · 32 live bursts", mean("acap-on", "frame_ms_at_cap") - mean("acap-off"), 1.0, "thirty-two live bursts"),
            ("A · spawn spike (p95)", sum(t["frame_ms"]["p95"] for t in head["acap-on"]["trials"]) / 5 -
             sum(t["frame_ms"]["p95"] for t in head["acap-off"]["trials"]) / 5, 1.0, "spawn spike"),
            ("B · trail, moving", mean("move-on") - mean("move-off"), 0.25, "the trail four"),
            ("Celebration · 4 live", mean("celebration-on") - mean("celebration-off"), 0.4, "all far under")]
    WORK.mkdir(parents=True, exist_ok=True)
    layers = frame_chrome("The price, measured", "Recorded measurements · evidence/assignment-6/cost · Apple M4 · Godot 4.7.2",
                          "CPU headless, 5 × 300 frames · GPU proxy: Mobile + Vulkan")
    layers.append(rect(PAD, TOP, 3418, 980))
    layers.append(text("CPU delta per frame, effects on − off, against its budget", PAD + 60, TOP + 40, 60, INK, "serif"))
    bar_x, bar_w = PAD + 1200, 2100
    for k, (name, delta, budget, cue) in enumerate(rows):
        t = at("B23", cue)
        y = TOP + 170 + k * 200
        frac = max(0.004, delta / budget)
        im = Image.new("RGBA", (bar_w, 70), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        dd.rectangle((0, 0, bar_w - 1, 69), fill="#ECE9E0")
        dd.rectangle((0, 0, int(bar_w * frac), 69), fill=SPARK)
        p = WORK / f"B23-bar{k}.png"
        im.save(p)
        layers += [text(name, PAD + 60, y, 50, INK, "sans-medium", t_in=t),
                   image(str(p.relative_to(REEL)), bar_x, y, bar_w, 70, t),
                   text(f"+{delta:.3f} ms of {budget:g} ms budget ({100 * delta / budget:.1f}%)", bar_x, y + 84, 48, SOFT, t_in=t)]
    t2 = at("B23", "The GPU number")
    layers += [rect(PAD, TOP + 1020, 1680, 520, t_in=t2),
               text("GPU · GL Compatibility (the game's renderer)", PAD + 50, TOP + 1060, 52, INK, "sans-medium", w=1580, t_in=t2),
               text("0.000 ms", PAD + 50, TOP + 1160, 140, SPARK, "serif-medium", t_in=t2),
               text("on every frame of every condition: not measurable here", PAD + 50, TOP + 1360, 48, SOFT, w=1580, t_in=t2)]
    t3 = at("B23", "A Vulkan proxy")
    layers += [rect(PAD + 1738, TOP + 1020, 1680, 520, t_in=t3),
               text("GPU · Mobile + Vulkan proxy (median deltas)", PAD + 1788, TOP + 1060, 52, INK, "sans-medium", w=1580, t_in=t3),
               text("A +0.01 · B −0.05 · celebration +0.09 ms", PAD + 1788, TOP + 1170, 62, INK, "serif-medium", w=1580, t_in=t3),
               text("all inside a ±0.1 ms run-to-run noise band; a proxy, not the shipped renderer", PAD + 1788, TOP + 1330, 48, SOFT, w=1580, t_in=t3)]
    spec_write("B23", layers, d)


BUILDERS = {"B03": b03, "B05": b05, "B07": b07, "B09": b09, "B11": b11, "B13": b13, "B15": b15, "B17": b17,
            "B19": b19, "B21": b21, "B23": b23}

if __name__ == "__main__":
    want = sys.argv[1:] or list(BUILDERS)
    for bid in want:
        BUILDERS[bid]()
