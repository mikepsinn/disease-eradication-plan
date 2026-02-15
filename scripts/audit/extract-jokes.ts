/**
 * extract-jokes.ts - Reads each book file + the style guide,
 * sends to Gemini Flash, and extracts every joke and memorable line.
 *
 * Usage: npx tsx scripts/audit/extract-jokes.ts              (all book files)
 *        npx tsx scripts/audit/extract-jokes.ts --file path   (single file)
 * Output: _analysis/joke-catalog.md
 */
import fs from 'fs/promises';
import path from 'path';
import dotenv from 'dotenv';
dotenv.config();

import { generateGeminiFlashContent } from '../lib/llm.js';
import { readBookFilesForLLM, getProjectRoot, writeAnalysis } from './book-utils.js';

function buildPrompt(styleGuide: string, filename: string, content: string): string {
  return `You are a comedy editor reviewing a chapter from a book that uses dark humor in the style of Douglas Adams and Kurt Vonnegut. The book's style guide is provided below for context.

YOUR TASK: Read this chapter and extract every joke, memorable line, dark humor beat, funny observation, and sharp analogy. For each one, provide:

1. The exact quote (the key line or two, not the whole paragraph)
2. What it targets: "system" (institutions, bureaucracy, incentive structures, the human condition) or "people" (voters, readers, individuals, specific groups)
3. Comedy technique (absurd analogy, understatement, ironic juxtaposition, deadpan, self-aware cynicism, dark observation, bathos, escalation, etc.)
4. Quality rating: 1-5 (5 = would make Adams or Vonnegut proud)
5. Irreplaceable: yes/no (would the book lose something unique and memorable if this were cut?)

Group your output into two sections:

## KEEP (System-targeting humor)
Lines that target broken systems, institutions, incentive structures, bureaucracy, or the human condition generally. These are on-brand per the style guide.

## REVIEW (People-targeting or borderline)
Lines that target specific groups of people (voters, readers, politicians as individuals). These may need rewriting to target the system instead, or may be fine in context.

For each line, use this format:

### [number]. "[exact quote]"
- **Targets:** [system/people] - [what specifically]
- **Technique:** [comedy technique]
- **Quality:** [1-5]/5
- **Irreplaceable:** [yes/no]
- **Notes:** [brief context: why this works, or what's wrong with it]

At the end, add a summary:

## Summary
- Total jokes/lines found: [N]
- System-targeting (keep): [N]
- People-targeting (review): [N]
- 5/5 quality lines: [list the quotes]
- Irreplaceable lines: [list the quotes]

=== STYLE GUIDE ===
${styleGuide}

=== CHAPTER: ${filename} ===
${content}`;
}

async function main() {
  console.log('=== Joke & Memorable Line Extractor ===\n');

  // Read style guide
  const styleGuidePath = path.join(getProjectRoot(), 'GUIDES', 'STYLE_GUIDE.md');
  const styleGuide = await fs.readFile(styleGuidePath, 'utf-8');

  // Determine which files to process
  const fileArgIndex = process.argv.indexOf('--file');
  const singleFile = fileArgIndex !== -1 ? process.argv[fileArgIndex + 1] : null;

  const files = singleFile
    ? await readBookFilesForLLM([singleFile])
    : await readBookFilesForLLM();

  console.log(`\nProcessing ${files.length} file${files.length === 1 ? '' : 's'}\n`);

  const results: string[] = [];

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    console.log(`[${i + 1}/${files.length}] ${file.filename} (${file.wordCount} words)`);

    const prompt = buildPrompt(styleGuide, file.filename, file.content);
    const result = await generateGeminiFlashContent(prompt);

    results.push([
      `# ${file.title}`,
      `**File:** \`${file.filename}\``,
      `**Words:** ${file.wordCount}`,
      '',
      result,
    ].join('\n'));
  }

  const timestamp = new Date().toISOString().split('T')[0];
  const output = [
    '# Joke & Memorable Line Catalog',
    '',
    `Generated: ${timestamp}`,
    `Files analyzed: ${files.length}`,
    '',
    '---',
    '',
    results.join('\n\n---\n\n'),
  ].join('\n');

  const outputPath = await writeAnalysis('joke-catalog.md', output);
  console.log(`\nResults written to: ${outputPath}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
