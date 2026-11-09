"""Word helpers."""


def word_count(text):
    """Number of whitespace-separated words."""
    return len(text.split())


def truncate_words(text, n, ellipsis="..."):
    words = text.split()
    out = " ".join(words[:n])
    return out + ellipsis if len(words) > n else out
