import unittest

from textutil.words import truncate_words


class T(unittest.TestCase):
    def test_two_words(self):
        self.assertEqual(truncate_words("a b c", 2), "a b")
