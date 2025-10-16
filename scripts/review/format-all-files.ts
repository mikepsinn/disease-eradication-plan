import { getStaleFiles, formatFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Identifying stale files for formatting...');
  const staleFiles = await getStaleFiles('lastFormatted');

  if (staleFiles.length === 0) {
    console.log('All files are up-to-date. No formatting needed.');
    return;
  }

  console.log(`Found ${staleFiles.length} files to format:`);
  for (const file of staleFiles) {
    console.log(`- ${file}`);
  }

  for (const file of staleFiles) {
    try {
      console.log(`\nFormatting ${file} with Gemini 2.5 Pro...`);
      await formatFileWithLLM(file);
      console.log(`Successfully formatted ${file}.`);
    } catch (error) {
      console.error(`Failed to format ${file}:`, error);
    }
  }

  console.log('\nFormatting process complete.');
}

main().catch(err => {
  console.error('An unexpected error occurred:', err);
  process.exit(1);
});
