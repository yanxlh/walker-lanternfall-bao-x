# Brief coverage checks — 9 November 2026

Godot 4.7.2, headless, fixed 60 fps. Run against a fresh imported copy of the current godot/ directory; source settings were not changed. Commands: Godot --headless --fixed-fps 60 --path <copied-godot> --script res://tests/<suite>.gd, with a separate log file for each suite.

| Suite | Assertions | Failures |
|---|---:|---:|
| test_defeat_sparks_config.gd | 40 | 0 |
| test_extra_particles_config.gd | 81 | 0 |
| test_particles_state.gd | 34 | 0 |
| test_particles_tree_pause.gd | 11 | 0 |

166 assertions, zero failures; all processes exited 0, with no SCRIPT ERROR or SHADER ERROR. Configuration coverage now includes A z_index=3, B z_index=1, and celebration z_index=3. Existing assertions are retained. The separate tree-pause test uses real start/movement input, sets SceneTree.paused, checks processing eligibility and unchanged player position/emission state, then verifies movement, trail processing, and stopping after resume. It does not render particles or measure their visible age.

This is a targeted rerun, not a new run of all regression suites. Earlier totals of 313 describe the earlier eight-suite run and are retained as historical results. Human visual checks and the r2 running-game verdict are not supplied by these tests.
