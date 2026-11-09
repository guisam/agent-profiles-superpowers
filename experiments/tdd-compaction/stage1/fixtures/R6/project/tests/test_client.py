import unittest

from svc.client import Client


class ClientTest(unittest.TestCase):
    def test_builds_urls(self):
        c = Client({"base_url": "https://x.test/", "timeout_s": 1, "retries": 0})
        self.assertEqual(c.url("/ping"), "https://x.test/ping")

    def test_loads_base_url_from_settings(self):
        self.assertEqual(Client().base_url, "https://api.example.test")


if __name__ == "__main__":
    unittest.main()
