/**
 * Regression test cases for LLM prompt transformations
 * Each test case represents a previously fixed issue or core transformation rule
 */

export interface TestCase {
  name: string;
  description: string;
  input?: string; // For snippet tests
  inputFile?: string; // For file tests (relative to knowledge/)
  expectedOutput?: string; // Exact match expected
  expectedPhrases?: string[]; // Must include these
  blacklistedPhrases?: string[]; // Must NOT include these
  assertions: TestAssertion[];
  audience: 'academic' | 'foundations' | 'both';
  isIntegrationTest?: boolean; // Full file test
  maxCostUSD?: number; // Skip if over budget
}

export interface TestAssertion {
  name: string;
  check: (output: string, input: string) => boolean;
  errorMessage?: string;
}

// Reusable assertion helpers
export const assertions = {
  includes: (substring: string): TestAssertion => ({
    name: `includes "${substring}"`,
    check: (output) => output.includes(substring),
    errorMessage: `Expected output to include "${substring}"`,
  }),

  notIncludes: (substring: string): TestAssertion => ({
    name: `does not include "${substring}"`,
    check: (output) => !output.includes(substring),
    errorMessage: `Expected output to NOT include "${substring}"`,
  }),

  preservesContractions: (): TestAssertion => ({
    name: 'preserves contractions',
    check: (output, input) => {
      const contractions = ["it's", "don't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't", "here's", "there's"];
      const inputContractions = contractions.filter(c => input.toLowerCase().includes(c));
      return inputContractions.every(c => output.toLowerCase().includes(c));
    },
    errorMessage: 'Contractions should be preserved, not expanded',
  }),

  notLongerThan: (maxExtraChars: number): TestAssertion => ({
    name: `not significantly longer than input (max +${maxExtraChars} chars)`,
    check: (output, input) => output.length <= input.length + maxExtraChars,
    errorMessage: `Output should not be significantly longer than input`,
  }),

  thirdPersonOnly: (): TestAssertion => ({
    name: 'uses third person (no "you" or "your")',
    check: (output) => {
      // Allow "you" in quotes or as part of other words
      const youPattern = /\b(you|your)\b/i;
      return !youPattern.test(output);
    },
    errorMessage: 'Academic version should use third person only',
  }),

  preservesNumbers: (): TestAssertion => ({
    name: 'preserves all numbers and statistics',
    check: (output, input) => {
      const inputNumbers = input.match(/\d+/g) || [];
      const outputNumbers = output.match(/\d+/g) || [];
      return inputNumbers.every(num => outputNumbers.includes(num));
    },
    errorMessage: 'All numbers from input should appear in output',
  }),

  includesAllPhrases: (phrases: string[]): TestAssertion => ({
    name: `includes all expected phrases (${phrases.length} phrases)`,
    check: (output) => phrases.every(phrase => output.includes(phrase)),
    errorMessage: `Missing expected phrases`,
  }),

  excludesAllPhrases: (phrases: string[]): TestAssertion => ({
    name: `excludes all blacklisted phrases (${phrases.length} phrases)`,
    check: (output) => phrases.every(phrase => !output.includes(phrase)),
    errorMessage: `Contains blacklisted phrases`,
  }),
};

// Test cases for ACADEMIC transformations
// All tests use full files from knowledge/ directory
export const academicTestCases: TestCase[] = [
  {
    name: 'AC-01: proof.qmd - landmines & key transformations',
    description: 'Test "stupid" → "awful", "defense" → "military", contractions, third person',
    inputFile: 'proof.qmd',
    expectedPhrases: [
      'awful',  // "stupid" → "awful"
      'military',  // "defense" → "military"
      "don't",  // Contractions preserved
      "can't",
      "won't",
      'everyone',  // Simple pronouns
      'kill',  // Casual vocabulary
      'die',
    ],
    blacklistedPhrases: [
      'landmines were stupid',  // Should be "awful"
      'landmines were useless',  // Bad previous output
      'defense contractors',  // Should be "military"
      'defense spending',
      'defense industry',
      'do not',  // No expanded contractions
      'cannot',
      'will not',
      'the population',  // No over-formalization
      'individuals',
      'utilize',
      'reside',
      'consume',
      'perish',
      '\byou\b',  // No second person (word boundary to avoid "your" matches in compound words)
      '\byour\b',
    ],
    assertions: [
      assertions.includes('awful'),
      assertions.notIncludes('stupid'),
      assertions.notIncludes('useless'),
      assertions.preservesNumbers(),
      assertions.preservesContractions(),
      assertions.thirdPersonOnly(),
      assertions.includesAllPhrases(['awful', 'military']),
      assertions.excludesAllPhrases([
        'stupid',
        'useless',
        'defense contractors',
        'defense spending',
        'the population',
      ]),
    ],
    audience: 'academic',
    isIntegrationTest: true,
    maxCostUSD: 0.10,
  },

  {
    name: 'AC-02: solution.qmd - comprehensive transformations',
    description: 'Test "defense" → "military", "your dFDA" → "a dFDA", joke deletion, third person',
    inputFile: 'solution.qmd',
    expectedPhrases: [
      'military contractors',
      'military spending',
      'a dFDA',
      'a decentralized',
      "don't",  // Contractions
      "can't",
      "isn't",
      'everyone',
      'nobody',
      'kill',
      'poison',
      'murder',
      'die',
      'eat',
    ],
    blacklistedPhrases: [
      'defense contractors',
      'defense spending',
      'defense industry',
      'your dFDA',
      'your decentralized framework',
      'do not',  // No expanded contractions
      'cannot',
      'is not',
      'the population',
      'reside',
      'utilize',
      'consume',
      'perish',
      'One general was asked',  // Unfunny joke should be deleted
      'He stopped talking',
    ],
    assertions: [
      assertions.thirdPersonOnly(),
      assertions.preservesNumbers(),
      assertions.preservesContractions(),
      assertions.includesAllPhrases([
        'military contractors',
        'military spending',
        'a dFDA',
        'everyone',
      ]),
      assertions.excludesAllPhrases([
        'defense contractors',
        'defense spending',
        'your dFDA',
        'the population',
        'One general was asked',  // Unfunny joke
      ]),
    ],
    audience: 'academic',
    isIntegrationTest: true,
    maxCostUSD: 0.15,
  },
];

// Test cases for FOUNDATIONS transformations
// All tests use full files from knowledge/ directory
export const foundationsTestCases: TestCase[] = [
  {
    name: 'FO-01: solution.qmd - keep personality & second person',
    description: 'Test second person preserved, "defense" → "military", contractions kept, 501(c)(3) compliance',
    inputFile: 'solution.qmd',
    expectedPhrases: [
      'you',  // Keep second person
      'your',
      'military contractors',
      'military spending',
      "don't",  // Contractions
      "can't",
      'everyone',
      'kill',
      'poison',
    ],
    blacklistedPhrases: [
      'defense contractors',
      'defense spending',
      'defense industry',
      'propaganda',  // 501(c)(3) risk
      'approach politicians',
      'we have voters',
      'lies',
      'fabricated',
      'do not',  // No expanded contractions
      'cannot',
      'the population',
      'reside',
      'utilize',
    ],
    assertions: [
      assertions.includes('you'),
      assertions.includes('your'),
      assertions.preservesNumbers(),
      assertions.preservesContractions(),
      assertions.includesAllPhrases([
        'military contractors',
        'everyone',
      ]),
      assertions.excludesAllPhrases([
        'defense contractors',
        'propaganda',
        'approach politicians',
        'the population',
      ]),
    ],
    audience: 'foundations',
    isIntegrationTest: true,
    maxCostUSD: 0.15,
  },
];

// Combined test cases for running both audiences
export const allTestCases = {
  academic: academicTestCases.filter(tc => tc.audience === 'academic' || tc.audience === 'both'),
  foundations: foundationsTestCases.filter(tc => tc.audience === 'foundations' || tc.audience === 'both'),
};
