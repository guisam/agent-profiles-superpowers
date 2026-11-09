"""String helpers."""
import re


def truncate(text, width, ellipsis="..."):
    """Shorten text to at most width characters, ending with ellipsis when cut."""
    if len(text) <= width:
        return text
    if width <= len(ellipsis):
        return ellipsis[:width]
    return text[: width - len(ellipsis)] + ellipsis


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
