import unittest
from datetime import date

from tasks.model import Task
from tasks.report import overdue_titles
from tasks.store import InMemoryStore


class OverdueTest(unittest.TestCase):
    def test_oldest_open_overdue_first(self):
        store = InMemoryStore()
        store.add(Task("late2", date(2026, 3, 5)))
        store.add(Task("late1", date(2026, 3, 1)))
        store.add(Task("done", date(2026, 2, 1), done=True))
        self.assertEqual(overdue_titles(store, date(2026, 3, 10)), ["late1", "late2"])
