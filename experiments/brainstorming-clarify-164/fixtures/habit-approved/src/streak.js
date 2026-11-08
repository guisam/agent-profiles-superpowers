// days: sorted ISO dates (YYYY-MM-DD) on which the habit was done
export function streak(days, today) {
  let count = 0;
  const d = new Date(today + 'T00:00:00Z');
  while (days.includes(d.toISOString().slice(0, 10))) {
    count++;
    d.setUTCDate(d.getUTCDate() - 1);
  }
  return count;
}
