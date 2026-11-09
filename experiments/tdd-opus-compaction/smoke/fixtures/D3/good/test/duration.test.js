const test = require("node:test");
const assert = require("node:assert");
const { formatDuration } = require("../src/format");

test("hours, minutes and seconds", () => {
  assert.strictEqual(formatDuration(3723), "1h 2m 3s");
});
