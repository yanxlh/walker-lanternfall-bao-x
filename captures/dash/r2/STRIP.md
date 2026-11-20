# Frame strip (fixture capture)

Movie Maker, 30 fps, `godot/previews/courier_preview.tscn` (fixtures in its header). Frame N is line N of `frames.log`.

| Frame | Tick | Dash frame | Phase | Label | Should show |
|---|---|---|---|---|---|
| 4 | 9 | - | - | before trigger | walking right, the sprite (cell 2 or 3) |
| 5 | 11 | 0 | startup | trigger | dash frame 0: the rig replaces the sprite, upright |
| 7 | 15 | 4 | active | active begins | the lean into the dash, lamp trailing |
| 12 | 25 | 14 | recovery | recovery begins | the end of the push, starting to settle |
| 15 | 31 | - | - | dash ends | back on the walk sprite |

What I see (Bao):

Claude's reading (a claim, not a check):

