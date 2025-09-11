import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { glob } from 'glob';

const workspaceRoot = process.cwd();
const outputFilePath = path.join(workspaceRoot, 'index.md');

async function getGitignorePatterns(): Promise<string[]> {
    try {
        const gitignoreContent = await fs.readFile(path.join(workspaceRoot, '.gitignore'), 'utf8');
        return gitignoreContent.split('\n').filter(line => line.trim() !== '' && !line.startsWith('#'));
    } catch (error) {
        console.warn('Could not read .gitignore, proceeding without it.');
        return [];
    }
}

interface FileInventory {
  path: string;
  [key: string]: any;
}

async function generateInventory() {
  console.log(`Starting inventory generation within: ${workspaceRoot}`);
  const gitignorePatterns = await getGitignorePatterns();
  const ignorePatterns = [...gitignorePatterns, 'archive/**', 'index.md'];

  const allFiles = await glob('**/*.md', { 
    cwd: workspaceRoot,
    ignore: ignorePatterns,
    nodir: true,
    absolute: true,
   });

  const inventory: FileInventory[] = [];
  const allFrontmatterKeys = new Set<string>();

  for (const filePath of allFiles) {
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
