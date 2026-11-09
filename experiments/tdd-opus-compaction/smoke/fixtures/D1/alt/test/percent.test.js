const test = require("node:test");
const assert = require("node:assert");
const { applyCoupon } = require("../src/discount");

test("a 10% coupon on 5000 cents leaves 4500", () => {
  assert.strictEqual(applyCoupon(5000, { type: "percent", value: 10 }), 4500);
});
