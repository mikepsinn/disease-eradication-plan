import { getStaleFiles, linkCheckFile } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Checking brain/book files for stale link-checks...');

  const staleFilesToCheck = await getStaleFiles('lastLinkCheckHash', 'brain/book');

  console.log(`\nFound ${staleFilesToCheck.length} stale files in brain/book to link-check\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All files in brain/book are up-to-date!');
    return;
  }

  console.log('Link-checking the following files:');
  staleFilesToCheck.forEach(file => console.log(`  - ${file}`));

  let processedCount = 0;
  for (const file of staleFilesToCheck) {
    processedCount++;
    const percent = Math.round((processedCount / staleFilesToCheck.length) * 100);

    try {
      console.log(`\n[${processedCount}/${staleFilesToCheck.length}] (${percent}%) Link checking: ${file}...`);
      await linkCheckFile(file);
    } catch (error) {
      console.error(`\n❌ FATAL ERROR link checking ${file}:`, error);
      console.error('\nStopping script due to error.');
      console.error(`Progress: ${processedCount}/${staleFilesToCheck.length} files processed`);
      process.exit(1);
    }
  }

  console.log('\nLink-checking process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
