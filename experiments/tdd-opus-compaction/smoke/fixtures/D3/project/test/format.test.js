const test = require("node:test");
const assert = require("node:assert");
const { pad2 } = require("../src/format");

test("pads single digits", () => {
  assert.strictEqual(pad2(5), "05");
});
