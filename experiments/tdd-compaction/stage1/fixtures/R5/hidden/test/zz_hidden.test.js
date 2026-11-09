const test = require("node:test");
const assert = require("node:assert");
const { formatBytes } = require("../src/format");

test("hidden: formatBytes", () => {
  assert.strictEqual(formatBytes(1536), "1.5 KB");
  assert.strictEqual(formatBytes(1048576), "1.0 MB");
  assert.strictEqual(formatBytes(2621440), "2.5 MB");
  assert.strictEqual(formatBytes(1610612736), "1.5 GB");
});
