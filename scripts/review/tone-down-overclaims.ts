import { getBookFilesForProcessing } from './utils';
import { updateFileWithHash } from '../lib/file-utils';
import { generateGeminiProContent } from '../lib/llm';
import dotenv from 'dotenv';
import fs from 'fs/promises';
import path from 'path';

dotenv.config();

const INSTRUCTIONS = `Review this document for language that's truly insulting or makes the writer sound totally salesy or completely crazy.

IMPORTANT: If nothing is truly problematic, return the file UNCHANGED.

ONLY FIX:

1. Truly insulting personal attacks
   - Calling people "idiots" or "morons" → change to "people" or "decision-makers"
   - Keep everything else: frustration, criticism, dark humor, sarcasm

2. Overclaims that sound totally salesy or completely crazy
   - "absolutely guaranteed", "impossible to fail", "100% certain" → tone down slightly
   - Keep confident language: "will", "should", "likely", "revolutionary" are all fine

That's it. Leave everything else alone.

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
