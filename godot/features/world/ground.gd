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
## Props that block the courier (Bao, 2026-09-29). Half-extents used until the generated sprite exists; with a
## sprite, the box is the sprite's opaque area inset by 2 px — what you bump into is what you see. A lantern post
## blocks only at its pole. Enemies are not blocked: moths fly over, fog-wraiths drift through.
const SOLID_HALF := {"stall": Vector2(28, 20), "cart": Vector2(28, 18), "crates": Vector2(18, 13), "post": Vector2(3, 20)}

var tile: Texture2D
var tex := {}
## [{kind, pos, layer}] — decals (layer 0) first, then props by y so lower ones overlap higher ones.
var props: Array = []
var solids: Array[Rect2] = []

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
	solids.clear()
	for p in props:
		if SOLID_HALF.has(p["kind"]):
			solids.append(_solid_box(p["kind"], p["pos"]))

func _solid_box(kind: String, pos: Vector2) -> Rect2:
	var t: Texture2D = tex.get(kind)
	if t and kind != "post":
		var used := t.get_image().get_used_rect()
		var top_left := pos - t.get_size() / 2 + Vector2(used.position)
		return Rect2(top_left + Vector2(2, 2), Vector2(used.size) - Vector2(4, 4))
	var half: Vector2 = SOLID_HALF[kind]
	return Rect2(pos - half, half * 2)

## True when a circle at p with radius r overlaps any solid prop.
func blocks(p: Vector2, r: float) -> bool:
	for box in solids:
		if box.grow(r).has_point(p) and _overlap(box, p, r):
			return true
	return false

func _overlap(box: Rect2, p: Vector2, r: float) -> bool:
	var c := p.clamp(box.position, box.end)
	return p.distance_to(c) < r or box.has_point(p)

## Moves a circle out of every solid it overlaps, along the shortest way out, so the courier slides along edges.
func push_out(p: Vector2, r: float) -> Vector2:
	for pass_i in 2:
		for box in solids:
			if not box.grow(r).has_point(p):
				continue
			if box.has_point(p):
				var left := p.x - box.position.x
				var right := box.end.x - p.x
				var up := p.y - box.position.y
				var down := box.end.y - p.y
				var m := minf(minf(left, right), minf(up, down))
				if m == left:
					p.x = box.position.x - r
				elif m == right:
					p.x = box.end.x + r
				elif m == up:
					p.y = box.position.y - r
				else:
					p.y = box.end.y + r
				continue
			var c := p.clamp(box.position, box.end)
			var d := p - c
			if d.length() < r and d.length() > 0.0001:
				p = c + d.normalized() * r
	return p

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
