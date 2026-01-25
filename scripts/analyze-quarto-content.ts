#!/usr/bin/env tsx
/**
 * Analyze Quarto config files and compare content against a reference document
 *
 * This script loops through all files in a Quarto config's render list and asks an LLM
 * whether each file contains valuable information that's not in the reference document
 * but would be good to include in an appendix.
 *
 * Usage:
 *   npx tsx scripts/analyze-quarto-content.ts <quarto-config> <reference-document>
 *
 * Examples:
 *   npx tsx scripts/analyze-quarto-content.ts _quarto-1-pct-treaty-impact.yml knowledge/economics/1-pct-treaty-impact.qmd
 *   npx tsx scripts/analyze-quarto-content.ts _quarto-iab.yml knowledge/appendix/incentive-alignment-bonds-paper.qmd
 */

import fs from 'fs/promises';
import path from 'path';
import yaml from 'js-yaml';
import { getCleanedContentForLLM } from './lib/file-utils';
import { generateGeminiFlashContent } from './lib/llm';

interface AnalysisResult {
  filePath: string;
  recommendation: 'keep' | 'remove' | 'merge';
  reasoning: string;
  valuableContent?: string;
}

async function parseQuartoConfig(configPath: string): Promise<string[]> {
  const configContent = await fs.readFile(configPath, 'utf-8');
  const config = yaml.load(configContent) as any;

  if (!config.project?.render) {
    throw new Error(`No render list found in ${configPath}`);
  }

  // Filter out comments and extract file paths
  const renderList: string[] = config.project.render
    .filter((item: string | object) => typeof item === 'string')
    .filter((item: string) => !item.trim().startsWith('#'))
    .filter((item: string) => item.trim().length > 0);

  return renderList;
}

async function analyzeFile(
  filePath: string,
  referenceContent: string,
  referenceDocPath: string
): Promise<AnalysisResult> {
  console.log(`\n📄 Analyzing: ${filePath}`);

  try {
    const fileContent = await getCleanedContentForLLM(filePath);

    const prompt = `You are analyzing content for an academic paper appendix.

REFERENCE DOCUMENT: ${referenceDocPath}

REFERENCE CONTENT:
${referenceContent}

FILE BEING EVALUATED: ${filePath}

FILE CONTENT:
${fileContent}

TASK: Does this file contain valuable information that is NOT already covered in the reference document but would strengthen an academic paper appendix?

Please respond with a JSON object with this structure:
{
  "recommendation": "keep" | "remove" | "merge",
  "reasoning": "Brief explanation (2-3 sentences) of why",
  "valuableContent": "If 'keep' or 'merge', describe what specific content adds value (1-2 sentences). If 'remove', omit this field."
}

DECISION CRITERIA:
- "keep": File contains substantial unique valuable content that would strengthen the appendix
- "merge": File has some valuable content but it could be merged into an existing section
- "remove": File is redundant with reference document or doesn't add academic value

Be concise and objective. Focus on academic value and uniqueness.`;

    const response = await generateGeminiFlashContent(prompt);

    // Extract JSON from response
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error(`No JSON found in LLM response for ${filePath}`);
    }

    const analysis = JSON.parse(jsonMatch[0]) as AnalysisResult;
    analysis.filePath = filePath;

    console.log(`   ✓ Recommendation: ${analysis.recommendation.toUpperCase()}`);

    return analysis;

  } catch (error) {
    console.error(`   ✗ Error analyzing ${filePath}:`, error);
    return {
      filePath,
      recommendation: 'remove',
      reasoning: `Error during analysis: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

async function generateReport(
  results: AnalysisResult[],
  configPath: string,
  referenceDocPath: string,
  outputPath: string
): Promise<void> {
  const timestamp = new Date().toISOString();

  const keepFiles = results.filter(r => r.recommendation === 'keep');
  const mergeFiles = results.filter(r => r.recommendation === 'merge');
  const removeFiles = results.filter(r => r.recommendation === 'remove');

  let report = `# Content Analysis Report

**Generated**: ${timestamp}
**Config**: ${configPath}
**Reference Document**: ${referenceDocPath}
**Total Files Analyzed**: ${results.length}

## Summary

- **Keep (valuable unique content)**: ${keepFiles.length} files
- **Merge (some valuable content)**: ${mergeFiles.length} files
- **Remove (redundant/low value)**: ${removeFiles.length} files

---

## Files to Keep (${keepFiles.length})

These files contain substantial unique valuable content that would strengthen the appendix.

`;

  for (const result of keepFiles) {
    report += `### ✅ ${result.filePath}

**Reasoning**: ${result.reasoning}

**Valuable Content**: ${result.valuableContent || 'N/A'}

---

`;
  }

  report += `## Files to Merge (${mergeFiles.length})

These files have some valuable content but could be merged into existing sections.

`;

  for (const result of mergeFiles) {
    report += `### 🔀 ${result.filePath}

**Reasoning**: ${result.reasoning}

**Valuable Content**: ${result.valuableContent || 'N/A'}

---

`;
  }

  report += `## Files to Remove (${removeFiles.length})

These files are redundant with the reference document or don't add significant academic value.

`;

  for (const result of removeFiles) {
    report += `### ❌ ${result.filePath}

**Reasoning**: ${result.reasoning}

---

`;
  }

  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, report, 'utf-8');

  console.log(`\n✅ Report saved to: ${outputPath}`);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error(`Usage: npx tsx scripts/analyze-quarto-content.ts <quarto-config> <reference-document>

Examples:
  npx tsx scripts/analyze-quarto-content.ts _quarto-1-pct-treaty-impact.yml knowledge/economics/1-pct-treaty-impact.qmd
  npx tsx scripts/analyze-quarto-content.ts _quarto-iab.yml knowledge/appendix/incentive-alignment-bonds-paper.qmd
`);
    process.exit(1);
  }

  const [configPath, referenceDocPath] = args;

  console.log(`\n🔍 Content Analysis Tool`);
  console.log(`${'='.repeat(80)}\n`);
  console.log(`Config: ${configPath}`);
  console.log(`Reference: ${referenceDocPath}\n`);

  // Parse config to get file list
  console.log('📋 Parsing Quarto config...');
  const fileList = await parseQuartoConfig(configPath);
  console.log(`   Found ${fileList.length} files to analyze\n`);

  // Load reference document
  console.log('📖 Loading reference document...');
  const referenceContent = await getCleanedContentForLLM(referenceDocPath);
  console.log(`   Reference loaded (${referenceContent.length} characters)\n`);

  // Analyze each file
  console.log(`🤖 Analyzing ${fileList.length} files...\n`);
  const results: AnalysisResult[] = [];

  for (let i = 0; i < fileList.length; i++) {
    const filePath = fileList[i];
    console.log(`[${i + 1}/${fileList.length}]`);

    try {
      const result = await analyzeFile(filePath, referenceContent, referenceDocPath);
      results.push(result);
    } catch (error) {
      console.error(`   ✗ Failed to analyze ${filePath}:`, error);
      results.push({
        filePath,
        recommendation: 'remove',
        reasoning: `Analysis failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
      });
    }
  }

  // Generate report
  console.log(`\n📊 Generating report...\n`);
  const reportName = path.basename(configPath, path.extname(configPath));
  const outputPath = `_analysis/${reportName}-content-analysis.md`;
  await generateReport(results, configPath, referenceDocPath, outputPath);

  // Print summary
  const keepCount = results.filter(r => r.recommendation === 'keep').length;
  const mergeCount = results.filter(r => r.recommendation === 'merge').length;
  const removeCount = results.filter(r => r.recommendation === 'remove').length;

  console.log(`\n${'='.repeat(80)}`);
  console.log(`\n📈 Analysis Complete!\n`);
  console.log(`   ✅ Keep: ${keepCount} files`);
  console.log(`   🔀 Merge: ${mergeCount} files`);
  console.log(`   ❌ Remove: ${removeCount} files`);
  console.log(`\n   📄 Full report: ${outputPath}\n`);
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
