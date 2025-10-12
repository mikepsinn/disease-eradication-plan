import fs from 'fs';
import path from 'path';
import { glob } from 'glob';

// Find all .qmd files
const qmdFiles = await glob('**/*.qmd', {
  ignore: ['node_modules/**', '**/node_modules/**', '_book/**']
});

const titles = [];

qmdFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');

  // Extract frontmatter
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);

  if (frontmatterMatch) {
    const frontmatter = frontmatterMatch[1];

    // Extract title (handle both quoted and unquoted)
    const titleMatch = frontmatter.match(/^title:\s*(.+?)$/m);

    if (titleMatch) {
      let title = titleMatch[1].trim();
      // Remove quotes if present
      title = title.replace(/^["']|["']$/g, '');
      titles.push({
        file,
        title,
        length: title.length
      });
    }
  }
});

// Sort by length (longest first)
titles.sort((a, b) => b.length - a.length);

// Print results
console.log('\n=== QMD File Titles Ranked by Length ===\n');
console.log('Rank | Length | Title | File');
console.log('-----|--------|-------|-----');

titles.forEach((item, index) => {
  console.log(`${(index + 1).toString().padStart(4)} | ${item.length.toString().padStart(6)} | ${item.title} | ${item.file}`);
});

console.log(`\nTotal files analyzed: ${titles.length}`);
console.log(`Average title length: ${Math.round(titles.reduce((sum, t) => sum + t.length, 0) / titles.length)} characters`);
console.log(`Longest: ${titles[0].length} characters`);
console.log(`Shortest: ${titles[titles.length - 1].length} characters`);
