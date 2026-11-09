import unittest

from listkit.seq import chunk


class HiddenChunkTest(unittest.TestCase):
    def test_cases(self):
        self.assertEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])
        self.assertEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(chunk([1, 2], 5), [[1, 2]])
        self.assertEqual(chunk([], 3), [])
        self.assertEqual(chunk(["a", "b", "c"], 1), [["a"], ["b"], ["c"]])

    def test_returns_lists(self):
        self.assertTrue(all(isinstance(c, list) for c in chunk((1, 2, 3), 2)))
