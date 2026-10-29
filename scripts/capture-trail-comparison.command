#!/usr/bin/env bash
# Run this from Finder to capture both preserved-original and accepted-ramp fixtures.
set -e
cd "$(dirname "$0")/.."
godot_bin="${GODOT_BIN:-/Applications/Godot.app/Contents/MacOS/Godot}"
comparison_dir="$PWD/captures/lantern_trail/comparison-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$comparison_dir" logs
"$godot_bin" --headless --path godot --log-file "$PWD/logs/trail-capture-import.log" --import --quit
for revision in r0 r1; do
  mkdir -p "$comparison_dir/$revision"
  baseline_args=()
  if [ "$revision" = r0 ]; then baseline_args=(-- --baseline); fi
  "$godot_bin" --path godot --log-file "$PWD/logs/trail-capture-${revision}.log" res://previews/lantern_trail_preview.tscn --write-movie "$comparison_dir/$revision/frame.png" --fixed-fps 30 --quit-after 75 "${baseline_args[@]}"
  python3 scripts/select_strip_frames.py "$comparison_dir/$revision" 10,12,20,39,40,45,51,60
done
printf '\nSaved comparison to: %s\n' "$comparison_dir"
printf 'Both are deterministic preview fixtures, not gameplay recordings.\n'
