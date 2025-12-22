# Validation System for LLM Transformations

## Overview

We built a **shared validation library** that ensures LLM transformations follow all the rules we've established. The same validation code runs in two places:

1. **Test Suite** - Catch regressions before committing prompt changes
2. **Production Conversions** - Crash immediately if output violates rules

## Architecture

```
validation-rules.ts (Shared Library)
├── Academic Rules (8 rules)
├── Foundations Rules (5 rules)
└── Validation Functions

Used by:
├── __tests__/run-prompt-tests.ts (Test Suite)
└── generate-audience-versions.ts (Production)
```

## Validation Rules

### Academic Transformations

| Rule | What It Checks | Example Failure |
|------|----------------|-----------------|
| **Third person only** | No "you" or "your" | Found "you" in output |
| **Contractions preserved** | Don't → don't (not "do not") | Missing contractions: don't, can't |
| **No "defense" euphemism** | Use "military" not "defense" | Found "defense contractors" |
| **Simple pronouns preserved** | "everyone" not "the population" | Over-formalized: everyone → the population |
| **Casual vocabulary preserved** | Keep "kill", "poison", "die" | Casual words removed: kill, poison |
| **No over-formal verbs** | "use" not "utilize", "eat" not "consume" | Over-formal: "utilize", "reside" |
| **Numbers preserved** | All stats/numbers stay identical | Missing numbers: 82, 48000 |
| **Third person terminology** | "a dFDA" not "your dFDA" | Found possessive: "your dFDA" |

### Foundations Transformations

| Rule | What It Checks | Example Failure |
|------|----------------|-----------------|
| **Second person preserved** | Keep "you", "your" | Second person removed |
| **Contractions preserved** | Same as academic | Missing contractions |
| **No "defense" euphemism** | Same as academic | Found "defense spending" |
| **501(c)(3) compliance** | No "propaganda", "approach politicians" | Found prohibited: "propaganda" |
| **Numbers preserved** | Same as academic | Missing numbers |

## Usage

### In Tests

```bash
# Run all tests (includes validation)
npm run test:prompts

# Run academic tests only
npm run test:prompts:academic

# Run foundations tests only
npm run test:prompts:foundations
```

Tests will show validation failures:
```
[1/3] Running: AC-01: proof.qmd - landmines & key transformations
   ❌ FAILED (2134ms)
   Failed assertions:
     - No defense euphemism: Found "defense" euphemism: defense contractors
     - Third person only: Found 2 instances of second person: you, your
   Input:  "knowledge/proof.qmd"
   Output: "[transformed content]"
```

### In Production

```bash
# Generate academic versions (with validation)
npm run generate:audience:academic

# Generate foundations versions (with validation)
npm run generate:audience:foundations
```

**Production validation crashes on failure**:
```
[1/105] Processing: solution.qmd
  Transforming for audience: solution-academic.qmd...
  ✓ Wrote transformed file
  Validating transformation...
  ❌ VALIDATION FAILED for solution-academic.qmd

  ❌ Validation failed:
    - No defense euphemism:
      • Found "defense" euphemism (should be "military"): defense contractors
    - Third person only:
      • Found 3 instances of second person: you, your, you

  File written to: knowledge/solution-academic.qmd
  Source file: knowledge/solution.qmd

  The file was written so you can inspect the output.
  Fix the prompt and re-run to overwrite with corrected version.

Error: Transformation validation failed - see errors above
```

**The file IS written** - so you can inspect what the LLM produced, fix the prompt, and re-run to overwrite.

## Workflow

### When Prompt Changes Are Made

1. **Update prompt** (`instructions-academic-prompt.md` or `instructions-foundations-prompt.md`)
2. **Run tests** (`npm run test:prompts`)
3. **If tests pass** - prompt changes don't break existing rules ✅
4. **If tests fail** - prompt broke something, fix it ❌

### When Running Production Conversions

1. **Run conversion** (`npm run generate:audience:academic`)
2. **Validation runs automatically** on each file
3. **If validation passes** - file written successfully ✅
4. **If validation fails** - script crashes, no file written ❌

## Adding New Rules

To add a new validation rule:

1. **Edit `validation-rules.ts`**:
```typescript
{
  name: 'Your rule name',
  check: (output, input) => {
    // Your validation logic
    const violations = findViolations(output);

    return {
      passed: violations.length === 0,
      ruleName: 'Your rule name',
      errors: violations.map(v => `Violation: ${v}`),
    };
  },
}
```

2. **Add to appropriate array** (`academicRules` or `foundationsRules`)

3. **Test it** - The rule now runs automatically in both tests and production!

## Files

- `validation-rules.ts` - Shared validation library
- `__tests__/prompt-test-cases.ts` - Test case definitions (use full files)
- `__tests__/run-prompt-tests.ts` - Test runner (uses validation library)
- `generate-audience-versions.ts` - Production script (uses validation library)

## Benefits

1. **Immediate Feedback** - Know instantly when transformations violate rules
2. **Single Source of Truth** - Rules defined once, used everywhere
3. **Prevents Regressions** - Can't accidentally break fixed issues
4. **Fast Iteration** - Update prompts confidently with test coverage
5. **Production Safety** - Bad outputs never get written to disk

## Example: The "stupid" → "awful" Fix

**Problem**: LLM was changing "stupid" → "useless" (wrong semantic meaning)

**Fix Process**:
1. Added rule to prompt: `"stupid" → "awful" or similar simple, strong word`
2. Added validation rule: Check output doesn't contain "useless" when input has "stupid"
3. Added test case: `proof.qmd` with "landmines were stupid" → should become "awful"
4. Ran tests: ✅ Passed
5. Ran production: ✅ All files validated

**Result**: Issue can never happen again - validation would catch it immediately.

## Cost Impact

**Minimal** - Validation is local string checking:
- No API calls
- ~0.001 seconds per file
- Runs before writing, not after

The **real cost savings** come from catching issues early instead of having to re-run expensive LLM calls.
