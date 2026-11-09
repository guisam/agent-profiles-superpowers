import unittest
from datetime import date
from unittest.mock import MagicMock

from tasks.model import Task
from tasks.report import overdue_titles


class OverdueTest(unittest.TestCase):
    def test_overdue_and_sorted_and_open(self):
        store = MagicMock()
        store.all.return_value = [Task("a", date(2026, 3, 1))]
        self.assertEqual(overdue_titles(store, date(2026, 3, 10)), ["a"])
