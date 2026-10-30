I implemented all three steps and every suite passes. I haven't committed anything.

| Suite | Mode | Result |
|---|---|---|
| `test_audio.gd` | realtime | 25 checks, 0 failures |
| the nine other existing suites | 60 | 307 checks, 0 failures |
| **existing total** | | **332, 0 failures (same as the baseline)** |
| `test_hurt_tint.gd` | 30, 60, 144 | 28 checks, 0 failures at each rate |

No run printed a `SHADER ERROR` or `SCRIPT ERROR` line. Most runs end with `WARNING: N ObjectDB instances were leaked` and `ERROR: N resources still in use at exit`. Several existing suites (audio, gameplay, particles) print these too. They don't affect `run-test.sh`'s exit code.

The first run failed to parse with five `SCRIPT ERROR` lines from my own test code: a negative bit shift and reading `source_code` off a preloaded class. I fixed both in the test.

**One step I couldn't do:** the `--import` command needs your approval, and this session can't give it. The two new scripts load by path, so the tests run without `.uid` files, but none exist yet. Please run `/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import` so Godot generates them.

## Diff

`godot/game/session.gd`: the preload constant plus the three setup lines from the plan, nothing else.
```diff
@@ -15,6 +15,7 @@
 const ParticlePresentation = preload("res://effects/particle_presentation.gd")
+const HurtTintPresentation = preload("res://effects/hurt_tint_presentation.gd")
@@ -87,6 +88,9 @@ func _ready() -> void:
 	particles.setup(self)
+	var hurt_tint = HurtTintPresentation.new()
+	add_child(hurt_tint)
+	hurt_tint.setup(self)
```

New file `godot/effects/hurt_tint_presentation.gd`, exactly as in the plan:
```gdscript
extends Node
## Read-only presentation: the courier's yellow tint follows the remaining i-frames. Never changes gameplay state.

const Tuning = preload("res://features/tuning.gd")
const GS = preload("res://game/game_state.gd")
const HurtTint = preload("res://shaders/hurt_tint.gdshader")

var session: Node2D
var material: ShaderMaterial

func setup(game: Node2D) -> void:
	session = game
	process_priority = 200
	# One material per session and courier; the Shader resource is shared.
	material = ShaderMaterial.new()
	material.shader = HurtTint
	game.player.material = material
	game.state.changed.connect(func(_from: int, _to: int): refresh())
	refresh()

func _process(_delta: float) -> void:
	refresh()

func amount() -> float:
	if session.state.current in [GS.PLAYING, GS.PAUSED, GS.LEVELUP]:
		return clampf(float(session.player.iframes) / Tuning.IFRAME_TICKS, 0.0, 1.0)
	return 0.0

func refresh() -> void:
	material.set_shader_parameter("hurt_amount", amount())
```

New file `godot/tests/test_hurt_tint.gd` (375 lines). It has every assertion in the plan's table, plus four small ones: `player-has-own-tint-material`, `real-start-input`, `no-time-no-resample` and `accepted-hits-spaced-48`.
- **Sampler:** a node with priority 100000 that keeps running when the tree is paused. It records one row per frame.
- **Input:** real Enter, W, P, R and 1 keys through `Input.parse_input_event`.
- **Hits:** always real wraith contact through `take_hit()`.
- **Fixtures:** they only place things. Wraiths get 1000 hp so the automatic beam can't kill them and drop gems. There's also a gem at the courier, `hp = 1` for the lethal run, and a `tick_count` 10 ticks before the end of the run for the win.
- **No direct driver calls:** the test never calls `refresh()` and never writes the courier's `hurt_amount`. The only write is on a second session's material, to show the two materials are independent.

Nothing in `godot/shaders/`, `player.gd` or the existing tests changed. The ten existing evidence JSONs were rewritten by the runs, and all but `gameplay.json` changed only their timestamp. `gameplay.json` also changed two camera values, but it is identical to `evidence/assignment-5/baseline/gameplay.json` apart from the timestamp. The committed copy dates from 14 October.

## Three test fixes made while running
1. **Tree pause:** the first run failed `tree-pause-resumes`. The test sets `paused = true` after that frame's physics tick but before its `_process`, so the counter reads 30 while the material keeps the driver's last value, 31/48. That matches the spec ("holds its last value"), and the held value is now asserted to equal it. The lag is 1 tick at 60 and 144, and 2 at 30. The game itself never pauses the tree.
2. **Time scale:** the time-scale check first passed with an empty result. It read the rows one frame too early, so it compared nothing. I fixed the read and the check now fails if the rows are missing.
3. **Duration tolerance at 144:** the tolerance came from a 1/120 s menu frame. It now uses the largest frame delta inside the hit window (0.00806 s at 144). That is still a little looser than 1/144 s (0.00694 s). The measured error was 0.0008 s.

## What the test proves (headless, at 30, 60 and 144)
- **The shader contract:**
  - Exactly two uniforms: `hurt_amount` is a float with range hint 0 to 1, and `hurt_color` is a Color. There are no samplers, and the uniform list is not empty.
  - Read from the source text: the defaults `0.0` and `vec4(1.0, 1.0, 0.0, 1.0)`, `canvas_item`, `unshaded` and the exact mix line. The source has no `TIME` and no `texture(`.
  - The driver writes only declared names.
- **Order:** the sampler's priority is above every other node's (highest other: 200, the driver).
- **The value curve over game time:**
  - On every sampled frame, `hurt_amount` equals iframes / 48, and iframes count down one per tick from the accepted hit.
  - The first sample is 1.0 at 60 and 144, and 47/48 at 30 (the hit lands on the first of two ticks in that frame).
  - It reaches 0 at hit + 48 ticks. The game time from hit to zero is 0.800 s at 60, 0.7958 s at 30 and 0.7992 s at 144.
- **Ignored hits:** during the window the wraith touches the courier on 11, 20 and 48 sampled frames at the three rates. There is no second hit, hp stays the same, and the curve never rises.
- **Holds and resumes:** real P (PAUSED) and a real pickup (LEVELUP) hold the value, the counter and the blink `modulate` for 30 frames. Resuming continues on the same tick curve. A tree pause holds too, with the driver stopped (`can_process()` false).
- **Next hit:** it lands only once protection has ended (gap of exactly 48 ticks) and starts a fresh window.
- **Terminal states and restart:**
  - LOST after a real lethal contact shows 0, with `iframes == 48`.
  - WON mid-window shows 0, with `iframes == 39`.
  - MENU shows exactly 0.0, not null.
  - Real R mid-window reads 0.0 inside `run_started` and again on the first sampled frame.
- **Materials:** two sessions get different materials that share one Shader, and writing one leaves the other unchanged.
- **Time scale 0.5, recorded (holds only under `--fixed-fps`):** 48 ticks still took 48 frames at 60 (24 at 30, 115 at 144). Scaled game time was 0.4 s and unscaled frame time 0.8 s. So under `--fixed-fps` the 0.8 s follows frame time, not scaled game time. A realtime run might behave differently, and wall-clock time (about 2 ms) means nothing in a headless run.

## What it cannot prove
A headless run draws nothing. Nothing here shows a colour, a pixel, readability, or whether the tint looks right next to the red, white and warm blink.

The mutation checks are yours, since I can't touch the shader. Removing a semicolon should exit 1 through `SHADER ERROR`. Renaming `hurt_amount` should fail `uniform-names-types` and `driver-uses-declared-names`. Restore with git afterwards.

## Checks only you can do
- The colour table: lamp (20,16) and coat (16,24) on the `idle` frame, at 0, 0.5 and 1, with red and white modulation captured separately.
- Set 2.0 from code, read it back, look at it, then restore.
- A playtest with several hits:
  - the yellow reads clearly;
  - the red blink is still visible at low tint;
  - there's no yellow in LOST or WON;
  - nothing stale shows after restart;
  - the empowered warm tint looks right.
- The known limitation you accepted: the F3 collision arc is tinted too.