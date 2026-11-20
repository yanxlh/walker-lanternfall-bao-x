#!/usr/bin/env python3
"""Master QC: one frame at 50 % of every beat of the final export into _qc/master-sheet.png (31 tiles), the first
and last frame around every cut into _qc/master-cuts/, and per-beat loudness of the export's audio
(_qc/master-audio.json): integrated LUFS and true peak per beat, plus the longest silent gap inside narration beats.

    python3 tools/master_qc.py exports/landscape/<slug>.mp4
"""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
M = REEL / sys.argv[1]
sheet = json.loads((REEL / "beat_sheet.json").read_text())
OUT = REEL / "_qc"
(OUT / "master-cuts").mkdir(parents=True, exist_ok=True)
spans, t = [], 0.0
for b in sheet["beats"]:
    d = float(b.get("render_duration_s") or b.get("actual_duration_s"))
    spans.append((b["beat_id"], t, d, b.get("kind"), bool(b.get("narration_text"))))
    t += d


def grab(ts, path, w=640):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ts:.3f}", "-i", str(M), "-frames:v", "1", "-vf",
                    f"scale={w}:-1", str(path)], check=True)


tiles = []
for bid, t0, d, _k, _n in spans:
    p = OUT / "master-cuts" / f"{bid}-mid.png"
    grab(t0 + d * 0.5, p)
    tiles.append((bid, p))
    grab(t0 + 0.05, OUT / "master-cuts" / f"{bid}-first.png", 480)
    grab(max(t0, t0 + d - 0.07), OUT / "master-cuts" / f"{bid}-last.png", 480)
cols = 4
rows = (len(tiles) + cols - 1) // cols
S = Image.new("RGB", (cols * 640, rows * 380), (255, 255, 255))
f = ImageFont.load_default()
for i, (bid, p) in enumerate(tiles):
    im = Image.open(p)
    x, y = (i % cols) * 640, (i // cols) * 380
    S.paste(im, (x, y))
    ImageDraw.Draw(S).text((x + 6, y + 362), bid, fill=(200, 0, 120), font=f)
S.save(OUT / "master-sheet.png")
audio = {}
for bid, t0, d, kind, narr in spans:
    r = subprocess.run(["ffmpeg", "-nostats", "-ss", f"{t0:.3f}", "-t", f"{d:.3f}", "-i", str(M), "-vn", "-af",
                        "ebur128=peak=true:framelog=quiet,silencedetect=n=-45dB:d=1.2", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)
    pk = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
    sil = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", r)]
    audio[bid] = {"start_s": round(t0, 2), "dur_s": round(d, 2), "kind": kind or "", "lufs": float(i[-1]) if i else None,
                  "true_peak_dbfs": float(pk[-1]) if pk else None, "silences_over_1.2s": sil}
(OUT / "master-audio.json").write_text(json.dumps(audio, indent=1))
for k, v in audio.items():
    print(k, v["start_s"], v["lufs"], v["true_peak_dbfs"], v["silences_over_1.2s"])
