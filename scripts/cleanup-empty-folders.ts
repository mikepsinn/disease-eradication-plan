import * as fs from 'fs';
import * as path from 'path';
// Assuming shared-utilities is converted to TypeScript
import { shouldIgnore } from './shared-utilities';

/**
 * Recursively deletes empty folders starting from a given path.
 * @param startPath The directory path to start cleaning up from.
 * @returns The total number of folders deleted.
 */
async function deleteEmptyFolders(startPath: string): Promise<number> {
  let items: fs.Dirent[];
  try {
    // Get list of files and directories in the current path
    items = fs.readdirSync(startPath, { withFileTypes: true });
  } catch (error) {
    console.error(`Error reading directory ${startPath}:`, error);
    return 0; // Return 0 deleted folders if directory can't be read
  }

  let foldersDeleted = 0;

  for (const item of items) {
    const fullPath = path.join(startPath, item.name);

    // Skip if path should be ignored
    if (shouldIgnore(fullPath)) {
      console.log(`Skipping ignored path: ${fullPath}`);
      continue;
    }

    try {
      // Check if it's a directory
      if (item.isDirectory()) {
        // Recursively process subdirectories first
        foldersDeleted += await deleteEmptyFolders(fullPath);

        // After processing subdirectories, check if this directory is now empty
        const remainingItems = fs.readdirSync(fullPath);
        if (remainingItems.length === 0) {
          try {
            fs.rmdirSync(fullPath);
            console.log(`✓ Deleted empty folder: ${fullPath}`);
            foldersDeleted++;
          } catch (error: any) {
            console.error(`✗ Failed to delete folder ${fullPath}:`, error.message);
          }
        } else {
          console.log(`Keeping non-empty folder: ${fullPath} (${remainingItems.length} items)`);
        }
      }
      // If it's a file, just continue (no action needed for files)
    } catch (error) {
      // Catch errors during fs.statSync implicitly used by item.isDirectory()
      console.error(`Error processing item ${fullPath}:`, error);
    }
  }

  return foldersDeleted;
}

/**
 * Main cleanup function.
 */
async function cleanup(): Promise<void> {
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