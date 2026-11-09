class InMemoryStore:
    """A real, dependency-free task store."""

    def __init__(self):
        self._tasks = []

    def add(self, task):
        self._tasks.append(task)
        return task

    def all(self):
        return list(self._tasks)
