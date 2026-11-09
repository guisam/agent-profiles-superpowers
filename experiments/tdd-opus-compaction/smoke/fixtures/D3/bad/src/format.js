// Zero-pad to two digits: 5 -> "05".
function pad2(n) {
  return String(n).padStart(2, "0");
}

function formatDuration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  return `${h}:${pad2(m)}:${pad2(seconds % 60)}`;
}

module.exports = { pad2, formatDuration };
