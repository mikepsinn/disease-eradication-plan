import {
  getStaleFiles,
  formatFileWithLLM,
  styleFileWithLLM,
  factCheckFileWithLLM,
  linkCheckFile,
  figureCheckFile,
  structureCheckFileWithLLM
} from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Starting comprehensive review process...');

  const checks = [
    { name: 'Structure Check', hashField: 'lastStructureCheckHash', checkFunction: structureCheckFileWithLLM }, // Run FIRST to remove/consolidate content
    { name: 'Formatting', hashField: 'lastFormattedHash', checkFunction: formatFileWithLLM },
    { name: 'Style & Content Quality', hashField: 'lastStyleHash', checkFunction: styleFileWithLLM },
    { name: 'Fact Check', hashField: 'lastFactCheckHash', checkFunction: factCheckFileWithLLM },
    { name: 'Link Check', hashField: 'lastLinkCheckHash', checkFunction: linkCheckFile },
    { name: 'Figure Check', hashField: 'lastFigureCheckHash', checkFunction: figureCheckFile }
  ];

  for (const check of checks) {
    console.log(`\n--- Running ${check.name} Check ---`);
    const staleFiles = await getStaleFiles(check.hashField);
    const bookFiles = staleFiles.filter(file => file.startsWith('brain\\book'));

    if (bookFiles.length === 0) {
      console.log(`All files are up-to-date for ${check.name}.`);
      continue;
    }

    console.log(`Found ${bookFiles.length} files needing a ${check.name.toLowerCase()} review.`);
    for (const file of bookFiles) {
      await check.checkFunction(file);
    }
  }

  console.log('\nComprehensive review process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred during the review process:', err);
  process.exit(1);
});
