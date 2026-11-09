import unittest
from datetime import date

from tasks.model import Task
from tasks.report import open_titles
from tasks.store import InMemoryStore


class OpenTitlesTest(unittest.TestCase):
    def test_lists_only_open_tasks(self):
        store = InMemoryStore()
        store.add(Task("write", date(2026, 3, 1)))
        store.add(Task("ship", date(2026, 3, 2), done=True))
        self.assertEqual(open_titles(store), ["write"])


if __name__ == "__main__":
    unittest.main()
