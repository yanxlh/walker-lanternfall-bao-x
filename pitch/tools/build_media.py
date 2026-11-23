#!/usr/bin/env python3
"""Draw every beat of the pitch film into media/<BID>.mp4 (3840 x 2160, 30 fps, no audio; art final adds narration).

Boards are layered with tools/compose.py (copied from the Assignment 7 film). Real pictures come only from files:
the cleaned take capture/clean/take-pitch-seed21.mov (tag a7, scripted input) and committed captures from earlier
assignments. Everything else is a constructed diagram and says so on screen. Board text uses the beat sheet's cue
times (word starts of the measured narration). No instructor name, handle or outro appears.

    ~/.venvs/general/bin/python tools/build_media.py [BID ...]
"""
import json, math, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parent
WORK = REEL / "media" / "_work"
TAKE = "capture/clean/take-pitch-seed21.mov"
FONTS = Path("/Users/yxlh/brutalist.art/runtime/fonts")
FONT_FILES = {"serif": FONTS / "EB_Garamond/static/EBGaramond-Regular.ttf",
              "serif-medium": FONTS / "EB_Garamond/static/EBGaramond-Medium.ttf",
              "sans": FONTS / "Inter/static/Inter_28pt-Regular.ttf",
              "sans-medium": FONTS / "Inter/static/Inter_28pt-Medium.ttf",
              "mono": FONTS / "PT_Mono/PTMono-Regular.ttf"}
INK, DIM, CARD, BORDER, TERRA, BG = "#3D3929", "#564739", "#FFFDF8", "#CFC6B5", "#D97757", "#FAF9F5"
GOLD, NIGHT, MIST = "#F2B84B", "#14121C", "#C7D0E0"
CHIP = {"implemented": "#2F5D3A", "observed": "#2F5D3A", "proposed": "#7A4A2A", "comparison": INK}
SHEET = json.loads((REEL / "beat_sheet.json").read_text())
BEATS = {b["beat_id"]: b for b in SHEET["beats"]}
SIGN = "Bao Xing · Lanternfall: First Delivery · pitch"


def dur(bid):
    return float(BEATS[bid]["actual_duration_s"])


def cue(bid, phrase):
    for c in BEATS[bid]["shot"].get("cues", []):
        if c["phrase"] == phrase:
            return float(c["at"])
    raise SystemExit(f"{bid}: no cue {phrase!r}")


def font(name, size):
    return ImageFont.truetype(str(FONT_FILES[name]), size)


# ---- layer helpers (compose.py spec entries) ----
def T(text, x, y, size, color=INK, f="sans", w=0, align="left", t0=0.0, t1=None, fade=0.3, spacing=1.25):
    return {"kind": "text", "text": text, "x": x, "y": y, "size": size, "color": color, "font": f, "w": w,
            "align": align, "spacing": spacing, "t": [t0, t1], "fade": fade}


def R(x, y, w, h, fill=CARD, outline=BORDER, width=4, radius=28, t0=0.0, t1=None, fade=0.3):
    return {"kind": "rect", "x": x, "y": y, "w": w, "h": h, "fill": fill, "outline": outline, "width": width,
            "radius": radius, "t": [t0, t1], "fade": fade}


def I(src, x, y, w, h, t0=0.0, t1=None, nearest=False, fade=0.3):
    return {"kind": "image", "src": src, "x": x, "y": y, "w": w, "h": h, "t": [t0, t1], "fade": fade,
            "resample": "nearest" if nearest else "lanczos"}


def V(ss, x, y, w, h, t0, t1):
    return {"kind": "video", "src": TAKE, "ss": ss, "x": x, "y": y, "w": w, "h": h, "t": [t0, t1], "fade": 0}


SAFE_SCALE = 0.96   # boards are laid out edge to edge, then shrunk about the centre into Gate V's title-safe area


def fit_safe(layers, k=SAFE_SCALE):
    for L in layers:
        L["x"] = round(1920 + (L["x"] - 1920) * k)
        L["y"] = round(1080 + (L["y"] - 1080) * k)
        for key in ("w", "h"):
            if L.get(key):
                L[key] = round(L[key] * k)
        if L["kind"] == "text":
            L["size"] = round(L["size"] * k)
        if L["kind"] == "rect":
            L["radius"] = round(L.get("radius", 0) * k)
    return layers


def render(bid, layers, bg=BG, safe=True):
    if safe:
        fit_safe(layers)
    d = dur(bid)
    total = math.ceil(d * 30 + 3) / 30          # a few frames of slack; art final trims to the narration
    for L in layers:
        if L["t"][1] is None:
            L["t"][1] = total
    spec = {"out": f"media/{bid}.mp4", "duration": total, "fps": 30, "bg": bg, "audio": None,
            "base": str(REEL), "layers": layers}
    WORK.mkdir(parents=True, exist_ok=True)
    p = WORK / f"{bid}.json"
    p.write_text(json.dumps(spec, indent=1))
    subprocess.run([sys.executable, str(REEL / "tools" / "compose.py"), str(p)], check=True)
    print(bid, "->", spec["out"], f"{total:.2f}s")


def chrome(bid, title, status, source):
    kind = BEATS[bid].get("design_status", "comparison")
    f = font("sans-medium", 46)
    tw = int(ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(status, font=f))
    return [T(title, 180, 92, 104, f="serif", t0=0, fade=0),
            R(180, 262, tw + 72, 84, fill=CHIP[kind], outline=None, width=0, radius=16, fade=0),
            T(status, 216, 276, 46, color=CARD, f="sans-medium", fade=0),
            T(source, 180, 2016, 40, color=DIM, w=2300, fade=0, spacing=1.3),
            T(SIGN, 2560, 2016, 40, color=DIM, w=1100, align="right", fade=0)]


def excerpt_panel(bid, section, x=180, y=400, w=1420, h=1540, size=52, t0=0.0):
    props = BEATS[bid]["shot"]["remotion"]["props"]
    s, e = props["source_lines"]
    shown = []
    for line in props["excerpt"].split("\n"):         # presentation only: outer table pipes and list dashes dropped
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            line = line[1:-1].strip()
        if line.startswith("- "):
            line = line[2:]
        shown.append(line)
    text = "\n".join(shown)
    f = font("sans", size)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    n = 0
    for para in text.split("\n"):
        cur, k = "", 1
        for wd in para.split(" "):
            nxt = wd if not cur else cur + " " + wd
            if probe.textlength(nxt, font=f) > w - 170 and cur:
                k, cur = k + 1, wd
            else:
                cur = nxt
        n += k
    ex_h = int(n * size * 1.36)
    where = f"line {s}" if s == e else f"lines {s}–{e}"
    return [R(x, y, w, h, t0=t0),
            T("GDD v0.3 · EXACT EXCERPT", x + 60, y + 50, 42, DIM, "sans-medium", t0=t0),
            T(section, x + 60, y + 118, 72, INK, "serif", w=w - 120, t0=t0),
            R(x + 60, y + 262, 10, ex_h, fill=TERRA, outline=None, width=0, radius=4, t0=t0),
            T(text, x + 100, y + 250, size, INK, "sans", w=w - 170, spacing=1.36, t0=t0),
            T(f"gdd/GDD-v0.3.md, {where}", x + 60, y + h - 92, 40, DIM, t0=t0)]


def card(x, y, w, h, title, body, t0, tag=None, title_size=62, body_size=48, outline=BORDER):
    out = [R(x, y, w, h, t0=t0, outline=outline),
           T(title, x + 50, y + 40, title_size, INK, "serif-medium", w=w - 100, t0=t0)]
    if body:
        out.append(T(body, x + 50, y + 60 + int(title_size * 1.4), body_size, INK, "sans", w=w - 100, t0=t0,
                     spacing=1.3))
    if tag:
        out.append(T(tag, x + 50, y + h - 80, 40, DIM, "sans-medium", t0=t0))
    return out


# ---- stills and drawings ----
def still(name, t, crop=None, scale=None):
    out = WORK / f"{name}.png"
    WORK.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", str(REEL / TAKE), "-frames:v", "1",
                    str(out)], check=True)
    return f"media/_work/{name}.png"


def crop_png(src, box, factor, name):
    im = Image.open(REPO / src).convert("RGBA").crop(box)
    im = im.resize((im.width * factor, im.height * factor), Image.NEAREST)
    out = WORK / f"{name}.png"
    im.save(out)
    return f"media/_work/{name}.png"


def drawing(name, w, h, draw_fn):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(im), im)
    out = WORK / f"{name}.png"
    WORK.mkdir(parents=True, exist_ok=True)
    im.save(out)
    return f"media/_work/{name}.png"


def gate_glyph(lit, restart=False):
    def fn(d, im):
        w, h = im.size
        cx = w // 2
        if lit:
            for r, a in ((230, 40), (170, 70), (115, 110)):
                d.ellipse((cx - r, 250 - r, cx + r, 250 + r), fill=(242, 184, 75, a))
        d.rectangle((cx - 16, 230, cx + 16, h - 120), fill="#8A5A3C", outline=INK, width=4)
        d.rectangle((cx - 110, 200, cx + 110, 232), fill="#8A5A3C", outline=INK, width=4)
        lamp = GOLD if lit else "#8B8F96"
        d.rectangle((cx - 60, 240, cx + 60, 330), fill=lamp, outline=INK, width=5)
        d.rectangle((cx - 90, h - 130, cx + 90, h - 96), fill="#6E5A44", outline=INK, width=4)
        if restart:
            f = font("sans-medium", 54)
            d.arc((40, 40, 170, 170), 40, 330, fill=INK, width=10)
            d.polygon([(150, 52), (182, 98), (128, 104)], fill=INK)
            d.text((200, 70), "restart", font=f, fill=INK)
    return fn


def turret_diagram(d, im):
    w, h = im.size
    cx, cy = 560, h // 2
    f, fs = font("sans-medium", 50), font("sans", 46)
    for i in range(0, 360, 10):                       # outer ring, dashed: release
        a0, a1 = math.radians(i), math.radians(i + 6)
        r = 330
        d.arc((cx - r, cy - r, cx + r, cy + r), i, i + 6, fill=INK, width=6)
    r = 230
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=6)
    d.rectangle((cx - 50, cy - 20, cx + 50, cy + 60), fill="#6E5A44", outline=INK, width=5)
    d.ellipse((cx - 40, cy - 70, cx + 40, cy + 10), fill=GOLD, outline=INK, width=5)
    d.line((cx + 30, cy - 30, cx + 150, cy - 110), fill=INK, width=12)
    for (ex, ey) in ((cx + 160, cy - 120), (cx - 270, cy + 120)):
        d.ellipse((ex - 26, ey - 26, ex + 26, ey + 26), fill="#3B4A6B", outline=INK, width=4)
    d.line((cx + 230, cy, 1040, cy - 60), fill=INK, width=4)
    d.text((1060, cy - 100), "acquire: inside the inner ring", font=f, fill=INK)
    d.line((cx + 330, cy + 40, 1040, cy + 80), fill=INK, width=4)
    d.text((1060, cy + 40), "release: outside the outer ring", font=f, fill=INK)
    d.text((1060, cy + 160), "the gap between them stops flicker", font=fs, fill=DIM)


def state_machine(d, im):
    w, h = im.size
    f, fs = font("sans-medium", 54), font("sans", 42)
    names = ["IDLE", "TRACK", "FIRE", "COOLDOWN"]
    bw, bh, gap, y = 360, 150, 120, 120
    xs = [20 + i * (bw + gap) for i in range(4)]
    for x, n in zip(xs, names):
        d.rounded_rectangle((x, y, x + bw, y + bh), radius=22, fill=CARD, outline=INK, width=5)
        tw = d.textlength(n, font=f)
        d.text((x + (bw - tw) / 2, y + 42), n, font=f, fill=INK)
    for i in range(3):
        x0, x1 = xs[i] + bw + 10, xs[i + 1] - 10
        d.line((x0, y + bh // 2, x1 - 20, y + bh // 2), fill=INK, width=6)
        d.polygon([(x1, y + bh // 2), (x1 - 30, y + bh // 2 - 18), (x1 - 30, y + bh // 2 + 18)], fill=INK)
    labels = ["target in range", "aimed", "shot fired"]
    for i, lab in enumerate(labels):
        tw = d.textlength(lab, font=fs)
        d.text(((xs[i] + bw + xs[i + 1]) / 2 - tw / 2, y - 62), lab, font=fs, fill=DIM)
    yb = y + bh + 110                                  # COOLDOWN -> TRACK, TRACK -> IDLE
    cx3, cx1, cx0 = xs[3] + bw // 2, xs[1] + bw // 2, xs[0] + bw // 2
    d.line((cx3, y + bh + 8, cx3, yb), fill=INK, width=5)
    d.line((cx3, yb, cx1 + 40, yb), fill=INK, width=5)
    d.line((cx1 + 40, yb, cx1 + 40, y + bh + 36), fill=INK, width=5)
    d.polygon([(cx1 + 40, y + bh + 8), (cx1 + 22, y + bh + 40), (cx1 + 58, y + bh + 40)], fill=INK)
    d.text((cx1 + 520, yb + 14), "ready again", font=fs, fill=DIM)
    d.line((cx1 - 40, y + bh + 8, cx1 - 40, yb - 50), fill=INK, width=5)
    d.line((cx1 - 40, yb - 50, cx0, yb - 50), fill=INK, width=5)
    d.line((cx0, yb - 50, cx0, y + bh + 36), fill=INK, width=5)
    d.polygon([(cx0, y + bh + 8), (cx0 - 18, y + bh + 40), (cx0 + 18, y + bh + 40)], fill=INK)
    d.text((cx0 + 30, yb - 40), "target lost", font=fs, fill=DIM)


def menu_sketch(d, im):
    w, h = im.size
    f, fb, fs = font("sans", 50), font("sans-medium", 54), font("sans", 40)
    d.rounded_rectangle((40, 40, w - 40, h - 40), radius=24, fill="#1F2540", outline=INK, width=5)
    d.text((90, 90), "POST OFFICE", font=fb, fill=GOLD)
    d.rounded_rectangle((90, 210, w - 90, 310), radius=14, fill="#3B4A6B", outline=GOLD, width=5)
    d.text((120, 230), "▶ Lamp-Head", font=f, fill="#FFF1C9")
    d.text((120, 350), "   Engineer", font=f, fill=MIST)
    d.text((120, 450), "   Start contract", font=f, fill=MIST)
    d.text((90, h - 170), "↑ ↓ choose · Enter start", font=fs, fill=MIST)


def window_sketch(d, im):
    w, h = im.size
    fb, fs = font("sans-medium", 50), font("sans", 42)
    d.rounded_rectangle((40, 40, w - 40, h - 40), radius=24, fill=CARD, outline=INK, width=5)
    d.rectangle((44, 44, w - 44, 120), fill="#D9D4C7")
    for i, c in enumerate(("#D97757", "#C7AE86", "#8B8F96")):
        d.ellipse((80 + i * 60, 66, 116 + i * 60, 102), fill=c)
    d.rounded_rectangle((w // 2 - 120, 230, w // 2 + 120, 470), radius=40, fill="#1F2540", outline=INK, width=5)
    d.rectangle((w // 2 - 30, 290, w // 2 + 30, 360), fill=GOLD, outline=INK, width=4)
    t = "Lanternfall.app"
    d.text((w / 2 - d.textlength(t, font=fb) / 2, 510), t, font=fb, fill=INK)
    t2 = "macOS build (planned)"
    d.text((w / 2 - d.textlength(t2, font=fs) / 2, 590), t2, font=fs, fill=DIM)


def terminal_sketch(lines):
    def fn(d, im):
        w, h = im.size
        f = font("mono", 48)
        d.rounded_rectangle((40, 40, w - 40, h - 40), radius=24, fill="#1E1B16", outline=INK, width=5)
        for i, (s, c) in enumerate(lines):
            d.text((90, 110 + i * 78), s, font=f, fill=c)
    return fn


def arrow(x, y, t0):
    return T("→", x, y, 110, INK, "sans", t0=t0)


# ---- beats ----
def b00():
    title = still("still-title", 1.0)
    L = [T("Lanternfall:", 180, 470, 200, f="serif", fade=0),
         T("First Delivery", 180, 690, 200, f="serif", fade=0),
         R(186, 950, 420, 12, fill=TERRA, outline=None, width=0, radius=4, t0=0.4),
         T("Bao Xing", 180, 1030, 92, f="serif-medium", t0=0.6),
         T("Final project pitch · CSYE 7270 · 23 November 2026", 180, 1180, 60, DIM, t0=0.9),
         R(180, 1400, 1700, 230, t0=2.0),
         T("Narration: an AI voice (Kokoro am_onyx) reading Bao's script, in Bao's words.", 230, 1440, 54,
           w=1600, t0=2.0, spacing=1.3),
         I(title, 2040, 470, 1620, 911, t0=1.0),
         T("Real capture, tag a7: the title screen today", 2040, 1410, 46, DIM, t0=1.0),
         T("In this film, gameplay is real capture of tag a7; anything not built yet is a labelled, constructed "
           "diagram.", 180, 1900, 46, DIM, w=3480, t0=2.4)]
    render("B00", L)


def b01():
    d = dur("B01")
    c1, c2, c3 = cue("B01", "full gauge"), cue("B01", "Max out"), cue("B01", "Survive three minutes")
    segs = [(1.0, 0.0, c1, "Run start · game clock 0:00"), (13.0, c1, c2, "Level-up card screen · 0:10"),
            (88.0, c2, c3, "Sunflare card, then the burst · 1:11"), (197.4, c3, d + 0.1, "3:00 · the fog lifts")]
    L = []
    for ss, a, b, label in segs:          # 1920 x 1080 take shown at 3200 x 1800 inside the title-safe area
        L.append(V(ss, 320, 110, 3200, 1800, a, b))
        L.append(R(2240, 1770, 1240, 96, fill="#14121CD9", outline=None, width=0, radius=14, t0=a, t1=b, fade=0))
        L.append(T(label, 2276, 1788, 50, "#FFF1C9", "sans-medium", t0=a, t1=b, fade=0))
    L.append(T("Real engine capture · scripted input (capture/pitch_driver.gd) · tag a7 = godot/ 5f09b7f · seed 21 · "
               "Movie Maker 1920×1080, 30 fps · game sound off · four excerpts at real speed",
               320, 1940, 44, MIST, w=3200, fade=0))
    render("B01", L, bg=NIGHT, safe=False)


def b02():
    L = chrome("B02", "What I will build", "PROPOSED · nothing on this board exists yet",
               "Excerpt: Bao's Assignment 4 GDD v0.3 (17 October 2026), converted to gdd/GDD-v0.3.md. "
               "Cards: the pitch's scope, constructed.")
    L += excerpt_panel("B02", "Development Scope", size=50)
    L += [T("One run becomes one delivery", 1720, 410, 84, f="serif", t0=6.0),
          T("a playable macOS build", 1720, 530, 54, DIM, t0=6.6)]
    cards = [("Post office menu", "the front door: pick a courier, start the contract", "post office menu"),
             ("One contract", "across the existing fog market", "one contract"),
             ("Lantern Gate", "the destination, the model from Assignment 3", "Lantern Gate"),
             ("The Engineer", "a second courier who places turrets", "the Engineer")]
    for i, (t, b, p) in enumerate(cards):
        x, y = 1720 + (i % 2) * 990, 680 + (i // 2) * 640
        L += card(x, y, 950, 580, t, b, cue("B02", p), tag="planned · not built", title_size=72, body_size=52)
    render("B02", L)


def b03():
    L = chrome("B03", "Why anyone would care", "PROPOSED · constructed diagram, not gameplay",
               "Diagram constructed for the pitch. The gate model is real (tag a3); its unlit and lit states and "
               "the saved record do not exist yet.")
    L += excerpt_panel("B03", "Design Pillars and Player Experience Goals", h=1000, size=58)
    g0, g1, g2 = (drawing(n, 560, 760, gate_glyph(lit, rs)) for n, lit, rs in
                  (("gate-unlit", False, False), ("gate-lit", True, False), ("gate-restart", True, True)))
    a, b = cue("B03", "delivery succeeds"), cue("B03", "still changed")
    xs = [1700, 2370, 3040]
    for x, g, t0, lab in zip(xs, (g0, g1, g2), (0.3, a, b),
                             ("Before: the route ends at the gate", "Delivered: the gate is lit",
                              "After a restart: still lit")):
        L += [R(x, 420, 620, 1060, t0=t0), I(g, x + 30, 460, 560, 760, t0=t0),
              T(lab, x + 40, 1250, 52, w=540, t0=t0, spacing=1.25)]
    L += [arrow(2318 - 20, 880, a), arrow(2988 - 20, 880, b),
          I("../evidence/a3/lantern-gate-room.png", 180, 1480, 640, 360, t0=0.3),
          T("The real Lantern Gate today: Assignment 3's separate 3D room (tag a3).", 860, 1530, 48, w=720,
            t0=0.3, spacing=1.3),
          R(1700, 1560, 1960, 300, t0=b),
          T("One saved delivery record, under save rules written before any save code.", 1750, 1610, 54,
            w=1860, t0=b, spacing=1.3)]
    render("B03", L)


def b04():
    L = chrome("B04", "What makes it different", "COMPARISON · game names only; no footage of other games",
               "Games played: Bao's answer, 23 November 2026. Run goals as stated in the narration. "
               "Lanternfall's side is proposed.")
    L.append(T("Games I have played", 180, 420, 64, f="serif"))
    games = ["Vampire Survivors", "Brotato", "20 Minutes Till Dawn", "Halls of Torment"]
    a, b, c = cue("B04", "Vampire Survivors, a run"), cue("B04", "Brotato, it's"), cue("B04", "Lanternfall gives")
    notes = {0: ("goal of a run: outlast the clock", a), 1: ("goal of a run: outlast twenty waves", b)}
    for i, g in enumerate(games):
        y = 560 + i * 300
        L += [R(180, y, 1560, 250, t0=0.2 + 0.3 * i), T(g, 240, y + 70, 70, f="serif-medium", t0=0.2 + 0.3 * i)]
        if i in notes:
            L += [R(180, y, 1560, 250, fill=None, outline=TERRA, width=8, t0=notes[i][1]),
                  T(notes[i][0], 900, y + 92, 48, INK, "sans-medium", t0=notes[i][1])]
    L += card(1900, 560, 1760, 1150, "Lanternfall (proposed)",
              "A run is a delivery to a named place.\n\nA successful delivery leaves that place changed, and the "
              "change survives a restart.", c, title_size=88, body_size=72)
    render("B04", L)


def b05():
    L = chrome("B05", "The second courier: the Engineer",
               "PROPOSED · constructed diagram; the Engineer and its turret do not exist yet",
               "Excerpt: the GDD's Initial Courier Roster. Diagrams constructed for the pitch. The turret state "
               "machine is the planned Assignment 9 technique (due 12 December 2026).")
    L += excerpt_panel("B05", "Initial Courier Roster", h=1000, size=56)
    L += [T("Every courier: one advantage, one rule change, one weakness (GDD).", 180, 1460, 52, w=1420,
            t0=2.5, spacing=1.3)]
    td = drawing("turret", 1960, 760, turret_diagram)
    sm = drawing("state-machine", 1960, 560, state_machine)
    a, b, c = cue("B05", "turret holds an area"), cue("B05", "state machine"), cue("B05", "Assignment nine")
    L += [R(1700, 400, 1960, 780, t0=a), I(td, 1700, 410, 1960, 760, t0=a),
          R(1700, 1220, 1960, 600, t0=b), I(sm, 1700, 1240, 1960, 560, t0=b),
          T("Planned Assignment 9 technique. If A9 changes it, the change is logged in FRICTIONAL.md.", 1700,
            1860, 46, DIM, w=1960, t0=c)]
    render("B05", L)


def b06():
    L = chrome("B06", "Who opens it: the first sixty seconds",
               "PROPOSED · constructed storyboard; the post office menu does not exist yet",
               "Storyboard constructed for the pitch, except the third frame (real capture, tag a7) and the "
               "command, which exists at tag a7.")
    L.append(T("Target role: gameplay programmer  ·  Reader: a hiring manager or a lead gameplay engineer",
               180, 400, 58, w=3480))
    a, c, d4, e = cue("B06", "In the first minute"), cue("B06", "press Enter"), cue("B06", "one test command"), \
        cue("B06", "Godot four")
    b = round((a + c) / 2, 2)
    L += [R(180, 560, 3480, 10, fill=INK, outline=None, width=0, radius=4, t0=a)]
    for x, lab in ((180, "0 s"), (1060, "10 s"), (1940, "30 s"), (2820, "after 60 s")):
        L.append(T(lab, x, 590, 46, DIM, "sans-medium", t0=a))
    win = drawing("window", 820, 760, window_sketch)
    menu = drawing("menu", 820, 760, menu_sketch)
    play = still("still-play", 6.5)
    term = drawing("terminal", 820, 760, terminal_sketch([("$ scripts/run-all-a7.sh", "#FFF1C9"),
                                                         ("23 runs", MIST), ("exit 0 each", MIST)]))
    frames = [(180, win, a, "Open the Mac build", "constructed"),
              (1060, menu, b, "Post office menu, focus set", "constructed"),
              (1940, None, c, "Moving, the Beam firing", "real capture, tag a7"),
              (2820, term, d4, "The lead runs the tests", "today's command (tag a7)")]
    for x, img, t0, lab, tag in frames:
        L.append(R(x, 680, 840, 1000, t0=t0))
        if img:
            L.append(I(img, x + 10, 690, 820, 760, t0=t0))
        else:
            L.append(I(play, x + 20, 840, 800, 450, t0=t0))
        L += [T(lab, x + 40, 1470, 50, INK, "sans-medium", w=760, t0=t0), T(tag, x + 40, 1560, 42, DIM, t0=t0)]
    L += [R(180, 1730, 3480, 120, fill="#F2E5D8", outline=BORDER, t0=e),
          T("Godot 4.7.2 · GDScript · GL Compatibility renderer · export target: macOS desktop (Apple Silicon)",
            230, 1760, 54, t0=e),
          T("Unknown yet: whether the macOS unsigned-app warning costs a stranger more than a minute; I will time "
            "it on a fresh macOS user account.", 180, 1880, 42, DIM, w=3480, t0=e)]
    render("B06", L)


def b07():
    L = chrome("B07", "What it proves", "OBSERVED · real captures and recorded test runs",
               "Captures committed in this repository: captures/a5-materials (d01df00), captures/defeat_sparks "
               "(a6), captures/dash/r1 (a7). Test counts: evidence/assignment-7 and pitch/evidence.")
    L.append(T("New systems added to a working game, each pinned by tests a stranger can rerun.", 180, 400, 62,
               w=3480))
    dash = crop_png("captures/dash/r1/frame00000012.png", (573, 312, 733, 402), 6, "dash-crop")
    tiles = [("../captures/a5-materials/20261030-131249-compare-shader-baseline/compare-shader-baseline.png",
              "Shaders and materials · a5", "hand-written cobblestone_surface on the material-room floor",
              "hand-written shaders", False),
             ("../captures/defeat_sparks/comparison-r0-r1/comparison-detail.png", "Particle effects · a6",
              "hit-spark bursts, fixture capture; cost report in evidence/assignment-6/cost", "particle effects", True),
             (dash, "Animation and state · a7",
              "the dash, active phase; 23 headless runs pass from a fresh clone; 8 of 8 mutations caught",
              "animation driven", True)]
    for i, (src, t, sub, p, nearest) in enumerate(tiles):
        x, t0 = 180 + i * 1190, cue("B07", p)
        L += [R(x, 540, 1110, 1120, t0=t0), I(src, x + 30, 570, 1050, 640, t0=t0, nearest=nearest),
              T(t, x + 40, 1240, 58, INK, "serif-medium", w=1030, t0=t0),
              T(sub, x + 40, 1340, 46, INK, w=1030, t0=t0, spacing=1.3)]
    z = cue("B07", "can't prove")
    L += [R(180, 1720, 3480, 200, fill="#F2E5D8", outline=TERRA, width=6, t0=z),
          T("It cannot prove that the game is fun, or that an export runs where I did not run it. "
            "No playtest is claimed.", 230, 1762, 54, w=3380, t0=z)]
    render("B07", L)


def b08():
    L = chrome("B08", "In, out, and why", "PROPOSED · scope for tag a10, due 20 December 2026",
               "Excerpt: the GDD's Risks and Mitigations table, row R-01. Lists: the pitch's scope (PROJECT-BRIEF.md).")
    L += excerpt_panel("B08", "Risks and Mitigations", h=1100, size=56)
    ins = ["Delivery objective and result (F-04)", "Post office menu, keyboard only", "One contract on the market route",
           "The Engineer and a capped turret", "One saved delivery record", "Lantern Gate lit after a delivery",
           "macOS export"]
    outs = ["The other four couriers", "A difficulty selector", "More maps and the fog boss",
            "Progression beyond one record", "Multiplayer", "Web, mobile and XR"]
    o, r = cue("B08", "What's out"), cue("B08", "My own risk table")
    L += [R(1700, 400, 940, 1500, t0=0.3), T("In", 1750, 440, 80, f="serif", t0=0.3),
          T("\n".join(ins), 1750, 590, 52, w=850, spacing=1.6, t0=0.5),
          R(2720, 400, 940, 1500, t0=o), T("Out, on purpose", 2770, 440, 80, f="serif", t0=o),
          T("\n".join(outs), 2770, 590, 52, w=850, spacing=1.6, t0=o),
          R(180, 400, 1420, 1100, fill=None, outline=TERRA, width=10, t0=r),
          T("Build order from R-01: one screen, one contract, the Engineer.", 180, 1560, 54, w=1420, t0=r,
            spacing=1.3)]
    render("B08", L)


def b09():
    L = chrome("B09", "What comes first", "COMPARISON · today is a real capture (tag a7); the delivery is proposed",
               "Left image: real capture of tag a7 (seed 21, scripted input). Flow and test: proposed; "
               "test_delivery.gd does not exist yet.")
    L += excerpt_panel("B09", "Open Questions", h=880, size=56)
    win = still("still-win", 201.0)
    L += [I(win, 1700, 400, 1280, 720, t0=0.2),
          T("Today, tag a7: survive 3:00, the fog lifts, the result panel", 3020, 420, 52, w=640, t0=0.2,
            spacing=1.3)]
    a, b = cue("B09", "For this slice"), cue("B09", "You'll know it ran")
    boxes = ["Survive until the fog lifts", "Reach the Lantern Gate", "DELIVERED"]
    for i, t in enumerate(boxes):
        x = 1700 + i * 680
        L += [R(x, 1220, 560, 240, t0=a, outline=TERRA if i == 2 else BORDER, width=6 if i == 2 else 4),
              T(t, x + 40, 1270, 54, INK, "sans-medium", w=480, t0=a, spacing=1.25)]
        if i < 2:
            L.append(arrow(x + 575, 1265, a))
    L += [T("My answer to Q-01 for this slice (proposed)", 1700, 1490, 46, DIM, t0=a),
          R(180, 1340, 1420, 560, t0=b), R(1700, 1600, 1960, 300, t0=b),
          T("How anyone knows it ran", 230, 1380, 62, f="serif-medium", t0=b),
          T("a headless test with a fixed seed drives a run to DELIVERED; the result panel shows it in a capture",
            230, 1490, 50, w=1320, t0=b, spacing=1.3),
          T("tests/test_delivery.gd (planned)\nfixed seed → DELIVERED → result panel", 1750, 1650, 52, INK, "mono",
            w=1860, t0=b, spacing=1.4)]
    render("B09", L)


def b10():
    L = chrome("B10", "What could sink it", "COMPARISON · measured in Assignment 6, mitigation planned",
               "Readings: evidence/assignment-6/cost/COST-REPORT.md (29 October 2026, Apple M4, Godot 4.7.2, "
               "GL Compatibility). Mitigation: proposed.")
    L += excerpt_panel("B10", "Risks and Mitigations", h=1000, size=56)
    L += [T("Every turret hit can spawn A6's hit sparks, in the busiest minute of the run.", 180, 1460, 54,
            w=1420, t0=1.0, spacing=1.3)]
    a, b = cue("B10", "zero milliseconds"), cue("B10", "So I'll cap")
    L += [R(1700, 400, 1960, 800, t0=a),
          T("A6 cost report · measured", 1750, 440, 50, DIM, "sans-medium", t0=a),
          T("GPU time under GL Compatibility on my Mac:", 1750, 530, 54, t0=a, w=1860),
          T("0.000 ms on every frame: not readable", 1750, 610, 66, INK, "serif-medium", t0=a, w=1860),
          T("CPU cost of hit sparks at the cap (32 live bursts):", 1750, 790, 54, t0=a, w=1860),
          T("+0.025 ms per frame, budget 1.0 ms", 1750, 870, 66, INK, "serif-medium", t0=a, w=1860),
          T("measured without turrets; turrets are new load", 1750, 1030, 46, DIM, t0=a, w=1860),
          R(1700, 1240, 1960, 660, t0=b),
          T("What I will do", 1750, 1270, 60, f="serif-medium", t0=b),
          T("1  Cap the active turrets\n2  Reuse turret shots\n3  Measure CPU frame time at the peak wave, "
            "same method as cost_effects.gd\n4  GPU through the Vulkan proxy run\n5  Cut turret sparks first",
            1750, 1380, 50, w=1860, spacing=1.42, t0=b)]
    render("B10", L)


def b11():
    L = chrome("B11", "Why this project", "COMPARISON · Bao's answers, 23 November 2026",
               "New versus already had: Bao's answers on 23 November 2026. Evidence: tags a5, a6, a7 in "
               "this repository.")
    a, b, c = cue("B11", "New to me"), cue("B11", "I already had"), cue("B11", "new code")
    L += [T("Both: learning, and showing what I have.", 180, 410, 70, f="serif", t0=0.3),
          R(180, 560, 1660, 1100, t0=a), T("New to me in this course", 240, 610, 72, f="serif-medium", t0=a),
          T("Godot and GDScript\nShaders and materials (a5)\nParticle effects (a6)", 240, 780, 60, w=1540,
            spacing=1.6, t0=a),
          R(2000, 560, 1660, 1100, t0=b), T("Already had", 2060, 610, 72, f="serif-medium", t0=b),
          T("Animation\nState machines\nTesting", 2060, 780, 60, w=1540, spacing=1.6, t0=b),
          T("Evidence: tag a7, 23 headless runs from a fresh clone, 8 of 8 mutations caught", 2060, 1380, 48, DIM,
            w=1540, spacing=1.3, t0=b),
          R(180, 1720, 3480, 180, fill="#F2E5D8", outline=TERRA, width=6, t0=c),
          T("New code in this game: the delivery, the save and the turret.", 240, 1765, 60, t0=c)]
    render("B11", L)


def b12():
    L = chrome("B12", "Exists today, and what will exist", "COMPARISON · left exists, with tags; right is proposed",
               "Status words from the GDD's own status convention. Tags and commits: github.com/yanxlh/"
               "walker-lanternfall-bao-x. Full lists in pitch/PROJECT-BRIEF.md.")
    L += excerpt_panel("B12", "Status convention", w=1100, h=1500, size=46)
    exists = ["Survival run, cards, Sunflare · a7", "Generated art, sound, music · 8a6f988",
              "Blender gate, stack, shrine · a3", "GDD v0.3 · A4, 17 Oct", "Two hand-written shaders · a5",
              "Three particle effects, cost report · a6", "Walk and dash, 23 test runs · a7"]
    will = ["1  Delivery objective (first)", "2  Post office menu", "3  Engineer and turret", "4  One saved record",
            "5  Gate lit after a delivery", "6  Turret load measurement", "7  macOS export"]
    a, b = cue("B12", "Nothing on the right"), cue("B12", "December twentieth")
    L += [R(1360, 400, 1120, 1500, t0=0.3), T("Exists today", 1410, 440, 72, f="serif-medium", t0=0.3),
          T("\n".join(exists), 1410, 590, 48, w=1030, spacing=1.7, t0=0.3),
          R(2540, 400, 1120, 1500, t0=a), T("Will exist by a10", 2590, 440, 72, f="serif-medium", t0=a),
          T("\n".join(will), 2590, 590, 48, w=1030, spacing=1.7, t0=a),
          T("No export exists yet.", 2590, 1560, 52, INK, "sans-medium", t0=a),
          T("Due 20 December 2026 · tag a10", 2590, 1660, 52, INK, "sans-medium", t0=b)]
    render("B12", L)


def b13():
    stills = [(still("still-title", 1.0), "title screen"), (still("still-cards", 14.0), "card screen"),
              (still("still-win", 201.0), "3:00, the fog lifts")]
    L = [T("Lanternfall: First Delivery", 0, 300, 230, f="serif", w=3840, align="center", fade=0.4),
         R(1720, 640, 400, 12, fill=TERRA, outline=None, width=0, radius=4, t0=0.3),
         T("A pitch by Bao Xing", 0, 710, 90, f="serif-medium", w=3840, align="center", t0=0.4),
         T("github.com/yanxlh/walker-lanternfall-bao-x · pitch/ at tag a8", 0, 880, 58, w=3840, align="center",
           t0=0.6)]
    for i, (src, lab) in enumerate(stills):
        x = 220 + i * 1150
        L += [I(src, x, 1080, 1100, 619, t0=0.8), T(lab, x, 1720, 46, DIM, w=1100, align="center", t0=0.8)]
    L.append(T("Narration: an AI voice reading Bao's script · stills: real capture of tag a7, scripted input", 0, 1860,
               44, DIM, w=3840, align="center", t0=1.0))
    render("B13", L)


ALL = {"B00": b00, "B01": b01, "B02": b02, "B03": b03, "B04": b04, "B05": b05, "B06": b06, "B07": b07,
       "B08": b08, "B09": b09, "B10": b10, "B11": b11, "B12": b12, "B13": b13}

if __name__ == "__main__":
    for bid in sys.argv[1:] or ALL:
        ALL[bid]()
