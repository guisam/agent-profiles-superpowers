"""Sequence helpers."""


def flatten(nested):
    """Flatten one level of nesting: [[1, 2], [3]] -> [1, 2, 3]."""
    return [item for inner in nested for item in inner]
