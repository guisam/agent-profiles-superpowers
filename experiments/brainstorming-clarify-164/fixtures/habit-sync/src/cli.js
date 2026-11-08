#!/usr/bin/env node
import { load, save } from './store.js';
import { streak } from './streak.js';

const [cmd, name] = process.argv.slice(2);
const today = new Date().toISOString().slice(0, 10);
const data = load();

if (cmd === 'add' && name) {
  data.habits[name] ??= [];
  save(data);
} else if (cmd === 'done' && name && data.habits[name]) {
  if (!data.habits[name].includes(today)) data.habits[name].push(today);
  save(data);
} else if (cmd === 'list') {
  for (const [habit, days] of Object.entries(data.habits)) {
    console.log(`${habit}: ${streak(days, today)} day streak`);
  }
} else {
  console.log('usage: habit add|done|list <name>');
  process.exitCode = 1;
}
