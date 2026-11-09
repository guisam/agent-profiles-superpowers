import unittest
from datetime import date

from tasks.model import Task
from tasks.report import overdue_titles
from tasks.store import InMemoryStore


class HiddenOverdueTest(unittest.TestCase):
    def test_overdue_open_oldest_first(self):
        s = InMemoryStore()
        s.add(Task("c", date(2026, 3, 5)))
        s.add(Task("a", date(2026, 3, 1)))
        s.add(Task("done", date(2026, 2, 1), done=True))
        s.add(Task("today", date(2026, 3, 10)))
        s.add(Task("future", date(2026, 4, 1)))
        s.add(Task("b", date(2026, 3, 3)))
        self.assertEqual(overdue_titles(s, date(2026, 3, 10)), ["a", "b", "c"])

    def test_empty(self):
        self.assertEqual(overdue_titles(InMemoryStore(), date(2026, 3, 10)), [])
