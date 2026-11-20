#!/bin/bash
# Assignment 7 film take. Bao runs this (the assignment: the student runs every capture).
# It never touches the repository's godot/: it unpacks `git archive 5f09b7f godot` into capture/copy/, sets the
# copy's window to 3840 x 2160 so Movie Maker writes 4K, adds film_driver.gd and film_main.tscn, imports once,
# records the take in a window, then repeats the same script headless (dry run) and compares the two logs.
cd "$(dirname "$0")" || exit 1
REV=5f09b7f
REPO="$(git rev-parse --show-toplevel)"
G=/Applications/Godot.app/Contents/MacOS/Godot
rm -rf copy && mkdir -p copy
git -C "$REPO" archive "$REV" godot | tar -x -C copy || exit 1
cd copy/godot || exit 1
sed -i '' 's/^window\/size\/window_width_override=1280$/window\/size\/window_width_override=3840/; s/^window\/size\/window_height_override=720$/window\/size\/window_height_override=2160/' project.godot
grep -q "window_width_override=3840" project.godot || { echo "window override not set" >&2; exit 1; }
cp ../../film_driver.gd ../../film_main.tscn .
"$G" --headless --path . --import > ../../import.log 2>&1 || exit 1
OUT="$(cd ../.. && pwd)"
"$G" --always-on-top --path . res://film_main.tscn --write-movie "$OUT/take-dash.avi" --fixed-fps 30 -- "$OUT/take-dash-log.jsonl" || exit 1
"$G" --headless --path . res://film_main.tscn --fixed-fps 30 -- "$OUT/take-dash-dryrun.jsonl" > /dev/null 2>&1 || exit 1
cd "$OUT"
python3 -I - <<'PY'
import json
def strip(p):
    return [{k: v for k, v in json.loads(l).items() if k not in ("sx", "sy")} for l in open(p)]
a, b = strip("take-dash-log.jsonl"), strip("take-dash-dryrun.jsonl")
print("rows: take %d, dry run %d, identical apart from screen position: %s" % (len(a), len(b), a == b))
PY
shasum -a 256 take-dash.avi take-dash-log.jsonl > takes.sha256
echo "Done: $OUT/take-dash.avi"
