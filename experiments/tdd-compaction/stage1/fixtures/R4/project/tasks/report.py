"""Reports over a task store."""


def open_titles(store):
    """Titles of tasks that are not done, in insertion order."""
    return [t.title for t in store.all() if not t.done]
