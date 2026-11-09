def open_titles(store):
    return [t.title for t in store.all() if not t.done]


def overdue_titles(store, today):
    return [t.title for t in store.all() if t.due < today]
