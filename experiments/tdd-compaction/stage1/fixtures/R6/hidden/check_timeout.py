import sys
sys.path.insert(0, ".")
from svc import settings
assert settings.load()["timeout_s"] == 15, settings.load()["timeout_s"]
