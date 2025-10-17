import { getStaleFiles, formatFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Checking brain/book files for stale formatting...');

  const staleFilesToCheck = await getStaleFiles('lastFormattedHash', 'brain/book');

  console.log(`\nFound ${staleFilesToCheck.length} stale files in brain/book to format\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All files in brain/book are up-to-date!');
    return;
  }

  console.log('Formatting the following files:');
  staleFilesToCheck.forEach(file => console.log(`  - ${file}`));

  for (const file of staleFilesToCheck) {
    await formatFileWithLLM(file);
  }

  console.log('\nFormatting process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
