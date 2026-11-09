"""Word helpers."""


def word_count(text):
    """Number of whitespace-separated words."""
    return len(text.split())

import re


def truncate_words(text, n):
    return " ".join(re.findall(r"\S+", text)[:n])
