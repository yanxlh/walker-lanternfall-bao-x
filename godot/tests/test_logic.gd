extends "res://tests/harness.gd"
const GS = preload("res://game/game_state.gd")

func run() -> void:
	suite = "logic"
	_state_tests()

func _state_tests() -> void:
	var s = GS.new()
	var changes: Array = []
	s.changed.connect(func(f, t): changes.append([f, t]))
	check("state-menu-rejects-won", not s.go(GS.WON) and s.current == GS.MENU)
	check("state-menu-to-playing", s.go(GS.PLAYING) and s.current == GS.PLAYING)
	check("state-levelup-roundtrip", s.go(GS.LEVELUP) and s.go(GS.PLAYING))
	check("state-pause-roundtrip", s.go(GS.PAUSED) and not s.go(GS.LEVELUP) and s.go(GS.PLAYING))
	s.go(GS.LOST)
	check("state-terminal-is-sticky", not s.go(GS.PLAYING) and not s.go(GS.WON) and s.is_terminal())
	check("state-restart-from-terminal", s.restart() and s.current == GS.PLAYING)
	check("state-signal-log", changes.size() == 7 and changes[-1] == [GS.LOST, GS.PLAYING], {"changes": changes})
	var m = GS.new()
	check("state-restart-not-from-menu", not m.restart())
