import assert from 'node:assert/strict';

import {
  classifyParameterUsage,
  extractParameterNames,
  findDependentsInSource,
} from '../parameter-audit';

const source = `
BASE_INPUT = Parameter(
  2,
  unit="USD",
)

DERIVED_VALUE = Parameter(
  BASE_INPUT * 3,
  unit="USD",
  inputs=["BASE_INPUT"],
  compute=lambda ctx: ctx["BASE_INPUT"] * 3,
)

ALIAS_VALUE = DERIVED_VALUE

UNUSED_VALUE = Parameter(
  5,
  unit="USD",
)
`;

assert.deepEqual([...extractParameterNames(source)].sort(), [
  'ALIAS_VALUE',
  'BASE_INPUT',
  'DERIVED_VALUE',
  'UNUSED_VALUE',
]);

const allParams = extractParameterNames(source);
const dependents = findDependentsInSource(source, allParams);
const result = classifyParameterUsage({
  allParams,
  dependents,
  qmdRefs: new Map(),
  scriptRefs: new Map(),
  codeRefs: new Map(),
});

assert.deepEqual(result.unused, ['ALIAS_VALUE', 'UNUSED_VALUE']);
assert.deepEqual(result.intermediate.map(item => item.name).sort(), [
  'BASE_INPUT',
  'DERIVED_VALUE',
]);
assert.deepEqual(
  result.intermediate.find(item => item.name === 'BASE_INPUT')?.deps,
  ['DERIVED_VALUE'],
);
assert.deepEqual(
  result.intermediate.find(item => item.name === 'DERIVED_VALUE')?.deps,
  ['ALIAS_VALUE'],
);

console.log('parameter-audit regression passed');
