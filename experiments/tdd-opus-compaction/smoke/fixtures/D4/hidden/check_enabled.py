import sys
sys.path.insert(0, ".")
from notify import settings
from notify.digest import should_send
# clause: "Turn on the daily digest emails" -> the configured service sends a digest when there are events
assert should_send(settings.load(), ["event"]) is True
