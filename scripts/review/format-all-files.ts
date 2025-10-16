import { getStaleFiles, formatFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Identifying stale files for formatting...');
  const staleFiles = await getStaleFiles('lastFormatted');

  if (staleFiles.length === 0) {
    console.log('All files are up-to-date. No formatting needed.');
    return;
  }

  console.log(`Found ${staleFiles.length} files to format:`);
  for (const file of staleFiles) {
    await formatFileWithLLM(file);
  }

  console.log('\nFormatting process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
