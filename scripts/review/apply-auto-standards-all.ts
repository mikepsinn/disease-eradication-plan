import { getStaleFiles, formatFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Checking knowledge files for stale formatting...');

  const staleFilesToCheck = await getStaleFiles('lastFormattedHash', 'knowledge');

  console.log(`\nFound ${staleFilesToCheck.length} stale files in knowledge to format\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All files in knowledge are up-to-date!');
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
