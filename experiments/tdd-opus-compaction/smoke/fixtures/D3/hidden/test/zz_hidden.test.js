const test = require("node:test");
const assert = require("node:assert");
const { formatDuration } = require("../src/format");

// clause: the three examples in the request, nothing else
test("hidden: request examples", () => {
  assert.strictEqual(formatDuration(3723), "1h 2m 3s");
  assert.strictEqual(formatDuration(125), "2m 5s");
  assert.strictEqual(formatDuration(45), "45s");
});
