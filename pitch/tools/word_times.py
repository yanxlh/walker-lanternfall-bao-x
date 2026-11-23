#!/usr/bin/env python3
"""Word start times of each beat's narration (faster-whisper base.en, word timestamps), so board reveals land on the
spoken words. Reads mp3/beat-<BID>.mp3 (no lead silence); writes word-times.json. Also prints each transcript, which
is the pronunciation check.

    ~/.venvs/general/bin/python tools/word_times.py
"""
import json, subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

REEL = Path(__file__).resolve().parents[1]
m = WhisperModel("base.en", device="cpu", compute_type="int8")
out = {}
for b in json.loads((REEL / "beat_sheet.json").read_text())["beats"]:
    bid = b["beat_id"]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(REEL / f"mp3/beat-{bid}.mp3"), "-ac", "1", "-ar", "16000",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    segs, _ = m.transcribe(np.frombuffer(raw, np.float32), beam_size=5, word_timestamps=True)
    words = [{"w": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for s in segs for w in s.words]
    out[bid] = words
    print(bid, " ".join(w["w"] for w in words))
(REEL / "word-times.json").write_text(json.dumps(out, indent=1) + "\n")
