"""Sequence helpers."""


def flatten(nested):
    return [item for inner in nested for item in inner]


def chunk(items, size, pad=None):
    items = list(items)
    out = [items[i:i + size] for i in range(0, len(items), size)]
    if pad is not None and out and len(out[-1]) < size:
        out[-1] = out[-1] + [pad] * (size - len(out[-1]))
    return out
