#!/usr/bin/env python3
"""Select Movie Maker fixture frames without deleting the full capture."""
from pathlib import Path
import re
import shutil
import sys

source = Path(sys.argv[1]).resolve()
frames = {}
for path in source.glob('frame*.png'):
    match = re.fullmatch(r'frame(\d+)\.png', path.name)
    if match:
        frames[int(match.group(1))] = path
wanted = [int(value) for value in sys.argv[2].split(",")] if len(sys.argv) > 2 else [10, 12, 15, 20, 30, 50]
missing = set(wanted) - frames.keys()
if missing:
    raise SystemExit(f'Missing frames: {sorted(missing)}. Check the Movie Maker output naming.')
strip = source / 'strip'
strip.mkdir(exist_ok=True)
for number in wanted:
    shutil.copy2(frames[number], strip / frames[number].name)
(strip / 'README.md').write_text(
    '# Particle fixture\n\n'
    'Real windowed Godot Movie Maker output at 30 fps. '
    'Trigger is requested during frame 10; inspect the actual first visible frame before making visual claims.\n\n'
    f'Selected frames: {wanted}. Fixed seed: 7280. '
    'Real market background and courier scale; no gameplay event is driven in this fixture.\n'
)
print(f'Strip saved to {strip}. Full sequence retained locally; commit only the strip.')
