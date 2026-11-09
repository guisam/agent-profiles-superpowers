const test = require("node:test");
const assert = require("node:assert");
const { formatBytes } = require("../src/format");

test("kilobytes with one decimal", () => {
  assert.strictEqual(formatBytes(1536), "1.5 KB");
});
