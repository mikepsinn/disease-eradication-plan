import fs from 'fs-extra';
import path from 'path';

const projectRoot = process.cwd();
const sourceDir = path.join(projectRoot, 'GUIDES');
const destDir = path.join(projectRoot, '.clinerules');

async function copyGuides() {
  try {
    console.log(`Copying GUIDES from ${sourceDir} to ${destDir}...`);
    // ensureDir creates a directory if it does not exist.
    await fs.ensureDir(path.dirname(destDir));
    // Remove existing contents to ensure a clean copy
    if (await fs.pathExists(destDir)) {
      console.log(`Removing existing contents from ${destDir}...`);
      await fs.remove(destDir);
    }
    await fs.copy(sourceDir, destDir, { overwrite: true });
    console.log(`Successfully copied GUIDES to ${destDir}.`);
  } catch (err) {
    console.error('Error copying GUIDES:', err);
    process.exit(1);
  }
}

copyGuides();
