#!/bin/bash
# Assignment 8 pitch film take. Never touches the repository's godot/: it unpacks `git archive a7 godot` into
# capture/copy/, sets the copy's window to 1920 x 1080 so Movie Maker writes 1080p, adds pitch_driver.gd and
# pitch_main.tscn, imports once, records the take in a window, then repeats the same script headless (dry run) and
# compares the two logs.   Usage: capture-pitch-take.command [seed]   (default 11)
cd "$(dirname "$0")" || exit 1
REV=a7
SEED="${1:-11}"
REPO="$(git rev-parse --show-toplevel)"
G=/Applications/Godot.app/Contents/MacOS/Godot
rm -rf copy && mkdir -p copy
git -C "$REPO" archive "$REV" godot | tar -x -C copy || exit 1
cd copy/godot || exit 1
sed -i '' 's/^window\/size\/window_width_override=1280$/window\/size\/window_width_override=1920/; s/^window\/size\/window_height_override=720$/window\/size\/window_height_override=1080/' project.godot
grep -q "window_width_override=1920" project.godot || { echo "window override not set" >&2; exit 1; }
cp ../../pitch_driver.gd ../../pitch_main.tscn .
"$G" --headless --path . --import > ../../import.log 2>&1 || exit 1
OUT="$(cd ../.. && pwd)"
LF_CAPTURE_LOG="$OUT/take-pitch-seed$SEED-log.jsonl" "$G" --always-on-top --path . res://pitch_main.tscn --write-movie "$OUT/take-pitch-seed$SEED.avi" --fixed-fps 30 -- pitch "$SEED" || exit 1
LF_CAPTURE_LOG="$OUT/take-pitch-seed$SEED-dryrun.jsonl" "$G" --headless --path . res://pitch_main.tscn --fixed-fps 30 -- pitch "$SEED" > /dev/null 2>&1 || exit 1
cd "$OUT"
python3 -I - "$SEED" <<'PY'
import json, sys
s = sys.argv[1]
def rows(p):
    return [{k: v for k, v in json.loads(l).items() if k not in ("pf", "process_frame", "stale")} for l in open(p)]
a, b = rows(f"take-pitch-seed{s}-log.jsonl"), rows(f"take-pitch-seed{s}-dryrun.jsonl")
print("rows: take %d, dry run %d, identical: %s" % (len(a), len(b), a == b))
PY
shasum -a 256 "take-pitch-seed$SEED.avi" "take-pitch-seed$SEED-log.jsonl" > takes.sha256
echo "Done: $OUT/take-pitch-seed$SEED.avi"
