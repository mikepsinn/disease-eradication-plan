import { getStaleFiles, linkCheckFile } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Identifying stale files for link-checking...');
  const staleFiles = await getStaleFiles('lastLinkCheck');
  const bookFiles = staleFiles.filter(file => file.startsWith('brain\\book'));

  console.log(`Checked ${staleFiles.length} total stale files.`);
  console.log(`Found ${bookFiles.length} files in brain/book to link-check:`);

  if (bookFiles.length === 0) {
    console.log('All files in brain/book are up-to-date.');
    return;
  }
  for (const file of bookFiles) {
    await linkCheckFile(file);
  }

  console.log('\nLink-checking process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
