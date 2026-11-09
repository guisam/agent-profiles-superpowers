"""Reports over a task store."""


def open_titles(store):
    """Titles of tasks that are not done, in insertion order."""
    return [t.title for t in store.all() if not t.done]


def overdue_titles(store, today):
    late = [t for t in store.all() if not t.done and t.due < today]
    return [t.title for t in sorted(late, key=lambda t: t.due)]
