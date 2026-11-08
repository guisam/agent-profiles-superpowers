import test from 'node:test';
import assert from 'node:assert/strict';
import { streak } from './streak.js';

test('counts consecutive days ending today', () => {
  assert.equal(streak(['2026-11-05', '2026-11-06', '2026-11-07'], '2026-11-07'), 3);
});

test('zero when today is missing', () => {
  assert.equal(streak(['2026-11-06'], '2026-11-07'), 0);
});
