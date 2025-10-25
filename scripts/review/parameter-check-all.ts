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

  for (const file of staleFilesToCheck) {
    await parameterizeFileWithLLM(file);
  }

  console.log('\nParameterization process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
