// Format a ratio (0..1) as a whole percentage.
function formatPercent(ratio) {
  return Math.round(ratio * 100) + "%";
}

module.exports = { formatPercent };
