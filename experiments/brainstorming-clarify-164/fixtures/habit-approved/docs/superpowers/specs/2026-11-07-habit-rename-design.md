# habit rename: short design

Status: approved by the user on 2026-11-07 ("Approved, go ahead.").

- Intent: fix typos in habit names without losing the streak.
- Approach (picked by the user): rename in place in the data that store.js loads and saves.
  Considered and dropped: an id layer (too much change for a tiny tool).
- Command: `habit rename <old> <new>`.
- Unknown `<old>`: print `no such habit: <old>`, exit 1.
- Existing `<new>`: print `habit already exists: <new>`, exit 1, change nothing.
- README usage block gets a `rename` line.
- Left to the builder: where the rename branch sits in cli.js; a test for the rename.
