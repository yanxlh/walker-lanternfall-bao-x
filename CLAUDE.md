# Project context

- Game: Lanternfall, a 2D night-market survival game (`README.md`, `godot/game/session.gd`).
- Engine: Godot 4.7.2.stable.official.ed1daf0bf, confirmed with `/Applications/Godot.app/Contents/MacOS/Godot --version`; also recorded in `README.md`.
- Renderer: GL Compatibility (`godot/project.godot`, rendering section).
- Display: 640 x 360 viewport, 1280 x 720 window (`godot/project.godot`, display section).
- Entry scene: `res://game/main.tscn` (`godot/project.godot`).
- Effect A: CPUParticles2D weapon-hit sparks (`godot/effects/defeat_sparks.tscn`, approved revision in `CHANGE-BRIEF.md`).
- A event: `weapon_hit(pos: Vector2)` in `godot/game/session.gd`, emitted in `damage()` after the dead-enemy guard, for lethal and nonlethal hits.
- Effect B: CPUParticles2D courier movement trail (`godot/effects/lantern_trail.tscn`).
- Extra: level-up celebration from `Session.leveled_up` (`godot/effects/level_up_sparks.tscn`).
- Controller: `godot/effects/particle_presentation.gd`, attached in `Session._ready()`. It reads state and listens to signals.
- B condition: read player displacement and `state.current` from `godot/game/session.gd`; state names are in `godot/game/game_state.gd`.
- Effects belong to the existing main game scene; independent previews belong in `godot/previews/` (`CHANGE-BRIEF.md`).
- Player sprite and origin: `godot/features/player/player.gd`; market background: `godot/features/world/ground.gd`.
- Existing tests extend `godot/tests/harness.gd` and write JSON to `evidence/`.
- Import: `/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import --quit` (`walker-lanternfall.command` and installed executable).
- Logic test: `./scripts/run-test.sh test_logic.gd 60` (`godot/tests/test_logic.gd`, `scripts/run-test.sh`).
- Gameplay test: `./scripts/run-test.sh test_gameplay.gd 60` (`godot/tests/test_gameplay.gd`, `scripts/run-test.sh`).
- Audio test: `./scripts/run-test.sh test_audio.gd realtime` (`godot/tests/test_audio.gd` includes audio playback waits; `scripts/run-test.sh`).
- A configuration: `./scripts/run-test.sh test_defeat_sparks_config.gd 60`.
- Trail/upgrade configuration: `./scripts/run-test.sh test_extra_particles_config.gd 60`.
- Real-input state suite: `./scripts/run-test.sh test_particles_state.gd 60`.
- Edge-case suite (blocker, discontinuity, LOST/WON): `./scripts/run-test.sh test_particles_edges.gd 60`.
- A fixture capture: `bash scripts/capture-defeat-sparks.command rN` (windowed; refuses an existing revision folder).
- Windowed play checks: `/Applications/Godot.app/Contents/MacOS/Godot --path godot --fixed-fps 60 --script res://tests/capture_play_checks.gd -- --out captures/play-checks/<stamp>`.
- Test definitions: corresponding scripts under `godot/tests/`; wrapper: `scripts/run-test.sh`.
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

# Headless facts

- Headless checks use a dummy renderer and provide no particle images or GPU timing.
- A GPU particle effect's headless CPU number cannot measure its GPU process cost.
- Real fixture captures require a windowed (not headless) run; the student allowed starting them from the terminal. Visual verdicts still come from the student.
- The A fixture loads and requests two bursts at frames 10 and 13; this does not verify its appearance.
- Baseline results: logic 32, gameplay 65, audio 25, all zero failures (`evidence/assignment-6/baseline/`).
- A configuration test: `./scripts/run-test.sh test_defeat_sparks_config.gd 60`, 39 checks (`godot/tests/test_defeat_sparks_config.gd`, `evidence/defeat_sparks_config.json`).

# Unconfirmed

- This local course-repository snapshot has no `a5` tag or previous shader directory; do not claim an A5 baseline exists.
- The recorded game GitHub URL does not establish that this snapshot matches its latest revision.
- GPU timing: `RenderingServer.viewport_get_measured_render_time_gpu` reads 0 under GL Compatibility (and Mobile/Metal) on this Mac; only a Mobile/Vulkan override exposes it (`evidence/assignment-6/cost/COST-REPORT.md`). The editor's Visual Profiler itself has not been opened.
- Student verdicts recorded so far: portrait placement kept, trail visibility kept, A scale r1 kept (`TUNING.md`). Crowded-play judgments in `captures/play-checks/*/PLAY-CHECKS.md` are pending.
- Baseline counts and configuration results are valid only when recorded from actual runs.
