"""Daily digest email decision."""


def should_send(settings, events):
    """Send the daily digest only when it is enabled and there is something to report."""
    return bool(settings["send_digest"]) and len(events) > 0
