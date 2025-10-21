import { analyzeArchivedFile } from './utils';
import fs from 'fs';

async function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Please provide a file path as an argument.');
    process.exit(1);
  }

  if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found at ${filePath}`);
    process.exit(1);
  }

  try {
    await analyzeArchivedFile(filePath);
    console.log(`\nFinished processing ${filePath}.`);
  } catch (error) {
    console.error(`An error occurred while processing ${filePath}:`, error);
    process.exit(1);
  }
}

main();
