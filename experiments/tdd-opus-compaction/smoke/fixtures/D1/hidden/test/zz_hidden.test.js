const test = require("node:test");
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
