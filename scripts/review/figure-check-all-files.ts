import { getStaleFiles, figureCheckFile } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Identifying stale files for figure-checking...');
  const staleFiles = await getStaleFiles('lastFigureCheckHash');
  const bookFiles = staleFiles.filter(file => file.startsWith('brain\\book'));

  console.log(`Checked ${staleFiles.length} total stale files.`);
  console.log(`Found ${bookFiles.length} files in brain/book to figure-check:`);

  if (bookFiles.length === 0) {
    console.log('All files in brain/book are up-to-date.');
    return;
  }
  for (const file of bookFiles) {
    await figureCheckFile(file);
  }

  console.log('\nFigure-checking process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
