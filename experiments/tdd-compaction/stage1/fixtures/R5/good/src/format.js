// Format a ratio (0..1) as a whole percentage.
function formatPercent(ratio) {
  return Math.round(ratio * 100) + "%";
}

function formatBytes(n) {
  const units = ["B", "KB", "MB", "GB"];
  let i = 0;
  while (n >= 1024 && i < units.length - 1) {
    n /= 1024;
    i++;
  }
  return n.toFixed(1) + " " + units[i];
}

module.exports = { formatPercent, formatBytes };
