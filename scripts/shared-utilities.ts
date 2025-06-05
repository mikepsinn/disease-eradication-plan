import * as fs from 'fs';
import * as path from 'path';

// Shared ignore list across multiple scripts
const ignoreList: string[] = [
  '.git',
  'node_modules',
  '.env',
  'package.json',
  'package-lock.json',
  '.gitignore',
  'scripts',
  '.vscode',
  '.idea'
];

// Universal file filtering
function shouldIgnore(filePath: string): boolean {
  return ignoreList.some(ignored => filePath.includes(ignored));
}

// Standardized directory crawler
async function getAllFiles(dir: string, extensions: string[] = []): Promise<string[]> {
  const files: string[] = [];
  const items = fs.readdirSync(dir);

  for (const item of items) {
    const fullPath = path.join(dir, item);
    if (shouldIgnore(fullPath)) continue;

    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      files.push(...await getAllFiles(fullPath, extensions));
    } else if (!extensions.length || extensions.includes(path.extname(fullPath).toLowerCase())) {
      files.push(fullPath);
    }
  }

  return files;
}

export {
  ignoreList,
  shouldIgnore,
  getAllFiles
}; 