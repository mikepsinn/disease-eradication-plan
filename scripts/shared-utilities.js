const fs = require('fs');
const path = require('path');

// Shared ignore list across multiple scripts
const ignoreList = [
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
function shouldIgnore(filePath) {
  return ignoreList.some(ignored => filePath.includes(ignored));
}

// Standardized directory crawler
async function getAllFiles(dir, extensions = []) {
  const files = [];
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

module.exports = {
  ignoreList,
  shouldIgnore,
  getAllFiles
}; 