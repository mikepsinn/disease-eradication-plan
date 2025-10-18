import { getStaleFiles, structureCheckFileWithLLM } from './utils';
import dotenv from 'dotenv';
import fs from 'fs/promises';

dotenv.config();

async function getMainChapterFiles(): Promise<string[]> {
  // Read _quarto.yml to get only main chapter files (not appendices)
  const quartoYmlContent = await fs.readFile('_quarto.yml', 'utf-8');
  const chapterPaths: string[] = [];

  const lines = quartoYmlContent.split('\n');
  let inAppendices = false;
  let inChapters = false;

  for (const line of lines) {
    // Check if we're entering chapters section
    if (line.trim() === 'chapters:') {
      inChapters = true;
      continue;
    }

    // Check if we're entering the appendices section
    if (line.trim() === 'appendices:') {
      inAppendices = true;
      inChapters = false;
      continue;
    }

    // Check if we're leaving a section (new top-level key)
    if (!line.startsWith(' ') && !line.startsWith('\t') && line.includes(':')) {
      inChapters = false;
      inAppendices = false;
    }

    // Only collect files from chapters section, not appendices
    if (inChapters && !inAppendices) {
      const match = line.match(/^\s*-\s+(brain\/[^\s]+\.qmd)/);
      if (match) {
        chapterPaths.push(match[1]);
      }
    }
  }

  return chapterPaths;
}

async function main() {
  console.log('Getting main chapter files from _quarto.yml...');

  // Get only main chapter files from _quarto.yml
  const mainChapterFiles = await getMainChapterFiles();
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
