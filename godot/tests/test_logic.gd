extends "res://tests/harness.gd"
const GS = preload("res://game/game_state.gd")
const Prog = preload("res://features/progression/progression.gd")

func run() -> void:
	suite = "logic"
	_state_tests()
	_progression_tests()

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

func _progression_tests() -> void:
	var p = Prog.new()
	var levels: Array = []
	p.leveled_up.connect(func(l): levels.append(l))
	var gained: int = p.add_xp(3 + 5 + 7)
	check("prog-multi-level", gained == 3 and p.level == 4 and p.pending_levelups == 3 and levels == [2, 3, 4], {"gained": gained, "levels": levels})
	var rng := RandomNumberGenerator.new()
	rng.seed = 42
	var offer: Array[String] = p.offer_cards(rng)
	var unique := {}
	for c in offer: unique[c] = true
	check("prog-offer-three-unique", offer.size() == 3 and unique.size() == 3 and not ("sunflare" in offer), {"offer": offer})
	var early: Array[String] = p.eligible_cards()
	check("prog-branches-offered", "beam_rate" in early and "beam_pierce" in early and "moth_new" in early and not ("moth_count" in early), {"eligible": early})
	p.apply("beam_rate")
	check("prog-beam-rate", p.beam_level == 2 and p.beam_cooldown_ticks == 30, {"cooldown": p.beam_cooldown_ticks})
	p.apply("beam_pierce")
	p.apply("moth_new")
	p.apply("moth_count")
	check("prog-not-ready-at-moth-2", not p.evolution_ready() and not ("sunflare" in p.offer_cards(rng)))
	p.apply("moth_radius")
	check("prog-maxed-weapons", p.beam_level == 3 and p.moth_level == 3 and p.moth_count == 3 and p.beam_pierce == 2)
	var evo: Array[String] = p.offer_cards(rng)
	check("prog-sunflare-offered-first", p.evolution_ready() and evo[0] == "sunflare" and evo.size() == 3, {"offer": evo})
	p.apply("sunflare")
	var after: Array[String] = p.eligible_cards()
	check("prog-after-evolve-no-weapon-cards", p.evolved_sunflare and not p.evolution_ready() and not ("beam_rate" in after) and not ("moth_count" in after), {"eligible": after})
	for k in ["pass_speed", "pass_speed", "pass_magnet", "pass_magnet", "pass_hp", "pass_hp"]:
		p.apply(k)
	check("prog-exhausted-pool-pads-heal", p.offer_cards(rng) == ["heal", "heal", "heal"])
	var a = Prog.new(); var b = Prog.new()
	var r1 := RandomNumberGenerator.new(); r1.seed = 7
	var r2 := RandomNumberGenerator.new(); r2.seed = 7
	check("prog-deterministic", a.offer_cards(r1) == b.offer_cards(r2))
