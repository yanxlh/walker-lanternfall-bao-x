extends SceneTree
## Assignment 7 clip strips: the saved courier_visual.tscn alone, 8x, on a flat grey ground, one image per clip frame
## (walk: 16 ticks; dash: every tick of the clip plus the rest pose at its end). Windowed only (a headless run draws nothing):
##   Godot --path godot --resolution 1280x720 --script res://tests/capture_courier_clip_strip.gd -- --out <dir>
## Each frame is seeked in manual mode, then captured after frame_post_draw. Writes walk-NN.png, dash-NN.png and
## strip-walk.png / strip-dash.png (labelled by the Python strip step, not here). The game never loads this script.
const SCENE := "res://features/player/courier_visual.tscn"
const FPS := 60.0
const ZOOM := 8.0

var out_dir := ""

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	var at := args.find("--out")
	out_dir = args[at + 1] if at >= 0 and at + 1 < args.size() else ProjectSettings.globalize_path("res://../captures/assignment-7/clip-strips")
	DirAccess.make_dir_recursive_absolute(out_dir)
	call_deferred("_main")

func _main() -> void:
	var ground := ColorRect.new()
	ground.color = Color(0.62, 0.62, 0.66)
	ground.size = Vector2(640, 360)
	root.add_child(ground)
	var visual: Node2D = load(SCENE).instantiate()
	visual.position = Vector2(320, 230)
	visual.scale = Vector2(ZOOM, ZOOM) / 2.0
	root.add_child(visual)
	var player: AnimationPlayer = visual.get_node("AnimationPlayer")
	var dash_frames := roundi(player.get_animation("dash").length * FPS) + 1
	for clip in [["walk", 16], ["dash", dash_frames]]:
		player.play(clip[0])
		for f in clip[1]:
			player.seek(f / FPS, true)
			await process_frame
			await RenderingServer.frame_post_draw
			var img := root.get_texture().get_image()
			var s := img.get_width() / 640.0
			var box := Rect2i(int((320 - 96) * s), int((230 - 160) * s), int(192 * s), int(200 * s))
			img.get_region(box).save_png("%s/%s-%02d.png" % [out_dir, clip[0], f])
	print("saved clip frames to ", out_dir)
	quit()
