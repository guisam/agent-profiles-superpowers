const test = require("node:test");
const assert = require("node:assert");
const { totalCents } = require("../src/total");

test("empty cart totals zero", () => {
  assert.strictEqual(totalCents([]), 0);
});

test("sums single items", () => {
  const lines = [
    { sku: "pen", priceCents: 199, qty: 1 },
    { sku: "pad", priceCents: 350, qty: 1 },
  ];
  assert.strictEqual(totalCents(lines), 549);
});

test("multiplies price by quantity", () => {
  assert.strictEqual(totalCents([{ sku: "pen", priceCents: 199, qty: 3 }]), 597);
});
