import { getStaleFiles, styleFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Checking brain/book files for stale style reviews...');

  const staleFilesToCheck = await getStaleFiles('lastStyleHash', 'brain/book');

  console.log(`\nFound ${staleFilesToCheck.length} stale files in brain/book to style-check\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All files in brain/book are up-to-date!');
    return;
  }

  console.log('Style-checking the following files:');
  staleFilesToCheck.forEach(file => console.log(`  - ${file}`));

  for (const file of staleFilesToCheck) {
    await styleFileWithLLM(file);
  }
  console.log('\nStyle review complete for all stale files.');
}

main().catch(error => {
  console.error('An error occurred during the style review process:', error);
  process.exit(1);
});
