import { getStaleFiles, nonprofitComplianceCheckFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Checking dih-economic-models files for nonprofit foundation compliance...');

  const staleFilesToCheck = await getStaleFiles('lastNonprofitComplianceHash', 'dih-economic-models');

  console.log(`\nFound ${staleFilesToCheck.length} stale files in dih-economic-models to review\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All files in dih-economic-models are up-to-date!');
    return;
  }

  console.log('Reviewing the following files for foundation compliance:');
  staleFilesToCheck.forEach(file => console.log(`  - ${file}`));

  let processedCount = 0;
  for (const file of staleFilesToCheck) {
    processedCount++;
    const percent = Math.round((processedCount / staleFilesToCheck.length) * 100);

    try {
      console.log(`\n[${processedCount}/${staleFilesToCheck.length}] (${percent}%) Reviewing: ${file}...`);
      await nonprofitComplianceCheckFileWithLLM(file);
    } catch (error) {
      console.error(`\n❌ FATAL ERROR reviewing ${file}:`, error);
      console.error('\nStopping script due to error.');
      console.error(`Progress: ${processedCount}/${staleFilesToCheck.length} files processed`);
      process.exit(1);
    }
  }
  console.log('\nNonprofit compliance review complete for all stale files.');
}

main().catch(error => {
  console.error('An error occurred during the compliance review process:', error);
  process.exit(1);
});
