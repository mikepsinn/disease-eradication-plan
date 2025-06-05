import * as fs from 'fs';
import * as path from 'path';

/**
 * Recursively delete empty folders starting from a given directory.
 * @param dirPath - Path to the directory to check.
 */
function deleteEmptyFolders(dirPath: string): void {
  // Check if the directory exists
  if (!fs.existsSync(dirPath)) {
    console.log(`Directory not found: ${dirPath}`);
    return;
  }

  // Read contents of the current directory
  let fileNames = fs.readdirSync(dirPath);

  // Remove empties or recurse into subfolders first
  for (const fileName of fileNames) {
    const currentPath = path.join(dirPath, fileName);
    const stats = fs.statSync(currentPath);

    // If this is a directory, recurse
    if (stats.isDirectory()) {
      deleteEmptyFolders(currentPath);
    }
  }

  // After processing subfolders, get the updated list of entries
  fileNames = fs.readdirSync(dirPath);

  // If the directory is now empty, delete it
  if (fileNames.length === 0) {
    fs.rmdirSync(dirPath);
    console.log(`Deleted empty folder: ${dirPath}`);
  }
}

// Example usage:
// Replace '.' with the actual path of the folder you want to scan
// or use process.argv[2] for a command-line argument
const targetDir = process.argv[2] || '.';
deleteEmptyFolders(targetDir); 