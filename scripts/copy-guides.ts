import fs from 'fs-extra';
import path from 'path';
import os from 'os';

const projectRoot = process.cwd();
const sourceDir = path.join(projectRoot, 'GUIDES');
// Per your custom instructions, the global .clinerules directory is located here.
// A subdirectory with the project's name is used to prevent conflicts.
const destDir = path.join(os.homedir(), 'OneDrive', 'Documents', 'Cline', 'Rules', 'decentralized-institutes-of-health', 'GUIDES');

async function copyGuides() {
  try {
    console.log(`Copying GUIDES from ${sourceDir} to ${destDir}...`);
    // ensureDir creates a directory if it does not exist.
    await fs.ensureDir(path.dirname(destDir));
    await fs.copy(sourceDir, destDir, { overwrite: true });
    console.log(`Successfully copied GUIDES to ${destDir}.`);
  } catch (err) {
    console.error('Error copying GUIDES:', err);
    process.exit(1);
  }
}

copyGuides();
