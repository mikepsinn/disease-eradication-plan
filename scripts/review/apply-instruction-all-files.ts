import { getBookFilesForProcessing } from './utils';
import { readFileWithMatter, updateFileWithHash } from '../lib/file-utils';
import { generateGeminiProContent } from '../lib/llm';
import dotenv from 'dotenv';
import fs from 'fs/promises';

dotenv.config();

async function applyInstructionToFile(
  filePath: string,
  instruction: string,
  hashField: string
): Promise<void> {
  console.log(`\nApplying instruction to ${filePath}...`);
  const { frontmatter, body } = await readFileWithMatter(filePath);

  // Build the prompt with the instruction and file content
  const prompt = `${instruction}

---

FILE CONTENT:

${body}

---

INSTRUCTIONS:
1. Apply the instruction above to the file content
2. Return ONLY the updated file content (without frontmatter)
3. If no changes are needed, return exactly: NO_CHANGES_NEEDED
4. Do NOT include markdown code fences (no \`\`\`) in your response
5. Preserve all existing formatting, spacing, and structure unless the instruction requires changes`;

  const responseText = await generateGeminiProContent(prompt);

  let finalBody;
  if (responseText.trim() === 'NO_CHANGES_NEEDED') {
    console.log(`File ${filePath} requires no changes. Updating metadata.`);
    finalBody = body;
  } else {
    // Strip markdown code blocks if present
    let cleaned = responseText.trim();
    cleaned = cleaned.replace(/^```[a-z]*\n?/i, '');
    cleaned = cleaned.replace(/\n?```\s*$/i, '');
    finalBody = cleaned.trim();
  }

  await updateFileWithHash(filePath, finalBody, frontmatter, hashField);
  console.log(`Successfully processed ${filePath}.`);
}

async function main() {
  // Get instruction from command line arguments or prompt.md file
  const args = process.argv.slice(2);
  let instruction: string;

  if (args.length === 0) {
    // Try to read from prompt.md
    try {
      instruction = await fs.readFile('prompt.md', 'utf-8');
      instruction = instruction.trim();

      if (!instruction) {
        console.error('ERROR: prompt.md exists but is empty.');
        console.error('\nUsage options:');
        console.error('  1. npx tsx scripts/review/apply-instruction-all-files.ts "Your instruction here"');
        console.error('  2. Create a prompt.md file in the root directory with your instruction');
        console.error('\nExample: npx tsx scripts/review/apply-instruction-all-files.ts "Replace all instances of \'utilise\' with \'use\'"');
        process.exit(1);
      }

      console.log('Reading instruction from prompt.md...\n');
    } catch (error) {
      console.error('ERROR: No instruction provided and prompt.md not found.');
      console.error('\nUsage options:');
      console.error('  1. npx tsx scripts/review/apply-instruction-all-files.ts "Your instruction here"');
      console.error('  2. Create a prompt.md file in the root directory with your instruction');
      console.error('\nExample: npx tsx scripts/review/apply-instruction-all-files.ts "Replace all instances of \'utilise\' with \'use\'"');
      process.exit(1);
    }
  } else {
    instruction = args.join(' ');
  }

  // Generate a hash field name from the instruction (sanitize for use as field name)
  const hashField = 'lastCustomInstructionHash';

  console.log('='.repeat(80));
  console.log('APPLY INSTRUCTION TO ALL FILES');
  console.log('='.repeat(80));
  console.log(`\nInstruction: ${instruction}`);
  console.log(`Hash field: ${hashField}\n`);

  // Get all book files for processing
  const allBookFiles = await getBookFilesForProcessing();

  // Additional exclusions (same as fact-check-all-files.ts)
  const excludedFiles = [
    'brain\\book\\vision.qmd',
    'index.qmd',
  ];

  const excludedPatterns = [
    /references\.qmd$/,  // Always exclude references
  ];

  // Filter files
  const filesToProcess = allBookFiles.filter(file => {
    const normalizedFile = file.replace(/\\/g, '/');

    // Check exact file matches
    if (excludedFiles.includes(file)) return false;

    // Check pattern matches
    if (excludedPatterns.some(pattern => pattern.test(file))) return false;

    return true;
  });

  console.log(`Found ${allBookFiles.length} total book files`);
  if (allBookFiles.length > filesToProcess.length) {
    console.log(`  - ${allBookFiles.length - filesToProcess.length} excluded (references.qmd, vision.qmd, futures chapters)`);
  }
  console.log(`  - ${filesToProcess.length} files to process\n`);

  if (filesToProcess.length === 0) {
    console.log('No files to process!');
    return;
  }

  // Confirm with user before proceeding
  console.log('Files to process:');
  filesToProcess.forEach(file => console.log(`  - ${file}`));
  console.log('\nPress Ctrl+C to cancel, or wait 5 seconds to continue...\n');

  await new Promise(resolve => setTimeout(resolve, 5000));

  let processedCount = 0;
  let changedCount = 0;
  let unchangedCount = 0;
  let errorCount = 0;

  for (const file of filesToProcess) {
    processedCount++;
    try {
      console.log(`\n[${ processedCount}/${filesToProcess.length}] Processing: ${file}...`);

      // Read file before processing to check if it changed
      const beforeContent = await fs.readFile(file, 'utf-8');

      await applyInstructionToFile(file, instruction, hashField);

      // Read file after processing to check if it changed
      const afterContent = await fs.readFile(file, 'utf-8');

      if (beforeContent !== afterContent) {
        changedCount++;
        console.log(`  ✓ File modified`);
      } else {
        unchangedCount++;
        console.log(`  ○ No changes`);
      }
    } catch (error) {
      errorCount++;
      console.error(`\n❌ ERROR processing ${file}:`, error);
      console.error('Continuing with next file...\n');
    }
  }

  console.log('\n' + '='.repeat(80));
  console.log('PROCESSING COMPLETE');
  console.log('='.repeat(80));
  console.log(`Total files: ${filesToProcess.length}`);
  console.log(`  ✓ Modified: ${changedCount}`);
  console.log(`  ○ Unchanged: ${unchangedCount}`);
  console.log(`  ✗ Errors: ${errorCount}`);
  console.log('='.repeat(80));
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});