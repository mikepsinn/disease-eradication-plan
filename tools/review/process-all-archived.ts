import { analyzeArchivedFile } from './utils';
import { glob } from 'glob';
import path from 'path';

async function main() {
  const archiveDir = path.join(process.cwd(), 'archive');
  const files = await glob('**/*.md', { cwd: archiveDir, absolute: true });

  if (files.length === 0) {
    console.log('No markdown files found in the archive directory.');
    return;
  }

  console.log(`Found ${files.length} markdown files to process.`);

  for (const file of files) {
    console.log(`\n--- Processing ${file} ---`);
    await analyzeArchivedFile(file);
  }

  console.log('\n--- All files processed. ---');
}

main().catch(error => {
  console.error('An unexpected error occurred:', error);
  process.exit(1);
});
