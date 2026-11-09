function formatPercent(ratio) {
  return Math.round(ratio * 100) + "%";
}

function formatBytes(n) {
  return (n / 1000).toFixed(1) + " KB";
}

module.exports = { formatPercent, formatBytes };
