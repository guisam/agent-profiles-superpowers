const test = require("node:test");
const assert = require("node:assert");
const { daysBetween } = require("../src/dates");

test("days between consecutive dates is one", () => {
  assert.strictEqual(daysBetween("2026-03-01", "2026-03-02"), 1);
});
