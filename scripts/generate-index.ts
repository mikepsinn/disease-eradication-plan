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

  const sortedFrontmatterKeys = Array.from(allFrontmatterKeys).sort();
  
  let markdownContent = '# Project File Index\n\n';
  markdownContent += 'This document provides a complete inventory of all markdown files in the repository and their frontmatter.\n\n';
  
  const headers = ['File Path', ...sortedFrontmatterKeys];
  markdownContent += `| ${headers.join(' | ')} |\n`;
  markdownContent += `|${headers.map(() => '---').join('|')}|\n`;

  inventory.forEach(item => {
    const row = [item.path, ...sortedFrontmatterKeys.map(key => {
      const value = item[key];
      if (value === null || value === undefined) {
        return '';
      }
      const stringValue = String(value);
      return stringValue.replace(/\r?\n|\r/g, ' ');
    })];
    markdownContent += `| ${row.join(' | ')} |\n`;
  });

  await fs.writeFile(outputFilePath, markdownContent);
  console.log(`Inventory successfully generated at: ${outputFilePath}`);
}

generateInventory().catch(console.error);
