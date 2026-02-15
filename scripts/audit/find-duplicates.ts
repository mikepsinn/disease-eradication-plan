/**
 * find-duplicates.ts - Sends the entire book to Gemini Pro (2M context)
 * and asks it to find all substantially duplicated content across files.
 *
 * Usage: npx tsx scripts/audit/find-duplicates.ts
 * Output: _analysis/duplication-map.md
 */
import dotenv from 'dotenv';
dotenv.config();

import { generateGeminiProContent } from '../lib/llm.js';
import { readBookFilesForLLM, buildBookText, writeAnalysis } from './book-utils.js';

const PROMPT = `You are a book editor conducting a thorough duplication audit of a 136,000-word manuscript. The complete book is provided below, with each chapter clearly marked.

YOUR TASK: Find every instance where substantially similar content appears in more than one file. This includes:

1. **Same statistic or fact** cited in multiple places (e.g., "$2,718 billion in military spending" or "150,000 deaths per day")
2. **Same argument or explanation** made in different words (e.g., "defense contractors should pivot to health" explained in two different chapters)
3. **Same structural element** repeated (e.g., a "Why 10%?" section, or an "80/10/10 revenue split" explanation appearing in multiple files)
4. **Same analogy, joke, or memorable line** used more than once

For each duplication found, output in this exact format:

## [Number]. [Brief description of duplicated content]

**Concept:** [One-sentence summary of what is being repeated]
**Found in:** [comma-separated list of filenames]

### Version in [filename1]
> [Exact quote, 1-3 sentences, enough to identify the passage]

### Version in [filename2]
> [Exact quote from file 2]

(Include Version 3, 4 if more files contain it.)

**Best version:** [which file has the strongest/most complete version and why]
**Suggested canonical home:** [which file should own this content based on its topic]

---

Be extremely thorough. Check EVERY file against EVERY other file. This book is known to have significant duplication. Pay special attention to:
- Military spending statistics and costs
- The 1% treaty concept and mechanics
- ROI calculations and returns
- Defense contractor incentive alignment
- The 80/10/10 revenue split
- The "ratchet effect" (1% expanding to 2%, 5%)
- "Why 10%?" explanations
- FDA cost/efficiency statistics
- The RECOVERY trial comparison
- Drug development cost increases
- Peace dividend calculations
- Incentive alignment bond mechanics

Do NOT flag:
- Intentional brief cross-references or "as discussed in Chapter X" callbacks
- The same term being defined once and used elsewhere
- Thematic consistency (e.g., multiple chapters mentioning "war on disease" as a phrase)

Only flag cases where the same content is explained at similar length or detail in multiple places.

=== COMPLETE BOOK TEXT ===
`;

async function main() {
  console.log('=== Book Duplication Finder ===\n');

  const files = await readBookFilesForLLM();
  const totalWords = files.reduce((sum, f) => sum + f.wordCount, 0);
  console.log(`\nRead ${files.length} files (${totalWords.toLocaleString()} words total)`);

  const bookText = buildBookText(files);
  const fullPrompt = PROMPT + bookText;

  const estimatedTokens = Math.round(fullPrompt.length / 4);
  console.log(`Prompt size: ~${estimatedTokens.toLocaleString()} tokens`);
  console.log('Sending to Gemini Pro (2M context)...\n');

  const result = await generateGeminiProContent(fullPrompt);

  const timestamp = new Date().toISOString().split('T')[0];
  const output = [
    '# Duplication Map',
    '',
    `Generated: ${timestamp}`,
    `Files analyzed: ${files.length}`,
    `Total words: ${totalWords.toLocaleString()}`,
    '',
    '---',
    '',
    result,
  ].join('\n');

  const outputPath = await writeAnalysis('duplication-map.md', output);
  console.log(`\nResults written to: ${outputPath}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
