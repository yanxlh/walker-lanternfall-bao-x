# RIFF — the judgments the narration makes, and what each rests on

| Judgment | Rests on |
|---|---|
| "An animation isn't a movie, it's a list of keys" | the walk clip's text in `courier_clips.tres` (one value track, two keys) and the dash's three continuous tracks |
| The walk's cast frames are not a broken loop | `captures/walk/r1/frames.log` (`pose=cast` on frames 1–3) and Bao's own reflection in FRICTIONAL.md |
| The clip and gameplay read the same tick | `callback_mode_process = 2`, `_show()` seeking from tick counters, and the measured `two-clocks-at-<rate>` (0 s at 30/60/144) |
| "Not invincible" | `take_hit()` and the take's log (hp 10 → 8 → 6 → 4 across the three hits) |
| The read-back proves a track points at something real, not the right thing | the assignment's own caveat; `sub in node` is also true for a method |
| A Godot 3 `loop = true` still loops in 4.7.2 | `evidence/assignment-7/godot3-names/probe.json` (loop_mode 1 from script and from `.tres`) |
| The r2 outline can read detached on the coat's back | Claude's reading of Bao's r2 strip (TUNING.md), labelled a claim; Bao's verdict in play overrides it for the decision |
| What a headless run cannot show | TEST-REPORT.md (Assignment 7) |
