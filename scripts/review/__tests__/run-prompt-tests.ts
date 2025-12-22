/**
 * Test runner for LLM prompt regression tests
 *
 * Usage:
 *   npm run test:prompts               # Run all tests
 *   npm run test:prompts academic      # Run only academic tests
 *   npm run test:prompts foundations   # Run only foundations tests
 */

import { generateGeminiProContent } from '../../lib/llm';
import { validateTransformation, formatValidationResults } from '../validation-rules';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { allTestCases, TestCase, TestAssertion } from './prompt-test-cases';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

interface TestResult {
  testCase: TestCase;
  output: string;
  passed: boolean;
  failedAssertions: Array<{
    assertion: TestAssertion;
    error: string;
  }>;
  executionTime: number;
}

interface TestSummary {
  audience: 'academic' | 'foundations';
  totalTests: number;
  passed: number;
  failed: number;
  results: TestResult[];
  totalTime: number;
  totalCost: number;
}

async function loadPromptInstructions(audience: 'academic' | 'foundations'): Promise<string> {
  const filename = audience === 'academic'
    ? 'instructions-academic-prompt.md'
    : 'instructions-foundations-prompt.md';

  const promptPath = path.join(__dirname, '..', filename);
  return await fs.readFile(promptPath, 'utf-8');
}

async function loadTestInput(testCase: TestCase): Promise<string> {
  if (testCase.input) {
    return testCase.input;
  }

  if (testCase.inputFile) {
    const filePath = path.join(__dirname, '..', '..', '..', 'knowledge', testCase.inputFile);
    return await fs.readFile(filePath, 'utf-8');
  }

  throw new Error('TestCase must have either input or inputFile');
}

async function runTestCase(
  testCase: TestCase,
  promptInstructions: string
): Promise<TestResult> {
  const startTime = Date.now();

  const input = await loadTestInput(testCase);

  const prompt = `${promptInstructions}

Now apply these transformations to the following text:

${input}

Return ONLY the transformed text, nothing else.`;

  try {
    const output = await generateGeminiProContent(prompt);
    const executionTime = Date.now() - startTime;

    // Run validation library checks FIRST
    const validation = validateTransformation(output, input, testCase.audience as 'academic' | 'foundations');
    const failedAssertions: TestResult['failedAssertions'] = [];

    // Add validation failures to assertions
    for (const validationResult of validation.results) {
      if (!validationResult.passed) {
        failedAssertions.push({
          assertion: {
            name: validationResult.ruleName,
            check: () => false,
          },
          error: validationResult.errors.join('; '),
        });
      }
    }

    // Check custom test-specific assertions
    for (const assertion of testCase.assertions) {
      try {
        const passed = assertion.check(output, input);
        if (!passed) {
          failedAssertions.push({
            assertion,
            error: assertion.errorMessage || `Assertion "${assertion.name}" failed`,
          });
        }
      } catch (error) {
        failedAssertions.push({
          assertion,
          error: `Assertion threw error: ${error}`,
        });
      }
    }

    // Check exact match if provided
    if (testCase.expectedOutput) {
      const exactMatch = output.trim() === testCase.expectedOutput.trim();
      if (!exactMatch) {
        failedAssertions.push({
          assertion: { name: 'exact match', check: () => false },
          error: `Expected exact output:\n"${testCase.expectedOutput}"\n\nGot:\n"${output}"`,
        });
      }
    }

    return {
      testCase,
      output,
      passed: failedAssertions.length === 0,
      failedAssertions,
      executionTime,
    };
  } catch (error) {
    return {
      testCase,
      output: '',
      passed: false,
      failedAssertions: [{
        assertion: { name: 'execution', check: () => false },
        error: `Test execution failed: ${error}`,
      }],
      executionTime: Date.now() - startTime,
    };
  }
}

async function runTestSuite(audience: 'academic' | 'foundations'): Promise<TestSummary> {
  console.log(`\n${'='.repeat(80)}`);
  console.log(`🧪 Running ${audience.toUpperCase()} prompt tests`);
  console.log('='.repeat(80));

  const testCases = allTestCases[audience];
  const promptInstructions = await loadPromptInstructions(audience);

  const startTime = Date.now();
  const results: TestResult[] = [];

  for (let i = 0; i < testCases.length; i++) {
    const testCase = testCases[i];
    console.log(`\n[${i + 1}/${testCases.length}] Running: ${testCase.name}`);
    console.log(`   ${testCase.description}`);

    const result = await runTestCase(testCase, promptInstructions);
    results.push(result);

    if (result.passed) {
      console.log(`   ✅ PASSED (${result.executionTime}ms)`);
    } else {
      console.log(`   ❌ FAILED (${result.executionTime}ms)`);
      console.log(`   Failed assertions:`);
      for (const failure of result.failedAssertions) {
        console.log(`     - ${failure.assertion.name}: ${failure.error}`);
      }
      console.log(`   Input:  "${testCase.input}"`);
      console.log(`   Output: "${result.output}"`);
    }
  }

  const totalTime = Date.now() - startTime;
  const passed = results.filter(r => r.passed).length;
  const failed = results.filter(r => !r.passed).length;

  // Rough cost estimate (Gemini Pro: $1.25/1M input, $5.00/1M output)
  const avgInputTokens = 800; // Approximate
  const avgOutputTokens = 50; // Approximate
  const costPerTest = (avgInputTokens / 1_000_000 * 1.25) + (avgOutputTokens / 1_000_000 * 5.00);
  const totalCost = costPerTest * testCases.length;

  return {
    audience,
    totalTests: testCases.length,
    passed,
    failed,
    results,
    totalTime,
    totalCost,
  };
}

function printSummary(summary: TestSummary) {
  console.log(`\n${'='.repeat(80)}`);
  console.log(`📊 ${summary.audience.toUpperCase()} Test Summary`);
  console.log('='.repeat(80));
  console.log(`Total tests:  ${summary.totalTests}`);
  console.log(`✅ Passed:    ${summary.passed} (${(summary.passed / summary.totalTests * 100).toFixed(1)}%)`);
  console.log(`❌ Failed:    ${summary.failed} (${(summary.failed / summary.totalTests * 100).toFixed(1)}%)`);
  console.log(`⏱️  Total time: ${(summary.totalTime / 1000).toFixed(2)}s`);
  console.log(`💰 Est. cost:  $${summary.totalCost.toFixed(4)} USD`);
  console.log('='.repeat(80));

  if (summary.failed > 0) {
    console.log(`\n❌ Failed tests:`);
    summary.results
      .filter(r => !r.passed)
      .forEach(r => {
        console.log(`   - ${r.testCase.name}`);
      });
  }
}

async function saveTestReport(summaries: TestSummary[]) {
  const report = {
    timestamp: new Date().toISOString(),
    summaries: summaries.map(s => ({
      audience: s.audience,
      totalTests: s.totalTests,
      passed: s.passed,
      failed: s.failed,
      totalTime: s.totalTime,
      totalCost: s.totalCost,
      failedTests: s.results
        .filter(r => !r.passed)
        .map(r => ({
          name: r.testCase.name,
          description: r.testCase.description,
          input: r.testCase.input,
          output: r.output,
          failedAssertions: r.failedAssertions.map(fa => ({
            name: fa.assertion.name,
            error: fa.error,
          })),
        })),
    })),
  };

  const reportPath = path.join(__dirname, 'test-report.json');
  await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
  console.log(`\n📄 Test report saved to: ${reportPath}`);
}

async function main() {
  const args = process.argv.slice(2);
  const audienceArg = args[0] as 'academic' | 'foundations' | undefined;

  const summaries: TestSummary[] = [];

  if (!audienceArg || audienceArg === 'academic') {
    const summary = await runTestSuite('academic');
    printSummary(summary);
    summaries.push(summary);
  }

  if (!audienceArg || audienceArg === 'foundations') {
    const summary = await runTestSuite('foundations');
    printSummary(summary);
    summaries.push(summary);
  }

  await saveTestReport(summaries);

  // Exit with error code if any tests failed
  const totalFailed = summaries.reduce((sum, s) => sum + s.failed, 0);
  if (totalFailed > 0) {
    console.log(`\n❌ ${totalFailed} test(s) failed`);
    process.exit(1);
  } else {
    console.log(`\n✅ All tests passed!`);
    process.exit(0);
  }
}

main().catch(error => {
  console.error('Test runner error:', error);
  process.exit(1);
});
