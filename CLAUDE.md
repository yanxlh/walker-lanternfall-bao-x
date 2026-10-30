@AGENTS.md

# Project context

## Engine and renderer
- Godot 4.7 (`godot/project.godot:8`); the exact build is 4.7.2.stable.official.ed1daf0bf (`README.md:17`).
- Renderer: `gl_compatibility` for desktop and mobile (`godot/project.godot:26-27`).
  The 2D canvas uses nearest filtering (`godot/project.godot:28`). `rendering/viewport/hdr_2d`
  is not set (absent from `godot/project.godot`).

## Main scene
- `res://game/main.tscn` (`godot/project.godot:7`): one `Node2D` named Main with
  `res://game/session.gd` attached (`godot/game/main.tscn:3-6`).
- The session builds everything in code, with no child scenes: ground, actors, player,
  weapon fx, camera, audio, HUD and particles (`godot/game/session.gd:59-89`).

## The shaded object: the courier (player)
- It has no scene of its own. `session.gd` creates it with `PlayerScript.new()` and adds it
  as a child of Main (`godot/game/session.gd:7,65-67`).
- Script: `godot/features/player/player.gd`, a `Node2D` (`player.gd:1`).
- Drawn in `_draw()` with `draw_texture_rect_region` from the 32 px frames of
  `res://assets/art/pc_sheet.png` (`player.gd:106-110`, `godot/features/art.gd:4`).
  Without the sheet it draws a placeholder of rects and circles (`player.gd:111-112,117-129`).
- The existing hit blink sets `modulate` every tick: red `(1,0.45,0.45)` while flashing,
  warm `(1.25,1.12,0.85)` when empowered, white otherwise (`player.gd:74-75`).
- The player has no `material` today; nothing in `godot/` references `hurt_tint` (searched).

## Game state that drives the effect
- Run state: `godot/game/game_state.gd`, enum `MENU, PLAYING, LEVELUP, PAUSED, WON, LOST`
  (`game_state.gd:6`) with allowed transitions (`:8-15`) and `restart()` (`:28-34`).
  `session.gd` owns the instance as `state` (`session.gd:31`).
- The session runs `tick()` only in PLAYING (`session.gd:111-115,121-123`), and `tick()`
  calls `player.step()` (`:129`). Restart goes through `start_run()`, which calls
  `player.reset()` (`:91-109`, input `:375-376`).
- Invulnerability counter: `player.iframes` (`player.gd:23`). It is set to
  `Tuning.IFRAME_TICKS` on an accepted hit (`player.gd:94-98`), decremented in `step()`
  (`:68-69`) and cleared in `reset()` (`:44`).
- `IFRAME_TICKS = 48`, `TICK_HZ = 60` (`godot/features/tuning.gd:4,14`).
- A lethal hit sends LOST through `died` and `_on_player_died` (`player.gd:101-103`,
  `session.gd:79,366-368`).

## 3D object for the textured shader
- Scene: `godot/a3/lantern_gate_room.tscn`. The brief targets Floor/Mesh and StandIn/Mesh
  (`CHANGE-BRIEF.md:17,109`).
- Floor/Mesh: a `BoxMesh` 8 x 0.2 x 8 with `material_override = Material_floor`
  (`lantern_gate_room.tscn:15-16,63-66`). That is an inline `StandardMaterial3D`
  sub-resource, albedo `(0.08,0.10,0.18)`, roughness 0.85 (`:18-20`).
- StandIn/Mesh: a `CapsuleMesh` r 0.25, h 1.2 with `material_override = Material_standin`
  (`:25-27,112-114`). That is an inline `StandardMaterial3D`, orange albedo with emission (`:29-32`).
- Lights and camera to reuse: Moon, LanternLight, Camera3D, ShrineLight (`:44-57,94-98`).
  Props: `lantern_gate.tscn`, `supply_stack.glb`, `oil_shrine.glb` (`:3-6`).

## Tests, all through `scripts/run-test.sh`
Usage: `scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]`
(`scripts/run-test.sh:2`). The file must sit in `godot/tests/` (`:26`). A number adds
`--fixed-fps N` and `realtime` adds nothing (`:9-15`). The default timeout is 120 s (`:26`).
The log goes to `logs/<test>_<tag>.log` (`:24`). The exit code is 1 if the log contains
`SHADER ERROR` or `SCRIPT ERROR` (`:36`). The wrapper does not import assets, so after any
new asset run the import step first (`AGENTS.md:27`):
`/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import`.

The ten existing suites, in the modes of the A5 baseline (`evidence/assignment-5/baseline/RUN.txt:2-11`):
```bash
./scripts/run-test.sh test_logic.gd 60
./scripts/run-test.sh test_gameplay.gd 60
./scripts/run-test.sh test_audio.gd realtime
./scripts/run-test.sh test_defeat_sparks_config.gd 60
./scripts/run-test.sh test_extra_particles_config.gd 60
./scripts/run-test.sh test_particles_state.gd 60
./scripts/run-test.sh test_particles_edges.gd 60
./scripts/run-test.sh test_a3_assets.gd 60
./scripts/run-test.sh test_lantern_gate.gd 60
./scripts/run-test.sh test_a3_camera.gd 60
```
Every suite extends `res://tests/harness.gd` (a `SceneTree`). It writes
`evidence/<suite>.json` and quits with 1 on any failure or an unfinished `run()`
(`godot/tests/harness.gd:1,13-31`). The baseline was 332 checks with 0 failures on `70c77e9`
(`FRICTIONAL.md:404`). Rendered captures need a window, not run-test.sh (`AGENTS.md:33-35`).

# Current change
@CHANGE-BRIEF.md

# Ownership
Bao writes every file in `godot/shaders/` by hand: today `hurt_tint.gdshader`,
`particles_generated.gdshader` and their `.uid` files, plus the planned
`cobblestone_surface.gdshader`. An agent never edits, creates, renames or deletes a file
there. It may read them and reference them from materials, drivers and tests. If a shader
looks wrong, report it to Bao.

# Out of scope
- Game rules and simulation: `player.gd` (the brief forbids editing it, `CHANGE-BRIEF.md:23`),
  and the gameplay paths in `session.gd`, `game_state.gd` and `tuning.gd`: health, damage,
  i-frame length, collision, movement, knockback, progression, tick rate and the state machine.
  The tint driver only reads `state.current` and `player.iframes`.
- The existing red, white and warm `modulate` blink. It stays as it is and is not adjusted
  to compensate for the tint.
- Any presentation clock: no fade timer, no shader `TIME` and no frame counting.
  The game itself never changes `Engine.time_scale` and never pauses the SceneTree.
- Audio buses, SFX rules and music behaviour.
- The three A3 props: their GLBs, `lantern_gate.tscn`, material names, geometry and
  collisions. Also the Blender sources, and the build scripts AGENTS.md lists.
- Existing tests and their expectations. New checks go in new test files.
- `.import` files written by hand and invented UIDs (AGENTS.md:37-38).

# Unconfirmed
- Where the A5 3D materials go. `CHANGE-BRIEF.md:17` says the Floor and StandIn overrides in
  `lantern_gate_room.tscn` "may be replaced". `:109` says to assign them "in an independent
  A5 presentation scene". No such scene exists yet. Ask Bao before editing `lantern_gate_room.tscn`.
- The A5 assets do not exist yet: no cobblestone textures, no `cobblestone_surface.gdshader`,
  no `test_materials.gd` and no `normal_map_check.gd`. Where the "assignment's"
  `normal_map_check.gd` comes from is not stated (`CHANGE-BRIEF.md:138`).
- The brief says the `idle`/`hurt` frames use only the four palette colours, measured from the
  PNG (`CHANGE-BRIEF.md:16`). I did not re-measure `pc_sheet.png`.
- Which node runs the hurt-tint driver, and where, is not specified. The courier is created in
  code, so there is no player scene to attach a material in.
- What the 0.8 s follows under `Engine.time_scale = 0.5` in 4.7 is unmeasured (`CHANGE-BRIEF.md:54`).
- Whether the 30 and 144 fps runs behave like the 60 fps baseline under run-test.sh. The
  wrapper accepts any positive rate (`scripts/run-test.sh:11`), but only 60 and realtime appear
  in the baseline.
