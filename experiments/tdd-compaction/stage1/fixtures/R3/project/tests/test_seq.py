import unittest

from listkit.seq import flatten


class FlattenTest(unittest.TestCase):
    def test_flattens_one_level(self):
        self.assertEqual(flatten([[1, 2], [3]]), [1, 2, 3])

    def test_empty(self):
        self.assertEqual(flatten([]), [])


if __name__ == "__main__":
    unittest.main()
