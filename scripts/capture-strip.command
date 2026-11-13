#!/bin/bash
# Assignment 7 frame strips. Bao runs these (the assignment: "you run every capture").
#   scripts/capture-strip.command watch dash      play the preview in a window, no recording (look before Claude does)
#   scripts/capture-strip.command dash r1         record captures/dash/r1/ at 30 fps, keep the brief's frames
#   scripts/capture-strip.command walk r1         record captures/walk/r1/, keep two walk cycles
cd "$(dirname "$0")/.." || exit 1
G=/Applications/Godot.app/Contents/MacOS/Godot
[ -d godot/.godot/imported ] || "$G" --headless --path godot --import --quit
PY=python3; [ -x "$HOME/.venvs/general/bin/python" ] && PY="$HOME/.venvs/general/bin/python"
if [ "$1" = watch ]; then
  exec "$G" --path godot res://previews/courier_preview.tscn -- --clip "${2:-dash}" --out "$PWD/captures/${2:-dash}/watch"
fi
clip="${1:-dash}"; rev="${2:-r1}"; out="$PWD/captures/$clip/$rev"
if [ -e "$out" ]; then echo "$out exists; pick a new revision name" >&2; exit 1; fi
mkdir -p "$out"
"$G" --path godot --log-file "$PWD/logs/capture-strip-$clip-$rev.log" res://previews/courier_preview.tscn \
  --write-movie "$out/frame.png" --fixed-fps 30 --quit-after 90 -- --clip "$clip" --out "$out" || exit $?
"$PY" -I scripts/keep_strip_frames.py "$out" "$clip"
echo "Done: $out (STRIP.md has a line for what you see; write your verdict in TUNING.md before asking Claude)"
