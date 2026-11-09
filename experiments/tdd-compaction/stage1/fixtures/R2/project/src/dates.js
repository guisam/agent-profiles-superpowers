// Whole days from a to b (ISO dates, YYYY-MM-DD).
function daysBetween(a, b) {
  const ms = Date.parse(b + "T00:00:00Z") - Date.parse(a + "T00:00:00Z");
  return Math.round(ms / 86400000) + 1;
}

module.exports = { daysBetween };
