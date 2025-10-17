import { getStaleFiles, factCheckFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Identifying stale files for fact-checking...');
  // Note: We get *all* stale files and then filter. 
  const staleFiles = await getStaleFiles('lastFactCheckHash'); 
  const bookFiles = staleFiles.filter(file => file.startsWith('brain\\book'));

  console.log(`Checked ${staleFiles.length} total stale files.`);
  console.log(`Found ${bookFiles.length} files in brain/book to fact-check:`);

  if (bookFiles.length === 0) {
    console.log('All files in brain/book are up-to-date.');
    return;
  }
  for (const file of bookFiles) {
    await factCheckFileWithLLM(file);
  }

  console.log('\nFact-checking process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
