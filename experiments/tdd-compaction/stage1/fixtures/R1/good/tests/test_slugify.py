import unittest

from textkit.strings import slugify


class SlugifyTest(unittest.TestCase):
    def test_spaces_become_hyphens(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation_runs_collapse_and_ends_are_trimmed(self):
        self.assertEqual(slugify(" Hi,  there!! "), "hi-there")
