#!/bin/bash
# Render Remotion beats through $ART/runtime/scripts/remotion_scenes.py, several queues at once without two writers on
# one reel: each beat renders in its own worker folder holding a copy of beat_sheet.json, then its media file is moved
# into the reel. A beat that fails (e.g. Remotion's 30 s per-frame timeout on an overloaded machine) is tried once
# more. Stamps are merged into the reel's beat sheet afterwards by tools/merge_remotion_stamps.py.
#   tools/remotion_workers.sh <worker-root> B00 B01 ...
ART=${ART:-/Users/yxlh/brutalist.art}
REEL="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$1"; shift
for b in "$@"; do
  [ -s "$REEL/media/$b.mp4" ] && { echo "$b exists, skipped"; continue; }
  for attempt in 1 2; do
    w="$ROOT/$b"; rm -rf "$w"; mkdir -p "$w"
    cp "$REEL/beat_sheet.json" "$w/beat_sheet.json"
    s=$(date +%s)
    (cd "$ART" && python3 runtime/scripts/remotion_scenes.py "$w" --only "$b") > "$w/render.log" 2>&1
    st=$?
    echo "$b attempt $attempt exit $st $(( $(date +%s) - s ))s"
    if [ $st -eq 0 ] && [ -s "$w/media/$b.mp4" ]; then mv "$w/media/$b.mp4" "$REEL/media/$b.mp4"; break; fi
  done
done
