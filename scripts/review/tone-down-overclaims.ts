import { getBookFilesForProcessing } from './utils';
import { updateFileWithHash } from '../lib/file-utils';
import { generateGeminiProContent } from '../lib/llm';
import dotenv from 'dotenv';
import fs from 'fs/promises';
import path from 'path';

dotenv.config();

const INSTRUCTIONS = `You are editing this document to fix overclaims, over-confidence, and salesy language while preserving all content and tone.

SPECIFIC CHANGES TO MAKE:

1. Replace insults with neutral analytical terms:
   - "stupid" → "illogical" or "irrational"
   - "idiots" → "decision-makers" or "people"
   - "dumb" → "flawed" or "poorly designed"
   - "morons" → "officials" or "authorities"

2. Fix over-confidence and overclaims:
   - "will definitely" → "could" or "might"
   - "guaranteed to work" → "might work" or "could work if"
   - "impossible to fail" → "designed to succeed if"
   - "always" → "often" or "typically"
   - "never" → "rarely" or "unlikely to"
   - "everyone" (when making claims) → "many people" or "most people"
   - "inevitable" → "possible" or "likely"

3. Remove salesy/pompous language:
   - "revolutionary" → just describe what it does
   - "game-changing" → just describe what it does
   - "unprecedented" → remove or be specific
   - "once-in-a-lifetime" → remove
   - Exclamation points used for hype → remove or use periods

4. Add conditional language where appropriate:
   - Add "if [condition]" to claims about outcomes
   - Add "could", "might", "may" to predictions
   - Add "typically", "often", "usually" to generalizations

CRITICAL RULES - DO NOT CHANGE:

- Keep ALL numbers, statistics, calculations, citations, references
- Keep the overall tone and personality (weary parent, dark humor)
- Keep casual vocabulary (kill, die, poison, eat) - these are not insults
- Keep section structure, headers, formatting
- Keep all technical content unchanged
- Preserve contractions
- Keep vivid analogies and metaphors
- Keep sarcasm about systems/structures (just tone down personal insults)
- DO NOT make the document bland or corporate
- 95% of text should remain identical

Return the complete .qmd file with frontmatter unchanged.`;

async function processFile(filePath: string): Promise<void> {
  console.log(`\nProcessing: ${path.basename(filePath)}`);

  const matter = await import('gray-matter');

  // Read the entire file
  const originalContent = await fs.readFile(filePath, 'utf-8');
  const { data: frontmatter, content: body } = matter.default(originalContent);

  const prompt = `${INSTRUCTIONS}

---

FILE CONTENT:

${originalContent}

---

Return the complete .qmd file with the fixes applied. Do NOT wrap in markdown code fences.`;

  console.log(`  Sending to Gemini Pro...`);
  const responseText = await generateGeminiProContent(prompt);

  // Strip markdown code blocks if the LLM wrapped the response
  let cleanedResponse = responseText.trim();
  cleanedResponse = cleanedResponse.replace(/^```[a-z]*\n?/i, '');
  cleanedResponse = cleanedResponse.replace(/\n?```\s*$/i, '');

  // Parse the transformed content
  const { data: finalFrontmatter, content: finalBody } = matter.default(cleanedResponse);

  // Save the file with a hash to track changes
  const hashField = 'lastToneDownHash';
  await updateFileWithHash(filePath, finalBody, finalFrontmatter, hashField);

  console.log(`  ✓ Updated file`);
}

async function main() {
  const args = process.argv.slice(2);

  // Parse arguments
  let specificFile: string | null = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--file=')) {
      specificFile = args[i].substring('--file='.length);
    } else if (args[i] === '--file' || args[i] === '-f') {
      specificFile = args[++i];
    }
  }

  console.log('='.repeat(80));
  console.log('TONE DOWN OVERCLAIMS AND INSULTS');
  console.log('='.repeat(80));
  console.log('\nThis will update source files to:');
  console.log('- Fix over-confidence and overclaims');
  console.log('- Remove salesy language');
  console.log('- Replace insults with neutral analytical terms\n');

  // Get all book files
  const allBookFiles = await getBookFilesForProcessing();

  // Filter out audience variants - we only want source files
  let sourceFiles = allBookFiles.filter(file => {
    const normalizedFile = file.replace(/\\/g, '/');
    // Exclude -academic and -foundations variants
    if (normalizedFile.includes('-academic.qmd')) return false;
    if (normalizedFile.includes('-foundations.qmd')) return false;
    return true;
  });

  // Filter to specific file if requested
  if (specificFile) {
    const absoluteSpecificFile = path.resolve(specificFile);
    sourceFiles = sourceFiles.filter(file => path.resolve(file) === absoluteSpecificFile);

    if (sourceFiles.length === 0) {
      console.error(`\nERROR: File not found or not a valid source file: ${specificFile}`);
      console.error('Make sure the file path is relative to the project root and is a source .qmd file (not -academic or -foundations)');
      process.exit(1);
    }

    console.log(`\nProcessing single file: ${specificFile}`);
  }

  console.log(`Found ${allBookFiles.length} total files`);
  console.log(`  - ${allBookFiles.length - sourceFiles.length} excluded (audience variants)`);
  console.log(`  - ${sourceFiles.length} source files to process\n`);

  if (sourceFiles.length === 0) {
    console.log('No source files to process!');
    return;
  }

  // Show files that will be processed
  console.log('Files to process:');
  sourceFiles.forEach(file => {
    console.log(`  ${path.basename(file)}`);
  });

  console.log('\nPress Ctrl+C to cancel, or wait 5 seconds to continue...\n');
  await new Promise(resolve => setTimeout(resolve, 5000));

  let processedCount = 0;
  let successCount = 0;
  let errorCount = 0;

  for (const file of sourceFiles) {
    processedCount++;
    console.log(`\n[${processedCount}/${sourceFiles.length}]`);

    try {
      await processFile(file);
      successCount++;
    } catch (error) {
      errorCount++;
      console.error(`\n  ❌ ERROR processing ${path.basename(file)}:`, error);
      console.error('  Continuing with next file...\n');
    }
  }

  console.log('\n' + '='.repeat(80));
  console.log('PROCESSING COMPLETE');
  console.log('='.repeat(80));
  console.log(`Total files: ${sourceFiles.length}`);
  console.log(`  ✓ Success: ${successCount}`);
  console.log(`  ✗ Errors: ${errorCount}`);
  console.log('='.repeat(80));
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
