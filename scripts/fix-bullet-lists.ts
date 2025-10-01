import { glob } from 'glob';
import fs from 'fs/promises';
import path from 'path';

async function fixBulletLists() {
  const markdownFiles = await glob('**/*.{qmd,md}', {
    ignore: 'node_modules/**',
  });

  for (const file of markdownFiles) {
    try {
      const filePath = path.resolve(file);
      const content = await fs.readFile(filePath, 'utf-8');
      
      // Regex to find a line that is not a list item, followed by a line that is a list item
      // It looks for a line that doesn't start with whitespace and a list marker,
      // followed by a line that does.
      const updatedContent = content.replace(
        /(^[^\s\-\*\+].*)\r?\n(^\s*[\-\*\+]\s.*)/gm,
        '$1\n\n$2'
      );

      if (content !== updatedContent) {
        await fs.writeFile(filePath, updatedContent, 'utf-8');
        console.log(`Fixed bullet lists in: ${file}`);
      }
    } catch (error) {
      console.error(`Error processing file ${file}:`, error);
    }
  }
}

fixBulletLists().catch(console.error);
