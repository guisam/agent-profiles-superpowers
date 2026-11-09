// coupon: { type: "percent", value } or { type: "fixed", valueCents }
function applyCoupon(totalCents, coupon) {
  if (!coupon) return totalCents;
  if (coupon.type === "fixed") return Math.max(0, totalCents - coupon.valueCents);
  if (coupon.type === "percent") return totalCents - coupon.value;
  return totalCents;
}

module.exports = { applyCoupon };
