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
