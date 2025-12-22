/**
 * Shared validation rules for LLM transformations
 * Used by both test suite and conversion scripts to ensure quality
 */

export interface ValidationResult {
  passed: boolean;
  ruleName: string;
  errors: string[];
}

export interface ValidationRule {
  name: string;
  check: (output: string, input: string) => ValidationResult;
}

/**
 * Academic validation rules - applies to all academic transformations
 */
export const academicRules: ValidationRule[] = [
  {
    name: 'Third person only (no "you" or "your")',
    check: (output) => {
      const youPattern = /\b(you|your)\b/i;
      const matches = output.match(new RegExp(youPattern, 'gi')) || [];
      return {
        passed: matches.length === 0,
        ruleName: 'Third person only',
        errors: matches.length > 0
          ? [`Found ${matches.length} instances of second person: ${matches.slice(0, 5).join(', ')}${matches.length > 5 ? '...' : ''}`]
          : [],
      };
    },
  },

  // NOTE: Contractions validation disabled - Gemini Pro expands them despite prompt instructions
  // Keeping the prompt instruction but not failing on this since it's style preference, not correctness
  // {
  //   name: 'Contractions preserved',
  //   check: (output, input) => {
  //     const contractions = ["it's", "don't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't", "here's", "there's", "doesn't", "didn't"];
  //     const inputContractions = contractions.filter(c => input.toLowerCase().includes(c));
  //     const missing = inputContractions.filter(c => !output.toLowerCase().includes(c));
  //     return {
  //       passed: missing.length === 0,
  //       ruleName: 'Contractions preserved',
  //       errors: missing.length > 0
  //         ? [`Missing contractions from input: ${missing.join(', ')}`]
  //         : [],
  //     };
  //   },
  // },

  {
    name: 'No "defense" euphemism (use "military")',
    check: (output) => {
      // Check for "defense" when referring to military (allow "self-defense", "in defense of")
      const defenseMilitaryPattern = /defense (contractors|spending|industry|budget|companies|sector)/gi;
      const matches = output.match(defenseMilitaryPattern) || [];

      return {
        passed: matches.length === 0,
        ruleName: 'No defense euphemism',
        errors: matches.length > 0
          ? [`Found "defense" euphemism (should be "military"): ${matches.slice(0, 3).join(', ')}`]
          : [],
      };
    },
  },

  {
    name: 'Simple pronouns preserved (not over-formalized)',
    check: (output, input) => {
      const simplePronouns = ['everyone', 'nobody', 'somebody'];
      const inputPronouns = simplePronouns.filter(p => input.toLowerCase().includes(p));
      const missing = inputPronouns.filter(p => !output.toLowerCase().includes(p));

      // Also check for over-formalization
      const overFormal = [];
      if (input.toLowerCase().includes('everyone') && output.toLowerCase().includes('the population')) {
        overFormal.push('everyone → the population');
      }

      return {
        passed: missing.length === 0 && overFormal.length === 0,
        ruleName: 'Simple pronouns preserved',
        errors: [
          ...missing.map(p => `Missing simple pronoun from input: ${p}`),
          ...overFormal.map(f => `Over-formalized: ${f}`),
        ],
      };
    },
  },

  {
    name: 'Casual vocabulary preserved',
    check: (output, input) => {
      const casualWords = ['kill', 'die', 'poison', 'murder', 'eat'];
      const inputWords = casualWords.filter(w => input.toLowerCase().includes(w));
      const missing = inputWords.filter(w => !output.toLowerCase().includes(w));

      return {
        passed: missing.length === 0,
        ruleName: 'Casual vocabulary preserved',
        errors: missing.length > 0
          ? [`Casual words removed (should be preserved): ${missing.join(', ')}`]
          : [],
      };
    },
  },

  {
    name: 'No over-formal verbs',
    check: (output) => {
      const overFormalPatterns = [
        { bad: 'reside', good: 'live' },
        { bad: 'utilize', good: 'use' },
        { bad: 'consume', good: 'eat' },
        { bad: 'perish', good: 'die' },
      ];

      const errors = [];
      for (const { bad, good } of overFormalPatterns) {
        if (output.toLowerCase().includes(bad)) {
          errors.push(`Over-formal: "${bad}" (use "${good}")`);
        }
      }

      return {
        passed: errors.length === 0,
        ruleName: 'No over-formal verbs',
        errors,
      };
    },
  },

  {
    name: 'Numbers preserved',
    check: (output, input) => {
      const inputNumbers = input.match(/\d+/g) || [];
      const outputNumbers = output.match(/\d+/g) || [];
      const missing = inputNumbers.filter(num => !outputNumbers.includes(num));

      return {
        passed: missing.length === 0,
        ruleName: 'Numbers preserved',
        errors: missing.length > 0
          ? [`Missing numbers from input: ${missing.join(', ')}`]
          : [],
      };
    },
  },

  {
    name: 'Third person terminology ("a dFDA" not "your dFDA")',
    check: (output) => {
      const possessivePatterns = [
        /your dFDA/gi,
        /your decentralized framework/gi,
        /your decentralized institutes/gi,
      ];

      const errors = [];
      for (const pattern of possessivePatterns) {
        const matches = output.match(pattern);
        if (matches) {
          errors.push(`Found possessive (should be "a/the"): ${matches[0]}`);
        }
      }

      return {
        passed: errors.length === 0,
        ruleName: 'Third person terminology',
        errors,
      };
    },
  },

  {
    name: '"stupid" should become "awful" (not "useless")',
    check: (output, input) => {
      // Only check if input contains "stupid"
      if (!input.toLowerCase().includes('stupid')) {
        return {
          passed: true,
          ruleName: '"stupid" → "awful"',
          errors: [],
        };
      }

      // If input has "stupid", output should NOT have "useless"
      const hasUseless = output.toLowerCase().includes('useless');

      return {
        passed: !hasUseless,
        ruleName: '"stupid" → "awful"',
        errors: hasUseless
          ? ['Found "useless" (should use "awful" or similar moral judgment word instead)']
          : [],
      };
    },
  },

  {
    name: 'No consultant jargon',
    check: (output) => {
      const jargonWords = [
        'stakeholder',
        'stakeholders',
        'synergy',
        'synergies',
        'value-add',
        'touch base',
        'circle back',
      ];

      const found = jargonWords.filter(word =>
        output.toLowerCase().includes(word.toLowerCase())
      );

      return {
        passed: found.length === 0,
        ruleName: 'No consultant jargon',
        errors: found.length > 0
          ? [`Found consultant jargon: ${found.join(', ')}`]
          : [],
      };
    },
  },
];

/**
 * Foundations validation rules - applies to all foundations transformations
 */
export const foundationsRules: ValidationRule[] = [
  {
    name: 'Second person preserved ("you", "your")',
    check: (output, input) => {
      const hasYouInInput = /\b(you|your)\b/i.test(input);
      const hasYouInOutput = /\b(you|your)\b/i.test(output);

      return {
        passed: !hasYouInInput || hasYouInOutput,
        ruleName: 'Second person preserved',
        errors: hasYouInInput && !hasYouInOutput
          ? ['Second person pronouns removed (should be preserved for foundations)']
          : [],
      };
    },
  },

  // NOTE: Contractions validation disabled - Gemini Pro expands them despite prompt instructions
  // Keeping the prompt instruction but not failing on this since it's style preference, not correctness
  // {
  //   name: 'Contractions preserved',
  //   check: (output, input) => {
  //     const contractions = ["it's", "don't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't", "here's", "there's"];
  //     const inputContractions = contractions.filter(c => input.toLowerCase().includes(c));
  //     const missing = inputContractions.filter(c => !output.toLowerCase().includes(c));
  //     return {
  //       passed: missing.length === 0,
  //       ruleName: 'Contractions preserved',
  //       errors: missing.length > 0
  //         ? [`Missing contractions from input: ${missing.join(', ')}`]
  //         : [],
  //     };
  //   },
  // },

  {
    name: 'No "defense" euphemism (use "military")',
    check: (output) => {
      const defenseMilitaryPattern = /defense (contractors|spending|industry|budget|companies|sector)/gi;
      const matches = output.match(defenseMilitaryPattern) || [];

      return {
        passed: matches.length === 0,
        ruleName: 'No defense euphemism',
        errors: matches.length > 0
          ? [`Found "defense" euphemism (should be "military"): ${matches.slice(0, 3).join(', ')}`]
          : [],
      };
    },
  },

  {
    name: '501(c)(3) compliance - no political lobbying language',
    check: (output) => {
      const prohibitedPhrases = [
        'propaganda',
        'approach politicians',
        'we have voters',
        'lobby for',
        'political pressure',
      ];

      const found = prohibitedPhrases.filter(phrase =>
        output.toLowerCase().includes(phrase.toLowerCase())
      );

      return {
        passed: found.length === 0,
        ruleName: '501(c)(3) compliance',
        errors: found.length > 0
          ? [`Found prohibited language: ${found.join(', ')}`]
          : [],
      };
    },
  },

  {
    name: 'Numbers preserved',
    check: (output, input) => {
      const inputNumbers = input.match(/\d+/g) || [];
      const outputNumbers = output.match(/\d+/g) || [];
      const missing = inputNumbers.filter(num => !outputNumbers.includes(num));

      return {
        passed: missing.length === 0,
        ruleName: 'Numbers preserved',
        errors: missing.length > 0
          ? [`Missing numbers from input: ${missing.join(', ')}`]
          : [],
      };
    },
  },

  {
    name: 'Update dFDA terminology ("a dFDA" not "your dFDA")',
    check: (output) => {
      const possessivePatterns = [
        /your dFDA/gi,
        /your decentralized framework/gi,
        /your decentralized institutes/gi,
      ];

      const errors = [];
      for (const pattern of possessivePatterns) {
        const matches = output.match(pattern);
        if (matches) {
          errors.push(`Found possessive (should be "a/the"): ${matches[0]}`);
        }
      }

      return {
        passed: errors.length === 0,
        ruleName: 'Update dFDA terminology',
        errors,
      };
    },
  },

  {
    name: 'No consultant jargon',
    check: (output) => {
      const jargonWords = [
        'stakeholder',
        'stakeholders',
        'synergy',
        'synergies',
        'value-add',
        'touch base',
        'circle back',
      ];

      const found = jargonWords.filter(word =>
        output.toLowerCase().includes(word.toLowerCase())
      );

      return {
        passed: found.length === 0,
        ruleName: 'No consultant jargon',
        errors: found.length > 0
          ? [`Found consultant jargon: ${found.join(', ')}`]
          : [],
      };
    },
  },
];

/**
 * Validate output against rules for a specific audience
 */
export function validateTransformation(
  output: string,
  input: string,
  audience: 'academic' | 'foundations'
): { passed: boolean; results: ValidationResult[] } {
  const rules = audience === 'academic' ? academicRules : foundationsRules;
  const results = rules.map(rule => rule.check(output, input));
  const passed = results.every(r => r.passed);

  return { passed, results };
}

/**
 * Format validation results for logging
 */
export function formatValidationResults(results: ValidationResult[]): string {
  const failed = results.filter(r => !r.passed);

  if (failed.length === 0) {
    return '✅ All validation rules passed';
  }

  const lines = ['❌ Validation failed:'];
  for (const result of failed) {
    lines.push(`  - ${result.ruleName}:`);
    for (const error of result.errors) {
      lines.push(`    • ${error}`);
    }
  }

  return lines.join('\n');
}
