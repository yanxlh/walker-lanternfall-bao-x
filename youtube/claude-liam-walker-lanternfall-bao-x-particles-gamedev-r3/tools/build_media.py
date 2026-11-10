#!/usr/bin/env python3
"""Build media/<BID>.mp4 for every evidence and game-sound beat of the revised particle film (4K, 30 fps).

Everything shown is real: the 4K Movie Maker takes in capture/ (isolated copy of the film's source snapshot), the
committed fixture strips, editor Visual Profiler screenshots, play-check shots and recorded tool output in the
snapshot, this film's own cost runs in tests/, and the takes' own per-frame logs. Held frames and replays are labelled.
Layout follows the first particle film's evidence beats (same chrome, same compose.py).

    python3 tools/build_media.py [B05 B07 ...]
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
SRC = Path((REEL / "FILM-SOURCE-PATH.txt").read_text().strip())   # the film's source snapshot (repository files)
COURSE = Path("/Users/yxlh/Documents/ChatGPT/csye 7280/course-repo-assignment2/fall-2026/xinghe-b/assignment-2/"
              "walker-lanternfall-bao-x/captures/defeat_sparks")   # full local r0/r1 sequences (strips match the repo)
TOOLS = REEL / "tools"
WORK = REEL / "media" / "_work"
sys.path.insert(0, str(TOOLS))
from compose import FONT_FILES  # noqa: E402

W, H, FPS = 3840, 2160, 30
PAD, TITLE_Y, TOP, BOT = 211, 97, 346, 1901
INK, SOFT, GHOST, SPARK, PAGE, CARD, BORDER = "#3D3929", "#73705F", "#A9A491", "#D97757", "#FAF9F5", "#FFFFFF", "#E5E2D9"
GOOD, DARK = "#4F7A4A", "#202531"
REV = "source tree " + (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()[:7]
SHEET = json.loads((REEL / "beat_sheet.json").read_text())
BEATS = {b["beat_id"]: b for b in SHEET["beats"]}
def _take(stem):
    """A take with stale frames is used through its clean copy (capture/clean/, frame n = game frame n), indexed by
    the headless dry run, whose log matches the take event for event without the stale offsets."""
    if (REEL / f"capture/clean/{stem}.mov").exists():
        return (f"capture/clean/{stem}.mov", f"capture/{stem}-dryrun.jsonl")
    return (f"capture/{stem}.avi", f"capture/{stem}-log.jsonl")


TAKES = {"main": _take("take-main-seed11"), "props": _take("take-props-seed11"),
         "study": ("capture/study-cpu-vs-gpu.avi", None)}
TAKE_NOTE = {"main": "main take · seed 11", "props": "props take · seed 11", "study": "study fixture · seed 7280"}
STATE = ["menu", "playing", "level-up cards", "paused", "won", "lost"]
CUR = SRC / "evidence/assignment-6/current-r2-validation"


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
    L = {"kind": "image", "src": str(src), "x": x, "y": y, "w": w, "h": h}
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


def video_raw(src, ss, x, y, w, h, t0, t1):
    return {"kind": "video", "src": src, "ss": ss, "x": x, "y": y, "w": w, "h": h, "t": [t0, t1]}


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
    f_t, f_s, f_l = font("serif", 72), font("sans", 36), font("sans", 40)
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


def crop_fit(src, box, w, h, name):
    """Crop a screenshot and scale it (smooth) to w x h; for editor screenshots, which are not pixel art."""
    WORK.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB").crop(box).resize((w, h), Image.LANCZOS)
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


def quote(x, y, w, who, words, t_in, size=72, h=300):
    return [rect(x, y, w, h, t_in=t_in),
            text(who, x + 50, y + 40, 52, SOFT, "serif", w=w - 100, t_in=t_in),
            text(f"“{words}”", x + 50, y + 125, size, INK, "serif-medium", w=w - 100, t_in=t_in)]


# ---------------------------------------------------------------- beats

def b03():
    take = Take("main")
    lv = take.find("levelup", level=5)[0]["pf"]
    f0, f1 = lv - 100, lv - 100 + 390
    d = (f1 - f0) / FPS
    panel = state_panel("B03-state", take, [(0, d, f0)], d)
    layers = frame_chrome("All three, with the game's sound", f"Real engine capture, {TAKE_NOTE['main']} · {REV}",
                          "readout from the take's per-frame log")
    layers += [video("main", f0, PAD, TOP, 2764, 1555), panel_layer(panel, 3015, TOP, 614, 1555, 0, d)]
    spec_write("B03", layers, d, audio="video")


def b05():
    """Three parts on the current r2 fixture strip (same layout as the first film's strip beat)."""
    d = dur("B05")
    frames = SRC / "captures/defeat_sparks/r2"
    crop = (560, 300, 200, 112)          # courier on the left for scale, the burst on the right (1280 x 720 fixture)
    real = strip_video("B05-real", frames, 0, 47, crop, 12)
    rows = [(9, "0.00 s", "EMISSION + DRAW", "14 × 14 px · sixteen at once, added to white"),
            (11, "0.07 s", "PROCESS", "24 × 24 px · spreading out"),
            (13, "0.13 s", "PROCESS", "35 × 34 px · slowing (damping)"),
            (15, "0.20 s", "PROCESS", "45 × 43 px · pale yellow (colour ramp)"),
            (17, "0.27 s", "PROCESS", "54 × 52 px · still bright"),
            (19, "0.33 s", "PROCESS", "64 × 55 px · shrinking orange (scale curve)"),
            (21, "0.40 s", "EMISSION", "last pixel · lifetime 0.45 s ends it")]
    layers = frame_chrome("What each part decides", "Real windowed fixture capture · captures/defeat_sparks/r2 · 30 fps · seed 7280",
                          "12× crop, nearest neighbour · measurements: comparison-r1-r2/COMPARISON.md")
    layers.append(video_raw(real, 0, PAD, TOP, 2400, 1344, 0, 1.6))
    layers.append(text("real speed (1.6 s)", PAD, TOP + 1370, 48, SOFT, t_in=0.0, t_out=1.6, fade=0.1))
    span = (d - 1.6) / len(rows)
    for k, (fr, ts, part, label) in enumerate(rows):
        t0 = 1.6 + k * span
        src = crop_png(frames / f"frame{fr:08d}.png", (crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]), 12, f"B05-f{fr}")
        layers.append(image(src, PAD, TOP, 2400, 1344, t0, t0 + span, nearest=True, fade=0.0))
        layers.append(text(f"held frame · file {fr} · {ts}", PAD, TOP + 1370, 48, SOFT, t_in=t0, t_out=t0 + span, fade=0.0))
    x = PAD + 2460
    layers.append(rect(x, TOP, 3629 - x, 1555))
    layers.append(text("r2, measured", x + 44, TOP + 36, 72, INK, "serif"))
    for k, (fr, ts, part, label) in enumerate(rows):
        t0 = 1.6 + k * span
        y = TOP + 160 + k * 190
        layers.append(text(f"{ts} · {part}", x + 44, y, 52, SPARK, "sans-medium", w=3629 - x - 88, t_in=t0, fade=0.2))
        layers.append(text(label, x + 44, y + 72, 46, INK, w=3629 - x - 88, t_in=t0, fade=0.2))
    spec_write("B05", layers, d)


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


def b07():
    take = Take("main")
    f0 = 2134
    d = dur("B07")
    vw, vh = 2764, 1555
    panel = state_panel("B07-state", take, [(0, d, f0)], d)
    rings = hit_rings("B07-rings", take, f0, d, vw, vh)
    t_s = at("B07", "A stress test")
    state = json.loads((CUR / "particles_state.json").read_text())
    res = {r["id"]: r for r in state["results"]}
    lines = [f"{res[k]['status']} {k} {json.dumps(res[k]['observed'])}".strip() for k in
             ("hit-cap-sees-all-events", "hit-cap-limits-instances", "hit-cap-allocation", "lethal-hit-survives-enemy-free")]
    card, _h = card_lines(PAD + 60, 1240, 2640, lines, t_s, size=46, mono=True,
                          title="Recorded: test_particles_state.gd (stress fixture: 40 hits in one volley)")
    layers = frame_chrome("Every hit, its own burst", f"Real engine capture, {TAKE_NOTE['main']} · full frame · {REV}",
                          "rings: logged hit positions · stress test: current-r2-validation")
    layers += [video("main", f0, PAD, TOP, vw, vh), panel_layer(rings, PAD, TOP, vw, vh, 0, d),
               panel_layer(panel, 3015, TOP, 614, 1555, 0, d),
               text("ring = a logged weapon_hit position (diagnostic overlay)", PAD, TOP - 66, 48, SOFT, t_out=t_s)]
    layers += card
    spec_write("B07", layers, d)


def b08():
    d = dur("B08")
    layers = frame_chrome("The intent, and the first strip", "CHANGE-BRIEF.md · Effect A visual intent (original record, 29 October)",
                          "first fixture strip: captures/defeat_sparks/r0 · 4× crops, nearest neighbour")
    x0, wl = PAD, 1640
    lines = ["First 0.07 s: a compact, bright cluster establishes the event position.",
             "0.07–0.20 s: sparks spread outward and slow down.",
             "0.20–0.45 s: sparks shrink and fade completely.",
             "About one character height initially; no more than two at the widest."]
    layers.append(rect(x0, TOP, wl, 1555))
    layers.append(text("Visual intent (brief)", x0 + 50, TOP + 40, 72, INK, "serif"))
    for k, ln in enumerate(lines):
        layers.append(text(ln, x0 + 50, TOP + 180 + k * 300, 58, INK, w=wl - 100))
    t1 = at("B08", "The first strip")
    crop = (560, 300, 200, 112)
    xs = PAD + 1700
    for k, (fr, ts) in enumerate([(9, "0.00 s · 11 × 12 px"), (11, "0.07 s · 23 × 22 px"), (15, "0.20 s · 45 × 43 px"), (21, "0.40 s · last pixel")]):
        src = crop_png(COURSE / "r0" / f"frame{fr:08d}.png", (crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]), 4, f"B08-r0-{fr}")
        x, y = xs + (k % 2) * 870, TOP + (k // 2) * 660
        layers += [image(src, x, y, 800, 448, t1, nearest=True), text(f"r0 · file {fr} · {ts}", x, y + 470, 46, SOFT, w=800, t_in=t1)]
    t2 = at("B08", "a third of a character")
    layers += [rect(xs, TOP + 1350, 1718, 200, t_in=t2),
               text("first frame: 11 × 12 px against a 34 px courier = 0.35 of a character height", xs + 40, TOP + 1385, 50, SPARK,
                    "sans-medium", w=1640, t_in=t2)]
    spec_write("B08", layers, d)


def b10():
    d = dur("B10")
    sheet = SRC / "captures/defeat_sparks/comparison-r0-r1/comparison-contact-sheet.png"
    layers = frame_chrome("r one: before and after", "Real fixture captures r0 / r1 · captures/defeat_sparks/comparison-r0-r1",
                          "same seed 7280, same frames · Bao's verdict from TUNING.md")
    layers.append(image(sheet, PAD, TOP, 3418, 744))
    rows = [("first visible frame", "≈ 15 × 15 px", "14 × 14 px", "matched", "predicted fifteen"),
            ("lit area to 0.20 s", "≈ 1.5×", "1.4–1.85×", "more than predicted", "chunkier"),
            ("footprint", "+3–4 px", "+1 px", "missed", "one pixel")]
    y0 = TOP + 770
    layers.append(rect(PAD, y0, 3418, 430))
    for i, h in enumerate(["top: r0 (1.2) · bottom: r1 (1.8)", "Predicted", "Measured", ""]):
        layers.append(text(h, PAD + [60, 1150, 2050, 3000][i], y0 + 30, 48, SOFT, "sans-medium"))
    for k, (name, pred, meas, ok, cue) in enumerate(rows):
        t = at("B10", cue)
        y = y0 + 110 + k * 95
        layers += [text(name, PAD + 60, y, 52, INK, t_in=t), text(pred, PAD + 1150, y, 52, INK, t_in=t),
                   text(meas, PAD + 2050, y, 52, SPARK if ok == "missed" else INK, "sans-medium", t_in=t),
                   text(ok, PAD + 2800, y, 52, {"matched": GOOD, "missed": SPARK}.get(ok, INK), "sans-medium", t_in=t)]
    tv = at("B10", "Bao played it")
    layers += quote(PAD, y0 + 470, 3418, "Bao, after playing:", "Keep it; it is clearer", tv, size=80, h=290)
    spec_write("B10", layers, d)


def b12():
    d = dur("B12")
    sheet = SRC / "captures/defeat_sparks/comparison-r1-r2/comparison-contact-sheet.png"
    layers = frame_chrome("r two: the observed change", "Real fixture captures r1 / r2 · captures/defeat_sparks/comparison-r1-r2",
                          "same seed 7280, same frames · Bao's verdict from TUNING.md")
    layers.append(image(sheet, PAD, TOP, 3418, 1201))
    layers.append(text("top: r1 · bottom: r2 · files 9, 12, 15, 17, 18, 20 (0.00–0.37 s)", PAD, TOP + 1215, 46, SOFT))
    rows = [("0.20 s · file 15", "luma 151 → 236", "bright px 21 → 189 of 189", "one hundred eighty-nine"),
            ("0.27 s · file 17", "luma 104 → 224", "bright px 2 → 83 of 83", "still bright"),
            ("extent, last frame", "identical in every file", "last trace file 21 in both", "The footprint"),
            ("colour (the miss)", "predicted yellow-orange", "measured pale yellow (255, 238, 163)", "The miss")]
    y0 = TOP + 1290
    for k, (name, a, b, cue) in enumerate(rows):
        t = at("B12", cue)
        x = PAD + (k % 2) * 1720
        y = y0 + (k // 2) * 150
        colour = SPARK if "miss" in name else INK
        layers += [text(name, x, y, 46, SOFT, "sans-medium", w=1680, t_in=t),
                   text(f"{a} · {b}", x, y + 58, 48, colour, "sans-medium", w=1680, t_in=t)]
    tv = at("B12", "Bao played it")
    layers += [rect(PAD - 20, TOP - 20, 3460, 1600, fill=PAGE, outline=PAGE, radius=0, t_in=tv),
               image(sheet, PAD, TOP, 3418, 1201, tv),
               rect(PAD, TOP + 1250, 3418, 300, t_in=tv),
               text("Bao, after playing r2 in the game:", PAD + 60, TOP + 1290, 52, SOFT, "serif", t_in=tv),
               text("“Yes”  ·  “They don't get mixed up”  ·  kept", PAD + 60, TOP + 1380, 80, INK, "serif-medium", w=3300, t_in=tv)]
    spec_write("B12", layers, d)


def b14():
    take = Take("props")
    d = dur("B14")
    ph = {e["name"]: e["pf"] for e in take.find("phase")}
    f_start, f_end = 60, 419
    real = (f_end - f_start) / FPS
    r0 = ph["push_right"] - 8
    replay = d - real
    segs = [(0, real, f_start), (real, d, r0)]
    strip = emit_strip("B14-emit", take, f_start, f_end, segs, d, 2764)
    layers = frame_chrome("No movement, no trail", f"Real engine capture, {TAKE_NOTE['props']} · 2× crop · {REV}",
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
    if replay > 0.1:
        layers.append(text(f"replay of frames {r0}–{r0 + round(replay * FPS)}, real speed", PAD, TOP - 64, 48, SOFT, t_in=real, fade=0.1))
    spec_write("B14", layers, d)


def lamp_centre(png):
    """Centre of the courier's lamp (bright warm pixels) in a 1280 x 720 fixture frame."""
    im = Image.open(png).convert("RGB")
    px = im.load()
    pts = [(x, y) for y in range(0, im.height, 1) for x in range(0, im.width, 1)
           if px[x, y][0] > 220 and px[x, y][1] > 150 and px[x, y][2] < 110]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return sum(xs) // len(xs), sum(ys) // len(ys)


def b16():
    d = dur("B16")
    cmp_dir = SRC / "captures/lantern_trail/comparison-20261029-135607"
    pc = SRC / "captures/play-checks/20261029-142138"
    layers = frame_chrome("A trail you can see", "Real fixture captures · captures/lantern_trail/comparison-20261029-135607",
                          "r0 re-rendered from its preserved resource · 4× crops")
    cw, ch, sc = 200, 110, 4
    for k, fr in enumerate((12, 20, 39)):
        for j, rev in enumerate(("r0", "r1")):
            src = cmp_dir / rev / "strip" / f"frame{fr:08d}.png"
            cx, cy = lamp_centre(src)
            box = (cx - 150, cy - 45, cx + 50, cy + 65)
            img = crop_png(src, box, sc, f"B16-{rev}-{fr}")
            x, y = PAD + j * 860, TOP + 70 + k * 500
            layers.append(image(img, x, y, cw * sc, ch * sc, nearest=True))
            if k == 0:
                layers.append(text(["r0 · alpha 0.55 / 0.30 / 0", "r1 · alpha 0.95 / 0.70 / 0"][j], x, TOP, 52, INK, "sans-medium"))
        layers.append(text(f"frame {fr}", PAD + 1720, TOP + 70 + k * 500 + 190, 48, SOFT))
    x = PAD + 1960
    wr = 3629 - x
    layers += [rect(x, TOP, wr, 390),
               text("Bao's first look:", x + 50, TOP + 40, 60, SOFT, "serif"),
               text("“The level-up sparks and movement trail are not obvious”", x + 50, TOP + 130, 60, INK, "serif-medium", w=wr - 100)]
    t1 = at("B16", "Raising only")
    layers += [rect(x, TOP + 430, wr, 330, t_in=t1),
               text("Only line 14 changed: start and middle alpha", x + 50, TOP + 470, 52, INK, "sans-medium", w=wr - 100, t_in=t1),
               text("Brighter at frames 10–39, same footprint, both clear at frames 51 and 60.", x + 50, TOP + 570, 48, SOFT, w=wr - 100, t_in=t1)]
    t2 = at("B16", "Bao played it")
    layers += [text("Bao played it and kept the brighter trail.", x, TOP + 800, 54, GOOD, "sans-medium", w=wr, t_in=t2)]
    t3 = at("B16", "In normal play")
    trail = crop_png(pc / "trail-dark-move45.png", (560, 330, 680, 400), 6, "B16-trail")
    spark = crop_png(pc / "hit-dark-hit+08.png", (690, 320, 810, 390), 6, "B16-spark")
    layers += [image(trail, x, TOP + 920, 720, 420, t3, nearest=True), image(spark, x + 750, TOP + 920, 720, 420, t3, nearest=True),
               text("play check · trail: 2–4 px, dim", x, TOP + 1360, 48, SOFT, w=720, t_in=t3),
               text("play check (r1 sparks) · hit spark: 6–11 px", x + 750, TOP + 1360, 48, SOFT, w=720, t_in=t3)]
    spec_write("B16", layers, d)


def b18():
    take = Take("main")
    d = dur("B18")
    lv = take.find("levelup", level=2)[0]["pf"]
    pick = take.find("card")[0]["pf"]
    f0 = lv - 45
    real = (pick + 30 - f0) / FPS
    box = (0, 1440, 900, 1995)             # lower-left: the card-screen portrait (4K take pixels), above the driver's label
    holds = [lv + 1, lv + 4, lv + 8, lv + 14, lv + 22, lv + 34]
    layers = frame_chrome("The celebration lands on the portrait", f"Real engine capture, {TAKE_NOTE['main']} · {REV}",
                          "held frames labelled · Bao's verdict from TUNING.md")
    layers.append(video("main", f0, PAD, TOP, 2040, 1148, 0, real))
    layers.append(video("main", f0, PAD + 2100, TOP, 1318, 813, 0, real, crop=[box[0], box[1], box[2], box[3] - box[1]]))
    layers.append(text("real speed · portrait enlarged", PAD + 2100, TOP + 840, 48, SOFT, t_out=real))
    span = (d - real - 3.0) / len(holds)
    for k, fr in enumerate(holds):
        t0 = real + k * span
        src = take_frame_png("main", fr, box, 2, f"B18-h{k}")
        layers.append(image(src, PAD + 300, TOP, 2800, 1555 - 200, t0, t0 + span, fade=0.0))
        layers.append(text(f"held frame · {(fr - lv) / FPS:.2f} s after the level-up", PAD + 600, TOP + 1370, 48, SOFT, t_in=t0, t_out=t0 + span, fade=0.0))
    tv = d - 3.0
    layers += [video("main", lv + 40, PAD, TOP, 2040, 1148, tv, d)]
    layers += quote(PAD + 2100, TOP + 300, 1318, "Bao, on this placement:", "That works", tv, size=110, h=420)
    spec_write("B18", layers, d)


def b20():
    take = Take("main")
    d = dur("B20")
    p0 = take.find("action", action="pause")[0]["pf"]
    f0, real = p0 - 40, 6.0
    box = (1760, 1040, 2000, 1175)        # the courier's feet and the frozen embers, 7x
    a = take_frame_png("main", p0 + 1, box, 7, "B20-pa")
    b = take_frame_png("main", p0 + 38, box, 7, "B20-pb")
    same = (Image.open(REEL / a).tobytes() == Image.open(REEL / b).tobytes())
    pc = SRC / "captures/play-checks/20261029-142138"
    layers = frame_chrome("Frozen, then cleared", f"Real engine capture, {TAKE_NOTE['main']} · {REV}",
                          "play-check shots: captures/play-checks/20261029-142138 (scripted, 1280 × 720)")
    layers.append(video("main", f0, PAD, TOP, 2764, 1555, 0, real))
    t1 = at("B20", "two frames")
    layers += [image(a, PAD, TOP, 1680, 945, t1, nearest=True), image(b, PAD + 1738, TOP, 1680, 945, t1, nearest=True),
               text(f"take frame {p0 + 1} · paused", PAD, TOP + 1000, 48, SOFT, t_in=t1),
               text(f"take frame {p0 + 38} · paused, 1.2 s later", PAD + 1738, TOP + 1000, 48, SOFT, t_in=t1),
               text("0 pixels differ" if same else "frames differ", PAD, TOP + 1090, 72, GOOD if same else SPARK, "sans-medium", t_in=t1)]
    t2 = at("B20", "The scripted play checks")
    layers += [rect(PAD - 20, TOP - 20, 3460, 1600, fill=PAGE, outline=PAGE, radius=0, t_in=t2),
               image(pc / "death-lost+00.png", PAD, TOP, 1680, 945, t2), image(pc / "win-won+00.png", PAD + 1738, TOP, 1680, 945, t2),
               text("lost+00 · first frame in LOST · hit bursts 0, trail stopped", PAD, TOP + 965, 48, SOFT, t_in=t2),
               text("won+00 · first frame in WON · hit bursts 0, trail stopped", PAD + 1738, TOP + 965, 48, SOFT, t_in=t2)]
    t3 = at("B20", "Bao's own check")
    layers += [rect(PAD, TOP + 1060, 3418, 480, t_in=t3),
               text("Bao's recorded check in the running game (TUNING.md):", PAD + 60, TOP + 1100, 52, SOFT, "serif", w=3300, t_in=t3),
               text("“When I stop moving, B stops producing new embers.”", PAD + 60, TOP + 1200, 62, INK, "serif-medium", w=3300, t_in=t3),
               text("“When I pause, the remaining sparks and trail stay frozen instead of continuing to move or fade.”",
                    PAD + 60, TOP + 1300, 62, INK, "serif-medium", w=3300, t_in=t3)]
    spec_write("B20", layers, d)
    if not same:
        print("WARNING B20: paused frames differ")


def b22():
    d = dur("B22")
    lines, total = [], 0
    for n in ["logic", "gameplay", "audio", "defeat_sparks_config", "extra_particles_config", "particles_state",
              "particles_edges", "shader_study_config", "particles_tree_pause"]:
        j = json.loads((CUR / f"{n}.json").read_text())
        lines.append(f"{j['suite']}: {j['checks']} checks, {j['failures']} failures")
        total += j["checks"]
    lines.append(f"total: {total} checks, 0 failures")
    card1, h1 = card_lines(PAD, TOP, 1660, lines, 0.0, size=40, mono=True, line_h=60, title="Recorded: nine suites, this source")
    t1 = at("B22", "Godot three name")
    g3 = [l.split(" -> ")[0] for l in (CUR / "godot3-name.log").read_text().splitlines() if l.startswith("FAIL") or "checks," in l]
    t2 = at("B22", "Change the spread")
    ws = [l.split(" -> ")[0] for l in (CUR / "wrong-spread.log").read_text().splitlines() if l.startswith("FAIL") or "checks," in l]
    t3 = at("B22", "Delete the movement guard")
    mut = (SRC / "evidence/assignment-6/mutations/edges-no-displacement-guard.log").read_text().splitlines()
    gd = [l.split(" -> ")[0] for l in mut if l.startswith("FAIL")] + [l.split(" -> ")[0] for l in mut if "checks," in l][:1]
    card2, h2 = card_lines(PAD + 1720, TOP, 1698, ["initial_velocity_min → initial_velocity · exit 1"] + g3, t1, size=40, mono=True,
                           title="Godot 3 name")
    card3, h3 = card_lines(PAD + 1720, TOP + h2 + 30, 1698, ["spread 180 → 90, brief unchanged · exit 1"] + ws, t2, size=40, mono=True,
                           title="Value drift")
    card4, h4 = card_lines(PAD + 1720, TOP + h2 + h3 + 60, 1698, ["guard removed (recorded 29 October)"] + gd, t3, size=38, mono=True,
                           title="Movement guard removed")
    sheet = SRC / "captures/defeat_sparks/mutation-godot3-name/mutation-vs-r1-sheet.png"
    layers = frame_chrome("The tests are real", "Recorded tool output · evidence/assignment-6/current-r2-validation and mutations",
                          "capture: captures/defeat_sparks/mutation-godot3-name")
    layers += card1 + card2 + card3 + card4
    y_img = TOP + h1 + 40
    layers += [image(sheet, PAD, y_img, 1660, int(1660 * 600 / 3418), t1),
               text("windowed: r1 (top) vs the Godot 3 name (bottom): loads silently, 45 × 43 → 40 × 42 px", PAD, y_img + int(1660 * 600 / 3418) + 16,
                    40, SOFT, w=1660, t_in=t1)]
    t4 = at("B22", "None of this")
    layers += [rect(PAD - 20, TOP - 20, 3460, 1600, fill=PAGE, outline=PAGE, radius=0, t_in=t4)]
    lim = ["Headless tests prove: settings read back from the loaded scenes; events fire, stop, freeze and clear on the right states; "
           "two hits in one lifetime make two bursts; the cap holds.",
           "They cannot prove: that anything is visible, readable, the right size, or the right colour. A dummy renderer draws nothing."]
    layers += [rect(PAD, TOP + 200, 3418, 900, t_in=t4),
               text("What no headless run can show", PAD + 60, TOP + 250, 80, INK, "serif", t_in=t4),
               text(lim[0], PAD + 60, TOP + 420, 58, INK, w=3300, t_in=t4),
               text(lim[1], PAD + 60, TOP + 720, 58, SPARK, "sans-medium", w=3300, t_in=t4)]
    spec_write("B22", layers, d)


def b24():
    d = dur("B24")
    crop = [1080, 780, 1680, 600]
    layers = frame_chrome("What the generated shader draws now", f"Real engine fixture capture · capture/study_capture.gd · {REV}",
                          "seed 7280 · held frames labelled")
    real = 3.0
    for k in range(2):
        layers.append(video("study", 0, PAD, TOP, 3418, 1221, k * real, (k + 1) * real, crop=crop, nearest=True))
    layers.append(text("real speed, played twice", PAD, TOP + 1240, 48, SOFT, t_out=2 * real, fade=0.1))
    holds = [9, 11, 13, 15, 18, 21, 24]
    t_hold_end = d - 2.9
    span = (t_hold_end - 2 * real) / len(holds)
    for k, fr in enumerate(holds):
        t0 = 2 * real + k * span
        src = take_frame_png("study", fr, (crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]), 2, f"B24-h{fr}")
        layers.append(image(src, PAD, TOP, 3418, 1221, t0, t0 + span, nearest=True, fade=0.0))
        layers.append(text(f"held frame {fr} · {(fr - 9) / FPS:.2f} s after the trigger", PAD, TOP + 1240, 48, SOFT, t_in=t0, t_out=t0 + span, fade=0.0))
    layers.append(video("study", 0, PAD, TOP, 3418, 1221, t_hold_end, d, crop=crop, nearest=True))
    layers += [text("CPU · the game's defeat_sparks.tscn (r2)", PAD + 200, TOP + 1320, 52, INK, "sans-medium"),
               text("GPU copy · the editor-generated process shader", PAD + 1800, TOP + 1320, 52, INK, "sans-medium")]
    layers += [rect(PAD + 1700, TOP + 1400, 1718, 140),
               text("GPU copy: color_ramp + scale_curve bound (a6-r2), ramp = r2", PAD + 1740, TOP + 1440, 46, GOOD,
                    "sans-medium", w=1640)]
    spec_write("B24", layers, d)


def runs_cpu(path):
    c = json.loads(Path(path).read_text())["conditions"]

    def m(k):
        tr = c[k]["trials"]
        return sum(t["frame_ms"]["mean"] for t in tr) / len(tr)
    return {e: m(f"{e}-on") - m(f"{e}-off") for e in ("acap", "move", "celebration")}


def bar_png(name, frac, w=1500):
    im = Image.new("RGBA", (w, 60), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.rectangle((0, 0, w - 1, 59), fill="#ECE9E0")
    if frac > 0:
        dd.rectangle((0, 0, max(4, int(w * min(frac, 1.0))), 59), fill=SPARK)
    p = WORK / f"{name}.png"
    WORK.mkdir(parents=True, exist_ok=True)
    im.save(p)
    return str(p.relative_to(REEL))


def b26():
    d = dur("B26")
    run1 = runs_cpu(CUR / "cpu-r2.json")
    run2 = runs_cpu(REEL / "tests/cpu-r2-headless-20261109.json")
    layers = frame_chrome("The CPU price, measured twice", "Recorded measurements · current-r2-validation/cpu-r2.json · this film's tests/cpu-r2-headless-20261109.json",
                          "headless, 5 × 300 frames · Apple M4 · Godot 4.7.2")
    layers.append(rect(PAD, TOP, 3418, 1050))
    layers.append(text("CPU delta per frame, effects on − off, against its budget", PAD + 60, TOP + 40, 60, INK, "serif"))
    rows = [("A · 32 live bursts", "acap", 1.0, "thirty-two live bursts"),
            ("B · trail, moving", "move", 0.25, "The trail's difference"),
            ("Celebration · 4 live", "celebration", 0.4, "The trail's difference")]
    for k, (name, key, budget, cue) in enumerate(rows):
        t = at("B26", cue)
        y = TOP + 170 + k * 290
        layers.append(text(name, PAD + 60, y, 52, INK, "sans-medium", t_in=t))
        for j, (run, label) in enumerate([(run1, "run 1"), (run2, "run 2")]):
            v = run[key]
            yy = y + 80 + j * 90
            layers += [image(bar_png(f"B26-{key}-{j}", v / budget), PAD + 600, yy, 1500, 60, t),
                       text(f"{label}: {v:+.3f} ms of {budget:g} ms", PAD + 2160, yy + 4, 46, SOFT if v >= 0 else SPARK, t_in=t)]
    t2 = at("B26", "Why trust a headless number")
    layers += [rect(PAD, TOP + 1090, 3418, 450, t_in=t2),
               text("Headless = a dummy renderer: nothing is drawn, no GPU work runs.", PAD + 60, TOP + 1130, 56, INK, "sans-medium", w=3300, t_in=t2),
               text("CPUParticles2D (A and B): the simulation runs on the processor, so the headless price is real CPU work.",
                    PAD + 60, TOP + 1240, 50, INK, w=3300, t_in=t2),
               text("GPUParticles2D: its process step is a shader on the graphics card, which headless never runs, so its headless price is near zero by construction.",
                    PAD + 60, TOP + 1350, 50, SPARK, w=3300, t_in=at("B26", "A GPU particle node"))]
    spec_write("B26", layers, d)


def b27():
    d = dur("B27")
    vp = SRC / "evidence/assignment-6/cost/visual-profiler-a-r2-current"
    box = (355, 1440, 1680, 1640)          # profiler rows and graph only: no editor chrome, so no UI-language text
    vh = round(1680 * (box[3] - box[1]) / (box[2] - box[0]))
    off = crop_fit(vp / "a-off-visible.png", box, 1680, vh, "B27-a-off")
    on = crop_fit(vp / "a-on-visible.png", box, 1680, vh, "B27-a-on")
    layers = frame_chrome("The GPU price, honestly", "Editor Visual Profiler screenshots · evidence/assignment-6/cost/visual-profiler-a-r2-current",
                          "Mobile + Vulkan proxy, not the shipped renderer · timer runs: current-r2-validation/gpu-r2.json, tests/gpu-*.json")
    layers += [rect(PAD, TOP, 3418, 300),
               text("GL Compatibility, the game's renderer: GPU 0.000 ms on every frame", PAD + 60, TOP + 50, 64, INK, "sans-medium", w=3300),
               text("= no timing available on this Mac, not zero cost", PAD + 60, TOP + 170, 52, SOFT, w=3300)]
    t1 = at("B27", "Visual Profiler")
    yi = TOP + 420
    for k, (img, cap) in enumerate([(off, "A off · profiler frame 715 · Render Viewports: CPU 0.30 ms, GPU 0.62 ms"),
                                    (on, "A on (r2) · profiler frame 782 · Render Viewports: CPU 0.61 ms, GPU 5.21 ms")]):
        x = PAD + k * 1738
        layers += [text("row", x + 20, yi - 60, 40, SOFT, "sans-medium", t_in=t1),
                   text("CPU", x + 380, yi - 60, 40, SOFT, "sans-medium", t_in=t1),
                   text("GPU", x + 560, yi - 60, 40, SOFT, "sans-medium", t_in=t1),
                   text("frame-time graph", x + 860, yi - 60, 40, SOFT, "sans-medium", t_in=t1),
                   image(img, x, yi, 1680, vh, t1),
                   text(cap, x, yi + vh + 24, 44, INK, w=1680, t_in=t1)]
    layers.append(text("crops of unedited editor screenshots: the profiler's rows and graph", PAD, yi + vh + 100, 40, GHOST, w=3400, t_in=t1))
    t2 = at("B27", "Averaged timer runs")
    rows = ["Visual Profiler, selected frames: A +0.69 ms (first pair) · +4.59 ms (second pair) · budget 0.75",
            "Viewport timer, A r2: −0.06 (5 trials) · +0.39 · +0.19 (3 trials) · +0.17 (15-trial median)",
            "B: profiler −1.40 ms; timer deltas change sign → noise · celebration: +0.91 ms on 29 October (over 0.4)"]
    layers += [rect(PAD, TOP + 1130, 3418, 410, t_in=t2)]
    for k, r in enumerate(rows):
        layers.append(text(r, PAD + 60, TOP + 1170 + k * 95, 46, INK, w=3300, t_in=t2))
    t3 = at("B27", "not settled")
    layers.append(text("A's GPU budget: unresolved", PAD + 60, TOP + 1460, 56, SPARK, "sans-medium", w=3300, t_in=t3))
    spec_write("B27", layers, d)


def b28():
    d = dur("B28")
    cards = [("Mistakes caught", "No study textures (fixed in a6-r2) · two test fixtures ran before their setup (fixtures fixed, game untouched) · "
              "“3 px wide” narrated for a radius · an old “GPU within noise” line kept after later runs disagreed", "Mistakes caught"),
             ("Claude against Bao", "No strip reading was overruled; Bao recorded no disagreement. The strips corrected Claude's "
              "predictions twice: r1's footprint, r2's colour.", "No strip reading"),
             ("Still uncertain", "A's GPU budget on the proxy · no GPU time on the shipped renderer · first frame 0.41 of a "
              "character height · r2 paler than the brief's yellow-orange", "Still uncertain"),
             ("Next step", "Measure A at its cap in the editor Visual Profiler over many frames, with a capped frame rate, "
              "and report the mean, not one selected frame.", "The next step"),
             ("Who did what", "Bao: observations, approvals, keep decisions, the process/draw explanation, the 9 November brief. "
              "Claude Code: scenes, controller, tests, captures, comparisons, this film, the 29 October brief draft. "
              "Codex: editor conversion, profiler captures, two tests.", "Bao made every observation"),
             ("Textures · revision", "spark.png: 3 × 3 cross written by scripts/generate_spark_texture.py, no external asset. "
              f"Game art FLUX.1-schnell, sound Stable Audio Open, music MusicGen (SOURCES.md). Shown: godot {REV} on commit c6e6343.",
              "three-by-three")]
    layers = frame_chrome("The rest of the record", "TEST-REPORT.md · TUNING.md · CONTRIBUTIONS-assignment-6.md · godot/assets/particles/ATTRIBUTION.md",
                          f"film source: {REV}")
    cw, chh = 1680, 490
    for k, (title, body, cue) in enumerate(cards):
        t = at("B28", cue)
        x = PAD + (k % 2) * (cw + 58)
        y = TOP + (k // 2) * (chh + 42)
        layers += [rect(x, y, cw, chh, t_in=t),
                   text(title, x + 44, y + 34, 64, SPARK, "serif", w=cw - 88, t_in=t),
                   text(body, x + 44, y + 125, 48, INK, w=cw - 88, t_in=t, spacing=1.28)]
    spec_write("B28", layers, d)


BUILDERS = {"B03": b03, "B05": b05, "B07": b07, "B08": b08, "B10": b10, "B12": b12, "B14": b14, "B16": b16, "B18": b18,
            "B20": b20, "B22": b22, "B24": b24, "B26": b26, "B27": b27, "B28": b28}

if __name__ == "__main__":
    want = sys.argv[1:] or list(BUILDERS)
    for bid in want:
        BUILDERS[bid]()
