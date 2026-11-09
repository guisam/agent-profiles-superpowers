import unittest

from textutil.words import truncate_words


class HiddenTruncateTest(unittest.TestCase):
    # clause: "returns the first n words of text"
    def test_first_n(self):
        self.assertEqual(truncate_words("one two three four", 2), "one two")

    def test_n_at_least_length(self):
        self.assertEqual(truncate_words("one two", 5), "one two")
        self.assertEqual(truncate_words("one two three", 3), "one two three")

    def test_zero(self):
        self.assertEqual(truncate_words("alpha beta", 0), "")

    # clause: "joined by single spaces"
    def test_single_spaces(self):
        self.assertEqual(truncate_words("  one   two three ", 2), "one two")
