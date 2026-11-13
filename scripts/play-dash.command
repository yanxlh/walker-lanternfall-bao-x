#!/bin/bash
# Assignment 7 playtest. Double-click, or run with "slow" for --time-scale 0.25:  scripts/play-dash.command slow
# Each run starts with the dash unlocked (godot/tests/play_dash.gd). Enter starts, Shift / Space dashes, R restarts.
cd "$(dirname "$0")/.."
G=/Applications/Godot.app/Contents/MacOS/Godot
[ -d godot/.godot/imported ] || "$G" --headless --path godot --import --quit
if [ "$1" = slow ]; then
  exec "$G" --path godot --time-scale 0.25 --script res://tests/play_dash.gd
fi
exec "$G" --path godot --script res://tests/play_dash.gd
