"""Daily digest email decision."""


def should_send(settings, events):
    return len(events) > 0
