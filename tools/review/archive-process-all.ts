import { analyzeArchivedFile } from './utils';
import { glob } from 'glob';
import fs from 'fs';
import path from 'path';

async function main() {
  const archiveDirs = [
    'archive',
    'C:\\code\\dFDA-whitepaper'
  ];

  const allMarkdownFiles: string[] = [];

  for (const archiveDir of archiveDirs) {
    if (!fs.existsSync(archiveDir)) {
      console.warn(`Warning: Directory not found at ${archiveDir}, skipping...`);
      continue;
    }

    const markdownFiles = await glob(`${archiveDir}/**/*.md`, {
      windowsPathsNoEscape: true
    });

    console.log(`Found ${markdownFiles.length} markdown files in ${archiveDir}`);
    allMarkdownFiles.push(...markdownFiles);
  }

  if (allMarkdownFiles.length === 0) {
    console.log('No markdown files found in any archive directories.');
    return;
  }

  console.log(`\nTotal: ${allMarkdownFiles.length} markdown files to process.\n`);

  for (const filePath of allMarkdownFiles) {
    console.log(`\n--- Processing ${filePath} ---`);
    await analyzeArchivedFile(filePath);
    console.log(`--- Finished processing ${filePath} ---`);
  }

  console.log('\nArchive processing complete.');
}

main().catch(error => {
  console.error('An unexpected error occurred:', error);
  process.exit(1);
});
