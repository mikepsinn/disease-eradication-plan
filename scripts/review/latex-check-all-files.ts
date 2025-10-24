import { latexCheckFileWithLLM } from './utils';
import { getBookFiles } from '../lib/file-utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Starting LaTeX check for all book files...');

  const filesToCheck = await getBookFiles({ includeAppendices: true });

  console.log(`Found ${filesToCheck.length} book files to check for LaTeX usage.`);

  if (filesToCheck.length === 0) {
    console.log('No files found to check.');
    return;
  }

  console.log('Checking the following files for proper LaTeX usage:');
  filesToCheck.forEach(file => console.log(`  - ${file}`));

  for (const file of filesToCheck) {
    await latexCheckFileWithLLM(file);
  }

  console.log('\nLaTeX checking process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred during the LaTeX check process:', err);
  process.exit(1);
});
