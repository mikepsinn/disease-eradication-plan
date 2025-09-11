import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { glob } from 'glob';
import ignore from 'ignore';

const workspaceRoot = process.cwd();
const outputFilePath = path.join(workspaceRoot, 'index.md');

interface FileInventory {
  path: string;
  [key: string]: any;
}

async function generateInventory() {
  console.log(`Starting inventory generation within: ${workspaceRoot}`);
  
  const gitignoreContent = await fs.readFile(path.join(workspaceRoot, '.gitignore'), 'utf8').catch(() => '');
  const ig = ignore().add(gitignoreContent);
  ig.add('archive/*');
  
  const allFiles = await glob('**/*.md', { 
    cwd: workspaceRoot,
    nodir: true,
    absolute: true,
   });

  const filteredFiles = allFiles.filter(file => {
    const relativePath = path.relative(workspaceRoot, file);
    return !ig.ignores(relativePath) && relativePath !== 'index.md';
  });

  const inventory: FileInventory[] = [];
  const allFrontmatterKeys = new Set<string>();

  for (const filePath of filteredFiles) {
    let relativePath = path.relative(workspaceRoot, filePath).replace(/\\/g, '/');
    try {
      const fileContent = await fs.readFile(filePath, 'utf8');
      if (!fileContent.trim()) {
        console.log(`Skipping empty file: ${filePath}`);
        continue;
      }
      const { data } = matter(fileContent);

      const inventoryItem: FileInventory = { path: relativePath };
      for (const key in data) {
        inventoryItem[key] = data[key];
        allFrontmatterKeys.add(key);
      }
      inventory.push(inventoryItem);
    } catch (error: any) {
      console.error(`Error processing file ${relativePath}: ${error.message}`);
    }
  }

  inventory.sort((a, b) => a.path.localeCompare(b.path));
  
  let markdownContent = '# Project File Index\n\n';
  markdownContent += 'This document provides a complete inventory of all markdown files in the repository and their frontmatter.\n\n';

  inventory.forEach((item, index) => {
    const linkPath = item.path.replace(/ /g, '%20');
    markdownContent += `### [\`${item.path}\`](./${linkPath})\n`;
    for (const key in item) {
      if (key === 'path' || key === 'editor') continue;
      let value = item[key];
      if (value instanceof Date) {
        value = value.toISOString().split('T')[0];
      }
      if (value) {
        markdownContent += `- **${key}:** ${String(value)}\n`;
      }
    }
    if (index < inventory.length - 1) {
      markdownContent += '\n---\n\n';
    }
  });

  await fs.writeFile(outputFilePath, markdownContent);
  console.log(`Inventory successfully generated at: ${outputFilePath}`);
}

generateInventory().catch(console.error);
