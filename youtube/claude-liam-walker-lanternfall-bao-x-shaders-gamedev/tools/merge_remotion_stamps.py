#!/usr/bin/env python3
"""Copy the provenance stamps (shot.remotion.rendered) written by remotion_scenes.py in each worker folder into the
reel's beat_sheet.json, for beats whose media file was moved into the reel by tools/remotion_workers.sh.

    python3 tools/merge_remotion_stamps.py <worker-root>
"""
import json, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
root = Path(sys.argv[1])
sheet_p = REEL / "beat_sheet.json"
sheet = json.loads(sheet_p.read_text())
beats = {b["beat_id"]: b for b in sheet["beats"]}
merged = []
for w in sorted(p for p in root.iterdir() if p.is_dir()):
    bid = w.name
    ws = w / "beat_sheet.json"
    if bid not in beats or not ws.exists() or not (REEL / "media" / f"{bid}.mp4").exists():
        continue
    wb = next((b for b in json.loads(ws.read_text())["beats"] if b["beat_id"] == bid), None)
    stamp = ((wb or {}).get("shot", {}).get("remotion") or {}).get("rendered")
    if stamp:
        beats[bid]["shot"]["remotion"]["rendered"] = stamp
        merged.append(bid)
sheet_p.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
print("stamps merged:", " ".join(merged))
