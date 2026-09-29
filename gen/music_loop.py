#!/usr/bin/env python3
"""Cut a bar-aligned segment and crossfade its tail into its head so the file loops seamlessly; write OGG Vorbis.

    python gen/music_loop.py SRC.wav DST.ogg --bars 8 [--skip-s 1.0] [--xfade-s 0.25]
    python gen/music_loop.py SRC.wav DST.ogg --match-frames REF.ogg   # stretch a layer to the base loop length

At the wrap the player goes out[L-1] -> out[0]. out[0] = seg[L] (the natural continuation of seg[L-1]) fading into seg[0],
so both sides of the seam are continuous.
"""
import argparse, json
from pathlib import Path
import librosa
import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--bars", type=int, default=8)
ap.add_argument("--beats-per-bar", type=int, default=4)
ap.add_argument("--skip-s", type=float, default=1.0)
ap.add_argument("--xfade-s", type=float, default=0.25)
ap.add_argument("--match-frames")
ap.add_argument("--sidecar", help="gen/log/<ID>/<run>.json to record this edit in")
a = ap.parse_args()
SR = 44100
y, _ = librosa.load(a.src, sr=SR, mono=True)
xf = int(a.xfade_s * SR)

if a.match_frames:
    L = sf.info(a.match_frames).frames
    rate = len(y) / (L + xf)
    y = librosa.effects.time_stretch(y, rate=rate)
    y = np.pad(y, (0, max(0, L + xf - len(y))))[: L + xf]
    start, bpm = 0, None
else:
    tempo, beats = librosa.beat.beat_track(y=y, sr=SR, units="samples")
    bpm = float(np.atleast_1d(tempo)[0])
    beats = beats[beats >= int(a.skip_s * SR)]
    n = a.bars * a.beats_per_bar
    if len(beats) <= n:
        raise SystemExit(f"only {len(beats)} beats after skip; use fewer bars")
    start, end = int(beats[0]), int(beats[n])
    L = end - start
    if start + L + xf > len(y):
        raise SystemExit("not enough audio after the loop end for the crossfade; use fewer bars")
seg = y[start: start + L + xf].copy()
out = seg[:L].copy()
t = np.linspace(0, np.pi / 2, xf)
out[:xf] = seg[:xf] * np.sin(t) + seg[L:L + xf] * np.cos(t)
out *= 10 ** (-3 / 20) / max(1e-9, np.abs(out).max())
Path(a.dst).parent.mkdir(parents=True, exist_ok=True)
sf.write(a.dst, out, SR, format="OGG", subtype="VORBIS")
result = {"tool": "gen/music_loop.py", "src": a.src, "dst": a.dst, "bpm": bpm, "bars": None if a.match_frames else a.bars,
          "skip_s": a.skip_s, "start_sample": int(start), "loop_frames": int(L), "seconds": round(L / SR, 3),
          "xfade_s": a.xfade_s, "match_frames": a.match_frames}
import sys; sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import log_processing
log_processing(a.sidecar, result)
print(json.dumps(result))
