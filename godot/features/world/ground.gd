extends Node2D
## The night market: two streets lined with stalls and noodle carts, lantern posts between them, crates beside
## the stalls, puddles and leaves on the cobbles. Decoration only — nothing collides — and built from its own
## fixed seed, so it never touches the game rng. A plaza around the spawn point stays clear.

const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

const PLAZA_RADIUS := 150.0
const STREETS_Y := [-300.0, 300.0]
const STALL_SPACING := 190.0
const PUDDLES := 36
const LEAVES := 60
const PATHS := {
	"stall": Art.STALL, "cart": Art.CART, "post": Art.POST, "crates": Art.CRATES,
	"puddle": Art.PUDDLE, "leaves": Art.LEAVES,
}
const DECALS := ["puddle", "leaves"]

var tile: Texture2D
var tex := {}
## [{kind, pos, layer}] — decals (layer 0) first, then props by y so lower ones overlap higher ones.
var props: Array = []

func _ready() -> void:
	z_index = -10
	texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	tile = Art.texture(Art.GROUND)
	for k in PATHS:
		tex[k] = Art.texture(PATHS[k])
	build()
	queue_redraw()

func build() -> void:
	props.clear()
	var r := RandomNumberGenerator.new()
	r.seed = 1234
	var a := Tuning.ARENA
	for street_y in STREETS_Y:
		var x: float = a.position.x + 90.0
		while x < a.end.x - 90.0:
			for side in [-1.0, 1.0]:
				var y: float = street_y + side * 72.0
				_add("cart" if r.randf() < 0.35 else "stall", Vector2(x + r.randf_range(-14, 14), y))
				if r.randf() < 0.55:
					_add("crates", Vector2(x + 46 + r.randf_range(-6, 6), y + 14))
				_add("post", Vector2(x + STALL_SPACING / 2.0, street_y + side * 34.0))
			x += STALL_SPACING
	for i in PUDDLES:
		_add("puddle", Vector2(r.randf_range(a.position.x, a.end.x), r.randf_range(a.position.y, a.end.y)))
	for i in LEAVES:
		_add("leaves", Vector2(r.randf_range(a.position.x, a.end.x), r.randf_range(a.position.y, a.end.y)))
	props.sort_custom(func(p, q): return p["layer"] < q["layer"] or (p["layer"] == q["layer"] and p["pos"].y < q["pos"].y))

func _add(kind: String, pos: Vector2) -> void:
	if pos.length() <= PLAZA_RADIUS or not Tuning.ARENA.grow(-24).has_point(pos):
		return
	props.append({"kind": kind, "pos": pos, "layer": 0 if kind in DECALS else 1})

func _draw() -> void:
	var a := Tuning.ARENA
	if tile:
		draw_texture_rect(tile, a, true)
	else:
		draw_rect(a, Color("#1F2540"))
		for x in range(int(a.position.x), int(a.end.x), 64):
			draw_line(Vector2(x, a.position.y), Vector2(x, a.end.y), Color("#3B4A6B", 0.35))
		for y in range(int(a.position.y), int(a.end.y), 64):
			draw_line(Vector2(a.position.x, y), Vector2(a.end.x, y), Color("#3B4A6B", 0.35))
	for p in props:
		var t: Texture2D = tex.get(p["kind"])
		var pos: Vector2 = p["pos"]
		if p["kind"] == "post":
			# a soft pool of lantern light on the cobbles (drawn, not generated)
			draw_circle(pos + Vector2(0, 18), 30.0, Color(0.95, 0.72, 0.29, 0.07))
		if t:
			draw_texture(t, pos - t.get_size() / 2)
		else:
			_draw_placeholder(p["kind"], pos)
	draw_rect(a, Color(0.95, 0.72, 0.29, 0.6), false, 2.0)

func _draw_placeholder(kind: String, p: Vector2) -> void:
	match kind:
		"stall":
			draw_rect(Rect2(p - Vector2(24, 16), Vector2(48, 32)), Color("#B5523B"))
			draw_circle(p - Vector2(0, 24), 6, Color("#F2B84B"))
		"cart":
			draw_rect(Rect2(p - Vector2(24, 12), Vector2(48, 24)), Color("#3B4A6B"))
			draw_circle(p - Vector2(10, 18), 5, Color("#F2B84B"))
		"post":
			draw_line(p + Vector2(0, 20), p - Vector2(0, 20), Color("#14121C"), 2.0)
			draw_circle(p - Vector2(0, 16), 5, Color("#F2B84B"))
		"crates":
			draw_rect(Rect2(p - Vector2(14, 10), Vector2(28, 20)), Color("#8A5A3C"))
		"puddle":
			draw_circle(p, 10, Color("#0E1020", 0.8))
		"leaves":
			draw_circle(p, 3, Color("#8A5A3C"))
