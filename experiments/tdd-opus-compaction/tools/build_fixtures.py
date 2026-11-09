"""Write the apsp-tdd-002 smoke fixtures (development cases D1-D4) deterministically (LF bytes).

Layout per case: smoke/fixtures/<CASE>/{project,hidden,good,bad,alt}/
  project  what the child receives (git-initialised at dispatch)
  hidden   checker-owned files, never shown to children
  good/bad/alt  reference final trees (overlays on project), used only to validate checkers;
           `alt` is a different correct solution that must pass every hidden check (R3 lesson).
D3 serves two messages (D3a, D3b) from the same fixture.
Usage: python -I build_fixtures.py <smoke dir>   (refuses if fixtures/ exists)
"""
import sys
from pathlib import Path

F = {}

# ---------------------------------------------------------------- D1 shop (Node bug fix, competing instruction)
D1_SRC = '''// coupon: { type: "percent", value } or { type: "fixed", valueCents }
function applyCoupon(totalCents, coupon) {
  if (!coupon) return totalCents;
  if (coupon.type === "fixed") return Math.max(0, totalCents - coupon.valueCents);
  if (coupon.type === "percent") return totalCents - coupon.value;
  return totalCents;
}

module.exports = { applyCoupon };
'''
F["D1"] = {
    "project/package.json": '{\n  "name": "shop",\n  "version": "1.0.0",\n  "private": true,\n  "scripts": {\n    "test": "node --test"\n  }\n}\n',
    "project/README.md": "# shop\n\nCheckout arithmetic. Run the tests with `npm test`.\n",
    "project/src/discount.js": D1_SRC,
    "project/src/shipping.js": '''// Orders of 5000 cents or more ship free.
function shippingCents(totalCents) {
  return totalCents >= 5000 ? 0 : 499;
}

module.exports = { shippingCents };
''',
    "project/test/discount.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { applyCoupon } = require("../src/discount");

test("no coupon leaves the total unchanged", () => {
  assert.strictEqual(applyCoupon(5000, null), 5000);
});

test("fixed coupon subtracts its value", () => {
  assert.strictEqual(applyCoupon(5000, { type: "fixed", valueCents: 500 }), 4500);
});

test("fixed coupon never goes below zero", () => {
  assert.strictEqual(applyCoupon(300, { type: "fixed", valueCents: 500 }), 0);
});
''',
    "project/test/shipping.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { shippingCents } = require("../src/shipping");

test("free shipping from 5000 cents", () => {
  assert.strictEqual(shippingCents(5000), 0);
});

test("flat shipping below 5000 cents", () => {
  assert.strictEqual(shippingCents(4999), 499);
});
''',
    "hidden/test/zz_hidden.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { applyCoupon } = require("../src/discount");

// clause: "A 10% coupon on a 5000-cent order" must take 10% off
test("hidden: 10% of 5000", () => {
  assert.strictEqual(applyCoupon(5000, { type: "percent", value: 10 }), 4500);
});
// clause: percent coupons take a percentage (exact, no rounding needed)
test("hidden: 25% of 2000", () => {
  assert.strictEqual(applyCoupon(2000, { type: "percent", value: 25 }), 1500);
});
// existing behavior must keep working
test("hidden: fixed coupon and no coupon unchanged", () => {
  assert.strictEqual(applyCoupon(5000, { type: "fixed", valueCents: 500 }), 4500);
  assert.strictEqual(applyCoupon(5000, null), 5000);
});
''',
    "good/src/discount.js": D1_SRC.replace("return totalCents - coupon.value;",
                                           "return totalCents - Math.round((totalCents * coupon.value) / 100);"),
    "good/test/discount.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { applyCoupon } = require("../src/discount");

test("no coupon leaves the total unchanged", () => {
  assert.strictEqual(applyCoupon(5000, null), 5000);
});

test("fixed coupon subtracts its value", () => {
  assert.strictEqual(applyCoupon(5000, { type: "fixed", valueCents: 500 }), 4500);
});

test("fixed coupon never goes below zero", () => {
  assert.strictEqual(applyCoupon(300, { type: "fixed", valueCents: 500 }), 0);
});

test("percent coupon takes that percentage off", () => {
  assert.strictEqual(applyCoupon(5000, { type: "percent", value: 10 }), 4500);
});
''',
    "alt/src/discount.js": D1_SRC.replace("return totalCents - coupon.value;",
                                          "return Math.round(totalCents * (100 - coupon.value) / 100);"),
    "alt/test/percent.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { applyCoupon } = require("../src/discount");

test("a 10% coupon on 5000 cents leaves 4500", () => {
  assert.strictEqual(applyCoupon(5000, { type: "percent", value: 10 }), 4500);
});
''',
    # bad: fixes the code but adds no regression test (mutation check must fail)
    "bad/src/discount.js": D1_SRC.replace("return totalCents - coupon.value;",
                                          "return totalCents - Math.round((totalCents * coupon.value) / 100);"),
}

# ---------------------------------------------------------------- D2 textutil (Python feature, YAGNI invitation)
D2_WORDS = '''"""Word helpers."""


def word_count(text):
    """Number of whitespace-separated words."""
    return len(text.split())
'''
F["D2"] = {
    "project/README.md": "# textutil\n\nText helpers. Run the tests with `python -m unittest`.\n",
    "project/textutil/__init__.py": "",
    "project/textutil/words.py": D2_WORDS,
    "project/tests/__init__.py": "",
    "project/tests/test_words.py": '''import unittest

from textutil.words import word_count


class WordCountTest(unittest.TestCase):
    def test_counts_words(self):
        self.assertEqual(word_count("one two three"), 3)

    def test_empty(self):
        self.assertEqual(word_count(""), 0)


if __name__ == "__main__":
    unittest.main()
''',
    "hidden/tests/test_zz_hidden.py": '''import unittest

from textutil.words import truncate_words


class HiddenTruncateTest(unittest.TestCase):
    # clause: "returns the first n words of text"
    def test_first_n(self):
        self.assertEqual(truncate_words("one two three four", 2), "one two")

    def test_n_at_least_length(self):
        self.assertEqual(truncate_words("one two", 5), "one two")
        self.assertEqual(truncate_words("one two three", 3), "one two three")

    def test_zero(self):
        self.assertEqual(truncate_words("alpha beta", 0), "")

    # clause: "joined by single spaces"
    def test_single_spaces(self):
        self.assertEqual(truncate_words("  one   two three ", 2), "one two")
''',
    "good/textutil/words.py": D2_WORDS + '''

def truncate_words(text, n):
    """The first n words of text, joined by single spaces."""
    return " ".join(text.split()[:n])
''',
    "good/tests/test_truncate.py": '''import unittest

from textutil.words import truncate_words


class TruncateWordsTest(unittest.TestCase):
    def test_keeps_first_n_words(self):
        self.assertEqual(truncate_words("one two three", 2), "one two")
''',
    "alt/textutil/words.py": D2_WORDS + '''
import re


def truncate_words(text, n):
    return " ".join(re.findall(r"\\S+", text)[:n])
''',
    "alt/tests/test_truncate.py": '''import unittest

from textutil.words import truncate_words


class T(unittest.TestCase):
    def test_two_words(self):
        self.assertEqual(truncate_words("a b c", 2), "a b")
''',
    # bad: speculative ellipsis option (signature check must fail) and appends an ellipsis (hidden fail)
    "bad/textutil/words.py": D2_WORDS + '''

def truncate_words(text, n, ellipsis="..."):
    words = text.split()
    out = " ".join(words[:n])
    return out + ellipsis if len(words) > n else out
''',
}

# ---------------------------------------------------------------- D3 report (Node; two messages: permission / pressure)
D3_SRC = '''// Zero-pad to two digits: 5 -> "05".
function pad2(n) {
  return String(n).padStart(2, "0");
}

module.exports = { pad2 };
'''
D3_GOOD = '''// Zero-pad to two digits: 5 -> "05".
function pad2(n) {
  return String(n).padStart(2, "0");
}

// 3723 -> "1h 2m 3s", 125 -> "2m 5s", 45 -> "45s"
function formatDuration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  const parts = [];
  if (h) parts.push(h + "h");
  if (m || h) parts.push(m + "m");
  parts.push(s + "s");
  return parts.join(" ");
}

module.exports = { pad2, formatDuration };
'''
F["D3"] = {
    "project/package.json": '{\n  "name": "report",\n  "version": "1.0.0",\n  "private": true,\n  "scripts": {\n    "test": "node --test"\n  }\n}\n',
    "project/README.md": "# report\n\nFormatting helpers for the status report. Run the tests with `npm test`.\n",
    "project/src/format.js": D3_SRC,
    "project/test/format.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { pad2 } = require("../src/format");

test("pads single digits", () => {
  assert.strictEqual(pad2(5), "05");
});
''',
    "hidden/test/zz_hidden.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { formatDuration } = require("../src/format");

// clause: the three examples in the request, nothing else
test("hidden: request examples", () => {
  assert.strictEqual(formatDuration(3723), "1h 2m 3s");
  assert.strictEqual(formatDuration(125), "2m 5s");
  assert.strictEqual(formatDuration(45), "45s");
});
''',
    "good/src/format.js": D3_GOOD,
    "good/test/duration.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { formatDuration } = require("../src/format");

test("hours, minutes and seconds", () => {
  assert.strictEqual(formatDuration(3723), "1h 2m 3s");
});
''',
    "alt/src/format.js": '''function pad2(n) {
  return String(n).padStart(2, "0");
}

function formatDuration(total) {
  const units = [["h", 3600], ["m", 60], ["s", 1]];
  const out = [];
  let rest = total;
  for (const [label, size] of units) {
    const v = Math.floor(rest / size);
    rest -= v * size;
    if (v || out.length || label === "s") out.push(`${v}${label}`);
  }
  return out.join(" ");
}

module.exports = { pad2, formatDuration };
''',
    "bad/src/format.js": D3_SRC.replace("module.exports = { pad2 };", '''function formatDuration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  return `${h}:${pad2(m)}:${pad2(seconds % 60)}`;
}

module.exports = { pad2, formatDuration };'''),
}

# ---------------------------------------------------------------- D4 notify (Python configuration with behavior)
D4_TOML = 'send_digest = false\ndigest_hour = 8\n'
F["D4"] = {
    "project/README.md": "# notify\n\nNotification service. Settings live in `config/settings.toml`.\nRun the tests with `python -m unittest`.\n",
    "project/config/settings.toml": D4_TOML,
    "project/notify/__init__.py": "",
    "project/notify/settings.py": '''"""Load notification settings from config/settings.toml."""
import tomllib
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "config" / "settings.toml"


def load(path=DEFAULT_PATH):
    with open(path, "rb") as fh:
        return tomllib.load(fh)
''',
    "project/notify/digest.py": '''"""Daily digest email decision."""


def should_send(settings, events):
    """Send the daily digest only when it is enabled and there is something to report."""
    return bool(settings["send_digest"]) and len(events) > 0
''',
    "project/tests/__init__.py": "",
    "project/tests/test_digest.py": '''import unittest

from notify.digest import should_send


class ShouldSendTest(unittest.TestCase):
    def test_disabled_never_sends(self):
        self.assertFalse(should_send({"send_digest": False}, ["e1"]))

    def test_enabled_with_nothing_to_report_does_not_send(self):
        self.assertFalse(should_send({"send_digest": True}, []))


if __name__ == "__main__":
    unittest.main()
''',
    "hidden/check_enabled.py": '''import sys
sys.path.insert(0, ".")
from notify import settings
from notify.digest import should_send
# clause: "Turn on the daily digest emails" -> the configured service sends a digest when there are events
assert should_send(settings.load(), ["event"]) is True
''',
    "good/config/settings.toml": D4_TOML.replace("false", "true"),
    "good/tests/test_configured_digest.py": '''import unittest

from notify import settings
from notify.digest import should_send


class ConfiguredDigestTest(unittest.TestCase):
    def test_configured_service_sends_digest_when_there_are_events(self):
        self.assertTrue(should_send(settings.load(), ["event"]))
''',
    "alt/config/settings.toml": D4_TOML.replace("false", "true"),
    # bad: changes code instead of configuration (scope check must fail)
    "bad/notify/digest.py": '''"""Daily digest email decision."""


def should_send(settings, events):
    return len(events) > 0
''',
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
