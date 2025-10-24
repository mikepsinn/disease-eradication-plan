import { glob } from 'glob';
import { latexCheckFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Starting LaTeX check for all .qmd files...');

  const allQmdFiles = await glob('brain/book/**/*.qmd');
  const excludedFile = 'brain/book/references.qmd';

  const filesToCheck = allQmdFiles.filter(file => !file.includes(excludedFile));

  console.log(`Found ${filesToCheck.length} .qmd files to check for LaTeX usage (after exclusions).`);

  if (filesToCheck.length === 0) {
    console.log('No .qmd files found to check.');
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
