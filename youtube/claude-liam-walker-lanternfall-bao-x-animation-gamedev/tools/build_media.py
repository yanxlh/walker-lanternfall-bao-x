#!/usr/bin/env python3
"""Build media/<BID>.mp4 for every evidence beat of the animation film (4K, 30 fps).

Everything shown is real: the 4K Movie Maker take in capture/ (recorded by Bao with capture-film-take.command), Bao's
committed 30 fps fixture strips, committed images and recorded tool output in the repository, and the take's own
per-frame log. Replays are labelled. Code lines and records are read from git (tools/src.py), never the working tree.
Layout and helpers follow the Assignment 5 film's evidence beats (same chrome, same compose.py).

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
from src import SHA as FULL_SHA, repo_text  # noqa: E402

RECORDS_REV = "9e2e958"     # TUNING.md / TEST-REPORT.md / CONTRIBUTIONS with Bao's words in English

W, H, FPS = 3840, 2160, 30
PAD, TITLE_Y, TOP, BOT = 211, 97, 346, 1901
RIGHT = W - PAD
INK, SOFT, GHOST, SPARK, PAGE, CARD, BORDER = "#3D3929", "#73705F", "#A9A491", "#D97757", "#FAF9F5", "#FFFFFF", "#E5E2D9"
GOOD, DARK, AMBER = "#4F7A4A", "#202531", "#B8860B"
SHA = FULL_SHA[:7]
SHEET = json.loads((REEL / "beat_sheet.json").read_text())
BEATS = {b["beat_id"]: b for b in SHEET["beats"]}
REPO_REL = "../.."          # repository root, relative to the reel (compose.py resolves sources from the reel)
TAKE = "capture/take-dash.avi"
TAKE_LOG = "capture/take-dash-log.jsonl"
CAP = REPO / "captures"
FIXTURE = "Fixture capture · recorded by Bao · 30 fps · frame N = frames.log line N"
TAKE_LABEL = "Real engine capture of " + "{sha}" + " · scripted input · fixtures: no spawns, the dash card set first, a wraith placed for each hit"


def font(name, size):
    return ImageFont.truetype(str(FONT_FILES[name]), size)


class Take:
    """The film take's per-frame log (capture/take-dash-log.jsonl): row N describes movie frame N."""
    def __init__(self):
        self.rows = [json.loads(l) for l in (REEL / TAKE_LOG).read_text().splitlines()]

    def first(self, event, after=0):
        return next(r["frame"] for r in self.rows[after:] if event in r["events"])

    def all(self, event):
        return [r["frame"] for r in self.rows if event in r["events"]]

    def row(self, frame):
        return self.rows[max(0, min(frame, len(self.rows) - 1))]


def log_rows(path):
    return [dict(kv.split("=", 1) for kv in l.split()) for l in Path(path).read_text().splitlines()]


def records(path):
    return repo_text(path, RECORDS_REV)
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
    h = (lh * len(lines)) + (150 if title else 80)
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


# ---------------------------------------------------------------- shared pieces

def strip_tiles(capture_dir, frames, tile, name):
    """Courier crops from a fixture strip's kept frames, centred on the logged screen position."""
    rows = log_rows(CAP / capture_dir / "frames.log")
    out = []
    for n in frames:
        r = rows[n]
        im = Image.open(CAP / capture_dir / f"frame{n:08d}.png").convert("RGB")
        s = im.width / 640
        cx, cy = float(r["sx"]) * s, float(r["sy"]) * s
        c = im.crop((int(cx - 36), int(cy - 48), int(cx + 36), int(cy + 24))).resize((tile, tile), Image.NEAREST)
        out.append((save_png(c, f"{name}-{n}"), r))
    return out


def tiles_row(tiles, x, y, tile, gap, t_in, labels, sublabels=None, t_out=None, sub_colours=None):
    layers = []
    for i, (src, r) in enumerate(tiles):
        xx = x + i * (tile + gap)
        layers.append(text(labels[i], xx, y, 40, INK, "sans-medium", w=tile + gap, t_in=t_in, t_out=t_out))
        layers.append(image(src, xx, y + 70, tile, tile, t_in=t_in, t_out=t_out, nearest=True))
        if sublabels:
            colour = (sub_colours[i] if sub_colours else None) or SOFT
            layers.append(text(sublabels[i], xx, y + 90 + tile, 36, colour, "sans", w=tile + gap, t_in=t_in, t_out=t_out))
    return layers


def take_tiles(take, frames, tile, name):
    out = []
    for n in frames:
        r = take.row(n)
        cx, cy = r["sx"] * 6, r["sy"] * 6
        out.append((take_frame_png(n, (int(cx - 180), int(cy - 220), int(cx + 180), int(cy + 140)), 1, f"{name}-{n}"), r))
    return out


def take_readout(name, take, frame_at, duration, width=560, height=1555):
    f_t, f_s, f_l = font("serif", 66), font("sans", 38), font("sans", 42)

    def draw(img, t):
        fr = frame_at(t)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, width - 1, height - 1), 28, fill=CARD, outline=BORDER, width=3)
        d.text((40, 36), "From the take's log", font=f_t, fill=INK)
        d.text((42, 126), "one row per movie frame", font=f_s, fill=SOFT)
        d.line((40, 196, width - 40, 196), fill=BORDER, width=3)
        if fr is None:
            return ("none",)
        r = take.row(fr)
        phase = r["phase"] or "—"
        rows = [("state", r["state"], INK), ("pose", r["pose"], INK),
                ("sheet cell", str(r["cell"]) if r["cell"] >= 0 else "rig", INK if r["cell"] >= 0 else SPARK),
                ("dash phase", phase, SPARK if r["phase"] else GHOST),
                ("dash frame", str(r["dash_ticks"]) if r["phase"] else "—", INK if r["phase"] else GHOST),
                ("cooldown", str(r["cooldown"]), INK if r["cooldown"] else GHOST), ("hp", str(r["hp"]), INK)]
        y = 226
        for label, value, colour in rows:
            d.text((44, y), label, font=f_l, fill=SOFT)
            size = 72
            while size > 40 and d.textlength(value, font=font("serif-medium", size)) > width - 88:
                size -= 4
            d.text((44, y + 46), value, font=font("serif-medium", size), fill=colour)
            y += 182
        d.text((44, height - 66), f"take frame {fr} · tick {r['tick']}", font=f_s, fill=GHOST)
        return (fr,)
    return render_panel(name, width, height, duration, draw)


def take_layers(bid, take, segments, vw=2880, vh=1620, crop=None):
    """Video segments [(t0, first_frame, last_frame, label)], shown one after another, with the live readout."""
    layers = []
    for t0, f0, f1, label in segments:
        t1 = t0 + (f1 - f0 + 1) / FPS
        layers.append(video(f0, PAD, TOP, vw, vh, t_in=t0, t_out=t1, crop=crop))
        if crop:
            layers.append(text("centre crop of the 4K take (the camera follows the courier), 3x", PAD + vw - 1260, TOP + vh - 70, 40, "#FFF1C9", "sans", w=1240, t_in=t0, t_out=t1))
        if label:
            layers.append(rect(PAD + 30, TOP + 30, 820, 96, fill="#202531", outline="#202531", t_in=t0, t_out=t1))
            layers.append(text(label, PAD + 60, TOP + 50, 48, "#FFF1C9", "sans-medium", w=760, t_in=t0, t_out=t1))

    def frame_at(t):
        for t0, f0, f1, _ in segments:
            n = int(round((t - t0) * FPS))
            if 0 <= n <= f1 - f0:
                return f0 + n
        return None
    end = max(t0 + (f1 - f0 + 1) / FPS for t0, f0, f1, _ in segments)
    panel = take_readout(f"{bid}-readout", take, frame_at, end)
    layers.append(panel_layer(panel, PAD + vw + 40, TOP, 560, 1555, 0.0, end))
    return layers, end


def sheet_png():
    sheet = Image.open(REPO / "godot/assets/art/pc_sheet.png").convert("RGBA")
    s = 10
    up = sheet.resize((sheet.width * s, sheet.height * s), Image.NEAREST)
    im = Image.new("RGB", (up.width, up.height + 110), (232, 230, 222))
    im.paste(up, (0, 0), up)
    d = ImageDraw.Draw(im)
    f = font("sans-medium", 54)
    for i in range(10):
        x0 = i * 32 * s
        d.rectangle((x0, 0, x0 + 32 * s - 1, 32 * s - 1), outline=(169, 164, 145), width=3)
        d.text((x0 + 140, 32 * s + 18), str(i), font=f, fill=(61, 57, 41))
    for i in (2, 3):
        x0 = i * 32 * s
        d.rectangle((x0 + 2, 2, x0 + 32 * s - 3, 32 * s - 3), outline=(217, 119, 87), width=10)
    return save_png(im, "sheet-grid")


# ---------------------------------------------------------------- beats

def b05():
    d = dur("B05")
    t_strip, t_quote = at("B05", "Bao's own strip"), at("B05", "for drift")
    layers = frame_chrome("The sheet, cut into ten", "godot/assets/art/pc_sheet.png (Bao's Assignment 2 sheet, 10x) · captures/walk/r1 (Bao's fixture strip)")
    layers.append(image(sheet_png(), PAD + 109, TOP + 10, 3200, 430))
    tiles = strip_tiles("walk/r1", list(range(12)), 250, "walk-r1")
    labels = [f"f{n} · cell {r['cell']}" for n, (_, r) in zip(range(12), tiles)]
    subs = [r["pose"].replace("walk_", "") for _, r in tiles]
    layers += tiles_row(tiles, PAD, TOP + 560, 250, 34, t_strip, labels, subs,
                        sub_colours=[SPARK if r["pose"] == "cast" else None for _, r in tiles])
    layers.append(text(FIXTURE + " · captures/walk/r1", PAD, TOP + 1000, 40, SOFT, "sans", w=3418, t_in=t_strip))
    c, _ = card_lines(PAD, TOP + 1110, 3418, ["Bao, 20 November 2026: “Looked at it; no drift.”"], t_quote, size=64,
                      line_h=96, fill="#EEF3EC")
    layers += c
    spec_write("B05", layers, d)


def b07():
    d = dur("B07")
    take = Take()
    k = take.first("card key 1")
    d1 = take.first("dash key", k + 1)
    f0, f1 = k + 6, d1 - 2
    seg = (f1 - f0 + 1) / FPS
    layers = frame_chrome("The walk, in the running game", TAKE_LABEL.format(sha=SHA))
    v, end = take_layers("B07", take, [(0.0, f0, f1, ""), (seg, f0, f1, "Replay · same frames")], crop=[1280, 720, 1280, 720])
    layers += v
    t_seam, t_bao = at("B07", "The seam rule"), at("B07", "Bao watched")
    strip_frames = list(range(f0 + 20, f0 + 36))
    tiles = take_tiles(take, strip_frames, 340, "walk-take")
    labels = [f"f{n} · cell {r['cell']}" for n, (_, r) in zip(strip_frames, tiles)]
    layers += tiles_row(tiles[:8], PAD, TOP + 20, 340, 96, end, labels[:8], t_out=None)
    layers += tiles_row(tiles[8:], PAD, TOP + 470, 340, 96, end, labels[8:], t_out=None)
    layers.append(text(f"take frames {strip_frames[0]}–{strip_frames[-1]}, one tile per movie frame (two ticks), crops at 1:1 around the courier; the cell is the logged sheet cell",
                       PAD, TOP + 920, 40, SOFT, "sans", w=3418, t_in=end))
    j = json.loads(records("evidence/courier_clips.json"))
    seam = next(r for r in j["results"] if r["id"] == "walk-seam")
    o = seam["observed"]
    c1, h1 = card_lines(PAD, TOP + 1020, 3418, [f"first key {o['first']} · last key {o['last']} · key interval {round(o['interval_frames'])} frames · last key to end {round(o['tail_frames'])} frames · {seam['status']}",
                                             "Frame-track seam rule: no duplicate across the wrap, and the gap from the last key to the end equals the key interval"],
                        max(end, t_seam), size=50, line_h=84, title="Read-back: walk-seam (evidence/courier_clips.json)")
    c2, _ = card_lines(PAD, TOP + 1020 + h1 + 40, 3418, ["The cycle seam, five wraps at normal speed: no problem reported (Bao, 20 November 2026; TEST-REPORT HUMAN CHECKS)"],
                       max(end, t_bao), size=50, line_h=84, fill="#EEF3EC")
    layers += c1 + c2
    spec_write("B07", layers, d)


def b09():
    d = dur("B09")
    t_strip, t_rev = at("B09", "Bao's strip"), at("B09", "six, ten, twelve")
    rows = ["Startup    begins on frame 0     key at 0 s",
            "Active     begins on frame 4     key at 4/60 = 0.0667 s",
            "Recovery   begins on frame 14    key at 14/60 = 0.2333 s",
            "Ends       on frame 20           key at 20/60 = 0.3333 s"]
    j = json.loads(records("evidence/courier_clips.json"))
    bnd = [r for r in j["results"] if r["id"].startswith("dash-phase-boundaries")]
    rows.append(f"read-back: {sum(r['status'] == 'PASS' for r in bnd)}/{len(bnd)} tracks keyed at 0 / 4 / 14 / 20")
    layers = frame_chrome("The table, the keys, the strip", "CHANGE-BRIEF.md (Bao's phase table) · godot/animations/courier_clips.tres · captures/dash/r1 (Bao's fixture strip)")
    c, h = card_lines(PAD, TOP, 3418, rows, 0.0, size=50, mono=True, line_h=78, title="Phase table → key times (60 per second)")
    layers += c
    tiles = strip_tiles("dash/r1", [5, 7, 12, 15], 520, "dash-r1")
    lab = {5: "trigger", 7: "active begins", 12: "recovery begins", 15: "dash ends"}
    labels = [f"f{n} · {lab[n]}" for n in (5, 7, 12, 15)]
    subs = [f"tick {r['tick']} · dash frame {r['dash_ticks'] if r['phase'] else '—'} · {r['phase'] or 'walk'}" for _, r in tiles]
    y = TOP + h + 50
    layers += tiles_row(tiles, PAD, y, 520, 80, t_strip, labels, subs)
    layers.append(text(FIXTURE + " · captures/dash/r1", PAD + 2420, y + 120, 40, SOFT, "sans", w=1000, t_in=t_strip))
    c2, _ = card_lines(PAD + 2420, y + 360, 998, ["r0 6 / 10 / 12 → r1 4 / 10 / 6", "proposal: a Codex reading", "Bao: “Keep 4/10/6.”"],
                       t_rev, size=48, line_h=80, fill="#FBEFEA", title="Revision r1")
    layers += c2
    spec_write("B09", layers, d)


def b11():
    d = dur("B11")
    take = Take()
    k = take.first("card key 1")
    d1 = take.first("dash key", k + 1)
    f1 = d1 + 30
    layers = frame_chrome("The card, the walk, the dash", TAKE_LABEL.format(sha=SHA))
    # Start on the first frame that shows the fixture's offer; frame 20 still shows the random offer (CAPTURE.md).
    f0 = take.first("offer set: dash, heal, heal")
    v, end = take_layers("B11", take, [(0.0, f0, f1, "")])
    layers += v
    strip_frames = list(range(d1, d1 + 12))
    tiles = take_tiles(take, strip_frames, 380, "dash1-take")
    labels = [f"{r['phase'] or 'walk'} {r['dash_ticks'] if r['phase'] else ''}" for _, r in tiles]
    layers += tiles_row(tiles[:6], PAD, TOP + 20, 380, 160, end, labels[:6])
    layers += tiles_row(tiles[6:], PAD, TOP + 500, 380, 160, end, labels[6:])
    layers.append(text(f"take frames {d1}–{d1 + 11}: the first dash, one tile per movie frame (two ticks), crops at 1:1 around the courier; phase and dash frame from the log",
                       PAD, TOP + 980, 40, SOFT, "sans", w=3418, t_in=end))
    t_m = at("B11", "Measured by the edge tests")
    lines = []
    for fps in (30, 60, 144):
        jj = json.loads(records(f"evidence/dash_edges_{fps}fps.json"))
        o = next(r for r in jj["results"] if r["id"].startswith("two-clocks"))["observed"]
        lines.append(f"{fps:>3} fps: clip vs gameplay tick {o['largest_clip_vs_gameplay_s']:.4f} s · render vs physics span {o['render_vs_physics_lag_span_s']:.4f} s · one tick {o['one_tick_s']:.4f} s")
    c, _ = card_lines(PAD, TOP + 1080, 3418, lines, max(end, t_m), size=50, mono=True, line_h=84,
                      title="Two clocks, measured on every rendered frame (test_dash_edges.gd)")
    layers += c
    spec_write("B11", layers, d)


def b13():
    d = dur("B13")
    take = Take()
    hits = take.all("wraith placed")
    keys = take.all("dash key")
    f0, f1 = keys[1] - 15, hits[2] + 40
    layers = frame_chrome("A hit in every phase", TAKE_LABEL.format(sha=SHA))
    v, end = take_layers("B13", take, [(0.0, f0, f1, "")], crop=[1280, 720, 1280, 720])
    layers += v
    y = TOP + 20
    for i, h in enumerate(hits):
        before, after = take.row(h - 1), take.row(h + 2)
        phase = before["phase"]
        frame_no = before["dash_ticks"] + 2 if phase else 0
        outcome = {"startup": "cancelled · no cooldown", "active": "the dash carries on", "recovery": "cancelled · cooldown 60"}[phase]
        hit_frames = [h - 1, h, h + 1, h + 3]
        tiles = take_tiles(take, hit_frames, 340, f"hit{i}")
        labels = [f"f{n} · {r['pose']}" for n, (_, r) in zip(hit_frames, tiles)]
        layers += tiles_row(tiles, PAD, y, 340, 50, end, labels)
        layers.append(text(f"{phase} frame {frame_no}: {outcome} · hp {before['hp']} → {after['hp']}",
                           PAD + 1640, y + 210, 54, INK, "sans-medium", w=1770, t_in=end))
        y += 450
    t_e = at("B13", "The edge tests")
    jj = json.loads(records("evidence/dash_edges_60fps.json"))
    edges = [r for r in jj["results"] if r["id"].startswith(("hit-before", "hit-on", "hit-after"))]
    line = f"test_dash_edges.gd: {sum(r['status'] == 'PASS' for r in edges)}/{len(edges)} hits a frame before, on and after boundaries 4, 14, 20 pass at 60 fps (also at 30 and 144)"
    layers.append(text(line, PAD, TOP + 1390, 46, SOFT, "sans", w=3418, t_in=max(end, t_e)))
    spec_write("B13", layers, d)


def b15():
    d = dur("B15")
    t_m, t_p, t_h = at("B15", "four mutations"), at("B15", "One surprise"), at("B15", "What no headless run")
    j = json.loads(records("evidence/courier_clips.json"))
    groups = [("frame keys", "-frame-keys"), ("cells inside the sheet", "-frames-inside-sheet"), ("discrete updates", "-discrete"),
              ("length and loop mode", "-length-and-loop"), ("Animation.step", "-step"), ("dash keys, boundaries, spacing", "dash-")]
    lines = [f"{j['checks'] - j['failures']}/{j['checks']} checks pass · every-track-resolves: {next(r['status'] for r in j['results'] if r['id'] == 'every-track-resolves')}"]
    for label, key in groups:
        rs = [r for r in j["results"] if key in r["id"]]
        lines.append(f"{label}: {sum(r['status'] == 'PASS' for r in rs)}/{len(rs)}")
    c1, h1 = card_lines(PAD, TOP, 1660, lines, 0.0, size=54, line_h=80, title="Read-back (evidence/courier_clips.json)")
    m = json.loads(records("evidence/assignment-7/mutations/mutations-required.json"))
    names = {"required-1-track-subname-broken": "Rig/Hips:rotation → rotaton", "required-2-cycle-loop-mode-none": "walk loop_mode = 0",
             "required-3-key-a-cell-the-sheet-lacks": "a walk key on cell 10", "required-4-reimport-from-empty-cache": "reimport from an empty cache"}
    mlines = []
    for r in m["mutations"]:
        if r["mutation"] in names:
            res = r["runs"][0]
            fails = len(res["failed_checks"])
            mlines.append(f"{names[r['mutation']]}: " + (f"{fails} check{'s' if fails != 1 else ''} fail{'' if fails != 1 else 's'}, exit {res['exit']}" if r["expect"] == "fail" else f"passes, exit {res['exit']} (expected)"))
    c2, h2 = card_lines(PAD + 1720, TOP, 1698, mlines + ["each in a fresh git worktree, no import cache"], t_m, size=54, line_h=84,
                        title="The four required mutations")
    p = json.loads(records("evidence/assignment-7/godot3-names/probe.json"))
    plines = [f"Animation loop = true → loop_mode {p['tres_loop_true']['loop_mode']} (LOOP_LINEAR): it loops",
              f"playback_speed = 2 → speed_scale {p['script_set_playback_speed_2']['speed_scale']}: ignored",
              f"AnimatedSprite2D playing = true → playing: {p['animated_sprite_frames_playing']['is_playing']}"]
    y = TOP + max(h1, h2) + 40
    c3, h3 = card_lines(PAD, y, 3418, plines, t_p, size=54, line_h=80, title="Godot 3 names in 4.7.2 (evidence/assignment-7/godot3-names/probe.json)")
    c4, _ = card_lines(PAD, y + h3 + 40, 3418, ["whether the walk wraps without a visible seam, whether the three dash phases read in play, whether the courier is readable on dark and light ground, whether the timing feels right"],
                       t_h, size=54, line_h=160, fill="#FBEFEA", title="What the headless runs cannot show (TEST-REPORT.md)")
    layers = frame_chrome("What the read-backs proved", "Recorded tool output · evidence/courier_clips.json · evidence/assignment-7/mutations/mutations-required.json")
    layers += c1 + c2 + c3 + c4
    spec_write("B15", layers, d)


def b17():
    d = dur("B17")
    t_c, t_b = at("B17", "Claude's reading"), at("B17", "Bao judged it")
    layers = frame_chrome("Revision two: before and after", "captures/dash/r1 and captures/dash/r2 (Bao's fixture strips) · TUNING.md")
    frames = [4, 5, 7, 12, 15]
    lab = {4: "before", 5: "trigger", 7: "active begins", 12: "recovery begins", 15: "dash ends"}
    for row, rev in enumerate(("r1", "r2")):
        tiles = strip_tiles(f"dash/{rev}", frames, 400, f"cmp-{rev}")
        y = TOP + row * 520
        layers.append(text(rev, PAD, y + 160, 110, INK, "serif"))
        layers += tiles_row(tiles, PAD + 240, y, 400, 236, 0.0, [f"f{n} · {lab[n]}" for n in frames])
    layers.append(text(FIXTURE + " · same position, logs identical tick for tick", PAD, TOP + 1030, 40, SOFT, "sans", w=3418))
    c1, _ = card_lines(PAD, TOP + 1120, 1680, ["the back-of-coat outline sits outside the sheet's dark ink, so on dark slate it can read as a detached line"],
                       t_c, size=52, line_h=140, title="Claude's reading (a claim)")
    c2, _ = card_lines(PAD + 1740, TOP + 1120, 1678, ["“Keep. It is clearer.”  — Bao, in play, 20 November 2026"], t_b, size=52, line_h=120,
                       title="Bao's verdict", fill="#EEF3EC")
    layers += c1 + c2
    spec_write("B17", layers, d)


def b19():
    d = dur("B19")
    t_u, t_n = at("B19", "Still uncertain"), at("B19", "The next step")
    wrong = ["the first pin record failed on a SCRIPT ERROR; the pin read the i-frames 60 ticks after the hit",
             "the edge test read the phase after the hit tick, and reported the hit as landing on no dash",
             "the structure test compared the clip with the state after the whole tick, not the pose inside step()",
             "the r1 re-pin missed a hard-coded before.size() == 5 until it failed at all three rates",
             "a header edit failed inside a chained command and the commit went through without it (fixed in 6a340da)"]
    c1, h1 = card_lines(PAD, TOP, 2140, wrong, 0.0, size=56, line_h=160, title="Agent mistakes caught (TEST-REPORT.md, shortened)")
    unc = ["no reference dash was measured", "4 / 10 / 6 came from a Codex reading, not from play",
           "the real-input pin was added after the change (verified on 9ccf078)", "the r2 outline can read detached on the coat's back"]
    c2, h2 = card_lines(PAD + 2200, TOP, 1218, unc, t_u, size=56, line_h=160, title="Still uncertain")
    c3, _ = card_lines(PAD + 2200, TOP + h2 + 40, 1218, ["Measure a reference dash, write its frames into the phase table, and retime from it."],
                       t_n, size=56, line_h=220, title="One next step", fill="#EEF3EC")
    layers = frame_chrome("Mistakes, open questions, next", "TEST-REPORT.md (Assignment 7) · README.md Known limitations · TUNING.md")
    layers += c1 + c2 + c3
    spec_write("B19", layers, d)


def b20():
    d = dur("B20")
    t_c, t_s, t_r = at("B20", "Claude Code"), at("B20", "The sheet"), at("B20", "The code you saw")
    bao = ["chose the dash and its rules: not invincible, a cooldown, unlocked by a card",
           "wrote the brief and the seven answers (18 November); kept 4 / 10 / 6",
           "saw the body vanish on dark slate, predicted the outline, approved it, kept it",
           "recorded the strips dash r1, walk r1, dash r2; the human checks; reviewed CLAUDE.md"]
    c1, h1 = card_lines(PAD, TOP, 1990, bao, 0.0, size=54, line_h=160, title="Bao (CONTRIBUTIONS-assignment-7.md)")
    ai = ["Claude Code (Claude Opus 5.5): the brief's first draft, CLAUDE.md, the builder and clips, the state machine and the dash, every test, probes, mutation runs, capture kits, records, and this film",
          "Codex: the 4 / 10 / 6 proposal"]
    c2, h2 = card_lines(PAD + 2050, TOP, 1368, ai, t_c, size=54, line_h=370, title="AI contributions")
    credit = ["Sheet: pc_sheet.png, Bao's own Assignment 2 sheet (ART-PC-01), FLUX.1-schnell 741f7c3, Apache-2.0, checked 13 November 2026",
              f"Source revision shown: {FULL_SHA}"]
    c3, _ = card_lines(PAD, TOP + 1555 - 300, 3418, credit, t_s, size=50, line_h=80)
    layers = frame_chrome("Who did what", "CONTRIBUTIONS-assignment-7.md · prompts/assignment-7.md · godot/assets/art/ATTRIBUTION.md")
    layers += c1 + c2 + c3
    spec_write("B20", layers, d)


BUILDERS = {"B05": b05, "B07": b07, "B09": b09, "B11": b11, "B13": b13, "B15": b15, "B17": b17, "B19": b19, "B20": b20}

if __name__ == "__main__":
    want = sys.argv[1:] or list(BUILDERS)
    for bid in want:
        BUILDERS[bid]()
