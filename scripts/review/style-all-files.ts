import { getStaleFiles, styleFileWithLLM } from './utils';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('Identifying stale files for style review...');
  
  try {
    const staleFiles = await getStaleFiles('lastStyleHash');
    const bookFiles = staleFiles.filter(file => file.startsWith('brain\\book'));
    
    if (bookFiles.length === 0) {
      console.log('No stale files to review. All content is up to date.');
      return;
    }

    console.log(`Found ${bookFiles.length} files in brain/book to review for style:\n`);
    for (const file of bookFiles) {
      try {
        await styleFileWithLLM(file);
      } catch (error) {
        console.error(`Failed to process ${file}:`, error);
      }
    }
    console.log('\nStyle review complete for all stale files.');
  } catch (error) {
    console.error('An error occurred during the style review process:', error);
    process.exit(1);
  }
}

main();
