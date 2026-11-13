#!/usr/bin/env bash
# Self-check of scripts/run-test.sh (Assignment 7): the fixture godot/tests/fixture_resource_load_error.gd exits 0
# but logs resource-load failures, so the wrapper must exit 1 on it; a passing suite must still exit 0.
cd "$(dirname "$0")/.." || exit 1
./scripts/run-test.sh fixture_resource_load_error.gd 60 > /dev/null 2>&1; fixture=$?
./scripts/run-test.sh test_courier_states.gd 60 > /dev/null 2>&1; passing=$?
echo "fixture_resource_load_error.gd -> exit $fixture (want 1); test_courier_states.gd -> exit $passing (want 0)"
[ "$fixture" = 1 ] && [ "$passing" = 0 ]
