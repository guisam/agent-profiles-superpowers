import unittest

from textutil.words import truncate_words


class TruncateWordsTest(unittest.TestCase):
    def test_keeps_first_n_words(self):
        self.assertEqual(truncate_words("one two three", 2), "one two")
