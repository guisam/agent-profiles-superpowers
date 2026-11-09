// coupon: { type: "percent", value } or { type: "fixed", valueCents }
function applyCoupon(totalCents, coupon) {
  if (!coupon) return totalCents;
  if (coupon.type === "fixed") return Math.max(0, totalCents - coupon.valueCents);
  if (coupon.type === "percent") return totalCents - Math.round((totalCents * coupon.value) / 100);
  return totalCents;
}

module.exports = { applyCoupon };
