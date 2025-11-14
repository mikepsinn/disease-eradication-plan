import fs from 'fs';
import path from 'path';

const ignoredDirs = new Set(['node_modules', '.git', '.github', '.vscode']);

async function deleteEmptyFolders(directory: string): Promise<void> {
  const files = await fs.promises.readdir(directory);
  if (files.length > 0) {
    for (const file of files) {
      const fullPath = path.join(directory, file);
      if (ignoredDirs.has(file)) {
        console.log(`- Ignoring ${fullPath}`);
        continue;
      }
      const stat = await fs.promises.lstat(fullPath);
      if (stat.isDirectory()) {
        await deleteEmptyFolders(fullPath);
      }
    }
  }

  const remainingFiles = await fs.promises.readdir(directory);
  if (remainingFiles.length === 0) {
    console.log(`- Deleting empty directory: ${directory}`);
    await fs.promises.rmdir(directory);
  }
}

const projectRoot = process.cwd();
console.log(`Starting cleanup in: ${projectRoot}`);

deleteEmptyFolders(projectRoot)
  .then(() => console.log('Cleanup complete.'))
  .catch(err => console.error('Error during cleanup:', err));
