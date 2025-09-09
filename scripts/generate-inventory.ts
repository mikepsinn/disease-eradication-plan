import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';

const workspaceRoot = process.cwd(); // Correctly use the current working directory
const outputFilePath = path.join(workspaceRoot, 'operations', 'refactoring_inventory.md');
const ignoreDirs = ['node_modules', '.git', '.vscode', '.idea', 'mcp_server'];

async function getAllMarkdownFiles(dir: string): Promise<string[]> {
  let files = await fs.readdir(dir, { withFileTypes: true });
  let markdownFiles: string[] = [];
  for (const file of files) {
    const fullPath = path.join(dir, file.name);
    if (file.isDirectory()) {
      if (!ignoreDirs.includes(file.name)) {
        markdownFiles = markdownFiles.concat(await getAllMarkdownFiles(fullPath));
      }
    } else if (file.name.endsWith('.md')) {
      markdownFiles.push(fullPath);
    }
  }
  return markdownFiles;
}

interface FileInventory {
  path: string;
  title: string;
  description: string;
}

async function generateInventory() {
  console.log(`Starting inventory generation within: ${workspaceRoot}`);
  const allFiles = await getAllMarkdownFiles(workspaceRoot);
  const inventory: FileInventory[] = [];

  for (const filePath of allFiles) {
    try {
      const fileContent = await fs.readFile(filePath, 'utf8');
      if (!fileContent.trim()) {
        console.log(`Skipping empty file: ${filePath}`);
        continue;
      }
      const { data } = matter(fileContent);

      const relativePath = path.relative(workspaceRoot, filePath).replace(/\\/g, '/');
      
      const description = data.description ? String(data.description) : 'No Description';

      inventory.push({
        path: relativePath,
        title: data.title || 'No Title',
        description: description,
      });
    } catch (error: any) {
      console.error(`Error processing file ${relativePath}: ${error.message}`);
    }
  }

  inventory.sort((a, b) => a.path.localeCompare(b.path));
  
  let markdownContent = '# Wiki Content Inventory\n\n';
  markdownContent += 'This document provides a complete inventory of all markdown files in the repository, including their titles and descriptions, to aid in the restructuring process.\n\n';
  markdownContent += '| File Path | Title | Description |\n';
  markdownContent += '|---|---|---|\n';

  inventory.forEach(item => {
    const descriptionText = item.description || '';
    markdownContent += `| ${item.path} | ${item.title} | ${descriptionText.replace(/\r?\n|\r/g, ' ')} |\n`;
  });

  await fs.writeFile(outputFilePath, markdownContent);
  console.log(`Inventory successfully generated at: ${outputFilePath}`);
}

generateInventory().catch(console.error);
