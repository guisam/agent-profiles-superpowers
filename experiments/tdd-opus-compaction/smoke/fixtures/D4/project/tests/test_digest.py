import unittest

from notify.digest import should_send


class ShouldSendTest(unittest.TestCase):
    def test_disabled_never_sends(self):
        self.assertFalse(should_send({"send_digest": False}, ["e1"]))

    def test_enabled_with_nothing_to_report_does_not_send(self):
        self.assertFalse(should_send({"send_digest": True}, []))


if __name__ == "__main__":
    unittest.main()
