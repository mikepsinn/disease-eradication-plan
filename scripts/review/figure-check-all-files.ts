import { getStaleFiles, figureCheckFile } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Checking brain/book files for stale figure-checks...');

  const staleFilesToCheck = await getStaleFiles('lastFigureCheckHash', 'brain/book');

  console.log(`\nFound ${staleFilesToCheck.length} stale files in brain/book to figure-check\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All files in brain/book are up-to-date!');
    return;
  }

  console.log('Figure-checking the following files:');
  staleFilesToCheck.forEach(file => console.log(`  - ${file}`));

  for (const file of staleFilesToCheck) {
    await figureCheckFile(file);
  }

  console.log('\nFigure-checking process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
