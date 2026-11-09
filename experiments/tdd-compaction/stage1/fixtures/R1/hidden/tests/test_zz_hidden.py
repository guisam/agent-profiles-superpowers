import unittest

from textkit.strings import slugify


class HiddenSlugifyTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "Hello World": "hello-world",
            "  Hello,  World!! ": "hello-world",
            "already-slug": "already-slug",
            "A--B__C": "a-b-c",
            "abc123 XYZ": "abc123-xyz",
            "!!!": "",
            "": "",
        }
        for given, want in cases.items():
            with self.subTest(given=given):
                self.assertEqual(slugify(given), want)

    def test_truncate_still_works(self):
        from textkit.strings import truncate
        self.assertEqual(truncate("abcdefgh", 6), "abc...")
