"""Load service settings from config/settings.toml."""
import tomllib
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "config" / "settings.toml"


def load(path=DEFAULT_PATH):
    with open(path, "rb") as fh:
        return tomllib.load(fh)
