"""Word helpers."""


def word_count(text):
    """Number of whitespace-separated words."""
    return len(text.split())


def truncate_words(text, n):
    """The first n words of text, joined by single spaces."""
    return " ".join(text.split()[:n])
