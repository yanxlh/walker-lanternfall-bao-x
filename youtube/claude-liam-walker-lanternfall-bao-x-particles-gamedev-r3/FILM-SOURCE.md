# Film source — what this film shows

The game in this film is a snapshot of the working tree of branch `assignment-6-r3`, taken on 9 November 2026 at 17:56 EST, while documents were still being edited.

| Identity | Value |
|---|---|
| Base commit | `c6e63434830075f288ab376712aa1cdea19f5231` (A r2 kept) |
| `godot/` tree id of the snapshot | `14e6b2ced0edbfc6d5db4686824af4903b9a5d7b` (`FILM-SOURCE-REVISION.txt`) |
| `godot/` tree id at the base commit | `bc5f93e0f3e5f4c52edcad0cd55e9eb49b68bbd2` |
| Snapshot tree (godot plus the documents and evidence read by the film) | `5bab6e4c4728fae26e8d72faa4976edca74ffa7d` |

Under `godot/`, the snapshot differs from the base commit only in tests that were not yet committed:
- `tests/test_defeat_sparks_config.gd` and `tests/test_extra_particles_config.gd` also read back `z_index`;
- `tests/test_particles_tree_pause.gd` is new.

Game code, effect scenes, shaders, assets and project settings are those of `c6e6343`.

Every file of the snapshot's `godot/` matches `evidence/assignment-6/current-r2-validation/source-sha256.json` (143 files, 0 mismatches). That is the copy on which nine suites passed 327 assertions.

To identify a later commit as this film's source, compare `git rev-parse <commit>:godot` with the tree id above. If they are equal, the film shows that commit's game source.

The tree ids were computed with a temporary git index (`GIT_INDEX_FILE`), so the repository's own index and working tree were not changed.
