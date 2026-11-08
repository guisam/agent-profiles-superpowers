import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const FILE = process.env.HABIT_FILE ?? join(homedir(), '.habit.json');

export function load() {
  return existsSync(FILE) ? JSON.parse(readFileSync(FILE, 'utf8')) : { habits: {} };
}

export function save(data) {
  writeFileSync(FILE, JSON.stringify(data, null, 2));
}
