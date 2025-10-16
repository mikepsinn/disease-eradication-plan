import path from 'path';
import { formatFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Please provide a file path to format.');
    process.exit(1);
  }

  const absolutePath = path.resolve(filePath);
  try {
    console.log(`Formatting ${absolutePath} with Gemini 2.5 Pro...`);
    await formatFileWithLLM(absolutePath);
    console.log('Formatting complete.');
  } catch (error) {
    console.error(`Failed to format ${absolutePath}:`, error);
    process.exit(1);
  }
}

main();
