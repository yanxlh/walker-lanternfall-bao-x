I've read CLAUDE.md, the brief, `hurt_tint.gdshader`, `player.gd`, `session.gd`, `game_state.gd`, `harness.gd`, `run-test.sh` and `particle_presentation.gd`. Nothing has been edited.

**Your shader meets the spec.** It has `canvas_item` and `unshaded`, the two uniforms with the specified types, hints and defaults, and the exact `mix` line. It has no `TIME`, no `texture()` and no sampler uniforms. I see nothing to report.

## Step 1: give the courier the material and drive it

**New file `godot/effects/hurt_tint_presentation.gd`** (about 30 lines, a read-only `Node` built like `ParticlePresentation`):

```gdscript
extends Node
## Read-only presentation: the courier's yellow tint follows the remaining i-frames. Never changes gameplay state.
const Tuning = preload("res://features/tuning.gd")
const GS = preload("res://game/game_state.gd")
const HurtTint = preload("res://shaders/hurt_tint.gdshader")
var session
var material: ShaderMaterial

func setup(game) -> void:
	session = game
	process_priority = 200
	material = ShaderMaterial.new()          # one per session/player; the Shader is shared
	material.shader = HurtTint
	game.player.material = material
	game.state.changed.connect(func(_from, _to): refresh())
	refresh()

func _process(_d: float) -> void:
	refresh()

func amount() -> float:
	if session.state.current in [GS.PLAYING, GS.PAUSED, GS.LEVELUP]:
		return clampf(float(session.player.iframes) / Tuning.IFRAME_TICKS, 0.0, 1.0)
	return 0.0

func refresh() -> void:
	material.set_shader_parameter("hurt_amount", amount())
```

**Edit `godot/game/session.gd`:** add 4 lines to `_ready()` after the particles (`:89`): a preload const, then `new`, `add_child` and `setup(self)`. No gameplay path in `session.gd` changes, and `player.gd` is not touched.

How this meets each rule:
- **Sampling after the simulation:** `_process` runs after that frame's `_physics_process` ticks, so it reads the latest `iframes`.
- **Refresh on state change and restart:** `start_run()` calls `player.reset()` before `state.restart()`. The `changed` signal therefore writes 0 at once, inside the same call.
- **MENU, WON and LOST:** these force 0, including after a lethal hit that leaves `iframes == 48`.
- **PAUSED and LEVELUP:** the driver keeps running, but `iframes` is frozen, so the value holds.
- **Tree pause:** the driver inherits the pausable mode, so it stops and the value holds.
- **No fade timer:** there is no timer and no frame counting. `hurt_color` is never written, so it stays at your shader default and remains editable.

**Side effect to accept or reject:** the F3 debug collision arc is drawn by the player, so it will be tinted too.

## Step 2: new test `godot/tests/test_hurt_tint.gd`

It extends `harness.gd` and uses the same input idiom as `test_particles_state.gd`: `Input.parse_input_event` for keys and `test_mode = false`, so the session's real `_physics_process` runs. A `Sampler` node with `process_priority = 100000` and `PROCESS_MODE_ALWAYS` records one row per frame: `hurt_amount`, `iframes`, state, `tick_count`, scaled delta and real µs. The test connects to `player.damaged` only to note the tick of each accepted hit. All assertions use the frame period read from `delta`, so the same file works at 30, 60 and 144.

| Assertion | Spec rule covered |
|---|---|
| `uniform-names-types`: `get_shader_uniform_list()` holds exactly `hurt_amount` (type 3, hint 1, `"0.0,1.0,…"`) and `hurt_color` (type 20) | Uniform names and types |
| `no-sampler-uniforms`: no uniform of Object type | No sampler uniforms |
| `shader-parses`: the list is non-empty; `run-test.sh` also fails on any `SHADER ERROR` | Shader parses |
| `defaults-from-source`: regex over `Shader.code` gives `= 0.0` and `= vec4(1.0, 1.0, 0.0, 1.0)`; also `canvas_item`, `unshaded` and the exact mix line | Defaults, read as text because headless does not report them |
| `driver-uses-declared-names`: every name the driver writes is in the uniform list | Misspelled uniform |
| `sampler-runs-last`: its priority is above every other node's in the tree | Sampling order |
| `menu-zero`: before Enter, the parameter is exactly `0.0`, not null | MENU forces 0 |
| `hit-starts-window`: in a real wraith contact in a seeded world, every sample equals `clamp(iframes/48)`. The first post-hit sample has `iframes == 48 − (tick − hit_tick)`. At 60 and 144 the peak sample is 1.0. | 1 on an accepted hit, subject to sample position |
| `zero-after-48-ticks`: the first zero sample is 48 ticks after the hit, and the frames × delta are within one frame period of 0.8 s | Duration at 30, 60 and 144 fps |
| `ignored-hit-no-retrigger`: an enemy overlaps the courier mid-window, `hp` is unchanged, the curve keeps falling one step per tick and nothing resets to 1 | Retrigger rule |
| `paused-holds` and `paused-resumes`: real `P` mid-window, wait 30 frames, value and `iframes` unchanged, then `P` and the countdown continues from the held value | PAUSED holds |
| `levelup-holds` and `levelup-resumes`: a real pickup (gem at the courier, as existing tests do) gives LEVELUP mid-window, then real `1` resumes | LEVELUP holds |
| `restart-writes-zero`: real `R` mid-window; the `run_started` callback and the first sampled frame both read 0 | Restart writes 0 |
| `lethal-lost-zero`: fixture `hp = 1`, real contact gives LOST with `iframes == 48` and `hurt_amount == 0` | LOST forces 0 |
| `won-zero`: fixture `tick_count` near the end, contact a few ticks before, WON arrives mid-window, value 0 | WON forces 0 |
| `tree-pause-holds`: `paused = true` mid-window, wait, value holds, unpause, countdown continues | Tree pause |
| `time-scale-ticks`: `Engine.time_scale = 0.5`; still exactly 48 ticks; records ticks, scaled game time and real time; resets to 1.0 afterwards | Time scale (observations recorded, no claim made) |
| `distinct-materials`: two sessions, materials not identical, same Shader; setting one material leaves the other unchanged | Each player has its own material |

**Fixtures to disclose:** the test seeds the world in the way existing tests do: it spawns enemies at chosen positions and sets `hp = 1` and `tick_count` for the terminal cases. Hits always come from real contact through `take_hit()`. The test never calls `refresh()` or sets `hurt_amount`, except to check that the two materials are independent.

## Step 3: run everything with `run-test.sh`

`test_audio.gd realtime`, then the other nine suites at `60`, then `test_hurt_tint.gd` at `30`, `60` and `144`. I'll show the real output, including any `SHADER ERROR` lines. The plan adds no new assets, so no `--import` is needed, but I'll run it once anyway because of the new `.gd` and its `.uid`.

## What this cannot prove headless

A headless run draws nothing (0 `frame_post_draw`). The test proves the wiring and the value of the uniform over game time, nothing about pixels.

**Checks only you can do (Bao):**
- **Mutations:** remove a semicolon from `hurt_tint.gdshader` and rename a uniform; the test should exit 1; then restore with git.
- **Colour table:** captured lamp (20,16) and coat (16,24) pixels on the `idle` frame at 0, 0.5 and 1, in both the red and white blink phases, against the hand table.
- **Out-of-range value:** set 2.0 from code, read it back, look at it, then restore.
- **Playtest:** the yellow reads, the red blink is still visible at low tint, there's no yellow in LOST or WON, nothing stale after restart, and the empowered warm modulation looks right.

Approve step 1 and I'll implement it and show the diff.