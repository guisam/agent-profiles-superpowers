const test = require("node:test");
const assert = require("node:assert");
const { shippingCents } = require("../src/shipping");

test("free shipping from 5000 cents", () => {
  assert.strictEqual(shippingCents(5000), 0);
});

test("flat shipping below 5000 cents", () => {
  assert.strictEqual(shippingCents(4999), 499);
});
