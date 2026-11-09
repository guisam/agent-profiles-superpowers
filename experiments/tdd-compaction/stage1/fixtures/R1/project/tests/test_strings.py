import unittest

from textkit.strings import truncate


class TruncateTest(unittest.TestCase):
    def test_short_text_is_unchanged(self):
        self.assertEqual(truncate("abc", 5), "abc")

    def test_long_text_ends_with_ellipsis(self):
        self.assertEqual(truncate("abcdefgh", 6), "abc...")

    def test_tiny_width_cuts_the_ellipsis(self):
        self.assertEqual(truncate("abcdefgh", 2), "..")


if __name__ == "__main__":
    unittest.main()
