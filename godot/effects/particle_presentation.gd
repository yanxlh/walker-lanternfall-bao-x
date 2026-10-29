extends Node2D
## Read-only presentation: signals in, particles out. Never changes gameplay state.

const HitScene = preload("res://effects/defeat_sparks.tscn")
const LevelScene = preload("res://effects/level_up_sparks.tscn")
const TrailScene = preload("res://effects/lantern_trail.tscn")
const LevelOverlayScene = preload("res://effects/level_up_overlay.tscn")
const GS = preload("res://game/game_state.gd")
const MAX_HIT_BURSTS := 32
const MAX_LEVEL_BURSTS := 4

var session: Node2D
var trail: CPUParticles2D
var level_overlay: CanvasLayer
var hit_bursts: Array[CPUParticles2D] = []
var level_bursts: Array[CPUParticles2D] = []
var hits_seen := 0
var hits_spawned := 0
var levels_seen := 0
var levels_spawned := 0
var previous_position := Vector2.ZERO
var have_position := false

func setup(game: Node2D) -> void:
	session = game
	process_physics_priority = 10
	process_priority = 100
	level_overlay = LevelOverlayScene.instantiate() as CanvasLayer
	add_child(level_overlay)
	_sync_overlay()
	trail = TrailScene.instantiate() as CPUParticles2D
	add_child(trail)
	game.weapon_hit.connect(_on_weapon_hit)
	game.leveled_up.connect(_on_leveled_up)
	game.run_started.connect(_on_run_started)
	game.state.changed.connect(_on_state_changed)
	_reset_position()
	_apply_policy()

func _reset_position() -> void:
	if is_instance_valid(session) and is_instance_valid(session.player):
		previous_position = session.player.global_position
		have_position = true
		if is_instance_valid(trail):
			trail.global_position = previous_position + Vector2(0, 7)

func _on_weapon_hit(at: Vector2) -> void:
	hits_seen += 1
	if session.state.current != GS.PLAYING or hit_bursts.size() >= MAX_HIT_BURSTS:
		return
	var burst := HitScene.instantiate() as CPUParticles2D
	add_child(burst)
	burst.global_position = session.to_global(at)
	hit_bursts.append(burst)
	burst.finished.connect(_on_hit_finished.bind(burst))
	burst.restart()
	hits_spawned += 1

func _on_leveled_up(_level: int) -> void:
	levels_seen += 1
	if session.state.current != GS.PLAYING or level_bursts.size() >= MAX_LEVEL_BURSTS:
		return
	var burst := LevelScene.instantiate() as CPUParticles2D
	_sync_overlay()
	level_overlay.add_child(burst)
	burst.position = session.hud.levelup_particle_anchor()
	level_bursts.append(burst)
	burst.finished.connect(_on_level_finished.bind(burst))
	burst.restart()
	levels_spawned += 1

func _on_hit_finished(burst: CPUParticles2D) -> void:
	hit_bursts.erase(burst)
	burst.queue_free()

func _on_level_finished(burst: CPUParticles2D) -> void:
	level_bursts.erase(burst)
	burst.queue_free()

func _clear_bursts() -> void:
	for burst in hit_bursts:
		burst.free()
	for burst in level_bursts:
		burst.free()
	hit_bursts.clear()
	level_bursts.clear()

func _on_run_started() -> void:
	_clear_bursts()
	hits_seen = 0
	hits_spawned = 0
	levels_seen = 0
	levels_spawned = 0
	trail.restart()
	trail.emitting = false
	_reset_position()
	_apply_policy()

func _on_state_changed(_from: int, to: int) -> void:
	if to in [GS.MENU, GS.WON, GS.LOST]:
		_clear_bursts()
		trail.restart()
		trail.emitting = false
	_reset_position()
	_apply_policy()

func _apply_policy() -> void:
	if not is_instance_valid(session) or not is_instance_valid(trail):
		return
	level_overlay.visible = is_visible_in_tree()
	var playing: bool = session.state.current == GS.PLAYING
	for burst in hit_bursts:
		burst.speed_scale = 1.0 if playing else 0.0
	for burst in level_bursts:
		# The upgrade screen intentionally allows its celebration to finish.
		burst.speed_scale = 1.0 if session.state.current in [GS.PLAYING, GS.LEVELUP] else 0.0
	trail.speed_scale = 1.0 if playing else 0.0
	if not playing or not trail.is_visible_in_tree():
		trail.emitting = false

func _physics_process(delta: float) -> void:
	if not is_instance_valid(session) or not is_instance_valid(trail):
		return
	_apply_policy()
	var current: Vector2 = session.player.global_position
	var distance: float = current.distance_to(previous_position) if have_position else 0.0
	var teleport_limit: float = session.player.speed * delta * 2.0 + 4.0
	trail.global_position = current + Vector2(0, 7)
	trail.emitting = session.state.current == GS.PLAYING and trail.is_visible_in_tree() and distance > 0.01 and distance <= teleport_limit
	previous_position = current
	have_position = true

func _sync_overlay() -> void:
	if is_instance_valid(session) and is_instance_valid(level_overlay):
		# Celebration belongs to the upgrade portrait, independent of world camera motion.
		level_overlay.transform = session.hud.transform

func _process(_delta: float) -> void:
	_sync_overlay()
