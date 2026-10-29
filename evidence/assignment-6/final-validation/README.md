# Final regression verification

Godot 4.7.2 was imported once into a clean project checkout. All seven suites were run through scripts/run-test.sh. Logic 32, gameplay 65, audio 25, hit configuration 39, extra particle configuration 79, state 34, edges 18: 292 assertions and zero failures. Audio used realtime mode; all others used fixed 60 mode. No SHADER ERROR or SCRIPT ERROR appeared.

Raw outputs and exit codes are kept in this directory. Existing resource-in-use shutdown diagnostics occurred in several suites; they are retained rather than hidden. The sandboxed import also logged inability to write user editor settings outside the workspace; it completed successfully and imported the game resources. No game source or expected assertions were changed.
