import { getStaleFiles, structureCheckFileWithLLM, parseQuartoYml } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Getting main chapter files from _quarto.yml...');

  // Get only main chapter files from _quarto.yml using the reusable function
  const { chapters: mainChapterFiles } = await parseQuartoYml();
  console.log(`Found ${mainChapterFiles.length} main chapter files (excluding appendices)`);

  // Get stale files that need checking
  const allStaleFiles = await getStaleFiles('lastStructureCheckHash', 'brain/book');

  // Filter to only include main chapter files that are stale
  const staleFilesToCheck = allStaleFiles.filter(file =>
    mainChapterFiles.some(chapterPath => file.includes(chapterPath))
  );

  console.log(`\nFound ${staleFilesToCheck.length} stale MAIN CHAPTER files to structure-check\n`);

  if (staleFilesToCheck.length === 0) {
    console.log('All main chapter files are up-to-date!');
    return;
  }

  console.log('Structure-checking the following files:');
  staleFilesToCheck.forEach(file => console.log(`  - ${file}`));

  for (const file of staleFilesToCheck) {
    await structureCheckFileWithLLM(file);
  }

  console.log('\nStructure-checking process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
