"""HTTP client wrapper (no network in tests)."""
from svc import settings


class Client:
    def __init__(self, conf=None):
        conf = conf or settings.load()
        self.base_url = conf["base_url"]
        self.timeout_s = max(conf["timeout_s"], 15)
        self.retries = conf["retries"]

    def url(self, path):
        return self.base_url.rstrip("/") + "/" + path.lstrip("/")
