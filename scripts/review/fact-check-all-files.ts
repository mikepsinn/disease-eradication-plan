import { getStaleFiles, factCheckFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Checking brain/book files for stale fact-checks...');

  // Exclude files that shouldn't be fact-checked
  const excludedFiles = [
    'brain\\book\\references.qmd',  // References file itself
    'brain\\book\\vision.qmd',       // Aspirational/hypothetical future scenarios
  ];

  // Get all files in brain/book that are stale (need fact-checking)
  const allStaleBookFiles = await getStaleFiles('lastFactCheckHash', 'brain/book');

  // Filter out explicitly excluded files
  const staleFilesToCheck = allStaleBookFiles.filter(file => !excludedFiles.includes(file));

  console.log(`\nFound ${allStaleBookFiles.length} stale files in brain/book`);
  if (allStaleBookFiles.length > staleFilesToCheck.length) {
    console.log(`  - ${allStaleBookFiles.length - staleFilesToCheck.length} excluded (references.qmd, vision.qmd)`);
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
