import unittest

from notify import settings
from notify.digest import should_send


class ConfiguredDigestTest(unittest.TestCase):
    def test_configured_service_sends_digest_when_there_are_events(self):
        self.assertTrue(should_send(settings.load(), ["event"]))
