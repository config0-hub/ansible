# workspace_relay_test

Validates host-order `workspace_id` behavior with two modes:

- `two_calls` lays `workspace_lay` into a shared workspace, waits, then runs `workspace_check` with the same `workspace_id`.
- `isolation` runs `workspace_check` in a fresh workspace and is expected to fail because `from_lay.txt` is absent.
