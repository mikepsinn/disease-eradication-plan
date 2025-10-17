import { figureCheckFile } from './utils';
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
    await figureCheckFile(filePath);
    console.log('\nFigure check complete.');
  } catch (error) {
    console.error('An error occurred during the figure-checking process:', error);
    process.exit(1);
  }
}

main();
