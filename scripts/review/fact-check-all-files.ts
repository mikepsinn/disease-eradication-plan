import { getStaleFiles, getBookFilesForProcessing, factCheckFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Checking brain/book files for stale fact-checks...');

  // Get all book files (already excludes references.qmd)
  const allBookFiles = await getBookFilesForProcessing();

  // Additional exclusions for fact-checking
  const excludedFiles = [
    'brain\\book\\vision.qmd',       // Aspirational/hypothetical future scenarios
  ];

  // Exclude futures chapters (aspirational/hypothetical scenarios)
  const excludedPatterns = [
    /brain[\\\/]book[\\\/]futures[\\\/]/
  ];

  // Get stale files that need fact-checking
  const allStaleBookFiles = await getStaleFiles('lastFactCheckHash', 'brain/book');

  // Filter to only book files that are stale and not excluded
  const staleFilesToCheck = allStaleBookFiles.filter(file => {
    // Must be in our book files list
    const normalizedFile = file.replace(/\\/g, '/');
    if (!allBookFiles.some(bookFile => bookFile.replace(/\\/g, '/') === normalizedFile)) return false;

    // Check exact file matches
    if (excludedFiles.includes(file)) return false;

    // Check pattern matches
    if (excludedPatterns.some(pattern => pattern.test(file))) return false;

    return true;
  });

  console.log(`\nFound ${allStaleBookFiles.length} stale files in brain/book`);
  if (allStaleBookFiles.length > staleFilesToCheck.length) {
    console.log(`  - ${allStaleBookFiles.length - staleFilesToCheck.length} excluded (references.qmd, vision.qmd, futures chapters)`);
  }
  console.log(`  - ${staleFilesToCheck.length} files to fact-check\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All files in brain/book are up-to-date!');
    return;
  }

  console.log('Fact-checking the following files:');
  staleFilesToCheck.forEach(file => console.log(`  - ${file}`));

  for (const file of staleFilesToCheck) {
    await factCheckFileWithLLM(file);
  }

  console.log('\nFact-checking process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
