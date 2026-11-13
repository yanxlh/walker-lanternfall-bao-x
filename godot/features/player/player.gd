extends Node2D
## The Lamp-Head Courier. Movement, facing, i-frames and pose selection; the session calls step() once per tick.
## The courier is drawn by courier_visual.tscn (a Sprite2D on the sheet, a cutout rig, one AnimationPlayer in
## manual mode). This script is the only code that plays or seeks that player (CHANGE-BRIEF.md, Assignment 7).

const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")
const VisualScene = preload("res://features/player/courier_visual.tscn")

signal damaged(hp: int)
signal died
signal dash_phase_changed(from: String, to: String)

## Frame order in pc_sheet.png (10 x 32 px). CHARACTER-SHEET R2 reduced 12 -> 10 poses.
const POSES := ["turn_front", "idle", "walk_contact", "walk_passing",
	"cast", "hurt", "levelup", "sunflare", "defeat", "victory"]
const FRAME := 32
## Frame pixel that sits on the node origin, i.e. the centre of the r = 10 hurtbox.
const SPRITE_ORIGIN := Vector2(16, 23)
const WALK_FRAME_TICKS := 8
## Visual states, highest priority first: the first one whose condition holds is shown.
const STATES := ["override", "dash", "hurt", "cast", "walk", "idle"]
## Legal dash phase changes; "" is no dash. A hit cancels startup (no cooldown) and recovery (cooldown starts).
const DASH_TRANSITIONS := {"": ["startup"], "startup": ["active", ""], "active": ["recovery"], "recovery": [""]}

var sheet: Texture2D
var visual: Node2D
var anim: AnimationPlayer
var hp: int = Tuning.PLAYER_MAX_HP
var max_hp: int = Tuning.PLAYER_MAX_HP
var speed: float = Tuning.PLAYER_SPEED
var facing := 1
var iframes := 0
var knock := Vector2.ZERO
var input_axis := Vector2.ZERO
var pose := "idle"
var override_pose := ""
var walk_ticks := 0
var cast_ticks := 0
var empowered := false
var show_collision := false
var dash_unlocked := false
## "", "startup", "active" or "recovery".
var dash_phase := ""
## Ticks since the dash started: the dash clip's time, and the phase.
var dash_ticks := 0
var dash_dir := Vector2.ZERO
var dash_cooldown := 0
## Set by request_dash() between ticks, consumed by the next step().
var dash_requested := false
## Anything with push_out(position, radius) -> Vector2 (the market ground); null = open field.
var blocker

func _ready() -> void:
	z_index = 2
	sheet = Art.texture(Art.PC_SHEET)
	visual = VisualScene.instantiate()
	# The visual draws under the courier's own _draw(), which keeps only the collision circle and the placeholder.
	visual.show_behind_parent = true
	add_child(visual)
	anim = visual.get_node("AnimationPlayer")
	_show()

func reset() -> void:
	hp = Tuning.PLAYER_MAX_HP
	max_hp = Tuning.PLAYER_MAX_HP
	speed = Tuning.PLAYER_SPEED
	facing = 1
	iframes = 0
	knock = Vector2.ZERO
	input_axis = Vector2.ZERO
	override_pose = ""
	walk_ticks = 0
	cast_ticks = 0
	empowered = false
	dash_unlocked = false
	dash_phase = ""
	dash_ticks = 0
	dash_dir = Vector2.ZERO
	dash_cooldown = 0
	dash_requested = false
	position = Vector2.ZERO
	sheet = Art.texture(Art.PC_SHEET)
	pose = "idle"
	_show()
	queue_redraw()

func step() -> void:
	var axis := input_axis.limit_length(1.0)
	_step_dash(axis)
	var move := axis * speed
	match dash_phase:
		"startup", "recovery":
			move = Vector2.ZERO
		"active":
			move = dash_dir * Tuning.DASH_SPEED
	position += (move + knock) / Tuning.TICK_HZ
	knock = knock.move_toward(Vector2.ZERO, Tuning.KNOCKBACK_DECAY / Tuning.TICK_HZ)
	if blocker:
		position = blocker.push_out(position, Tuning.PLAYER_RADIUS)
	var margin := Vector2(16, 16)
	position = position.clamp(Tuning.ARENA.position + margin, Tuning.ARENA.end - margin)
	if dash_phase == "":
		_face(axis)
	if iframes > 0:
		iframes -= 1
	if cast_ticks > 0:
		cast_ticks -= 1
	walk_ticks = walk_ticks + 1 if axis.length() > 0.1 and dash_phase == "" else 0
	pose = choose_pose()
	var flashing := iframes > 0 and (iframes / 4) % 2 == 0
	modulate = Color(1, 0.45, 0.45) if flashing else (Color(1.25, 1.12, 0.85) if empowered else Color.WHITE)
	_show()
	queue_redraw()

func _face(axis: Vector2) -> void:
	if axis.x > Tuning.FACING_DEADZONE:
		facing = 1
	elif axis.x < -Tuning.FACING_DEADZONE:
		facing = -1

## True when a press now would start a dash on the next tick.
func can_dash() -> bool:
	return dash_unlocked and dash_phase == "" and dash_cooldown == 0 and hp > 0

## A press between ticks. Dropped, not queued, while the dash is locked, running or cooling down.
func request_dash() -> bool:
	dash_requested = can_dash()
	return dash_requested

## Advances a running dash or its cooldown by one tick, then starts a requested dash. The tick a dash starts is
## startup frame 0, so it moves nothing.
func _step_dash(axis: Vector2) -> void:
	if dash_phase != "":
		dash_ticks += 1
		var next := _phase_at(dash_ticks)
		if next == "":
			_end_dash()
		elif next != dash_phase:
			_set_dash_phase(next)
	elif dash_cooldown > 0:
		dash_cooldown -= 1
	if dash_requested:
		dash_requested = false
		if can_dash():
			dash_dir = axis.normalized() if axis.length() > 0.1 else Vector2(facing, 0)
			_face(dash_dir)
			dash_ticks = 0
			_set_dash_phase("startup")

func _phase_at(t: int) -> String:
	if t < Tuning.DASH_STARTUP_TICKS:
		return "startup"
	if t < Tuning.DASH_STARTUP_TICKS + Tuning.DASH_ACTIVE_TICKS:
		return "active"
	if t < Tuning.DASH_STARTUP_TICKS + Tuning.DASH_ACTIVE_TICKS + Tuning.DASH_RECOVERY_TICKS:
		return "recovery"
	return ""

## Ends the dash and starts the cooldown, whether recovery completed or a hit cut it short.
func _end_dash() -> void:
	_set_dash_phase("")
	dash_ticks = 0
	dash_cooldown = Tuning.DASH_COOLDOWN_TICKS

func _set_dash_phase(next: String) -> void:
	if not DASH_TRANSITIONS[dash_phase].has(next):
		push_error("illegal dash transition %s -> %s" % [dash_phase, next])
		return
	var from := dash_phase
	dash_phase = next
	dash_phase_changed.emit(from, next)

## The visual state: the first entry of STATES whose condition holds.
func current_state() -> String:
	if override_pose != "":
		return "override"
	if dash_phase != "":
		return "dash"
	if iframes > Tuning.IFRAME_TICKS - Tuning.HURT_POSE_TICKS:
		return "hurt"
	if cast_ticks > 0:
		return "cast"
	if walk_ticks > 0:
		return "walk"
	return "idle"

func choose_pose() -> String:
	match current_state():
		"override":
			return override_pose
		"walk":
			return "walk_contact" if (walk_ticks / WALK_FRAME_TICKS) % 2 == 0 else "walk_passing"
		var s:
			return s

## The clip a state plays and the time to show, from integer tick counters (the brief's state table).
func clip_and_time() -> Array:
	match current_state():
		"override":
			return [override_pose, 0.0]
		"walk":
			return ["walk", (walk_ticks % (2 * WALK_FRAME_TICKS)) / float(Tuning.TICK_HZ)]
		"dash":
			return ["dash", dash_ticks / float(Tuning.TICK_HZ)]
		var s:
			return [s, 0.0]

## The only place that drives the AnimationPlayer. It runs in manual mode, so the clip moves only when the
## simulation ticks or an override is set; a frozen run freezes the courier.
func _show() -> void:
	if anim == null:
		return
	visual.visible = sheet != null
	visual.scale.x = facing
	var shown := clip_and_time()
	anim.play(shown[0])
	anim.seek(shown[1], true)

func set_override(p: String) -> void:
	override_pose = p
	pose = choose_pose()
	_show()
	queue_redraw()

func take_hit(from: Vector2, dmg: int) -> bool:
	if iframes > 0 or hp <= 0:
		return false
	hp = maxi(0, hp - dmg)
	iframes = Tuning.IFRAME_TICKS
	var away := position - from
	knock = (away.normalized() if away.length() > 0.01 else Vector2(-facing, 0)) * Tuning.KNOCKBACK
	# Not invincible: the hit lands in every phase. It cancels startup (no dash happened, so no cooldown) and the
	# rest of recovery (the cooldown starts); an active dash carries on.
	match dash_phase:
		"startup":
			_set_dash_phase("")
			dash_ticks = 0
		"recovery":
			_end_dash()
	damaged.emit(hp)
	if hp == 0:
		died.emit()
	return true

## The sheet is drawn by the visual; without it the placeholder is drawn here. The collision circle stays on top.
func _draw() -> void:
	if sheet == null:
		_draw_placeholder()
		draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	if show_collision:
		draw_arc(Vector2.ZERO, Tuning.PLAYER_RADIUS, 0, TAU, 24, Color(0, 1, 0.6), 1.0)

func _draw_placeholder() -> void:
	var ink := Color("#14121C")
	var tilt := {"hurt": -0.35, "defeat": 1.4}.get(pose, 0.0) as float
	draw_set_transform(Vector2.ZERO, tilt, Vector2(facing, 1))
	draw_rect(Rect2(-5, -6, 10, 12), Color("#2E3A59"))
	draw_rect(Rect2(-9, -2, 4, 5), Color("#8A5A3C"))
	draw_circle(Vector2(0, -12), 6, Color("#F2B84B"))
	draw_arc(Vector2(0, -12), 6, 0, TAU, 16, ink, 1.0)
	var stride := 2.0 if pose == "walk_contact" else (-2.0 if pose == "walk_passing" else 0.0)
	draw_line(Vector2(-2, 6), Vector2(-2 - stride, 11), ink, 2.0)
	draw_line(Vector2(2, 6), Vector2(2 + stride, 11), ink, 2.0)
	if pose in ["cast", "sunflare", "levelup", "victory"]:
		draw_line(Vector2(3, -3), Vector2(9, -9), ink, 2.0)
