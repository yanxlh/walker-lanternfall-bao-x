#!/usr/bin/env python3
"""Level the Kokoro narration and add the two planned silences.

Each beat's mp3 is loudness-normalised (EBU R128, -16 LUFS, true peak -1.5 dBTP) into mp3/beat-<BID>.wav, which
becomes the beat's audio_file. B00 gets its lead_silence_s in front and B13 its tail_silence_s after, and
actual_duration_s is re-measured from the wav. Writes audio-levels.json. Adapted from the Assignment 7 film's tool.

    ~/.venvs/general/bin/python tools/level_audio.py
"""
import json, re, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
TARGET = "loudnorm=I=-16:TP=-1.5:LRA=11"


def lufs(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-vn", "-af", "ebur128=peak=true:framelog=quiet",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
    return (float(i[-1]) if i else None, float(p[-1]) if p else None)


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(path)], capture_output=True, text=True).stdout.strip())


def main():
    sheet_p = REEL / "beat_sheet.json"
    sheet = json.loads(sheet_p.read_text())
    log = {"filter": TARGET, "beats": {}}
    for b in sheet["beats"]:
        bid = b["beat_id"]
        mp3 = REEL / f"mp3/beat-{bid}.mp3"
        wav = REEL / f"mp3/beat-{bid}.wav"
        lead, tail = float(b.get("lead_silence_s", 0)), float(b.get("tail_silence_s", 0))
        af = TARGET
        if lead:
            af += f",adelay={int(lead * 1000)}:all=1"
        if tail:
            af += f",apad=pad_dur={tail}"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-af", af, "-ar", "48000", "-ac", "2",
                        "-c:a", "pcm_s16le", str(wav)], check=True)
        d0, d1 = dur(mp3), dur(wav)
        if abs(d1 - (d0 + lead + tail)) > 0.06:
            raise SystemExit(f"{bid}: levelled narration length {d0:.3f} + {lead + tail} -> {d1:.3f}")
        b["audio_file"] = f"mp3/beat-{bid}.wav"
        b["audio_levelled"] = {"from": f"mp3/beat-{bid}.mp3", "filter": af}
        b["actual_duration_s"] = round(d1, 2)
        log["beats"][bid] = {"kokoro_s": round(d0, 2), "wav_s": round(d1, 2), "before": lufs(mp3), "after": lufs(wav)}
    sheet_p.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    (REEL / "audio-levels.json").write_text(json.dumps(log, indent=1) + "\n")
    after = [v["after"][0] for v in log["beats"].values()]
    total = sum(v["wav_s"] for v in log["beats"].values())
    print(f"{len(after)} beats, {min(after)} to {max(after)} LUFS, narration total {total:.1f}s")


if __name__ == "__main__":
    main()
