const fs = require('fs');
const path = require('path');
const { shouldIgnore } = require('./shared-utilities');

async function deleteEmptyFolders(startPath) {
  // Get list of files and directories in the current path
  const items = fs.readdirSync(startPath);
  let foldersDeleted = 0;

  for (const item of items) {
    const fullPath = path.join(startPath, item);
    
    // Skip if path should be ignored
    if (shouldIgnore(fullPath)) {
      console.log(`Skipping ignored path: ${fullPath}`);
      continue;
    }

    // Check if it's a directory
    if (fs.statSync(fullPath).isDirectory()) {
      // Recursively process subdirectories first
      foldersDeleted += await deleteEmptyFolders(fullPath);
      
      // After processing subdirectories, check if this directory is now empty
      const remainingItems = fs.readdirSync(fullPath);
      if (remainingItems.length === 0) {
        try {
          fs.rmdirSync(fullPath);
          console.log(`✓ Deleted empty folder: ${fullPath}`);
          foldersDeleted++;
        } catch (error) {
          console.error(`✗ Failed to delete folder ${fullPath}:`, error.message);
        }
      } else {
        console.log(`Keeping non-empty folder: ${fullPath} (${remainingItems.length} items)`);
      }
    }
  }

  return foldersDeleted;
}

async function cleanup() {
  try {
    console.log('Starting empty folder cleanup...\n');
    const startPath = process.cwd();
    const deletedCount = await deleteEmptyFolders(startPath);
    
    console.log('\nCleanup completed!');
    console.log(`Total empty folders deleted: ${deletedCount}`);
  } catch (error) {
    console.error('Cleanup failed:', error);
    process.exit(1);
  }
}

// Run the script
cleanup(); 