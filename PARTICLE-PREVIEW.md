# Particle preview fixtures

The preview scenes are independent fixtures, not normal gameplay captures. The integrated game includes weapon-hit sparks, a movement trail and a level-up celebration.

Open the project with Godot 4.7.2. Run `scripts/preview-defeat-sparks.command` for the hit-spark fixture. Space triggers a burst, R triggers two bursts 0.1 seconds apart, and Escape closes the preview.

For a new capture revision, run `bash scripts/capture-defeat-sparks.command rN`. Existing revision directories are protected from replacement. Selected frames are stored below `captures/defeat_sparks/rN/strip/`; label them as fixtures. Compare the strips and record the student's separate running-game verdict in `TUNING.md`.

Run `./scripts/run-test.sh test_defeat_sparks_config.gd 60` for the configuration check (39 assertions). Full state, edge, extra configuration and regression commands are in `CLAUDE.md`.
