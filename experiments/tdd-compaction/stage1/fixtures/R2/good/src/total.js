// lines: [{ sku, priceCents, qty }]
function totalCents(lines) {
  return lines.reduce((sum, line) => sum + line.priceCents * line.qty, 0);
}

module.exports = { totalCents };
