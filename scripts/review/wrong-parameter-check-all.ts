import fs from 'fs/promises';
import { getBookFilesForProcessing } from './utils';
import { generateGeminiFlashContent } from '../lib/llm';
import { loadPromptTemplate } from '../lib/llm';
import { readFileWithMatter } from '../lib/file-utils';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config();

interface ParameterIssue {
  line: number;
  parameter: string;
  context: string;
  problem: string;
  parameterMeaning: string;
  parameterValue: string;
  parameterUnit: string;
  suggestedFix: string;
}

interface FileCheckResult {
  filePath: string;
  status: 'issues_found' | 'no_issues_found' | 'error';
  issues: ParameterIssue[];
  errorMessage?: string;
}

async function checkFileForWrongParameters(filePath: string): Promise<FileCheckResult> {
  console.log(`Checking: ${filePath}`);

  try {
    const { body } = await readFileWithMatter(filePath);

    // Load parameters file
    const parametersFile = await fs.readFile('dih_models/parameters.py', 'utf-8');

    // Load and fill prompt template
    const prompt = await loadPromptTemplate('tools/prompts/wrong-parameter-check.md', {
      '{{parametersFile}}': parametersFile,
      '{{body}}': body
    });

    // Call Gemini 2.5 Flash
    const responseText = await generateGeminiFlashContent(prompt);

    // Parse JSON response
    let response;
    try {
      // Try to extract JSON from markdown code blocks or raw text
      const jsonMatch = responseText.match(/```json\s*([\s\S]*?)\s*```/) ||
                       responseText.match(/```\s*([\s\S]*?)\s*```/) ||
                       [null, responseText];

      const jsonText = jsonMatch[1] || responseText;
      response = JSON.parse(jsonText.trim());
    } catch (parseError) {
      console.error(`Failed to parse JSON from response for ${filePath}`);
      console.error('Raw response:', responseText);
      return {
        filePath,
        status: 'error',
        issues: [],
        errorMessage: `JSON parse error: ${parseError}`
      };
    }

    if (response.status === 'no_issues_found') {
      console.log(`✓ No issues found in ${filePath}`);
      return {
        filePath,
        status: 'no_issues_found',
        issues: []
      };
    }

    if (response.status === 'issues_found' && response.issues && response.issues.length > 0) {
      console.log(`⚠ Found ${response.issues.length} semantic parameter error(s) in ${filePath}`);
      response.issues.forEach((issue: ParameterIssue, i: number) => {
        console.log(`  ${i + 1}. Line ${issue.line}: ${issue.parameter} - ${issue.problem}`);
      });

      return {
        filePath,
        status: 'issues_found',
        issues: response.issues
      };
    }

    // Unexpected response format
    console.warn(`Unexpected response format for ${filePath}:`, response);
    return {
      filePath,
      status: 'error',
      issues: [],
      errorMessage: 'Unexpected response format from LLM'
    };

  } catch (error) {
    console.error(`Error checking ${filePath}:`, error);
    return {
      filePath,
      status: 'error',
      issues: [],
      errorMessage: String(error)
    };
  }
}

async function main() {
  console.log('Checking knowledge files for semantic parameter errors using Gemini 2.5 Flash...\n');

  // Get all QMD files from knowledge directory using glob
  const glob = (await import('glob')).glob;
  const knowledgeFiles = await glob('knowledge/**/*.qmd', {
    ignore: ['**/node_modules/**', '**/_freeze/**', '**/_book/**']
  });

  console.log(`Found ${knowledgeFiles.length} files to check\n`);

  const results: FileCheckResult[] = [];
  let processedCount = 0;

  // Initialize progress log file
  const progressLogPath = 'SEMANTIC-PARAMETER-CHECK-PROGRESS.log';
  await fs.writeFile(progressLogPath, `Started checking ${knowledgeFiles.length} files at ${new Date().toISOString()}\n\n`);

  for (const file of knowledgeFiles) {
    processedCount++;
    const percent = Math.round((processedCount / knowledgeFiles.length) * 100);

    console.log(`\n[${processedCount}/${knowledgeFiles.length}] (${percent}%)`);

    const result = await checkFileForWrongParameters(file);
    results.push(result);

    // Append result to progress log immediately
    let logEntry = `[${processedCount}/${knowledgeFiles.length}] ${file}: `;
    if (result.status === 'no_issues_found') {
      logEntry += '✓ CLEAN\n';
    } else if (result.status === 'issues_found') {
      logEntry += `⚠ ${result.issues.length} error(s)\n`;
      result.issues.forEach((issue, i) => {
        logEntry += `  ${i + 1}. Line ${issue.line}: ${issue.parameter} - ${issue.problem}\n`;
      });
    } else {
      logEntry += `✗ ERROR: ${result.errorMessage}\n`;
    }
    logEntry += '\n';

    await fs.appendFile(progressLogPath, logEntry);

    // Save incremental JSON backup every 10 files
    if (processedCount % 10 === 0) {
      await fs.writeFile('SEMANTIC-PARAMETER-ERRORS-GEMINI-PARTIAL.json', JSON.stringify(results, null, 2));
    }

    // Add a small delay to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  // Generate summary report
  console.log('\n\n' + '='.repeat(80));
  console.log('SEMANTIC PARAMETER ERROR REPORT');
  console.log('='.repeat(80) + '\n');

  const filesWithIssues = results.filter(r => r.status === 'issues_found');
  const filesClean = results.filter(r => r.status === 'no_issues_found');
  const filesWithErrors = results.filter(r => r.status === 'error');

  console.log(`Total files checked: ${results.length}`);
  console.log(`Files with semantic errors: ${filesWithIssues.length}`);
  console.log(`Files verified clean: ${filesClean.length}`);
  console.log(`Files with check errors: ${filesWithErrors.length}`);

  const totalIssues = filesWithIssues.reduce((sum, r) => sum + r.issues.length, 0);
  console.log(`Total semantic errors found: ${totalIssues}\n`);

  if (filesWithIssues.length > 0) {
    console.log('\nFILES WITH SEMANTIC PARAMETER ERRORS:\n');

    filesWithIssues.forEach((result, index) => {
      console.log(`${index + 1}. ${result.filePath} (${result.issues.length} errors)`);
      result.issues.forEach((issue, i) => {
        console.log(`   ${i + 1}. Line ${issue.line}: {{< var ${issue.parameter} >}}`);
        console.log(`      Problem: ${issue.problem}`);
        console.log(`      Context: ${issue.context.substring(0, 80)}...`);
        console.log(`      Fix: ${issue.suggestedFix}`);
      });
      console.log('');
    });
  }

  if (filesWithErrors.length > 0) {
    console.log('\nFILES WITH CHECK ERRORS:\n');
    filesWithErrors.forEach((result, index) => {
      console.log(`${index + 1}. ${result.filePath}`);
      console.log(`   Error: ${result.errorMessage}\n`);
    });
  }

  // Save detailed report to file
  const reportPath = 'SEMANTIC-PARAMETER-ERRORS-GEMINI.json';
  await fs.writeFile(reportPath, JSON.stringify(results, null, 2));
  console.log(`\nDetailed report saved to: ${reportPath}`);

  // Save human-readable summary
  const summaryPath = 'SEMANTIC-PARAMETER-ERRORS-SUMMARY.md';
  let summary = '# Semantic Parameter Errors - Gemini 2.5 Flash Check\n\n';
  summary += `**Date:** ${new Date().toISOString()}\n\n`;
  summary += `## Summary\n\n`;
  summary += `- Total files checked: ${results.length}\n`;
  summary += `- Files with errors: ${filesWithIssues.length}\n`;
  summary += `- Files clean: ${filesClean.length}\n`;
  summary += `- Total issues: ${totalIssues}\n\n`;

  if (filesWithIssues.length > 0) {
    summary += `## Files with Errors\n\n`;
    filesWithIssues.forEach((result) => {
      summary += `### ${result.filePath}\n\n`;
      summary += `**${result.issues.length} semantic error(s) found**\n\n`;
      result.issues.forEach((issue, i) => {
        summary += `#### Error ${i + 1}\n\n`;
        summary += `- **Line:** ${issue.line}\n`;
        summary += `- **Parameter:** \`{{< var ${issue.parameter} >}}\`\n`;
        summary += `- **Parameter Meaning:** ${issue.parameterMeaning}\n`;
        summary += `- **Parameter Value:** ${issue.parameterValue} ${issue.parameterUnit}\n`;
        summary += `- **Problem:** ${issue.problem}\n`;
        summary += `- **Context:** \`${issue.context}\`\n`;
        summary += `- **Suggested Fix:** ${issue.suggestedFix}\n\n`;
      });
    });
  }

  await fs.writeFile(summaryPath, summary);
  console.log(`Human-readable summary saved to: ${summaryPath}\n`);

  console.log('Check complete!');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
