"""Regenerate the Opus 5.5 TDD candidate from the pinned upstream bytes. No model calls.

Applies the edits O1-O8 (see packages/test-driven-development-opus-5-5/RATIONALE.md) to
packages/test-driven-development-upstream/7.0.2/SKILL.md. Each edit replaces an exact passage
that must occur exactly once. Resources and LICENSE are copied byte-for-byte.
Usage: python -I make_candidate.py [--check]   (--check: compare with the committed candidate)
"""
import hashlib
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "packages/test-driven-development-upstream/7.0.2"
DST = REPO / "packages/test-driven-development-opus-5-5/0.1.0"

DIAGRAM = '''```dot
digraph tdd_cycle {
    rankdir=LR;
    red [label="RED\\nWrite failing test", shape=box, style=filled, fillcolor="#ffcccc"];
    verify_red [label="Verify fails\\ncorrectly", shape=diamond];
    green [label="GREEN\\nMinimal code", shape=box, style=filled, fillcolor="#ccffcc"];
    verify_green [label="Verify passes\\nAll green", shape=diamond];
    refactor [label="REFACTOR\\nClean up", shape=box, style=filled, fillcolor="#ccccff"];
    next [label="Next", shape=ellipse];

    red -> verify_red;
    verify_red -> green [label="yes"];
    verify_red -> red [label="wrong\\nfailure"];
    green -> verify_green;
    verify_green -> refactor [label="yes"];
    verify_green -> green [label="no"];
    refactor -> verify_green [label="stay\\ngreen"];
    verify_green -> next;
    next -> red;
}
```
'''

RED_EXAMPLES = '''<Good>
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
Clear name, tests real behavior, one thing
</Good>

<Bad>
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
Vague name, tests mock not code
</Bad>

'''

GREEN_EXAMPLES = '''<Good>
```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```
Just enough to pass
</Good>

<Bad>
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI
}
```
Over-engineered
</Bad>

'''

BUG_EXAMPLE = '''## Example: Bug Fix

**Bug:** Empty email accepted

**RED**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**
```bash
$ npm test
FAIL: expected 'Email required', got undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**Verify GREEN**
```bash
$ npm test
PASS
```

**REFACTOR**
Extract validation for multiple fields if needed.

'''

GOOD_TESTS_TABLE = '''| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |
'''

GOOD_TESTS_LIST = '''- **Minimal:** one thing. "and" in name? Split it.
- **Clear:** name describes behavior.
- **Shows intent:** demonstrates desired API.
'''

# (id, old, new) - every old must occur exactly once in the text at the time it is applied.
EDITS = [
    ("O1", "## Red-Green-Refactor\n\n" + DIAGRAM + "\n",
     "## Red-Green-Refactor\n\nWork one behavior at a time, in this order: RED, Verify RED, GREEN, Verify GREEN,\nREFACTOR, then the next failing test.\n\n"),
    ("O2", "Write one minimal test showing what should happen.\n\n" + RED_EXAMPLES,
     "Write one minimal test showing what should happen.\n\n"),
    ("O3", "**Test errors?** Fix error, re-run until it fails correctly.\n",
     "**Test errors?** Fix error, re-run until it fails correctly.\n\n"
     "**Fails for another reason?** Go back to RED and correct the test.\n"),
    ("O4", "Write simplest code to pass the test.\n\n" + GREEN_EXAMPLES,
     "Write simplest code to pass the test.\n\n"),
    ("O5", BUG_EXAMPLE, ""),
    ("O6", "**MANDATORY. Never skip.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n",
     "**MANDATORY. Never skip.** Run the test.\n"),
    ("O7", "**MANDATORY.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n",
     "**MANDATORY.** Run the test.\n"),
    ("O8", GOOD_TESTS_TABLE, GOOD_TESTS_LIST),
]

PACKAGE_YAML = '''schema_version: 1
package:
  name: "@apsp/test-driven-development-opus-5-5"
  version: "0.1.0"
  type: skill
  description: "UNVALIDATED candidate for claude-opus-5-5 only. Derived from obra/superpowers test-driven-development v7.0.2 (22f0b46): SKILL.md compacted contract-first (cycle diagram, worked code examples, placeholder commands and bad-example column removed; one diagram condition extracted); frontmatter, every rule, rebuttal, red flag and checklist item, and resources unchanged. See companion RATIONALE.md."
  license: MIT
entrypoint: SKILL.md
behavior:
  delivery: instruction
  hosts: []
  effects: [commands]
'''


def build():
    text = (SRC / "SKILL.md").read_text(encoding="utf-8")
    for eid, old, new in EDITS:
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{eid}: expected exactly one occurrence, found {n}")
        text = text.replace(old, new)
    return text


def main(argv):
    text = build()
    if "--check" in argv:
        cur = (DST / "SKILL.md").read_text(encoding="utf-8")
        ok = cur == text and (DST / "package.yaml").read_text(encoding="utf-8") == PACKAGE_YAML
        print("candidate matches generator" if ok else "MISMATCH: candidate differs from generator")
        return 0 if ok else 1
    DST.mkdir(parents=True, exist_ok=True)
    (DST / "SKILL.md").write_text(text, encoding="utf-8", newline="\n")
    (DST / "package.yaml").write_text(PACKAGE_YAML, encoding="utf-8", newline="\n")
    for f in ("writing-good-tests.md", "LICENSE"):
        shutil.copyfile(SRC / f, DST / f)
    print("SKILL.md", len(text.encode()), hashlib.sha256(text.encode()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
