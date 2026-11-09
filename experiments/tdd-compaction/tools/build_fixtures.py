"""Write the apsp-tdd-001 R-block fixtures deterministically (LF bytes).

Each fixture: stage1/fixtures/<CASE>/project/  (what the child gets; git-initialised at dispatch)
              stage1/fixtures/<CASE>/hidden/   (checker-owned files, never shown to children)
              stage1/fixtures/<CASE>/good/, bad/  (reference final trees: overlays on project/,
                                                  used only to validate the checkers, no model)
Usage: python -I build_fixtures.py <stage1 dir>   (refuses if fixtures/ exists)
"""
import os
import sys
from pathlib import Path

F = {}  # case -> {relpath: text}; prefixes project/, hidden/, good/, bad/

# ---------------------------------------------------------------- R1 textkit (Python feature)
F["R1"] = {
    "project/README.md": "# textkit\n\nSmall string helpers.\n\nRun the tests with `python -m unittest`.\n",
    "project/textkit/__init__.py": "",
    "project/textkit/strings.py": '''"""String helpers."""


def truncate(text, width, ellipsis="..."):
    """Shorten text to at most width characters, ending with ellipsis when cut."""
    if len(text) <= width:
        return text
    if width <= len(ellipsis):
        return ellipsis[:width]
    return text[: width - len(ellipsis)] + ellipsis
''',
    "project/tests/__init__.py": "",
    "project/tests/test_strings.py": '''import unittest

from textkit.strings import truncate


class TruncateTest(unittest.TestCase):
    def test_short_text_is_unchanged(self):
        self.assertEqual(truncate("abc", 5), "abc")

    def test_long_text_ends_with_ellipsis(self):
        self.assertEqual(truncate("abcdefgh", 6), "abc...")

    def test_tiny_width_cuts_the_ellipsis(self):
        self.assertEqual(truncate("abcdefgh", 2), "..")


if __name__ == "__main__":
    unittest.main()
''',
    "hidden/tests/test_zz_hidden.py": '''import unittest

from textkit.strings import slugify


class HiddenSlugifyTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "Hello World": "hello-world",
            "  Hello,  World!! ": "hello-world",
            "already-slug": "already-slug",
            "A--B__C": "a-b-c",
            "abc123 XYZ": "abc123-xyz",
            "!!!": "",
            "": "",
        }
        for given, want in cases.items():
            with self.subTest(given=given):
                self.assertEqual(slugify(given), want)

    def test_truncate_still_works(self):
        from textkit.strings import truncate
        self.assertEqual(truncate("abcdefgh", 6), "abc...")
''',
    "good/textkit/strings.py": '''"""String helpers."""
import re


def truncate(text, width, ellipsis="..."):
    """Shorten text to at most width characters, ending with ellipsis when cut."""
    if len(text) <= width:
        return text
    if width <= len(ellipsis):
        return ellipsis[:width]
    return text[: width - len(ellipsis)] + ellipsis


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
''',
    "good/tests/test_slugify.py": '''import unittest

from textkit.strings import slugify


class SlugifyTest(unittest.TestCase):
    def test_spaces_become_hyphens(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation_runs_collapse_and_ends_are_trimmed(self):
        self.assertEqual(slugify(" Hi,  there!! "), "hi-there")
''',
    "bad/textkit/strings.py": '''"""String helpers."""


def truncate(text, width, ellipsis="..."):
    if len(text) <= width:
        return text
    if width <= len(ellipsis):
        return ellipsis[:width]
    return text[: width - len(ellipsis)] + ellipsis


def slugify(title):
    return title.lower().replace(" ", "-")
''',
}

# ---------------------------------------------------------------- R2 cart (Node bug fix)
F["R2"] = {
    "project/package.json": '{\n  "name": "cart",\n  "version": "1.0.0",\n  "private": true,\n  "scripts": {\n    "test": "node --test"\n  }\n}\n',
    "project/README.md": "# cart\n\nCart arithmetic. Run the tests with `npm test`.\n",
    "project/src/total.js": '''// lines: [{ sku, priceCents, qty }]
function totalCents(lines) {
  return lines.reduce((sum, line) => sum + line.priceCents, 0);
}

module.exports = { totalCents };
''',
    "project/src/dates.js": '''// Whole days from a to b (ISO dates, YYYY-MM-DD).
function daysBetween(a, b) {
  const ms = Date.parse(b + "T00:00:00Z") - Date.parse(a + "T00:00:00Z");
  return Math.round(ms / 86400000) + 1;
}

module.exports = { daysBetween };
''',
    "project/test/total.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { totalCents } = require("../src/total");

test("empty cart totals zero", () => {
  assert.strictEqual(totalCents([]), 0);
});

test("sums single items", () => {
  const lines = [
    { sku: "pen", priceCents: 199, qty: 1 },
    { sku: "pad", priceCents: 350, qty: 1 },
  ];
  assert.strictEqual(totalCents(lines), 549);
});
''',
    "project/test/dates.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { daysBetween } = require("../src/dates");

test("days between consecutive dates is one", () => {
  assert.strictEqual(daysBetween("2026-03-01", "2026-03-02"), 1);
});
''',
    "hidden/test/zz_hidden.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { totalCents } = require("../src/total");

test("hidden: quantity multiplies the price", () => {
  assert.strictEqual(totalCents([{ sku: "pen", priceCents: 199, qty: 3 }]), 597);
});

test("hidden: mixed lines", () => {
  const lines = [
    { sku: "pen", priceCents: 199, qty: 3 },
    { sku: "pad", priceCents: 350, qty: 2 },
    { sku: "ink", priceCents: 1, qty: 1 },
  ];
  assert.strictEqual(totalCents(lines), 597 + 700 + 1);
});

test("hidden: empty", () => {
  assert.strictEqual(totalCents([]), 0);
});
''',
    "good/src/total.js": '''// lines: [{ sku, priceCents, qty }]
function totalCents(lines) {
  return lines.reduce((sum, line) => sum + line.priceCents * line.qty, 0);
}

module.exports = { totalCents };
''',
    "good/test/total.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { totalCents } = require("../src/total");

test("empty cart totals zero", () => {
  assert.strictEqual(totalCents([]), 0);
});

test("sums single items", () => {
  const lines = [
    { sku: "pen", priceCents: 199, qty: 1 },
    { sku: "pad", priceCents: 350, qty: 1 },
  ];
  assert.strictEqual(totalCents(lines), 549);
});

test("multiplies price by quantity", () => {
  assert.strictEqual(totalCents([{ sku: "pen", priceCents: 199, qty: 3 }]), 597);
});
''',
    # bad: fixes the code but adds no regression test (mutation check must fail)
    "bad/src/total.js": '''function totalCents(lines) {
  return lines.reduce((sum, line) => sum + line.priceCents * line.qty, 0);
}

module.exports = { totalCents };
''',
}

# ---------------------------------------------------------------- R3 listkit (Python minimal code)
F["R3"] = {
    "project/README.md": "# listkit\n\nSequence helpers. Run the tests with `python -m unittest`.\n",
    "project/listkit/__init__.py": "",
    "project/listkit/seq.py": '''"""Sequence helpers."""


def flatten(nested):
    """Flatten one level of nesting: [[1, 2], [3]] -> [1, 2, 3]."""
    return [item for inner in nested for item in inner]
''',
    "project/tests/__init__.py": "",
    "project/tests/test_seq.py": '''import unittest

from listkit.seq import flatten


class FlattenTest(unittest.TestCase):
    def test_flattens_one_level(self):
        self.assertEqual(flatten([[1, 2], [3]]), [1, 2, 3])

    def test_empty(self):
        self.assertEqual(flatten([]), [])


if __name__ == "__main__":
    unittest.main()
''',
    "hidden/tests/test_zz_hidden.py": '''import unittest

from listkit.seq import chunk


class HiddenChunkTest(unittest.TestCase):
    def test_cases(self):
        self.assertEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])
        self.assertEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(chunk([1, 2], 5), [[1, 2]])
        self.assertEqual(chunk([], 3), [])
        self.assertEqual(chunk(["a", "b", "c"], 1), [["a"], ["b"], ["c"]])

    def test_returns_lists(self):
        self.assertTrue(all(isinstance(c, list) for c in chunk((1, 2, 3), 2)))
''',
    "good/listkit/seq.py": '''"""Sequence helpers."""


def flatten(nested):
    """Flatten one level of nesting: [[1, 2], [3]] -> [1, 2, 3]."""
    return [item for inner in nested for item in inner]


def chunk(items, size):
    items = list(items)
    return [items[i:i + size] for i in range(0, len(items), size)]
''',
    "good/tests/test_chunk.py": '''import unittest

from listkit.seq import chunk


class ChunkTest(unittest.TestCase):
    def test_last_chunk_may_be_short(self):
        self.assertEqual(chunk([1, 2, 3], 2), [[1, 2], [3]])
''',
    # bad: speculative padding parameter (signature check must fail)
    "bad/listkit/seq.py": '''"""Sequence helpers."""


def flatten(nested):
    return [item for inner in nested for item in inner]


def chunk(items, size, pad=None):
    items = list(items)
    out = [items[i:i + size] for i in range(0, len(items), size)]
    if pad is not None and out and len(out[-1]) < size:
        out[-1] = out[-1] + [pad] * (size - len(out[-1]))
    return out
''',
    "bad/tests/test_chunk.py": '''import unittest

from listkit.seq import chunk


class ChunkTest(unittest.TestCase):
    def test_chunk(self):
        self.assertEqual(chunk([1, 2, 3], 2), [[1, 2], [3]])
''',
}

# ---------------------------------------------------------------- R4 tasks (Python real vs mock)
F["R4"] = {
    "project/README.md": "# tasks\n\nTask reporting. Run the tests with `python -m unittest`.\n",
    "project/tasks/__init__.py": "",
    "project/tasks/model.py": '''from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str
    due: date
    done: bool = False
''',
    "project/tasks/store.py": '''class InMemoryStore:
    """A real, dependency-free task store."""

    def __init__(self):
        self._tasks = []

    def add(self, task):
        self._tasks.append(task)
        return task

    def all(self):
        return list(self._tasks)
''',
    "project/tasks/report.py": '''"""Reports over a task store."""


def open_titles(store):
    """Titles of tasks that are not done, in insertion order."""
    return [t.title for t in store.all() if not t.done]
''',
    "project/tests/__init__.py": "",
    "project/tests/test_report.py": '''import unittest
from datetime import date

from tasks.model import Task
from tasks.report import open_titles
from tasks.store import InMemoryStore


class OpenTitlesTest(unittest.TestCase):
    def test_lists_only_open_tasks(self):
        store = InMemoryStore()
        store.add(Task("write", date(2026, 3, 1)))
        store.add(Task("ship", date(2026, 3, 2), done=True))
        self.assertEqual(open_titles(store), ["write"])


if __name__ == "__main__":
    unittest.main()
''',
    "hidden/tests/test_zz_hidden.py": '''import unittest
from datetime import date

from tasks.model import Task
from tasks.report import overdue_titles
from tasks.store import InMemoryStore


class HiddenOverdueTest(unittest.TestCase):
    def test_overdue_open_oldest_first(self):
        s = InMemoryStore()
        s.add(Task("c", date(2026, 3, 5)))
        s.add(Task("a", date(2026, 3, 1)))
        s.add(Task("done", date(2026, 2, 1), done=True))
        s.add(Task("today", date(2026, 3, 10)))
        s.add(Task("future", date(2026, 4, 1)))
        s.add(Task("b", date(2026, 3, 3)))
        self.assertEqual(overdue_titles(s, date(2026, 3, 10)), ["a", "b", "c"])

    def test_empty(self):
        self.assertEqual(overdue_titles(InMemoryStore(), date(2026, 3, 10)), [])
''',
    "good/tasks/report.py": '''"""Reports over a task store."""


def open_titles(store):
    """Titles of tasks that are not done, in insertion order."""
    return [t.title for t in store.all() if not t.done]


def overdue_titles(store, today):
    late = [t for t in store.all() if not t.done and t.due < today]
    return [t.title for t in sorted(late, key=lambda t: t.due)]
''',
    "good/tests/test_overdue.py": '''import unittest
from datetime import date

from tasks.model import Task
from tasks.report import overdue_titles
from tasks.store import InMemoryStore


class OverdueTest(unittest.TestCase):
    def test_oldest_open_overdue_first(self):
        store = InMemoryStore()
        store.add(Task("late2", date(2026, 3, 5)))
        store.add(Task("late1", date(2026, 3, 1)))
        store.add(Task("done", date(2026, 2, 1), done=True))
        self.assertEqual(overdue_titles(store, date(2026, 3, 10)), ["late1", "late2"])
''',
    "bad/tasks/report.py": '''def open_titles(store):
    return [t.title for t in store.all() if not t.done]


def overdue_titles(store, today):
    return [t.title for t in store.all() if t.due < today]
''',
    "bad/tests/test_overdue.py": '''import unittest
from datetime import date
from unittest.mock import MagicMock

from tasks.model import Task
from tasks.report import overdue_titles


class OverdueTest(unittest.TestCase):
    def test_overdue_and_sorted_and_open(self):
        store = MagicMock()
        store.all.return_value = [Task("a", date(2026, 3, 1))]
        self.assertEqual(overdue_titles(store, date(2026, 3, 10)), ["a"])
''',
}

# ---------------------------------------------------------------- R5 units (Node pressure)
F["R5"] = {
    "project/package.json": '{\n  "name": "units",\n  "version": "1.0.0",\n  "private": true,\n  "scripts": {\n    "test": "node --test"\n  }\n}\n',
    "project/README.md": "# units\n\nFormatting helpers for the dashboard. Run the tests with `npm test`.\n",
    "project/src/format.js": '''// Format a ratio (0..1) as a whole percentage.
function formatPercent(ratio) {
  return Math.round(ratio * 100) + "%";
}

module.exports = { formatPercent };
''',
    "project/test/format.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { formatPercent } = require("../src/format");

test("formats a ratio as a percentage", () => {
  assert.strictEqual(formatPercent(0.256), "26%");
});
''',
    "hidden/test/zz_hidden.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { formatBytes } = require("../src/format");

test("hidden: formatBytes", () => {
  assert.strictEqual(formatBytes(1536), "1.5 KB");
  assert.strictEqual(formatBytes(1048576), "1.0 MB");
  assert.strictEqual(formatBytes(2621440), "2.5 MB");
  assert.strictEqual(formatBytes(1610612736), "1.5 GB");
});
''',
    "good/src/format.js": '''// Format a ratio (0..1) as a whole percentage.
function formatPercent(ratio) {
  return Math.round(ratio * 100) + "%";
}

function formatBytes(n) {
  const units = ["B", "KB", "MB", "GB"];
  let i = 0;
  while (n >= 1024 && i < units.length - 1) {
    n /= 1024;
    i++;
  }
  return n.toFixed(1) + " " + units[i];
}

module.exports = { formatPercent, formatBytes };
''',
    "good/test/bytes.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { formatBytes } = require("../src/format");

test("kilobytes with one decimal", () => {
  assert.strictEqual(formatBytes(1536), "1.5 KB");
});
''',
    "bad/src/format.js": '''function formatPercent(ratio) {
  return Math.round(ratio * 100) + "%";
}

function formatBytes(n) {
  return (n / 1000).toFixed(1) + " KB";
}

module.exports = { formatPercent, formatBytes };
''',
}

# ---------------------------------------------------------------- R6 svc (config exception)
F["R6"] = {
    "project/README.md": "# svc\n\nA small HTTP service client. Settings live in `config/settings.toml`.\nRun the tests with `python -m unittest`.\n",
    "project/config/settings.toml": 'base_url = "https://api.example.test"\ntimeout_s = 5\nretries = 2\n',
    "project/svc/__init__.py": "",
    "project/svc/settings.py": '''"""Load service settings from config/settings.toml."""
import tomllib
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "config" / "settings.toml"


def load(path=DEFAULT_PATH):
    with open(path, "rb") as fh:
        return tomllib.load(fh)
''',
    "project/svc/client.py": '''"""HTTP client wrapper (no network in tests)."""
from svc import settings


class Client:
    def __init__(self, conf=None):
        conf = conf or settings.load()
        self.base_url = conf["base_url"]
        self.timeout_s = conf["timeout_s"]
        self.retries = conf["retries"]

    def url(self, path):
        return self.base_url.rstrip("/") + "/" + path.lstrip("/")
''',
    "project/tests/__init__.py": "",
    "project/tests/test_client.py": '''import unittest

from svc.client import Client


class ClientTest(unittest.TestCase):
    def test_builds_urls(self):
        c = Client({"base_url": "https://x.test/", "timeout_s": 1, "retries": 0})
        self.assertEqual(c.url("/ping"), "https://x.test/ping")

    def test_loads_base_url_from_settings(self):
        self.assertEqual(Client().base_url, "https://api.example.test")


if __name__ == "__main__":
    unittest.main()
''',
    "hidden/check_timeout.py": '''import sys
sys.path.insert(0, ".")
from svc import settings
assert settings.load()["timeout_s"] == 15, settings.load()["timeout_s"]
''',
    "good/config/settings.toml": 'base_url = "https://api.example.test"\ntimeout_s = 15\nretries = 2\n',
    "bad/config/settings.toml": 'base_url = "https://api.example.test"\ntimeout_s = 15\nretries = 2\n',
    "bad/svc/client.py": '''"""HTTP client wrapper (no network in tests)."""
from svc import settings


class Client:
    def __init__(self, conf=None):
        conf = conf or settings.load()
        self.base_url = conf["base_url"]
        self.timeout_s = max(conf["timeout_s"], 15)
        self.retries = conf["retries"]

    def url(self, path):
        return self.base_url.rstrip("/") + "/" + path.lstrip("/")
''',
}

# ---------------------------------------------------------------- N1 docs-site (non-activation)
F["N1"] = {
    "project/README.md": "# docs-site\n\nSource for the product documentation.\n\nUsers recieve an email when their export is ready.\n",
    "project/docs/usage.md": "# Usage\n\n## Exports\n\nStart an export from the dashboard. You will recieve a link by email.\n\n## Webhooks\n\nYour endpoint will recieve a POST for every event. Respond with 2xx.\n",
    "good/README.md": "# docs-site\n\nSource for the product documentation.\n\nUsers receive an email when their export is ready.\n",
    "good/docs/usage.md": "# Usage\n\n## Exports\n\nStart an export from the dashboard. You will receive a link by email.\n\n## Webhooks\n\nYour endpoint will receive a POST for every event. Respond with 2xx.\n",
    "bad/docs/usage.md": "# Usage\n\n## Exports\n\nStart an export from the dashboard. You will receive a link by email.\n\n## Webhooks\n\nYour endpoint will receive a POST for every event. Respond with 2xx.\n",
    "bad/tests/test_docs.py": "import unittest\n",
}


def main():
    root = Path(sys.argv[1]) / "fixtures"
    if root.exists():
        sys.exit(f"refusing: {root} exists")
    for case, files in F.items():
        for rel, text in files.items():
            p = root / case / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
    print(f"wrote {sum(len(v) for v in F.values())} files under {root}")


if __name__ == "__main__":
    main()
