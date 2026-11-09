const test = require("node:test");
const assert = require("node:assert");
const { totalCents } = require("../src/total");

test("hidden: quantity multiplies the price", () => {
  assert.strictEqual(totalCents([{ sku: "pen", priceCents: 199, qty: 3 }]), 597);
});

test("hidden: mixed lines", () => {
  const lines = [
    { sku: "pen", priceCents: 199, qty: 3 },
    { sku: "pad", priceCents: 350, qty: 2 },
    { sku: "ink", priceCents: 1, qty: 1 },
  ];
  assert.strictEqual(totalCents(lines), 597 + 700 + 1);
});

test("hidden: empty", () => {
  assert.strictEqual(totalCents([]), 0);
});
