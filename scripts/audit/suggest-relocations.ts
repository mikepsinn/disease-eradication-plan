/**
 * suggest-relocations.ts - Sends overview chapters + destination chapters
 * to Gemini Pro and finds unique content that would be lost if overviews
 * were condensed.
 *
 * Usage: npx tsx scripts/audit/suggest-relocations.ts
 * Output: _analysis/relocation-suggestions.md
 */
import dotenv from 'dotenv';
dotenv.config();

import { generateGeminiProContent } from '../lib/llm.js';
import { readBookFilesForLLM, buildBookText, writeAnalysis } from './book-utils.js';

// Overview files that summarize/preview other chapters
const OVERVIEW_FILES = new Set([
  'index-manual.qmd',
  'knowledge/problem.qmd',
  'knowledge/solution.qmd',
]);

const PROMPT = `You are a book editor analyzing overview/introduction chapters to find content that should be relocated before these chapters are condensed.

This book has three overview chapters (index-manual.qmd, knowledge/problem.qmd, knowledge/solution.qmd) that summarize content from their respective sections. The goal is to condense these overviews to reduce reader fatigue, but we must NOT lose any unique jokes, memorable lines, arguments, or data that don't exist elsewhere in the book.

Below you'll find:
1. The overview chapters (marked as OVERVIEW)
2. All other chapters (marked as DESTINATION)

YOUR TASK: For each overview chapter, find content that is UNIQUE to that overview (not present in substantially similar form in any destination chapter). This is content that would be LOST if the overview were condensed.

Output format:

## [Overview filename]

### Unique Content (MUST RELOCATE before condensing)

#### 1. "[Exact quote or summary of passage]"
- **Section in overview:** [section heading where this appears]
- **Best destination:** [filename of the chapter where this should move]
- **Why:** [brief reason this chapter is the best home]
- **Type:** [joke / argument / data / analogy / unique framing]

### Redundant Content (safe to cut from overview)

#### 1. "[Exact quote or summary]"
- **Also in:** [filename where this content already exists, with better/equal version]
- **Better version in destination?:** [yes/no]

---

Be thorough. Every unique joke, every data point not found elsewhere, every memorable analogy must be flagged. The goal is zero loss of good material when we condense these overviews.

=== BOOK CONTENT ===
`;

async function main() {
  console.log('=== Content Relocation Suggester ===\n');

  const allFiles = await readBookFilesForLLM();
  const totalWords = allFiles.reduce((sum, f) => sum + f.wordCount, 0);
  console.log(`\nRead ${allFiles.length} files (${totalWords.toLocaleString()} words total)`);

  // Label files as OVERVIEW or DESTINATION
  const bookText = buildBookText(allFiles, f =>
    OVERVIEW_FILES.has(f.filename) ? 'OVERVIEW' : 'DESTINATION'
  );

  const fullPrompt = PROMPT + bookText;

  const estimatedTokens = Math.round(fullPrompt.length / 4);
  console.log(`Prompt size: ~${estimatedTokens.toLocaleString()} tokens`);
  console.log('Sending to Gemini Pro (2M context)...\n');

  const result = await generateGeminiProContent(fullPrompt);

  const timestamp = new Date().toISOString().split('T')[0];
  const overviewList = [...OVERVIEW_FILES].join(', ');
  const output = [
    '# Relocation Suggestions',
    '',
    `Generated: ${timestamp}`,
    `Overview files: ${overviewList}`,
    `Total files analyzed: ${allFiles.length}`,
    '',
    '---',
    '',
    result,
  ].join('\n');

  const outputPath = await writeAnalysis('relocation-suggestions.md', output);
  console.log(`\nResults written to: ${outputPath}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
