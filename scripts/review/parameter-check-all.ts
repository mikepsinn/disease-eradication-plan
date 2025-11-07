import { getStaleFiles, parameterizeFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Checking brain/book files for hardcoded numbers...');

  const staleFilesToCheck = await getStaleFiles('lastParamCheckHash', 'brain/book');

  console.log(`\nFound ${staleFilesToCheck.length} stale files in brain/book to check for parameterization.\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All files in brain/book are up-to-date!');
    return;
  }

  console.log('Parameterizing the following files:');
  staleFilesToCheck.forEach(file => console.log(`  - ${file}`));

  let processedCount = 0;
  for (const file of staleFilesToCheck) {
    processedCount++;
    const percent = Math.round((processedCount / staleFilesToCheck.length) * 100);

    try {
      console.log(`\n[${processedCount}/${staleFilesToCheck.length}] (${percent}%) Parameterizing: ${file}...`);
      await parameterizeFileWithLLM(file);
    } catch (error) {
      console.error(`\n❌ FATAL ERROR parameterizing ${file}:`, error);
      console.error('\nStopping script due to error.');
      console.error(`Progress: ${processedCount}/${staleFilesToCheck.length} files processed`);
      process.exit(1);
    }
  }

  console.log('\nParameterization process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
