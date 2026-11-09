const test = require("node:test");
const assert = require("node:assert");
const { formatPercent } = require("../src/format");

test("formats a ratio as a percentage", () => {
  assert.strictEqual(formatPercent(0.256), "26%");
});
