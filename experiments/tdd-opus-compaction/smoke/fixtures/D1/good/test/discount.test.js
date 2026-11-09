const test = require("node:test");
const assert = require("node:assert");
const { applyCoupon } = require("../src/discount");

test("no coupon leaves the total unchanged", () => {
  assert.strictEqual(applyCoupon(5000, null), 5000);
});

test("fixed coupon subtracts its value", () => {
  assert.strictEqual(applyCoupon(5000, { type: "fixed", valueCents: 500 }), 4500);
});

test("fixed coupon never goes below zero", () => {
  assert.strictEqual(applyCoupon(300, { type: "fixed", valueCents: 500 }), 0);
});

test("percent coupon takes that percentage off", () => {
  assert.strictEqual(applyCoupon(5000, { type: "percent", value: 10 }), 4500);
});
