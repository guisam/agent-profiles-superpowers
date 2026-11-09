// lines: [{ sku, priceCents, qty }]
function totalCents(lines) {
  return lines.reduce((sum, line) => sum + line.priceCents, 0);
}

module.exports = { totalCents };
