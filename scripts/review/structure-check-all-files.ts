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

  // Files to exclude from structure checking:
  // - references.qmd: Reference list, not a narrative chapter
  // - Part intro files: These are meant to summarize their child chapters
  const excludedFiles = [
    'brain/book/references.qmd',
    'brain/book/problem.qmd',     // Part I: The Problem intro
    'brain/book/solution.qmd',    // Part II: The Solution intro
    'brain/book/proof.qmd',       // Part III: The Case intro
    'brain/book/economics.qmd',   // The Economic Case intro
    'brain/book/futures.qmd',     // Intro to Paths
    'brain/book/strategy.qmd',    // Strategy section intro
  ];

  // Filter to only include main chapter files that are stale
  // Normalize paths to use forward slashes for comparison (cross-platform)
  const staleFilesToCheck = allStaleFiles.filter(file => {
    const normalizedFile = file.replace(/\\/g, '/');

    // Check if file is in exclusion list
    if (excludedFiles.some(excluded => normalizedFile.includes(excluded))) {
      return false;
    }

    return mainChapterFiles.some(chapterPath => normalizedFile.includes(chapterPath));
  });

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
