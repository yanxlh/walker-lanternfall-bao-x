extends Node2D
## Tiled ground and decorative stalls. Uses its own fixed seed so it never touches the game rng.
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var tile: Texture2D
var stall: Texture2D
var props: Array[Vector2] = []

func _ready() -> void:
	z_index = -10
	texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	tile = Art.texture(Art.GROUND)
	stall = Art.texture(Art.STALL)
	var r := RandomNumberGenerator.new()
	r.seed = 1234
	var a := Tuning.ARENA
	while props.size() < 18:
		var p := Vector2(r.randf_range(a.position.x + 48, a.end.x - 48), r.randf_range(a.position.y + 48, a.end.y - 48))
		if p.length() > 120:
			props.append(p)
	queue_redraw()

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
		if stall:
			draw_texture(stall, p - stall.get_size() / 2)
		else:
			draw_rect(Rect2(p - Vector2(24, 16), Vector2(48, 32)), Color("#B5523B"))
			draw_circle(p - Vector2(0, 24), 6, Color("#F2B84B"))
	draw_rect(a, Color(0.95, 0.72, 0.29, 0.6), false, 2.0)
