import { analyzeArchivedFile } from './utils';
import { glob } from 'glob';
import fs from 'fs';

async function main() {
  const archiveDir = 'archive';
  if (!fs.existsSync(archiveDir)) {
    console.error(`Error: Directory not found at ${archiveDir}`);
    process.exit(1);
  }

  const markdownFiles = await glob(`${archiveDir}/**/*.md`);

  if (markdownFiles.length === 0) {
    console.log('No markdown files found in the archive directory.');
    return;
  }

  console.log(`Found ${markdownFiles.length} markdown files to process.`);

  for (const filePath of markdownFiles) {
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
