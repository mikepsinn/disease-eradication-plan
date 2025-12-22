# LLM Prompt Regression Test Suite

This test suite validates that prompt changes don't break previously fixed issues. It uses a **shared validation library** that runs in both:
- **Test suite** - Catches regressions before committing
- **Conversion scripts** - Crashes immediately on validation failures during production runs

## Quick Start

```bash
# Run all tests (both academic and foundations)
npm run test:prompts

# Run only academic tests
npm run test:prompts:academic

# Run only foundations tests
npm run test:prompts:foundations
```

## What Gets Tested

### Academic Transformations

Tests verify that academic versions:
- ✅ Convert to third person correctly
- ✅ Replace "stupid" with "awful" (not "useless")
- ✅ Replace "defense" with "military"
- ✅ Preserve contractions (don't → don't, not "do not")
- ✅ Keep simple pronouns ("everyone", not "the population")
- ✅ Delete unfunny jokes after third-person conversion
- ✅ Keep casual vocabulary ("poison", "kill", not "harm", "terminate")
- ✅ Preserve all numbers and statistics
- ✅ Keep sentences similar length
- ✅ Use simple words ("use" not "utilize", "help" not "facilitate")

### Foundations Transformations

Tests verify that foundations versions:
- ✅ Keep second-person voice ("you", "your")
- ✅ Remove profanity appropriately
- ✅ Soften crude language
- ✅ Remove 501(c)(3) risks (propaganda → communications, etc.)
- ✅ Preserve humor and personality
- ✅ Keep vivid analogies
- ✅ Replace "defense" with "military"

## Architecture

### Shared Validation Library

**File**: `scripts/review/validation-rules.ts`

Contains all validation rules used by both:
1. **Test suite** (`run-prompt-tests.ts`) - Runs on test files
2. **Conversion script** (`generate-audience-versions.ts`) - Runs on every conversion

#### Academic Rules
- ✅ Third person only (no "you"/"your")
- ✅ Contractions preserved
- ✅ No "defense" euphemism (use "military")
- ✅ Simple pronouns preserved ("everyone" not "the population")
- ✅ Casual vocabulary preserved ("kill", "poison")
- ✅ No over-formal verbs ("use" not "utilize")
- ✅ Numbers preserved
- ✅ Third person terminology ("a dFDA" not "your dFDA")

#### Foundations Rules
- ✅ Second person preserved ("you", "your")
- ✅ Contractions preserved
- ✅ No "defense" euphemism
- ✅ 501(c)(3) compliance (no "propaganda", "approach politicians")
- ✅ Numbers preserved

### Validation in Production

When running conversions, validation happens **automatically**:

```bash
npm run generate:audience:academic
```

Output:
```
[1/105] Processing: solution.qmd
  Transforming for audience: solution-academic.qmd...
  Validating transformation...
  ✓ Validation passed (8 rules checked)
  ✓ Transformed complete file
```

**If validation fails**, the script **writes the file but crashes with errors**:
```
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

This ensures **you can inspect bad transformations** to understand what went wrong, then fix the prompt and re-run.

## Test Output

Example output:
```
================================================================================
🧪 Running ACADEMIC prompt tests
================================================================================

[1/12] Running: AC-01: Replace "stupid" with "awful"
   Moral judgments should stay moral judgments, not become factual claims
   ✅ PASSED (1243ms)

[2/12] Running: AC-02: Preserve contractions
   Modern academic writing allows contractions for accessibility
   ✅ PASSED (1156ms)

...

================================================================================
📊 ACADEMIC Test Summary
================================================================================
Total tests:  12
✅ Passed:    11 (91.7%)
❌ Failed:    1 (8.3%)
⏱️  Total time: 14.52s
💰 Est. cost:  $0.0150 USD
================================================================================
```

## Test Report

After each run, a detailed JSON report is saved to:
```
scripts/review/__tests__/test-report.json
```

This includes:
- Timestamp
- Pass/fail counts
- Failed test details
- Actual outputs vs expected
- Cost estimates

## Adding New Tests

Edit `prompt-test-cases.ts`:

```typescript
{
  name: 'AC-13: Your test name',
  description: 'What this test verifies',
  input: 'Input text to transform',
  expectedOutput: 'Exact expected output (optional)',
  assertions: [
    assertions.includes('expected phrase'),
    assertions.notIncludes('unwanted phrase'),
    // Custom assertion:
    {
      name: 'custom check',
      check: (output, input) => output.includes('something'),
      errorMessage: 'Expected something',
    },
  ],
  audience: 'academic', // or 'foundations' or 'both'
}
```

### Reusable Assertions

The test suite provides helpers:

```typescript
assertions.includes('text')           // Output must include text
assertions.notIncludes('text')        // Output must not include text
assertions.preservesContractions()    // All contractions from input preserved
assertions.notLongerThan(20)          // Output max 20 chars longer than input
assertions.thirdPersonOnly()          // No "you" or "your"
assertions.preservesNumbers()         // All numbers from input in output
```

## Cost Estimates

- **Gemini Pro pricing**: $1.25/1M input tokens, $5.00/1M output tokens
- **Avg cost per test**: ~$0.0012 USD
- **Full suite (20 tests)**: ~$0.024 USD

Running tests frequently is cheap! Don't hesitate to run them often.

## Best Practices

1. **Add a test for every bug fix** - If you fix a prompt issue, add a test case
2. **Run tests before committing** - Ensure your changes don't break existing fixes
3. **Keep test inputs short** - Focused tests are faster and cheaper
4. **Use assertions over exact matches** - More flexible as prompts evolve
5. **Document the "why"** - Use descriptive names and descriptions

## Continuous Integration

To add to CI/CD:

```yaml
# .github/workflows/test-prompts.yml
name: Test LLM Prompts
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install
      - run: npm run test:prompts
        env:
          GOOGLE_GENERATIVE_AI_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

## Files

- `prompt-test-cases.ts` - Test case definitions
- `run-prompt-tests.ts` - Test runner
- `test-report.json` - Latest test results (gitignored)
- `README.md` - This file

## Troubleshooting

**Tests failing after prompt changes?**
- Review the failed assertion details
- Check if the change was intentional
- Update test expectations if needed

**Slow test runs?**
- Tests run sequentially to avoid rate limits
- Consider running specific audiences only
- Each test ~1-2 seconds

**API errors?**
- Check GOOGLE_GENERATIVE_AI_API_KEY is set
- Verify API key has Gemini Pro access
- Check for rate limiting

## Future Improvements

- [ ] Parallel test execution (with rate limiting)
- [ ] Caching test results for unchanged prompts
- [ ] Semantic similarity metrics (not just exact matches)
- [ ] Visual diff tool for test failures
- [ ] Test coverage reporting
- [ ] Benchmark suite for performance regression
