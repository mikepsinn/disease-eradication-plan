import { getStaleFiles, styleFileWithLLM } from './utils';

async function main() {
  console.log('Identifying stale files for style review...');
  
  try {
    const staleFiles = await getStaleFiles('lastStyleHash');
    
    if (staleFiles.length === 0) {
      console.log('No stale files to review. All content is up to date.');
      return;
    }

    console.log(`Found ${staleFiles.length} files to review for style:\n`);
    for (const file of staleFiles) {
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
