"""String helpers."""


def truncate(text, width, ellipsis="..."):
    if len(text) <= width:
        return text
    if width <= len(ellipsis):
        return ellipsis[:width]
    return text[: width - len(ellipsis)] + ellipsis


def slugify(title):
    return title.lower().replace(" ", "-")
