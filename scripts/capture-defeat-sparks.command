#!/usr/bin/env bash
# The student runs this windowed capture; it does not substitute for a playtest.
cd "$(dirname "$0")/.." || exit 1
godot_bin="${GODOT_BIN:-/Applications/Godot.app/Contents/MacOS/Godot}"
revision="${1:-r0}"
if [[ ! "$revision" =~ ^r[0-9]+$ ]]; then echo 'Use a revision such as r0 or r1'; exit 2; fi
capture_dir="$PWD/captures/defeat_sparks/$revision"
if [ -d "$capture_dir" ]; then
  echo "Capture directory already exists: $capture_dir. Choose a new revision to preserve evidence."
  exit 1
fi
mkdir -p "$capture_dir" logs
"$godot_bin" --headless --path godot --log-file "$PWD/logs/capture-import.log" --import --quit || exit $?
"$godot_bin" --path godot --log-file "$PWD/logs/capture-defeat-sparks-${revision}.log" res://previews/defeat_sparks_preview.tscn --write-movie "$capture_dir/frame.png" --fixed-fps 30 --quit-after 60 || exit $?
python3 scripts/select_strip_frames.py "$capture_dir"
printf '\nCapture saved to %s\n' "$capture_dir"
