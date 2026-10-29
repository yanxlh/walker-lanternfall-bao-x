# Project context

- Game: Lanternfall, a 2D night-market survival game (`README.md`, `godot/game/session.gd`).
- Engine: Godot 4.7.2.stable.official.ed1daf0bf, confirmed with `/Applications/Godot.app/Contents/MacOS/Godot --version`; also recorded in `README.md`.
- Renderer: GL Compatibility (`godot/project.godot`, rendering section).
- Display: 640 x 360 viewport, 1280 x 720 window (`godot/project.godot`, display section).
- Entry scene: `res://game/main.tscn` (`godot/project.godot`).
- Effect A: proposed CPUParticles2D enemy-defeat sparks (`CHANGE-BRIEF.md`).
- A event: `enemy_killed(pos: Vector2)` in `godot/game/session.gd`, emitted in `damage()` before the enemy is freed.
- Effect B: proposed CPUParticles2D courier movement trail (`CHANGE-BRIEF.md`).
- B condition: read player displacement and `state.current` from `godot/game/session.gd`; state names are in `godot/game/game_state.gd`.
- Effects belong to the existing main game scene; independent previews belong in `godot/previews/` (`CHANGE-BRIEF.md`).
- Player sprite and origin: `godot/features/player/player.gd`; market background: `godot/features/world/ground.gd`.
- Existing tests extend `godot/tests/harness.gd` and write JSON to `evidence/`.
- Import: `/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import --quit` (`walker-lanternfall.command` and installed executable).
- Logic test: `./scripts/run-test.sh test_logic.gd 60` (`godot/tests/test_logic.gd`, `scripts/run-test.sh`).
- Gameplay test: `./scripts/run-test.sh test_gameplay.gd 60` (`godot/tests/test_gameplay.gd`, `scripts/run-test.sh`).
- Audio test: `./scripts/run-test.sh test_audio.gd realtime` (`godot/tests/test_audio.gd` includes audio playback waits; `scripts/run-test.sh`).
- New configuration tests use 60; audio-dependent tests use realtime (`scripts/run-test.sh`, assignment instructions).
- Wrapper logs are under `logs/`; optional argument 3 sets timeout seconds (`scripts/run-test.sh`).

# Current change

@CHANGE-BRIEF.md

# Ownership

- Effect settings live in scene files in `godot/effects/`, not in code.
- Existing Assignment 5 shaders in `godot/shaders/` must remain hand-written and unchanged by an agent.
- The editor-generated process shader is a separate study artifact; it is not used by gameplay.
- Human observations, tuning acceptance decisions, and shader explanations must come from the student.
- Keep earlier submission documents and test expectations intact; add separately identified current evidence.

# Godot 4 names

Use Godot 4 class and property names for 4.7.2 only. Never guess a property from a Godot 3 example.
CPUParticles2D uses `scale_amount_min`, `scale_amount_max`, and `scale_amount_curve`, confirmed by runtime property inspection.
GPUParticles2D process settings belong to ParticleProcessMaterial; its names are not interchangeable with CPU node names.
Say what is unconfirmed instead of claiming a setting exists.

# Out of scope

Do not change collision, movement, input, game-state logic, timing, progression, existing assertions, or source textures.
Presentation code may read game state but must not write it.
Do not add planned GDD systems such as contracts, a hub, persistent upgrades, or additional couriers.
Do not publish, push, create submission tags, or overwrite earlier reports as part of an implementation step.

# Unconfirmed

- This local course-repository snapshot has no `a5` tag or previous shader directory; do not claim an A5 baseline exists.
- The recorded game GitHub URL does not establish that this snapshot matches its latest revision.
- Visual Profiler GPU timing support on this renderer and machine is not yet checked.
- No human playtest or tuning verdict has been collected for the new effects.
- Baseline counts and configuration results are valid only when recorded from actual runs.
