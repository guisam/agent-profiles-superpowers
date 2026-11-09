// Zero-pad to two digits: 5 -> "05".
function pad2(n) {
  return String(n).padStart(2, "0");
}

module.exports = { pad2 };
