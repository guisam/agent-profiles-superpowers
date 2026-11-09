function pad2(n) {
  return String(n).padStart(2, "0");
}

function formatDuration(total) {
  const units = [["h", 3600], ["m", 60], ["s", 1]];
  const out = [];
  let rest = total;
  for (const [label, size] of units) {
    const v = Math.floor(rest / size);
    rest -= v * size;
    if (v || out.length || label === "s") out.push(`${v}${label}`);
  }
  return out.join(" ");
}

module.exports = { pad2, formatDuration };
