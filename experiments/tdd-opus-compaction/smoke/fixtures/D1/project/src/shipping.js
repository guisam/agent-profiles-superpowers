// Orders of 5000 cents or more ship free.
function shippingCents(totalCents) {
  return totalCents >= 5000 ? 0 : 499;
}

module.exports = { shippingCents };
