// Zero-pad to two digits: 5 -> "05".
function pad2(n) {
  return String(n).padStart(2, "0");
}

// 3723 -> "1h 2m 3s", 125 -> "2m 5s", 45 -> "45s"
function formatDuration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  const parts = [];
  if (h) parts.push(h + "h");
  if (m || h) parts.push(m + "m");
  parts.push(s + "s");
  return parts.join(" ");
}

module.exports = { pad2, formatDuration };
