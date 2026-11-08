# habit

A tiny command-line habit tracker. Data lives in `~/.habit.json`.

    habit add <name>      start tracking a habit
    habit done <name>     mark today as done
    habit list            show habits and current streaks

## Sync

`~/.habit.json` is also read by `habit-sync`, the phone app I use. It only
understands `{"habits": {"<name>": ["YYYY-MM-DD", ...]}}` and rejects the
whole file if it finds any other field. Keep that file's shape exactly as it is.
